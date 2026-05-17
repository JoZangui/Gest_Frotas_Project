from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def motoristas(request):
    return render(request, 'motoristas.html')

def veiculos(request):
    return render(request, 'veiculos.html')

def manutencoes(request):
    return render(request, 'manutencoes.html')

def abastecimentos(request):
    return render(request, 'abastecimentos.html')

def viagens(request):
    return render(request, 'viagens.html')
