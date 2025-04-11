from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .signals import PhoneSendOtp
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'teachers', TeacherViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LogginApi.as_view()),  # 👈 APIView uchun `as_view()` ishlatiladi!
    path('post_phone_send_otp/', PhoneSendOtp.as_view(), name='get_phone'),
]
