from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import ReferralCode


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "username", "first_name", "last_name", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email must be unique.")
        return value

    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ["user", "code", "created_at", "expiration_date", "is_active"]
