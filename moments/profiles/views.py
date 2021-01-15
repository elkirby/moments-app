from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView

from albums.models import Album


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        return {
            **super(UserDetailView, self).get_context_data(),
            'breadcrumbs': {
                'Home': reverse('Home'),
                'User Profile': None
            }
        }


def get_album(request, slug, name):
    album = get_object_or_404(Album, name=name, owner__username=slug)

    if not album.public and (slug != request.user.username):
        return render(request, 'base.html', status=401, context={"error_msg": '401: Unauthorized'})

    context = {
        'album': album,
        'breadcrumbs': {
            'Home': reverse('Home'),
            'User Profile': reverse('User Profile', args=[slug]),
            album.name: None
        }
    }

    return render(request, 'albums/album_detail.html', context)
