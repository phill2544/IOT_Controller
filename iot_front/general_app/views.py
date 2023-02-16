from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
import requests
from .models import Iot

# Create your views here.

servername = "http://192.168.0.140:3000"


def home(request):
    return render(request, 'home.html', {'data': Iot.objects.all()})


def test(request):
    data = Iot.objects.get(id=1)
    context = {'temp': data.temp, 'humid': data.humid, 'adc': data.adc, 'status_fan': data.status_fan,
               'status_water': data.status_water, 'status_lamp': data.status_lamp}
    return JsonResponse(context)


def change_state_lamp(request):
    print('lamp')
    status = Iot.objects.get(id=1).status_lamp
    Iot.objects.filter(id=1).update(status_lamp=not status)
    return JsonResponse({"status": not status})


def change_state_water(request):
    print('water')
    status = Iot.objects.get(id=1).status_water
    Iot.objects.filter(id=1).update(status_water=not status)
    return JsonResponse({"status": not status})


def change_state_fan(request):
    print('fan')
    status = Iot.objects.get(id=1).status_fan
    Iot.objects.filter(id=1).update(status_fan=not status)
    return JsonResponse({"status": not status})


def get_status(request):
    status = Iot.objects.get(id=1).status
    return JsonResponse({"status": status})


def control(request):
    return render(request, 'control.html')
