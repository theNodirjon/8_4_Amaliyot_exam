from django.db import models
from .model_group import GroupStudent

class Homework(models.Model):
    # Uy vazifasi: guruh, mavzu, deadline
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.group.name}"
