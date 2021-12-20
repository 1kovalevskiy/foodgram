from django.conf import settings
from django.contrib import admin

from tags.models import Tag

class SiteAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class UserAdmin(SiteAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = settings.EMPTY_VALUE
