# # # apps/finance/admin.py
# # # Developed by SAYAB

# # from django.contrib import admin
# # from .models import FeeChallan, Payment, Scholarship

# # @admin.register(FeeChallan)
# # class FeeChallanAdmin(admin.ModelAdmin):
# #     list_display = ("student", "amount", "due_date", "status")
# #     list_filter = ("status",)

# # @admin.register(Payment)
# # class PaymentAdmin(admin.ModelAdmin):
# #     list_display = ("student", "amount", "paid_at", "method")
# #     list_filter = ("method",)

# # @admin.register(Scholarship)
# # class ScholarshipAdmin(admin.ModelAdmin):
# #     list_display = ("student", "amount", "type")


# # apps/finance/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import FeeChallan, Payment, Scholarship

# @admin.register(FeeChallan)
# class FeeChallanAdmin(admin.ModelAdmin):
#     list_display = ("student", "amount_due", "due_date", "status")
#     list_filter = ("status",)
#     search_fields = ("student__user__username",)

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ("student", "amount_paid", "paid_on", "payment_method")
#     list_filter = ("payment_method",)
#     search_fields = ("student__user__username",)

# @admin.register(Scholarship)
# class ScholarshipAdmin(admin.ModelAdmin):
#     list_display = ("student", "name", "scholarship_type", "amount")
#     list_filter = ("scholarship_type",)
#     search_fields = ("student__user__username",)


# File: backend/apps/finance/admin.py
# Admin registration for finance (Developed by SAYAB)

from django.contrib import admin
from .models import FeeChallan, Payment

admin.site.register(FeeChallan)
admin.site.register(Payment)
