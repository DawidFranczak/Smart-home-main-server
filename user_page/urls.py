from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    UserChangeEmail,
    UserChangeImage,
    UserChangeImageReset,
    UserChangeNgrok,
    UserChangePassword,
    UserDelete,
    UserPage,
)

urlpatterns = [
    path("", UserPage.as_view(), name="user_page"),
    path(
        "zmiana-hasla/",
        UserChangePassword.as_view(),
        name="user_change_password",
    ),
    path(
        "zmiana-emaila/<int:pk>",
        UserChangeEmail.as_view(),
        name="user_change_email",
    ),
    path(
        "zmiana-zdjec/<int:pk>",
        UserChangeImage.as_view(),
        name="user_change_image",
    ),
    path(
        "zmiana-zdjec/reset/",
        UserChangeImageReset.as_view(),
        name="user_change_image_reset",
    ),
    path(
        "usun-konto/<int:pk>",
        UserDelete.as_view(),
        name="user_delete",
    ),
    path(
        "zmiana-linku/<int:pk>",
        UserChangeNgrok.as_view(),
        name="user_change_url",
    ),
    path(
        "reset-hasło/",
        auth_views.PasswordResetView.as_view(template_name="password_reset_view.html"),
        name="password_reset",
    ),
    path(
        "reset-hasło/koniec/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-hasło/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-hasło-ukończone/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
