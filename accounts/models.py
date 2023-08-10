from django.db import models
from django.contrib.auth.models import AbstractUser, User #bu orqali biz user ga qo'shimcha kiritaolamz


"""class User(AbstractUser):
    photo=models.ImageField() # bu usulni biz abstractuserni loyihaning boshidan ishlatib kelsakkina foydalanamiz
    date_of_birth=models.DateTimeField()
    address=models.TextField()"""

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='users/', blank=True, null=True)
    date_of_birth=models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} profili"




