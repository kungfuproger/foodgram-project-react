from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import download_shopping_cart, favorites, in_cart
from .viewsets import IngredientsViewSet, RecipesViewSet, TagsViewSet

router = DefaultRouter()
router.register("ingredients", IngredientsViewSet)
router.register("tags", TagsViewSet)
router.register("recipes", RecipesViewSet, basename="recipes")

urlpatterns = [
    path("recipes/<int:id>/favorite/", favorites),
    path("recipes/download_shopping_cart/", download_shopping_cart),
    path("recipes/<int:id>/shopping_cart/", in_cart),
    path("", include(router.urls)),
]
