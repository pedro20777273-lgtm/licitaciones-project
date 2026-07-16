# Aria — Asistente Personal por WhatsApp

Tu asistente personal con IA (basado en [AgentKit](https://github.com/Hainrixz/whatsapp-agentkit)).
Le escribes por WhatsApp y él trabaja por ti.

## Qué hace

| Capacidad | Ejemplo de lo que le escribes |
|-----------|-------------------------------|
| 🩺 **Buscar citas médicas** | "Búscame un dermatólogo en Ciudad de México" |
| 💬 **Escribir a negocios por WhatsApp** | "Pregúntale al consultorio +52... si tienen cita el viernes" |
| ✅ **Gestionar pendientes** | "Recuérdame que tengo que pagar la luz antes del 20" |
| ⏰ **Recordatorios proactivos** | "Recuérdame mañana a las 9am llamar al dentista" — te llega un WhatsApp a esa hora |
| 📋 **Planificar tu día** | "¿Qué tengo pendiente hoy? Organízame el día" |

## Regla de oro: autorización

El asistente **NUNCA envía mensajes a terceros sin tu permiso**. Siempre:
1. Te muestra el texto exacto y el número al que piensa escribir
2. Espera tu confirmación ("sí, envíalo")
3. Solo entonces envía el mensaje
4. Cuando el negocio responde, te reenvía la respuesta

## Cómo funciona

```
TÚ escribes por WhatsApp ("busca un dentista y agéndame")
        │
        ▼
Proveedor de WhatsApp (Twilio / Meta) → webhook → FastAPI (agent/main.py)
        │
        ▼
Cerebro (agent/brain.py) — Claude AI con herramientas reales:
   tareas · recordatorios · búsqueda de citas · mensajes a negocios
        │
        ▼
El asistente ejecuta, te confirma, y el scheduler (agent/scheduler.py)
te envía los recordatorios a la hora exacta
```

Solo **tu número** (`OWNER_PHONE_NUMBER`) puede darle órdenes. Si escribe
cualquier otro número, se trata como respuesta de un negocio contactado y
se te reenvía como aviso.

## Instalación

```bash
# 1. Instalar dependencias (Python 3.11+)
pip install -r requirements.txt

# 2. Configurar variables
cp .env.example .env
# Edita .env: ANTHROPIC_API_KEY, OWNER_PHONE_NUMBER y tu proveedor de WhatsApp
```

## Probar sin WhatsApp (modo consola)

Con `WHATSAPP_PROVIDER=consola` en tu `.env` (es el default), todo funciona
en la terminal — los mensajes "a negocios" se imprimen en pantalla:

```bash
python tests/test_local.py
```

```
Tú: recuérdame mañana a las 9 llamar al dentista
Aria: ✅ Listo, te lo recuerdo mañana a las 9:00am por WhatsApp.

Tú: busca un dermatólogo en Guadalajara
Aria: Encontré estas opciones en Doctoralia: ...
```

## Conectar WhatsApp real

Elige un proveedor y pon sus credenciales en `.env`:

- **Twilio** (rápido para empezar): sandbox gratis en [twilio.com](https://twilio.com).
  Necesitas `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
  y `WHATSAPP_PROVIDER=twilio`.
- **Meta Cloud API** (oficial): [developers.facebook.com](https://developers.facebook.com).
  Necesitas `META_ACCESS_TOKEN`, `META_PHONE_NUMBER_ID`, `META_VERIFY_TOKEN`
  y `WHATSAPP_PROVIDER=meta`.

Arranca el servidor y apunta el webhook del proveedor a `https://tu-dominio/webhook`:

```bash
uvicorn agent.main:app --reload --port 8000
```

## Deploy a producción (Railway)

```bash
docker compose up --build   # probar el build localmente
```

1. Sube el repo a GitHub (el `.gitignore` ya protege tu `.env`)
2. En [railway.app](https://railway.app): New Project → Deploy from GitHub repo
3. Agrega las variables de entorno de tu `.env` en Railway → Variables
4. Configura el webhook del proveedor con la URL pública de Railway: `https://tu-app.up.railway.app/webhook`

## Estructura

```
agent/
├── main.py          Servidor FastAPI + webhook (distingue dueño vs terceros)
├── brain.py         Claude AI con tool use (loop agéntico)
├── memory.py        SQLite: historial, tareas, recordatorios, acciones pendientes
├── tools.py         Herramientas: tareas, recordatorios, citas médicas, WhatsApp
├── scheduler.py     Envío proactivo de recordatorios cada minuto
└── providers/       Twilio / Meta / consola (patrón adaptador)
config/
├── asistente.yaml   Tu nombre, plataformas médicas, configuración
└── prompts.yaml     Personalidad y reglas del asistente
tests/
└── test_local.py    Chat de prueba en terminal
```

## Personalizar

Edita `config/prompts.yaml` (personalidad y reglas) y `config/asistente.yaml`
(nombre del asistente, plataformas médicas de tu país). No hace falta tocar código.
