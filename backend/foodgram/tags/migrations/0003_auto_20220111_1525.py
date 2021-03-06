# Generated by Django 3.2.9 on 2022-01-11 15:25

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_alter_tag_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', max_length=18, samples=None, verbose_name='tag color'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='tag name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, verbose_name='tag slug'),
        ),
    ]
