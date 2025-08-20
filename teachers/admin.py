from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "teacher_id",
        "get_full_name",
        "position",
        "hire_date",
        "office_room",
        "is_active",
    )
    list_filter = ("position", "hire_date", "is_active")
    search_fields = (
        "teacher_id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "specialization",
    )
    ordering = ("teacher_id",)

    fieldsets = (
        (
            "Thông tin cơ bản",
            {"fields": ("user", "teacher_id", "hire_date", "position", "is_active")},
        ),
        (
            "Thông tin học vấn và chuyên môn",
            {"fields": ("education_background", "specialization", "experience")},
        ),
        ("Thông tin công việc", {"fields": ("office_room", "consultation_hours")}),
    )

    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Họ tên")
    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ("created_at", "updated_at")
        return self.readonly_fields
