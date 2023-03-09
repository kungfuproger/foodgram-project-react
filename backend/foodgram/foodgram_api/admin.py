from django.contrib import admin

from .models import (
    Favorite,
    IngredientAmount,
    IngredientUnit,
    Recipe,
    ShoppingCart,
    Tag,
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
                    "text",
                    "favorites_count",
                    "cooking_time",
                    "image",
                    "tags",
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


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )


admin.site.register(IngredientUnit, IngredientUnitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
