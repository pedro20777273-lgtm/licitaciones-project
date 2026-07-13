# SKILL CHECK AVAL — Verificación de Avales Bancarios v1.0

**Autor:** Pedro Moronta — Tender Specialist — Hologic Iberia, S.L.U.
**Fecha creación:** 16/06/2026
**Última actualización:** 16/06/2026

---

## 1. OBJETIVO

Esta skill permite:
1. **Verificar PALABRA POR PALABRA** que un borrador de aval bancario se ajusta al modelo oficial de aval de la Comunidad Autónoma (CCAA) correspondiente.
2. **Cruzar todos los datos** del aval con los del requerimiento/PCAP del expediente de contratación.
3. **Detectar y clasificar discrepancias** (BLOQUEANTE / MENOR / COSMÉTICA).
4. **Generar un email profesional** de consulta/envío para el bastanteo y depósito de la garantía ante el Servicio Jurídico y Caja de Depósitos de la CCAA.

> ⚠️ **Esta skill es aplicable a CUALQUIER Comunidad Autónoma de España**, no solo a Canarias.

---

## 2. DATOS FIJOS DE HOLOGIC (para cruce automático)

| Dato | Valor |
|:--|:--|
| **Razón social** | HOLOGIC IBERIA, S.L.U. |
| **Nota razón social** | ⚠️ En algunos expedientes y registros puede figurar como "S.L." en lugar de "S.L.U." — **verificar siempre** cuál usa el órgano de contratación y cuál tiene el banco |
| **CIF** | B83279331 |
| **Domicilio** | C/ Arequipa nº 1, Esc. 2, 3º — 28043 Madrid |
| **Email concursos** | concursos@hologic.com |
| **Teléfono** | +34 91 344 6990 / +34 616 424 922 |

---

## 3. RECURSOS QUE DEBE CONTENER LA CARPETA DE LA SKILL

Estructura de carpeta recomendada:

```
📁 SKILL_CHECK_AVAL/
│
├── 📄 SKILL_CHECK_AVAL_v1.md              ← (este archivo)
├── 📄 PROMPT_INVOCACION_CHECK_AVAL.md     ← prompt para activar la skill
├── 📄 ERRORES_SKILL_CHECK_AVAL.md         ← log de errores (se va actualizando)
├── 📄 CONTACTOS_BASTANTEO.md              ← contactos por CCAA para bastanteo/depósito
│
├── 📁 Modelos_Oficiales_CCAA/             ← modelos oficiales de aval por CCAA
│   ├── Modelo_Canarias_BOC182_2018.pdf
│   ├── Modelo_Andalucia.pdf
│   ├── Modelo_Madrid.pdf
│   ├── Modelo_Cataluña.pdf
│   ├── Modelo_Valencia.pdf
│   ├── Modelo_PaisVasco.pdf
│   ├── Modelo_Aragon.pdf
│   ├── Modelo_Navarra.pdf
│   ├── Modelo_CastillaLaMancha.pdf
│   ├── Modelo_CastillaYLeon.pdf
│   ├── Modelo_Galicia.pdf
│   ├── Modelo_Murcia.pdf
│   ├── Modelo_Extremadura.pdf
│   ├── Modelo_Baleares.pdf
│   ├── Modelo_Asturias.pdf
│   ├── Modelo_Cantabria.pdf
│   ├── Modelo_LaRioja.pdf
│   └── (ir añadiendo según se necesiten)
│
└── 📁 Contactos_Bastanteo_CCAA/
    └── CONTACTOS_BASTANTEO.md
```

> 📌 **IMPORTANTE:** Si al ejecutar la skill no se encuentra el modelo oficial de la CCAA en la carpeta, se DEBE AVISAR al usuario para que lo descargue del BOE/BOC/BOJA/DOGV correspondiente y lo añada antes de continuar.

---

## 4. PROCEDIMIENTO DE VERIFICACIÓN (PASO A PASO)

### Paso 4.1 — LECTURA DE INPUTS

Leer los **3 documentos OBLIGATORIOS**:

| # | Documento | Fuente |
|:--|:--|:--|
| A | **Borrador del aval** (PDF emitido por el banco) | Adjuntado por el usuario o URL |
| B | **Modelo oficial de la CCAA** | Subcarpeta `Modelos_Oficiales_CCAA/` |
| C | **Requerimiento del expediente o PCAP** (cláusula de garantía definitiva) | Adjuntado por el usuario o URL |

Si falta alguno de los 3, **DETENER la ejecución** e indicar al usuario qué falta.

---

### Paso 4.2 — IDENTIFICAR LA CCAA Y MODELO APLICABLE

1. Leer el requerimiento para identificar el **órgano de contratación** y su **Comunidad Autónoma**.
2. Cargar el **modelo oficial** correspondiente de la subcarpeta.
3. Si el modelo NO está en la carpeta:
   - ❌ AVISAR: *"No se ha encontrado el modelo oficial de [CCAA] en la carpeta. Descárgalo e inclúyelo antes de continuar."*
   - Proporcionar pista de dónde buscarlo (ej: BOC, BOJA, DOGV, etc.).
