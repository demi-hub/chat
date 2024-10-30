
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User
from django.contrib.auth import get_user_model, authenticate


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'city', 'dob']
        widgets = {
            'password': forms.PasswordInput(),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #
    #     if not password:
    #         raise forms.ValidationError("Password error")
    #     return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)

