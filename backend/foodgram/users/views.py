from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import UserRecipeListSerializer
from .models import User, Subscribe


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = UserRecipeListSerializer

    @action(detail=False)
    def subscriptions(self, request):
        subscribes = request.user.my_subscribes.all()  # добавить Prefect_related
        serializer = self.get_serializer(
            [sub.my_subscribe for sub in subscribes], many=True
        )
        return Response(serializer.data)

    @action(methods=["post", "delete"], detail=True)
    def subscribe(self, request, id):
        target = User.objects.get(id=id)
        if request.method == "DELETE":
            get_object_or_404(
                Subscribe, me=request.user, my_subscribe=target
            ).delete()
            return Response(status=204)
        Subscribe.objects.get_or_create(me=request.user, my_subscribe=target)
        serializer = self.get_serializer(target)
        return Response(serializer.data)


# @login_required
# def profile_follow(request, username):
#     user = request.user
#     author = User.objects.get(username=username)
#     if user != author:
#         Follow.objects.get_or_create(
#             user=user,
#             author=author
#         )
#     return redirect('posts:follow_index')
