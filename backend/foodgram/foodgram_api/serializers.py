import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Ingredient, IngredientAmount, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор объектов Tag, для TagsViewSet.
    """

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор объектов Ingredient, для IngredientsViewSet.
    """

    class Meta:
        model = Ingredient
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
        queryset=Ingredient.objects.all(),
        source="ingredient",
    )
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор объектов Recipe, для RecipesViewSet.
    """

    tags = CustomTagsField(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
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

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj in user.favorites.all()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj in user.in_cart.all()

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        all_ingredients = []
        for ingredient_data in ingredients:
            ingredient = ingredient_data.get("ingredient")
            amount = ingredient_data.get("amount")
            ingredient_new, _ = IngredientAmount.objects.get_or_create(
                ingredient=ingredient, amount=amount
            )
            all_ingredients.append(ingredient_new)
        recipe.ingredients.add(*all_ingredients)
        recipe.tags.add(*tags)
        return recipe

    def update(self, instance, validated_data):
        instance.delete()
        return self.create(validated_data)
