from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "saccess": False,
                    "detail":"User does not exist"
                }
            )

        auth_user = authenticate(username=username, password=password)
        if not auth_user is None:
            raise serializers.ValidationError(
                {
                    "saccess": False,
                    "detail":"Username or password is incorrect"
                }
            )
        attrs ["user"] = auth_user
        return attrs

