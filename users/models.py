from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен для заполнения')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        phone_number = extra_fields.get('phone_number')
        if not phone_number:
            raise ValueError('Для суперпользователя номер телефона обязателен.')
        if not str(phone_number).startswith('996'):
            raise ValueError('Номер телефона суперпользователя должен начинаться с 996.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REGISTRATION_SOURCES = (
        ('local', 'Local'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    registration_source = models.CharField(
        max_length=20,
        choices=REGISTRATION_SOURCES,
        default='local'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email