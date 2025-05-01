from .model_group import *
from .model_teacher import *
from .auth_users import User


class Student(BaseModel):
    # Student model: user bilan OneToOne va guruh bilan ForeignKey
    STATUS_CHOICES = (
        ("registered", "Ro'yxatdan o'tgan"),
        ("studying", "O'qiyotgan"),
        ("graduated", "Bitirib ketgan"),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    group = models.ManyToManyField('configapp.GroupStudent', related_name='get_student', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="registered")


    def __str__(self):
        return f"{self.user.phone_number}"