from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        "Название ингредиента", max_length=200, blank=False, null=False
    )
    measurement_unit = models.CharField(
        "Eдиница измерения", max_length=200, blank=False, null=False
    )


class Tag(models.Model):
    name = models.CharField(
        "Название тега", max_length=200, unique=True, blank=False, null=False
    )
    color = models.CharField(
        "Цвет в HEX", max_length=7, unique=True, blank=False, null=False
    )
    slug = models.SlugField(
        "Уникальный слаг", unique=True, blank=False, null=False
    )


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
        blank=False,
        null=False,
    )
    name = models.CharField(
        "Название рецепта", max_length=200, blank=False, null=False
    )
    image = models.ImageField(
        "Картинка, закодированная в Base64",
        upload_to="recipes/images/%Y/%m/%d/",
        null=True,
        default=None,
        blank=False,
    )
    text = models.TextField("Описание", blank=False, null=False)
    ingredients = models.ManyToManyField(
        IngredientAmount, related_name="recipes", verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False
    )
    favorited_users = models.ManyToManyField(User, related_name="favorites", verbose_name="Добавили в избранное")
    carted_users = models.ManyToManyField(User, related_name="in_cart", verbose_name="Добавили в корзину")
