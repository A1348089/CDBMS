from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *

class CollegeLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

class CollegeRegisterForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ['college_code', 'college_name', 'college_email', 'phone_no']

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

class AddressForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.all())
    class Meta:
        model = Address
        fields = ['doorNo', 'village', 'street', 'mandal', 'district', 'pin_code', 'state']
        widgets = {
            'doorNo': forms.TextInput(attrs={'class': 'small-field-size', 'value':' '}),
            'village': forms.TextInput(attrs={'value':' '}),
            'street': forms.TextInput(attrs={'value':' '}),
            'mandal': forms.TextInput(attrs={'value':' '}),
            'district': forms.Select(attrs={'class': 'common-field-size','value':'Null'}),
            'state': forms.Select(attrs={'class': 'common-field-size','value':'Null'}),
            'pin_code': forms.TextInput(attrs={'value':' '}),
        }
class Bank_NameForm(forms.ModelForm):
    class Meta:
        model = Bank_Name
        fields = ['bank']

class BankForm(forms.ModelForm):
    bank_name = forms.ModelChoiceField(queryset=Bank_Name.objects.all())
    class Meta:
        model = Bank_details
        fields = ['bank_account_num', 'bank_name', 'branch_name', 'ifsc_code']
        widgets = {
            'bank_name': forms.Select(attrs={'class': 'common-field-size', 'value':' '}),
            'bank_account_num': forms.TextInput(attrs={'class': 'common-field-size', 'value':' '}),
            'branch_name': forms.TextInput(attrs={'class': 'common-field-size', 'value':' '}),
            'ifsc_code': forms.TextInput(attrs={'class': 'common-field-size', 'value':' '})
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
    
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'

class SubjectCombinationForm(forms.ModelForm):
    class Meta:
        model = SubjectCombination
        fields = '__all__'