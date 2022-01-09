# Generated by Django 3.2.9 on 2021-12-31 05:00

import django.core.validators
from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), recipes.models.validate_nonzero]),
        ),
    ]
