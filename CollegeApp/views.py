from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from staff.models import Staff
from student.models import Student
from .models import *
from CollegeApp.models import *

from .forms import AddressForm, BankForm, CollegeRegisterForm

import logging

logger = logging.getLogger(__name__)

def home(request):
    template_name = "College/index.html"
    return render(request, template_name=template_name)
    
def get_states(request):
    states = list(State.objects.all().values('id', 'name'))
    return JsonResponse(states, safe=False)

def get_districts(request):
    state_id = request.GET.get('state_id')
    if state_id:
        try:
            districts = District.objects.filter(state_id=state_id).values('id', 'district')
            return JsonResponse({"districts": list(districts)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({'districts': []})

def get_subject_combination(request):
    program_id = request.GET.get('program_id')
    if program_id:
        try:
            combinations = SubjectCombination.objects.filter(program_id=program_id).values('id', 'combination_short_form', 'combination_full_form')
            return JsonResponse({"combinations":list(combinations)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"combinations":[]})

def register_college(request):
    if request.method == 'POST':
        form = CollegeRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # Form errors will be passed to the template
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = CollegeRegisterForm()
    context = {'form':form}
    return render(request, 'registration/register.html', context)

@login_required
def dashboard(request):
    # Retrieve college_code from the session
    user = request.user
    if user.is_staff:
        colleges = College.objects.all().order_by('created_at')
        context = {'colleges': colleges,}
    else:
        college = get_object_or_404(College, college_email=user.email) # Fetch the college instance
        request.session['college_code'] = college.college_code  # Set college_code in session

        # Use annotate to count teaching staff efficiently
        college = College.objects.annotate(total_staff=Count('staff'),
                                           teaching_staff_count=Count('staff',filter=Q(staff__staff_type='Teaching')),
                                           non_teaching_staff_count=Count('staff', filter=Q(staff__staff_type='Non Teaching')),
                                           working_staff_count=Count('staff', filter=Q(staff__status='Working')),
                                           transferred_staff_count=Count('staff', filter=Q(staff__status='Transferred')),
                                           departed_staff_count=Count('staff', filter=Q(staff__status='Departed')),

                                           total_students_count=Count('student'),
                                           ongoing_students_count=Count('student',filter=Q(student__status='OnGoing')),
                                           graduate_students_count=Count('student',filter=Q(student__status='Graduate')),
                                           dropout_students_count=Count('student',filter=Q(student__status='DropOut')),
                                           ).get(id=college.id)

        # total_staff = Staff.objects.filter(college=college.id).count()
        # teaching_staff = Staff.objects.filter(college=college.id,staff_type='Teaching').count()
        # non_teaching_staff = Staff.objects.filter(college=college.id,staff_type='Non Teaching').count()

        # total_students = Student.objects.filter(college=college.id).count()
        context = {'college': college,
                #    'total_staff':total_staff,
                #    'teaching_staff':teaching_staff,
                #    'non_teaching_staff':non_teaching_staff,
                #    'total_students':total_students
                   }
    # Render the template with context
    return render(request, 'dashboard.html', context=context)
    
def medium(request,medium):
    medium_id = get_object_or_404(Medium,medium=medium)
    # medium_id = Medium.objects.filter(medium=medium)


@login_required
def manage_address_details(request, entity_type, id):
    """
    Generic function to manage address details for students and staff.

    Args:
        request: The HTTP request object.
        entity_type (str): Type of entity ('student' or 'staff').
        id (int): ID of the student or staff.
    """
    # Determine the model based on entity_type
    if entity_type == "student":
        entity = get_object_or_404(Student, id=id)
    elif entity_type == "staff":
        entity = get_object_or_404(Staff, id=id)
    else:
        messages.error(request, "Invalid entity type provided.")
        return redirect('home')  # Redirect to a valid page

    # Fetch existing address details or create a new Address instance
    address_details = entity.address if hasattr(entity, 'address') and entity.address else Address()
    # print(entity,entity_type)
    if request.method == 'POST':        
        form = AddressForm(request.POST, instance=address_details)
        if form.is_valid():
            print(entity)
            address = form.save()
            entity.address = address  # Link address to the student or staff
            entity.save()
            messages.success(request, f"Address details updated successfully for {entity_type}.")
            logger.info(f"Address details updated for {entity_type} {entity.id} by user {request.user.id}.")
            return redirect('manage_bank_details', entity_type=entity_type, id=entity.id)  # Adjust redirect as needed
        else:
            messages.error(request, f"Failed to update address details for {entity_type}. Please fix the errors below.")
            logger.error(f"Address form errors for {entity_type} {entity.id}: {form.errors}")
    else:
        form = AddressForm(instance=address_details)
        states = State.objects.all()
    
    context = {
        'address_form': form,
        'states': states,
        'entity': entity,
        'entity_type': entity_type,  # Helps in templates to distinguish student/staff
    }

    return render(request, 'College/components/add_address.html', context)

@login_required
def manage_bank_details(request, entity_type, id):
    # Determine the model based on entity_type
    if entity_type == "student":
        entity = get_object_or_404(Student, id=id)
        success_page = redirect('student_view', id=entity.id)
    elif entity_type == "staff":
        entity = get_object_or_404(Staff, id=id)
        success_page = redirect('view_staff', id=entity.id)
    else:
        messages.error(request, "Invalid entity type provided.")
        return redirect('home')  # Redirect to a valid page

    # Fetch existing bank details or create a new Bank instance
    bank_details = entity.bank if hasattr(entity, 'bank') and entity.bank else Bank_details()

    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank_details)
        if form.is_valid():
            # Save the bank details
            bank = form.save()
            entity.bank = bank  # Link bank details to the entity
            entity.save()

            messages.success(request, "Bank details updated successfully.")
            logger.info(f"Bank details updated for {entity_type} {entity.id} by user {request.user.id}.")
     
            return success_page
        else:
            messages.error(request, "Failed to update bank details. Please fix the errors below.")
            logger.error(f"Bank form errors for {entity_type} {entity.id}: {form.errors}")
    # Prepopulate the form with existing data for GET request
    form = BankForm(instance=bank_details)

    context = {
        'bank_form': form,
        'entity': entity,
        'entity_type': entity_type,
    }
    return render(request, 'College/components/add_bank.html', context)

