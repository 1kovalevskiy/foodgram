import pytest

from tags.models import Tag
from ingredients.models import Ingredient


@pytest.fixture
def tag_breakfast():
    return Tag.objects.create(
        name='Breakfast', color='#FFFFFF', slug='breakfast'
    )


@pytest.fixture
def tag_dinner():
    return Tag.objects.create(
        name='Dinner', color='#AAAAAA', slug='dinner'
    )


@pytest.fixture
def tag_supper():
    return Tag.objects.create(
        name='Supper', color='#000000', slug='supper'
    )


@pytest.fixture
def ingredient_1():
    return Ingredient.objects.create(
        name='ingredient_1', measurement_unit='г'
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='ingredient_2', measurement_unit='л'
    )


@pytest.fixture
def ingredient_3():
    return Ingredient.objects.create(
        name='ingredient_3', measurement_unit='по вкусу'
    )
