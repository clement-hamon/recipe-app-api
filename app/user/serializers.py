from rest_framework import serializers
from core.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 3}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
