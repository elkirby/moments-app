from django.urls import path

from .views import CreateAlbum, AlbumPublicListView

urlpatterns = [
    path('', AlbumPublicListView.as_view(), name='Public Albums'),
    path('new', CreateAlbum.as_view(), name='Create New Album'),
]
