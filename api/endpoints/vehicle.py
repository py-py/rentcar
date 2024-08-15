from datetime import datetime

from core.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from geo.models import City
from geo.models import Country
from pyuploadcare.dj.client import get_uploadcare_client
from rest_framework import mixins
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from vehicle.models import Vehicle
from vehicle.models import VehicleImage
from vehicle.models import VehicleReservation

from ..filters import VehicleFilterSet
from ..permissions import IsInvestor
from ..permissions import IsManager


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
            "uuid",
            "vehicle_id",
            "image",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        fd: InMemoryUploadedFile = attrs["image"]
        client = get_uploadcare_client()
        attrs["image"] = client.upload(fd, size=fd.size)
        return attrs


# TODO: might be extend depend on the Agent/Manager/Owner
class ReadVehicleReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleReservation
        fields = ["id", "starts_at", "ends_at"]


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
    images = VehicleImageSerializer(many=True, read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        required=False,
        queryset=Country.objects.all(),
        source="country",
    )
    city_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        required=False,
        queryset=City.objects.all(),
        source="city",
    )

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "uuid",
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
            "country_id",
            "city_id",
            "images",
        )


class VehicleMixinViewSet:
    queryset = Vehicle.objects.available().prefetch_related("images")
    serializer_class = VehicleSerializer
    filterset_class = VehicleFilterSet

    def perform_destroy(self, instance: Vehicle):
        instance.is_removed = True
        instance.save(update_fields=("is_removed",))

    @action(detail=True, serializer_class=ReadVehicleReservationSerializer)
    def reservations(self, request, *args, **kwargs):
        vehicle: Vehicle = self.get_object()
        queryset = vehicle.reservations.order_by("starts_at")
        serializer = ReadVehicleReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class OwnedVehicleViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    permission_classes = [IsInvestor]

    def get_queryset(self):
        return super().get_queryset().filter(investor=self.request.user)


class ManagedVehicleViewSet(VehicleMixinViewSet, viewsets.ModelViewSet):
    permission_classes = [IsManager]

    def get_queryset(self):
        return super().get_queryset().filter(manager=self.request.user)


class AgentVehicleViewSet(VehicleMixinViewSet, viewsets.ReadOnlyModelViewSet):
    pass


class VehicleImageViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = VehicleImage.objects.select_related("vehicle")
    serializer_class = VehicleImageSerializer
    permission_classes = [IsInvestor | IsManager]

    def get_queryset(self):
        filters = Q(vehicle__investor=self.request.user) | Q(vehicle__manager=self.request.user)
        return super().get_queryset().filter(filters)


class CreateVehicleReservationSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        required=False,
        queryset=Vehicle.objects.available(),
        source="vehicle",
    )

    class Meta:
        model = VehicleReservation
        fields = [
            "id",
            "vehicle_id",
            "starts_at",
            "ends_at",
            "daily_price",
            "client_name",
            "client_phone",
            "notes",
        ]

    @staticmethod
    def validate_starts_at(value: datetime):
        return value.replace(minute=0, second=0, microsecond=0)

    @staticmethod
    def validate_ends_at(value: datetime):
        return value.replace(minute=0, second=0, microsecond=0)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        vehicle: Vehicle = attrs["vehicle"]
        if (
            Vehicle.objects.filter(id=vehicle.id)
            .reserved(starts_at=attrs["starts_at"], ends_at=attrs["ends_at"])
            .exists()
        ):
            raise serializers.ValidationError({"vehicle": "The vehicle is busy at this time."})
        return attrs


class VehicleReservationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = VehicleReservation.objects.all()
    serializer_class = CreateVehicleReservationSerializer
