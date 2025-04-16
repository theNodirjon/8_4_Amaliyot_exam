from rest_framework import serializers
from ..models import Departments, User


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'

        # def create_user(self, data):
        #     user = User()
        #     user.id = data['id']
        #     user.first_name = data['first_name']
        #     user.last_name = data['last_name']
        #     phone_number = data['phone_number']
        #     user.phone_number = phone_number
        #
        #     return user