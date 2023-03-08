from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'Register__div__input',
                   'placeholder': ' ',
                   'type': 'login'}),
        label=_("Login*"),
        min_length=5,
        max_length=150
    )

    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'Register__div__input',
                   'placeholder': ' ',
                   'type': 'password'}),
        label=_("Password*")
    )

    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'Register__div__input',
                   'placeholder': ' ',
                   'type': 'password'}),
        label=_("Repeat password*")
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'Register__div__input',
                   'placeholder': ' '}),
        label=_("Email*")
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'Register__div__input',
                   'placeholder': ' '}),
        required=False,
        label=_("Name")
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'Register__div__input',
                   'placeholder': ' '}),
        required=False,
        label=_("Last name")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("User is already exists."))
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError(
                _("Password is too short. Must have 8 characters"))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(_("Passwords isn't this same"))
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email is already exists"))
        return email

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'email', 'first_name', 'last_name']
