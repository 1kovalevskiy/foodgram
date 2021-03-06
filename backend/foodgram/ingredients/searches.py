import django_filters
from django_filters import rest_framework as filters

from ingredients.models import Ingredient


class CustomFilter(filters.FilterSet):
    name = django_filters.BooleanFilter(method='namefilter')

    def namefilter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

    class Meta:
        model = Ingredient
        fields = ('name', )
