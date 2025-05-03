from django.urls import path
from .views import *

urlpatterns = [
    path('adminlogin/', adminlogin, name='adminlogin'),
    path('adminhome/', adminhome, name='adminhome'),
    path('view-requested/', view_requested, name='view-requested'),
    path('view-active/', view_active, name='view-active'),
    path('view-rejected/', view_rejected, name='view-rejected'),
    path('activate/<int:id>/', activate, name='activate'),
    path('reject/<int:id>/', reject, name='reject'),
]