from django.http import JsonResponse
from rest_framework.views import APIView


class ServerHealth(APIView):
    def get(self, request):
        response = {
            'health': 'up'
        }
        return JsonResponse(response)
