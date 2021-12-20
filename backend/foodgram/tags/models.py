from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField()
    # color = models.CharField(
    #     verbose_name=('Color'),
    #     max_length=7,
    #     help_text=('HEX color, as #RRGGBB')
    # )
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]