# Generated by Django 3.2.9 on 2022-01-11 15:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ingredients', '0004_auto_20220111_1525'),
        ('tags', '0003_auto_20220111_1525'),
        ('recipes', '0007_auto_20220109_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritedrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_user', to='recipes.recipe', verbose_name='recipe for favorited'),
        ),
        migrations.AlterField(
            model_name='favoritedrecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to=settings.AUTH_USER_MODEL, verbose_name='favorited user of recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='recipe author'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), recipes.models.validate_nonzero], verbose_name='time of cooking'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='the image in recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, verbose_name='recipe name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.RecipeTags', to='tags.Tag', verbose_name='recipe tags'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='main recipe'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), recipes.models.validate_nonzero], verbose_name='amount of ingredient in recipe'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='ingredients.ingredient', verbose_name='ingredient of recipe'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe', verbose_name='recipe of ingredient'),
        ),
        migrations.AlterField(
            model_name='recipetags',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='recipe for tag'),
        ),
        migrations.AlterField(
            model_name='recipetags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag', verbose_name='tag of recipe'),
        ),
        migrations.AlterField(
            model_name='shoppingrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopped_user', to='recipes.recipe', verbose_name='recipe for shopping list of user'),
        ),
        migrations.AlterField(
            model_name='shoppingrecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping', to=settings.AUTH_USER_MODEL, verbose_name='shopping user of recipe'),
        ),
    ]
