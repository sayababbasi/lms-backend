import secrets
import string
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .models import PasswordHistory, AuditLog, OrganizationSettings

class PasswordService:
    @staticmethod
    def generate_secure_password(length=8):
        """Generates a cryptographically secure random password."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)):
                return password

    @staticmethod
    def validate_password_strength(password, user=None):
        """Validates password against organization settings and history."""
        settings = OrganizationSettings.objects.first()
        if not settings:
            settings = OrganizationSettings.objects.create()

        if len(password) < settings.min_password_length:
            return False, f"Password must be at least {settings.min_password_length} characters long."
        if settings.require_uppercase and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter."
        # Assuming lower is always required implicitly in modern systems
        if not any(c.islower() for c in password): 
            return False, "Password must contain at least one lowercase letter."
        if settings.require_numbers and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number."
        if settings.require_special_chars and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character."
        
        if user:
            # Check history
            history = PasswordHistory.objects.filter(user=user).order_by('-created_at')[:5]
            for record in history:
                if check_password(password, record.hashed_password):
                    return False, "Cannot reuse any of the last 5 passwords."
            
            # Check username/email match
            if password.lower() in [user.username.lower(), user.email.lower()]:
                return False, "Password cannot match or contain username or email."
            if user.first_name and user.first_name.lower() in password.lower():
                return False, "Password cannot contain first name."
            if user.last_name and user.last_name.lower() in password.lower():
                return False, "Password cannot contain last name."

        return True, "Valid"

    @staticmethod
    def hash_password(password):
        """Hashes the password using Django's default hasher (Argon2id or PBKDF2 depending on settings)."""
        return make_password(password)

    @staticmethod
    def record_password_history(user, raw_password):
        """Records the hashed password in history."""
        hashed = PasswordService.hash_password(raw_password)
        PasswordHistory.objects.create(user=user, hashed_password=hashed)

class AuthenticationService:
    @staticmethod
    def handle_failed_login(user):
        """Increments failed login attempts and locks the account if necessary."""
        settings = OrganizationSettings.objects.first()
        if not settings:
            settings = OrganizationSettings.objects.create()

        user.failed_login_attempts += 1
        if user.failed_login_attempts >= settings.max_failed_attempts:
            user.password_status = 'LOCKED'
            user.locked_until = timezone.now() + timedelta(minutes=30)
            AuditLogService.log_action(user=user, admin=None, action="Account Locked due to max failed attempts")
        user.save()

    @staticmethod
    def handle_successful_login(user):
        """Resets failed login attempts."""
        if user.failed_login_attempts > 0 or user.password_status == 'LOCKED':
            user.failed_login_attempts = 0
            user.locked_until = None
            if user.password_status == 'LOCKED':
                user.password_status = 'ACTIVE'
            user.save()

class AuditLogService:
    @staticmethod
    def log_action(user=None, admin=None, action="", ip_address=None):
        """Safely logs security events."""
        AuditLog.objects.create(
            user=user,
            admin=admin,
            action=action,
            ip_address=ip_address
        )

class NotificationService:
    @staticmethod
    def send_welcome_email(user, temporary_password):
        """Mock: Sends welcome email with temporary credentials."""
        # In a real system, use Django's send_mail or an email service.
        print(f"MOCK EMAIL: Welcome {user.username}. Temp password: {temporary_password}")

    @staticmethod
    def send_password_reset_email(user, reset_link):
        """Mock: Sends password reset email."""
        print(f"MOCK EMAIL: Password reset for {user.username}. Link: {reset_link}")
