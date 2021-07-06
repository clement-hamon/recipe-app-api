from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def test_create_user__valid(self):
        payload = {
            'email': 'some@email.com',
            'password': 'my_password',
            'name': 'clement'
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
            'name': 'clement'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user__password_too_short(self):
        payload = {
            'email': 'some@email.com',
            'password': 'my',
            'name': 'clement'
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
            'name': 'clement'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_invalid_password(self):
        payload = {'email': 'some@email.com', 'password': 'my_password', 'name': 'clement'}
        create_user(**payload)

        wrong_payload = {
            'email': 'some@email.com',
            'password': 'not_my_password',
                        'name': 'clement'
        }
        res = self.client.post(TOKEN_URL, wrong_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_user(self):
        payload = {'email': 'some@email.com', 'password': 'my_password', 'name': 'clement'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_none_existing_password(self):
        payload = {'email': 'some@email.com', 'password': '', 'name': 'clement'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_user_me_info_unauthorized(self):
        """Test that the user need to be logged in to access user endpoint"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        # create user
        payload = {'email': 'some@email.com', 'password': 'my_password', 'name': 'clement'}
        self.user = create_user(**payload)
        # force loggin
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_access_user_me_info_authorized(self):
        """Test that a logged in user can access user endpoint"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
    
    def test_post_me_not_allowed(self):
        """Test that the POST method is not allowed"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test modification of the user info for authenticated user"""
        payload = {'name': 'raymon', 'password': 'new_password'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
