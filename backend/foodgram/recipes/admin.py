from django.conf import settings
from django.contrib import admin

from recipes.models import Recipe, RecipeTags, RecipeIngredients


class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(SiteAdmin):
    list_display = (
        'pk',
        'name',
        'text',
        'cooking_time',
        'image',
        'author',
    )
    search_fields = ('name',)
    empty_value_display = settings.EMPTY_VALUE


@admin.register(RecipeTags)
class RecipeTagAdmin(SiteAdmin):
    list_display = (
        'pk',
        'recipe',
        'tag'
    )
    search_fields = ('recipe', 'tag')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(RecipeIngredients)
class RecipeIngredientAdmin(SiteAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = ('recipe', 'tag')
    empty_value_display = settings.EMPTY_VALUE
