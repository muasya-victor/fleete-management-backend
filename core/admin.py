from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import   User, VehicleService , ServiceType ,SubService, VehiclePart , Vehicle 


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Other Fields",
            {
                "fields": (
                    "phone_code",
                    "phone_number",
                    "user_type",
                   
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Other Fields",
            {
                "fields": (
                    "phone_code",
                    "phone_number",
                    "user_type",
                    "email",
                   

                )
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(VehicleService)
admin.site.register(ServiceType)
admin.site.register(Vehicle)
admin.site.register(VehiclePart)
admin.site.register(SubService)

