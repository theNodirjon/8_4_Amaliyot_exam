from django.db import models
from django.utils import timezone

from .model_student import *
from .model_lessons import Lesson

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'), #bor
        ('absent', 'Absent'), #yo'q
    )
    # Yo'qlama modeli: darsga qatnashgan, sababli kelmagan va kelmaganlar
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=timezone.now)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    present_students = models.ManyToManyField(Student, related_name='attended')
    excused_students = models.ManyToManyField(Student, related_name='excused')

    def total_students(self):
        # Jami studentlar soni - darsdagi guruhga qarab olinadi
        return self.lesson.group.student_set.count()

    def absent_students(self):
        # Kelmaganlar: jami - (kelgan + sababli)
        present_ids = self.present_students.values_list('id', flat=True)
        excused_ids = self.excused_students.values_list('id', flat=True)
        return self.lesson.group.student_set.exclude(id__in=present_ids.union(excused_ids))

    def __str__(self):
        return f"Yo'qlama - {self.lesson}"