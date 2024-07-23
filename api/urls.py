from rest_framework import routers

from .endpoints.vehicle import VehicleInGarageViewSet
from .endpoints.vehicle import VehicleViewSet

router = routers.SimpleRouter()
router.register("garage/vehicles", VehicleInGarageViewSet, basename="garage-vehicle")
router.register("vehicles", VehicleViewSet)

urlpatterns = router.urls
