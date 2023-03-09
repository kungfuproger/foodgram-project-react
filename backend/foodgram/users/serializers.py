from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram_api.models import Recipe
from .models import User, UserSubscription


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""
    id = serializers.IntegerField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return UserSubscription.objects.filter(
            subscriber=user, publisher=obj
        ).exists()


class CustomRecipeSerializer(serializers.ModelSerializer):
    """
    Кастомный сериализатор.
    Краткое представление рецептов.
    """

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class UserRecipesSerializer(CustomUserSerializer):
    """
    Сериализатор для системы подписок.
    Возвращает пользователя и кратко его рецепты.
    """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return UserSubscription.objects.filter(
            subscriber=user, publisher=obj
        ).exists()

    def get_recipes(self, obj):
        recipes_limit = self.context.get("recipes_limit")
        if recipes_limit:
            recipes = obj.recipes.all()[:recipes_limit]
        else:
            recipes = obj.recipes.all()
        return CustomRecipeSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
