from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from .views.group_view import *
from .views.lesson_view import LessonViewSet
from .views.pay_view import PaymentViewSet
from .views.teacher_views import *
from .views.student_view import *
from .views.attendance_view import *
from .views.test_view import TestApi

router = DefaultRouter()
router.register(r'teacher_api', TeacherApi, basename='teacher_api')
router.register(r'teacher_view', TeacherViewSet, basename='teacher_view')
router.register(r'teachers_crud', TeacherAdminViewSet, basename='teachers_crud')


router.register(r'student_api', StudentApi, basename='student_api')
router.register(r'student_view', StudentViewSet, basename='student_view')
router.register(r'student_crud', StudentAdminViewSet, basename='student_crud')


router.register(r'group', GroupViewSet, basename='group')
router.register(r'davomat', AttendanceViewSet, basename='davomat')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('post_send_otp/', PhoneSendOTP.as_view()),
    path('post_v_otp/', VerifySMS.as_view()),
    path('register/', RegisterUserApi.as_view()),
    path('token/', LoginApi.as_view(), name='token'),
    path('teacher/create/', TeacherCreateApi.as_view(), name='teacher-create'),
    path('random_number/', TestApi.as_view(), name='random-number' ),
    path('', include(router.urls)),
]

