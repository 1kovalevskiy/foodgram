from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer, PasswordSerializer

User = get_user_model()


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer



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


