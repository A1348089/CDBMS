from django.urls import path
from .views import home, login_view

urlpatterns = [
    path('login/', login_view, name='login' ),
]
