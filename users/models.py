import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='номер телефона')

    verify_code = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Код верификации')
    is_verified = models.BooleanField(default=False, verbose_name='Верификация')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('block_user', 'Заблокировать пользователя')
        ]
