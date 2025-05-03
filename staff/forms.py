from datetime import date
from django import forms

from CollegeApp.models import Department, District, State
from staff.models import Staff

class StaffForm(forms.ModelForm):
    SALUTATION_CHOICES = [('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss.')]
    
    staff_type = forms.ChoiceField(
        choices=[('', 'Choose Staff Type')] + list(Staff.STAFF_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': ''})
    )
    salutation = forms.ChoiceField(choices=SALUTATION_CHOICES)
    status = forms.ChoiceField(
        choices=[('', 'Choose Status')] + list(Staff.STAFF_STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': ''})
    )
    
    # Use a normal CharField instead of FormMethodField
    experience = forms.CharField(
        label="Experience",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Staff
        fields = [
            'staff_id', 'cfms_id', 'salutation', 'first_name', 'last_name', 'gender', 'photo',
            'staff_type', 'mobile_no', 'email', 'date_of_birth', 'doj_in_govt_service', 'doj_in_college', 
            'date_of_exite', 'designation', 'department', 'is_hod', 'aadhar_number', 'status',
            'salary', 'bank', 'previous_working_station', 'transferred_college_name', 'experience'
        ]

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

        # Calculate and set initial value for experience
        if self.instance and self.instance.doj_in_govt_service:
            self.fields['experience'].initial = self.calculate_experience(self.instance.doj_in_govt_service)

        # Set optional fields
        optional_fields = [
            'first_name', 'photo', 'email', 'previous_working_station', 'date_of_birth',
            'transferred_college_name', 'bank', 'department', 'salary', 'is_hod',
            'doj_in_govt_service', 'date_of_exite', 'experience'
        ]
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False

        # Add CSS classes to fields
        common_fields = [
            'staff_id', 'cfms_id', 'first_name', 'last_name', 'photo', 'mobile_no', 'email',
            'designation', 'department', 'aadhar_number', 'doj_in_college',
            'previous_working_station', 'staff_type', 'status', 'date_of_birth', 'transferred_college_name'
        ]
        small_fields = ['gender', 'salary', 'is_hod', 'doorNo', 'salutation', 'experience']

        for field_name in common_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'common-field-size'})

        for field_name in small_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'small-field-size'})

    @staticmethod
    def calculate_experience(doj_in_govt_service):
        return date.today().year - doj_in_govt_service.year
    
class StaffFilterForm(forms.Form):
    experience = forms.IntegerField(required=False,
                                    widget=forms.NumberInput(attrs={'class': '',
                                                                    'placeholder': 'Years of Experience'
                                                                    })
                                                                    )
    staff_type = forms.ChoiceField(choices=[('', 'Choose Staff Type')] + list(Staff.STAFF_TYPE_CHOICES),
                                   required=False,
                                   widget=forms.Select(attrs={'class': ''})
                                   )
    
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        required=False,
                                        empty_label="Choose Department",
                                        widget=forms.Select(attrs={'class': ''})
                                        )
    gender = forms.ChoiceField(choices=[('', 'Choose Gender'), ('Male', 'Male'), ('Female', 'Female')],
                               required=False,
                               widget=forms.Select(attrs={'class': ''})
                               )
    
    status = forms.ChoiceField(choices=[('', 'Choose Status')] + list(Staff.STAFF_STATUS_CHOICES),
                               required=False,
                               widget=forms.Select(attrs={'class': ''})
                               )
    
    state = forms.ModelChoiceField(queryset=State.objects.all(),
                                   required=False,
                                   empty_label="Choose State",
                                   widget=forms.Select(attrs={'class': ''})
                                   )
    
    district = forms.ModelChoiceField(queryset=District.objects.all(),
                                      required=False,
                                      empty_label="Select District",
                                      widget=forms.Select(attrs={'class': ''})
                                      )
    
    is_hod = forms.BooleanField(required=False,
                               widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
                               )
    