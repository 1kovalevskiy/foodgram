from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(SiteAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('username',)
    empty_value_display = settings.EMPTY_VALUE
