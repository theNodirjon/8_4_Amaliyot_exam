from rest_framework import serializers
from ..models.model_pay import Payment
from ..models.model_student import Student

class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Foydalanuvchi nomi chiqadi

    class Meta:
        model = Payment
        fields = '__all__'
