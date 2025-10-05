from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm

from apps.accounts.models.accounts import CustomUser

class AdminUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={"class": "form-control"}),
        }

class AdminUserChangeForm(UserChangeForm):
    password = None  # no queremos que aparezca el campo de password aquí

    class Meta:
        model = CustomUser
        fields = ("username", "email", "role", "is_active")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={"class": "form-control"}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }