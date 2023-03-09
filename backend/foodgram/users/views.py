from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import User, UserSubscription
from .serializers import UserRecipesSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    """Представление системы подписки."""
    queryset = UserSubscription.objects.all()
    serializer_class = UserRecipesSerializer

    @action(detail=False)
    def subscriptions(self, request):
        paginator = PageNumberPagination()
        publishers = User.objects.filter(subscribers__subscriber=request.user)
        paginated_publishers = paginator.paginate_queryset(publishers, request)
        recipes_limit = int(request.query_params.get("recipes_limit"))
        serializer = self.get_serializer(
            paginated_publishers,
            many=True,
            context={
                "request": request,
                "recipes_limit": recipes_limit,
            },
        )
        return paginator.get_paginated_response(serializer.data)

    @action(methods=["post", "delete"], detail=True)
    def subscribe(self, request, id):
        target = User.objects.get(id=id)
        if request.method == "DELETE":
            get_object_or_404(
                UserSubscription, subscriber=request.user, publisher=target
            ).delete()
            return Response(status=204)
        try:
            UserSubscription.objects.get_or_create(
                subscriber=request.user, publisher=target
            )
        except IntegrityError as e:
            raise ValidationError(e.args[0][25:])
        serializer = self.get_serializer(target)
        return Response(serializer.data)
