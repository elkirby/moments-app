from django.urls import path

from .views import CreateAlbum

urlpatterns = [
    path('new', CreateAlbum.as_view(), name='Create New Album'),
]
