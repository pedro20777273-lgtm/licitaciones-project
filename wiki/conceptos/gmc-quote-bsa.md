---
tipo: concepto
tags: [gmc, quote, bsa, oracle, cadena-de-precio]
fuentes: [row/SKILL_hologic_quote_creation_bsh.md, row/Order_Management/ (KB y logs)]
actualizado: 2026-07-14
---

# GMC → Quote → BSA: la cadena de custodia del precio

El concepto que une las dos mitades del trabajo de Pedro. Un precio nace en una negociación y debe
llegar intacto hasta la factura. Cada eslabón donde se rompe genera una categoría de PRQ.

```
KAM negocia → GMC (Global Management Console) → Quote firmada (.docx generada por skill)
   → carga en Oracle como BSA o Standalone Modifier → el PO del cliente dispara ese precio
   → booking → factura
```

## Reglas de la cadena
1. **La quote firmada es la fuente SUPREMA de verdad del precio.** Si Oracle no coincide con la
   quote, el error es de carga del BSA (PTWP), no del cliente.
2. El **GMC** identifica la negociación (formato `GMC.ES.<división>.Q.<año>.<número>`, ej.
   `GMC.ES.Cyto.Q.26.036844`) y es la referencia que cruza emails, BSAs, quotes y tickets.
3. Del GMC sale la quote ([skill quote BSH](../skills/quote-creation-bsh.md)); de la quote sale el
   BSA ([BSA vs Standalone](bsa-vs-standalone.md)); del BSA sale el precio del pedido
   ([PRQ Resolver](../skills/prq-resolver.md)).

## Dónde se rompe la cadena (evidencia de los logs de semana 28)
| Rotura | Reason code | Ejemplo real |
|---|---|---|
| Quote emitida pero BSA nunca cargado | PTNP | CPC Granada: GMC.ES.Cyto.T.26.037336 pendiente desde 30/06 |
| BSA cargado con precio erróneo | PTWP | Maresme: BSA 3124409 con sospecha de error unit/pack (ratios 5x y 2,5x) |
| BSA vigente que no dispara (mapping) | PTBA | Quirón/IDCQ: ShipTos sin mapear tras migración de cuenta |
| Contrato expirado sin renovar | SEC | Candelaria: prórroga vencida marzo/2026, KAM sin emitir GMC nuevo |
| Cliente usa precio viejo | CWPP | — |

## Implicación
Automatizar el eslabón **quote → BSA** (verificación de carga contra la quote) y un **radar de
expiración** de BSAs eliminaría la mayoría de PRQs de origen interno. Propuesto en
[mejoras](../mejoras.md).
