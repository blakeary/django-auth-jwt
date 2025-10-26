import logging
from django.core.mail import send_mail
from django.conf import settings
from .email_templates import (
    email_verification_template,
    password_reset_template,
    email_change_verification_template,
    email_change_notification_template
)

logger = logging.getLogger(__name__)


def send_verification_email(user, token):
    """Send email verification to user"""
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token.token}"

    subject = "Verify Your Email Address"
    text_content = f"Please verify your email: {verification_url}"
    html_content = email_verification_template(user, verification_url)

    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, text_content, from_email, [user.email], html_message=html_content)
    logger.info(f"Verification email sent: {user.email}")


def send_password_reset_email(user, token):
    """Send password reset email to user"""
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token.token}"

    subject = "Reset Your Password"
    text_content = f"Reset your password: {reset_url}"
    html_content = password_reset_template(user, reset_url)

    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, text_content, from_email, [user.email], html_message=html_content)
    logger.info(f"Password reset email sent: {user.email}")


def send_email_change_verification(user, token, new_email):
    """Send email change verification to NEW email address"""
    verification_url = f"{settings.FRONTEND_URL}/change-email-confirm?token={token.token}"

    subject = "Verify Your New Email Address"
    text_content = f"Confirm your email change: {verification_url}"
    html_content = email_change_verification_template(user, new_email, verification_url)

    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, text_content, from_email, [new_email], html_message=html_content)
    logger.info(f"Email change verification sent: {new_email}")


def send_email_change_notification(user, new_email, token):
    """Send email change notification to OLD email address"""
    cancel_url = f"{settings.FRONTEND_URL}/change-email-cancel?token={token.token}"

    subject = "Email Change Request"
    text_content = f"Email change requested to {new_email}. Cancel here: {cancel_url}"
    html_content = email_change_notification_template(user, new_email, cancel_url)

    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, text_content, from_email, [user.email], html_message=html_content)
    logger.info(f"Email change notification sent: {user.email}")