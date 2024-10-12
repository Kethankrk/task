from rest_framework import serializers
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    cpassword = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "cpassword"]

    def validate(self, attrs):
        cpassword = attrs.get("cpassword")
        password = attrs.get("password")

        if cpassword != password:
            raise serializers.ValidationError("password and confirm password mismatch")

        return attrs

    def create(self, validated_data: dict):
        validated_data.pop("cpassword")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    password = serializers.CharField()
    cpassword = serializers.CharField()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]
