from .model_group import *
from .model_teacher import *
from .auth_users import User


class Student(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    group = models.ManyToManyField(GroupStudent,related_name='get_student')
    # descreptions = models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.user.phone_number