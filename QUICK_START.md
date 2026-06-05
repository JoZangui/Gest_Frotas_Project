# ⚡ Quick Start - PWA Rastreamento de Frotas

## 🚀 Comece Agora em 3 Passos

### Passo 1: Iniciar o Servidor
```bash
# Terminal 1 - Django Server
python manage.py runserver 0.0.0.0:8000
```

### Passo 2: Acessar a Aplicação
- **Desktop**: http://localhost:8000/
- **Smartphone**: http://SEU_IP:8000/

### Passo 3: Permitir Permissões
Quando o navegador solicitar:
1. ✅ Permitir Localização
2. ✅ Permitir Notificações

**Pronto!** O rastreamento iniciará automaticamente. 🎉

---

## 📱 Instalar como App

### Android (Chrome/Firefox)
1. Menu ⋮ → "Instalar app"
2. Confirmar

### iOS (Safari)
1. Compartilhar ↗️ → "Adicionar à tela inicial"
2. Nomear e adicionar

---

## 🎛️ Painel de Controle

Acesse: **http://localhost:8000/rastreamento/**

Aqui você pode:
- 📊 Ver status do rastreamento em tempo real
- 📍 Ver ID único do dispositivo
- ⏳ Ver localizações pendentes
- ▶️ Iniciar/parar rastreamento
- 🔄 Sincronizar dados manualmente

---

## 👨‍💻 Console JavaScript (Avançado)

Pressione **F12** e teste:

```javascript
// Ver status
window.geoTracker.getStatus()

// Iniciar rastreamento
window.geoTracker.startTracking()

// Parar rastreamento
window.geoTracker.stopTracking()

// Sincronizar dados offline
await window.geoTracker.syncPendingLocations()
```

---

## 📊 Visualizar Dados

### Admin Django
1. Acesse: http://localhost:8000/admin/
2. Login com seu usuário
3. **Gest Frotas App** → **Localizações do Veículo**

### API
```bash
# Listar últimas 10 localizações
curl http://localhost:8000/api/listar/?limit=10

# Filtrar por dispositivo
curl "http://localhost:8000/api/listar/?vehicle_id=DEVICE-XXX"

# Última localização de um dispositivo
curl http://localhost:8000/api/rastreamento/DEVICE-XXX/
```

---

## ✅ Verificar Instalação

```bash
python verify_pwa_setup.py
```

Este script verifica se tudo foi instalado corretamente.

---

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Rastreamento não inicia | Verifique permissões de localização no navegador |
| Dados não sincronizam | Verifique conexão de internet |
| App não instala | Use HTTPS em produção |
| Localização imprecisa | Aguarde alguns segundos para GPS calibrar |

---

## 📚 Documentação Completa

- **PWA_GUIDE.md** - Guia completo com screenshots
- **IMPLEMENTATION_SUMMARY.md** - Resumo técnico das mudanças
- **Este arquivo** - Quick Start

---

## 🎯 Recursos Principais

✨ **Geolocalização Automática**
- Coleta GPS contínua em tempo real
- Funciona offline com sincronização automática

✨ **PWA (Progressive Web App)**
- Instalável em smartphones
- Funciona como app nativa
- Funciona offline

✨ **Banco de Dados**
- Todas as localizações são registradas em `LocalizacaoDoVeiculo`
- Cada smartphone recebe um ID único

---

## 🎓 Próximas Funcionalidades (Opcional)

- Histórico de rotas em mapa
- Alertas de zona geográfica
- Dashboard com estatísticas
- Exportação de dados

---

**Pronto para começar?** 🚀

Acesse: http://localhost:8000/
