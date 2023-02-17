from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.user_page, name="user_page"),
    path('zmiana-hasla', views.user_change_password, name="user_change_password"),
    path('zmiana-emaila', views.user_change_email, name="user_change_email"),
    path('zmiana-zdjec', views.user_change_image, name="user_change_image"),
    path('usun-konto', views.user_delete, name="user_delete"),
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
