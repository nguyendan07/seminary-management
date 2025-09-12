from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class BaseUserCreationForm(forms.ModelForm):
    """Base form for creating users with profile"""

    username = forms.CharField(max_length=150, label="Mã người dùng")
    first_name = forms.CharField(max_length=150, label="Tên")
    last_name = forms.CharField(max_length=150, label="Họ")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    avatar = forms.ImageField(required=False, label="Ảnh đại diện")

    def create_user(self, user_type):
        """Create user with given type"""
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            user_type=user_type,
        )
        # Set avatar if provided
        if self.cleaned_data.get("avatar"):
            user.avatar = self.cleaned_data["avatar"]
            user.save()
        return user


class BaseProfileAdmin(admin.ModelAdmin):
    """Base admin for profile models"""

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields) if self.readonly_fields else []
        if obj:  # editing an existing object
            readonly.extend(["created_at", "updated_at"])
        return readonly

    def get_form(self, request, obj=None, **kwargs):
        if obj is None and hasattr(self, "creation_form_class"):
            kwargs["form"] = self.creation_form_class
        return super().get_form(request, obj, **kwargs)

    @admin.display(description="Mã người dùng")
    def get_user_id(self, obj):
        return obj.user.username

    @admin.display(description="Họ tên")
    def get_full_name(self, obj):
        return obj.user.get_full_name()


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
