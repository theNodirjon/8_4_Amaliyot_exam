from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from .views.group_view import *
from .views.teacher_views import *
from .views.student_view import *
from .views.attendance_view import *

router = DefaultRouter()
router.register(r'teacher_api', TeacherApi, basename='teacher_api')
router.register(r'teacher_view', TeacherViewSet, basename='teacher_view')
router.register(r'teachers_crud', TeacherAdminViewSet, basename='teachers_crud')


router.register(r'student_api', StudentApi, basename='student_api')
router.register(r'student_view', StudentViewSet, basename='student_view')
router.register(r'student_crud', StudentAdminViewSet, basename='student_crud')


router.register(r'group', GroupViewSet, basename='group')
router.register('davomat', AttendanceViewSet, basename='davomat')

urlpatterns = [
    path('post_send_otp/', PhoneSendOTP.as_view()),
    path('post_v_otp/', VerifySMS.as_view()),
    path('register/', RegisterUserApi.as_view()),
    path('token/', LoginApi.as_view(), name='token'),
    path('teacher/create/', TeacherCreateApi.as_view(), name='teacher-create'),
    path('', include(router.urls)),
]


'''
Student yaratish: json

POST /api/students_cdud/  # 3/ 

{
  "user": {
    "username": "student1",
    "password": "1234"
  },
  "phone": "+998901234567"
}
'''