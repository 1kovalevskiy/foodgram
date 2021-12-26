from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from foodgram.paginations import DefaultResultsSetPagination
from recipes.models import Recipe, RecipeTags, RecipeIngredients, \
    FavoritedRecipe
from recipes.searches import CustomFilter
from recipes.serializers import RecipeSerializer


User = get_user_model()

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = DefaultResultsSetPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filterset_class = CustomFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        old_tags = RecipeTags.objects.filter(recipe=instance)
        old_ingredients = RecipeIngredients.objects.filter(recipe=instance)
        old_tags.delete()
        old_ingredients.delete()
        instance.delete()

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=401)
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if FavoritedRecipe.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Already subscribed'}, status=400)
            pass
        elif request.method == 'DELETE':
            pass
        return Response(status=401)
