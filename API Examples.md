# API Examples

Complete request and response examples for all authentication endpoints.

## Table of Contents
- [Registration & Verification](#registration--verification)
- [Authentication](#authentication)
- [Password Management](#password-management)
- [Profile Management](#profile-management)
- [Email Management](#email-management)

---

## Registration & Verification

### Register

Create a new user account and send verification email.

**Endpoint:** `POST /api/auth/register/`

**Request:**
```json
{
  "email": "test@example.com",
  "password": "testpass123",
  "first_name": "Test",
  "last_name": "User",
  "phone": "1234567890"
}
```

**Response:**
```json
{
  "detail": "Registration successful"
}
```

**Note:** A verification email will be sent to the provided email address.

---

### Verify Email

Verify user email with token from email.

**Endpoint:** `POST /api/auth/verify-email/`

**Request:**
```json
{
  "token": "7s4LLCsxaujXxqKjmWpisPxIaCGGKF0CkBT6sY_Ygjw"
}
```

**Response:**
```json
{
  "detail": "Email verification successful"
}
```

---

## Authentication

### Login

Authenticate user and receive JWT tokens.

**Endpoint:** `POST /api/auth/login/`

**Request:**
```json
{
  "email": "test@example.com",
  "password": "testpass123"
}
```

**Response:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** Use the `access` token in Authorization header for authenticated requests. Use `refresh` token to get a new access token when it expires.

---

### Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /api/auth/refresh/`

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** Both tokens are rotated for security.

---

### Logout

Blacklist refresh token to invalidate session.

**Endpoint:** `POST /api/auth/logout/`

**Authorization:** Bearer Token Required

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "detail": "Logout successful"
}
```

---

## Password Management

### Reset Password

Request password reset email.

**Endpoint:** `POST /api/auth/reset-password/`

**Request:**
```json
{
  "email": "test@example.com"
}
```

**Response:**
```json
{
  "detail": "Password reset email sent"
}
```

**Note:** A password reset email will be sent with a token link.

---

### Reset Password Confirm

Confirm password reset with token and set new password.

**Endpoint:** `POST /api/auth/reset-password-confirm/`

**Request:**
```json
{
  "token": "LKXnjOT1ZMRswLnve4c1HVupjgRMIlhMmtC-f2biL74",
  "password": "newpassword123"
}
```

**Response:**
```json
{
  "detail": "Password reset successful"
}
```

---

### Change Password

Change password while authenticated.

**Endpoint:** `POST /api/auth/change-password/`

**Authorization:** Bearer Token Required

**Request:**
```json
{
  "old_password": "currentpassword",
  "new_password": "newpassword456"
}
```

**Response:**
```json
{
  "detail": "Password change successful"
}
```

---

## Profile Management

### Get Profile

Retrieve current user profile information.

**Endpoint:** `GET /api/auth/profile/`

**Authorization:** Bearer Token Required

**Response:**
```json
{
  "id": 3,
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "phone": "1234567890",
  "is_email_verified": true,
  "date_joined": "2025-10-24T19:12:03.920609-04:00"
}
```

---

### Update Profile

Update user profile information (first name, last name, phone).

**Endpoint:** `PATCH /api/auth/profile/`

**Authorization:** Bearer Token Required

**Request:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "0987654321"
}
```

**Response:**
```json
{
  "detail": "Profile updated successfully"
}
```

**Note:** All fields are optional. Only provide fields you want to update.

---

### Delete Profile

Permanently delete user account.

**Endpoint:** `DELETE /api/auth/profile/`

**Authorization:** Bearer Token Required

**Request:**
```json
{
  "password": "testpass123"
}
```

**Response:**
```json
{
  "detail": "Profile deleted successfully"
}
```

**Warning:** This action is permanent and cannot be undone.

---

## Email Management

### Change Email

Request email change. Sends verification to new email and notification to old email.

**Endpoint:** `POST /api/auth/change-email/`

**Authorization:** Bearer Token Required

**Request:**
```json
{
  "new_email": "newemail@example.com",
  "password": "currentpassword"
}
```

**Response:**
```json
{
  "detail": "Verification email sent to new address"
}
```

**Note:** Two emails are sent:
1. Verification email to new address (to confirm change)
2. Notification email to old address (to cancel if unauthorized)

---

### Change Email Confirm

Confirm email change with token from verification email.

**Endpoint:** `POST /api/auth/change-email-confirm/`

**Request:**
```json
{
  "token": "v_7_vGFjKF8OOs3El4KAtsBUVjA7l6nUhZtENiySZ9k"
}
```

**Response:**
```json
{
  "detail": "Email change successful"
}
```

---

### Change Email Cancel

Cancel email change request (from notification email).

**Endpoint:** `POST /api/auth/change-email-cancel/`

**Request:**
```json
{
  "token": "dusMaMolpXiYotjdF6qXRQIuXFcjFa7U5sM2qGFy4CM"
}
```

**Response:**
```json
{
  "detail": "Email change cancelled"
}
```

**Note:** This invalidates the email change request and clears any pending email changes.

---

## Authentication Header Format

For endpoints requiring authentication, include the access token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Error Responses

All endpoints return error responses in the following format:
```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `404 Not Found` - Resource not found

## Token Expiration

- **Access Token:** 15 minutes
- **Refresh Token:** 7 days
- **Email Verification Token:** 24 hours
- **Password Reset Token:** 24 hours
- **Email Change Token:** 24 hours