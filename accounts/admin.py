from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_staff",
        "is_active",
    )

    # Filters for the admin list view
    list_filter = ("user_type", "is_staff", "is_active", "date_joined")

    # Search fields
    search_fields = ("username", "first_name", "last_name", "email")

    # Fields to display in the admin form
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {"fields": ("user_type", "phone", "address", "date_of_birth", "avatar")},
        ),
    )

    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {"fields": ("user_type", "phone", "address", "date_of_birth", "avatar")},
        ),
    )
