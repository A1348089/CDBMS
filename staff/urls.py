from django.urls import path
from staff import views

urlpatterns = [
    # Staff URLs
    path('create/', views.create_staff, name='create_staff'),  # For creating a new staff
    path('staff_list/', views.staff_list, name='staff_list'),
    path('staff_list/download/', views.download_staffs_excel, name='download_staffs_excel'),
    path('<int:id>/', views.ManageStaff.view_staff, name='view_staff'),
    path('<int:id>/edit/', views.ManageStaff.update_staff, name='update_staff'),
    path('<str:id>/delete/', views.ManageStaff.delete_staff, name='delete_staff'),  # For deleting staff

    path('api/search-staffs/', views.search_staffs, name='search-staffs'),

]
