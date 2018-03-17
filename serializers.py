# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 04:45:41 2018

@author: Mark
"""

from rest_framework import serializers
from .models import Newss
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newss
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create(email=validated_data['email'],username=validated_data['username'],password = make_password(validated_data['password']))
        return user
