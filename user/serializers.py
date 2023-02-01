from abc import ABC
from django.contrib.auth import authenticate
from django.forms import forms
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from user.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'phnno', 'password', 'city']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception('Invalid Credentials')
        return user


class ResetPasswordRequestSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)

    class Meta:
        fields = ['password']
    # def validate (self,attrs):
    #     try:
    # password.get('password')
