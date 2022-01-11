from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='ingredient name')
    measurement_unit = models.CharField(
        max_length=20, verbose_name='measurement unit of ingredient'
    )

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]
