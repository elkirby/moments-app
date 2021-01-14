from django.urls import path

from .views import AlbumDetailView, CreateAlbum, AlbumPublicListView

urlpatterns = [
    path('', AlbumPublicListView.as_view(), name='Public Albums'),
    path('new', CreateAlbum.as_view(), name='Create New Album'),
    path('<slug:slug>', AlbumDetailView.as_view(), name='View Album'),
]
