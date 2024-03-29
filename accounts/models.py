from django.db import models
import uuid
from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class myAccountManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("users must have a username")
        if not full_name:
            raise ValueError("Users must provide their full names ")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, full_name):
    
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            full_name=full_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(
        max_length=100, primary_key=True, unique=True, default=uuid.uuid4
    )
    email = models.EmailField(verbose_name="email", max_length=80, unique=True)
    username = models.CharField(unique=True, max_length=50)
    full_name = models.CharField(unique=True, max_length=50)
    is_email_verified = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "full_name"]

    objects = myAccountManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
