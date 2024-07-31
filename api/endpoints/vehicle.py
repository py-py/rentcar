from core.models import User
from rest_framework import serializers
from rest_framework import viewsets
from vehicle.models import Vehicle

from api.permissions import IsInvestor
from api.permissions import IsManager


class VehicleSerializer(serializers.ModelSerializer):
    investor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.investors(),
        source="investor",
    )
    manager_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        required=False,
        queryset=User.objects.managers(),
        source="manager",
    )

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "brand",
            "model",
            "year_of_production",
            "car_mileage",
            "type",
            "transmission_type",
            "fuel_type",
            "passengers",
            "manager_id",
            "investor_id",
            "investor_daily_price",
            "manager_daily_price",
            "post_service_duration",
            "is_removed",
            "images",
        )


class VehicleMixinViewSet:
    queryset = Vehicle.objects.available()
    serializer_class = VehicleSerializer
    filterset_fields = (
        "type",
        "transmission_type",
        "fuel_type",
        "passengers",
        "fuel_type",
    )

    def perform_destroy(self, instance: Vehicle):
        instance.is_removed = True
        instance.save(update_fields=("is_removed",))


class OwnedVehicleViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    permission_classes = [IsInvestor]

    def get_queryset(self):
        return super().get_queryset().filter(investor=self.request.user)


class ManagedVehicleViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    permission_classes = [IsManager]

    def get_queryset(self):
        return super().get_queryset().filter(manager=self.request.user)


class VehicleViewSet(VehicleMixinViewSet, viewsets.ReadOnlyModelViewSet):
    pass
