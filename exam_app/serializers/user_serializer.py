from rest_framework import serializers
from ..models import *

#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'phone_number', 'role']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'password', 'is_teacher']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class DepartmentsSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, required=False)  # Bir nechta foydalanuvchilar bo‘lishi mumkin

    class Meta:
        model = Departments
        fields = '__all__'

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])  # Foydalanuvchilar ma'lumotlarini ajratib olamiz
        department = Departments.objects.create(**validated_data)

        for user_data in users_data:
            User.objects.create(department=department, **user_data)  # Foydalanuvchi yaratamiz

        return department
