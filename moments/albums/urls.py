from django.urls import path

from .views import CreateAlbum, AlbumPublicListView

urlpatterns = [
    path('', AlbumPublicListView.as_view(), name='album-list'),
    path('new', CreateAlbum.as_view(), name='create-album'),
]
