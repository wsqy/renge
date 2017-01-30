from django import forms
from RGPY.models import Student


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("username", "password", "first_name", "email", "phone", "banji")
