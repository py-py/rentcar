from rest_framework import routers

from .endpoints.vehicle import VehicleViewSet

router = routers.SimpleRouter()

router.register("vehicles", VehicleViewSet)

urlpatterns = router.urls
