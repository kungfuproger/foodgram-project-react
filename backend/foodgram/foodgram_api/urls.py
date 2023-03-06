from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import IngredientsViewSet, RecipesViewSet, TagsViewSet

router = DefaultRouter()
router.register("ingredients", IngredientsViewSet)
router.register("tags", TagsViewSet)
router.register("recipes", RecipesViewSet, basename="recipes")

urlpatterns = [
    path("", include(router.urls)),
]
