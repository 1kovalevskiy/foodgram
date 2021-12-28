from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe, RecipeTags, RecipeIngredients, \
    FavoritedRecipe, ShoppingRecipe
from tags.models import Tag
from ingredients.models import Ingredients
from users.serializers import UserSerializer


class RecipeTagSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    color = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = RecipeTags
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = RecipeTagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'ingredients',
            'name',
            'text',
            'cooking_time',
            'image',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        try:
            user = request.user
        except AttributeError:
            return False
        if isinstance(user, AnonymousUser):
            return False
        elif FavoritedRecipe.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        try:
            user = request.user
        except AttributeError:
            return False
        if isinstance(user, AnonymousUser):
            return False
        elif ShoppingRecipe.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def create(self, validated_data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            tag = get_object_or_404(Tag, id=tag)
            RecipeTags.objects.create(recipe=recipe, tag=tag)
        for ingredient in ingredients:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_id = get_object_or_404(Ingredients, id=id)
            RecipeIngredients.objects.create(
                recipe=recipe, ingredient=ingredient_id, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        old_tags = RecipeTags.objects.filter(recipe=instance)
        old_ingredients = RecipeIngredients.objects.filter(recipe=instance)
        old_tags.delete()
        old_ingredients.delete()
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        for tag in tags:
            tag = get_object_or_404(Tag, id=tag)
            RecipeTags.objects.create(recipe=instance, tag=tag)
        for ingredient in ingredients:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_id = get_object_or_404(Ingredients, id=id)
            RecipeIngredients.objects.create(
                recipe=instance, ingredient=ingredient_id, amount=amount
            )
        return instance
