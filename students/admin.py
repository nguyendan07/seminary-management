from django.contrib import admin

from .models import Student, StudentNote


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
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "get_full_name",
        "current_year",
        "status",
        "entry_year",
        "parish",
    )
    list_filter = ("status", "current_year", "entry_year", "parish__diocese", "parish")
    search_fields = (
        "student_id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "hometown",
    )
    ordering = ("student_id",)

    inlines = [StudentNoteInline]

    fieldsets = (
        (
            "Thông tin cơ bản",
            {"fields": ("user", "student_id", "entry_year", "current_year", "status")},
        ),
        (
            "Thông tin cá nhân",
            {"fields": ("hometown", "family_situation", "previous_education")},
        ),
        (
            "Thông tin tâm linh",
            {"fields": ("baptism_date", "confirmation_date", "parish", "community")},
        ),
        ("Thông tin rửa tội", {"fields": ("baptism_parish", "baptism_priest")}),
    )

    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Họ tên")
    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ("created_at", "updated_at")
        return self.readonly_fields


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
        "student__student_id",
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
