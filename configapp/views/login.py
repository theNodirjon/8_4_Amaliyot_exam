from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..make_token import *
from ..serializers import *
import random

class LoginApi(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token = get_tokens_for_user(user)
        token['is_admin'] = user.is_admin
        return Response(data=token, status=status.HTTP_200_OK)

class TeacherCreateApi(APIView):
    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "detail": "Teacher created"})
        return Response({"status": False, "errors": serializer.errors}, status=400)

class PhoneSendOTP(APIView):
    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone_number__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'Phone number already exist'
                })
            else:
                key = send_otp()
                print("=======================", key)
                if key:
                    # Verification code cache for 5 minutes
                    cache.set(phone_number, key, 600)
                    return Response({'message': "SMS sent successfully"}, status=status.HTTP_200_OK)
                return Response({'message': "SMS sent Failed"}, status=status.HTTP_400_BAD_REQUEST)

def send_otp():
    otp = str(random.randint(1001, 999900))
    return otp

class VerifySMS(APIView):
    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))
            if verification_code == str(cached_code):
                return Response({
                    'status':True,
                    'detail': 'Otp matched. proceed for registration'
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'Otp INCORRECT'
                })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserApi(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response({
                    'status': True,
                    'detail': 'CREATE Account'
            })

    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)
