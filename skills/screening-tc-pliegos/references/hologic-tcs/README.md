# T&C de referencia Hologic — PENDIENTES DE CARGAR ⚠️

La skill A1 carga `hologic-tcs/{division}/{tipo_contrato}/terms.md`. **Ningún T&C está cargado
aún**: mientras tanto la skill clasifica el lado Hologic como ⚪ GRIS y puede extraer T&Cs de
quotes/contratos que se le suban.

## Estructura a poblar
```
hologic-tcs/
├── bsh/{suministro,servicio,mixto}/terms.md
├── dx/{suministro,servicio,mixto}/terms.md
└── gss/{suministro,servicio,mixto}/terms.md
```

## Formato de cada terms.md
```markdown
# Hologic T&C — [División] — [Tipo de contrato] — Iberia

## Payment Terms
- Plazo estándar de pago: [X] días desde fecha de factura
- Periodicidad de facturación: [mensual/trimestral/a la entrega]

## Service Commitments
- Tiempo de respuesta: [X] horas · Tiempo de resolución: [X] horas
- Mantenimiento preventivo: [frecuencia] · Uptime comprometido: [%]

## Penalties
- Tope de penalidades aceptado: [%] · ...

## Insurance / Liability
- RC estándar: [importe] · Límite de responsabilidad: [...]
```

Fuente sugerida: los T&C de la página 3+ de las quotes (skill quote-creation-bsh los preserva
intactos — "NUNCA TOCAR") y los contratos firmados de H1/Box.
