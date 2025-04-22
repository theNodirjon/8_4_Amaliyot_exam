from django.db import models
from . import Student, Teacher
from . import GroupStudent

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # True = bor, False = yo'q

    def __str__(self):
        return f"{self.student.user.first_name} - {self.date} - {'Bor' if self.status else 'Yo‘q'}"
