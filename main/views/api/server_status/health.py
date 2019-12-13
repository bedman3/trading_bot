from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.views import APIView

from main.util.logger.init_logger import get_logger

logger = get_logger(__name__)


class ServerHealth(APIView):
    url = 'api/server_status/health'

    def get(self, request):
        logger.info(self.url)

        response = {
            'health': 'up'
        }
        return JsonResponse(response)


class SecretHealth(APIView):
    url = 'api/server_status/secrethealth'

    @login_required(login_url='/accounts/login/')
    def get(self, request):
        logger.info(self.url)

        response = {
            'health': 'up'
        }
        return JsonResponse(response)
