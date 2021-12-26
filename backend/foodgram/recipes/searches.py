from django_filters import rest_framework

from recipes.models import Recipe


class CustomFilter(rest_framework.FilterSet):
    author = rest_framework.CharFilter(
        field_name='author__username'
    )
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
