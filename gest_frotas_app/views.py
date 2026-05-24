import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'home.html')

def motoristas(request):
    return render(request, 'motoristas.html')

def veiculos(request):
    return render(request, 'veiculos.html')

def rotas(request):
    return render(request, 'rotas.html')

def metricas(request):
    return render(request, 'metricas.html')


@csrf_exempt
def receber_localizacao(request):
    if request.method == "POST":
        dados = json.loads(request.body)
        lat = dados.get("lat")
        lng = dados.get("lng")
        vehicle_id = dados.get("vehicle_id")
        # Salvar no banco de dados
        # VehicleLocation.objects.create(vehicle_id=vehicle_id, latitude=lat, longitude=lng)
        return JsonResponse({"status": "ok"})
