from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class IngredientUnit(models.Model):
    """Ингредиент и его единицы измерения."""
    name = models.CharField(
        "Название ингредиента", max_length=200, blank=False, null=False
    )
    measurement_unit = models.CharField(
        "Eдиница измерения", max_length=200, blank=False, null=False
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тег."""
    name = models.CharField("Название тега", max_length=200, unique=True)
    color = models.CharField("Цвет в HEX", max_length=7, unique=True)
    slug = models.SlugField("Уникальный слаг", unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт."""
    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True,
    )
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
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления в минутах",
        validators=[MinValueValidator(1)],
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name

    @property
    def favorites_count(self):
        return self.favorites.count()

    favorites_count.fget.short_description = "Добавивших в избранное"


class IngredientAmount(models.Model):
    """Ингредиент и его колличество в свзянном рецепте."""
    recipe = models.ForeignKey(
        Recipe, related_name="ingredients", on_delete=models.CASCADE
    )
    ingredient_unit = models.ForeignKey(
        IngredientUnit, on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=False,
        verbose_name="Сколько",
    )

    class Meta:
        verbose_name = "Ингредиента в рецепте"
        verbose_name_plural = "Ингредиента в рецептах"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient_unit"],
                name="Ингредиет уже добавлен в рецепт",
            ),
        ]


class Favorite(models.Model):
    """Избранное."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Избранное",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="in_favorites",
        on_delete=models.CASCADE,
        verbose_name="В избранном",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="Рецепт уже добавлен в избранное",
            ),
        ]


class ShoppingCart(models.Model):
    """Корзина."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Корзина",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="in_carts",
        on_delete=models.CASCADE,
        verbose_name="В корзине",
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="Рецепт уже добавлен в корзину",
            ),
        ]
