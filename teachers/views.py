from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Teacher
from .forms import TeacherProfileForm


@login_required
def teacher_profile_view(request):
    """
    Display the teacher's profile information.
    """
    try:
        teacher_profile = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "You do not have a teacher profile.")
        return redirect("home")

    return render(
        request, "teachers/teacher_profile.html", {"teacher": teacher_profile}
    )


@login_required
def teacher_profile_update_view(request):
    """
    Allow a teacher to update their own profile information.
    """
    try:
        teacher_profile = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect("home")

    if request.method == "POST":
        form = TeacherProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("teacher_profile")
    else:
        form = TeacherProfileForm(instance=teacher_profile)

    return render(request, "teachers/teacher_profile_form.html", {"form": form})
