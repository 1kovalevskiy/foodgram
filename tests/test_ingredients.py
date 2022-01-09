import pytest
from rest_framework.reverse import reverse
from http import HTTPStatus


@pytest.fixture
def ingredients_list():
    return reverse("ingredients:ingredients-list")


def list_of_ingredients():
    return [
        {"id": 1, "name": "ingredient_1", "measurement_unit": "г"},
        {"id": 2, "name": "ingredient_2", "measurement_unit": "л"},
        {"id": 3, "name": "ingredient_3", "measurement_unit": "по вкусу"},
    ]


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', (HTTPStatus.OK, 3, list_of_ingredients())),
    ('invalid_token_client', (HTTPStatus.UNAUTHORIZED,)),
    ('auth_client_1', (HTTPStatus.OK, 3, list_of_ingredients())),
])
def test_ingredients(clients, expected, ingredients_list, request):
    client = request.getfixturevalue(clients)
    response = client.get(ingredients_list)
    assert response.status_code == expected[0]
    if len(expected) == 1:
        return
    data = response.json()
    assert len(data) == expected[1]
    assert data == expected[2]


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', (HTTPStatus.OK, list_of_ingredients())),
    ('invalid_token_client', (HTTPStatus.UNAUTHORIZED,)),
    ('auth_client_1', (HTTPStatus.OK, list_of_ingredients())),
])
@pytest.mark.parametrize('ingredient_id', [1, 2, 3])
def test_ingredient(clients, expected, ingredients_list, ingredient_id,
                    request):
    client = request.getfixturevalue(clients)
    response = client.get(ingredients_list + str(ingredient_id) + '/')
    assert response.status_code == expected[0]
    if len(expected) == 1:
        return
    data = response.json()
    assert data == expected[1][ingredient_id-1]


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.NOT_FOUND),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.NOT_FOUND),
])
def test_tag_not_found(clients, expected, ingredients_list, request):
    client = request.getfixturevalue(clients)
    response = client.get(ingredients_list + str(4) + '/')
    assert response.status_code == expected
