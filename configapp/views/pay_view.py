from rest_framework import viewsets
from ..models.model_pay import Payment
from ..serializers.pay_serializer import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    # O‘quvchi o‘zining to‘lov tarixini ko‘rishi uchun endpoint
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        student = getattr(request.user, 'student', None)
        if student is not None:
            payments = Payment.objects.filter(student=student)
            serializer = self.get_serializer(payments, many=True)
            return Response(serializer.data)
        return Response({"detail": "Siz student emassiz."}, status=403)
