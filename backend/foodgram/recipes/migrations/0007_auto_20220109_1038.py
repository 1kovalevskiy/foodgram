# Generated by Django 3.2.9 on 2022-01-09 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipeingredients_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritedrecipe',
            options={'verbose_name': 'favorite_recipe', 'verbose_name_plural': 'favorite_recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'recipe', 'verbose_name_plural': 'recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredients',
            options={'verbose_name': 'ingredient_in_recipe', 'verbose_name_plural': 'ingredients_in_recipe'},
        ),
        migrations.AlterModelOptions(
            name='recipetags',
            options={'verbose_name': 'tag_in_recipe', 'verbose_name_plural': 'tags_in_recipe'},
        ),
        migrations.AlterModelOptions(
            name='shoppingrecipe',
            options={'verbose_name': 'recipe_in_shopping_list', 'verbose_name_plural': 'recipes_in_shopping_list'},
        ),
    ]
