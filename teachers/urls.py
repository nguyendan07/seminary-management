from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.teacher_profile_view, name="teacher_profile"),
    path(
        "profile/update/",
        views.teacher_profile_update_view,
        name="teacher_profile_update",
    ),
]
