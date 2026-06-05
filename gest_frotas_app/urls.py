""" urls.py para gest_frotas_app """
# gest_frotas_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('veiculos/', views.veiculos, name='veiculo_list'),
    path('motoristas/', views.motoristas, name='motorista_list'),
    path('rotas/', views.rotas, name='rotas'),
    path('metricas/', views.metricas, name='metricas'),
    path("mapa/", views.mapa, name="mapa"),
    path("rastreamento/", views.rastreamento_painel, name="rastreamento_painel"),
    
    # API endpoints para geolocalização
    path("api/localizacao/", views.receber_localizacao, name="receber_localizacao"),
    path("api/listar/", views.listar_localizacoes, name="listar_localizacoes"),
    path("api/rastreamento/<str:vehicle_id>/", views.obter_ultimo_rastreamento, name="obter_rastreamento"),
]