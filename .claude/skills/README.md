# Skills del proyecto

## agent-browser

Skill de automatización de navegador ([vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)), instalada con `npx skills add vercel-labs/agent-browser`. El archivo real vive en `.agents/skills/agent-browser/SKILL.md`; aquí hay un symlink para que Claude Code la descubra.

### Requisitos en cada sesión (el contenedor es efímero)

```bash
# 1. Instalar la CLI
npm install -g agent-browser

# 2. En entornos remotos de Claude Code, usar el Chromium preinstalado
#    (no ejecutar `agent-browser install`)
agent-browser open <url> --executable-path /opt/pw-browsers/chromium

# 3. Si aparece net::ERR_CERT_AUTHORITY_INVALID, agregar la CA del proxy
#    al almacén NSS que usa Chromium:
apt-get update && apt-get install -y libnss3-tools
certutil -d sql:/root/.pki/nssdb -A -t "C,," -n ccr-agent-proxy -i /root/.ccr/agent-proxy-ca.crt
```

Un `net::ERR_TUNNEL_CONNECTION_FAILED` o 403 del proxy significa que el host destino está bloqueado por la política de red del entorno; no es un error de la skill.
