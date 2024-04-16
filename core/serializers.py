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
        fields = ['id', 'user_first_name', 'user_last_name','user_email', 'user_phone_code', 'user_phone_number', 'username', 'password', 
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
        service_type.save()
        if service_type is not None:
            instance.service_type =service_type
        instance.save()
        return instance

class VehiclePartSerializer(serializers.ModelSerializer):
    vehicle_part_sub_service= serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=SubService.objects.all(), required=False)
    # vehicle_part_sub_service = SubServiceSerializer(read_only=True)
    class Meta:
        model = VehiclePart
        fields = ['id', 'vehicle_part_sub_service', 'vehicle_part_name', 'vehicle_part_comments', 
                  'vehicle_part_working_condition']
        
    def validate(self, data):
        request = self.context.get("request", None)
        if request is None:
            raise serializers.ValidationError("Request object is invalid.")
        user = request.user
        # Check if the user is a not a mechanic
        if user.user_type != "mechanic":
            raise serializers.ValidationError("Only mechanics can inspect and write the report on vehicle wellbeing.")
        return data
        
    
    def create(self, validated_data):
        # Extract the sub_service_id from validated_data
        vehicle_part_sub_service = validated_data.pop('vehicle_part_sub_service', None)
        

        vehicle_part = VehiclePart.objects.create(vehicle_part_sub_service=vehicle_part_sub_service, **validated_data)

        return vehicle_part
    
    def update(self, instance, validated_data):

        return super().update(instance, validated_data)

class VehicleServiceSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(write_only= True, 
            # queryset=User.objects.all(), required= False)
    vehicle_part = serializers.PrimaryKeyRelatedField(write_only = True,
                         queryset = VehiclePart.objects.all(), required = False)
    class Meta:
        model = VehicleService
        fields = ['id',  'vehicle_next_service_date', 'vehicle_previous_service_date','vehicle_part']


    def validate(self, data):
        request =self.context.get('request', None)
        vehicle_next_service_date = data.get('vehicle_next_service_date')
        vehicle_previous_service_date = data.get('vehicle_previous_service_date')
        if request is None:
            raise serializers.ValidationError("Request object is invalid.")
        user = request.user
        current_date = timezone.now().date()

        if user.user_type != 'mechanic':
            raise serializers.ValidationError('only mechanics can service the vehicle')
            
        if vehicle_next_service_date and vehicle_next_service_date <= current_date:
            raise serializers.ValidationError('Next service date cannot be in the past or today.')
        
        if vehicle_previous_service_date and vehicle_previous_service_date >= current_date:
            raise serializers.ValidationError('Previous service date cannot be in the future.')
        
        return data

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            raise serializers.ValidationError("Request object is invalid.")
        user = request.user
       
        vehicle_part= validated_data.pop('vehicle_part', None)
        vehicle_service = VehicleService.objects.create(vehicle_part=vehicle_part, **validated_data)

        return vehicle_service
    
    def update(self, instance, validated_data):
        vehicle_part = validated_data.pop('vehicle_part', None)
        vehicle_service = super().update(instance, validated_data)
        vehicle_service.save()
        if vehicle_part is not None:
            instance.vehicle_part = vehicle_part
        instance.save()
        return instance

class VehicleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_plate_number', 'vehicle_owner', 'vehicle_parts',
                  'vehicle_general_condition', 'vehicle_type', 'vehicle_model',
                  'vehicle_engine_number', 'vehicle_color']

    def validate(self, data):
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError("Request object is invalid.")
        
        user = request.user
        
        if user.user_type != 'mechanic':
            raise serializers.ValidationError("Only mechanics can access this endpoint.")
        print(user)

        # Ensure the vehicle owner's user type is 'vehicle_owner'
        vehicle_owner = data.get('vehicle_owner')
        if vehicle_owner and vehicle_owner.user_type != 'vehicle_owner':
            raise serializers.ValidationError("Vehicle owner must have user type 'vehicle_owner'.")
        print(vehicle_owner)
        return data

    def create(self, validated_data):
        vehicle = Vehicle.objects.create(**validated_data)
        return vehicle
    
    def update(self, instance, validated_data):
        vehicle = super().update(instance, validated_data)
        vehicle.save()

        instance.save()
        return instance