from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from ..models import Teacher, Student
from ..serializers import TeacherSerializer
from ..serializers.teacher_serializer import TeacherSerializer, TeacherPostSerializer, TeacherUserSerializer
from ..models import User
from ..permissions import IsGetOrPatchOnly
from ..pagination import TeacherPagination
from rest_framework.decorators import action



class TeacherApi(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = TeacherPagination
    permission_classes = [IsGetOrPatchOnly]

    def get_serializer_class(self):
        data={'success':True}
        if self.action == 'create':
            return TeacherPostSerializer
        return TeacherSerializer

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        teacher_data = request.data.get('teacher')

        user_serializer = TeacherUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        validated_user = user_serializer.validated_data
        validated_user['password'] = make_password(validated_user['password'])
        validated_user['is_teacher'] = True
        validated_user['is_active'] = True

        user = User.objects.create(**validated_user)

        teacher_serializer = TeacherSerializer(data=teacher_data)
        teacher_serializer.is_valid(raise_exception=True)

        teacher = teacher_serializer.save(user=user)

        if 'departments' in teacher_data:
            teacher.departments.set(teacher_data['departments'])
        if 'course' in teacher_data:
            teacher.course.set(teacher_data['course'])

        response_data = {
            'user': TeacherUserSerializer(user).data,
            'teacher': TeacherSerializer(teacher).data,
            'success': True
        }
        return Response(response_data, status=status.HTTP_201_CREATED)



class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = TeacherPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Agar foydalanuvchi teacher bo‘lsa, faqat o‘z guruhidagi studentlarni ko‘rsatadi
        if hasattr(user, 'teacher'):
            group = user.teacher.group
            return Student.objects.filter(group=group)
        return Student.objects.all()

    # Teacher faqat o'z guruhini ko'rishi uchun custom action
    @action(detail=False, methods=['get'])
    def my_group_students(self, request):
        user = request.user
        if hasattr(user, 'teacher'):
            group = user.teacher.group
            students = Student.objects.filter(group=group)
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)
        return Response({"detail": "Siz teacher emassiz."}, status=403)


class TeacherAdminViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = TeacherPagination
    permission_classes = [IsAdminUser]  # faqat admin




























#
#
#
#
# class TeacherApi(APIView):
#     @swagger_auto_schema(request_body=TeacherPostSerializer)
#     def post(self, request):
#         data = {"success": True}
#         user_data = request.data['user']
#         teacher_data = request.data['teacher']
#
#         user_serializer = TeacherUserSerializer(data=user_data)
#         user_serializer.is_valid(raise_exception=True)
#
#         validated_user = user_serializer.validated_data
#         validated_user['password'] = make_password(validated_user['password'])
#         validated_user['is_teacher'] = True
#         validated_user['is_active'] = True
#
#         user = User.objects.create(**validated_user)
#
#         teacher_serializer = TeacherSerisalizer(data=teacher_data)
#         teacher_serializer.is_valid(raise_exception=True)
#
#         teacher = teacher_serializer.save(user=user)
#
#         if 'departments' in teacher_data:
#             teacher.departments.set(teacher_data['departments'])
#         if 'course' in teacher_data:
#             teacher.course.set(teacher_data['course'])
#
#         data['user'] = TeacherUserSerializer(user).data
#         data['teacher'] = TeacherSerisalizer(teacher).data
#         return Response(data)
#
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from django.contrib.auth.hashers import make_password
# from rest_framework.response import Response
# from rest_framework import status
#
# from ..models import Teacher, User
# from ..serializers.teacher_serializer import (TeacherSerializer,TeacherPostSerializer,TeacherUserSerializer
# )
