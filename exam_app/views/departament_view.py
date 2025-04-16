from rest_framework import viewsets
from ..models import Departments
from ..serializers import DepartmentsSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer

    @swagger_auto_schema(
        request_body=DepartmentsSerializer,
        responses={201: DepartmentsSerializer},
        operation_description="Yangi bo'lim yaratish va foydalanuvchilarni kiritish",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
