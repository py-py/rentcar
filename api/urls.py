from django.urls import path
from rest_framework import routers

from .endpoints.healthcheck import HealthCheckAPIView
from .endpoints.user import UserViewSet
from .endpoints.vehicle import ManagedVehicleViewSet
from .endpoints.vehicle import OwnedVehicleViewSet
from .endpoints.vehicle import VehicleImageViewSet
from .endpoints.vehicle import VehicleViewSet

router = routers.SimpleRouter()
router.register("vehicles/owned", OwnedVehicleViewSet, basename="vehicles-owned")
router.register("vehicles/managed", ManagedVehicleViewSet, basename="vehicles-managed")
router.register("vehicles", VehicleViewSet)
router.register("images", VehicleImageViewSet)
router.register("users", UserViewSet)

urlpatterns = router.urls + [
    path("healthcheck/", HealthCheckAPIView.as_view()),
]
