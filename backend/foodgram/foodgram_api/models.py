from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from core.models import CreatedModel
from users.models import User


class Ingredient(CreatedModel):
    """Ингредиент."""

    name = models.CharField(
        "Название ингредиента", max_length=200, blank=False, null=False
    )
    measurement_unit = models.CharField(
        "Eдиница измерения", max_length=200, blank=False, null=False
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(CreatedModel):
    """Тег."""

    name = models.CharField("Название тега", max_length=200, unique=True)
    color = models.CharField("Цвет в HEX", max_length=7, unique=True)
    slug = models.SlugField("Уникальный слаг", unique=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class IngredientAmount(CreatedModel):
    """
    Промежуточная модель - конкретный ингредиент
    и его колличество в рецепте.
    """

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Количество ингредиента в рецепте"
        verbose_name_plural = "Записи количества ингредиентов в рецептах"


class Recipe(CreatedModel):
    """Рецепт."""

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
        "Изображение",
        upload_to="recipes/images/%Y/%m/%d/",
        null=False,
        blank=False,
    )
    text = models.TextField("Описание", blank=False, null=False)
    ingredients = models.ManyToManyField(
        IngredientAmount, related_name="recipes", verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    cooking_time = models.IntegerField(
        "Время приготовления в минутах",
        validators=[MinValueValidator(1)],
        blank=False,
        null=False,
    )
    favorited_users = models.ManyToManyField(
        User,
        related_name="favorites",
        verbose_name="Добавили в избранное",
        blank=True,
        null=True,
    )
    carted_users = models.ManyToManyField(
        User,
        related_name="in_cart",
        verbose_name="Добавили в корзину",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name

    @property
    def favorites_count(self):
        return self.favorited_users.count()

    favorites_count.fget.short_description = "Добавивших в избранное"
