from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User
from .sites import rentie_site


@admin.register(User, site=rentie_site)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": ("groups",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
                "classes": ("wide",),
            },
        ),
    )
