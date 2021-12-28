from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ingredients.models import Ingredients
from ingredients.searches import CustomFilter
from ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter
