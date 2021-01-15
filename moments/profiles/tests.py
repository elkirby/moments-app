from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from albums.models import Album


class UserDetailTestCase(TestCase):

    @staticmethod
    def get_album_page_url(album: Album):
        return reverse('View Album', args=[album.owner.username, album.name])

    @staticmethod
    def create_attribute_reference_tag(url: str):
        return f'<a href="{url}">'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.user = User.objects.create_user(username="test_user")
        cls.user_page = reverse('User Profile', args=[cls.user.username])
        cls.user_template = 'auth/user_detail.html'

        cls.public_album = Album.objects.create(name="public_album", owner=cls.user)
        cls.public_page = cls.get_album_page_url(cls.public_album)
        cls.public_page_link = cls.create_attribute_reference_tag(cls.public_page)

        cls.private_album = Album.objects.create(name="private_album", owner=cls.user, public=False)
        cls.private_page = cls.get_album_page_url(cls.private_album)
        cls.private_page_link = cls.create_attribute_reference_tag(cls.private_page)

    def tearDown(self) -> None:
        self.client.logout()

    def test_get_profile_anonymous(self):
        """
        Tests that only public albums are shown when an anonymous user visits a user profile
        """
        with self.assertTemplateUsed(self.user_template):
            response = self.client.get(self.user_page)
            self.assertContains(response, self.public_page_link)
            self.assertNotContains(response, self.private_page_link)

    def test_get_own_profile(self):
        """
        Tests that all albums are shown when a user visits their own user profile
        """
        self.client.force_login(self.user)
        with self.assertTemplateUsed(self.user_template):
            response = self.client.get(self.user_page)
            for page_link in [self.public_page_link, self.private_page_link]:
                self.assertContains(response, page_link)

    def test_get_other_profile_logged_in(self):
        """
        Tests that only public albums are shown when a user visits another user's profile
        """
        other_user = User.objects.create(username="other_user")
        self.client.force_login(other_user)
        with self.assertTemplateUsed(self.user_template):
            response = self.client.get(self.user_page)
            self.assertContains(response, self.public_page_link)
            self.assertNotContains(response, self.private_page_link)


class GetAlbumTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user("test_user")
        cls.album_name = "test_album"
        cls.album_page = reverse('View Album', args=[cls.user.username, cls.album_name])
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
