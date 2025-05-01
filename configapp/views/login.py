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
    @swagger_auto_schema(tags=['Teacher'])
    def get(self, request):
        return Response({"message": "Teacher list"})

    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "detail": "Teacher created"})
        return Response({"status": False, "errors": serializer.errors}, status=400)


class PhoneSendOTP(APIView):
    @swagger_auto_schema(
        request_body=SMSSerializer,
        tags=['Auth'],
        operation_description="Telefon raqamga OTP yuboradi. Agar raqam mavjud bo‘lsa, xatolik qaytaradi."
    )
    def post(self, request, *args, **kwargs):
        serializer = SMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        phone = str(phone_number)

        if User.objects.filter(phone_number__iexact=phone).exists():
            return Response({
                'status': False,
                'detail': 'Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.'
            }, status=status.HTTP_400_BAD_REQUEST)

        otp_code = send_otp()
        if otp_code:
            cache.set(phone, otp_code, 600)  # 10 daqiqa
            return Response({'message': "SMS muvaffaqiyatli yuborildi"}, status=status.HTTP_200_OK)

        return Response({'message': "SMS yuborilmadi"}, status=status.HTTP_400_BAD_REQUEST)


def send_otp():
    otp_code = str(random.randint(1001, 999900))
    return otp_code

class VerifySMS(APIView):
    @swagger_auto_schema(tags=['verify sms'])
    def get(self, request):
        return Response({"message": "sms list"})

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
    @swagger_auto_schema(
        request_body=UserSerializer,
        tags=["Auth"],
        operation_summary="Foydalanuvchini ro‘yxatdan o‘tkazish",
        operation_description="Yangi foydalanuvchi yaratadi. Parol avtomatik tarzda xeshlanadi."
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')
        serializer.validated_data['password'] = make_password(password)
        serializer.save()

        return Response({
            'status': True,
            'detail': 'Account muvaffaqiyatli yaratildi'
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Auth"],
        operation_summary="Foydalanuvchilar ro‘yxatini olish",
        operation_description="Tizimdagi barcha foydalanuvchilar ro‘yxatini qaytaradi."
    )
    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
