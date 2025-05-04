from rest_framework import serializers
from ..models.model_pay import Payment

class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # faqat o‘qish uchun

    class Meta:
        model = Payment
        fields = '__all__'
