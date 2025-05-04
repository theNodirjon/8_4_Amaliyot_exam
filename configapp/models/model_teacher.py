from django.db import models
from rest_framework import filters
from .auth_users import *
from django.contrib.admin import SimpleListFilter

class TeacherUserFilter(SimpleListFilter):
    title = 'User (teachers only)'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        teachers = User.objects.filter(teacher__isnull=False)
        return [(user.id, str(user)) for user in teachers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__id=self.value())
        return queryset


# Markazda oqitiladigan fanlar
class Course(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


# Xodimlarning darajasini belgilash uchun
class Departments(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return f"{self.user.description}"


# Xodimlarning datalarini saqlash uchun yuqoridagi Course va Departments modellari Worker bog'langan
class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.RESTRICT,related_name="teacher")
    groups = models.ManyToManyField('configapp.GroupStudent', max_length=500, related_name='get_teachers')
    # departments = models.ManyToManyField(Departments, related_name='get_department')
    course = models.ManyToManyField(Course, related_name='get_course')
    descriptions = models.CharField(max_length=500, blank=True, null=True)
    subject = models.CharField(max_length=100)  #Mutaxasisligi

    def __str__(self):
        return self.user.phone_number