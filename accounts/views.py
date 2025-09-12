from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AvatarUpdateForm


@login_required
def update_avatar_view(request):
    """
    Allow a logged-in user to update their avatar.
    """
    if request.method == 'POST':
        # Important: pass request.FILES to the form
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your avatar has been updated successfully!')
            
            # Redirect to the appropriate profile page based on user type
            if request.user.user_type == 'student':
                return redirect('student_profile')
            elif request.user.user_type == 'teacher':
                return redirect('teacher_profile')
            else:
                return redirect('home') # Fallback redirect
    else:
        form = AvatarUpdateForm(instance=request.user)

    return render(request, 'accounts/update_avatar.html', {'form': form})
