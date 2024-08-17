from django.db import models
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel

from .constants import CURRENCIES
from .constants import CURRENCY_EUR


class Country(TimeStampedModel):
    code = CountryField(max_length=2, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CURRENCY_EUR)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.code.name


class City(TimeStampedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name} ({self.country.code.code})"
