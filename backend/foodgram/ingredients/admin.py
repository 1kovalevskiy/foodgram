from django.conf import settings
from django.contrib import admin

from ingredients.models import Ingredient


class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(SiteAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    empty_value_display = settings.EMPTY_VALUE
