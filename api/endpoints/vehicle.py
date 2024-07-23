from rest_framework import serializers
from rest_framework import viewsets
from vehicle.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "user",
            "make",
            "model",
            "type",
            "gearshift",
            "passengers",
            "price",
        )


class VehicleMixinViewSet:
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_fields = ("make", "model", "type", "gearshift", "passengers")


class VehicleInGarageViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_fields = ("make", "model", "type", "gearshift", "passengers")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class VehicleViewSet(VehicleMixinViewSet, viewsets.ReadOnlyModelViewSet):
    pass
