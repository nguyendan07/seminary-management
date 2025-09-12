from django import forms
from django.contrib import admin

from accounts.admin import BaseUserCreationForm, BaseProfileAdmin

from .models import Student, StudentNote


class StudentCreationForm(BaseUserCreationForm):
    username = forms.CharField(max_length=150, label="Mã chủng sinh")

    class Meta:
        model = Student
        fields = [
            "entry_year",
            "current_year",
            "status",
            "hometown",
            "baptism_name",
            "baptism_date",
            "confirmation_date",
            "parish",
            "community",
        ]

    def save(self, commit=True):
        user = self.create_user("student")
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student


class StudentNoteInline(admin.TabularInline):
    model = StudentNote
    extra = 0
    fields = ("note_type", "title", "content", "is_private", "created_by")
    readonly_fields = ("created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Student)
class StudentAdmin(BaseProfileAdmin):
    creation_form_class = StudentCreationForm

    list_display = (
        "get_user_id",
        "get_full_name",
        "current_year",
        "status",
        "entry_year",
        "parish",
    )
    list_filter = ("status", "current_year", "entry_year", "parish__diocese", "parish")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "hometown",
    )
    ordering = ("user__username",)
    inlines = [StudentNoteInline]

    fieldsets = (
        ("Thông tin người dùng", {"fields": ("user", "hometown")}),
        ("Thông tin cơ bản", {"fields": ("entry_year", "current_year", "status")}),
        (
            "Thông tin tâm linh",
            {
                "fields": (
                    "baptism_name",
                    "baptism_date",
                    "confirmation_date",
                    "parish",
                    "community",
                )
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Adding new student
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
                            "hometown",
                        )
                    },
                ),
                (
                    "Thông tin cơ bản",
                    {"fields": ("entry_year", "current_year", "status")},
                ),
                (
                    "Thông tin tâm linh",
                    {
                        "fields": (
                            "baptism_name",
                            "baptism_date",
                            "confirmation_date",
                            "parish",
                            "community",
                        )
                    },
                ),
            )
        return self.fieldsets

    @admin.display(description="Mã chủng sinh")
    def get_user_id(self, obj):
        return super().get_user_id(obj)


@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_student_name",
        "note_type",
        "created_by",
        "is_private",
        "created_at",
    )
    list_filter = ("note_type", "is_private", "created_at")
    search_fields = (
        "title",
        "content",
        "student__user__first_name",
        "student__user__last_name",
    )
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Thông tin ghi chú",
            {"fields": ("student", "note_type", "title", "content", "is_private")},
        ),
        (
            "Thông tin tạo",
            {"fields": ("created_by", "created_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_by", "created_at")

    @admin.display(description="Học sinh")
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
