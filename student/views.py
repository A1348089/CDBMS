from asyncio.log import logger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

import logging

import pandas as pd
from django.urls import reverse
from django.db.models import Q

from .forms import StudentFilterForm, StudentForm, ParentForm

from .models import Parent, Student
from CollegeApp.models import College, Program
# Create your views here.

# Create student view
# Setup logger
logger = logging.getLogger(__name__)

@login_required
def create_student(request):
    user = request.user

    if request.method == "POST":
        try:
            # Fetch the associated college for the logged-in user
            college = College.objects.get(user=user)
        except ObjectDoesNotExist:
            messages.error(request, "You need to associate with a college to add a student.")
            logger.warning(f"College not found for user {user.id} ({user.username}).")
            return redirect('dashboard')

        # Initialize form with POST data
        student_form = StudentForm(request.POST, request.FILES)

        if student_form.is_valid():
            # Create Student instance
            student = student_form.save(commit=False)
            student.college = college
            student.save()  # Save the student

            messages.success(request, "Student record created successfully.")
            logger.info(f"Student record created for {student.id} by user {user.id}.")

            # Redirect to add parents details
            return redirect(reverse('manage_student_parent_details', kwargs={'id': student.id}))
        else:
            messages.error(request, "Failed to create Student record. Please fix the errors below.")
            logger.error(f"Student form errors for user {user.id}: {student_form.errors}")

    # For GET request: Initialize empty forms
    student_form = StudentForm()
    programs = Program.objects.all()
    context = {
        'student_form': student_form,
        'programs': programs,
    }
    return render(request, 'College/student/create_student.html', context)

@login_required
def manage_student_parent_details(request,id):
    # Fetch the student based on the id extracted from the URL
    student = get_object_or_404(Student, id=id)

    # Fetch existing bank details or create a blank instance
    parent_details = student.parent if student.parent else Parent()
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent_details)
        if form.is_valid():
            # Save the bank details
            parents = form.save()
            student.parent = parents  # Link bank details to the student
            student.save()

            messages.success(request, "Parents details updated successfully.")
            logger.info(f"Parents details updated for student {student.first_name} {student.last_name} by user {request.user.id}.")
            return redirect('manage_address_details', entity_type="student", id=student.id)  # Adjust redirect as needed
        else:
            messages.error(request, "Failed to update Parents details. Please fix the errors below.")
            logger.error(f"Parents form errors for student {student.id}: {form.errors}")
    else:
        # Prepopulate the form with existing data for GET request
        form = ParentForm(instance=parent_details)

    context = {
        'parent_form': form,
        'student': student,
    }
    return render(request, 'College/components/add_parents.html', context)
from django.core.paginator import Paginator

def student_list(request):
    user = request.user
    try:
        # Get the college associated with the logged-in user
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        messages.error(request, "You are not associated with any college.")
        return redirect('error_page')  # Customize this redirect as needed

    form = StudentFilterForm(request.GET or None)
    
    # Add a default ordering (e.g., by 'id' or 'first_name')
    students = Student.objects.filter(college=college).order_by('id')  

    if request.method == "GET" and form.is_valid():
        filters = {
            'college': college,
            'year_of_admission': form.cleaned_data.get('academic_year'),
            'status': form.cleaned_data.get('status'),
            'gender': form.cleaned_data.get('gender'),
            'address__state': form.cleaned_data.get('state'),
            'address__district': form.cleaned_data.get('district'),
            'program': form.cleaned_data.get('program'),
            'subject_combination': form.cleaned_data.get('group'),
            'medium': form.cleaned_data.get('medium'),
        }
        # Apply filters
        filters = {key: value for key, value in filters.items() if value}
        students = Student.objects.filter(**filters).order_by('OAMDC_NO')  # Add order_by here as well

    paginator = Paginator(students, 50)  # Show 10 students per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,  # Fix: Removed extra space in dictionary key
        'college':college,
    }
    return render(request, 'College/student/students_list.html', context)

from .serializers import StudentSerializer

@login_required
def search_students(request):
    user = request.user
    try:
        # Get the college associated with the logged-in user
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        messages.error(request, "You are not associated with any college.")
        return redirect('error_page')  # Customize this redirect as needed

    query = request.GET.get('query', '').strip()

    if not query:
        print('no query')
        return JsonResponse({'error': 'No search query provided'}, status=400)

    students = Student.objects.filter(
       Q(college=college) & Q(OAMDC_NO__iexact=query) | Q(mobile_no__iexact=query)
    )

    serialized_data = StudentSerializer(students, many=True).data
    return JsonResponse({'students': serialized_data}, safe=False)

