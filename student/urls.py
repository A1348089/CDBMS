from django.urls import path
from .views import (create_student, delete_student, download_students_excel, search_students, student_list, student_view, student_update,
                    manage_student_parent_details)
from CollegeApp.views import manage_bank_details
urlpatterns = [
    path('create/', create_student, name='create_student'),
    path('list/', student_list, name='student_list'),
    path('<int:id>/',student_view,name='student_view'),
    path('<int:id>/edit/',student_update,name='student_update'),
    path('student_list/download/', download_students_excel, name='download_students_excel'),
    path('<int:id>/add_parent/',manage_student_parent_details,name='manage_student_parent_details'),
    path('<int:id>/add_bank/',manage_bank_details,name='manage_bank_details'),
    path('<int:id>/delete/',delete_student,name='delete_student'),
    
    path('api/search-students/', search_students, name='search-students'),

]