4. Identificar si el impuesto aplicable es **IVA** (península/Baleares) o **IGIC** (Canarias).

---

### Paso 4.3 — VERIFICACIÓN CAMPO POR CAMPO

Verificar los siguientes **13 campos**, uno por uno, comparando borrador vs modelo vs requerimiento:

| Campo | Qué verificar | Dónde cruzar |
|:--|:--|:--|
| **(1) Entidad avalista** | Razón social completa, NIF, domicilio social, sucursal | Modelo: campo (1) |
| **(2) Apoderados del banco** | Nombre completo, DNI de cada apoderado | Modelo: campo (2) |
| **(3) Cláusula de poderes** | Debe referenciar la normativa de la CCAA correspondiente (Decreto, Reglamento, BOC/BOJA, etc.). NO puede referenciar normativa de otra CCAA | Modelo: párrafo introductorio |
| **(4) Normativa aplicable** | Art. 107 y ss. Ley 9/2017 LCSP + RD 1098/2001 (u otra que indique el pliego) | Modelo: campo (4) + Requerimiento |
| **(5) Obligación garantizada** | Debe coincidir con el **objeto exacto del contrato** del requerimiento. Verificar si incluye el **LOTE específico** adjudicado. | Modelo: campo (5) + Requerimiento |
| **(6) Beneficiario** | Nombre completo del órgano (Consejería, DG, Servicio de Salud, etc.) + NIF | Modelo: campo (6) + Requerimiento |
| **(7) Importe** | En **cifra y en letra**. Verificar que = 5% × precio adjudicado sin impuestos (IVA/IGIC). Cálculo: `Garantía = Importe adjudicado sin impuestos × 0,05` | Modelo: campo (7) + Requerimiento |
| **(8) Solidaridad + primer requerimiento** | Debe incluir renuncia a beneficios de orden, división y excusión. Indicar ante quién se obliga al pago (Caja de Depósitos de la CCAA o del Estado) | Modelo: campo (8) |
| **(9) Validez** | Normalmente **INDEFINIDA** para garantías definitivas en contratos públicos | Modelo: campo (9) + Requerimiento |
| **(10) Carácter ejecutivo** | Frase estándar sobre Reglamento General de Recaudación | Modelo |
| **(11) Registro Especial de Avales** | Número de inscripción completo | Modelo: campo (10) |
| **(12) Verificación de representación** | Provincia, fecha, nº o código del bastanteo previo de poderes del banco | Modelo: sección inferior |
| **(13) Bastanteo** | Sección que **DEBE estar en blanco** (a cumplimentar por el Servicio Jurídico) | Modelo: sección inferior |

---

### Paso 4.4 — VERIFICACIÓN TEXTUAL LITERAL

Comparar **FRASE POR FRASE** el borrador del aval con el modelo oficial:

1. Copiar cada párrafo del modelo.
2. Comparar con el párrafo equivalente del borrador.
3. Señalar **CUALQUIER diferencia**, por mínima que sea.
4. Clasificar cada diferencia:

| Clasificación | Significado | Ejemplos |
|:--|:--|:--|
| 🔴 **BLOQUEANTE** | Error que impide el bastanteo o invalida el aval | NIF incorrecto, importe erróneo, beneficiario equivocado, normativa de otra CCAA, falta cláusula obligatoria |
| 🟡 **MENOR** | No debería impedir el bastanteo, pero conviene confirmar | S.L. vs S.L.U., falta especificar lote, ligera variación en redacción de la obligación |
| ⚪ **COSMÉTICA** | Diferencia sin impacto jurídico | "Así mismo" vs "Asimismo", espacios extra, mayúsculas/minúsculas, formato de fecha |

---

### Paso 4.5 — CRUCE CON REQUERIMIENTO

Verificar los siguientes datos cruzando borrador del aval ↔ requerimiento/PCAP:

| Dato | Aval dice… | Requerimiento dice… | ¿Coincide? |
|:--|:--|:--|:--|
| Razón social avalado | (extraer) | (extraer) | ✅/⚠️/❌ |
| CIF avalado | (extraer) | (extraer) | ✅/⚠️/❌ |
| Nº expediente (completo) | (extraer) | (extraer) | ✅/⚠️/❌ |
| Objeto del contrato | (extraer) | (extraer) | ✅/⚠️/❌ |
| Lote adjudicado | (extraer) | (extraer) | ✅/⚠️/❌ |
| Importe garantía (€) | (extraer) | (extraer: 5% × adjudicación s/impuestos) | ✅/⚠️/❌ |
| Importe en letra | (extraer) | (verificar coherencia con cifra) | ✅/⚠️/❌ |
| Órgano beneficiario | (extraer) | (extraer) | ✅/⚠️/❌ |
| NIF beneficiario | (extraer) | (extraer) | ✅/⚠️/❌ |

---

### Paso 4.6 — TABLA RESUMEN DE VERIFICACIÓN

Generar una tabla consolidada con formato:

