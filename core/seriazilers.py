import os
from datetime import timedelta

import requests
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import ( User, VehicleService, ServiceType, SubService, Vehicle, VehiclePart)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_code', 'phone_number', 'username', 
                   'user_type']
    
        
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ServiceType
        fields = ['id', 'service_type']

class SubServiceSerializer(serializers.ModelSerializer):
    service_type_id= serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ServiceType.objects.all(), required=False)
    service_type = ServiceTypeSerializer(read_only=True)

    class Meta:
        model = SubService
        fields = ['id', 'service_type_id', 'service_type', 'subservice_name']

    def create(self, validated_data):
        user = self.context['request'].user
        service_type = validated_data.pop('service_type_id', None)
        service_type = SubService.objects.create(service_type= service_type, **validated_data)

        return service_type
    
    def update(self, instance, validated_data):
        service_type = validated_data.pop('service_type_id', None)
        service_type = super().update(instance, validated_data)
        return service_type
     