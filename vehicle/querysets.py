from django.db import models


class VehicleQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_removed=False)

    def removed(self):
        return self.filter(is_removed=True)