@login_required
def download_students_excel(request):
    user = request.user
    try:
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        return HttpResponse("Unauthorized", status=401)

    form = StudentFilterForm(request.GET or None)

    students = Student.objects.filter(college=college).order_by('OAMDC_NO')

    if form.is_valid():
        filters = {
            'college': college,
            'year_of_admission': form.cleaned_data.get('academic_year'),
            'status': form.cleaned_data.get('status'),
            'gender': form.cleaned_data.get('gender'),
            'address__state': form.cleaned_data.get('state'),
            'address__district': form.cleaned_data.get('district'),
            'program': form.cleaned_data.get('program'),
            'subject_combination': form.cleaned_data.get('group'),
            'medium': form.cleaned_data.get('medium'),
        }
        filters = {key: value for key, value in filters.items() if value}
        students = students.filter(**filters)

    # Get selected columns from request
    selected_columns = request.GET.getlist('columns')

    # Define column mapping
    column_mapping = {
        'OAMDC_NO': 'OAMDC No',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'mobile_no': 'Mobile No',
        'email': 'Email',
        'gender': 'Gender',
        'date_of_birth': 'Date of Birth',
        'program__program_full_name': 'Program',
        'program__program_short_name': 'Program',
        'subject_combination__combination_full_form': 'Subject Combination',
        'subject_combination__combination_short_form': 'Subject Combination',
        'status': 'Status',
        'year_of_admission':'Academic year',

        'bank__bank_account_num': 'Account No',
        'bank__bank_name__bank':'Bank Name',
        'bank__ifsc_code': 'IFSC',
        'bank__branch_name': 'Branch',

        'address__doorNo': 'Door No',
        'address__village':'Village/Town',
        'address__street':'street',
        'address__mandal':'Mandal',
        'address__district__district':'District',
        'address__state__name':'State',
        'address__pin_code':'PinCode',

        
        'aadhar_no': 'Aadhar',
        'caste':'Cast',
        'caste_certificate_no':'Cast Certificate No',
        'income_certificate_no': 'Income Certificate No',

        'ssc_hall_ticket': 'SSC Hall Ticket No',
        'ssc_school_name': 'SSC School Name',
        'ssc_year_of_study': 'SSC year',
        'ssc_marks': 'SSC Marks',

        'intermediate_hall_ticket_no': '12th Hallticket No',
        'intermediate_college_name': '12th College Name',
        'intermediate_year_of_study': '12th completion year',
        'intermediate_marks': '12th Marks',
    }

    # Filter selected columns
    selected_column_keys = [key for key in column_mapping if key in selected_columns]

    # If no columns are selected, return all
    if not selected_column_keys:
        selected_column_keys = list(column_mapping.keys())

    # Fetch student data based on selected columns
    student_data = students.values(*selected_column_keys)

    # Convert to DataFrame
    df = pd.DataFrame(list(student_data))

    # Rename columns
    df.rename(columns=column_mapping, inplace=True)

    # Create Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
    df.to_excel(response, index=False)

    return response

def student_view(request, id):
    try:
        student = Student.objects.get(id=id)

    except ObjectDoesNotExist:
            messages.error(request, f"Student with OAMDC {id} Number not found.")
            return redirect('dashboard')
    context = {'student':student}
    return render(request, 'College/student/view_student.html',context)

def student_update(request, id):
    user = request.user
    try:
        college = College.objects.get(user=user)

    except College.DoesNotExist:
            return redirect('error_page')
    student = get_object_or_404(Student, id = id, college = college)

    if request.method == "POST":
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        if student_form.is_valid():
            student_form.save()
            messages.success(request, "Student record updated successfully.")
            return redirect('student_view', id=id)
        else:
            messages.error('please fill all neccessory details')
    # For GET request: Initialize empty forms
    student_form = StudentForm(instance=student)
    context = {
        'form': student_form,
        'student':student,
    }
    return render(request, 'College/student/update_student.html', context)

def delete_student(request, id):
    user = request.user
    try:
        college = College.objects.get(user=user)

    except College.DoesNotExist:
            return redirect('error_page')
    student = get_object_or_404(Student, id = id, college = college)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    context ={'student':student}
    return render(request, 'College\student\delete_student.html', context)