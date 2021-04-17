from django import forms
from django.db import transaction

from .models import Customer, Item
from django.contrib.auth import get_user_model
from .tasks import send_feedback_email_task

User = get_user_model()


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'color', 'image', 'description', 'price', 'price_discount', 'tag', 'slug', ]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'input-image-control'}),
            'title': forms.TextInput({'class': 'form-control'}),
            'category': forms.Select({'class': 'form-control'}),
            'color': forms.TextInput({'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 6}),
            'price': forms.TextInput({'class': 'form-control'}),
            'price_discount': forms.TextInput({'class': 'form-control'}),
            'tag': forms.SelectMultiple({'class': 'form-control'}),
            'slug': forms.TextInput({'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User

        fields = ('last_name', 'first_name', 'email', 'username',)
        labels = {
            'email': 'Адрес email',
            'username': 'Никнейм',
        }


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином "{username} не найден в системе')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверные учетные данные")
        return self.cleaned_data


# ACCOUNT_SIGNUP_FORM_CLASS = 'main.forms.CustomSignupForm' ==== не работает
class CustomerSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

    @transaction.atomic
    def save(self, request, user):
        user.save()  # save the user object first so you can use it for relationships


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={'rows': 5}))
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def send_email(self):
        # try to trick spammers by checking whether the honeypot field is
        # filled in; not super complicated/effective but it works
        if self.cleaned_data['honeypot']:
            return False
        send_feedback_email_task.delay(
            self.cleaned_data['email'], self.cleaned_data['message'])
