from django.urls import path, include

from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='Sign Up'),
    path('login', views.user_login, name='Login'),
]