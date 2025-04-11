from django.db import models
from .auth_user import BaseModel, User
from .model_teacher import *

class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='student')
    groups = models.ManyToManyField("GroupStudent", blank=True, related_name="get_group")
    # course = models.ManyToManyField(Course, blank=True, related_name="student")
    is_line = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.phone_number

class Parents(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
