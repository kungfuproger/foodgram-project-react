import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import CustomRecipeSerializer
from .models import Recipe


def add_or_remove_ralation(request, id, relation):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "DELETE":
        getattr(request.user, relation).remove(recipe)
        return Response()
    getattr(request.user, relation).add(recipe)
    return Response(CustomRecipeSerializer(recipe).data, status=201)


@api_view(["POST", "DELETE"])
def favorites(request, id):
    """Добавить или удалить в избранное."""
    return add_or_remove_ralation(request, id, "favorites")


@api_view(["POST", "DELETE"])
def in_cart(request, id):
    """Добавить или удалить в корзину."""
    return add_or_remove_ralation(request, id, "in_cart")


@api_view(["GET"])
def download_shopping_cart(request):
    """Скачать список ингредиентов."""
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
        content_type="text/plain",
        headers={
            "Content-Disposition": 'attachment; filename="shopping_cart.txt"'
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
