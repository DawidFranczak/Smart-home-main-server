from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django import forms

from .models import HomeNavImage
# from django.utils.translation import gettext as _


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "Register__div__input"}),
        label="Podaj aktualne hasło")

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "Register__div__input"}),
        label="Podaj nowe hasło")

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "Register__div__input"}),
        label="Powtórz nowe hasło")

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Podane hsało jest nieprawidłowe.")
        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        if len(new_password1) < 8:
            raise forms.ValidationError("Hasło jest za krótkie.")
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("Hasła nie są takie same.")
        return new_password2

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]


class ChangeEmailForm(forms.Form):

    new_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "Email__div__input"}),
        label="Podaj nowego emaila",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        new_email = self.cleaned_data.get("new_email")
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("Adres email jest już zajęty")
        return new_email

    def save(self, commit=True):
        new_email = self.cleaned_data.get("new_email")
        user = User.objects.get(email=self.user.email)
        user.email = new_email
        if commit:
            user.save(update_fields=["email"])
        return self.user

    class Meta:
        model = User
        fields = ["email"]


class ChangeImageForm(forms.Form):
    home = forms.ImageField(
        label="Zdjęcie domku",
        required=False)
    rpl = forms.ImageField(
        label="Zdjęcie grupowania urządzeń",
        required=False)
    aquarium = forms.ImageField(
        label="Zdjęcie akwarium",
        required=False)
    sunblind = forms.ImageField(
        label="Zdjęcie rolet",
        required=False)
    temperature = forms.ImageField(
        label="Zdjęcie temperatury",
        required=False)
    profile = forms.ImageField(
        label="Zdjęcie ustawień",
        required=False)
    light = forms.ImageField(
        label="Zdjęcie światła",
        required=False)
    stairs = forms.ImageField(
        label="Zdjęcie schodów",
        required=False)
    sensor = forms.ImageField(
        label="Zdjęcie dodawania urządzeń",
        required=False)
    logout = forms.ImageField(
        label="Zdjęcie wylogowywania",
        required=False)

    IMAGES = ["home", "rpl", "aquarium", "sunblind", "temperature",
              "profile", "light", "stairs", "sensor", "logout"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def reset(self, user):

        user_image = user.homenavimage
        user_image.home = "images/home.png"
        user_image.rpl = "images/rfid.png"
        user_image.aquarium = "images/aqua.png"
        user_image.sunblind = "images/sunblind.png"
        user_image.temperature = "images/temp.png"
        user_image.profile = "images/user.png"
        user_image.light = "images/lamp.png"
        user_image.stairs = "images/stairs.png"
        user_image.sensor = "images/sensor.png"
        user_image.logout = "images/logout.png"
        user_image.save()

        return self.user

    def clean(self):
        IMAGES = ["home", "rpl", "aquarium", "sunblind", "temperature",
                  "profile", "light", "stairs", "sensor", "logout"]

        cleaned_data = super().clean()
        for name in IMAGES:
            if cleaned_data[name] is not None:
                image = cleaned_data.get(name)
                w, h = get_image_dimensions(image)

                w_max = 600 if name == "home" else 400
                h_max = 600 if name == "home" else 400

                if w > w_max or h > h_max:
                    self.add_error(
                        name, f"Zdjęcie za duże, powinno mieć {w_max}px na {h_max}px")

        if self.errors:
            raise forms.ValidationError("Proszę przesłać zdjęcia jeszcze raz")

    def save(self, user):

        user_image = user.homenavimage

        if self.cleaned_data.get("home") is not None:
            user_image.home = self.cleaned_data.get("home")
        if self.cleaned_data.get("rpl") is not None:
            user_image.rpl = self.cleaned_data.get("rpl")
        if self.cleaned_data.get("aquarium") is not None:
            user_image.aquarium = self.cleaned_data.get("aquarium")
        if self.cleaned_data.get("sunblind") is not None:
            user_image.sunblind = self.cleaned_data.get("sunblind")
        if self.cleaned_data.get("temperature") is not None:
            user_image.temperature = self.cleaned_data.get("temperature")
        if self.cleaned_data.get("profile") is not None:
            user_image.profile = self.cleaned_data.get("profile")
        if self.cleaned_data.get("light") is not None:
            user_image.light = self.cleaned_data.get("light")
        if self.cleaned_data.get("stairs") is not None:
            user_image.stairs = self.cleaned_data.get("stairs")
        if self.cleaned_data.get("sensor") is not None:
            user_image.sensor = self.cleaned_data.get("sensor")
        if self.cleaned_data.get("logout") is not None:
            user_image.logout = self.cleaned_data.get("logout")

        user_image.save()
        return self.user

    class Meta:
        model = HomeNavImage
        fields = "__all__"


class ChangeNgrokForm(forms.Form):

    new_link = forms.URLField(
        widget=forms.URLInput(
            attrs={"class": "URL__div__input"}
        ),
        label="Podaj nowy adres URL",
        validators=[
            URLValidator(
                schemes=["https", "http"], message='Adres powienien zaczynać się od "https"'),
        ]
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["new_link"].error_messages = {"validators": {
            "URLValidator": "Czemu to musi być 2 razy napisane ? "
        }}

    def save(self):
        new_link = self.cleaned_data.get("new_link")
        self.user.ngrok.ngrok = new_link
        self.user.ngrok.save(update_fields=["ngrok"])
        return self.user
