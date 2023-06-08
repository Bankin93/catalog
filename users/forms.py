from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, AuthenticationForm, \
    PasswordResetForm, SetPasswordForm
from transliterate.utils import _

from catalog_app.forms import FormStyleMixin
from users.models import User


class CustomUserChangeForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class CustomUserRegisterForm(FormStyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class CustomAuthenticationForm(FormStyleMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomPasswordResetForm(FormStyleMixin, PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User


class CustomResetConfirmForm(SetPasswordForm):
    class Meta:
        model = User
