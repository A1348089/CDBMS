from django.db import models

from CollegeApp.models import Address, Bank_details, College, Medium, Program, SubjectCombination, validate_year

from django.core.validators import RegexValidator

from staff.models import Staff

# Create your models here.

class Parent(models.Model):
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    father_aadhar = models.CharField(max_length=12, validators=[RegexValidator(regex='^[0-9]{12}$',
                                                                               message='Aadhar number must be 12 digits.',
                                                                               code='invalid_aadhar'
                                                                               ),
                                                                               ], blank=True)
    mother_aadhar = models.CharField(max_length=12, validators=[RegexValidator(regex='^[0-9]{12}$',
                                                                               message='Aadhar number must be 12 digits.',
                                                                               code='invalid_aadhar'
                                                                               ),
                                                                               ], blank=True)
    mobile = models.CharField(max_length=10, validators=[RegexValidator(regex='^[0-9]{10}$',
                                                                               message='Mobile number must be 10 digits.',
                                                                               code='invalid_mobile'
                                                                               ),
                                                                               ], blank=True)

    def __str__(self):
        return f"Parent of are {self.mother_name} {self.father_name}"
from django.utils.timezone import now
class Student(models.Model):
    LANGUAGE_CHOICES = [('English', 'English'),
                        ('Hindi', 'Hindi'),
                        ('Telugu', 'Telugu'),
                        ('Tamil', 'Tamil'),
                        ('Kannada', 'Kannada'),
                        ('Malayalam', 'Malayalam'),
                        ('Marathi', 'Marathi'),
                        ('Bengali', 'Bengali'),
                        ('Gujarati', 'Gujarati'),
                        ('Punjabi', 'Punjabi'),
                        ('Urdu', 'Urdu'),
                        ]
    STATUS = [('OnGoing','OnGoing'),
              ('Graduate','Graduate'),
              ('DropOut', 'DropOut'),]
    
    OAMDC_NO = models.CharField(max_length=20, unique=True, null=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='media/student_pics/', blank=True)
    mobile_no = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex='^[0-9]{10}$',
                                                                           message='Mobile number must be 10 digits.',
                                                                           code='invalid_mobile'
                                                                           ),
                                                                           ])
    email = models.EmailField(null=False, blank=False)
    gender = models.CharField(max_length=15, choices=Staff.GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    mother_tongue = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    nationality = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=10, null=True)
    place_of_birth = models.CharField(max_length=100, null=True)

    # SSC
    ssc_hall_ticket = models.CharField(max_length=20, null=True, blank=True)
    ssc_school_name = models.CharField(max_length=100, null=True, blank=True)
    ssc_year_of_study = models.IntegerField(validators=[validate_year], null=True, blank=True)
    ssc_marks = models.CharField(max_length=6, null=True, blank=True)
    ssc_marks_file = models.FileField(upload_to='media/ssc_marks_file/', null=True, blank=True)

    # Intermediate
    intermediate_hall_ticket_no = models.CharField(max_length=20, null=True, blank=True)
    intermediate_college_name = models.CharField(max_length=100, null=True, blank=True)
    intermediate_year_of_study = models.IntegerField(validators=[validate_year], null=True, blank=True)
    intermediate_marks = models.CharField(max_length=6, null=True, blank=True)
    intermediate_marks_file = models.FileField(upload_to='media/intermediate_marks_file/', null=True, blank=True)
    
    # Caste
    caste = models.CharField(max_length=50, null=True, blank=True)
    caste_certificate_no = models.CharField(max_length=20, null=True, blank=True)
    caste_certificate_file = models.FileField(upload_to='media/caste_certificates_file/', null=True, blank=True)
    
    # Income
    income_certificate_no = models.CharField(max_length=20, null=True, blank=True)
    income_certificate_file = models.FileField(upload_to='media/income_certificates_file/', null=True, blank=True)
    
    # Aadhar
    aadhar_no = models.CharField(max_length=20, null=True, blank=True, validators=[RegexValidator(regex='^[0-9]{12}$',
                                                                                                  message='Aadhar number must be 12 digits.',
                                                                                                  code='invalid_aadhar'
                                                                                                  ),
                                                                                                  ])
    aadhar_file = models.FileField(upload_to='media/aadhar_files/', null=True, blank=True)
    
    # Address as a OneToOneField
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    # Academic
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    subject_combination = models.ForeignKey(SubjectCombination, on_delete=models.SET_NULL, null=True)
    medium = models.ForeignKey(Medium, on_delete=models.SET_NULL, null=True)
    year_of_admission = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS)
    
    # Bank
    bank = models.OneToOneField(Bank_details, on_delete=models.SET_NULL, null=True, blank=True)
    # Relationship with a specific teacher
    mentor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='student')  

    parent = models.OneToOneField(Parent, on_delete=models.CASCADE, null=True, blank=True)
    # College
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='student')
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Stores creation time

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.college} {self.medium.medium}"
    
    # def save(self, college=None, *args, **kwargs):
    #     if college:
    #         college = College.objects.get(college=college)
    #         self.college = college
    #     return super().save()