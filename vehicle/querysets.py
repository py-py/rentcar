from django.db import models


class VehicleQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_removed=False)

    def removed(self):
        return self.filter(is_removed=True)

    def reserved(self, starts_at, ends_at):
        return self.filter(
            reservations__is_cancelled=False,
            reservations__ends_at__gte=starts_at,
            reservations__starts_at__lte=ends_at,
        )

    def unreserved(self, starts_at, ends_at):
        return self.exclude(id__in=self.reserved(starts_at, ends_at))
