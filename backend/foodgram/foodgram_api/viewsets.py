from rest_framework import permissions, viewsets

from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление ингредиентов.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление тегов.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Представление рецептов.
    """

    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Recipe.objects.all()

        # Фильтрация по тегам
        tags = self.request.query_params.getlist("tags")
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        if self.request.user.is_authenticated:
            # Фильтрация по автору
            author_id = self.request.query_params.get("author")
            if author_id:
                queryset = queryset.filter(author=author_id)

            # Фильтрация по наличию в списке избранного
            is_favorited = self.request.query_params.get("is_favorited")
            if is_favorited:
                queryset = queryset.filter(favorited_users=self.request.user)

            # Фильтрация по наличию в списке покупок
            is_in_shopping_cart = self.request.query_params.get(
                "is_in_shopping_cart"
            )
            if is_in_shopping_cart:
                queryset = queryset.filter(carted_users=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
