from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from .models import Album


class CreateAlbum(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['name', 'public']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
