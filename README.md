# Sofía — Agente de WhatsApp (Asistente personal de citas)

Agente de WhatsApp con IA construido con [AgentKit](https://github.com/Hainrixz/whatsapp-agentkit).
Funciona como asistente personal: **responde mensajes** en tu WhatsApp y
**gestiona tu agenda de citas** (consulta disponibilidad, agenda, lista,
reagenda y cancela) usando herramientas reales de Claude (tool use),
no solo texto.

## Qué hace

- Responde mensajes de WhatsApp 24/7 en español, con tono amigable y profesional
- Consulta disponibilidad real de tu agenda antes de proponer horarios
- Agenda citas con nombre, fecha, hora y motivo (evita dobles reservas)
- Lista, reagenda y cancela citas — cada persona solo ve/gestiona las suyas
- Te avisa por WhatsApp cuando alguien agenda o cancela (opcional, `NUMERO_DUENO`)
- Recuerda la conversación de cada contacto (memoria por número de teléfono)
- Puedes darle contexto extra poniendo archivos `.txt`/`.md` en `/knowledge`

## Estructura

```
agent/
  main.py            Servidor FastAPI + webhook de WhatsApp
  brain.py           Conexión con Claude API (tool use + knowledge)
  memory.py          Historial de conversaciones (SQLite/PostgreSQL)
  agenda.py          Motor de citas: disponibilidad, agendar, cancelar
  tools.py           Herramientas que Claude puede usar en la conversación
  providers/         Adaptadores de WhatsApp (Meta Cloud API y Twilio)
config/
  business.yaml      Datos del negocio + horario de la agenda
  prompts.yaml       Personalidad del agente (system prompt)
knowledge/           Archivos con información extra para el agente
tests/
  test_local.py      Chat en terminal (simula WhatsApp, requiere API key)
  test_agenda.py     Pruebas del motor de citas (sin API key)
```

## Puesta en marcha

### 1. Instala dependencias

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configura tus llaves

```bash
cp .env.example .env
```

Edita `.env`:

- `ANTHROPIC_API_KEY` — en [platform.anthropic.com](https://platform.anthropic.com/settings/api-keys)
- `WHATSAPP_PROVIDER` — `twilio` (recomendado para empezar, sandbox gratis) o `meta`
- Las credenciales del proveedor elegido (ver comentarios del `.env.example`)
- `NUMERO_DUENO` — tu número, para recibir avisos de citas nuevas/canceladas (opcional)

### 3. Pruébalo en la terminal (sin WhatsApp)

```bash
python tests/test_agenda.py   # verifica el motor de citas (no necesita API key)
python tests/test_local.py    # chatea con el agente (necesita ANTHROPIC_API_KEY)
```

Ejemplo de conversación:

```
Tu: Hola, quiero una cita para mañana en la tarde
Agente: ¡Hola! Claro que sí. Mañana jueves 17 de julio tengo estos
        horarios disponibles por la tarde: 15:00, 16:00 y 17:00.
        ¿Cuál te acomoda? ¿Me compartes tu nombre y el motivo de la cita?
```

### 4. Arranca el servidor

```bash
uvicorn agent.main:app --reload --port 8000
```

### 5. Conecta WhatsApp

**Twilio** (Console → Messaging → WhatsApp Sandbox Settings):
- "When a message comes in": `https://TU-URL/webhook` (método POST)

**Meta Cloud API** (developers.facebook.com → tu app → WhatsApp → Configuration):
- Callback URL: `https://TU-URL/webhook`
- Verify Token: el mismo de `META_VERIFY_TOKEN`
- Suscríbete al campo `messages`

Para desarrollo local puedes exponer el puerto con [ngrok](https://ngrok.com): `ngrok http 8000`.

## Deploy a producción (Railway)

1. Sube el repo a GitHub (el `.env` nunca se sube, ya está en `.gitignore`)
2. En [railway.app](https://railway.app): New Project → Deploy from GitHub repo
3. Agrega las variables de entorno (las mismas de tu `.env`, con `ENVIRONMENT=production`;
   si agregas PostgreSQL, Railway te da el `DATABASE_URL`)
4. Configura el webhook de tu proveedor con la URL pública de Railway

También hay `Dockerfile` y `docker-compose.yml` (`docker compose up --build`).

## Personalización

- **Horario de la agenda, duración de citas y zona horaria**: `config/business.yaml` (sección `agenda`)
- **Nombre, tono y reglas del agente**: `config/prompts.yaml`
- **Información extra** (precios, servicios, FAQ): archivos `.txt` o `.md` en `/knowledge`
- **Modelo de Claude**: variable `CLAUDE_MODEL` en `.env`
