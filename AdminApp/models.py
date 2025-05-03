from django.db import models
from django.utils import timezone
import uuid
# Create your models here.


class AdminCredentials(models.Model):
    adminemail = models.CharField(max_length=50)
    adminpassword = models.CharField(max_length=50)

    

