from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import   User, VehicleService
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Other Fields",
            {
                "fields": (
                    "phone_number",
                    "company"
                   
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Other Fields",
            {
                "fields": (
                    "phone_number",
                    "company"

                )
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(VehicleService)
