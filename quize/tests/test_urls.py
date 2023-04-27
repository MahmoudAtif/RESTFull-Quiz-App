from rest_framework.test import APITestCase
from quize.views import *
from django.urls import resolve, reverse

class TestUrl(APITestCase):

    def test_signin_url(self):
        url=reverse('signin')
        self.assertEqual(resolve(url).func.view_class, SignInView)

    def test_signup_url(self):
        url=reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_change_password_url(self):
        url=reverse('change_password')
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)

    def test_categories_url(self):
        url=reverse('categories')
        self.assertEqual(resolve(url).func.view_class, CategoryView)
