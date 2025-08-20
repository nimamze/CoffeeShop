from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import os
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **kwargs):
        if not phone:
            raise ValueError("Users must have a phone number")
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, email, password, **kwargs)


def user_image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("prof", filename)


class CustomUser(AbstractUser):
    username = None
    phone = models.CharField(unique=True, max_length=15, verbose_name="شماره تلفن")
    email = models.EmailField(verbose_name="ایمیل")
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20, verbose_name="نام")
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی")
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        if self.phone:
            return self.phone
        elif self.email:
            return self.email
        elif self.first_name:
            return self.first_name
        return "User"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
