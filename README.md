# Django Auth JWT

A complete, production-ready authentication backend built with Django REST Framework and Simple JWT. Features email verification, password management, profile operations, and AWS SES email integration.

## Features

### Core Authentication
- JWT Authentication - Access and refresh token management with automatic rotation
- Token Blacklist - Secure logout with token invalidation
- Email Verification - Required email verification on registration
- Custom User Model - Email-based authentication (no username required)

### Password Management
- Password Reset - Secure forgot password flow with email tokens
- Password Change - Change password while authenticated
- Password Validation - Django's built-in password strength validation

### Profile Management
- Get Profile - Retrieve user information
- Update Profile - Modify first name, last name, and phone
- Delete Account - Self-service account deletion with password confirmation

### Email Management
- Change Email - Update email with verification
- Email Verification - Verify new email address before change
- Email Notifications - Security notifications sent to old email
- Cancel Email Change - Security feature to cancel unauthorized changes

### Email System
- AWS SES Integration - Production-ready email delivery
- Console Backend - Development mode prints emails to console
- HTML Templates - Professional, responsive email templates
- Token-based Links - Secure 24-hour expiring verification links

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/blakeary/django-auth-jwt.git
cd django-auth-jwt
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Copy .env.example to .env and configure your settings:
```bash
cp .env.example .env
```

Edit .env:
- Set SECRET_KEY (generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
- Set DEFAULT_FROM_EMAIL
- Configure AWS SES credentials (or use console backend for development)
- Set FRONTEND_URL for email links

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at http://localhost:8000

## API Documentation

For detailed API endpoint examples with request/response formats, see [API Examples](https://github.com/blakeary/django-auth-jwt/blob/main/API%20Examples.md).

### Endpoints Summary

**Registration and Verification**
- POST /api/auth/register/
- POST /api/auth/verify-email/

**Authentication**
- POST /api/auth/login/
- POST /api/auth/refresh/
- POST /api/auth/logout/

**Password Management**
- POST /api/auth/reset-password/
- POST /api/auth/reset-password-confirm/
- POST /api/auth/change-password/

**Profile Management**
- GET /api/auth/profile/
- PATCH /api/auth/profile/
- DELETE /api/auth/profile/

**Email Management**
- POST /api/auth/change-email/
- POST /api/auth/change-email-confirm/
- POST /api/auth/change-email-cancel/

## Configuration

### Development Mode

For local development, emails will print to console. Set in .env:
```
DEBUG=True
```

### Production Mode

For production, configure AWS SES:
```
DEBUG=False
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_SES_REGION_NAME=us-east-1
```

See AWS SES documentation for setup instructions.

## Technology Stack

- Django 5.2.7
- Django REST Framework 3.15.2
- Simple JWT 5.3.1
- AWS SES (django-ses 4.2.0)
- Python Dotenv 1.0.0

## Project Structure
```
django-auth-jwt/
├── accounts/              # User authentication app
│   ├── models.py          # CustomUser and VerifyEmailToken models
│   ├── views.py           # All authentication endpoints
│   ├── serializers.py     # User serializers
│   ├── utils.py           # Registration utility
│   └── urls.py            # Auth URL routing
├── core/                  # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Main URL routing
│   ├── email.py           # Email sending functions
│   └── email_templates.py # HTML email templates
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
└── manage.py              # Django management script
```

## Security Features

- JWT token rotation with blacklist
- Password strength validation
- Email verification required
- Token expiration (24 hours)
- Secure password reset flow
- Email change verification with cancellation
- CORS configuration
- Environment-based configuration

## Testing

Use the included API documentation to test endpoints with tools like Postman or curl.

Example register request:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this in your projects.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

Built with Django, Django REST Framework, and Simple JWT.