import pytest
from rest_framework.reverse import reverse
from http import HTTPStatus


@pytest.fixture
def tags_list():
    return reverse("tags:tags-list")


def list_of_tag():
    return [
        {"id": 1, "name": "Breakfast", "color": "#FFFFFF", "slug": "breakfast"},
        {"id": 2, "name": "Dinner", "color": "#AAAAAA", "slug": "dinner"},
        {"id": 3, "name": "Supper", "color": "#000000", "slug": "supper"}
    ]


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', (HTTPStatus.OK, 3, list_of_tag())),
    ('invalid_token_client', (HTTPStatus.UNAUTHORIZED,)),
    ('auth_client_1', (HTTPStatus.OK, 3, list_of_tag())),
])
def test_tags(clients, expected, tags_list, request):
    client = request.getfixturevalue(clients)
    response = client.get(tags_list)
    assert response.status_code == expected[0]
    if len(expected) == 1:
        return
    data = response.json()
    assert len(data) == expected[1]
    assert data == expected[2]


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', (HTTPStatus.OK, list_of_tag())),
    ('invalid_token_client', (HTTPStatus.UNAUTHORIZED,)),
    ('auth_client_1', (HTTPStatus.OK, list_of_tag())),
])
@pytest.mark.parametrize('tag_id', [1, 2, 3])
def test_tag(clients, expected, tags_list, tag_id, request):
    client = request.getfixturevalue(clients)
    response = client.get(tags_list + str(tag_id) + '/')
    assert response.status_code == expected[0]
    if len(expected) == 1:
        return
    data = response.json()
    assert data == expected[1][tag_id-1]


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.NOT_FOUND),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.NOT_FOUND),
])
def test_tag_not_found(clients, expected, tags_list, request):
    client = request.getfixturevalue(clients)
    response = client.get(tags_list + str(4) + '/')
    assert response.status_code == expected
