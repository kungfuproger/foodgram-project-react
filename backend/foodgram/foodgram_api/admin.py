from django.contrib import admin

from .models import Ingredient, Tag, Recipe, IngredientAmount


class IngredientAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "id",
        "name",
        "measurement_unit",
    )


class TagAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )


class RecipeAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "id",
        "author",
        "name",
        "image",
        "text",
        "cooking_time",
    )


class IngredientAmountAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "ingredient",
        "amount",
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
