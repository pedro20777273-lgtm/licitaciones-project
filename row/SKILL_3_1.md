---
name: requerimientos-licitaciones
description: Genera los entregables de un REQUERIMIENTO DE DOCUMENTACIÓN PREVIA a la adjudicación en licitaciones públicas españolas (LCSP) para Hologic Iberia. Úsala SIEMPRE que el usuario adjunte o mencione un requerimiento de adjudicatario, pliegos (PCAP, CRC, Anexo I, PPT), o pida preparar la documentación previa a la adjudicación, un índice de documentación presentada, una ficha de aval bancario, una declaración responsable, o localizar/recopilar documentos corporativos para un expediente. Triggers: "requerimiento", "documentación previa", "índice de documentación", "ficha de aval", "garantía definitiva", "propuesto adjudicatario", "presentar documentación licitación". Produce 3 entregables (.docx) preservando EXACTAMENTE el formato de las plantillas Hologic.
---

# Requerimientos de documentación previa — Hologic Iberia

Convierte un expediente de licitación (requerimiento + pliegos) en 3 entregables listos
para presentar, preservando **exactamente** el formato de las plantillas Hologic.

## Recursos de la skill
- `assets/plantilla_indice.docx` — Índice de documentación (fuente Proxima Nova, pie azul #0F206C).
- `assets/plantilla_aval.docx` — Ficha base para solicitud de aval bancario.
- `assets/plantilla_declaracion.docx` — Declaración responsable genérica (firma Sergio Sánchez de Torres).
- `assets/rolece_hologic.pdf` — Certificado ROLECE vigente de referencia.
- `references/datos_fijos_hologic.md` — Datos de empresa, apoderado y cifras de negocio. **Leer siempre.**
- `references/reglas_extraccion.md` — Dónde buscar cada dato y reglas por entregable. **Leer siempre.**

## Regla de oro sobre el formato
Las plantillas se rellenan con los scripts incluidos, que **clonan los párrafos-plantilla y
sustituyen solo el texto conservando su `rPr`** (fuente, negrita, tamaño) y el pie de página.
NUNCA regenerar el documento desde cero ni con un docx nuevo: se perdería el formato corporativo.
Si necesitas un cambio estructural no soportado, edita el XML directamente con `unpack.py` /
`pack.py`, no reescribas la plantilla.

## Flujo de trabajo

### Paso 0 — Reunir entradas
El usuario aporta DOS URL de carpeta general (no una por documento):
- **Carpeta de pliegos del expediente:** localiza tú dentro de ella el requerimiento, PCAP,
  CRC/Anexo I y PPT.
- **Carpeta de recursos / documentos corporativos:** para el Entregable 3 (certificados, poder,
  cuentas anuales, etc.).

Si dentro de la carpeta de pliegos falta el PCAP o el CRC, pídelos antes de continuar: el índice
y el aval dependen de ellos. Si las URL requieren autenticación y no son accesibles, pide al
usuario que suba los pliegos al chat.
Lee primero `references/datos_fijos_hologic.md` y `references/reglas_extraccion.md`.

### Paso 1 — RESUMEN del expediente
Extrae y muestra: nº de expediente, objeto (literal), órgano de contratación, tipo de
procedimiento, plazo de presentación, PBL, y garantía definitiva (importe y %).

### Paso 2 — ENTREGABLE 1: Índice de documentación
1. Identifica TODOS los documentos exigidos al adjudicatario (requerimiento + PCAP + CRC).
2. Construye un JSON con `expediente`, `objeto` y `documentos` (cadenas, o `{texto, subitems}`
   para desgloses de solvencia con letras a/b/c). Ver formato en la cabecera del script.
3. Genera el .docx:
   ```bash
   python scripts/rellenar_indice.py assets/plantilla_indice.docx datos_indice.json /mnt/user-data/outputs/Indice_[expediente].docx
   ```
Aplica las reglas estrictas de `references/reglas_extraccion.md` (no inventar documentos,
importes literales, ROLECSP, CCAA del certificado tributario).

### Paso 3 — ENTREGABLE 2: Ficha de aval
1. Busca en el CRC (puntos de garantías) el importe, beneficiario y modelo de aval.
2. Construye el JSON de datos (claves en la cabecera de `rellenar_aval.py`). El avalado es
   siempre Hologic; el órgano disponente es el ente superior (no el hospital).
3. Genera el .docx:
   ```bash
   python scripts/rellenar_aval.py assets/plantilla_aval.docx datos_aval.json /mnt/user-data/outputs/Aval_[expediente].docx
   ```

### Paso 4 — ENTREGABLE 3: Tabla de localización
Para cada documento del índice, localiza el archivo en el repositorio del usuario (si dio URL)
o pídeselo. Muestra una tabla: # | Documento | Archivo encontrado | Fecha | Vigente | Enlace o Acción.
Aplica los criterios de selección y de acción (PREPARAR / DESCARGAR / SOLICITAR) de
`references/reglas_extraccion.md`.

### Paso 5 — Declaraciones responsables que falten
Para cada documento marcado **PREPARAR** que sea una DR redactable, genérala:
```bash
python scripts/rellenar_declaracion.py assets/plantilla_declaracion.docx datos_dr.json /mnt/user-data/outputs/DR_[tipo].docx
```
JSON: `{"titulo": "...", "cuerpo": "..."}` (cuerpo admite varios párrafos con `\n`).

### Paso 6 — Cierre
Presenta los .docx generados con `present_files` y una LISTA de pendientes con acciones concretas.

## Notas
- Nombres de salida sugeridos: `Indice_[expediente].docx`, `Aval_[expediente].docx`, `DR_[tipo]_[expediente].docx`.
- Si el usuario tiene más plantillas estándar, pueden vivir en `assets/` de esta misma skill
  (ver README de assets) y añadir su propio script de relleno si su estructura difiere.
- Validar siempre el resultado abriéndolo con python-docx antes de declararlo hecho.
