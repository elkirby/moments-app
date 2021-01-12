from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.utils import DataError
from django.test import TestCase

from .models import Album


class AlbumModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("test_user")
        cls.album_name = "test_album"

    def test_add_album_minimum(self):
        test_album = Album.objects.create(owner=self.user, name=self.album_name)
        self.assertIsNotNone(test_album)
        self.assertTrue(test_album.public)

    def test_add_private_album(self):
        test_album = Album.objects.create(owner=self.user,
                                          name=self.album_name,
                                          public=False)
        self.assertFalse(test_album.public)

    def test_add_album_no_owner(self):
        with self.assertRaisesRegex(expected_exception=IntegrityError,
                                    expected_regex="null value in column \"owner_id\".*"):
            Album.objects.create(name=self.album_name)

    def test_add_album_long_name(self):
        with self.assertRaisesRegex(expected_exception=DataError,
                                    expected_regex=".*value too long.*"):
            Album.objects.create(owner=self.user, name='a' * 141)

    def test_add_duplicate_album(self):
        album_attrs = dict(owner=self.user, name=self.album_name)
        test_album = Album.objects.create(**album_attrs)
        self.assertIsNotNone(test_album)
        with self.assertRaisesRegex(expected_exception=IntegrityError,
                                    expected_regex=".*duplicate key value violates unique constraint.*"):
            Album.objects.create(**album_attrs)

    def test_add_album_same_name(self):
        user_2 = User.objects.create_user('different_user')
        Album.objects.create(owner=self.user, name=self.album_name)
        Album.objects.create(owner=user_2, name=self.album_name)

        expected_owners = [self.user.username, user_2.username]
        actual_owners = [album.owner.username for album in Album.objects.filter(name=self.album_name)]
        self.assertListEqual(expected_owners, actual_owners)
