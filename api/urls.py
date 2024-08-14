from django.urls import path
from rest_framework import routers

from .endpoints.geo import CityViewSet
from .endpoints.geo import CountryViewSet
from .endpoints.healthcheck import HealthCheckAPIView
from .endpoints.user import UserViewSet
from .endpoints.vehicle import ManagedVehicleViewSet
from .endpoints.vehicle import OwnedVehicleViewSet
from .endpoints.vehicle import VehicleImageViewSet
from .endpoints.vehicle import VehicleOrderViewSet
from .endpoints.vehicle import VehicleViewSet

router = routers.SimpleRouter()
router.register("vehicles/owned", OwnedVehicleViewSet, basename="vehicles-owned")
router.register("vehicles/managed", ManagedVehicleViewSet, basename="vehicles-managed")
router.register("vehicles/orders", VehicleOrderViewSet)
router.register("vehicles", VehicleViewSet)
router.register("images", VehicleImageViewSet)

router.register("geo/countries", CountryViewSet)
router.register("geo/cities", CityViewSet)

router.register("users", UserViewSet)


urlpatterns = router.urls + [
    path("healthcheck/", HealthCheckAPIView.as_view()),
]
