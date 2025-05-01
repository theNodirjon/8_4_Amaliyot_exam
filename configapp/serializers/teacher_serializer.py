from rest_framework import serializers

from . import UserSerializer
from ..models import *

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Foydalanuvchi ismini chiqaradi

    class Meta:
        model = Teacher
        user = UserSerializer()
        fields = ['id','user','course','descriptions','subject']

        def create(self, validated_data):
            user_data = validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            teacher = Teacher.objects.create(user=user, **validated_data)
            return teacher

        def update(self, instance, validated_data):
            user_data = validated_data.pop('user', None)
            if user_data:
                user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
            return super().update(instance, validated_data)



class TeacherUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=False)
    is_teacher = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=False)


    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_staff', 'is_admin', 'is_teacher', 'is_student')



class TeacherPostSerializer(serializers.Serializer):
    user = TeacherUserSerializer()
    teacher = TeacherSerializer()