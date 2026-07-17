# # File: backend/apps/finance/serializers.py
# # Serializers for finance (Developed by SAYAB)

# from rest_framework import serializers
# from .models import FeeChallan, Payment

# class FeeChallanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FeeChallan
#         fields = "__all__"

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = "__all__"


from rest_framework import serializers
from .models import FeeChallan, Payment, PaymentProof

class FeeChallanSerializer(serializers.ModelSerializer):
    student_detail = serializers.SerializerMethodField()
    total_due = serializers.SerializerMethodField()
    proof_status = serializers.SerializerMethodField()

    class Meta:
        model = FeeChallan
        fields = "__all__"
        extra_kwargs = {'student': {'write_only': True}}

    def get_student_detail(self, obj):
        data = {
            "id": obj.student.id,
            "username": obj.student.username,
            "email": obj.student.email,
            "name": f"{obj.student.first_name} {obj.student.last_name}",
            "cnic": getattr(obj.student, 'cnic', 'N/A')
        }
        try:
            profile = obj.student.student_profile
            data.update({
                "roll_number": profile.roll_number,
                "department": profile.department,
                "program": profile.program,
                "semester": profile.semester
            })
        except:
            data.update({
                "roll_number": "N/A",
                "department": "N/A",
                "program": "N/A",
                "semester": "N/A"
            })
        return data

    def get_total_due(self, obj):
        return float(obj.amount) + float(obj.arrears)

    def get_proof_status(self, obj):
        latest_proof = obj.proofs.order_by('-submitted_at').first()
        if latest_proof:
            return latest_proof.status
        return None

class PaymentSerializer(serializers.ModelSerializer):
    challan_detail = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_challan_detail(self, obj):
        return {
            "id": obj.challan.id,
            "amount": str(obj.challan.amount),
            "due_date": obj.challan.due_date
        }

class PaymentProofSerializer(serializers.ModelSerializer):
    challan_detail = serializers.SerializerMethodField()
    student_detail = serializers.SerializerMethodField()

    class Meta:
        model = PaymentProof
        fields = "__all__"
        read_only_fields = ['verified_by', 'verified_at', 'status']

    def get_challan_detail(self, obj):
        return {
            "id": obj.challan.id,
            "amount": str(obj.challan.amount),
            "arrears": str(obj.challan.arrears),
            "total_due": str(float(obj.challan.amount) + float(obj.challan.arrears)),
            "due_date": obj.challan.due_date
        }

    def get_student_detail(self, obj):
        student = obj.challan.student
        return {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "email": student.email
        }
