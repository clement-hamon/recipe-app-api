from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def test_create_user__valid(self):
        payload = {
            'email': 'some@email.com',
            'password': 'my_password',
            'name': 'some name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user__already_exists(self):
        payload = {
            'email': 'some@email.com',
            'password': 'my_password',
            'name': 'some name'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user__password_too_short(self):
        payload = {
            'email': 'some@email.com',
            'password': 'my',
            'name': 'some name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_create_user__token_created(self):
        """ test that the token is created when the user is created """
        payload = {
            'email': 'some@email.com',
            'password': 'my_password',
            'name': 'some name'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_invalid_password(self):
        payload = {'email': 'some@email.com', 'password': 'my_password', 'name': 'some name'}
        create_user(**payload)

        wrong_payload = {
                        'email': 'some@email.com',
                        'password': 'not_my_password',
                        'name': 'some name'
                        }
        res = self.client.post(TOKEN_URL, wrong_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_user(self):
        payload = {'email': 'some@email.com', 'password': 'my_password', 'name': 'some name'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_none_existing_password(self):
        payload = {'email': 'some@email.com', 'password': '', 'name': 'some name'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
