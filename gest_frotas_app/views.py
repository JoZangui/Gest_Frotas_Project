import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import LocalizacaoDoVeiculo, Veiculo

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'gest_frotas_app/home.html')

def motoristas(request):
    return render(request, 'gest_frotas_app/motoristas.html')

def veiculos(request):
    return render(request, 'gest_frotas_app/veiculos.html')

def rotas(request):
    return render(request, 'gest_frotas_app/rotas.html')

def metricas(request):
    return render(request, 'gest_frotas_app/metricas.html')


def mapa(request):
    return render(request, "gest_frotas_app/mapa.html")


def rastreamento_painel(request):
    """
    Painel de controle de rastreamento de geolocalização.
    Permite visualizar e gerenciar o status do rastreamento.
    """
    return render(request, "gest_frotas_app/rastreamento_painel.html")


@csrf_exempt
@require_http_methods(["POST"])
def receber_localizacao(request):
    """
    Recebe localização do dispositivo móvel e armazena no banco de dados.
    
    Esperado JSON:
    {
        "vehicle_id": "DEVICE-XXX-YYY",
        "lat": -23.5505,
        "lng": -46.6333,
        "accuracy": 10.5,
        "timestamp": "2026-06-04T10:30:00Z"
    }
    """
    try:
        dados = json.loads(request.body)
        
        # Validar dados obrigatórios
        vehicle_id = dados.get("vehicle_id")
        latitude = dados.get("lat")
        longitude = dados.get("lng")
        
        if not all([vehicle_id, latitude, longitude]):
            logger.warning(f"Dados incompletos recebidos: {dados}")
            return JsonResponse(
                {"status": "error", "message": "Dados incompletos"},
                status=400
            )
        
        # Validar tipos de dados
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            logger.warning(f"Coordenadas inválidas: lat={latitude}, lng={longitude}")
            return JsonResponse(
                {"status": "error", "message": "Coordenadas inválidas"},
                status=400
            )
        
        # Criar ou obter veículo
        vehicle, created = Veiculo.objects.get_or_create(
            placa=vehicle_id,
            defaults={
                'marca': 'Dispositivo Móvel',
                'modelo': 'PWA Rastreador',
                'ano': timezone.now().year,
                'tipo': 'smartphone',
                'status': 'ativo',
                'km_atual': 0
            }
        )
        
        if created:
            logger.info(f"Novo veículo criado: {vehicle_id}")
        
        # Criar registro de localização
        localizacao = LocalizacaoDoVeiculo.objects.create(
            veiculo=vehicle,
            latitude=latitude,
            longitude=longitude
        )
        
        logger.info(f"Localização registrada - Veículo: {vehicle_id}, "
                   f"Lat: {latitude}, Lng: {longitude}")
        
        return JsonResponse({
            "status": "ok",
            "message": "Localização registrada com sucesso",
            "location_id": localizacao.pk,
            "timestamp": localizacao.timestamp.isoformat()
        })
        
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar JSON")
        return JsonResponse(
            {"status": "error", "message": "JSON inválido"},
            status=400
        )
    except Exception as e:
        logger.error(f"Erro ao registrar localização: {str(e)}")
        return JsonResponse(
            {"status": "error", "message": "Erro ao processar requisição"},
            status=500
        )


@require_http_methods(["GET"])
def listar_localizacoes(request):
    """
    Lista as últimas 50 localizações registradas.
    
    Query parameters:
    - vehicle_id: Filtrar por ID do veículo
    - limit: Número máximo de registros (padrão: 50)
    """
    try:
        limit = int(request.GET.get('limit', 50))
        limit = min(limit, 500)  # Máximo de 500 registros
        
        vehicle_id = request.GET.get('vehicle_id')
        
        queryset = LocalizacaoDoVeiculo.objects.order_by("-timestamp")
        
        if vehicle_id:
            queryset = queryset.filter(veiculo__placa=vehicle_id)
        
        localizacoes = queryset[:limit]
        
        data = [
            {
                "id": loc.pk,
                "vehicle_id": loc.veiculo.placa,
                "vehicle_name": f"{loc.veiculo.marca} {loc.veiculo.modelo}",
                "lat": loc.latitude,
                "lng": loc.longitude,
                "timestamp": loc.timestamp.isoformat()
            }
            for loc in localizacoes
        ]
        
        return JsonResponse({
            "status": "ok",
            "count": len(data),
            "locations": data
        })
        
    except ValueError:
        return JsonResponse(
            {"status": "error", "message": "Parâmetro 'limit' inválido"},
            status=400
        )
    except Exception as e:
        logger.error(f"Erro ao listar localizações: {str(e)}")
        return JsonResponse(
            {"status": "error", "message": "Erro ao processar requisição"},
            status=500
        )


@require_http_methods(["GET"])
def obter_ultimo_rastreamento(request, vehicle_id):
    """
    Obter a última localização de um veículo específico.
    """
    try:
        localizacao = LocalizacaoDoVeiculo.objects.filter(
            veiculo__placa=vehicle_id
        ).order_by("-timestamp").first()
        
        if not localizacao:
            return JsonResponse(
                {"status": "error", "message": "Nenhuma localização encontrada"},
                status=404
            )
        
        return JsonResponse({
            "status": "ok",
            "location": {
                "id": localizacao.pk,
                "vehicle_id": localizacao.veiculo.placa,
                "vehicle_name": f"{localizacao.veiculo.marca} {localizacao.veiculo.modelo}",
                "lat": localizacao.latitude,
                "lng": localizacao.longitude,
                "timestamp": localizacao.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter rastreamento: {str(e)}")
        return JsonResponse(
            {"status": "error", "message": "Erro ao processar requisição"},
            status=500
        )

