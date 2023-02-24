from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import UserPage, UserChangePassword, UserChangeEmail, UserChangeImage, UserDelete, UserChangeNgrok

urlpatterns = [
    path('', login_required(UserPage.as_view(),
         login_url='login'), name="user_page"),
    path('zmiana-hasla/', login_required(UserChangePassword.as_view(),
         login_url='login'), name="user_change_password"),
    path('zmiana-emaila/', login_required(UserChangeEmail.as_view(),
         login_url='login'), name="user_change_email"),
    path('zmiana-zdjec/', login_required(UserChangeImage.as_view(),
         login_url='login'), name="user_change_image"),
    path('usun-konto/', login_required(UserDelete.as_view(),
         login_url='login'), name="user_delete"),
    path('zmiana-linku/', login_required(UserChangeNgrok.as_view(),
         login_url='login'), name="user_change_url"),



    path('reset-hasło/', auth_views.PasswordResetView.as_view(
        template_name='base/password_reset_view.html'),
        name='password_reset'),
    path('reset-hasło/koniec/', auth_views.PasswordResetDoneView.as_view(
        template_name='base/password_reset_done.html'),
        name='password_reset_done'),
    path('reset-hasło/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='base/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset-hasło-ukończone/', auth_views.PasswordResetCompleteView.as_view(
        template_name='base/password_reset_complete.html'),
        name='password_reset_complete'),
]
