# Pip imports
from django.contrib.auth.models import User
from rest_framework import serializers


class UserInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    verified_email = serializers.BooleanField()
    name = serializers.CharField()
    given_name = serializers.CharField()
    family_name = serializers.CharField()
    picture = serializers.CharField()

    class Meta:
        user_model = User
        fields = ["id", "email", "verified_email", "name", "given_name", "family_name", "picture"]
