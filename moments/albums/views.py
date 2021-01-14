from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, edit

from .models import Album


class CreateAlbum(LoginRequiredMixin, edit.CreateView):
    model = Album
    fields = ['name', 'public']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.success_url = reverse('View Album', args=[form.instance.name])

        return super().form_valid(form)


class AlbumDetailView(DetailView):
    model = Album
    slug_field = 'name'
