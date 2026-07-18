import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """
    Centralized service to dispatch emails synchronously.
    Using simple HTML layouts inside the functions for portability.
    """
    
    @staticmethod
    def _send(subject, html_content, recipients):
        email_user = getattr(settings, 'EMAIL_HOST_USER', None)
        if not email_user:
            print(f"EMAIL_HOST_USER not set! Mocking email to {recipients}: {subject}")
            logger.warning(f"EMAIL_HOST_USER not set! Mocking email to {recipients}: {subject}")
            return
            
        if isinstance(recipients, str):
            recipients = [recipients]
            
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients
        )
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            print(f"Successfully sent email to {recipients}")
            logger.info(f"Successfully sent email to {recipients}")
        except Exception as e:
            print(f"Error sending email to {recipients}: {str(e)}")
            logger.error(f"Error sending email to {recipients}: {str(e)}")

    @staticmethod
    def _base_html(title, body):
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <div style="background-color: #1E293B; padding: 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0;">Revotic AI LMS</h1>
            </div>
            <div style="padding: 30px; background-color: #ffffff; color: #334155;">
                <h2 style="color: #0f172a; margin-top: 0;">{title}</h2>
                <div style="line-height: 1.6; font-size: 16px;">
                    {body}
                </div>
            </div>
            <div style="background-color: #f8fafc; padding: 15px; text-align: center; color: #64748b; font-size: 14px;">
                &copy; Revotic AI Pvt Ltd. All rights reserved.
            </div>
        </div>
        """

    @staticmethod
    def send_welcome_email(user, password=None):
        title = "Welcome to Revotic AI LMS!"
        body = f"<p>Hello {user.username},</p><p>Your account has been successfully created.</p>"
        if password:
            body += f"""
            <div style="background-color: #f1f5f9; padding: 15px; border-radius: 4px; margin: 20px 0;">
                <strong>Your Temporary Password:</strong> <code style="font-size: 18px; color: #e2e8f0; background: #0f172a; padding: 5px 10px; border-radius: 4px;">{password}</code>
            </div>
            <p>Please log in and change your password immediately.</p>
            """
        html = EmailService._base_html(title, body)
        EmailService._send(title, html, user.email)

    @staticmethod
    def send_password_reset(user, reset_link):
        title = "Password Reset Request"
        body = f"""
        <p>Hello {user.username},</p>
        <p>You have requested to reset your password. Click the button below to proceed:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_link}" style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Reset Password</a>
        </div>
        <p>If you did not request this, please ignore this email.</p>
        """
        html = EmailService._base_html(title, body)
        EmailService._send(title, html, user.email)

    @staticmethod
    def send_enrollment_notification(student, course, status):
        title = f"Enrollment {status}"
        body = f"""
        <p>Hello {student.username},</p>
        <p>Your enrollment request for the course <strong>{course.title} ({course.code})</strong> has been <strong>{status}</strong>.</p>
        """
        if status.upper() == 'APPROVED':
            body += "<p>You can now access the course materials from your student dashboard.</p>"
        html = EmailService._base_html(title, body)
        EmailService._send(title, html, student.email)

    @staticmethod
    def send_assignment_notification(course, assignment):
        title = "New Assignment Published"
        body = f"""
        <p>A new assignment has been published in <strong>{course.title}</strong>.</p>
        <p><strong>Assignment:</strong> {assignment.title}</p>
        <p><strong>Due Date:</strong> {assignment.due_date.strftime('%Y-%m-%d %H:%M') if assignment.due_date else 'No due date'}</p>
        <p>Please check your dashboard for more details and submission instructions.</p>
        """
        html = EmailService._base_html(title, body)
        # Assuming course has a students field (M2M)
        recipients = [student.user.email for student in course.students.all() if student.user.email]
        if recipients:
            EmailService._send(f"[{course.code}] New Assignment: {assignment.title}", html, recipients)

    @staticmethod
    def send_grade_notification(submission):
        title = "Assignment Graded"
        body = f"""
        <p>Hello {submission.student.username},</p>
        <p>Your submission for <strong>{submission.assignment.title}</strong> has been graded.</p>
        <div style="background-color: #f1f5f9; padding: 15px; border-radius: 4px; margin: 20px 0;">
            <strong>Score:</strong> {submission.grade.score if hasattr(submission, 'grade') else 'N/A'} / {submission.assignment.max_score}
        </div>
        <p>Login to your dashboard to view detailed feedback.</p>
        """
        html = EmailService._base_html(title, body)
        EmailService._send(title, html, submission.student.email)

    @staticmethod
    def send_instructor_invitation(email, link):
        title = "Invitation to Teach"
        body = f"""
        <p>Hello,</p>
        <p>You have been invited to join the Revotic AI LMS as an Instructor.</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{link}" style="background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Accept Invitation & Register</a>
        </div>
        """
        html = EmailService._base_html(title, body)
        EmailService._send(title, html, email)

    @staticmethod
    def send_announcement(course, message):
        title = f"Announcement: {course.title}"
        body = f"""
        <p>Your instructor has posted a new announcement for <strong>{course.title}</strong>:</p>
        <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #3b82f6; margin: 20px 0;">
            {message}
        </div>
        """
        html = EmailService._base_html(title, body)
        recipients = [student.user.email for student in course.students.all() if student.user.email]
        if recipients:
            EmailService._send(title, html, recipients)

    @staticmethod
    def send_fee_alert(student, amount, due_date):
        title = "Fee Payment Reminder"
        body = f"""
        <p>Hello {student.user.username},</p>
        <p>This is a reminder that you have an outstanding fee payment.</p>
        <ul>
            <li><strong>Amount:</strong> Rs. {amount}</li>
            <li><strong>Due Date:</strong> {due_date}</li>
        </ul>
        <p>Please upload your payment proof in the finance section of your dashboard.</p>
        """
        html = EmailService._base_html(title, body)
        EmailService._send(title, html, student.user.email)

    @staticmethod
    def send_admin_alert(subject, message):
        title = "System Alert"
        body = f"""
        <p><strong>Admin Alert</strong></p>
        <p>{message}</p>
        """
        html = EmailService._base_html(title, body)
        # Notify superusers
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)
        recipients = [email for email in admins if email]
        if recipients:
            EmailService._send(subject, html, recipients)
