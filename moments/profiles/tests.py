from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class UserDetailTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.user = User.objects.create_user(username="test_user")
        cls.user_page = reverse('User Profile', args=[cls.user.username])
        cls.user_template = 'auth/user_detail.html'

    def tearDown(self) -> None:
        self.client.logout()

    def test_get_profile_anonymous(self):
        """
        Tests when an anonymous user visits a user profile
        """
        with self.assertTemplateUsed(self.user_template):
            self.client.get(self.user_page)

    def test_get_own_profile(self):
        """
        Tests when a user visits their own user profile
        """
        self.client.force_login(self.user)
        with self.assertTemplateUsed(self.user_template):
            self.client.get(self.user_page)

    def test_get_other_profile_logged_in(self):
        """
        Tests when a user visits another user's profile
        """
        other_user = User.objects.create(username="other_user")
        self.client.force_login(other_user)
        with self.assertTemplateUsed(self.user_template):
            self.client.get(self.user_page)
