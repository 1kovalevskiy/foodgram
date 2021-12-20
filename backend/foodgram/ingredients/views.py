from rest_framework import viewsets

from ingredients.models import Ingredients
from ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
