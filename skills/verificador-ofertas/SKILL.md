---
name: verificador-ofertas-licitaciones
description: Chequeo final exhaustivo de una oferta de licitación pública española (LCSP 9/2017) ANTES de subirla al portal, para evitar causas de exclusión. Úsala SIEMPRE que el usuario vaya a presentar/enviar una oferta o sobres (administrativo, técnico, económico o sobre único), pida revisar/verificar/chequear los documentos de una licitación antes de presentarla, o quiera detectar contaminación de sobres, defectos subsanables/no subsanables, incoherencias de datos, incumplimientos económicos o técnicos. Triggers: "verificar oferta", "chequeo antes de presentar", "revisar sobres", "antes de subir al portal", "causa de exclusión", "contaminación de sobres", "está listo para enviar". Actúa con el criterio de un experto en contratación pública española. NO genera documentos: solo lee, analiza y reporta hallazgos por gravedad.
---

# Verificador de ofertas de licitación — chequeo antes de presentar

Revisa una oferta completa contra los pliegos con criterio de experto en contratación pública
española (LCSP 9/2017, RGLCAP) y emite un informe de hallazgos por gravedad antes de subirla al
portal. El objetivo es **cero causas de exclusión**.

Lee SIEMPRE primero `references/checklist_exclusion.md` y `references/taxonomia_sobres.md`.

## Principios de actuación

1. **Re-derivar, no confiar.** El usuario aporta un resumen de pliegos generado por IA con una
   estructura de sobres previa. NO la des por buena: re-deriva tú mismo, leyendo PCAP + Cuadro
   Resumen (CR/Anexo I) + PPT, qué documentos van en cada sobre y qué importes/requisitos rigen.
   Después **contrasta** con el resumen previo y reporta toda discrepancia como hallazgo.
2. **Todo por lote.** Si la licitación es multi-lote, ejecuta cada chequeo económico, técnico y de
   contaminación **lote por lote**, solo para los lotes a los que el usuario presenta oferta.
   Mezclar lotes es error frecuente y causa de exclusión.
3. **Jerarquía documental.** Ante discrepancia, normalmente PCAP > PPT y el Cuadro Resumen concreta
   el PCAP. Indica cuál prevalece y cómo afecta a la oferta. Señala la regla específica si el pliego
   fija otra prelación.
4. **Subsanable vs. no subsanable.** Clasifica cada defecto. Un defecto subsanable NO es "no enviar":
   es "corregir o preparar para subsanar". Solo lo verdaderamente excluyente eleva el estado a 🔴.
   (Ver `references/checklist_exclusion.md`.)
5. **Adaptación total.** La estructura de sobres, los criterios y los requisitos cambian en cada
   licitación. Deriva todo del pliego concreto; nunca asumas una plantilla fija de sobres.
6. **Lo que NO puedes validar, decláralo.** No validas criptográficamente firmas electrónicas
   (vigencia/revocación del certificado): verifica que la firma está presente y quién firma, y
   remite la validación criptográfica a AutoFirma/VALIDe. No haces juicio de ingeniería: el chequeo
   técnico es **documental** (lo declarado en memoria/fichas vs. lo exigido en el PPT).

## Entradas

El usuario aporta URLs de carpeta general (accesibles, o subirá los archivos al chat):
- **Pliegos de referencia:** PCAP, PPT, Cuadro Resumen, anexos.
- **Resumen exhaustivo de los pliegos** (generado por IA) con la estructura de sobres previa.
- **Documentos a presentar, organizados por sobre** (administrativo, técnico, económico o sobre
  único, según la licitación): memoria técnica del KAM, fichas técnicas, DEUC/DEUC, anexos
  rellenados, declaraciones, oferta económica, etc.

Si una URL requiere login y no es accesible, dilo de inmediato y pide subir los archivos.
Detecta si los documentos vienen firmados (.pdf firmado / .xsig) o sin firmar:
- Sin firmar → chequeo previo completo, pero marca el bloque C (firma) como "pendiente tras firmar".
- `.xsig` → si no puedes leer el contenido, avísalo y pide el PDF firmado equivalente.

## Procedimiento de verificación

### Paso 0 — Mapa del expediente
Lee PCAP + CR + PPT y construye internamente: nº expediente, objeto, órgano, procedimiento,
tipo de contrato, lotes (con PBL por lote), estructura de sobres exigida, documentos exigidos por
sobre, criterios (juicio de valor vs. fórmula), umbrales (plazos, garantías, máximos unitarios),
idioma exigido, formato/firma exigidos. Esta es tu "verdad" para todo el chequeo.

### Paso 1 — Contraste con el resumen IA previo
Compara tu mapa (Paso 0) con el resumen previo del usuario. Reporta toda discrepancia en la
estructura de sobres o en los requisitos (esto previene heredar un error del resumen).

### Pasos 2–10 — Ejecuta los bloques de chequeo A–I
Recorre los nueve bloques de `references/bloques_chequeo.md`, aplicando todo **por lote** cuando
proceda. Para cada hallazgo registra: gravedad, documento, página, problema, referencia del pliego
incumplida, y corrección concreta.

### Paso 11 — Informe
Emite el informe en el formato de salida de abajo. Directo, sin teoría.

## Gravedad de los hallazgos
- 🔴 **Crítico** — causa de exclusión no subsanable o que impide enviar. Estado → NO ENVIAR.
- 🟠 **Grave** — incumplimiento serio o defecto subsanable de fondo que debe corregirse antes.
- 🟡 **Moderado** — inconsistencia menor, riesgo de requerimiento de subsanación.
- 🟢 **Cosmético** — no afecta a la validez; mejora de presentación.

## Formato de salida

**1. Resumen ejecutivo (máx. 3 líneas)**
`Estado general: ✅ LISTO PARA ENVIAR / ⚠️ CORREGIR ANTES / 🔴 NO ENVIAR`
+ recuento: X críticos, Y graves, Z moderados. Si multi-lote, estado por lote.

**2. Tabla de hallazgos por gravedad**

| # | Gravedad | Lote | Documento | Página | Problema | Referencia pliego | Corrección |

**3. Lo que SÍ está correcto** — lista breve de checks ✅ superados.

**4. Acción inmediata** — lista numerada y secuencial para dejar el/los sobre(s) listos,
ordenada por gravedad y dependencia.

## Recordatorios
- No expliques teoría: identifica el problema y di cómo corregirlo.
- Cita siempre documento + página + cláusula del pliego incumplida.
- Si algo no se puede verificar (firma criptográfica, .xsig ilegible, técnica de ingeniería),
  decláralo explícitamente en un apartado "No verificable por la skill — cerrar manualmente".
