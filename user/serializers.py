from abc import ABC
from django.contrib.auth import authenticate
from django.forms import forms
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from user.models import User
import logging

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'phnno', 'password', 'city']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        try:
            return User.objects.create_user(**validated_data)
        except Exception as ex:
            logger.exception(ex)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise serializers.ValidationError("Incorrect Credentials")
        validated_data.update({'user': user})
        self.context.update({'user': user})
        return user
