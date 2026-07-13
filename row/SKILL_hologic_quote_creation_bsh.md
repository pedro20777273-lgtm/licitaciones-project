# SKILL: hologic-quote-creation-bsh

## Descripción
Skill para generación automatizada de presupuestos (quotes) de Hologic Iberia — división BSH (Breast & Skeletal Health). Genera documentos .docx y .pdf a partir de datos GMC (Global Management Console) usando templates de KAM (Key Account Manager) específicos.

## Alcance
- **BSH Equipment Purchase** — Compra de equipos (DXA, mammography workstations, software)
- **BSH IBS Consumables** — Consumibles IBS (agujas Somatex, markers, canisters, sterile packs)
- **NO incluye**: Diagnostics (Cyto/Molecular) — eso es skill `hologic-quote-creation-dx` (pendiente)

---

## WORKFLOW OPERATIVO

### Paso 1: Analizar el GMC
Extraer del texto GMC:
- `GMC#` → Número de presupuesto
- `Sales Rep` → Identificar KAM y seleccionar template
- `BillTo Account name` → Nombre del cliente
- `Contact name` → Contacto (Sr./Sra./Dr.)
- `Contract start date` → Fecha del contrato
- `Address` → Dirección (si está vacía, preguntar)
- `Comments` → Comentarios KAM (pueden indicar Title, departamento, etc.)
- `Warranty` → Garantía (en la sección Instruments)
- `No Service contract at Point of Sale` → Si aparece, NO incluir fila "Servicio"
- `Instruments` / `Consumables` → Lista de ítems con precios
- `Other > Installation costs` → Costos internos, NO mostrar al cliente
- `FOC Box summary` → Ítems gratuitos (precio en blanco)

### Paso 2: Confirmar template
Decir: "Voy a usar template de [nombre KAM]" → ESPERAR confirmación del usuario.

### Paso 3: Informar comentarios KAM
Si hay Comments en el GMC, informar al usuario.

### Paso 4: Preguntar dirección
Si el campo Address está vacío en el GMC, preguntar dirección al usuario.

### Paso 5: Generar .docx + .pdf
Usar el workflow técnico descrito abajo.

### Paso 6: Trigger de correo
Si el usuario dice **"envía el correo"**, preparar email a pedro2777273@gmail.com con asunto `[GMC number] — [Cliente] — [Versión]` y archivo adjunto.

---

## TEMPLATES DISPONIBLES

### Equipment Purchase (4 columnas: Código | Descripción | Cantidad | Precio)

| KAM | Archivo template (.doc) | Bookmark IDs | Grid |
|-----|------------------------|-------------|------|
| María del Mar Coronado | `MARIA_DEL_MAR_CORONADO_MARTINEZ_QUOTE_EQUIPMENT_PURCHASE_ES_V2025-09_NEW_DRAFT___1_.doc` | id=2/3/4 | 1250→1800 / 2191→4187 / 3684→1100 / 2162→2200 |
| Alicia López Segura | `ALICIA_LOPEZ_SEGURA_QUOTE_EQUIPMENT_PURCHASE_ES_V2025-09_NEW_DRAFT_.doc` | id=2/3/4 | misma estructura MdM |
| Carlos Hernández | `Carlos_Hernández_QUOTE_EQUIPMENT_PURCHASE_ES_V2025-09_NEW_DRAFT___2_.doc` | id=2/3/4 | grid ya proporcional 1970/5325/943/1686, filas resumen preexistentes con "€" placeholder, fecha usa bCs no b |
| Marta García Menéndez | `MARTA_GARCIA_MENENDEZ_Hologic_Iberia_QUOTE_EQUIPMENT_PURCHASE_ES_V2025-09_NEW_DRAFT___1_.doc` | id=2/3/4 | misma estructura MdM |

### IBS Consumables (5 columnas: Código | Descripción | Precio | EAN | Presentación)

| KAM | Archivo template (.doc) | Bookmark IDs |
|-----|------------------------|-------------|
| Raquel Gubern | `RAQUEL_GUBERN_QUOTE-CONSUMABLES_PURCHASE_ES_V_2025-09_IBS_CONSUMABLES_NEW_DRAFT____1_.doc` | id=0/1/2 |
| Miriam Villanueva | `MIRIAM_VILLANUEVA_Hologic_Iberia_QUOTE-CONSUMABLES_IBS_NEEDLES_PURCHASE_ES_V5_0.doc` | id=0/1/2, tiene 2 secciones OPCIONAL |

### Excel EAN
`CODIGOS_EAN_BREAST__1_.xlsx` — Sheet "Base": columnas PRODUCTO (A), REFERENCIA (B), CODIGO EAN (C), UDS POR CAJA (D)

