from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model

from .models import Teacher

User = get_user_model()


class TeacherCreationForm(forms.ModelForm):
    # User fields
    username = forms.CharField(max_length=150, label="Mã giáo viên")
    first_name = forms.CharField(max_length=150, label="Tên")
    last_name = forms.CharField(max_length=150, label="Họ")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    avatar = forms.ImageField(required=False, label="Ảnh đại diện")

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
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            user_type="teacher",
        )
        # Set avatar if provided
        if self.cleaned_data.get("avatar"):
            user.avatar = self.cleaned_data["avatar"]
            user.save()
        
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "get_teacher_id",
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
        (
            "Thông tin người dùng",
            {"fields": ("user",)},
        ),
        (
            "Thông tin cơ bản",
            {"fields": ("hire_date", "position")},
        ),
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
                    {"fields": ("username", "first_name", "last_name", "email", "password", "avatar")},
                ),
                (
                    "Thông tin cơ bản",
                    {"fields": ("hire_date", "position")},
                ),
                (
                    "Thông tin học vấn và chuyên môn",
                    {"fields": ("education_background", "specialization", "experience")},
                ),
                ("Thông tin công việc", {"fields": ("office_room", "consultation_hours")}),
            )
        return self.fieldsets  # Editing existing teacher

    @admin.display(description="Mã giáo viên")
    def get_teacher_id(self, obj):
        return obj.user.username

    @admin.display(description="Họ tên")
    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ("created_at", "updated_at")
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = TeacherCreationForm
        return super().get_form(request, obj, **kwargs)
