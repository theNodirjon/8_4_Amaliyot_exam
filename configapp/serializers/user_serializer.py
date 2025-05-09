from rest_framework import serializers
from ..models.auth_users import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['*']

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                password = validated_data.pop('password')
                instance.set_password(password)
            return super().update(instance, validated_data)