---

## REGLAS BSH — EQUIPMENT PURCHASE (NO NEGOCIABLES)

### Tabla de productos
1. **NUNCA precios individuales por equipo** → solo Total. EXCEPCIÓN: si el KAM lo pide explícitamente en Comments del GMC
2. **3 filas resumen**: Subtotal (sin IVA) + IVA 21% + TOTAL (IVA incluido)
3. **FOC a 0€** → precio en **blanco** (no escribir "0" ni "0,00 €")
4. **Excluir ítems GMC_** → los que empiezan con GMC_ son internos
5. **Installation costs** del GMC = interno, **NO mostrar** al cliente
6. **Columnas proporcionales**: Descripción ancha, Cantidad estrecha
   - Grid recomendado: 1800 / 4187 / 1100 / 2200

### Template Carlos Hernández — ESPECIAL
- Grid ya proporcional (no cambiar): 1970/5325/943/1686
- Filas resumen **preexistentes** ("Total sin IVA"/"IVA 21%"/"Total con IVA" con "€" placeholder)
- Solo rellenar el "€" con el valor real — **NO crear filas nuevas**
- Fecha usa `bCs` en vez de `b` — no poner negrita
- **Preservar encabezados azules** (shd fill="B8CCE4")

### Campos del documento
7. **Garantía** → SIEMPRE del GMC (campo Warranty), nunca default template
8. **Contacto** → Sr./Sra. según género; "Dr." si aparece así; "Estimado cliente" si no hay contacto
9. **Sin gap contacto-cliente** → eliminar párrafo Title si está vacío
10. **Comentario KAM "Departamento de..."** → poner en campo Title
11. **Comentario KAM "Suministros"** → poner en campo Title
12. **Ship To en blanco** si = Bill To
13. **Fecha** → SIN negrita, Calibri 10, formato DD/MM/YYYY
14. **"Dirección de entrega"** → **SIEMPRE ELIMINAR** del quote (el label subrayado/sombreado)
15. **Resaltado amarillo** → **SIEMPRE ELIMINAR** del párrafo de aceptación
16. **Fila "Servicio"** → **ELIMINAR** si "No Service contract at Point of Sale"
17. **T&C** (Términos y condiciones) y todo después de página 2 → **NUNCA TOCAR**

### Condiciones adicionales (dentro del recuadro)
18. Reemplazar [OPCIONAL] con bullets reales (usar numId=7 del template):
    - Validez de la Oferta: 30 días
    - Condiciones de Garantía: X (texto) años ← del GMC
    - Plazo de Entrega: según disponibilidad de los equipos.
    - Entrega llave en mano, incluyendo Instalación, Funcionamiento y Entrenamiento de Operadores.
    - Forma de pago: A la Entrega y Puesta en Servicio de los equipos

### REF Fields y Headers
19. **REF fields**: actualizar texto en **TODOS** los XML (header1.xml + body "Para aceptación")
20. **Bookmark `customername`** debe **ENVOLVER** el texto (bookmarkStart antes, bookmarkEnd después)
21. **Header** (header1.xml): reemplazar tanto Customer Name como Quotation log number

### Archivo de salida
22. Nombre: `[GMC]_[Cliente]_V0.docx` (sin caracteres especiales, "/" → "-")

---

## REGLAS BSH — IBS CONSUMABLES (NO NEGOCIABLES)

### Tabla de productos (5 columnas)
1. **Código del producto** | **Descripción** | **Precio de Oferta** | **Código EAN** | **Presentación**
2. **NO poner Subtotal/IVA/Total** — nunca filas de resumen
3. **Buscar EAN** en Excel CODIGOS_EAN_BREAST por referencia del ítem
4. **Presentación** = "Caja de X uds" (con "uds", no solo número) — X viene de columna UDS POR CAJA del Excel
5. **Mantener fila encabezados azul** (shd fill="B8CCE4")
6. **"Estimado cliente"** si no hay contacto
7. **Fecha contrato** del GMC en cláusula: "El plazo del contrato comienza el [fecha en texto] de [año] y tiene una duración mínima de 12 meses."
8. **"Dirección de entrega"** → SIEMPRE ELIMINAR (misma regla que Equipment)
9. Mismas reglas de contacto, Ship To, bookmark, REF fields que Equipment

---

## REGLAS DX (DIAGNOSTICS) — Referencia futura

