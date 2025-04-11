from rest_framework import status
from rest_framework.response import  Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ..make_token import *
from ..serializers import  *

class LogginApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token = get_token_for_user(user)
        token['Salom'] = 'HI'
        token['is_admin'] = user.is_superuser

        return Response(data=token, status=status.HTTP_200_OK)


