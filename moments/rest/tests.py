from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from albums.models import Album, Photo


# FIXME: This test module succeeds on its own, and fails when run as part of the suite.
# I am baffled as to why.

class RESTUserDetailTestCase(TestCase):
    @staticmethod
    def toisostring(dt: datetime):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.user = User.objects.create_user(username="test_user")
        cls.public_album = Album.objects.create(name="public_album", owner=cls.user)
        cls.private_album = Album.objects.create(name="private_album", owner=cls.user, public=False)
        cls.user_albums = Album.objects.filter(owner=cls.user).values('created', 'name')

        cls.other_user = User.objects.create_user(username="other_user")

        cls.album_list_api_endpoint = reverse('rest:user-list', current_app='rest', kwargs={'slug': cls.user.username})

    def tearDown(self) -> None:
        self.client.logout()

    def test_get_albums_anonymous(self):
        """
        Tests only public albums returned when not logged in
        """
        response = self.client.get(self.album_list_api_endpoint, data={'slug': self.user.username})

        expected = list(self.user_albums.filter(public=True))
        for album in expected:
            album['created'] = self.toisostring(album['created'])
        actual = response.json()

        self.assertListEqual(expected, actual)

    def test_get_albums_other_user(self):
        """
        Tests only public albums returned when logged in as another user
        """
        self.client.force_login(self.other_user)

        response = self.client.get(self.album_list_api_endpoint, data={'slug': self.user.username})

        expected = list(self.user_albums.filter(public=True))
        for album in expected:
            album['created'] = self.toisostring(album['created'])
        actual = response.json()

        self.assertListEqual(expected, actual)

    def test_get_albums_self(self):
        """
        Tests all albums returned when looking at own albums
        """
        self.client.force_login(self.user)

        response = self.client.get(self.album_list_api_endpoint, data={'slug': self.user.username})

        expected = list(self.user_albums)
        for album in expected:
            album['created'] = self.toisostring(album['created'])
        actual = response.json()

        self.assertListEqual(expected, actual)


class GetPhotosTestCase(TestCase):

    @staticmethod
    def get_api_endpoint(user, album):
        return reverse('rest:album-detail', current_app='rest', kwargs={'slug': user, 'album': album})

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.user = User.objects.create_user(username="test_user")
        cls.public_album = Album.objects.create(name="public_album", owner=cls.user)
        Photo.objects.create(title='test_photo_public', album=cls.public_album)
        cls.public_photos = Photo.objects.filter(album=cls.public_album).values('title')

        cls.private_album = Album.objects.create(name="private_album", owner=cls.user, public=False)
        Photo.objects.create(title='test_photo_private', album=cls.private_album)
        cls.private_photos = Photo.objects.filter(album=cls.private_album).values('title')

        cls.other_user = User.objects.create_user(username="other_user")
        other_album = Album.objects.create(name=cls.public_album.name, owner=cls.other_user)
        Photo.objects.create(title='other_user_photo', album=other_album)

    def test_get_photos_public(self):
        """
        Tests that only photos for that album name and that user are returned for a public album
        """
        endpoint = self.get_api_endpoint(self.user.username, self.public_album.name)
        response = self.client.get(endpoint)

        expected_photos = list(self.public_photos)
        expected = dict(photos=expected_photos)
        actual = response.json()

        self.assertDictEqual(expected, actual)

    def test_get_photos_private_anonymous(self):
        """
        Photos not returned for a private album when logged out
        """
        endpoint = self.get_api_endpoint(self.user.username, self.private_album.name)
        response = self.client.get(endpoint)
        self.assertEqual(404, response.status_code)

    def test_get_photos_private_other_user(self):
        """
        Photos not returned for a private album when logged in as a different user
        """
        self.client.force_login(self.other_user)
        endpoint = self.get_api_endpoint(self.user.username, self.private_album.name)
        response = self.client.get(endpoint)
        self.assertEqual(404, response.status_code)

    def test_get_photos_private(self):
        """
        Photos not returned for a private album when logged in as the owner
        """
        self.client.force_login(self.user)
        endpoint = self.get_api_endpoint(self.user.username, self.private_album.name)
        response = self.client.get(endpoint)
        self.assertEqual(200, response.status_code)

        expected_photos = list(self.private_photos)
        expected = dict(photos=expected_photos)
        actual = response.json()

        self.assertDictEqual(expected, actual)
