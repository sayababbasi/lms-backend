# # # # # apps/finance/models.py
# # # # # Developed by SAYAB

# # # # from django.db import models
# # # # from apps.users.models import Student

# # # # class FeeChallan(models.Model):
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     amount = models.DecimalField(max_digits=10, decimal_places=2)
# # # #     due_date = models.DateField()
# # # #     is_paid = models.BooleanField(default=False)
# # # #     created_at = models.DateTimeField(auto_now_add=True)

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} - {self.amount} Challan"

# # # # class Payment(models.Model):
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     challan = models.ForeignKey(FeeChallan, on_delete=models.CASCADE)
# # # #     paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
# # # #     payment_date = models.DateField(auto_now_add=True)
# # # #     payment_method = models.CharField(max_length=50)

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} - {self.paid_amount} Paid"

# # # # class Scholarship(models.Model):
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     title = models.CharField(max_length=100)
# # # #     amount = models.DecimalField(max_digits=10, decimal_places=2)
# # # #     awarded_date = models.DateField(auto_now_add=True)

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} - {self.title}"

# # # # apps/finance/admin.py
# # # # Developed by SAYAB

# # # from django.contrib import admin
# # # from .models import FeeChallan, Payment, Scholarship

# # # @admin.register(FeeChallan)
# # # class FeeChallanAdmin(admin.ModelAdmin):
# # #     list_display = ("student", "amount_due", "due_date", "status")  # ensure these fields exist
# # #     list_filter = ("status", "due_date")

# # # @admin.register(Payment)
# # # class PaymentAdmin(admin.ModelAdmin):
# # #     list_display = ("student", "amount_paid", "paid_on", "payment_method")  # ensure fields match
# # #     list_filter = ("payment_method",)

# # # @admin.register(Scholarship)
# # # class ScholarshipAdmin(admin.ModelAdmin):
# # #     list_display = ("student", "name", "scholarship_type", "amount")  # ensure fields exist
# # #     list_filter = ("scholarship_type",)


# # # apps/finance/models.py
# # # Developed by SAYAB

# # from django.db import models
# # from apps.users.models import Student

# # class FeeChallan(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     amount_due = models.DecimalField(max_digits=10, decimal_places=2)
# #     due_date = models.DateField()
# #     status = models.CharField(max_length=50, choices=[("Paid","Paid"),("Unpaid","Unpaid")])

# #     def __str__(self):
# #         return f"{self.student.user.username} - {self.amount_due}"

# # class Payment(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
# #     paid_on = models.DateTimeField(auto_now_add=True)
# #     payment_method = models.CharField(max_length=50, choices=[("Cash","Cash"),("Card","Card"),("Online","Online")])

# #     def __str__(self):
# #         return f"{self.student.user.username} - {self.amount_paid}"

# # class Scholarship(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     name = models.CharField(max_length=255)
# #     scholarship_type = models.CharField(max_length=100)
# #     amount = models.DecimalField(max_digits=10, decimal_places=2)

# #     def __str__(self):
# #         return f"{self.name} - {self.student.user.username}"

# # File: backend/apps/finance/models.py
# # Minimal finance models: fee challans and payments (Developed by SAYAB)

# from django.db import models
# from django.conf import settings

# class FeeChallan(models.Model):
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="challans")
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     due_date = models.DateField()
#     paid = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Payment(models.Model):
#     challan = models.ForeignKey(FeeChallan, on_delete=models.CASCADE, related_name="payments")
#     transaction_id = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     paid_at = models.DateTimeField(auto_now_add=True)


# File: backend/apps/finance/models.py
# Fee challan & Payment models (Developed by SAYAB)

from django.db import models
from django.conf import settings

class FeeChallan(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="challans")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    arrears = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Challan: {self.student} - {self.amount}"

class Payment(models.Model):
    challan = models.ForeignKey(FeeChallan, on_delete=models.CASCADE, related_name="payments")
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.transaction_id}"

class PaymentProof(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    challan = models.ForeignKey(FeeChallan, on_delete=models.CASCADE, related_name="proofs")
    proof_image = models.ImageField(upload_to='payment_proofs/')
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    verified_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Proof for {self.challan} - {self.status}"
