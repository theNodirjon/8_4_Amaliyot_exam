
from rest_framework import viewsets
from ..models import GroupStudent
from ..pagination import GroupPagination
from ..serializers import GroupStudentSerializer
from rest_framework.permissions import IsAuthenticated



class GroupViewSet(viewsets.ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    pagination_class = GroupPagination
    permission_classes = [IsAuthenticated]