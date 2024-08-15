from django_filters.fields import IsoDateTimeRangeField
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from vehicle.models import Vehicle


class ReservationRangeFilter(filters.Filter):
    field_class = IsoDateTimeRangeField

    def filter(self, qs, value):
        if value and value.start is not None and value.stop is not None:
            qs = qs.unreserved(starts_at=value.start, ends_at=value.stop)
        return qs


class VehicleFilterSet(FilterSet):
    dt = ReservationRangeFilter()

    class Meta:
        model = Vehicle
        fields = (
            "type",
            "transmission_type",
            "fuel_type",
            "passengers",
            "fuel_type",
            "country_id",
            "city_id",
            "dt",
        )
