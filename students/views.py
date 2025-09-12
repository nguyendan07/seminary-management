from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentProfileForm


@login_required
def student_profile_view(request):
    """
    Display the student's profile information.
    """
    try:
        student_profile = request.user.student_profile
    except Student.DoesNotExist:
        # Handle cases where a user might not have a student profile
        # This could be an admin or other user type.
        messages.error(request, "You do not have a student profile.")
        return redirect("home")  # Redirect to a safe page, like a dashboard or home

    return render(
        request, "students/student_profile.html", {"student": student_profile}
    )


@login_required
def student_profile_update_view(request):
    """
    Allow a student to update their own profile information.
    """
    try:
        student_profile = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect("home")  # Or some other appropriate URL

    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("student_profile")  # Redirect to the profile view page
    else:
        form = StudentProfileForm(instance=student_profile)

    return render(request, "students/student_profile_form.html", {"form": form})
