from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import RecipeViewSet


app_name = 'recipes'

router = SimpleRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path(r'', include(router.urls)),
]
