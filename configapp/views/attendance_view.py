from rest_framework import viewsets, permissions
from ..models import Attendance, Teacher
from ..serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Attendance.objects.filter(teacher=Teacher)
        return Attendance.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)
