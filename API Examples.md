**Accounts**

- **Register**
    
    POST - http://localhost:8000/api/auth/register/
    
    Request
    
    ```json
    {
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "1234567890"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Registration successful"
    }
    ```
    
- **Verify Email**
    
    POST - http://localhost:8000/api/auth/verify-email/
    
    Request
    
    ```json
    {
        "token": "7s4LLCsxaujXxqKjmWpisPxIaCGGKF0CkBT6sY_Ygjw"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Email verification successful"
    }
    ```
    
- **Login**
    
    POST - http://localhost:8000/api/auth/login/
    
    Request
    
    ```json
    {
        "email": "test@example.com",
        "password": "testpass123"
    }
    ```
    
    Response
    
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MjEwMjk1NCwiaWF0IjoxNzYxNDk4MTU0LCJqdGkiOiIxNDMyMzVhZWMxNjk0OTFkYmZhZjI5NDMyNTg3YzBkZSIsInVzZXJfaWQiOiIzIn0._sc1K2R3ulZFCEp_Pau95qu-2YbRiTdFb769kWAIMeM",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNDk5MDU0LCJpYXQiOjE3NjE0OTgxNTQsImp0aSI6IjY4NTg0ZjEyNGIzMzRmMDFhYWYxMTNjOWIyYzNiYWQyIiwidXNlcl9pZCI6IjMifQ.y92KAtB6n9Ax10DA_DEucwBlwY3-np8BMM_A7Yx7vy8"
    }
    ```
    
- **Refresh**
    
    POST - http://localhost:8000/api/auth/refresh/
    
    Request
    
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MTk0ODkwMCwiaWF0IjoxNzYxMzQ0MTAwLCJqdGkiOiIwNzBlYTBiMDVlNzA0N2M1YThkOWE1YzJlYjdhZWFmZiIsInVzZXJfaWQiOiIxIn0.497y83u40g0h3mHzGs7vMtgJ-fzDf0hw8bg5e0lPW6I"
    }
    ```
    
    Response
    
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzQ1NzA2LCJpYXQiOjE3NjEzNDQ4MDYsImp0aSI6IjBkYjhiMWI1MTFiODQxMmRhMzY0MzhjNDMwNjdiOGU0IiwidXNlcl9pZCI6IjEifQ.YcliJSenMeQaW-vmn0qTfePnEKsLvcONWeww0BDG_xE",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MTk0OTYwNiwiaWF0IjoxNzYxMzQ0ODA2LCJqdGkiOiI0MzYxNDUzYjQ4ODM0ZmZmOTBkYjRlZTJhMjQ2MzJjMyIsInVzZXJfaWQiOiIxIn0.DdXtGG4sj-kOacu31GEXDkFyGZOWdyRap0AmEI5-gpU"
    }
    ```
    
- **Reset Password**
    
    POST - http://localhost:8000/api/auth/reset-password/
    
    Request
    
    ```json
    {
        "email": "test@example.com"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Password reset email sent"
    }
    ```
    
- **Reset Password Confirm**
    
    POST - http://localhost:8000/api/auth/reset-password-confirm/
    
    Request
    
    ```json
    {
        "token": "LKXnjOT1ZMRswLnve4c1HVupjgRMIlhMmtC-f2biL74",
        "password": "newpassword123"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Password reset successful"
    }
    ```
    
- **Profile**
    
    GET - http://localhost:8000/api/auth/profile/
    
    Authorization Header - Bearer Token
    
    Request
    
    ```json
    {
        "token": "LKXnjOT1ZMRswLnve4c1HVupjgRMIlhMmtC-f2biL74",
        "password": "testpass123"
    }
    ```
    
    Response
    
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
    
- **Update Profile**
    
    PATCH - http://localhost:8000/api/auth/profile/
    
    Authorization Header - Bearer Token
    
    Request
    
    ```json
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "0987654321"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Profile updated successfully"
    }
    ```
    
- **Delete Profile**
    
    DELETE - http://localhost:8000/api/auth/profile/
    
    Authorization Header - Bearer Token
    
    Request
    
    ```json
    {
        "password": "testpass123"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Profile deleted successfully"
    }
    ```
    
- **Change Password**
    
    POST - http://localhost:8000/api/auth/change-password/
    
    Authorization Header - Bearer Token
    
    Request
    
    ```json
    {
        "old_password": "newpassword123",
        "new_password": "newpassword456"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Password change successful"
    }
    ```
    
- **Change Email**
    
    POST - http://localhost:8000/api/auth/change-email/
    
    Authorization Header - Bearer Token
    
    Request
    
    ```json
    {
        "new_email": "test2@example.com",
        "password": "newpassword456"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Verification email sent to new address"
    }
    ```
    
- **Change Email Confirm**
    
    POST - http://localhost:8000/api/auth/change-email-confirm/
    
    Request
    
    ```json
    {
        "token": "v_7_vGFjKF8OOs3El4KAtsBUVjA7l6nUhZtENiySZ9k"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Email change successful"
    }
    ```
    
- **Change Email Cancel**
    
    POST - http://localhost:8000/api/auth/change-email-cancel/
    
    Request
    
    ```json
    {
        "token": "dusMaMolpXiYotjdF6qXRQIuXFcjFa7U5sM2qGFy4CM"
    }
    ```
    
    Response
    
    ```json
    {
        "detail": "Email change cancelled"
    }
    ```