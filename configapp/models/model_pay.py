from django.db import models
from .model_student import Student

class Payment(models.Model):
    # To'lov modeli: qaysi student, qancha va qachon to'lov qilgan
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # qiymati
    payment_date = models.DateField() #tolo'v sanasi

    def __str__(self):
        return f"{self.student} - {self.amount} so‘m - {self.payment_date}"
