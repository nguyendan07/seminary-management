from django import forms

from .models import User


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]
