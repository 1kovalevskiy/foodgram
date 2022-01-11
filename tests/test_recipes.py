import pytest
from rest_framework.reverse import reverse
from http import HTTPStatus

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeTags
import json

from tags.models import Tag


@pytest.fixture
def new_recipe():
    recipe = {
        "ingredients": [json.dumps({"id": 1, "amount": 10}), ],
        "tags": [1, 2],
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",  # noqa
        "name": "string",
        "text": "string",
        "cooking_time": 1
    }
    return recipe


@pytest.fixture
def recipes():
    return reverse("recipes:recipes-list")


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.OK),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.OK)
])
@pytest.mark.django_db
def test_get_recipes(clients, expected, recipes, request):
    client = request.getfixturevalue(clients)
    response = client.get(recipes)
    assert response.status_code == expected
    if expected == HTTPStatus.UNAUTHORIZED:
        return
    recipe_count = Recipe.objects.count()
    data = response.json()
    assert data.get('count') == recipe_count


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.UNAUTHORIZED),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.CREATED)
])
@pytest.mark.django_db
def test_create_recipe(clients, expected, recipes, new_recipe, request):
    client = request.getfixturevalue(clients)
    response = client.post(recipes, new_recipe, format='json')
    assert response.status_code == expected
    if expected == HTTPStatus.UNAUTHORIZED:
        return
    last_recipe = Recipe.objects.all().last()
    data = response.json()
    assert data.get('name') == last_recipe.name
    tags = Tag.objects.filter(recipe__id=data.get('id')).values_list(
        'id', flat=True)
    for tag in tags:
        assert tag in new_recipe.get('tags')
    ingredients = Ingredient.objects.filter(recipes__id=data.get(
        'id')).values_list('id', flat=True)
    for ingredient in new_recipe.get('ingredients'):
        assert eval(ingredient).get('id') in ingredients


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.UNAUTHORIZED),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.NOT_FOUND)
])
@pytest.mark.django_db
def test_create_recipe_with_unreal_tag(clients, expected, recipes, new_recipe,
                                       request):
    client = request.getfixturevalue(clients)
    new_recipe = new_recipe
    new_recipe['tags'] = [5, 7]
    response = client.post(recipes, new_recipe, format='json')
    assert response.status_code == expected
    if expected == HTTPStatus.UNAUTHORIZED:
        return
