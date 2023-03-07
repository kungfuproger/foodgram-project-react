from django.urls import include, path

from .views import SubscribeViewSet

urlpatterns = [
    path(
        "users/subscriptions/",
        SubscribeViewSet.as_view({"get": "subscriptions", }),
    ),
    path(
        "users/<int:id>/subscribe/",
        SubscribeViewSet.as_view({"post": "subscribe", "delete": "subscribe"}),
    ),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
