from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_year(value):
    if value < 2018 or value > 2100:  # Adjust the range as needed
        raise ValidationError(f"{value} is not a valid year. Year must be between 2018 and 2100.")

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    district = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.district

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    doorNo = models.CharField(max_length=10, null=True)
    village = models.CharField(max_length=300, null=True)
    street = models.CharField(max_length=30, null=True)
    mandal = models.CharField(max_length=50, null=True, blank=True, default=None)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    pin_code = models.CharField(max_length=6, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mandal}, {self.state}, {self.pin_code}"

class Bank_Name(models.Model):
    bank = models.CharField(max_length=250, null=False)
    def __str__(self):
        return self.bank
    
class Bank_details(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_account_num = models.CharField(max_length=20, null=True)
    bank_name = models.ForeignKey(Bank_Name, on_delete=models.CASCADE, null=True, blank=True)
    ifsc_code = models.CharField(max_length=20, null=True)
    branch_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.bank_name.bank} - {self.branch_name}"

class College(models.Model):
    college_code = models.CharField(max_length=6, unique=True)
    college_name = models.CharField(max_length=100, null=True)
    college_email = models.EmailField(unique=True, null=True)
    phone_no = models.CharField(max_length=10, null=True, unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=6, default="pending")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Stores creation time

    def __str__(self):
        return self.college_name

class Medium(models.Model):
    id = models.AutoField(primary_key=True)
    medium = models.CharField(max_length=50)
    def __str__(self):
        return self.medium

class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_short_name = models.CharField(max_length=10)
    program_full_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.program_full_name} {self.program_short_name}"

class SubjectCombination(models.Model):
    id = models.AutoField(primary_key=True)
    combination_short_form = models.CharField(max_length=10, unique=True)
    combination_full_form = models.CharField(max_length=50, default=None)
    program = models.ForeignKey(Program, on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return f"{self.combination_short_form} ({self.combination_full_form})"

class Department(models.Model):

    departmentName = models.CharField(max_length=100)

    def __str__(self):
        return self.departmentName
