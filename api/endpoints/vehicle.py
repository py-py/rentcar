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
            "images",
            "post_service_duration",
        )


class VehicleMixinViewSet:
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_fields = (
        "type",
        "transmission_type",
        "fuel_type",
        "passengers",
        "fuel_type",
    )


class VehicleInGarageViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsInvestor | IsManager]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_investor():
            return queryset.filter(investor=self.request.user)
        elif self.request.user.is_manager():
            return queryset.filter(manager=self.request.user)
        else:
            return queryset.none()


class VehicleViewSet(VehicleMixinViewSet, viewsets.ReadOnlyModelViewSet):
    pass
