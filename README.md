# Сервис Foodgram
![foodgram-project-react](https://github.com/1kovalevskiy/foodgram/actions/workflows/main.yml/badge.svg)
![coverage](https://github.com/1kovalevskiy/foodgram/blob/master/coverage.svg)

Учебный сервис "Foodgram" Продуктовый помощник

«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.

Можно использовать в качестве личногй книги рецептов, а можно использовать в качестве места, где можно поделиться своими рецептами с другимим и узнать чего-то нового.

Можно подписываться на каких-то кокретных авторов, чтобы получать рецепты только от них. Можно добавлять рецепты в избранное, чтобы не забыть попробовать их приготовить, а можно добавлять рецепты в список покупок, где ингредиенты из различных рецептов будут агрегироваться, чтобы получился единый список покупок.

[Дизайн-проект фронта](https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/%D0%9F%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%BE%D0%B2%D1%8B%D0%B9-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D0%BD%D0%B8%D0%BA-(Final)?node-id=0%3A1)

## Deploy
В папке `infra` 
- Создать файл `.env` по примеру файла `.env.sample`
- Запустить `docker-compose up -d`

## Тестовый сервер
[Тестовый сервер](http://foodgram.kovalevskiy.xyz)

## Технологии
- Готовый "фронт" на React
- API на "Django + DRF"
- Тестирование на "Pytest + pytest-django"
- БД PostgreSQL
- Proxy Nginx
- Контейнеризация с помощью Docker

## Техническая информация
Вся структура API представлена в [OpenAPI](https://github.com/1kovalevskiy/foodgram/blob/master/docs/openapi-schema.yml)

## Покрытие тестами
[![](https://github.com/1kovalevskiy/foodgram-project-react/blob/master/pytest.png)](https://github.com/1kovalevskiy/foodgram-project-react/blob/master/pytest.pnghttp://)
