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
    name = models.CharField(max_length=200, verbose_name='recipe name')
    text = models.TextField(verbose_name='main recipe')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), validate_nonzero],
        verbose_name='time of cooking'
    )
    image = models.ImageField(verbose_name='the image in recipe')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='recipe author'
    )
    tags = models.ManyToManyField(
        Tag, through='RecipeTags', verbose_name='recipe tags'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='publication date'
    )

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"
        ordering = ['-pub_date']

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='recipe for tag'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='tag of recipe'
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
        related_name='ingredients',
        verbose_name='recipe of ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='ingredient of recipe'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1), validate_nonzero],
        verbose_name='amount of ingredient in recipe'
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
        User, on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='favorited user of recipe'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorited_user',
        verbose_name='recipe for favorited'
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
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='shopping user of recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopped_user',
        verbose_name='recipe for shopping list of user'
    )

    class Meta:
        verbose_name = "recipe_in_shopping_list"
        verbose_name_plural = "recipes_in_shopping_list"

    def __str__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'

    def __repr__(self):
        return f'{self.user.username[:15]} -> {self.recipe.name[:15]}'
