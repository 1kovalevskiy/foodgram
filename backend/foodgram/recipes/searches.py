import django_filters
from django_filters import rest_framework

from recipes.models import Recipe


class CustomFilter(rest_framework.FilterSet):
    author = rest_framework.CharFilter(
        field_name='author__id'
    )
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = django_filters.BooleanFilter(method='favorite')
    is_in_shopping_cart = django_filters.BooleanFilter(method='shopping')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def favorite(self, queryset, name, value):
        if value is True:
            queryset = queryset.filter(
                favorited_user__user__username=self.request.user
            )
            return queryset
        elif value is False:
            queryset = queryset.exclude(
                favorited_user__user__username=self.request.user
            )
            return queryset
        else:
            return queryset

    def shopping(self, queryset, name, value):
        if value is True:
            queryset = queryset.filter(
                shopped_user__user__username=self.request.user
            )
            return queryset
        elif value is False:
            queryset = queryset.exclude(
                shopped_user__user__username=self.request.user
            )
            return queryset
        else:
            return queryset
