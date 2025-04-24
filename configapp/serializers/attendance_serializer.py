from rest_framework import serializers
from ..models import Attendance
from ..models.model_student import Student
from ..models.model_lessons import Lesson

class AttendanceSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField()  # Dars nomi chiqadi
    present_students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    excused_students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

    class Meta:
        model = Attendance
        fields = '__all__'
