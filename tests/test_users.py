import pytest
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from http import HTTPStatus


User = get_user_model()


@pytest.fixture
def users():
    return reverse("authentication:users-list")


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.OK),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.OK)
])
def test_users_list(clients, expected, users, request):
    client = request.getfixturevalue(clients)
    response = client.get(users)
    assert response.status_code == expected, (
        'проверь систему аутентификации'
    )
    if expected == HTTPStatus.UNAUTHORIZED:
        return
    data = response.json()
    assert data.get('count')
    assert len(data.get('results')) == 3


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.CREATED),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.CREATED)
])
@pytest.mark.django_db
def test_good_registration(clients, expected, users, request):
    user_param = {
        "email": "vpupkin@yandex.ru",
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "Qwerty123"
    }

    client = request.getfixturevalue(clients)
    old_user_count = User.objects.count()
    response = client.post(users, user_param)
    assert response.status_code == expected, (
        'проверь систему аутентификации'
    )
    if expected == HTTPStatus.UNAUTHORIZED:
        return
    new_user_count = User.objects.count()
    assert new_user_count == old_user_count + 1
    new_user = User.objects.all().last()
    assert new_user.email == user_param.get('email')
    assert new_user.username == user_param.get('username')
    assert new_user.first_name == user_param.get('first_name')
    assert new_user.last_name == user_param.get('last_name')
    assert new_user.password != user_param.get('password')


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.BAD_REQUEST),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.BAD_REQUEST)
])
@pytest.mark.django_db
def test_duplicated_registration(clients, expected, users, request):
    user_param = {
        "email": "test1@mail.ru",
        "username": "TestUser1",
        "first_name": "TestUser1",
        "last_name": "TestUser1",
        "password": "TestPassword"
    }

    client = request.getfixturevalue(clients)
    old_user_count = User.objects.count()
    response = client.post(users, user_param)
    assert response.status_code == expected, (
        'проверь систему аутентификации'
    )
    if expected == HTTPStatus.UNAUTHORIZED:
        return
    new_user_count = User.objects.count()
    assert new_user_count == old_user_count


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.BAD_REQUEST),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.BAD_REQUEST)
])
@pytest.mark.parametrize('user_param', [
    {"email": "", "username": "", "first_name": "", "last_name": "",
     "password": ""},
    {"email": "bad_email", "username": "good.username",
     "first_name": "good_name", "last_name": "good_name",
     "password": "Good_password1!"},
    {"email": "good@email.ru", "username": "bad_username&^",
     "first_name": "normal_name", "last_name": "normal_name",
     "password": "Good_password1!"},
    {"email": "good@email.ru", "username": "good.username",
     "first_name": "normal_name", "last_name": "normal_name",
     "password": ""},
    {"email": "good@email.ru", "username": "good.username",
     "first_name": "", "last_name": "normal_name",
     "password": "Good_password1!"},
    {"email": "good@email.ru", "username": "good.username",
     "first_name": "normal_name", "last_name": "",
     "password": "Good_password1!"},
])
@pytest.mark.django_db
def test_bad_registration(clients, expected, users, user_param, request):
    client = request.getfixturevalue(clients)
    old_user_count = User.objects.count()
    response = client.post(users, user_param)
    assert response.status_code == expected
    if expected == HTTPStatus.UNAUTHORIZED:
        return
    new_user_count = User.objects.count()
    assert new_user_count == old_user_count


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.OK),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.OK)
])
@pytest.mark.parametrize('user_param, user_expected', [
    (1, HTTPStatus.OK),
    (2, HTTPStatus.OK),
    (3, HTTPStatus.OK),
    (4, HTTPStatus.NOT_FOUND)
])
def test_user_detail(clients, expected, users, user_param, user_expected,
                     request):
    client = request.getfixturevalue(clients)
    response = client.get(f'{users}{user_param}/')
    assert response.status_code in (expected, user_expected)


@pytest.mark.parametrize('clients, expected', [
    ('unauth_client', HTTPStatus.UNAUTHORIZED),
    ('invalid_token_client', HTTPStatus.UNAUTHORIZED),
    ('auth_client_1', HTTPStatus.NO_CONTENT)
])
def test_change_password(clients, expected, users, request):
    client = request.getfixturevalue(clients)
    response = client.post(
        f'{users}set_password/',
        {
            "new_password": "NewTestPassword",
            "current_password": "TestPassword"
        }
    )
    assert response.status_code == expected
