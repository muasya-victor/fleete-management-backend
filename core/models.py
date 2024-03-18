from django.db import models
import django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import os
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.crypto import get_random_string

phone_validator = RegexValidator(r"^\d{9,10}$", "Enter a valid phone number.")

phone_code_validator = RegexValidator(r"^\+\d{1,3}$")

class UtilColumnsModel(models.Model):
    """Abstract model for created_at & updated_at fields."""

    created_at = models.DateTimeField(
        default=django.utils.timezone.now, null=True, blank=True
    )
    updated_at = models.DateTimeField(
        blank=True, null=True, default=django.utils.timezone.now
    )
    is_active = models.BooleanField(default=True)



class User(AbstractUser):
    user_email = models.EmailField(max_length=100, unique=True)
    user_phone_code = models.CharField(
        max_length=4, validators=[phone_code_validator], blank=True, null=True , default= "+254"
    )
    user_first_name = models.CharField(max_length= 30, blank=True, null= True)
    user_last_name = models.CharField(max_length = 30, blank= True, null= True)
    user_avatar = models.FileField(blank=True, null= True)
    username = models.CharField(max_length = 56,  unique=True,  default = 'admin')
    password = models.CharField(max_length=128, default='123456')
    user_phone_number = models.CharField(
        max_length=10, validators=[phone_validator], blank=True, null=True, unique=True
    )
    USER_TYPES = [
        ('vehicle_owner', 'Vehicle Owner'),
        ('mechanic', 'Mechanic'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES,default='mechanic')

    def __str__(self):
        return self.username


class ServiceType(models.Model):
    SERVICE_CHOICES = [
        ('Regular Maintenance', 'Regular Maintenance'),
        ('Diagnostic Services', 'Diagnostic Services'),
        ('Brake Services', 'Brake Services'),
        ('Tire Services', 'Tire Services'),
        ('Exhaust System Services', 'Exhaust System Services'),
        ('Transmission Services', 'Transmission Services'),
        ('Electrical System Services', 'Electrical System Services'),
        ('Cooling System Services', 'Cooling System Services'),
        ('Air Conditioning Services', 'Air Conditioning Services'),
        ('Fuel System Services', 'Fuel System Services'),
        ('Suspension and Steering Services', 'Suspension and Steering Services'),
        ('Engine Services', 'Engine Services'),
        ('Safety Inspections', 'Safety Inspections'),
        ('Preventive Maintenance', 'Preventive Maintenance'),
    ]

    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)

    def __str__(self):
        return self.service_type



class SubService(models.Model):
    SERVICE_CHOICES = [
        ('Oil change', 'Oil change'),
        ('Fluid checks', 'Fluid checks'),
        ('Tire rotation', 'Tire rotation'),
        ('Battery inspection', 'Battery inspection'),
        ('Engine diagnostics', 'Engine diagnostics'),
        ('Computerized vehicle inspection', 'Computerized vehicle inspection'),
        ('Brake pad replacement', 'Brake pad replacement'),
        ('Brake fluid flush', 'Brake fluid flush'),
        ('Brake system inspection', 'Brake system inspection'),
        ('Tire replacement', 'Tire replacement'),
        ('Wheel alignment', 'Wheel alignment'),
        ('Tire balancing', 'Tire balancing'),
        ('Exhaust system repair', 'Exhaust system repair'),
        ('Catalytic converter replacement', 'Catalytic converter replacement'),
        ('Transmission fluid change', 'Transmission fluid change'),
        ('Transmission system inspection and repair', 'Transmission system inspection and repair'),
        ('Battery replacement', 'Battery replacement'),
        ('Alternator repair', 'Alternator repair'),
        ('Radiator flush', 'Radiator flush'),
        ('Thermostat replacement', 'Thermostat replacement'),
        ('A/C recharge', 'A/C recharge'),
        ('A/C system inspection and repair', 'A/C system inspection and repair'),
        ('Fuel injector cleaning', 'Fuel injector cleaning'),
        ('Fuel filter replacement', 'Fuel filter replacement'),
        ('Shock and strut replacement', 'Shock and strut replacement'),
        ('Power steering fluid flush', 'Power steering fluid flush'),
        ('Engine tune-up', 'Engine tune-up'),
        ('Timing belt replacement', 'Timing belt replacement'),
        ('State vehicle inspections', 'State vehicle inspections'),
        ('General safety inspections', 'General safety inspections'),
        ('Comprehensive vehicle checkups', 'Comprehensive vehicle checkups'),
     
    ]

    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.CASCADE
    )
    subservice_name = models.CharField(max_length=100, choices=SERVICE_CHOICES, default=None)


    def __str__(self):
        return f"{self.service_type} - {self.subservice_name}"

  

class VehiclePart(models.Model):
    vehicle_part_name = models.CharField(max_length=255)
    vehicle_part_comments = models.TextField(blank=True, null=True)
    vehicle_part_working_condition = models.BooleanField(default=True)
    vehicle_part_sub_service= models.ForeignKey(SubService, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.vehicle_part_name

class VehicleService(models.Model):
    user =models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vehicle_next_service_date = models.DateField()
    vehicle_previous_service_date = models.DateField()
    vehicle_part = models.ForeignKey(VehiclePart, on_delete= models.CASCADE)

    def __str__(self):
        return f"VehicleService {self.vehicle_part}"


class Vehicle(models.Model):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
    
    CONDITION_CHOICES = [
        ('healthy', 'Healthy'),
        ('unhealthy', 'Unhealthy'),
    ]

    vehicle_plate_number = models.CharField(max_length=255, unique=True)
    vehicle_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_parts = models.ForeignKey(VehiclePart, on_delete=models.CASCADE)
    vehicle_general_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default=HEALTHY)
    vehicle_type = models.CharField(max_length=40)
    vehicle_model = models.CharField(max_length=255)
    vehicle_engine_number = models.CharField(max_length=255, unique=True)
    vehicle_color = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self. vehicle_plate_number} - {self.vehicle_model}"
