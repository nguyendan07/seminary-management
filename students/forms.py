from django import forms

from .models import Student


class StudentProfileForm(forms.ModelForm):
    """
    Form for students to update their own profile information.
    """

    class Meta:
        model = Student
        fields = [
            "hometown",
            "baptism_name",
            "baptism_date",
            "confirmation_date",
            "parish",
            "community",
        ]
        widgets = {
            "baptism_date": forms.DateInput(attrs={"type": "date"}),
            "confirmation_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
