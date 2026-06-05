# Guia PWA - Sistema de Rastreamento de Frotas

## 📱 Instalação da PWA

### Como instalar em Android
1. Acesse a aplicação no navegador Chrome, Firefox ou Edge
2. Toque no menu (⋮) no canto superior direito
3. Selecione **"Instalar app"** ou **"Adicionar à tela inicial"**
4. Confirme a instalação
5. A app será adicionada à sua tela inicial como um app nativo

### Como instalar em iOS
1. Abra a aplicação no Safari
2. Toque no botão de compartilhamento (↗️) na parte inferior
3. Selecione **"Adicionar à tela inicial"**
4. Escolha um nome para o app
5. Toque em **"Adicionar"**

### Em Desktop
1. Acesse a aplicação no navegador
2. Clique no ícone de instalação (🔗) na barra de endereço
3. Selecione **"Instalar"**

---

## 📍 Rastreamento de Localização

### Funcionalidades
- ✅ **Rastreamento automático** em tempo real
- ✅ **Sincronização offline** - localizações são armazenadas quando offline
- ✅ **Notificações** quando o rastreamento está ativo
- ✅ **ID único do dispositivo** - cada smartphone recebe um ID único

### Permissões Necessárias
A aplicação solicitará as seguintes permissões:
- **Localização**: Para coletar a posição GPS do smartphone
- **Notificações**: Para alertar sobre o status do rastreamento

**Importante**: Você deve aceitar estas permissões para que o rastreamento funcione corretamente.

### Como Usar

#### 1. Iniciar o Rastreamento
Quando você acessa qualquer página da aplicação, o rastreamento inicia automaticamente:

```javascript
// O script geolocation.js inicia automaticamente
// Você verá uma notificação "Rastreamento Ativo"
```

#### 2. Visualizar Status
Abra o console do navegador (F12) e execute:

```javascript
console.log(window.geoTracker.getStatus());
// Retorna: {
//   isTracking: true,
//   vehicleId: "DEVICE-XXXXX-YYYY",
//   pendingLocations: 0
// }
```

#### 3. Parar o Rastreamento
```javascript
window.geoTracker.stopTracking();
```

#### 4. Retomar o Rastreamento
```javascript
window.geoTracker.startTracking();
```

---

## 🔄 Sincronização de Dados

### Sincronização Automática
- As localizações são enviadas a cada 60 segundos (configurável)
- Se o envio falhar, as localizações são armazenadas localmente
- A sincronização automática ocorre a cada 5 minutos
- Se perder internet, os dados serão sincronizados quando a conexão retornar

### Sincronização Manual
```javascript
// Sincronizar localizações pendentes
await window.geoTracker.syncPendingLocations();
```

### Dados Armazenados Localmente
Os seguintes dados são armazenados no smartphone:
- `frotasVehicleId` - ID único do dispositivo
- `frotasPendingLocations` - Localizações que não foram sincronizadas

---

## 🔌 API de Geolocalização

### Endpoint: POST `/api/localizacao/`
Recebe a localização do dispositivo

**Requisição:**
```json
{
    "vehicle_id": "DEVICE-XXXXX-YYYY",
    "lat": -23.5505,
    "lng": -46.6333,
    "accuracy": 10.5,
    "timestamp": "2026-06-04T10:30:00Z"
}
```

**Resposta:**
```json
{
    "status": "ok",
    "message": "Localização registrada com sucesso",
    "location_id": 123,
    "timestamp": "2026-06-04T10:30:00Z"
}
```

---

### Endpoint: GET `/api/listar/`
Lista as localizações registradas

**Query Parameters:**
- `limit` (padrão: 50, máximo: 500) - Número de registros
- `vehicle_id` (opcional) - Filtrar por ID do veículo

**Exemplo:**
```
GET /api/listar/?limit=10&vehicle_id=DEVICE-XXXXX-YYYY
```

**Resposta:**
```json
{
    "status": "ok",
    "count": 10,
    "locations": [
        {
            "id": 123,
            "vehicle_id": "DEVICE-XXXXX-YYYY",
            "vehicle_name": "Dispositivo Móvel PWA Rastreador",
            "lat": -23.5505,
            "lng": -46.6333,
            "timestamp": "2026-06-04T10:30:00Z"
        }
    ]
}
```

---

### Endpoint: GET `/api/rastreamento/<vehicle_id>/`
Obter a última localização de um veículo

**Exemplo:**
```
GET /api/rastreamento/DEVICE-XXXXX-YYYY/
```

**Resposta:**
```json
{
    "status": "ok",
    "location": {
        "id": 123,
        "vehicle_id": "DEVICE-XXXXX-YYYY",
        "vehicle_name": "Dispositivo Móvel PWA Rastreador",
        "lat": -23.5505,
        "lng": -46.6333,
        "timestamp": "2026-06-04T10:30:00Z"
    }
}
```

---

## 🛠️ Configuração do Rastreamento

### Alterar Intervalo de Rastreamento
```javascript
// Modificar tempo entre coletas (em milissegundos)
window.geoTracker.trackingInterval = 30000; // 30 segundos
```

### Desabilitar Alta Precisão
```javascript
// Se a bateria for um problema
window.geoTracker.enableHighAccuracy = false;
```

### Parar de Usar Geolocalização
```javascript
window.geoTracker.stopTracking();
```

---

## 📊 Visualizar Dados no Django Admin

1. Acesse http://localhost:8000/admin/
2. Navegue até **Gest Frotas App** → **Localizações do Veículo**
3. Você verá todas as localizações registradas com:
   - Placa/ID do Veículo
   - Latitude e Longitude
   - Timestamp (data e hora)

---

## 🐛 Troubleshooting

### Rastreamento não inicia
- Verifique se as permissões de localização foram aceitas
- Abra o DevTools (F12) e verifique a console
- Verifique se o GPS está ativado no smartphone

### Dados não sincronizam
- Verifique a conexão de internet
- Abra a console: `console.log(window.geoTracker.pendingLocations)`
- Force sincronização: `window.geoTracker.syncPendingLocations()`

### App não instala
- Certifique-se de acessar por HTTPS (em produção)
- Verifique se o manifest.json está sendo servido
- Limpe o cache do navegador

### Localização muito imprecisa
- Certifique-se de estar ao ar livre (GPS funciona melhor)
- Desligue "Alta Precisão" se a bateria for um problema
- Aguarde alguns segundos para o GPS se calibrar

---

## 📝 Logs e Debugging

### Visualizar logs no console
```javascript
// Todos os logs contêm [Geolocation] no início
console.log(window.geoTracker);
```

### Exportar dados locais
```javascript
// Copiar ID do dispositivo
copy(localStorage.getItem('frotasVehicleId'));

// Copiar localizações pendentes
copy(localStorage.getItem('frotasPendingLocations'));
```

---

## 🔒 Segurança

### Dados enviados
- ✅ Localização GPS (latitude, longitude)
- ✅ Precisão da localização
- ✅ Timestamp
- ✅ ID único do dispositivo

### Dados NOT enviados
- ❌ Dados pessoais do usuário
- ❌ Histórico de navegação
- ❌ Dados de contatos

---

## 📞 Suporte

Para problemas ou sugestões, entre em contato com o administrador do sistema.

**Versão**: 1.0
**Última atualização**: 2026-06-04
