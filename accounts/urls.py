from django.urls import path
from . import views

urlpatterns = [
    # Registration and verification
    path('register/', views.register_view, name='register'),
    path('verify-email/', views.verify_email_view, name='verify_email'),

    # Password management
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('reset-password-confirm/', views.reset_password_confirm_view, name='reset_password_confirm'),

    # Profile management (authenticated)
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('change-email/', views.change_email_view, name='change_email'),
    path('change-email-confirm/', views.change_email_confirm_view, name='change_email_confirm'),
    path('change-email-cancel/', views.change_email_cancel_view, name='change_email_cancel'),
    path('logout/', views.logout_view, name='logout'),
]