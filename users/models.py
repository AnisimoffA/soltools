from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here. Please work
class CustomUsers(AbstractUser):
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    # тут надо добавить таблицу с кошелями 1 ко многим



    def __str__(self):
        return f"{self.first_name} {self.last_name}"
