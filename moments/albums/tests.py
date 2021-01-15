from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.utils import DataError
from django.test import TestCase, Client
from django.urls import reverse

from .forms import total_photo_fields
from .models import Album


class AlbumModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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


class CreateAlbumViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(username="test_user")
        cls.album_name = "test_album"
        cls.album_template = "albums/album_form.html"

        cls.create_album_page = reverse('Create New Album')
        cls.login_page = reverse('Login')

    def tearDown(self) -> None:
        self.client.logout()

    def test_create_album_login_required(self):
        with self.assertTemplateNotUsed(self.album_template):
            response = self.client.get(self.create_album_page)

            self.assertEqual(302, response.status_code)

            expected_response_url = f"{self.login_page}?next={self.create_album_page}"
            self.assertEqual(expected_response_url, response['Location'])

    def test_create_album_logged_in(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed(self.album_template):
            response = self.client.get(self.create_album_page)

            self.assertEqual(200, response.status_code)

    def test_create_album_post(self):
        self.client.force_login(self.user)
        # FIXME: Everything about this is hacky ... even if it gets the job done
        request_data = {
            'name': self.album_name,
            'public': 'on',
            'photo_set-TOTAL_FORMS': total_photo_fields,
            'photo_set-INITIAL_FORMS': 0,
            'photo_set-MIN_NUM_FORMS': 0,
            'photo_set-MAX_NUM_FORMS': 1000,
        }

        photo_fields = ('title', 'image', 'id', 'album')
        for i in range(total_photo_fields):
            for field in photo_fields:
                request_data[f"photo_set-{i}-{field}"] = ''

        response = self.client.post(self.create_album_page, data=request_data)

        expected_response_url = f"/{self.user.username}/albums/{self.album_name}"
        self.assertEqual(expected_response_url, response['Location'])

        test_album = Album.objects.get(name=self.album_name)
        self.assertIsNotNone(test_album)


class AlbumListTestCase(TestCase):

    def populate_albums(self):
        is_public_idx = [True, False, False, True]

        for i in range(4):
            username = f"user_{i % 2}"
            is_public = is_public_idx[i]
            album = Album.objects.create(owner=getattr(self, username),
                                         name=f"test_album_{i}",
                                         public=is_public)
            if is_public:
                #
                self.expected_albums.insert(0, repr(album))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user_0 = User.objects.create_user("user_0")
        cls.user_1 = User.objects.create_user("user_1")
        cls.album_page = reverse('Public Albums')
        cls.album_template = "albums/album_list.html"

    def setUp(self) -> None:
        self.expected_albums = []
        self.populate_albums()

    def test_get_all_public_albums(self):
        response = self.client.get(self.album_page)
        self.assertQuerysetEqual(values=self.expected_albums, qs=response.context['album_list'])

    def test_get_only_public_albums_logged_in(self):
        self.client.force_login(self.user_0)
        response = self.client.get(self.album_page)
        self.assertQuerysetEqual(values=self.expected_albums, qs=response.context['album_list'])


class AlbumFormTestCase(TestCase):
    # TODO: Need tests for validators
    pass
