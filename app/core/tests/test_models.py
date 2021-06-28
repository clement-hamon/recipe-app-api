from django.test import TestCase

from core.models import User


class UserTest(TestCase):

    def test_create_user(self):
        """ create a user and test if the password is correct """
        email = "clement@test.com"
        password = "fakepassword"

        user: User = User.objects.create_user(email=email, password=password)

        self.assertTrue(user.check_password("fakepassword"))
