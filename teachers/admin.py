from django import forms
from django.contrib import admin

from accounts.admin import BaseUserCreationForm, BaseProfileAdmin

from .models import Teacher


class TeacherCreationForm(BaseUserCreationForm):
    username = forms.CharField(max_length=150, label="Mã giáo viên")

    class Meta:
        model = Teacher
        fields = [
            "hire_date",
            "position",
            "education_background",
            "specialization",
            "experience",
            "office_room",
            "consultation_hours",
        ]

    def save(self, commit=True):
        user = self.create_user("teacher")
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher


@admin.register(Teacher)
class TeacherAdmin(BaseProfileAdmin):
    creation_form_class = TeacherCreationForm

    list_display = (
        "get_user_id",
        "get_full_name",
        "position",
        "hire_date",
        "office_room",
    )
    list_filter = ("position", "hire_date")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "specialization",
    )
    ordering = ("user__username",)

    fieldsets = (
        ("Thông tin người dùng", {"fields": ("user",)}),
        ("Thông tin cơ bản", {"fields": ("hire_date", "position")}),
        (
            "Thông tin học vấn và chuyên môn",
            {"fields": ("education_background", "specialization", "experience")},
        ),
        ("Thông tin công việc", {"fields": ("office_room", "consultation_hours")}),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Adding new teacher
            return (
                (
                    "Thông tin người dùng",
                    {
                        "fields": (
                            "username",
                            "first_name",
                            "last_name",
                            "email",
                            "password",
                            "avatar",
                        )
                    },
                ),
                ("Thông tin cơ bản", {"fields": ("hire_date", "position")}),
                (
                    "Thông tin học vấn và chuyên môn",
                    {
                        "fields": (
                            "education_background",
                            "specialization",
                            "experience",
                        )
                    },
                ),
                (
                    "Thông tin công việc",
                    {"fields": ("office_room", "consultation_hours")},
                ),
            )
        return self.fieldsets

    @admin.display(description="Mã giáo viên")
    def get_user_id(self, obj):
        return super().get_user_id(obj)