- **Precio de oferta** debe mostrar **AMBOS** valores: precio por test/unidad (ej. "15,40 € /Test") Y precio por pack (ej. "1.540,00€/pack")
- **Datos internos** del GMC como gastos de etiquetas (-100€) o installation costs **NO se muestran** al cliente
- Referencia visual: quote Cyto Sant Joan de Déu (GMC.ES.Cyto.Q.26.035303)
- **Pendiente crear skill DX completa** con templates de KAMs DX (Mónica Martínez, etc.)

---

## WORKFLOW TÉCNICO

### 1. Convertir template .doc → .docx
```bash
python scripts/office/soffice.py --headless --convert-to docx template.doc
```

### 2. Desempaquetar (unpack)
```bash
python scripts/office/unpack.py template.docx unpacked_dir/
```

### 3. Editar XML
Archivo principal: `unpacked_dir/word/document.xml`
Header: `unpacked_dir/word/header1.xml`

Operaciones típicas con Python string replace:
- Reemplazar placeholders (`<Customer Name>`, `<Address Line>`, `<Quotation log number>`, `<Date of quote issuance>`, `<nombre del contacto>`)
- Insertar filas de tabla (data rows + summary rows)
- Eliminar párrafos (Dirección de entrega, Title vacío)
- Eliminar highlights (`<w:highlight w:val="yellow"/>`)
- Eliminar filas (Servicio)
- Actualizar REF fields en header1.xml

### 4. Reempaquetar (pack)
```bash
python scripts/office/pack.py unpacked_dir/ output.docx --original template.docx --validate false
```

### 5. Convertir a PDF
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
```

### 6. Preview (verificación visual)
```bash
pdftoppm -jpeg -r 200 -f 1 -l 2 output.pdf preview
```

### 7. Copiar a outputs
```bash
cp output.docx /mnt/user-data/outputs/
cp output.pdf /mnt/user-data/outputs/
```

---

## PATRONES XML CLAVE

### Bookmark customername (CORRECTO — envolviendo texto)
```xml
<w:bookmarkStart w:id="2" w:name="customername"/>
<w:r>
  <w:rPr>...</w:rPr>
  <w:t>NOMBRE DEL CLIENTE</w:t>
</w:r>
<w:bookmarkEnd w:id="2"/>
```

### Fila de datos Equipment (sin precio individual)
```xml
<w:tr>
  <w:trPr><w:trHeight w:val="275" w:hRule="atLeast"/></w:trPr>
  <!-- 4 celdas: código, descripción, cantidad "1", precio " " (vacío) -->
</w:tr>
```

### Fila de resumen Equipment
```xml
<w:tr>
  <w:trPr>...</w:trPr>
  <w:tc>
    <w:tcPr><w:tcW w:w="7087" w:type="dxa"/><w:gridSpan w:val="3"/>...</w:tcPr>
    <!-- Label alineado a la derecha -->
    <w:t>Subtotal (sin IVA)</w:t>
  </w:tc>
  <w:tc>
    <!-- Valor -->
    <w:t>55.050,00 €</w:t>
  </w:tc>
</w:tr>
```

### Fila de datos IBS Consumables
```xml
<w:tr>
  <w:trPr/>
  <!-- 5 celdas: código(1271), descripción(2189), precio(1958), EAN(1951), presentación(1867) -->
</w:tr>
```

### Bullet de condiciones (numId=7 para Marta, verificar en otros templates)
```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Normal"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="7"/></w:numPr>
    ...
  </w:pPr>
  <w:r>
    <w:rPr>...</w:rPr>
    <w:t>Validez de la Oferta: 30 días</w:t>
  </w:r>
</w:p>
```

### Fecha SIN negrita (quitar `<w:b/>`)
```xml
<w:r>
  <w:rPr>
    <w:rFonts w:eastAsia="Times New Roman" w:cs="Arial"/>
    <!-- NO w:b/ aquí -->
    <w:sz w:val="20"/>
    <w:szCs w:val="20"/>
    <w:lang w:val="es-ES_tradnl"/>
  </w:rPr>
  <w:t>19/03/2026</w:t>
