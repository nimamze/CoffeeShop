from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["phone", "email", "password", "first_name", "last_name"]


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
