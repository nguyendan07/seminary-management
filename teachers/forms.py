from django import forms

from .models import Teacher


class TeacherProfileForm(forms.ModelForm):
    """
    Form for teachers to update their own profile information.
    """

    class Meta:
        model = Teacher
        fields = [
            "position",
            "education_background",
            "specialization",
            "experience",
            "office_room",
            "consultation_hours",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
