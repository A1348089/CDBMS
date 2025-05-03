from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from django.db.models import Q
from staff.serializers import StaffSerializer

from .models import Staff, College
from .forms import StaffFilterForm, StaffForm

from datetime import datetime
import pandas as pd

# Create your views here.
@login_required
def create_staff(request):
    user = request.user
    try:
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        messages.error(request, "College not found.")
        return redirect('dashboard')  # Redirect to a suitable page if college is not found
    staff_form = StaffForm()
    if request.method == 'POST':
        staff_form = StaffForm(request.POST, request.FILES)
        if staff_form.is_valid():
            staff = staff_form.save(commit=False)
            staff.college = college  # Associate the staff with the college
            staff.save()
            messages.success(request, f"Staff record created successfully with ID: {staff.pk}.")
            return redirect('manage_address_details', entity_type="staff", id=staff.id)  # Redirect to a staff list or another view
        
        else:
            messages.error(request, "Please fill all the required fields correctly.")
        
    context = {'form': staff_form}
    return render(request, 'College/staff/create_staff.html', context)

def calculate_threshold_year(experience):
    """
    Calculate the threshold year based on experience in years.
    """
    if experience is None:
        return None
    try:
        experience_years = int(experience)
        current_year = datetime.now().year
        return current_year - experience_years
    except ValueError:
        return None
    
@login_required
def staff_list(request):
    user = request.user
    try:
        # Get the college associated with the logged-in user
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        messages.error(request, "You are not associated with any college.")
        return redirect('error_page')  # Customize this redirect as needed

    # Initialize form and staff queryset
    form = StaffFilterForm(request.GET or None)
    staffs = Staff.objects.filter(college=college).order_by('staff_id')

    if request.method == 'GET' and form.is_valid():
        # Experience filtering
        experience = form.cleaned_data.get('experience')
        threshold_year = calculate_threshold_year(experience)

        # Apply filters dynamically
        filters = {
            'college': college,
            'staff_type': form.cleaned_data.get('staff_type'),
            'department': form.cleaned_data.get('department'),
            'doj_in_govt_service__year__gte': threshold_year,  # greater than or equal
            'is_hod': form.cleaned_data.get('is_hod'),
            'gender': form.cleaned_data.get('gender'),
            'status': form.cleaned_data.get('status'),
            'address__state': form.cleaned_data.get('state'),
            'address__district': form.cleaned_data.get('district')  # Fixed district filter
        }
        # Apply all filters
        filters = {key: value for key, value in filters.items() if value}
        staffs = Staff.objects.filter(**filters).order_by('staff_id')

    for staff in staffs:
        staff.experience = staff.calculate_experience()

    paginator = Paginator(staffs, 50)  # Show 10 staffs per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'College/staff/staff_list.html', context)

@login_required  # Ensures only logged-in users can access
def search_staffs(request):
    user = request.user
    try:
        # Get the college associated with the logged-in user
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        messages.error(request, "You are not associated with any college.")
        return redirect('error_page')  # Customize this redirect as needed

    query = request.GET.get('query', '').strip()

    if not query:
        return JsonResponse({'error': 'No search query provided'}, status=400)

    staffs = Staff.objects.filter(
       Q(college=college) & Q(staff_id__iexact=query) | Q(mobile_no__iexact=query)
    )
    serialized_data = StaffSerializer(staffs, many=True).data
    return JsonResponse({'staffs': serialized_data}, safe=False)

