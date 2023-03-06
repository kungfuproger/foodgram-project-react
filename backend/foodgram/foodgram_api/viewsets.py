import csv

from django.db.models import BooleanField, Exists, OuterRef, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import CustomRecipeSerializer
from .models import Favorite, IngredientUnit, Recipe, Shopping_cart, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (
    IngredientUnitSerializer,
    RecipeSerializer,
    TagSerializer,
)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление ингредиентов."""
    queryset = IngredientUnit.objects.all()
    serializer_class = IngredientUnitSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Представление рецептов."""
    lookup_field = "id"
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            queryset = Recipe.objects.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField()),
            ).all()
        else:
            queryset = Recipe.objects.annotate(
                is_favorited=Exists(
                    self.request.user.favorites.filter(recipe=OuterRef("pk"))
                ),
                is_in_shopping_cart=Exists(
                    self.request.user.carts.filter(recipe=OuterRef("pk"))
                ),
            ).all()
            author_id = self.request.query_params.get("author")
            if author_id:
                queryset = queryset.filter(author=author_id)
            is_favorited = self.request.query_params.get("is_favorited")
            if is_favorited:
                queryset = queryset.filter(is_favorited=True)
            is_in_shopping_cart = self.request.query_params.get(
                "is_in_shopping_cart"
            )
            if is_in_shopping_cart:
                queryset = queryset.filter(is_in_shopping_cart=True)
        tags = self.request.query_params.getlist("tags")
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def add_or_remove_ralation(self, request, id, relation_model):
        recipe = get_object_or_404(Recipe, id=id)
        obj, _ = relation_model.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if request._request.method == "DELETE":
            obj.delete()
            return Response()
        return Response(CustomRecipeSerializer(recipe).data, status=201)

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, id):
        """Добавить или удалить в избранное."""
        return self.add_or_remove_ralation(request, id, Favorite)

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, id):
        """Добавить или удалить в корзину."""
        return self.add_or_remove_ralation(request, id, Shopping_cart)

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Скачать список ингредиентов."""
        carts = request.user.carts.all()
        ingredient_dict = {}
        for cart in carts:
            recipe = cart.recipe
            for ingredient in recipe.ingredients.all():
                ingredient_id = ingredient.ingredient_unit.id
                if ingredient_id in ingredient_dict:
                    ingredient_dict[ingredient_id][
                        "amount"
                    ] += ingredient.amount
                else:
                    ingredient_dict[ingredient_id] = {
                        "name": ingredient.ingredient_unit.name,
                        "measurement_unit": ingredient.ingredient_unit.measurement_unit,
                        "amount": ingredient.amount,
                    }
        ingredients = sorted(
            list(ingredient_dict.values()), key=lambda x: x["name"]
        )
        response = HttpResponse(
            content_type="text/plain",
            headers={
                "Content-Disposition": "attachment; filename='shopping_cart.txt'"
            },
        )
        writer = csv.writer(response)
        writer.writerow(["Список покупок:"])
        n = int()
        for ingredient in ingredients:
            n += 1
            name = ingredient["name"].capitalize()
            measurement_unit = ingredient["measurement_unit"]
            amount = ingredient["amount"]
            writer.writerow([f"{n}. {name} ({measurement_unit}) - {amount}"])
        return response
