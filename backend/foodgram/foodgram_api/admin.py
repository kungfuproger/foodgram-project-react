from django.contrib import admin

from .models import (
    IngredientAmount,
    IngredientUnit,
    Recipe,
    Tag,
    Favorite,
    ShoppingCart,
)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class IngredientUnitAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )


class RecipeAdmin(admin.ModelAdmin):
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
                ]
            },
        ),
    ]
    readonly_fields = ("favorites_count",)
    inlines = [IngredientAmountInline, FavoriteInline, ShoppingCartInline]


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        "ingredient_unit",
        "amount",
    )


admin.site.register(IngredientUnit, IngredientUnitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