</w:r>
```

---

## CHECKLIST DE VERIFICACIÓN (post-generación)

Antes de entregar el quote, verificar visualmente en el PDF:

- [ ] Nombre del cliente correcto en encabezado izquierdo
- [ ] GMC number correcto en encabezado derecho
- [ ] Fecha sin negrita
- [ ] Contacto con Sr./Sra./Dr. correcto (o "Estimado cliente")
- [ ] Dirección correcta
- [ ] NO aparece "Dirección de entrega"
- [ ] NO aparece resaltado amarillo
- [ ] Tabla con ítems correctos
- [ ] Sin precios individuales (Equipment) o sin totales (IBS)
- [ ] FOC con precio en blanco
- [ ] Subtotal/IVA/Total correctos (Equipment)
- [ ] EAN y Presentación correctos (IBS)
- [ ] Condiciones adicionales con bullets (Validez, Garantía, etc.)
- [ ] Sin fila "Servicio" si no hay service contract
- [ ] Headers en página 2+ con Cliente + GMC
- [ ] "Para aceptación" con nombre del cliente
- [ ] T&C intactos
- [ ] KAM nombre/email/teléfono correctos

---

## QUOTES GENERADOS (HISTÓRICO DE REFERENCIA)

### Equipment Purchase
| GMC | Cliente | KAM | Ítems | Total |
|-----|---------|-----|-------|-------|
| GMC.ES.BH.Q.26.034658 | Centre de Diagnosi per la Imatge | Alicia López | 2 tablas | — |
| GMC.ES.BH.Q.26.035263 | H. Tomelloso | Carlos Hernández | 2 (precios individuales por excepción KAM) | 14.762,00 € |
| GMC.ES.Sk/BH.Q.26.035250 | Athletic Club de Bilbao | Marta | 3 (Horizon-W+Iris+FOC) | 66.610,50 € |
| GMC.ES.Sk/BH.Q.26.035251 | Athletic Club de Bilbao | Marta | 4 (Horizon-WI+Iris+IVA-I+FOC) | 53.300,50 € |
| GMC.ES.Sk/BH.Q.26.035252 | Athletic Club de Bilbao | Marta | 3 (Horizon-A+Iris+FOC) | 81.142,60 € |
| GMC.ES.Sk.Q.26.035313 | Universidad de Granada IMUDs | MdM | 3 (Horizon-W+TBS+FOC) | 62.883,70 € |
| GMC.ES.Sk.Q.26.035312 | Universidad de Granada IMUDs | MdM | 3 (Horizon-WI+TBS+FOC) | 60.463,70 € |
| GMC.ES.BH.Q.26.035336 | Servicio cántabro de salud | Marta | 2 (SecurView DX400+FOC) | 40.535,00 € |

### IBS Consumables
| GMC | Cliente | KAM | Ítems |
|-----|---------|-----|-------|
| GMC.ES.BH.Q.26.035070 | Hospital d'Olot | Raquel | 4 agujas Somatex |
| GMC.ES.BH.Q.26.035095 | Consorcio Sanitario Anoia | Raquel | 10 |
| GMC.ES.BH.Q.26.035097 | Consorci Sanitari Terrassa | Raquel | 8 |
| GMC.ES.BH.Q.26.035094 | Hospital HLA Inmaculada Granada | Miriam | 10 |
| GMC.ES.BH.Q.26.035222 | Hospital de Mérida | Miriam | 5 |
| GMC.ES.BH.Q.26.035311 | R.M. Y T.C. Nuestra Señora del Rosario | Miriam | 11 |
| GMC.ES.BH.Q.26.035260 | HM Hospitales | Miriam | 4 sterile packs |
| GMC.ES.BH.Q.26.035406 | Hospital Univ. de Cuenca | Miriam | 10 (URGENTE) |
| GMC.ES.BH.Q.26.035391 | Hospital Univ. Virgen Macarena | Miriam | 2 TUMARK |

---

## ERRORES COMUNES Y SOLUCIONES

| Error | Causa | Solución |
|-------|-------|----------|
| Condiciones adicionales vacías | Se blanqueó [OPCIONAL] en vez de reemplazar con bullets | Reemplazar contenido del `<w:p>` dentro de la celda con 5 párrafos bullet (numId=7) |
| "Total sin IVA" duplicado | Se crearon filas de resumen nuevas en template Carlos que ya las tenía | En Carlos, solo rellenar "€" placeholder con valor — NO crear filas nuevas |
| Encabezado azul borrado | Se reemplazó toda la tabla incluyendo header row | Preservar header row (shd fill="B8CCE4") — solo reemplazar data rows |
| Bookmark no funciona | bookmarkEnd antes del texto | bookmarkStart → texto → bookmarkEnd (envolver) |
| Header sin cliente | No se actualizó header1.xml | SIEMPRE actualizar header1.xml con Customer Name y Quotation log number |
| Fecha en negrita | Se copió el `<w:b/>` del placeholder | Omitir `<w:b/>` en el run de la fecha |
| "Dirección de entrega" visible | No se eliminó el párrafo | Eliminar el `<w:p>` completo que contiene "Dirección de entrega" |

---

*Skill creado por Pedro — Hologic Iberia BSH Quote Automation — v1.0 — Marzo 2026*
