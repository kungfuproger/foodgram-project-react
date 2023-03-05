from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "name",
        "color",
        "slug",
    )


class RecipeAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "name",
        "author",
    )
    list_filter = (
        "name",
        "author",
        "tags",
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "author",
                    "name",
                    "image",
                    "text",
                    "ingredients",
                    "cooking_time",
                ]
            },
        ),
        (
            "Дполнительно",
            {
                "fields": [
                    "tags",
                    "favorites_count",
                    "favorited_users",
                    "carted_users",
                ]
            },
        ),
    ]
    readonly_fields = ("favorites_count",)


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
