from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__)


@cache_page(5 * 60)
def say_hello(request):
    response = requests.get("https://httpbin.org/delay/2")
    data = response.json()
    return render(request, "hello.html", context={"name": data})


class SayHi(APIView):
    def get(self, request):
        try:
            logger.info("calling httpBin")
            response = requests.get("https://httpbin.org/delay/2")
            logger.info("Received the response")
            data = response.json()
        except Exception as e:
            logger.critical("Failed to connect to httpBin")
        return render(request, "hello.html", context={"name": data})
