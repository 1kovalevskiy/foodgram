from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag
from ingredients.models import Ingredient


User = get_user_model()


def validate_nonzero(value):
    if value == 0:
        raise ValidationError(
            f'Quantity {value}s is not allowed',
            params={'value': value},
        )


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), validate_nonzero]
    )
    image = models.ImageField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag, through='RecipeTags'
    )

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

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

    class Meta:
        verbose_name = "tag_in_recipe"
        verbose_name_plural = "tags_in_recipe"

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
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1), validate_nonzero]
    )

    class Meta:
        verbose_name = "ingredient_in_recipe"
        verbose_name_plural = "ingredients_in_recipe"

    def __str__(self):
        return f'{self.recipe.name[:15]} -> {self.ingredient.name[:15]}'

    def __repr__(self):
        return f'{self.recipe.name[:15]} -> {self.ingredient.name[:15]}'


class FavoritedRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorited_user'
    )

    class Meta:
        verbose_name = "favorite_recipe"
        verbose_name_plural = "favorite_recipes"

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

    class Meta:
        verbose_name = "recipe_in_shopping_list"
        verbose_name_plural = "recipes_in_shopping_list"

    def __str__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'

    def __repr__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'