@login_required
def download_staffs_excel(request):
    user = request.user
    try:
        college = College.objects.get(user=user)
    except College.DoesNotExist:
        return HttpResponse("Unauthorized", status=401)

    form = StaffFilterForm(request.GET or None)

    staffs = Staff.objects.filter(college=college).order_by('staff_id')

    if form.is_valid():
        # Experience filtering
        experience = form.cleaned_data.get('experience')
        threshold_year = calculate_threshold_year(experience)

        # Apply filters dynamically
        filters = {
            'college': college,
            'staff_type': form.cleaned_data.get('staff_type'),
            'department': form.cleaned_data.get('department'),
            'doj_in_govt_service__year__gte': threshold_year,  # greater than or equal
            'is_hod': form.cleaned_data.get('is_hod'),
            'gender': form.cleaned_data.get('gender'),
            'status': form.cleaned_data.get('status'),
            'address__state': form.cleaned_data.get('state'),
            'address__district': form.cleaned_data.get('district')  # Fixed district filter
        }
        filters = {key: value for key, value in filters.items() if value}
        staffs = staffs.filter(**filters)

    # Get selected columns from request
    selected_columns = request.GET.getlist('columns')

    # Define column mapping
    column_mapping = {
        'staff_id': 'Staff No',
        'cfms_id': 'CFMS ID',
        'staff_type': 'Staff type',
        'salutation': 'Salutation',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'mobile_no': 'Mobile No',
        'email': 'Email',
        'gender': 'Gender',

        'doj_in_govt_service': 'Date of Joining in Govt. Service',
        'doj_in_college': 'Date of Joining in College',
        'date_of_exite': 'Date of Exit',
        'threshold_year': 'Experience',

        'designation': 'Designation',
        'department': 'Department',
        'is_hod': 'is hod',
        'status':'Status',
        'salary':'Salary',
        'previous_working_station':'previous working station',
        'transferred_college_name': 'Transferred college name',

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
    }

    # Filter selected columns
    selected_column_keys = [key for key in column_mapping if key in selected_columns]

    # If no columns are selected, return all
    if not selected_column_keys:
        selected_column_keys = list(column_mapping.keys())

    # Fetch staff data based on selected columns
    staff_data = staffs.values(*selected_column_keys)

    # Convert to DataFrame
    df = pd.DataFrame(list(staff_data))

    # Rename columns
    df.rename(columns=column_mapping, inplace=True)

    # Create Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Staffs.xlsx"'
    df.to_excel(response, index=False)

    return response

class ManageStaff:
    @staticmethod
    def view_staff(request, id):
        user = request.user
        # Ensure the logged-in user is associated with a college
        try:
            college = College.objects.get(user=user)
        except College.DoesNotExist:
            return redirect('error_page')  # Customize this redirection as needed

        # Get the staff member belonging to the logged-in user's college
        staff = get_object_or_404(Staff, id=id, college=college)

        context = {'staff': staff,}  # Pass the staff object for display

        return render(request, 'College/staff/viewstaffdata.html', context)
    
    @staticmethod
    def update_staff(request, id):
        user = request.user

        # Ensure the logged-in user is associated with a college
        try:
            college = College.objects.get(user=user)
        except College.DoesNotExist:
            return redirect('error_page')  # Customize this redirection as needed

        # Get the staff member belonging to the logged-in user's college
        staff = get_object_or_404(Staff, id=id, college=college)

        if request.method == "POST":
            staff_form = StaffForm(request.POST, request.FILES, instance=staff)
            if staff_form.is_valid():
                # Update staff details
                staff_form.save()
                messages.success(request, "Staff record updated successfully.")
                return redirect('view_staff', id=id)  # Redirect to the view page after update
            else:
                if not staff_form.is_valid():
                    messages.error(request, "please fill the neccessory fields of staff")
        else:
            # Initialize forms with existing staff data for GET requests
            staff_form = StaffForm(instance=staff)
        context = {
            'staff_form': staff_form,
            'staff': staff,  # Pass the staff object for context
        }
        return render(request, 'College/staff/update_staff.html', context)
    
    @staticmethod
    def delete_staff(request, id):
        user = request.user
        # Ensure the logged-in user is associated with a college
        try:
            college = College.objects.get(user=user)
        except College.DoesNotExist:
            return redirect('error_page')  # Customize this redirection as needed

        # Get the staff member belonging to the logged-in user's college
        staff = get_object_or_404(Staff, id=id, college=college)

        if request.method == "POST":
            staff.delete()
            messages.success(request, "Staff removed successfuly")
            return redirect("staff_list")
        return render(request, 'College/staff/delete_staff.html',{"staff":staff})