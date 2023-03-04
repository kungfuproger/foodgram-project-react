import csv
import io

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.serializers import CustomRecipeSerializer
from .models import Ingredient, Tag, Recipe
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


@api_view(["POST", "DELETE"])
def favorites(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "DELETE":
        request.user.favorites.remove(recipe)
        return Response()
    request.user.favorites.add(recipe)
    return Response(CustomRecipeSerializer(recipe).data, status=201)


@api_view(["GET"])
def download_shopping_cart(request):
    recipes = request.user.in_cart.all()
    ingredient_dict = {}
    for recipe in recipes:
        for ingredient in recipe.ingredients.all():
            ingredient_id = ingredient.ingredient.id
            if ingredient_id in ingredient_dict:
                ingredient_dict[ingredient_id]["amount"] += ingredient.amount
            else:
                ingredient_dict[ingredient_id] = {
                    "name": ingredient.ingredient.name,
                    "measurement_unit": ingredient.ingredient.measurement_unit,
                    "amount": ingredient.amount,
                }
    ingredients = sorted(
        list(ingredient_dict.values()), key=lambda x: x["name"]
    )
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="shopping_cart.csv"'
        },
    )
    writer = csv.writer(response)
    writer.writerow(["Список покупок:"])
    n = int()
    for ingredient in ingredients:
        n += 1
        writer.writerow(
            [
                f"{n}. {ingredient['name'].capitalize()} ({ingredient['measurement_unit']}) - {ingredient['amount']}"
            ]
        )
    return response


@api_view(["POST", "DELETE"])
def in_cart(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "DELETE":
        request.user.in_cart.remove(recipe)
        return Response()
    request.user.in_cart.add(recipe)
    return Response(CustomRecipeSerializer(recipe).data, status=201)
