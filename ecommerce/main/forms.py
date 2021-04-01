from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# inlineformset_factory(User, Profile, fields=('birthday',))