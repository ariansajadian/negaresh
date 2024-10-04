from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from authentication.managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [""]

    def __str__(self):
        return self.email

# Create your models here.
