from rest_framework import viewsets

from albums.models import Album
from rest.serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    lookup_field = 'owner'

    def get_queryset(self):
        username = self.kwargs['slug']
        queryset = Album.objects.filter(owner__username=username)
        if not username == self.request.user.username:
            queryset = queryset.filter(public=True)

        return queryset
