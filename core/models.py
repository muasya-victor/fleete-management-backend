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


class VehicleService(models.Model):
    id = models.AutoField(primary_key=True)
    next_service_date = models.DateTimeField()
    previous_service_date = models.DateTimeField()
    service_type = models.IntegerField()

    def __str__(self):
        return f"VehicleService {self.id}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_code = models.CharField(
        max_length=4, validators=[phone_code_validator], blank=True, null=True
    )
    username = models.CharField(max_length = 128, unique =True,  default = 'admin')
    password = models.CharField(max_length=128, default='123456')
    phone_number = models.CharField(
        max_length=10, validators=[phone_validator], blank=True, null=True, unique=True
    )

    