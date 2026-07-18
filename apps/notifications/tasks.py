from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, recipient_list, template_name, context):
    """
    Celery task to send an email asynchronously.
    """
    from utils.email_service import EmailService
    
    logger.info(f"Executing Celery task: send_email_task to {recipient_list}")
    try:
        # We pass log_email=True so it creates an EmailLog entry
        success = EmailService.send_template_email(subject, recipient_list, template_name, context, log_email=True)
        if success:
            logger.info(f"Successfully sent email to {recipient_list}")
        else:
            logger.error(f"Failed to send email to {recipient_list} from Celery task")
        return success
    except Exception as e:
        logger.error(f"Error in send_email_task: {str(e)}")
        return False
