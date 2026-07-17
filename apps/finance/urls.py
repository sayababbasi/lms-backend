# File: backend/apps/finance/urls.py
# Router for finance (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeChallanViewSet, PaymentViewSet, StudentChallanViewSet, PaymentProofViewSet

router = DefaultRouter()
router.register(r"challans", FeeChallanViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"student", StudentChallanViewSet, basename='student-challan')
router.register(r"proofs", PaymentProofViewSet)

urlpatterns = [path("", include(router.urls))]
