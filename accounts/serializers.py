from rest_framework import serializers
from .models import User


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class MeUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class MeResponseSerializer(serializers.Serializer):
    user = MeUserSerializer()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "nickname", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            email=validated_data["email"],
        )
        return user
