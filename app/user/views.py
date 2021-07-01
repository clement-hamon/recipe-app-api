from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    "View for creating a new user"
    serializer_class = UserSerializer
