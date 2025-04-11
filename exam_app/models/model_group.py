from ..models import *
from .auth_user import *


class GroupStudent(BaseModel):
    title = models.CharField(max_length=50, unique=True)  # xona nomi
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    teacher = models.ManyToManyField(Teacher, related_name='get_teacher')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    start_date = models.DateField()  # boshlasj vaqti
    end_date = models.DateField()   # tugash vaqti
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ['-created']





# ============================_______________________________________________________________________________________________________________________________________________________________________________________________________________________________
# KEYINCHALIK QO'SHILADI
# ============================_______________________________________________________________________________________________________________________________________________________________________________________________________________________________

# class Day(BaseModel):
#     title = models.CharField(max_length=50)
#     descriptions = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.title

# class TableType(BaseModel):
#     title = models.CharField(max_length=50)
#     descriptions = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.title

# class Rooms(BaseModel):
#     title = models.CharField(max_length=50)
#     descriptions = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.title

# class Table(BaseModel):
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     room = models.ForeignKey(Rooms, on_delete=models.RESTRICT)
#     type = models.ForeignKey(TableType, on_delete=models.RESTRICT)
#     descriptions = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.start_time