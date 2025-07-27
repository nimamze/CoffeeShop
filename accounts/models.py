from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):

    def create_user(self,phone,email,password,**kwargs):

        email = self.normalize_email(email)
        user = self.model(phone = phone,**kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,phone,email,password,**kwargs):

        kwargs.setdefault("is_staff", True) 
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        return self.create_user(phone,email, password, **kwargs)  

    
class CustomUser(AbstractUser):

    username = None
    phone = models.CharField(unique=True,max_length=15)
    email = models.EmailField()
    image = models.ImageField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    USERNAME_FIELD = 'phone'
    objects = CustomUserManager() # type: ignore

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"