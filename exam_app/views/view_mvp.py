from django.shortcuts import render
from rest_framework import viewsets
from exam_app.models import User, Student, Group, Teacher
from exam_app.serializers import UserSerializer, StudentSerializer, GroupSerializer, TeacherSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# class TeacherViewSet(viewsets.ModelViewSet):
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer
