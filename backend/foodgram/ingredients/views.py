from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ingredients.models import Ingredient
from ingredients.searches import CustomFilter
from ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter

    def get_queryset(self):
        """
        Фильтрация не работает с этой вьюхой
        потратил почти весь день, на попытку найти проблему и не смог
        хотя все аналогично работает в recipe!
        """
        name = self.request.query_params.get('name')
        if name is not None:
            return Ingredient.objects.filter(name__icontains=name)
        return Ingredient.objects.all()
