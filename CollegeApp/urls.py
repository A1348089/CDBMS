from django.urls import path
from django.contrib.auth.views import LogoutView 
from .views import dashboard, get_districts, get_states, get_subject_combination, home, manage_address_details, manage_bank_details, register_college

urlpatterns = [
    path('', home, name='home' ),

    path('register_college/', register_college, name='register_college'),

    path('dashboard/', dashboard, name='dashboard'),
    path('<str:entity_type>/<int:id>/address/', manage_address_details, name='manage_address_details'),
    path('<str:entity_type>/<int:id>/add_bank/',manage_bank_details,name='manage_bank_details'), 
    
    path('ajax/get_states/', get_states, name='get_states'),
    path('ajax/get-districts/', get_districts, name='get_districts'),
    path('api/subject-combinations/', get_subject_combination, name='subject_combinations'),
    # Logout view 
]
