import logging
from .models import CustomUser, VerifyEmailToken
from core.email import send_verification_email

logger = logging.getLogger(__name__)


def register(email, password, first_name, last_name, phone=''):
    """Create new user account"""
    if CustomUser.objects.filter(email=email).exists():
        raise Exception("Email already exists")

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        is_active=True,
        is_email_verified=False
    )

    token = VerifyEmailToken.generate_token(user, 'verify_email')
    send_verification_email(user, token)

    logger.info(f"Registration successful: {email}")
    return user