from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.student_profile_view, name="student_profile"),
    path(
        "profile/update/",
        views.student_profile_update_view,
        name="student_profile_update",
    ),
]
