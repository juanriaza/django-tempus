from __future__ import unicode_literals

from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User

from tempus.utils import tempus_dumps


class TestAutoLogin(TestCase):
    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)

        self.username = 'john'
        self.email = 'lennon@thebeatles.com'
        self.password = 'password'
        self.user = User.objects.create_user(self.username,
                                             self.email,
                                             self.password)
        self.token_data = tempus_dumps(self.user.pk)

    def test_redirect(self):
        response = self.client.get('/user/',
                                   {'tempus': self.token_data})
        self.assertRedirects(response, '/user/')

    def test_login_user(self):
        response = self.client.get('/user/',
                                   {'tempus': self.token_data},
                                   follow=True)
        self.assertEqual(response.content, b'john')

    def test_bad_token(self):
        response = self.client.get('/user/',
                                   {'tempus': 'WRONGTOKEN'},
                                   follow=True)
        self.assertEqual(response.content, b'anonymous')

    def test_no_token(self):
        response = self.client.get('/user/')
        self.assertEqual(response.content, b'anonymous')


class TestPromo(TestCase):
    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        promo_data = {'discount': 5}
        self.token_data = tempus_dumps(promo_data)

    def test_redirect(self):
        response = self.client.get('/promo/',
                                   {'promo': self.token_data})
        self.assertRedirects(response, '/promo/')

    def test_promotion(self):
        response = self.client.get('/promo/',
                                   {'promo': self.token_data},
                                   follow=True)
        self.assertEqual(response.content, b'20')

    def test_bad_token(self):
        response = self.client.get('/promo/',
                                   {'promo': 'WRONGTOKEN'},
                                   follow=True)
        self.assertEqual(response.content, b'25')

    def test_no_token(self):
        response = self.client.get('/promo/')
        self.assertEqual(response.content, b'25')
