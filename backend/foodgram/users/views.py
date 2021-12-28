from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow
from users.serializers import UserSerializer, PasswordSerializer, \
    SubscribeSerializer

User = get_user_model()


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=401)
        user = get_object_or_404(User, username=request.user)
        author = get_object_or_404(User, pk=pk)
        if request.method == 'GET':
            if Follow.objects.filter(user=user, author=author).exists():
                return Response({'errors': 'Already subscribed'}, status=400)
            elif user == author:
                return Response(
                    {'errors': "You can't subscribe to yourself"}, status=400)
            follow = Follow.objects.create(user=user, author=author)
            context = {
                'recipes_limit': request.query_params.get('recipes_limit')}
            response = SubscribeSerializer(follow, context=context)
            return Response(response.data)
        elif request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, author=author)
            if not follow.exists():
                return Response(
                    {'errors': "You are not subscribed"}, status=400)
            follow.delete()
            return Response(status=204)
        return Response(status=400)


@api_view(['GET'])
def me_view(request):
    if request.user.is_anonymous:
        return Response(status=401)
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def set_password(request):
    if request.user.is_anonymous:
        return Response(status=401)
    serializer = PasswordSerializer(data=request.data)
    if serializer.is_valid():
        current_password = serializer.data.get("current_password")
        if not request.user.check_password(current_password):
            return Response({"current_password": ["Wrong password."]},
                            status=400)
        request.user.set_password(serializer.data.get("new_password"))
        request.user.save()
        return Response(status=204)

    return Response(status=400)


class SubscriptionsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        queryset = Follow.objects.filter(user=user)
        return queryset
