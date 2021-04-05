from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError


class CustomerAdapter(DefaultAccountAdapter):

    # def clean_username(self, username):
    #     if len(username) > 30:
    #         raise ValidationError('Please enter a username value less than the current one')
    #     return DefaultAccountAdapter.clean_username(self, username)  # For other default validations.

    def clean_email(self, email):
        RestrictedList = ['test@test.com']
        if email in RestrictedList:
            raise ValidationError('You are restricted from registering. Please contact admin.')
        return email

    def clean_password(self, password):
        if len(password) > 20:
            raise ValidationError('Please Enter a password greater that you can remember.')
        return DefaultAccountAdapter.clean_password(self, password)

    def get_logout_redirect_url(self, request):
        return '/login/'

    def save_user(self, request, user, form, commit=False):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        user = super(CustomerAdapter, self).save_user(request, user, form, commit=commit)
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        # user.save() This would be called later in your custom SignupForm
