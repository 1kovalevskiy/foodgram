from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField()
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name[:15]

    def __repr__(self):
        return self.name[:15]
