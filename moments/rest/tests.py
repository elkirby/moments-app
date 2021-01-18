from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from albums.models import Album


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

        cls.album_list_api_endpoint = reverse('rest:album-list', current_app='rest', kwargs={'slug': cls.user.username})

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
