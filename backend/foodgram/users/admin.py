from django.contrib import admin

from .models import User, UserSubscription


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
    list_filter = (
        "email",
        "username",
    )


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "publisher")


admin.site.register(User, UserAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
