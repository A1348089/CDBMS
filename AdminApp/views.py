from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from CollegeApp.models import College
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.models import User
from django.conf import settings
import random
import string
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
# Create your views here.

def adminlogin(req):
    if req.method == 'POST':
        adminemail = req.POST['adminemail']
        adminpassword = req.POST['adminpassword']
        
        # Check if admin credentials exist, create default if not
        if not AdminCredentials.objects.exists():
            AdminCredentials(adminemail='admin@gmail.com', adminpassword='admin').save()

        # Check credentials
        admin = AdminCredentials.objects.filter(adminemail=adminemail, adminpassword=adminpassword).first()
        
        if admin:
            req.session['adminemail']=admin.adminemail
            return redirect('adminhome')
        else:
            error = "Invalid Email or password"
            return render(req, 'adminlogin.html', {'error': error})

    return render(req, 'adminlogin.html')

@login_required
def adminhome(req):
    return render(req, 'adminhome.html')

@login_required
def view_requested(req):
    colleges = College.objects.filter(status='pending')
    return render(req, 'view_requested.html', {'colleges': colleges})

@login_required
def view_active(req):
    colleges = College.objects.filter(status='accepted')
    return render(req, 'view_active.html', {'colleges': colleges})

@login_required
def view_rejected(req):
    colleges = College.objects.filter(status='rejected')
    return render(req, 'view_rejected.html', {'colleges': colleges})

def generate_credentials():
    # Generate a random password that starts with 'SV' and followed by 10 random letters and digits
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    password = 'SV' + random_part
    return password

@login_required
def activate(req, id):
    logger.debug(f"Authenticating college with code: {id}")
    college = get_object_or_404(College, id=id)  # Fetch a single college using the id

    user_email = college.college_email
    college_name = college.college_name
    username = college.phone_no
    # Generate credentials
    password = generate_credentials()
    hashed_password = make_password(password)
    
    # Send email with credentials
    try:
        send_mail(
            subject=f"Hi {college_name}, Your Registration Request Has Been Approved By The Admin",
            message=f'Here are your login credentials:\n\Email: {user_email}\nUsername: {username}\nPassword: {password}',
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use your default from email address from settings
            recipient_list=[user_email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        # Handle the exception (log it, show an error message, etc.)
    
    # Create a user in the User model
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': user_email,
            'password': hashed_password,  # Store the hashed password
        }
    )
    
    if created:
        logger.info(f"User with email {user_email} created successfully.")
    else:
        logger.warning(f"User with email {user_email} already exists.")

    # Update the status of the college and link the user
    college.status = 'accepted'
    college.user = user  # Link the created user to the college
    college.save()
    
    return redirect('view-requested')
    
@login_required
def reject(req, id):
    college = get_object_or_404(College, pk=id)  # Fetch a single college using the id
    
    # Assuming the College model has fields named 'college_email' and 'college_name'
    user_email = college.college_email
    college_name = college.college_name
    
    # Update the status of the college_email to 'rejected'
    college.status = 'rejected'
    college.save()
    # Send email notification
    send_mail(
        subject=f"Hi {college_name}, Your Registration Request Has Been Rejected By The Admin",
        message=f'Your registration request for {college_name} has been rejected.',
        from_email='EMAIL_HOST_USER',  # Replace with your from email address
        recipient_list=[user_email],
        fail_silently=False,
    )
    return redirect('view_requested')


# def forgotpassword(req):
#     return redirect('reset_password_request')

# def reset_password_request(req):
#     if req.method == 'POST':
#         adminemail = req.POST.get('adminemail')
#         admin = get_object_or_404(AdminCredentials, adminemail=adminemail)
#         if admin is not None:
#             # Store the email in the session
#             req.session['adminemail'] = adminemail
#             # Send reset email with token link
#             send_reset_email(admin.adminemail)

#             return redirect('reset_password_confirm')  # Redirect to a confirmation page
        

#     return render(req, 'reset_password_request.html')

# def send_reset_email(admin_email):
#     reset_link = f'http://127.0.0.1:8000/'  # Replace with your actual domain
#     send_mail(
#         'Password Reset Request',
#         f'Click the link below to reset your password:\n\n{reset_link}',
#         'EMAIL_HOST_USER',  # Replace with your from email address
#         [admin_email],
#         fail_silently=False,
#     )


# def reset_password_confirm(req):
#     adminemail = req.session['adminemail']
#     admin = AdminCredentials.objects.filter(adminemail=adminemail).first() 
#     if req.method == 'POST':
#         new_password = req.POST.get('new_password')
#         admin.adminpassword = new_password
#         admin.save()

#         msg = "Your Password Reset Is Completed Successfully"
#         return render(req, 'adminlogin.html', {'msg': msg})  # Redirect to password reset complete page
    
#     return render(req, 'reset_password_confirm.html')

