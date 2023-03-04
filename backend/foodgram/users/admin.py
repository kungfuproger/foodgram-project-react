from django.contrib import admin

from .models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "password",
    )
    search_fields = (
        "email",
        "username",
    )


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("me", "my_subscribe")


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
