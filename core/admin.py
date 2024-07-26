from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.core.exceptions import ValidationError

from .models import User
from .sites import rentie_site


class UserChangeForm(DjangoUserChangeForm):
    def clean_groups(self):
        if self.cleaned_data["groups"].count() > 1:
            self.add_error("groups", ValidationError("Only one group allowed."))
            return None
        return self.cleaned_data["groups"]


@admin.register(User, site=rentie_site)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
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
