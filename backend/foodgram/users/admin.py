from django.conf import settings
from django.contrib import admin

from .models import User


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

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form