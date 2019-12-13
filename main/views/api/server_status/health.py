from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from main.util.logger.init_logger import get_logger

logger = get_logger(__name__)


class ServerHealth(APIView):
    url = 'api/server_status/health'

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('testing', openapi.IN_QUERY, description='im just testing',
                          type=openapi.TYPE_STRING)], )
    def get(self, request):
        logger.info(self.url)

        response = {
            'health': 'up'
        }
        return JsonResponse(response)


class SecretHealth(APIView):
    url = 'api/server_status/secrethealth'

    @method_decorator(login_required)
    def get(self, request):
        logger.info(self.url)

        response = {
            'health': 'up'
        }
        return JsonResponse(response)
