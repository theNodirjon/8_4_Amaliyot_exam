from drf_yasg.utils import swagger_auto_schema
from ..dekoratir import registr_amalga_oshgan
from ..models.model_pay import Payment
from ..serializers.pay_serializer import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @registr_amalga_oshgan
    @swagger_auto_schema(tags=['Payment'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        operation_description="Foydalanuvchi o‘ziga tegishli barcha to‘lovlarni ko‘rishi.",
        tags=['Payment']
    )
    def my_payments(self, request):
        # Auth user bilan bog‘langan studentni olamiz
        student = getattr(request.user, 'student', None)
        if student is None:
            return Response({"detail": "Siz student emassiz."}, status=403)

        payments = Payment.objects.filter(student=student)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)