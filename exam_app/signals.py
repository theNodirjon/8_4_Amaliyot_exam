from django.core import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import *
from .models.auth_user import User

def send_sms(phone_number, code):
    print(f"SMS sent to {phone_number} with code {code}")

#  Bu - User modeli uchun ishlaydi. Foydalanuvchi yaratilganda avtomatik ravishda tasdiqlash SMS-kodi yuboriladi.

import random

@receiver(post_save, sender=User)
def send_verification_code(sender, instance, created, **kwargs):
    code = random.randint(10000, 99999)
    send_sms(instance.phone_number, code)

    return code


# # OTP yuborish uchun alohida metod yoki API funksiyasini taqdim etish
# def send_otp(phone_number):
#     # Twilio yoki boshqa SMS yuborish tizimidan foydalaning
#     # Misol uchun: send_sms_via_twilio(phone_number)
#     key = str(random.randint(1000, 9999))  # misol uchun tasodifiy 4 xonali OTP
#     # Yuborilgan OTPni keshga saqlash uchun
#     return key

class PhoneSendOtp(APIView):
    # permission_classes = [AllowAny]  # Foydalanuvchi autentifikatsiyasi talab qilinmaydi

    @swagger_auto_schema(request_body=LoginSerializer())
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({
                'status': False,
                'detail': 'Phone number is required!'
            }, status=status.HTTP_400_BAD_REQUEST)

        phone = str(phone_number)  # Telefon raqamini stringga o'tkazish
        user = User.objects.filter(phone_number=phone)  # Telefon raqami orqali foydalanuvchini qidirish

        if user.exists():
            return Response({
                'status': False,
                'detail': 'Phone number already exists!'
            }, status=status.HTTP_400_BAD_REQUEST)

        key = send_verification_code(phone)  # OTP yuborish
        if key:
            cache.set(phone, key, timeout=600)  # OTPni keshga saqlash (10 daqiqa)
            return Response({'message': 'OTP sent successfully!'}, status=status.HTTP_200_OK)

        return Response({'message': 'OTP sending failed!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

