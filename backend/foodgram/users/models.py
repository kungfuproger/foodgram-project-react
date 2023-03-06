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
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class UserSubscription(models.Model):
    """Подписки пользователя."""
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subscriptions",
    )
    publisher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subscribers",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "publisher"],
                name="Подписка уже оформлена",
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F("publisher")),
                name="Нельзя подписаться на себя",
            ),
        ]
