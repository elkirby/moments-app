from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import edit, ListView

from .forms import AlbumForm, AlbumPhotosFormSet
from .models import Album


class CreateAlbum(LoginRequiredMixin, edit.CreateView):
    form_class = AlbumForm
    template_name = "albums/album_form.html"
    context_object_name = "album_form"

    def get_context_data(self, **kwargs):

        data = super(CreateAlbum, self).get_context_data(**kwargs)

        if self.request.POST:
            data['photos'] = AlbumPhotosFormSet(self.request.POST, self.request.FILES)
        else:
            data['photos'] = AlbumPhotosFormSet()

        data['breadcrumbs'] = {
            'Home': reverse('Home'),
            'Profile Home': None
        }

        return data

    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        photos = context['photos']

        self.success_url = reverse('View Album', args=[form.instance.owner, form.instance.name])

        name = form.instance.name
        owner = form.instance.owner
        existing_album = Album.objects.filter(name=name, owner=owner).exists()
        if existing_album:
            form.add_error('name', f"An album already exists for user '{owner}' with name '{name}'")

        if not form.errors:
            self.object = form.save()

            if photos.is_valid():
                photos.instance = self.object
                photos.save()
                return super().form_valid(form)

        if not existing_album:
            Album.objects.get(name=name).delete()

        return render(self.request, self.template_name, {'form': form, 'photos': photos})


class AlbumPublicListView(ListView):
    queryset = Album.objects.filter(public=True).all()
    ordering = '-created'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(AlbumPublicListView, self).get_context_data(),
            'breadcrumbs': {
                'Home': reverse('Home'),
                'All Albums': None
            }
        }
