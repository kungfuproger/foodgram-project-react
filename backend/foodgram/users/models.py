from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        "Адрес электронной почты",
        unique=True,
        blank=False,
        null=False,
        max_length=254,
    )
    username = models.CharField(
        "Уникальный юзернейм",
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text="Required. 150 characters or fewer. "
        "Letters, digits and @/./+/-/_ only. Can't be 'me' or 'admin'.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField(
        "Имя",
        blank=False,
        null=False,
        max_length=150,
    )
    last_name = models.CharField(
        "Фамилия",
        blank=False,
        null=False,
        max_length=150,
    )
    password = models.CharField(
        "Пароль",
        blank=False,
        null=False,
        max_length=150,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    me = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="my_subscribes"
    )
    my_subscribe = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subscribers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["me", "my_subscribe"], name="subscribe"
            )
        ]
