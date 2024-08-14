import uuid
from datetime import date

from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.dj.models import ImageField

from .constants import FUEL_GAS
from .constants import FUEL_TYPES
from .constants import PASSENGERS_4
from .constants import PASSENGERS_TYPES
from .constants import TRANSMISSION_AUTO
from .constants import TRANSMISSION_TYPES
from .constants import TYPE_SEDAN
from .constants import TYPES
from .querysets import VehicleQuerySet


class Vehicle(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    investor = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    manager = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_vehicles",
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
    is_removed = models.BooleanField(default=False)

    country = models.ForeignKey(
        "geo.Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        "geo.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = models.Manager.from_queryset(VehicleQuerySet)()

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"


class VehicleImage(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vehicle = models.ForeignKey(
        "vehicle.Vehicle",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = ImageField()

    def delete(self, *args, **kwargs):
        client = get_uploadcare_client()
        client.delete_files(files=[self.image])
        super().delete(*args, **kwargs)


class VehicleOrder(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vehicle = models.ForeignKey(
        "vehicle.Vehicle",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    starts_at = models.DateTimeField()
    finishes_at = models.DateTimeField()

    client_name = models.CharField(max_length=256)
    client_phone = PhoneNumberField()
