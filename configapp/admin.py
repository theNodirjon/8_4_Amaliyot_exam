from re import search
from django.contrib import admin
from .models import *
from .models.model_pay import Payment

# Register your models here.
admin.site.register([Departments,Course,GroupStudent,Attendance,Payment])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_admin', 'is_teacher', 'is_student', 'is_active', 'is_staff')
    list_filter = ('is_admin', 'is_teacher', 'is_student', 'is_active', 'is_staff')
    search_fields = ('phone_number',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'descriptions', 'subject',)
    list_filter = (TeacherUserFilter, 'descriptions', 'subject')
    search_fields = ('phone_number',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'get_groups')  # group o‘rniga get_groups
    list_filter = ('user', 'phone')  # list_filter da ManyToManyField ishlamaydi
    search_fields = ('phone_number',)

    def get_groups(self, obj):
        return ", ".join([str(group.title) for group in obj.group.all()])
    get_groups.short_description = 'Groups'
