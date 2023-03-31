from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django import forms

from django.utils.translation import gettext_lazy as _

from .models import HomeNavImage
from log.models import Ngrok


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "Register__div__input"}),
        label=_("Current password"),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "Register__div__input"}),
        label=_("New password"),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "Register__div__input"}),
        label=_("Repeat new password"),
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")

        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("New password is incorrect"))
        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        if len(new_password1) < 8:
            raise forms.ValidationError(
                _("Password is too short. Must have 8 characters")
            )
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError(_("Passwords isn't this same"))
        return new_password2

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]


class ChangeEmailForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "Email__div__input"}),
        label=_("New email"),
    )

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email is already exist."))
        return email

    class Meta:
        model = User
        fields = ["email"]


class ChangeImageForm(forms.ModelForm):
    home = forms.ImageField(label=_("Home icon"), required=False)
    rpl = forms.ImageField(label=_("RPL icon"), required=False)
    aquarium = forms.ImageField(label=_("Aquarium icon"), required=False)
    sunblind = forms.ImageField(label=_("Sunblind icon"), required=False)
    temperature = forms.ImageField(label=_("Chart icon"), required=False)
    profile = forms.ImageField(label=_("Settings icon"), required=False)
    light = forms.ImageField(label=_("Light icon"), required=False)
    stairs = forms.ImageField(label=_("Stairs icon"), required=False)
    sensor = forms.ImageField(label=_("Devices icon"), required=False)
    logout = forms.ImageField(label=_("Logout icon"), required=False)

    IMAGES = [
        "home",
        "rpl",
        "aquarium",
        "sunblind",
        "temperature",
        "profile",
        "light",
        "stairs",
        "sensor",
        "logout",
    ]

    def clean(self):
        IMAGES = [
            "home",
            "rpl",
            "aquarium",
            "sunblind",
            "temperature",
            "profile",
            "light",
            "stairs",
            "sensor",
            "logout",
        ]

        cleaned_data = super().clean()
        for name in IMAGES:
            print(cleaned_data[name])
            if cleaned_data[name] is not None:
                image = cleaned_data.get(name)
                w, h = get_image_dimensions(image)

                w_max = 1000
                h_max = 1000
                if w > w_max or h > h_max:
                    self.add_error(
                        name,
                        _(f"Picture is to big, it should has {w_max}px x {h_max}px"),
                    )

        if self.errors:
            raise forms.ValidationError(_("Please send images once again."))

    class Meta:
        model = HomeNavImage
        exclude = ["user"]


class ChangeNgrokForm(forms.ModelForm):
    ngrok = forms.URLField(
        widget=forms.URLInput(attrs={"class": "URL__div__input"}),
        label=_("New URL"),
        validators=[
            URLValidator(
                schemes=["https", "http"],
                message=_('URL should start with "https" or "http"'),
            ),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ngrok"].error_messages = {
            "validators": {"URLValidator": "Czemu to musi być 2 razy napisane ? "}
        }

    class Meta:
        model = Ngrok
        fields = ["ngrok"]
