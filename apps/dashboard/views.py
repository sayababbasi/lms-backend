from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.models import Student
from apps.courses.models import Course
from apps.assignments.models import Assignment
from apps.finance.models import Payment
from django.db.models import Sum
from django.utils import timezone

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        last_month = now - timezone.timedelta(days=30)
        last_week = now - timezone.timedelta(days=7)
        last_year = now - timezone.timedelta(days=365)

        # 1. Basic Stats
        total_students = Student.objects.count()
        active_courses = Course.objects.count()
        pending_assignments = Assignment.objects.filter(due_date__gte=now).count()

        # 2. Revenue Stats
        total_revenue_agg = Payment.objects.aggregate(Sum('amount'))
        total_revenue = total_revenue_agg['amount__sum'] or 0

        revenue_month_agg = Payment.objects.filter(paid_at__gte=last_month).aggregate(Sum('amount'))
        revenue_month = revenue_month_agg['amount__sum'] or 0

        revenue_week_agg = Payment.objects.filter(paid_at__gte=last_week).aggregate(Sum('amount'))
        revenue_week = revenue_week_agg['amount__sum'] or 0

        revenue_year_agg = Payment.objects.filter(paid_at__gte=last_year).aggregate(Sum('amount'))
        revenue_year = revenue_year_agg['amount__sum'] or 0

        # 3. Fee & Enrollment Stats
        # Assuming FeeChallan model has 'paid' boolean
        from apps.finance.models import FeeChallan
        paid_challans = FeeChallan.objects.filter(paid=True).count()
        total_challans = FeeChallan.objects.count()

        # Active Users (Last Month) - utilizing AbstractUser's last_login
        # Need to ensure User model is imported if not already, usually accessed via request.user or direct import
        from django.contrib.auth import get_user_model
        User = get_user_model()
        active_users_last_month = User.objects.filter(last_login__gte=last_month).count()

        # Course Enrollments
        # Get top courses by enrollment
        courses_data = []
        for course in Course.objects.all():
            courses_data.append({
                "title": course.title,
                "code": course.code,
                "students": course.students.count()
            })

        data = {
            "total_students": total_students,
            "active_courses": active_courses,
            "pending_assignments": pending_assignments,
            "total_revenue": total_revenue,
            "detailed_stats": {
                "revenue": {
                    "last_week": revenue_week,
                    "last_month": revenue_month,
                    "last_year": revenue_year,
                },
                "fees": {
                    "paid_challans": paid_challans,
                    "total_challans": total_challans,
                },
                "users": {
                    "active_last_month": active_users_last_month
                },
                "courses": courses_data
            }
        }

        return Response(data)
