from django.contrib import admin
from django.utils.html import format_html
from .models import AcademicYear, Subject, Course, Enrollment, Assignment, Attendance


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "start_date",
        "end_date",
        "is_current",
        "courses_count",
        "created_at",
    ]
    list_filter = ["is_current", "start_date"]
    search_fields = ["name"]
    readonly_fields = ["created_at"]

    @admin.display(description="Số lớp học")
    def courses_count(self, obj):
        return obj.course_set.count()


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "category",
        "level",
        "credits",
        "year_taught",
        "is_required",
        "current_courses_count",
        "is_active",
    ]
    list_filter = ["category", "level", "is_required", "year_taught", "is_active"]
    search_fields = ["code", "name", "english_name"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["prerequisites"]

    fieldsets = [
        (
            "Thông tin cơ bản",
            {"fields": ["code", "name", "english_name", "category", "level"]},
        ),
        (
            "Thông tin học tập",
            {
                "fields": [
                    "credits",
                    "theory_hours",
                    "practice_hours",
                    "year_taught",
                    "is_required",
                ]
            },
        ),
        ("Mô tả", {"fields": ["description", "learning_objectives", "prerequisites"]}),
        ("Trạng thái", {"fields": ["is_active"]}),
        ("Metadata", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Lớp hiện tại")
    def current_courses_count(self, obj):
        count = obj.current_courses_count
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>', count
            )
        return count


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "subject",
        "class_code",
        "instructor",
        "academic_year",
        "semester",
        "enrolled_count",
        "max_students",
        "status",
        "is_active",
    ]
    list_filter = [
        "academic_year",
        "semester",
        "status",
        "subject__category",
        "is_active",
    ]
    search_fields = [
        "subject__name",
        "subject__code",
        "class_code",
        "instructor__user__first_name",
        "instructor__user__last_name",
    ]
    readonly_fields = ["created_at", "updated_at", "enrolled_count", "available_slots"]

    fieldsets = [
        (
            "Thông tin cơ bản",
            {
                "fields": [
                    "subject",
                    "instructor",
                    "academic_year",
                    "semester",
                    "class_code",
                ]
            },
        ),
        ("Cấu hình lớp học", {"fields": ["max_students", "classroom", "schedule"]}),
        (
            "Thời gian",
            {
                "fields": [
                    "start_date",
                    "end_date",
                    "registration_start",
                    "registration_end",
                ]
            },
        ),
        (
            "Đánh giá",
            {
                "fields": [
                    "midterm_weight",
                    "final_weight",
                    "assignment_weight",
                    "attendance_required",
                ]
            },
        ),
        ("Trạng thái", {"fields": ["status", "is_active", "notes"]}),
        (
            "Thống kê",
            {"fields": ["enrolled_count", "available_slots"], "classes": ["collapse"]},
        ),
        ("Metadata", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Số sinh viên đã đăng ký")
    def enrolled_count(self, obj):
        count = obj.enrolled_count
        if obj.is_full:
            return format_html(
                '<span style="color: red; font-weight: bold;">{}</span>', count
            )
        elif count > obj.max_students * 0.8:  # Gần đầy (>80%)
            return format_html(
                '<span style="color: orange; font-weight: bold;">{}</span>', count
            )
        return count


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = [
        "enrollment_date",
        "overall_score",
        "letter_grade",
        "attendance_rate",
    ]
    fields = [
        "student",
        "status",
        "midterm_score",
        "final_score",
        "overall_score",
        "letter_grade",
        "attendance_count",
        "total_sessions",
    ]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "course",
        "overall_score",
        "letter_grade",
        "attendance_rate",
        "status",
        "enrollment_date",
    ]
    list_filter = [
        "status",
        "course__academic_year",
        "course__semester",
        "course__subject__category",
        "letter_grade",
    ]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__student_id",
        "course__subject__name",
    ]
    readonly_fields = ["enrollment_date", "updated_at", "overall_score", "letter_grade"]

    fieldsets = [
        (
            "Thông tin cơ bản",
            {"fields": ["student", "course", "enrollment_date", "status"]},
        ),
        (
            "Điểm số",
            {
                "fields": [
                    "assignment_scores",
                    "midterm_score",
                    "final_score",
                    "overall_score",
                    "letter_grade",
                ]
            },
        ),
        (
            "Chuyên cần",
            {"fields": ["attendance_count", "total_sessions", "participation_score"]},
        ),
        ("Ghi chú", {"fields": ["instructor_notes", "withdrawal_reason"]}),
        (
            "Metadata",
            {"fields": ["completion_date", "updated_at"], "classes": ["collapse"]},
        ),
    ]

    @admin.display(description="Điểm chuyên cần")
    def attendance_rate(self, obj):
        rate = obj.attendance_rate
        if rate < 50:
            return format_html(
                '<span style="color: red; font-weight: bold;">{:.1f}%</span>', rate
            )
        elif rate < 80:
            return format_html(
                '<span style="color: orange; font-weight: bold;">{:.1f}%</span>', rate
            )
        else:
            return format_html(
                '<span style="color: green; font-weight: bold;">{:.1f}%</span>', rate
            )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "course",
        "type",
        "due_date",
        "max_score",
        "weight",
        "is_active",
    ]
    list_filter = ["type", "course__academic_year", "course__semester", "is_active"]
    search_fields = ["title", "course__subject__name", "course__class_code"]
    readonly_fields = ["assigned_date", "created_at"]

    fieldsets = [
        ("Thông tin cơ bản", {"fields": ["course", "title", "type", "description"]}),
        ("Thời gian", {"fields": ["assigned_date", "due_date"]}),
        ("Điểm số", {"fields": ["max_score", "weight"]}),
        ("Tài liệu", {"fields": ["instruction_file"]}),
        ("Trạng thái", {"fields": ["is_active"]}),
    ]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "course",
        "date",
        "session_number",
        "status",
        "recorded_by",
    ]
    list_filter = ["status", "date", "course__academic_year", "course__semester"]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "course__subject__name",
    ]
    readonly_fields = ["created_at"]
    date_hierarchy = "date"

    fieldsets = [
        (
            "Thông tin cơ bản",
            {"fields": ["course", "student", "date", "session_number"]},
        ),
        ("Điểm danh", {"fields": ["status", "notes", "recorded_by"]}),
        ("Metadata", {"fields": ["created_at"], "classes": ["collapse"]}),
    ]
