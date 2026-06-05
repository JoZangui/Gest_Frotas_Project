# ⚙️ Configuração Avançada - PWA Rastreamento de Frotas

## 📋 Índice
1. [Configurações do Geolocation](#configurações-do-geolocation)
2. [Configurações do Service Worker](#configurações-do-service-worker)
3. [Configurações do Manifest](#configurações-do-manifest)
4. [Variáveis de Ambiente](#variáveis-de-ambiente)
5. [Performance](#performance)
6. [Segurança](#segurança)

---

## Configurações do Geolocation

### Via JavaScript (Console)

```javascript
// Exemplo 1: Customizar intervalo de rastreamento
window.geoTracker.trackingInterval = 30000; // 30 segundos

// Exemplo 2: Desabilitar alta precisão (economizar bateria)
window.geoTracker.enableHighAccuracy = false;

// Exemplo 3: Customizar timeout
window.geoTracker.timeout = 15000; // 15 segundos

// Exemplo 4: Customizar idade máxima do cache
window.geoTracker.maximumAge = 5000; // 5 segundos
```

### Via Variáveis de Ambiente (Django)

Adicione ao `settings.py`:

```python
# Configurações de Geolocalização
GEOLOCATION_CONFIG = {
    'TRACKING_INTERVAL': 60000,      # milissegundos
    'ENABLE_HIGH_ACCURACY': True,    # melhor precisão
    'TIMEOUT': 30000,                # timeout em ms
    'MAXIMUM_AGE': 0,                # sempre obter novo
    'AUTO_SYNC_INTERVAL': 300000,    # 5 minutos
    'MAX_RETRY_ATTEMPTS': 3,         # máximas tentativas
}
```

---

## Configurações do Service Worker

### Modificar Cache Strategy

Em `static/js/service-worker.js`:

```javascript
// Network First (conexão rápida)
event.respondWith(
    fetch(request)
        .then(response => {
            caches.open(CACHE_NAME).then(cache => {
                cache.put(request, response.clone());
            });
            return response;
        })
        .catch(() => caches.match(request))
);

// Cache Only (offline completo)
event.respondWith(caches.match(request));
```

### Adicionar Mais URLs ao Cache

```javascript
const urlsToCache = [
    '/',
    '/mapa/',
    '/static/js/geolocation.js',
    '/static/js/manifest.json',
    '/static/css/style.css',  // Adicione suas CSS
    '/static/images/logo.png' // Adicione suas imagens
];
```

---

## Configurações do Manifest

### Temas Personalizados

Em `static/js/manifest.json`:

```json
{
  "name": "Seu Nome Custom",
  "short_name": "Seu App",
  "theme_color": "#FF6B6B",
  "background_color": "#FFFFFF",
  "display": "fullscreen",
  "orientation": "landscape"
}
```

### Adicionar Ícone Dinâmico

```json
{
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/static/icons/icon-maskable-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

---

## Variáveis de Ambiente

### Arquivo `.env`

```bash
# Django
DEBUG=False
SECRET_KEY=seu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# PWA
PWA_ENABLED=True
PWA_NAME=Gestão de Frotas
PWA_SHORT_NAME=Frotas

# Geolocation
GEO_TRACKING_INTERVAL=60000
GEO_ENABLE_HIGH_ACCURACY=True
GEO_AUTO_SYNC_INTERVAL=300000

# Database
DATABASE_URL=sqlite:///db.sqlite3

# API
API_TIMEOUT=30000
MAX_LOCATIONS_STORED=1000
```

### Usar no Django

```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'insecure-key')
```

---

## Performance

### Otimizações Recomendadas

#### 1. Reduzir Frequência de Rastreamento em Modo Economia de Bateria

```javascript
// Detectar modo economia de bateria
if ('getBattery' in navigator) {
    navigator.getBattery().then(battery => {
        if (battery.level < 0.2) {
            // Reduzir frequência
            window.geoTracker.trackingInterval = 120000; // 2 minutos
        }
        battery.addEventListener('levelchange', () => {
            if (battery.level < 0.2) {
                window.geoTracker.trackingInterval = 120000;
            } else {
                window.geoTracker.trackingInterval = 60000;
            }
        });
    });
}
```

#### 2. Usar Web Workers para Rastreamento

```javascript
// worker.js
self.onmessage = (event) => {
    const locations = event.data;
    // Processar localizações em background
    self.postMessage(processedData);
};
```

#### 3. Compressão de Dados

```javascript
// Comprimir dados antes de enviar
async function compressLocation(location) {
    const encoded = JSON.stringify(location);
    const compressed = await compress(encoded);
    return compressed;
}
```

---

## Segurança

### 1. HTTPS Obrigatório em Produção

```python
# settings.py
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 2. Content Security Policy

```python
MIDDLEWARE = [
    # ...
    'django_csp.middleware.CSPMiddleware',
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_CONNECT_SRC = ("'self'", "https://nominatim.openstreetmap.org")
```

### 3. Validação de IP

```python
# views.py
from django.core.exceptions import PermissionDenied

def receber_localizacao(request):
    # Whitelist de IPs
    allowed_ips = ['192.168.1.0/24', 'localhost']
    
    if not is_allowed_ip(request.META['REMOTE_ADDR'], allowed_ips):
        raise PermissionDenied()
```

### 4. Rate Limiting

```python
# settings.py
INSTALLED_APPS = ['django_ratelimit', ...]

# views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='POST')
def receber_localizacao(request):
    # Máximo 10 requests por minuto
    pass
```

### 5. Autenticação de Token

```python
# views.py
from django.middleware.csrf import ensure_csrf_cookie
from rest_framework.authentication import TokenAuthentication

@require_http_methods(["POST"])
def receber_localizacao(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token not in ALLOWED_TOKENS:
        return JsonResponse({"error": "Unauthorized"}, status=401)
```

---

## Monitoramento

### Logging Detalhado

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/geolocation.log',
        },
    },
    'loggers': {
        'gest_frotas_app': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Métrica de Performance

```javascript
// Medir tempo de resposta
const start = performance.now();
await fetch('/api/localizacao/', {
    method: 'POST',
    body: JSON.stringify(location)
});
const duration = performance.now() - start;
console.log(`API Response time: ${duration}ms`);
```

---

## Escalabilidade

### Para Muitos Dispositivos

1. **Use Fila de Tarefas** (Celery)
```python
from celery import shared_task

@shared_task
def processar_localizacao(location_data):
    # Processar asincronamente
    pass
```

2. **Cache com Redis**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

3. **Database Indexing**
```python
# models.py
class LocalizacaoDoVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['veiculo', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]
```

---

## Exemplo Completo de Customização

```python
# settings.py - Configuração Completa

GEOLOCATION = {
    # Tracking
    'INTERVAL': 60000,
    'HIGH_ACCURACY': True,
    'TIMEOUT': 30000,
    
    # Sync
    'AUTO_SYNC_INTERVAL': 300000,
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 5000,
    
    # Storage
    'MAX_LOCAL_STORAGE': 100,
    'CACHE_TIMEOUT': 3600,
    
    # API
    'API_ENDPOINT': '/api/localizacao/',
    'API_TIMEOUT': 10000,
    
    # Security
    'REQUIRE_AUTH': True,
    'RATE_LIMIT': '10/m',
    'VALIDATE_IP': False,
}
```

---

## Links Úteis

- [Web Geolocation API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)
- [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)

---

**Versão**: 1.0  
**Última atualização**: 2026-06-04
