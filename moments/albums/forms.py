from django.forms import ModelForm, inlineformset_factory

from .models import Album, Photo


class AlbumForm(ModelForm):
    class Meta:
        exclude = ['owner']
        model = Album

    def clean(self):
        cleaned_data = super(AlbumForm, self).clean()
        name = cleaned_data.get('name')

        if name.lower() == 'new':
            self.add_error('name', 'Good one, please use a different album title.')


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']

    def clean(self):
        cleaned_data = super(PhotoForm, self).clean()
        title = cleaned_data.get('title')
        image = cleaned_data.get('image')

        if title and not image:
            self.add_error('image', 'Image field cannot be empty.')


total_photo_fields = 5
AlbumPhotosFormSet = inlineformset_factory(Album, Photo, form=PhotoForm, extra=total_photo_fields)
