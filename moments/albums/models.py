from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Album(models.Model):
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'],
                                    name='unique_user_album')
        ]
