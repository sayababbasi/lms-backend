import logging
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import traceback

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_template_email(subject, recipient_list, template_name, context, log_email=True):
        """
        Sends an HTML email using a Django template with a plain-text fallback.
        In production, this should be called asynchronously via a Celery task.
        """
        from apps.notifications.models import EmailLog
        
        email_log = None
        if log_email:
            email_log = EmailLog.objects.create(
                recipient=recipient_list[0] if recipient_list else 'unknown',
                subject=subject,
                template_name=template_name,
                status='PENDING',
                context_data=context
            )
            
        try:
            # 1. Render HTML content
            html_content = render_to_string(template_name, context)
            
            # 2. Use Brevo HTTP API to bypass Render SMTP port blocking
            brevo_api_key = os.getenv("BREVO_API_KEY")
            if brevo_api_key:
                import requests
                headers = {
                    "accept": "application/json",
                    "api-key": brevo_api_key,
                    "content-type": "application/json"
                }
                payload = {
                    "sender": {
                        "name": "Revotic AI Pvt. Ltd.",
                        "email": "contact@revoticai.com"
                    },
                    "to": [
                        {"email": recipient} for recipient in recipient_list
                    ],
                    "subject": subject,
                    "htmlContent": html_content
                }
                response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
                if response.status_code in [200, 201, 202]:
                    logger.info(f"Brevo HTTP API sent email successfully to {recipient_list}")
                else:
                    raise Exception(f"Brevo HTTP API error {response.status_code}: {response.text}")
            else:
                # Fallback to standard SMTP
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=recipient_list
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
            
            if email_log:
                from django.utils import timezone
                email_log.status = 'SENT'
                email_log.sent_at = timezone.now()
                email_log.save()
                
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_list}: {str(e)}\n{traceback.format_exc()}")
            if email_log:
                email_log.status = 'FAILED'
                email_log.error_message = str(e)
                email_log.save()
            return False

    @staticmethod
    def send_async_email(subject, recipient_list, template_name, context):
        """
        Pushes the email sending to a Celery background task.
        """
        from apps.notifications.tasks import send_email_task
        send_email_task.delay(subject, recipient_list, template_name, context)

    # --- Upgraded Specific Email Helpers ---

    @staticmethod
    def send_welcome_email(user, password=None):
        subject = "Welcome to Revotic AI LMS!"
        context = {
            'heading': 'Welcome to Revotic AI LMS!',
            'message': f'Hello {user.username}, your account has been successfully created.',
        }
        if password:
            context['message'] += f'<br><br><strong>Your Temporary Password:</strong> <code>{password}</code><br>Please log in and change your password immediately.'
            
        EmailService.send_async_email(subject, [user.email], "emails/notification.html", context)

    @staticmethod
    def send_password_reset(user, reset_link):
        subject = "Password Reset Request"
        context = {
            'heading': 'Reset Your Password',
            'message': f'Hello {user.username}, you have requested to reset your password. Click the button below to proceed.',
            'cta_text': 'Reset Password',
            'cta_url': reset_link
        }
        EmailService.send_async_email(subject, [user.email], "emails/notification.html", context)

    @staticmethod
    def send_enrollment_notification(student, course, status):
        subject = f"Enrollment {status}"
        message = f'Hello {student.username}, your enrollment request for the course <strong>{course.title} ({course.code})</strong> has been <strong>{status}</strong>.'
        if status.upper() == 'APPROVED':
            message += "<br><br>You can now access the course materials from your student dashboard."
            
        context = {
            'heading': f'Course Enrollment {status}',
            'message': message,
        }
        EmailService.send_async_email(subject, [student.email], "emails/notification.html", context)

    @staticmethod
    def send_assignment_notification(course, assignment):
        subject = f"[{course.code}] New Assignment: {assignment.title}"
        due_date_str = assignment.due_date.strftime('%Y-%m-%d %H:%M') if assignment.due_date else 'No due date'
        message = f"A new assignment has been published in <strong>{course.title}</strong>.<br><br><strong>Assignment:</strong> {assignment.title}<br><strong>Due Date:</strong> {due_date_str}<br><br>Please check your dashboard for more details and submission instructions."
        
        context = {
            'heading': 'New Assignment Published',
            'message': message,
        }
        recipients = [student.user.email for student in course.students.all() if student.user.email]
        if recipients:
            EmailService.send_async_email(subject, recipients, "emails/notification.html", context)

    @staticmethod
    def send_grade_notification(submission):
        subject = "Assignment Graded"
        score = submission.grade.score if hasattr(submission, 'grade') else 'N/A'
        message = f"Hello {submission.student.username}, your submission for <strong>{submission.assignment.title}</strong> has been graded.<br><br><strong>Score:</strong> {score} / {submission.assignment.max_score}<br><br>Login to your dashboard to view detailed feedback."
        
        context = {
            'heading': 'Assignment Graded',
            'message': message,
        }
        EmailService.send_async_email(subject, [submission.student.email], "emails/notification.html", context)

    @staticmethod
    def send_instructor_invitation(email, link):
        subject = "Invitation to Teach"
        message = "Hello, you have been invited to join the Revotic AI LMS as an Instructor."
        
        context = {
            'heading': 'Invitation to Teach',
            'message': message,
            'cta_text': 'Accept Invitation & Register',
            'cta_url': link
        }
        EmailService.send_async_email(subject, [email], "emails/notification.html", context)

    @staticmethod
    def send_announcement(course, message_text):
        subject = f"Announcement: {course.title}"
        message = f"Your instructor has posted a new announcement for <strong>{course.title}</strong>:<br><br><blockquote>{message_text}</blockquote>"
        
        context = {
            'heading': f'New Announcement',
            'message': message,
        }
        recipients = [student.user.email for student in course.students.all() if student.user.email]
        if recipients:
            EmailService.send_async_email(subject, recipients, "emails/notification.html", context)

    @staticmethod
    def send_fee_alert(student, amount, due_date):
        subject = "Fee Payment Reminder"
        message = f"Hello {student.user.username}, this is a reminder that you have an outstanding fee payment.<br><br><strong>Amount:</strong> Rs. {amount}<br><strong>Due Date:</strong> {due_date}<br><br>Please upload your payment proof in the finance section of your dashboard."
        
        context = {
            'heading': 'Fee Payment Reminder',
            'message': message,
        }
        EmailService.send_async_email(subject, [student.user.email], "emails/notification.html", context)

    @staticmethod
    def send_admin_alert(subject, message):
        context = {
            'heading': 'System Alert',
            'message': message,
        }
        # Notify superusers
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admins = User.objects.filter(is_superuser=True).values_list('email', flat=True)
        recipients = [email for email in admins if email]
        if recipients:
            EmailService.send_async_email(subject, recipients, "emails/notification.html", context)

    @staticmethod
    def send_contact_form_email(name, email, subject, message):
        email_subject = f"LMS Contact Form Submission: {subject}"
        message_body = (
            f"You received a new message from the LMS contact form:<br><br>"
            f"<strong>Name:</strong> {name}<br>"
            f"<strong>Email:</strong> {email}<br>"
            f"<strong>Subject:</strong> {subject}<br><br>"
            f"<strong>Message:</strong><br>{message}"
        )
        context = {
            'heading': 'New Contact Form Message',
            'message': message_body,
        }
        EmailService.send_async_email(email_subject, ["management.revoticai@gmail.com"], "emails/notification.html", context)
