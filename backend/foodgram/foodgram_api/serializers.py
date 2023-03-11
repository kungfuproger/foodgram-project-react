import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import IngredientAmount, IngredientUnit, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор объектов Tag, для TagsViewSet."""
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientUnitSerializer(serializers.ModelSerializer):
    """Сериализатор объектов Ingredient, для IngredientsViewSet."""
    class Meta:
        model = IngredientUnit
        fields = ("id", "name", "measurement_unit")


class Base64ImageField(serializers.ImageField):
    """
    Кастомное поле. Для RecipeSerializer.
    Принимает - данные формата Base64.
    Отдает - сериализованное ImageField.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            formatstr, imgstr = data.split(";base64,")
            ext = formatstr.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="image." + ext)
        return super().to_internal_value(data)


class CustomTagsField(TagSerializer):
    """
    Кастомное поле. Для RecipeSerializer.
    Принимает - данные формата int.
    Отдает - сериализованные в TagSerializer, Tags.
    """

    def to_internal_value(self, data):
        return data


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Промежуточный сериализатор, для сериализатора RecipeSerializer.
    Принимает - Dict["id":int, "amount":int].
    Отдает - сериализованные объекты IngredientAmount.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=IngredientUnit.objects.all(),
        source="ingredient_unit",
    )
    name = serializers.CharField(source="ingredient_unit.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient_unit.measurement_unit", read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор объектов Recipe, для RecipesViewSet."""
    tags = CustomTagsField(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients:
            ingredient_unit = ingredient_data.get("ingredient_unit")
            amount = ingredient_data.get("amount")
            IngredientAmount.objects.get_or_create(
                recipe=recipe, ingredient_unit=ingredient_unit, amount=amount
            )
        recipe.tags.add(*tags)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get("cooking_time", instance.cooking_time)
        ingredients = validated_data.get("ingredients")
        for ingredient_data in ingredients:
            ingredient_unit = ingredient_data.get("ingredient_unit")
            amount = ingredient_data.get("amount")
            IngredientAmount.objects.get_or_create(
                recipe=instance, ingredient_unit=ingredient_unit, amount=amount
            )
        tags = validated_data.get("tags")
        instance.tags.set(tags)
        instance.save()
        return instance
