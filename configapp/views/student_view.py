from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from ..models import Student, User
from ..serializers import StudentSerializer, StudentUserSerializer, StudentPostSerializer
from ..pagination import StudentPagination



class StudentApi(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentPostSerializer
        return StudentSerializer

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        student_data = request.data.get('student')  # nomni to‘g‘riladik

        serializer_user = StudentUserSerializer(data=user_data)
        serializer_user.is_valid(raise_exception=True)
        validated_user = serializer_user.validated_data
        validated_user['password'] = make_password(validated_user['password'])
        validated_user['is_student'] = True
        validated_user['is_active'] = True

        user = User.objects.create(**validated_user)

        student_serializer = StudentSerializer(data=student_data)
        student_serializer.is_valid(raise_exception=True)
        student = student_serializer.save(user=user)

        if 'departments' in student_data:
            student.departments.set(student_data['departments'])

        if 'course' in student_data:
            student.course.set(student_data['course'])

        response_data = {
            'user': StudentUserSerializer(user).data,
            'student': StudentSerializer(student).data,
            'success': True
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    permission_classes = [IsAuthenticated]


class StudentAdminViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    permission_classes = [IsAdminUser]  # faqat admin




