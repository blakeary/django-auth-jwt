from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, VerifyEmailToken
from .utils import register
from .serializers import RegisterUserSerializer, UserProfileSerializer
from core.email import send_verification_email, send_password_reset_email, send_email_change_verification, \
    send_email_change_notification
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new user or resend verification if email exists and unverified"""
    serializer = RegisterUserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'detail': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    email = serializer.validated_data['email']

    try:
        # Check if user already exists
        existing_user = CustomUser.objects.filter(email=email).first()

        if existing_user:
            # If email already verified, return error
            if existing_user.is_email_verified:
                return Response(
                    {'detail': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # If email not verified, resend verification email
            token = VerifyEmailToken.generate_token(existing_user, 'verify_email')
            send_verification_email(existing_user, token)

            logger.info(f"Verification email resent: {email}")

            return Response(
                {'detail': 'Verification email sent'},
                status=status.HTTP_200_OK
            )

        # Create new user
        user = register(
            email=email,
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            phone=serializer.validated_data.get('phone', '')
        )

        return Response(
            {'detail': 'Registration successful'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return Response(
            {'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_view(request):
    """Verify user email with token"""
    token_string = request.data.get('token')

    if not token_string:
        return Response(
            {'detail': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = VerifyEmailToken.objects.get(token=token_string, token_type='verify_email')

        if not token.is_valid():
            return Response(
                {'detail': 'Token expired or used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token.user
        user.is_email_verified = True
        user.save()

        token.is_used = True
        token.save()

        logger.info(f"Email verification successful: {user.email}")

        return Response(
            {'detail': 'Email verification successful'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Email verification failed: {str(e)}")
        return Response(
            {'detail': 'Email verification failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    """Request password reset"""
    email = request.data.get('email')

    if not email:
        return Response(
            {'detail': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(email=email)

        # Generate reset token
        token = VerifyEmailToken.generate_token(user, 'reset_password')
        send_password_reset_email(user, token)

        logger.info(f"Password reset email sent: {email}")

        return Response(
            {'detail': 'Password reset email sent'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Password reset request failed: {str(e)}")
        # Don't reveal if email exists or not
        return Response(
            {'detail': 'Password reset email sent'},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm_view(request):
    """Confirm password reset with token"""
    token_string = request.data.get('token')
    password = request.data.get('password')

    if not token_string or not password:
        return Response(
            {'detail': 'Token and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Validate password strength
        validate_password(password)

        token = VerifyEmailToken.objects.get(token=token_string, token_type='reset_password')

        if not token.is_valid():
            return Response(
                {'detail': 'Token expired or used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token.user
        user.set_password(password)
        user.save()

        token.is_used = True
        token.save()

        logger.info(f"Password reset successful: {user.email}")

        return Response(
            {'detail': 'Password reset successful'},
            status=status.HTTP_200_OK
        )

    except ValidationError as e:
        return Response(
            {'detail': e.messages},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Password reset confirmation failed: {str(e)}")
        return Response(
            {'detail': 'Password reset failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Get, update, or delete user profile"""
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        logger.info(f"Profile updated: {user.email}")

        return Response(
            {'detail': 'Profile updated successfully'},
            status=status.HTTP_200_OK
        )

    elif request.method == 'DELETE':
        password = request.data.get('password')

        if not password:
            return Response(
                {'detail': 'Password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify password
        if not user.check_password(password):
            return Response(
                {'detail': 'Password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = user.email
        user.delete()

        logger.info(f"Profile deleted: {email}")

        return Response(
            {'detail': 'Profile deleted successfully'},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Change password while authenticated"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response(
            {'detail': 'Old password and new password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = request.user

        # Verify old password
        if not user.check_password(old_password):
            return Response(
                {'detail': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate new password strength
        validate_password(new_password, user)

        user.set_password(new_password)
        user.save()

        logger.info(f"Password change successful: {user.email}")

        return Response(
            {'detail': 'Password change successful'},
            status=status.HTTP_200_OK
        )

    except ValidationError as e:
        return Response(
            {'detail': e.messages},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Password change failed: {str(e)}")
        return Response(
            {'detail': 'Password change failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email_view(request):
    """Request email change"""
    new_email = request.data.get('new_email')
    password = request.data.get('password')

    if not new_email or not password:
        return Response(
            {'detail': 'New email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = request.user

        # Verify password
        if not user.check_password(password):
            return Response(
                {'detail': 'Password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if new email already exists
        if CustomUser.objects.filter(email=new_email).exists():
            return Response(
                {'detail': 'Email already in use'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if trying to change to same email
        if user.email == new_email:
            return Response(
                {'detail': 'New email is the same as current email'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Invalidate all existing change_email tokens for this user
        VerifyEmailToken.objects.filter(
            user=user,
            token_type='change_email'
        ).update(is_used=True)

        # Update pending email
        user.pending_email = new_email
        user.save()

        # Generate new token
        token = VerifyEmailToken.generate_token(user, 'change_email', new_email=new_email)

        # Send verification email to NEW address
        send_email_change_verification(user, token, new_email)

        # Send notification to OLD address
        send_email_change_notification(user, new_email, token)

        logger.info(f"Email change requested: {user.email} -> {new_email}")

        return Response(
            {'detail': 'Verification email sent to new address'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Email change request failed: {str(e)}")
        return Response(
            {'detail': 'Email change request failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def change_email_confirm_view(request):
    """Confirm email change with token"""
    token_string = request.data.get('token')

    if not token_string:
        return Response(
            {'detail': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = VerifyEmailToken.objects.get(token=token_string, token_type='change_email')

        if not token.is_valid():
            return Response(
                {'detail': 'Token expired or used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token.user
        new_email = token.new_email

        # Update email
        user.email = new_email
        user.pending_email = None
        user.save()

        # Mark token as used
        token.is_used = True
        token.save()

        logger.info(f"Email change successful: {new_email}")

        return Response(
            {'detail': 'Email change successful'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Email change confirmation failed: {str(e)}")
        return Response(
            {'detail': 'Email change confirmation failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def change_email_cancel_view(request):
    """Cancel email change request"""
    token_string = request.data.get('token')

    if not token_string:
        return Response(
            {'detail': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = VerifyEmailToken.objects.get(token=token_string, token_type='change_email')

        user = token.user

        # Invalidate all change_email tokens for this user
        VerifyEmailToken.objects.filter(
            user=user,
            token_type='change_email'
        ).update(is_used=True)

        # Clear pending email
        user.pending_email = None
        user.save()

        logger.info(f"Email change cancelled: {user.email}")

        return Response(
            {'detail': 'Email change cancelled'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Email change cancellation failed: {str(e)}")
        return Response(
            {'detail': 'Email change cancellation failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user by blacklisting refresh token"""
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response(
            {'detail': 'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        logger.info(f"Logout successful: {request.user.email}")

        return Response(
            {'detail': 'Logout successful'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        return Response(
            {'detail': 'Logout failed'},
            status=status.HTTP_400_BAD_REQUEST
        )