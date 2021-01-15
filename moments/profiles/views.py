from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView

from albums.models import Album


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    context_object_name = 'current_user'


def get_album(request, slug, name):
    album = get_object_or_404(Album, name=name, owner__username=slug)

    if not album.public and (slug != request.user.username):
        return render(request, 'base.html', status=401, context={"error_msg": '401: Unauthorized'})

    return render(request, 'albums/album_detail.html', {'album': album})
