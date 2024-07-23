from django.db import models
from django_extensions.db.models import TimeStampedModel

from .constants import GEARSHIFT_TYPE_AUTO
from .constants import GEARSHIFT_TYPES
from .constants import PASSENGERS_4
from .constants import PASSENGERS_TYPES
from .constants import VEHICLE_TYPE_SEDAN
from .constants import VEHICLE_TYPES

# Create your models here.


class Vehicle(TimeStampedModel):
    user = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    type = models.CharField(
        max_length=32,
        choices=VEHICLE_TYPES,
        default=VEHICLE_TYPE_SEDAN,
    )
    gearshift = models.CharField(
        max_length=8,
        choices=GEARSHIFT_TYPES,
        default=GEARSHIFT_TYPE_AUTO,
    )
    passengers = models.PositiveSmallIntegerField(
        choices=PASSENGERS_TYPES,
        default=PASSENGERS_4,
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
