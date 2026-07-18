# File: backend/apps/notifications/views.py
# Viewset for notifications and messages (Developed by SAYAB)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, Message
from .serializers import NotificationSerializer, MessageSerializer

# from rest_framework import viewsets
# from .models import Notification
# from .serializers import NotificationSerializer

# class NotificationViewSet(viewsets.ModelViewSet):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    Direct Messaging:
    - Users see messages sent to or by them.
    - Admins can see specific audit logs (logic in get_queryset).
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Filter by conversation if recipient provided in query params
        recipient_id = self.request.query_params.get('recipient')
        if recipient_id:
            return Message.objects.filter(
                (Q(sender=user) & Q(recipient_id=recipient_id)) |
                (Q(sender_id=recipient_id) & Q(recipient=user))
            ).order_by('created_at')

        if user.is_staff: 
            # Admin can see:
            # 1. Their own messages (Privacy: no other admin can read them)
            # 2. Student-Teacher logs for monitoring
            return Message.objects.filter(
                Q(sender=user) | Q(recipient=user) |
                (Q(sender__is_student=True) & Q(recipient__is_teacher=True)) |
                (Q(sender__is_teacher=True) & Q(recipient__is_student=True))
            ).distinct().order_by('created_at')
        
        # Default: only user's own messages
        return Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('created_at')

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        # Create a notification for the recipient
        Notification.objects.create(
            recipient=message.recipient,
            title=f"New message from {message.sender.first_name or message.sender.username}",
            message=message.content[:100] + ('...' if len(message.content) > 100 else '')
        )

    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """
        Returns a list of unique users the current user has conversed with.
        """
        user = request.user
        # Get all messages involving the user
        messages = Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-created_at')
        
        contacts = {}
        for msg in messages:
            other_user = msg.recipient if msg.sender == user else msg.sender
            if other_user.id not in contacts:
                # Add unread count for the student/teacher
                unread_count = Message.objects.filter(sender=other_user, recipient=user, is_read=False).count()
                
                contacts[other_user.id] = {
                    'id': other_user.id,
                    'name': f"{other_user.first_name} {other_user.last_name}".strip() or other_user.username,
                    'last_message': msg.content,
                    'timestamp': msg.created_at,
                    'unread_count': unread_count,
                    'is_online': False # Placeholder for now
                }
        
        return Response(list(contacts.values()))

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a specific message as read.
        """
        message = self.get_object()
        if message.recipient == request.user:
            message.is_read = True
            message.save()
            return Response({'status': 'marked as read'})
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def mark_conversation_read(self, request):
        """
        Mark all messages from a specific sender as read.
        """
        sender_id = request.data.get('sender_id')
        if not sender_id:
            return Response({'error': 'sender_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        Message.objects.filter(sender_id=sender_id, recipient=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'conversation marked as read'})
    @action(detail=False, methods=['post'])
    def send_email(self, request):
        """
        API endpoint to send an actual email.
        """
        recipient_email = request.data.get('email')
        subject = request.data.get('subject')
        message_body = request.data.get('message')

        if not all([recipient_email, subject, message_body]):
            return Response({'error': 'Missing email, subject, or message'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from utils.email_service import EmailService
            EmailService.send_async_email(
                subject=subject,
                recipient_list=[recipient_email],
                template_name="emails/notification.html",
                context={'message': message_body, 'heading': subject}
            )
            return Response({'status': 'Email queued successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .models import EmailLog
from rest_framework import serializers

class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'

class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for Admin Dashboard to view and manage emails.
    """
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = EmailLog.objects.count()
        sent = EmailLog.objects.filter(status='SENT').count()
        failed = EmailLog.objects.filter(status='FAILED').count()
        pending = EmailLog.objects.filter(status='PENDING').count()
        
        return Response({
            'total': total,
            'sent': sent,
            'failed': failed,
            'pending': pending,
            'success_rate': round((sent / total * 100), 2) if total > 0 else 0
        })

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        email = self.get_object()
        if email.status != 'FAILED':
            return Response({'error': 'Can only retry failed emails'}, status=status.HTTP_400_BAD_REQUEST)
            
        from utils.email_service import EmailService
        
        success = EmailService.send_template_email(
            subject=email.subject,
            recipient_list=[email.recipient],
            template_name=email.template_name,
            context=email.context_data,
            log_email=False 
        )
        
        if success:
            email.status = 'SENT'
            from django.utils import timezone
            email.sent_at = timezone.now()
            email.error_message = ''
        else:
            email.retry_count += 1
            
        email.save()
        return Response({'success': success, 'status': email.status})
