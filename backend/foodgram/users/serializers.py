from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram_api.models import Recipe
from .models import User, Subscribe


class CustomUserCreateSerializer(UserCreateSerializer):
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
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("email", "id", "username", "first_name", "last_name")


class CustomRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class UserRecipeListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = CustomRecipeSerializer(read_only=True, many=True)
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
        user = self.context['request'].user
        return Subscribe.objects.filter(me=user, my_subscribe=obj).exists()
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()