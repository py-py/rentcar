from core.models import User
from rest_framework import views
from rest_framework.response import Response


class HealthCheckAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            User.objects.exists()
            return Response({"status": "success"})
        except Exception:
            return Response({"status": "failed"})
