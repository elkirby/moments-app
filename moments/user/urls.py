from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('sign-up', views.sign_up, name='Sign Up'),
    path('login', views.user_login, name='Login'),
]