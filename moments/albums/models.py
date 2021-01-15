import pathlib

from django.contrib.auth.models import User
from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'],
                                    name='unique_user_album')
        ]


def upload_to(instance, filename):
    user = instance.album.owner.username
    album = instance.album.name
    ext = pathlib.Path(filename).suffix

    return f"{user}/albums/{album}/{instance.title}{ext}"


class Photo(models.Model):
    title = models.CharField(max_length=140)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'album'],
                                    name='unique_album_title'),
            models.UniqueConstraint(fields=['album', 'image'],
                                    name='unique_album_img')
        ]