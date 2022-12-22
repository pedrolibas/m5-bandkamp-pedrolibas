from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators = [UniqueValidator(User.objects.all(), "This field must be unique.")])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "is_superuser"]
        read_only_fields = ["is_superuser"]
        write_only_fields = ["password"]
        extra_kwargs = {"password": {"write_only": True}, "username": {"validators": [UniqueValidator(queryset=User.objects.all(), message="A user with that username already exists.")]}}

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance