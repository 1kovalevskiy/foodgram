# Generated by Django 3.2.9 on 2021-12-28 04:44

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18, samples=None)),
                ('slug', models.SlugField(max_length=200)),
            ],
        ),
    ]
