# from .model_student import Student
from .auth_users import *
from .model_teacher import Course


class GroupStudent(BaseModel):
    title = models.CharField(max_length=40, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # student = models.OneToOneField(Student.user, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.title} - {self.course}"