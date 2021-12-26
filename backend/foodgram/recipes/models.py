from django.contrib.auth import get_user_model
from django.db import models

from tags.models import Tag
from ingredients.models import Ingredients


User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField()
    image = models.ImageField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag, through='RecipeTags'
    )
    # ingredients = models.ManyToManyField(
    #     Ingredients, through='RecipeIngredients'
    # )

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.recipe.name[:15]} -> {self.tag.name[:15]}'

    def __repr__(self):
        return f'{self.recipe.name[:15]} -> {self.tag.name[:15]}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipe.name[:15]} -> {self.ingredient.name[:15]}'

    def __repr__(self):
        return f'{self.recipe.name[:15]} -> {self.ingredient.name[:15]}'


class FavoritedRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorided_user'
    )

    def __str__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'

    def __repr__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'


class ShoppingRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopped_user'
    )

    def __str__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'

    def __repr__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'
