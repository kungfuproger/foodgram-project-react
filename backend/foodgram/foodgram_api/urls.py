from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IngredientsViewSet,
    TagsViewSet,
    RecipesViewSet,
    favorites,
    download_shopping_cart,
    in_cart,
)

router = DefaultRouter()
router.register("ingredients", IngredientsViewSet)
router.register("tags", TagsViewSet)
router.register("recipes", RecipesViewSet)

urlpatterns = [
    path("recipes/<int:id>/favorite/", favorites),
    path("recipes/download_shopping_cart/", download_shopping_cart),
    path("recipes/<int:id>/shopping_cart/", in_cart),
    path("", include(router.urls)),
]
