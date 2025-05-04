import random

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestApi(APIView):
    @swagger_auto_schema(
        operation_description="tasodifiy sonlar uchun",
        manual_parameters=[
        openapi.Parameter('min', openapi.IN_QUERY, description='Minimum' , type=openapi.TYPE_INTEGER),
        openapi.Parameter('max', openapi.IN_QUERY, description='Maximum' , type=openapi.TYPE_INTEGER),
    ]
)

    def get(self,request):
        min_value = int(request.query_params.get('min', 0))
        max_value = int(request.query_params.get('max', 100))

        if min_value > max_value:
            return Response({'detail': 'xato '}, status.HTTP_400_BAD_REQUEST)

        number = random.randint(min_value, max_value)
        return Response({'random number': number}, status.HTTP_200_OK)
