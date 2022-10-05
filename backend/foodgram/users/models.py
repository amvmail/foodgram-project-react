# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''Измененная модель User.'''
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=200,
        null=True,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )
    first_name = models.TextField(
        verbose_name='Имя',
        null=True,
    )
    last_name = models.TextField(
        verbose_name='Имя',
        null=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
