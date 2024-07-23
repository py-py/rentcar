from rest_framework import serializers
from rest_framework import viewsets
from vehicle.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = (
            "user",
            "type",
            "gearshift",
            "passengers",
        )


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
