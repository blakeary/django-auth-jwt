def email_verification_template(user, verification_url):
    """HTML template for email verification"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #3498db;">Verify Your Email Address</h2>
        <p>Hi {user.first_name or 'there'},</p>
        <p>Please verify your email address by clicking the button below:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_url}" style="background-color: #27ae60; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">Verify Email</a>
        </div>
        <p style="font-size: 14px; color: #666;">
            Or copy and paste this link: {verification_url}
        </p>
        <p style="font-size: 14px; color: #666;">
            This link expires in 24 hours. If you didn't create an account, please ignore this email.
        </p>
    </div>
    """


def password_reset_template(user, reset_url):
    """HTML template for password reset"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #e74c3c;">Reset Your Password</h2>
        <p>Hi {user.first_name or 'there'},</p>
        <p>You requested to reset your password. Click the button below to set a new password:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_url}" style="background-color: #e74c3c; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">Reset Password</a>
        </div>
        <p style="font-size: 14px; color: #666;">
            Or copy and paste this link: {reset_url}
        </p>
        <p style="font-size: 14px; color: #666;">
            This link expires in 24 hours. If you didn't request a password reset, please ignore this email.
        </p>
    </div>
    """


def email_change_verification_template(user, new_email, verification_url):
    """HTML template for email change verification (sent to NEW email)"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #f39c12;">Verify Your New Email Address</h2>
        <p>Hi {user.first_name or 'there'},</p>
        <p>You requested to change your email address to <strong>{new_email}</strong>.</p>
        <p>Click the button below to confirm this change:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_url}" style="background-color: #f39c12; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">Confirm Email Change</a>
        </div>
        <p style="font-size: 14px; color: #666;">
            Or copy and paste this link: {verification_url}
        </p>
        <p style="font-size: 14px; color: #666;">
            This link expires in 24 hours. If you didn't request this change, please ignore this email.
        </p>
    </div>
    """


def email_change_notification_template(user, new_email, cancel_url):
    """HTML template for email change notification (sent to OLD email)"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #e67e22;">Email Change Request</h2>
        <p>Hi {user.first_name or 'there'},</p>
        <p>A request was made to change your email address to <strong>{new_email}</strong>.</p>
        <p style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #f39c12; margin: 20px 0;">
            <strong>⚠️ Security Notice:</strong> If you did not request this change, click the button below immediately to cancel it.
        </p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{cancel_url}" style="background-color: #e74c3c; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">Cancel Email Change</a>
        </div>
        <p style="font-size: 14px; color: #666;">
            Or copy and paste this link: {cancel_url}
        </p>
        <p style="font-size: 14px; color: #666;">
            If you did request this change, no action is needed. The change will be complete once the new email address is verified.
        </p>
    </div>
    """