| # | Campo | Borrador del aval | Modelo oficial / Requerimiento | Veredicto |
|:--|:--|:--|:--|:--|
| 1 | Entidad avalista | … | … | ✅ / ⚠️ / ❌ |
| 2 | Apoderados | … | … | ✅ / ⚠️ / ❌ |
| … | … | … | … | … |
| 13 | Bastanteo (en blanco) | … | … | ✅ / ⚠️ / ❌ |

---

### Paso 4.7 — LISTA DE OBSERVACIONES

Generar lista numerada de todas las discrepancias:

```
### OBSERVACIONES

| # | Clasificación | Campo | Descripción | Acción recomendada |
|:--|:--|:--|:--|:--|
| 1 | 🔴 BLOQUEANTE | … | … | … |
| 2 | 🟡 MENOR | … | … | … |
| 3 | ⚪ COSMÉTICA | … | … | … |
```

---

### Paso 4.8 — VEREDICTO GLOBAL

Emitir uno de los 3 veredictos:

| Veredicto | Significado |
|:--|:--|
| 🟢 **CORRECTO** | El aval se ajusta al modelo y al requerimiento sin observaciones |
| 🟡 **CORRECTO CON OBSERVACIONES** | El aval es sustancialmente correcto pero tiene observaciones menores que conviene confirmar |
| 🔴 **ERRORES BLOQUEANTES** | El aval tiene errores que impiden el bastanteo. Se debe corregir y regenerar |

---

## 5. GENERACIÓN DE EMAIL

### Paso 5.1 — Buscar contactos

Consultar el archivo `CONTACTOS_BASTANTEO.md` para obtener:
- Email del Servicio Jurídico de la CCAA
- Email de la Caja de Depósitos de la CCAA
- Teléfono de contacto

Si no hay contacto registrado para esa CCAA: **AVISAR** para que se investigue y se añada.

### Paso 5.2 — Generar email

Estructura del email:

```
Para: [email servicio jurídico] ; [email caja depósitos]
CC: concursos@hologic.com
Asunto: Solicitud de bastanteo de aval — Expte. [Nº expediente] — [Lote X]

---

Estimados,

[Párrafo 1: contexto del expediente — nº, objeto, adjudicación lote X]

[Párrafo 2: se adjunta borrador de aval por importe de X € emitido por [banco], nº inscripción [nº], para su revisión y bastanteo]

[Párrafo 3: SI HAY OBSERVACIONES — mencionarlas explícitamente y pedir confirmación]

[Párrafo 4: plazo del requerimiento — fecha límite]

[Párrafo 5: datos de contacto Hologic]

Reciban un cordial saludo,

Pedro Moronta
Tender Specialist
HOLOGIC IBERIA, S.L.U.
C/ Arequipa nº 1, Esc. 2, 3º — 28043 Madrid
concursos@hologic.com | +34 91 344 6990

---

Adjunto: Borrador aval [banco] — Expte. [Nº]
```

### Paso 5.3 — Preguntas explícitas

Si hay observaciones sobre datos críticos (ej: S.L. vs S.L.U., falta de lote en el texto, etc.), **incluir pregunta explícita** en el email para que el Servicio Jurídico confirme antes de finalizar el bastanteo.

---

## 6. REGLAS GENERALES

1. **NUNCA inventar datos.** Si falta un modelo, un contacto o un documento, DECIRLO.
2. **SIEMPRE leer el log de errores** (`ERRORES_SKILL_CHECK_AVAL.md`) antes de ejecutar.
3. **SIEMPRE verificar PALABRA POR PALABRA**, nunca resúmenes.
4. El **impuesto** puede ser **IVA** (península/Baleares) o **IGIC** (Canarias) — **calcular correctamente el 5%** sobre el importe SIN impuestos.
5. La **Caja de Depósitos** puede ser:
   - La de la propia CCAA (ej: Canarias, Andalucía, Cataluña, Madrid, Valencia…)
   - La **Caja General de Depósitos del Estado** (para CCAA que no tienen caja propia)
6. Verificar **siempre** si el bastanteo es obligatorio según el pliego/PCAP.
7. Si el órgano beneficiario **es un departamento** (no una persona), el saludo del email debe ser **"Estimados,"** sin mención al departamento.
8. Respetar **exactamente** el formato, estilo y estructura de esta skill.
9. Cuando el banco emite el aval con firma electrónica, verificar que la sección de bastanteo está **vacía** (la rellena el Servicio Jurídico, no el banco).
10. Si el borrador ya tiene alguna sección del modelo rellenada que debería estar en blanco → ❌ SEÑALAR.

---

## 7. LOG DE ERRORES

Referencia: leer siempre `ERRORES_SKILL_CHECK_AVAL.md` antes de ejecutar. Actualizar tras cada error detectado o tras cada ejecución que revele algo nuevo que deba tenerse en cuenta en futuras verificaciones.

---

## 8. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|:--|:--|:--|
| 1.0 | 16/06/2026 | Creación inicial basada en verificación real del aval del Expte. 23/S/25/SU/DG/A/AM35 (SCS Canarias) |

---

*Fin de la skill.*
