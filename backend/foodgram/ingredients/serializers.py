from rest_framework import serializers

from ingredients.models import Ingredients


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = '__all__'