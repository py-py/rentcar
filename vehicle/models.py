from datetime import date

from django.db import models
from django_extensions.db.models import TimeStampedModel

from .constants import FUEL_GAS
from .constants import FUEL_TYPES
from .constants import PASSENGERS_4
from .constants import PASSENGERS_TYPES
from .constants import TRANSMISSION_AUTO
from .constants import TRANSMISSION_TYPES
from .constants import TYPE_SEDAN
from .constants import TYPES

# Create your models here.


class Vehicle(TimeStampedModel):
    investor = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    brand = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    year_of_production = models.DateField(default=date(2020, 1, 1))
    car_mileage = models.PositiveIntegerField(default=1000)
    type = models.CharField(
        max_length=32,
        choices=TYPES,
        default=TYPE_SEDAN,
    )
    transmission_type = models.CharField(
        max_length=8,
        choices=TRANSMISSION_TYPES,
        default=TRANSMISSION_AUTO,
    )
    fuel_type = models.CharField(
        max_length=8,
        choices=FUEL_TYPES,
        default=FUEL_GAS,
    )
    passengers = models.PositiveSmallIntegerField(
        choices=PASSENGERS_TYPES,
        default=PASSENGERS_4,
    )
    investor_daily_price = models.PositiveSmallIntegerField()
    manager_daily_price = models.PositiveSmallIntegerField()
    post_service_duration = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
