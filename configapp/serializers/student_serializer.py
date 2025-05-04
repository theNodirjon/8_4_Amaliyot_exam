from rest_framework import serializers
from ..models import Student, User
from .user_serializer import UserSerializer
from .group_serializer import GroupStudentSerializer

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() # Foydalanuvchi ismini chiqaradi
    group = GroupStudentSerializer()

    class Meta:
        model = Student
        user = UserSerializer()  #Userga bog'lanish
        fields = ['id', 'user', 'group']

        def create(self, validated_data):
            user_data = validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            student = Student.objects.create(user=user, **validated_data)
            return student

        def update(self, instance, validated_data):
            user_data = validated_data.pop('user', None)
            if user_data:
                user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
            return super().update(instance, validated_data)

class StudentUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=False)
    is_teacher = serializers.BooleanField(read_only=False)
    is_student = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=False)

    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_staff', 'is_admin', 'is_teacher', 'is_student',)

class StudentPostSerializer(serializers.Serializer):
    user = StudentUserSerializer()
    student = StudentSerializer()