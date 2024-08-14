from core.sites import rentie_site
from django.contrib import admin

from .models import City
from .models import Country


class CityTabularInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(Country, site=rentie_site)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "code_display", "currency")
    ordering = ("code",)
    inlines = (CityTabularInline,)

    @admin.display(description="Code", ordering="code")
    def code_display(self, obj: Country):
        return obj.code.code
