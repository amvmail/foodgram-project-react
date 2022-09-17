from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Измененная модель User.'''
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        verbose_name='username',
        max_length=100,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=100,
        unique=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=200,
        unique=False
    )
    bio = models.TextField(
        verbose_name='Информация о себе',
        null=True,
        blank=True,
        unique=False
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

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]


class ChangePassword(models.Model):
    old_password = models.CharField(max_length=20)
    new_password = models.CharField(max_length=20)
    confirm_new_password = models.CharField(max_length=20)
