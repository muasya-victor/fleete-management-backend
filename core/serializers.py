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
        fields = ['id', 'email', 'phone_code', 'phone_number', 'username', 'password', 
                   'user_type']
        write_only_fields = ['password']
    
        
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

    def validate(self, data):
        request = self.context.get("request", None)
        if request is None:
            raise serializers.ValidationError("Request Object is invalid. ")
        user = request.user

        # Access the service_type from the validated data
        service_type = data.get('service_type')

        # Access the subservice_name from the validated data
        subservice_name = data.get('subservice_name')

        # Validate based on the service_type and subservice_name
        if service_type and subservice_name:
            if service_type.service_type == 'Regular Maintenance' and subservice_name not in ['Oil change', 'Fluid checks']:
                raise serializers.ValidationError("Invalid subservice_name for Regular Maintenance service_type.")

        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        service_type = validated_data.pop('service_type_id', None)
        service_type = SubService.objects.create(service_type= service_type, **validated_data)

        return service_type
    

    def update(self, instance, validated_data):
        service_type = validated_data.pop('service_type_id', None)
        service_type = super().update(instance, validated_data)
        return service_type
    