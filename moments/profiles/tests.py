import shutil

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from albums.models import Album, Photo
from moments.settings import MEDIA_ROOT


class UserDetailTestCase(TestCase):

    @staticmethod
    def get_album_page_url(album: Album):
        return reverse('album-detail', args=[album.owner.username, album.name])

    @staticmethod
    def create_attribute_reference_tag(url: str):
        return f'<a href="{url}">'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.user = User.objects.create_user(username="test_user")
        cls.user_page = reverse('user-detail', args=[cls.user.username])
        cls.user_template = 'auth/user_detail.html'

        cls.public_album = Album.objects.create(name="public_album", owner=cls.user)
        cls.public_page = cls.get_album_page_url(cls.public_album)
        cls.public_page_link = cls.create_attribute_reference_tag(cls.public_page)

        # Add photo to public album
        cls.image = SimpleUploadedFile(name='test_image.jpg', content=open('profiles/data/tuckie.jpg', 'rb').read(),
                                       content_type='image/jpeg')
        cls.photo = Photo.objects.create(title="Tuckie", album=cls.public_album, image=cls.image)
        cls.photo_link = f"background-image: url('{cls.photo.image.url}')"

        cls.private_album = Album.objects.create(name="private_album", owner=cls.user, public=False)
        cls.private_page = cls.get_album_page_url(cls.private_album)
        cls.private_page_link = cls.create_attribute_reference_tag(cls.private_page)

        cls.new_album_form = reverse('create-album')
        cls.new_album_link = cls.create_attribute_reference_tag(cls.new_album_form)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(f"{MEDIA_ROOT}/{cls.user.username}")

    def tearDown(self) -> None:
        self.client.logout()

    def test_get_profile_anonymous(self):
        """
        Tests that when an anonymous user visits a user profile:
            - Only public albums shown
            - No link to create a new album
        """
        with self.assertTemplateUsed(self.user_template):
            response = self.client.get(self.user_page)
            self.assertContains(response, self.public_page_link)
            self.assertNotContains(response, self.private_page_link)
            self.assertNotContains(response, self.new_album_link)

    def test_get_own_profile(self):
        """
        Tests that when a user visits their own user profile:
            - All albums shown
            - Link to create a new album
            - Photo preview for album with photo
            - Default SVG for album without photo
            - "create-album" SVG
        """
        self.client.force_login(self.user)

        default_svg = "/static/img/question-circle-regular.svg"
        create_album_svg_img = '<img class="card-img-top" src="/static/img/plus-solid.svg">'
        with self.assertTemplateUsed(self.user_template):
            response = self.client.get(self.user_page)
            for page_link in [self.public_page_link,
                              self.private_page_link,
                              self.new_album_link,
                              self.photo_link,
                              default_svg,
                              create_album_svg_img]:
                self.assertContains(response, page_link)

    def test_get_other_profile_logged_in(self):
        """
        Tests that when a user visits another user's profile:
            - Only public albums shown
            - No link to create a new album
        """
        other_user = User.objects.create(username="other_user")
        self.client.force_login(other_user)
        with self.assertTemplateUsed(self.user_template):
            response = self.client.get(self.user_page)
            self.assertContains(response, self.public_page_link)
            self.assertNotContains(response, self.private_page_link)
            self.assertNotContains(response, self.new_album_link)


class GetAlbumTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user("test_user")
        cls.album_name = "test_album"
        cls.album_page = reverse('album-detail', args=[cls.user.username, cls.album_name])
        cls.album_template = "albums/album_detail.html"

    def tearDown(self) -> None:
        self.client.logout()

    def test_get_album(self):
        Album.objects.create(owner=self.user, name=self.album_name)
        with self.assertTemplateUsed(self.album_template):
            self.client.get(self.album_page)

    def test_get_album_does_not_exist(self):
        with self.assertTemplateNotUsed(self.album_template):
            response = self.client.get(self.album_page)
            self.assertEqual(404, response.status_code)

    def test_get_own_private_album(self):
        self.client.force_login(self.user)
        Album.objects.create(owner=self.user, name=self.album_name, public=False)
        response = self.client.get(self.album_page)
        self.assertEqual(200, response.status_code)

    def test_get_private_album_anonymous(self):
        Album.objects.create(owner=self.user, name=self.album_name, public=False)
        response = self.client.get(self.album_page)
        self.assertEqual(401, response.status_code)

    def test_get_other_user_private_album(self):
        other_user = User.objects.create_user(username="other_user")
        self.client.force_login(other_user)
        Album.objects.create(owner=self.user, name=self.album_name, public=False)
        response = self.client.get(self.album_page)
        self.assertEqual(401, response.status_code)
