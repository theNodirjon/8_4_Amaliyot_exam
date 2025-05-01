from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from ..models import Lesson
from ..pagination import LessonPagination
from ..serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Lesson'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

