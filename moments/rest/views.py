from rest_framework import viewsets

from albums.models import Album, Photo
from rest.serializers import AlbumSerializer, PhotoAlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    lookup_field = 'owner'

    def get_queryset(self):
        username = self.kwargs['slug']
        queryset = Album.objects.filter(owner__username=username)
        if not username == self.request.user.username:
            queryset = queryset.filter(public=True)

        return queryset


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoAlbumSerializer
    lookup_url_kwarg = 'album'
    lookup_field = 'name'

    def get_queryset(self):
        username = self.kwargs['slug']
        name = self.kwargs['album']
        album = Album.objects.filter(owner__username=username, name=name)
        if not username == self.request.user.username:
            album = album.filter(public=True)

        return album
