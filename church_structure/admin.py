from django.contrib import admin

from .models import Diocese, Parish, Community


@admin.register(Diocese)
class DioceseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code", 
        "bishop",
        "parish_count",
        "student_count",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["name", "code", "bishop", "email"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        ("Thông tin cơ bản", {"fields": ["name", "code", "bishop"]}),
        ("Liên hệ", {"fields": ["address", "phone", "email", "website"]}),
        ("Thông tin bổ sung", {"fields": ["patron_saint"]}),
        ("Metadata", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]


@admin.register(Parish)
class ParishAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
        "diocese", 
        "pastor",
        "community_count",
        "student_count",
        "established_date",
    ]
    list_filter = ["diocese", "established_date", "created_at"]
    search_fields = ["name", "code", "pastor", "diocese__name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        ("Thông tin cơ bản", {"fields": ["name", "code", "diocese", "pastor"]}),
        ("Liên hệ", {"fields": ["address", "phone", "email"]}),
        ("Thông tin tâm linh", {"fields": ["patron_saint", "established_date"]}),
        ("Metadata", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "parish",
        "leader", 
        "student_count",
        "created_at",
    ]
    list_filter = ["parish__diocese", "parish", "created_at"]
    search_fields = ["name", "leader", "parish__name"]
    readonly_fields = ["created_at", "updated_at"]
    
    fieldsets = [
        ("Thông tin cơ bản", {"fields": ["name", "parish", "leader"]}),
        ("Liên hệ", {"fields": ["address", "phone"]}),
        ("Metadata", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]
