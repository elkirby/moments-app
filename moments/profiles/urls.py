from django.urls import path

from .views import UserDetailView, get_album

urlpatterns = [
    path('', UserDetailView.as_view(), name='User Profile'),
    path('albums/<name>', get_album, name='View Album'),

]
