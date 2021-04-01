from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User

        fields = ('last_name', 'first_name', 'email', 'username', 'password')
        labels = {
            'email': 'Адрес email',
            'username': 'Ник',
        }
