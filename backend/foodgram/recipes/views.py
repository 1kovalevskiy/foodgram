import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from foodgram.paginations import DefaultResultsSetPagination
from recipes.models import (Recipe, RecipeTags, RecipeIngredients,
                            FavoritedRecipe, ShoppingRecipe)
from recipes.searches import CustomFilter
from recipes.serializers import RecipeSerializer
from users.serializers import RecipesMiniSerializer


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
    def favorite(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=401)
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if FavoritedRecipe.objects.filter(
                    user=user, recipe=recipe
            ).exists():
                return Response({'errors': 'Already favorite'}, status=400)
            favorite = FavoritedRecipe.objects.create(user=user, recipe=recipe)
            response = RecipesMiniSerializer(favorite.recipe)
            return Response(response.data, status=201)
        elif request.method == 'DELETE':
            favorite = FavoritedRecipe.objects.filter(user=user, recipe=recipe)
            if not favorite.exists():
                return Response(
                    {'errors': "You are not favorite"}, status=400)
            favorite.delete()
            return Response(status=204)
        return Response(status=401)

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=401)
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            if ShoppingRecipe.objects.filter(user=user,
                                             recipe=recipe).exists():
                return Response(
                    {'errors': 'Already in shopping cart'}, status=400)
            shopping = ShoppingRecipe.objects.create(user=user, recipe=recipe)
            response = RecipesMiniSerializer(shopping.recipe)
            return Response(response.data, status=201)
        elif request.method == 'DELETE':
            shopping = ShoppingRecipe.objects.filter(user=user, recipe=recipe)
            if not shopping.exists():
                return Response(
                    {'errors': "You are not shopping"}, status=400)
            shopping.delete()
            return Response(status=204)
        return Response(status=401)


@api_view(['GET'])
def download_shopping_cart(request):
    if request.user.is_anonymous:
        return Response(status=401)
    user = get_object_or_404(User, username=request.user)
    ingredients = RecipeIngredients.objects.filter(
        recipe__shopped_user__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount')).values_list(
        'ingredient__name', 'ingredient_amount', 'ingredient__measurement_unit'
    )
    # https://docs.djangoproject.com/en/4.0/howto/outputting-csv/
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename="'
                                   f'{request.user.username}.csv"'},
    )
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for product in list(ingredients):
        writer.writerow(product)
    return response
