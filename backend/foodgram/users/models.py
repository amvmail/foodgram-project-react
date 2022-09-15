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

    login = models.CharField(
        verbose_name='login',
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
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Информация о себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

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

