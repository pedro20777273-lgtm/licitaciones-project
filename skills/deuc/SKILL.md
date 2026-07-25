# SKILL DEUC: RELLENADO DEL DEUC (ESPDResponse) - VERSION 4.0

Pedro Moronta - Hologic Iberia, S.L.U.

Rellena el DEUC del licitador (ESPDResponse) editando QUIRÚRGICAMENTE el XML que
exporta el visor español, sin regenerarlo. Objetivo: que el visor
(visor.registrodelicitadores.gob.es) y espd.eu lo acepten al reimportarlo.

---

## 1. POR QUÉ LA v4 FUNCIONA Y LA v3 NO

La v3 transformaba un `ESPDRequest` → `Response` e INSERTABA un bloque
`cac:EconomicOperatorParty` con una estructura que el visor español NO usa
(`EconomicOperatorMetadata`, namespace distinto). El visor lo rechazaba.

La v4 parte del **`espd:ESPDResponse` ya exportado del visor**. Ese XML trae:
  - La estructura real `espd-cac:EconomicOperatorParty` + `RepresentativeNaturalPerson`.
  - Las respuestas a TODOS los criterios ya puestas y correctas
    (exclusiones = false, ALL_SATISFIED = true, UTE/subcontrata/medios externos = false).
  - Los datos de empresa y firmante vacíos (campos con ".").

El script solo **rellena los huecos**. No toca estructura, namespaces, UUIDs ni orden.
Eso maximiza la aceptación al reimportar.

## 2. INPUT CORRECTO (IMPRESCINDIBLE)

El input NO es el PDF ni el `ESPDRequest` del órgano directamente. Es un
**`ESPDResponse` exportado del visor**. Cómo se obtiene:
  1. Descargar el XML del DEUC del órgano (`ESPDRequest`) del perfil del contratante.
  2. Importarlo en visor.registrodelicitadores.gob.es como **operador económico**.
  3. Exportar / guardar el documento como Response (XML). Ese es el input.

Si Pedro solo tiene el `ESPDRequest` o el PDF: hay que pasar antes por el visor
(paso 2-3). El script avisa si el XML no es un `ESPDResponse`.

## 3. DATOS FIJOS (ya codificados en el script, fuente ROLECE)

- Empresa: HOLOGIC IBERIA, S.L.U. — NIF B83279331 — VAT ESB83279331
- Domicilio: CALLE AREQUIPA Nº 1, PLANTA 3, ESC. 2,3 Y 4, EDIFICIO MAR DE CRISTAL, 28043 MADRID
- Web: https://www.hologic.com · Contacto: concursos@hologic.com · +34 913446990
- Apoderado: SERGIO SÁNCHEZ DE TORRES (cargo: Apoderado)
- ROLECSP: código de operador 43522, primera inscripción 2018-10-16
- No PYME → SMEIndicator = false · UTE = No · Medios externos = No · Inscrita ROLECSP = Sí

NO se inventa la fecha ni el lugar de nacimiento del apoderado. Se dejan vacíos
(el visor los admite en blanco). Si el órgano los exige, Pedro los pone en el visor
o los pasa en el JSON (`rep_birthdate`, `rep_birthplace`).

## 4. DATOS POR LICITACIÓN (JSON de entrada)

Fichero `datos_licitacion.json` (ver `datos_licitacion.ejemplo.json`):
```json
{
  "expediente": "A/SUM-000563/2026",
  "organo": "H.G.U. Gregorio Marañón (Comunidad de Madrid)",
  "lotes": "Lote 4",
  "rep_birthdate": "",
  "rep_birthplace": ""
}
```
`expediente` y `organo` son obligatorios. El resto, opcional.

## 5. FLUJO

PASO 1 — Verificar el input:
- Confirmar que es un `ESPDResponse` (el script aborta si no).
- Mostrar a Pedro: órgano, expediente, nº de criterios.

PASO 2 — Ejecutar:
```
python3 scripts/rellenar_deuc.py response_visor.xml RESPONSE_<EXPEDIENTE>.xml --datos datos_licitacion.json
```

PASO 3 — Control de calidad (el script lo imprime; verificar TODO True):
- XML BIEN FORMADO
- Empresa OK (HOLOGIC + B83279331) · Apoderado OK (SERGIO)
- SMEIndicator false · ROLECSP true
- Placeholders "." restantes = 0

PASO 4 — Entrega:
- Nombre: `RESPONSE_<EXPEDIENTE>.xml`
- Reimportar en el visor, revisar en pantalla, generar el PDF oficial y firmarlo con
  la firma electrónica del apoderado (Sergio Sánchez de Torres) antes de subirlo.

## 6. DEPURACIÓN — SI EL VISOR RECHAZA EL XML

NO adivinar: pedir el MENSAJE DE ERROR EXACTO (pantallazo o texto literal) y la línea.
Casos típicos:
- "No es un DEUC válido" / error de esquema: comparar raíz y namespaces del Response
  con los del Response ORIGINAL del visor. Deben ser idénticos.
- Faltan respuestas: el export del visor ya las traía; revisar que se partió del
  Response correcto, no de un Request en bruto.
- No aparecen los datos de empresa: revisar el bloque `espd-cac:EconomicOperatorParty`.
- Cada órgano puede publicar variantes del esquema. Por eso SIEMPRE se parte del
  Response exportado del visor para ESA licitación, nunca de una plantilla genérica.

Alternativa de emergencia: rellenar a mano en el visor con el plan de respuestas
(todas exclusiones No, ALL_SATISFIED Sí, UTE No, medios externos No, ROLECSP Sí,
datos de Hologic del ROLECE, apoderado Sergio). ~5 min.

## 7. INSTRUCCIÓN DE USO (copiar y pegar)

RELLENA EL DEUC

Skill y recursos: lee toda esta carpeta antes de empezar.
XML del DEUC (ESPDResponse exportado del visor): [adjunto]
Expediente: [número]
Órgano: [nombre]
Lotes a los que oferto: [todos / lotes X,Y / sin lotes]

EJECUTA:
1. Verifica que el XML es un ESPDResponse y muéstrame órgano, expediente y nº de criterios.
2. Genera datos_licitacion.json con expediente, órgano y lotes.
3. Ejecuta scripts/rellenar_deuc.py sobre MI XML.
4. Haz el control de calidad del paso 3 y muéstramelo (todo debe dar True, 0 placeholders).
5. Entrégame el RESPONSE_<EXPEDIENTE>.xml con las instrucciones de reimportación y firma.
6. Si el visor me dio error, te paso el mensaje exacto: usa la sección DEPURACIÓN.
