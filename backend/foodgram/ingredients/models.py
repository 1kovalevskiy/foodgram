from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]
