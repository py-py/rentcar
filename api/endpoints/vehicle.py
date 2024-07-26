from core.models import User
from rest_framework import serializers
from rest_framework import viewsets
from vehicle.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(queryset=User.objects.investors())

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "investor",
            "brand",
            "model",
            "year_of_production",
            "car_mileage",
            "type",
            "transmission_type",
            "fuel_type",
            "passengers",
            "investor_daily_price",
            "manager_daily_price",
            "post_service_duration",
        )


class VehicleMixinViewSet:
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_fields = (
        "brand",
        "model",
        "type",
        "transmission_type",
        "passengers",
        "fuel_type",
    )


class VehicleInGarageViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return super().get_queryset().filter(investor=self.request.user)


class VehicleViewSet(VehicleMixinViewSet, viewsets.ReadOnlyModelViewSet):
    pass
