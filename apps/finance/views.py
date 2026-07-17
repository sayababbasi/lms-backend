# File: backend/apps/finance/views.py
# Viewsets for finance (Developed by SAYAB)

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import FeeChallan, Payment, PaymentProof
from .serializers import FeeChallanSerializer, PaymentSerializer, PaymentProofSerializer

class FeeChallanViewSet(viewsets.ModelViewSet):
    queryset = FeeChallan.objects.all().order_by('-created_at')
    serializer_class = FeeChallanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['paid', 'student', 'due_date']
    search_fields = ['student__username', 'student__email', 'student__student_profile__roll_number']

    def perform_create(self, serializer):
        student = serializer.validated_data['student']
        arrears = 0
        unpaid_challans = FeeChallan.objects.filter(student=student, paid=False)
        for challan in unpaid_challans:
            arrears += challan.amount
        serializer.save(arrears=arrears)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class StudentChallanViewSet(viewsets.ReadOnlyModelViewSet):
    """Student's personal challans view"""
    serializer_class = FeeChallanSerializer
    
    def get_queryset(self):
        return FeeChallan.objects.filter(student=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def submit_proof(self, request, pk=None):
        """Submit payment proof for a challan"""
        challan = self.get_object()
        
        if challan.paid:
            return Response({'error': 'This challan is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if there's already a pending proof
        existing_pending = challan.proofs.filter(status='pending').exists()
        if existing_pending:
            return Response({'error': 'You already have a pending proof submission'}, status=status.HTTP_400_BAD_REQUEST)
        
        proof_image = request.FILES.get('proof_image')
        if not proof_image:
            return Response({'error': 'proof_image is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        proof = PaymentProof.objects.create(
            challan=challan,
            proof_image=proof_image,
            transaction_reference=request.data.get('transaction_reference', '')
        )
        
        return Response(PaymentProofSerializer(proof).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def my_proofs(self, request):
        """Get all payment proofs submitted by the student"""
        proofs = PaymentProof.objects.filter(challan__student=request.user).order_by('-submitted_at')
        serializer = PaymentProofSerializer(proofs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rerequest_verification(self, request, pk=None):
        """Allow student to re-request verification for a rejected proof"""
        try:
            proof = PaymentProof.objects.get(challan_id=pk, challan__student=request.user)
        except PaymentProof.DoesNotExist:
            return Response({'error': 'Payment proof not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if proof.status != 'rejected':
            return Response({'error': 'Only rejected proofs can be re-requested'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset status to pending
        proof.status = 'pending'
        proof.remarks = ''
        proof.verified_by = None
        proof.verified_at = None
        proof.save()
        
        return Response({'message': 'Verification re-requested successfully', 'proof': PaymentProofSerializer(proof).data})


    @action(detail=False, methods=['get'])

    def summary(self, request):
        """Get financial summary for the student"""
        user = request.user
        challans = FeeChallan.objects.filter(student=user)
        
        total_fees = sum(float(c.amount) + float(c.arrears) for c in challans)
        total_paid = sum(float(c.amount) + float(c.arrears) for c in challans.filter(paid=True))
        total_pending = total_fees - total_paid
        pending_verifications = PaymentProof.objects.filter(challan__student=user, status='pending').count()
        
        return Response({
            'total_fees': total_fees,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'pending_verifications': pending_verifications,
            'unpaid_challans': challans.filter(paid=False).count(),
            'paid_challans': challans.filter(paid=True).count()
        })

class PaymentProofViewSet(viewsets.ModelViewSet):
    """Admin view for managing payment proofs"""
    queryset = PaymentProof.objects.all().order_by('-submitted_at')
    serializer_class = PaymentProofSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a payment proof"""
        proof = self.get_object()
        
        if proof.status != 'pending':
            return Response({'error': 'This proof has already been processed'}, status=status.HTTP_400_BAD_REQUEST)
        
        action_type = request.data.get('action')  # 'approve' or 'reject'
        remarks = request.data.get('remarks', '')
        
        if action_type == 'approve':
            proof.status = 'verified'
            proof.challan.paid = True
            proof.challan.save()
        elif action_type == 'reject':
            proof.status = 'rejected'
        else:
            return Response({'error': 'action must be "approve" or "reject"'}, status=status.HTTP_400_BAD_REQUEST)
        
        proof.verified_by = request.user
        proof.verified_at = timezone.now()
        proof.remarks = remarks
        proof.save()
        
        return Response(PaymentProofSerializer(proof).data)
