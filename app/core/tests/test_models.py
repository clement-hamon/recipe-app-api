from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import User


class UserTest(TestCase):

    def test_create_user(self):
        """ create a user and test if the password is correct """
        email = "clement@test.com"
        password = "fakepassword"

        user: User = get_user_model().objects.create_user(email=email, password=password)

        self.assertTrue(user.check_password("fakepassword"))

    def test_new_user_email_normalized(self):
        """ test that the email is norm"""
        email = "test@HOSTDOMAIN.fr"
        user: User = get_user_model().objects.create_user(email, "test132")

        self.assertEquals(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ test that an error is thrown if the email is None"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test132")

    def test_new_super_user(self):
        """ An operator can create a super user"""
        email = "test@hostdomain.com"
        super_user: User = get_user_model().objects.create_superuser(email, "test123")

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
