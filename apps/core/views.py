# apps/core/views.py
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Health check endpoint for infrastructure monitoring.

    Purpose:
        - Used by Docker, Kubernetes, load balancers, and uptime monitoring
          to verify that the Django process is alive and responsive.
        - Does NOT perform database or cache checks
          (that's handled in readiness probes).

    Access:
        - Public (AllowAny)
        - Safe, fast, deterministic

    Response:
        - 200 OK with JSON {"status": "ok"}
    """

    permission_classes = [AllowAny]

    @extend_schema(responses={200})
    def get(self, request):
        return Response({"status": "ok"})
