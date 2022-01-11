from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=('email address'),
        unique=True
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email', 'username')
        verbose_name = "user"
        verbose_name_plural = "users"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='following user'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='followed user'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name="unique_followers"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(user=models.F("author")),
            ),
        ]
        verbose_name = "follow_user"
        verbose_name_plural = "follow_users"

    def __str__(self):
        return self.user.username[:15] + '-->' + self.author.username[:15]

    def __repr__(self):
        return self.user.username[:15] + '-->' + self.author.username[:15]
