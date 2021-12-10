from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=('email address'),
        unique=True,
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email', 'username')