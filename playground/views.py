from django.shortcuts import render
from django.http import HttpResponse
from .tasks import notify_customers

def say_hello(request):
    notify_customers.delay("Hello from Celery!")
    return render(request, 
                  "hello.html", 
                  context={"name": "Javad"})
