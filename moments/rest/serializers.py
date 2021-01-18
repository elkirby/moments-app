from rest_framework import serializers

from albums.models import Album

class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'created']
        lookup_field = 'owner'
