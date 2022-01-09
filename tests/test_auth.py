import pytest
from rest_framework.reverse import reverse
from http import HTTPStatus


@pytest.fixture
def me():
    return reverse("authentication:my_profile")


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.UNAUTHORIZED),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
])
def test_invalid_token(clients, expected, me, request):
    client = request.getfixturevalue(clients)
    response = client.get(me)
    assert response.status_code == expected, 'проверь аутентификацию'


@pytest.mark.parametrize('clients, expected', [
    ('auth_client_1', (HTTPStatus.OK, 'TestUser1')),
    ('auth_client_2', (HTTPStatus.OK, 'TestUser2')),
    ('auth_client_3', (HTTPStatus.OK, 'TestUser3')),
])
def test_good_auth(clients, expected, me, request):
    client = request.getfixturevalue(clients)
    response = client.get(me)
    assert response.status_code == expected[0], (
        'проверь систему аутентификации'
    )
    data = response.json()
    assert data.get('username') == expected[1], (
        'проверь правильность сервиса информации о текущем пользователе'
    )
