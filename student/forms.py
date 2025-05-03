from django import forms

from CollegeApp.models import District, State

from .models import *
from datetime import datetime

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['father_name', 'mother_name', 'father_aadhar', 'mother_aadhar', 'mobile']

class StudentForm(forms.ModelForm):
    year_of_admission = forms.ChoiceField(label="Year of Admission")
    program = forms.ModelChoiceField(queryset=Program.objects.all())
    class Meta:
        model = Student
        fields = ['OAMDC_NO', 'first_name', 'last_name', 'pic',
                  'mobile_no', 'email', 'gender', 'date_of_birth',
                  'mother_tongue', 'nationality', 'blood_group',
                  'place_of_birth', 'ssc_hall_ticket', 'ssc_school_name',
                  'ssc_year_of_study', 'ssc_marks', 'ssc_marks_file',
                  'intermediate_hall_ticket_no', 'intermediate_college_name', 'intermediate_year_of_study',
                  'intermediate_marks', 'intermediate_marks_file', 'caste',
                  'caste_certificate_no', 'caste_certificate_file', 'income_certificate_no',
                  'income_certificate_file', 'aadhar_no', 'aadhar_file',
                  'program', 'subject_combination', 'medium', 
                  'year_of_admission','status']
        
        widgets = {'program': forms.Select(attrs={'class': 'common-field-size','value':'Null'}),}
         
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        
        # Generate a list of years from 2000 to the current year
        current_year = datetime.now().year

        academic_year = f"{current_year}-{current_year + 3}"
        
        start_year = 2010
        years = [('', 'Choose Academic Year')]+[(f"{year}-{year + 1}", f"{year}-{year + 3}") for year in range(start_year, current_year + 3)]

        # Assign the choices to the field
        self.fields['year_of_admission'].choices = years
        # Set the default value to the current academic year
        self.fields['year_of_admission'].initial = academic_year

        # Set optional fields as not required        
        optional_fields = ['first_name', 'pic', 'date_of_birth',
                           'blood_group', 'place_of_birth', 'ssc_hall_ticket', 
                           'ssc_school_name', 'ssc_year_of_study', 'ssc_marks', 'ssc_marks_file',
                           'intermediate_hall_ticket_no', 'intermediate_college_name', 'intermediate_year_of_study', 'intermediate_marks', 'intermediate_marks_file',
                           'caste', 'caste_certificate_no', 'caste_certificate_file', 'income_certificate_no', 'income_certificate_file', 'aadhar_no', 'aadhar_file',
                           'program', 'subject_combination', 'medium', 'year_of_admission', 'status']

        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False
    
class StudentFilterForm(forms.Form):
    academic_year = forms.ChoiceField(required=False,label="Academic year")
    status = forms.ChoiceField(choices=[('','choose status')]+list(Student.STATUS),
                               required=False)
    gender = forms.ChoiceField(choices=[('','choose')]+list(Staff.GENDER_CHOICES),
                               required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all(),
                                        required=False)
    district = forms.ModelChoiceField(queryset=District.objects.all(),
                                        required=False)
    program = forms.ModelChoiceField(queryset=Program.objects.all(),
                                required=False)
    group = forms.ModelChoiceField(queryset=SubjectCombination.objects.all(),
                                           required=False)
    medium = forms.ModelChoiceField(queryset=Medium.objects.all(),
                               required=False)    


    def __init__(self, *args, **kwargs):
        super(StudentFilterForm, self).__init__(*args, **kwargs)  # Use the correct class name here

        # Generate a list of years from 2000 to the current year
        current_year = datetime.now().year

        academic_year = f"{current_year}-{current_year + 3}"
        
        start_year = 2010
        years = [('', 'Choose Academic Year')]+[(f"{year}-{year + 1}", f"{year}-{year + 3}") for year in range(start_year, current_year + 3)]

        # Assign the choices to the field
        self.fields['academic_year'].choices = years
        # Set the default value to the current academic year
        self.fields['academic_year'].initial = academic_year