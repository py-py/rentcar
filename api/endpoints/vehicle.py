from core.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from pyuploadcare.dj.client import get_uploadcare_client
from rest_framework import mixins
from rest_framework import serializers
from rest_framework import viewsets
from vehicle.models import Vehicle
from vehicle.models import VehicleImage

from api.permissions import IsInvestor
from api.permissions import IsManager


class UploadCareImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None
        return value.cdn_url


class VehicleImageSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source="vehicle",
    )
    image = UploadCareImageField()

    class Meta:
        model = VehicleImage
        fields = (
            "id",
            "vehicle_id",
            "image",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        fd: InMemoryUploadedFile = attrs["image"]
        client = get_uploadcare_client()
        attrs["image"] = client.upload(fd, size=fd.size)
        return attrs


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
    images = VehicleImageSerializer(many=True)

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
    queryset = Vehicle.objects.available().prefetch_related("images")
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


class VehicleImageViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    queryset = VehicleImage.objects.select_related("vehicle")
    serializer_class = VehicleImageSerializer
    permission_classes = [IsInvestor | IsManager]

    def get_queryset(self):
        filters = Q(vehicle__investor=self.request.user) | Q(vehicle__manager=self.request.user)
        return super().get_queryset().filter(filters)
