from datetime import timedelta

from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Attendance, Teacher, Student
from ..serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Attendance'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Attendance.objects.filter(teacher=Teacher)
        return Attendance.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)


    # Qo‘shimcha custom API: yo‘qlama statistikasi (jami/kelgan/sababli/kemagan)
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        attendance = self.get_object()
        group = attendance.lesson.group
        all_students = Student.objects.filter(group=group)
        present_ids = attendance.present_students.values_list('id', flat=True)
        excused_ids = attendance.excused_students.values_list('id', flat=True)
        absent_ids = all_students.exclude(id__in=present_ids).exclude(id__in=excused_ids).values_list('id', flat=True)

        return Response({
            'jami_student': all_students.count(),
            'kelgan_student': list(present_ids),
            'sababli_student': list(excused_ids),
            'kemagan_student': list(absent_ids),
        })

    #  Butun guruh uchun bitta yo‘qlama bilan qatnashuvni belgilash
    @action(detail=True, methods=['post'])
    def mark_group_attendance(self, request, pk=None):
        attendance = self.get_object()
        lesson = attendance.lesson
        group_students = Student.objects.filter(group=lesson.group)

        present_ids = request.data.get('present_students', []) #kegan
        excused_ids = request.data.get('excused_students', []) #sababli

        attendance.present_students.set(present_ids)
        attendance.excused_students.set(excused_ids)

        return Response({
            'detail': 'Guruh uchun yo‘qlama saqlandi.',
            'jami_student': group_students.count(),
            'kelgan_student': present_ids,
            'sababli_student': excused_ids,
            'kemagan_student': list(
                group_students.exclude(id__in=present_ids).exclude(id__in=excused_ids).values_list('id', flat=True))
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        attendance = self.get_object()
        group = attendance.lesson.group
        all_students = Student.objects.filter(group=group)
        present_ids = attendance.present_students.values_list('id', flat=True)
        excused_ids = attendance.excused_students.values_list('id', flat=True)
        absent_ids = all_students.exclude(id__in=present_ids).exclude(id__in=excused_ids).values_list('id', flat=True)

        return Response({
            'jami_student': all_students.count(),
            'kelgan_student': list(present_ids),
            'sababli_student': list(excused_ids),
            'kemagan_student': list(absent_ids),
        })

    # Attendance-Yo'qlama statistikasi (30 kunlik davomat)
    @action(detail=False, methods=['get'])
    def last_30_days(self, request):
        today = now().date()
        start_date = today - timedelta(days=30)
        user = request.user

        # Agar Teacher bo‘lsa, o‘z guruhidagi studentlarning statistikasi
        attendances = Attendance.objects.filter(
            date__range=(start_date, today),
            student__group__teacher=user
        )

        total = attendances.count()
        present = attendances.filter(status='present').count()
        absent = attendances.filter(status='absent').count()

        return Response({
            "total_records": total,
            "present": present,
            "absent": absent,
            "from": start_date,
            "to": today
        })
