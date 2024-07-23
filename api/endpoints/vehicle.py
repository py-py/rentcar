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


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filterset_fields = ("make", "model", "type", "gearshift", "passengers")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
