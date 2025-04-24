from django.db import models

from . import BaseModel
from .model_group import GroupStudent

class Lesson(BaseModel):
    # Darslar model: mavzu, sana, vaqt va qaysi guruhga tegishli
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.title} - {self.group.name} - {self.date}"