from datetime import date
from django.core.validators import RegexValidator

from django.db import models

from CollegeApp.models import Address, Bank_details, College, Department

# Create your models here.
from django.utils.timezone import now
class Staff(models.Model):
    TEACHING = 'Teaching'
    NON_TEACHING = 'Non Teaching'
    
    STAFF_TYPE_CHOICES = [(TEACHING, 'Teaching'),
                          (NON_TEACHING, 'Non Teaching')]

    WORKING = 'Working'
    TRANSFERRED = 'Transferred'
    DEPARTED = 'Departed'
    
    STAFF_STATUS_CHOICES = [(WORKING, 'Working'),
                            (TRANSFERRED, 'Transferred'),
                            ( DEPARTED, 'Departed')]
    
    MALE = 'Male'
    FEMALE = 'Female'
    TRANSGENDER = 'Transgender'

    GENDER_CHOICES = [(MALE, 'Male'),
                      (FEMALE, 'Female'),
                      ( TRANSGENDER, 'Transgender')]

    staff_id = models.CharField(max_length=20, unique=True, null=False)
    cfms_id = models.CharField(max_length=50)
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15, null=True, choices=GENDER_CHOICES, default='Choose')
    photo = models.ImageField(upload_to='media/staff_pics/',blank=True)

    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES, default='Choose')

    mobile_no = models.CharField(max_length=10, unique=True, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[0-9]{10}$',
            message='Mobile number must be 10 digits.',
            code='invalid_mobile'
        ),
    ])
    email = models.EmailField(null=True, blank=False)
    date_of_birth = models.DateField(null=True)

    # Foreign key to the College model
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=False, related_name='staff')
    doj_in_govt_service = models.DateField(null=True)
    # Teaching staff specific fields
    doj_in_college = models.DateField(null=False)
    date_of_exite = models.DateField(default=None, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    is_hod = models.BooleanField(default=False)

    # Address as a OneToOneField
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    bank = models.OneToOneField(Bank_details, on_delete=models.SET_NULL, null=True, blank=True)

    aadhar_number = models.CharField(max_length=20, null=True, validators=[
        RegexValidator(
            regex='^[0-9]{12}$',
            message='Aadhar number must be 12 digits.',
            code='invalid_mobile'
        ),
    ])
    status = models.CharField(max_length=20, choices=STAFF_STATUS_CHOICES, default='Choose')
    salary = models.CharField(max_length=8, null=True)
    previous_working_station = models.CharField(max_length=100, null=True)

    transferred_college_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Stores creation time

    def __str__(self):
        return f"{self.salutation} {self.first_name} {self.last_name} {self.college} {self.department.departmentName}, {self.calculate_experience}"
    
    def calculate_experience(self):
        if self.doj_in_govt_service:
            return date.today().year - self.doj_in_govt_service.year
        return 0  # Return 0 if no appointment date is available