from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import RecipeViewSet, download_shopping_cart


app_name = 'recipes'

router = SimpleRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path(r'recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path(r'', include(router.urls)),

]
