from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='tag name')
    color = ColorField(verbose_name='tag color')
    slug = models.SlugField(max_length=200, verbose_name='tag slug')

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]
