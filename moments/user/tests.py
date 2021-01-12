from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class HomeTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "test_user"
        cls.password = "test_password"
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        cls.home_page = reverse('Home')

    def test_home_anonymous(self):
        with self.assertTemplateUsed('splash.html'):
            self.client.get(self.home_page)

    def test_home_logged_in(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed('welcome.html'):
            self.client.get(self.home_page)


class UserSignUpTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "test_user"
        cls.password = "test_password"
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        cls.home_page = reverse('Home')
        cls.sign_up_page = reverse('Sign Up')

    def test_sign_up_get_anonymous(self):
        with self.assertTemplateUsed('sign-up.html'):
            self.client.get(self.sign_up_page, follow=True)
            self.assertTemplateNotUsed('welcome.html')

    def test_sign_up_get_logged_in(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed('welcome.html'):
            self.client.get(self.sign_up_page, follow=True)
            self.assertTemplateNotUsed('sign-up.html')

    def test_sign_up_post_anonymous(self):
        username = 'user123'
        password = 'testpass123'
        request_data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        # Assert user does not already exist
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=username)

        response = self.client.post(self.sign_up_page, data=request_data)

        # Assert successful redirect to home page
        expected_response_status = 302
        self.assertEqual(expected_response_status, response.status_code)

        expected_redirect = self.home_page
        self.assertEqual(expected_redirect, response['Location'])

        # Assert user created and logged in
        test_user = User.objects.get(username=username)
        self.assertIsNotNone(test_user)
        self.assertTrue(test_user.is_authenticated)

    def test_sign_up_post_anonymous_validation(self):
        password = 'test_password123'
        request_data = {
            "username": self.username,
            "password1": password,
            "password2": password
        }
        # Assert user exists
        User.objects.get(username=self.username)

        response = self.client.post(self.sign_up_page, data=request_data)

        # Assert no redirect
        expected_response_status = 200
        self.assertEqual(expected_response_status, response.status_code)

        # Assert form validation error
        self.assertFormError(response, 'signup_form', 'username', 'A user with that username already exists.')

    def test_sign_up_post_logged_in(self):
        self.client.force_login(self.user)

        password = 'test_password'
        request_data = {
            "username": self.username,
            "password1": password,
            "password2": password
        }

        response = self.client.post(self.sign_up_page, data=request_data)

        # Assert successful redirect to home page
        expected_response_status = 302
        self.assertEqual(expected_response_status, response.status_code)

        expected_redirect = self.home_page
        self.assertEqual(expected_redirect, response['Location'])


class UserLoginTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "test_user"
        cls.password = "test_password"
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        cls.home_page = reverse('Home')
        cls.login_page = reverse('Login')

    def test_login_get_anonymous(self):
        with self.assertTemplateUsed('login.html'):
            self.client.get(self.login_page, follow=True)
            self.assertTemplateNotUsed('welcome.html')

    def test_login_get_logged_in(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed('welcome.html'):
            self.client.get(self.login_page, follow=True)
            self.assertTemplateNotUsed('login.html')

    def test_login_post_anonymous(self):
        response = self.client.post(self.login_page, data=dict(username=self.username, password=self.password))

        # Assert expected redirect
        expected_response_status = 302
        self.assertEqual(expected_response_status, response.status_code)
        expected_redirect = self.home_page
        self.assertEqual(expected_redirect, response['Location'])

        self.assertTrue(self.user.is_authenticated)

    def test_login_post_anonymous_redirect(self):
        redirect_path = '/foo'
        response = self.client.post(f"{self.login_page}?next={redirect_path}",
                                    data=dict(username=self.username,
                                              password=self.password))

        # Assert expected redirect
        expected_response_status = 302
        self.assertEqual(expected_response_status, response.status_code)
        expected_redirect = redirect_path
        self.assertEqual(expected_redirect, response['Location'])

        self.assertTrue(self.user.is_authenticated)

    def test_login_post_anonymous_validation(self):
        request_data = {
            "username": self.username,
            "password": f"bad_{self.password}"
        }
        response = self.client.post(self.login_page, data=request_data, follow=True)

        expected_error = "Please enter a correct username and password. Note that both fields may be case-sensitive."

        # Assert no redirect
        expected_response_status = 200
        self.assertEqual(expected_response_status, response.status_code)

        # Assert form validation error
        self.assertFormError(response, 'login_form', None, expected_error)


    def test_login_post_logged_in(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed('welcome.html'):
            self.client.post(self.login_page, data=dict(username=self.username, password=self.password), follow=True)
            self.assertTemplateNotUsed('login.html')
