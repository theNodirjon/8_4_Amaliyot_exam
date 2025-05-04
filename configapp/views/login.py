import json
import os
import random
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..make_token import *
from ..serializers import *


class LoginApi(APIView):
    permission_classes = [AllowAny]

    # Login endpoint - token olish uchun
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token = get_tokens_for_user(user)
        token['is_admin'] = user.is_admin
        return Response(data=token, status=status.HTTP_200_OK)


class TeacherCreateApi(APIView):
    # Faqat test uchun - Teacher ro'yxati va yaratish
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
    # Telefon raqamga OTP yuboradi
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

        # Telefon raqam avval ro'yxatdan o'tganligini tekshiradi
        if User.objects.filter(phone_number__iexact=phone).exists():
            return Response({
                'status': False,
                'detail': 'Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # OTP generatsiya va log qilish
        otp_code = send_otp_and_log(phone)
        if otp_code:
            cache.set(phone, otp_code, 600)  # 10 daqiqa saqlanadi
            return Response({'message': "SMS muvaffaqiyatli yuborildi va log qilindi"}, status=status.HTTP_200_OK)

        return Response({'message': "SMS yuborilmadi"}, status=status.HTTP_400_BAD_REQUEST)


def send_otp_and_log(phone):
    # OTP kod generatsiya qilinadi
    otp_code = str(random.randint(1001, 9999))
    log_dir = os.path.join(settings.BASE_DIR, 'sms_logs')  # Log fayllar joylashgan papka
    log_file = os.path.join(log_dir, 'otp_log.json')       # JSON fayl yo'li

    os.makedirs(log_dir, exist_ok=True)  # Papka mavjud bo'lmasa yaratadi

    # Fayl bo'lmasa, bo'sh dict yoziladi
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            json.dump({}, f)

    # Eski log ma'lumotlarini o'qish
    with open(log_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    # Hozirgi vaqtni olish
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Telefon raqam uchun yangi yozuv qo'shish
    if phone not in data:
        data[phone] = []

    data[phone].append({
        "code": otp_code,
        "timestamp": now
    })

    # Yangi ma'lumotni faylga yozish
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=4)

    return otp_code


class VerifySMS(APIView):
    # OTP kodni tekshiruvchi endpoint
    @swagger_auto_schema(
        request_body=VerifySMSSerializer,
        tags=['Auth'],
        operation_summary="OTP tasdiqlash",
        operation_description="Kiritilgan OTP kodni tekshiradi."
    )
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        verification_code = serializer.validated_data['verification_code']
        cached_code = cache.get(phone_number)

        # Agar kod mavjud bo'lmasa yoki muddati o'tgan bo'lsa
        if cached_code is None:
            return Response({
                'status': False,
                'detail': 'Bu raqam uchun kod topilmadi yoki muddati tugagan.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Kodlar mos kelsa
        if str(cached_code) == str(verification_code):
            return Response({
                'status': True,
                'detail': 'OTP to‘g‘ri. Ro‘yxatdan o‘tishni davom ettiring.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'detail': 'OTP noto‘g‘ri.'
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserApi(APIView):
    # Ro'yxatdan o'tish endpointi
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

    # Foydalanuvchilar ro'yxatini olish
    @swagger_auto_schema(
        tags=["Auth"],
        operation_summary="Foydalanuvchilar ro‘yxatini olish",
        operation_description="Tizimdagi barcha foydalanuvchilar ro‘yxatini qaytaradi."
    )
    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
