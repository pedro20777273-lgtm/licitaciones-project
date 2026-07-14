---
tipo: entidad
tags: [sistemas, oracle, plataformas, portales]
fuentes: [transversal]
actualizado: 2026-07-14
---

# Sistemas y plataformas del ecosistema

## Internos Hologic
| Sistema | Para qué | Skills que lo usan |
|---|---|---|
| **Oracle EBS** (OU: HOLX_IBR_OU) | Sales Orders, BSAs, modifiers, pending reason codes (attachment en CAPS por catálogo) | [PRQ Resolver](../skills/prq-resolver.md) |
| **GMC** (Global Management Console) | Registro de negociaciones/presupuestos; origen de quotes y BSAs | [quote BSH](../skills/quote-creation-bsh.md), [PRQ](../skills/prq-resolver.md) — ver [cadena GMC→quote→BSA](../conceptos/gmc-quote-bsa.md) |
| **Qlik** | Reporting de PRQs por reason code | PRQ (por eso los códigos no se inventan) |
| **Orbit Report** | 4 emails/día con pedidos en hold | PRQ (⚠️ muestra List Price, no Selling) |
| **H1 / Box** | Repositorio de quotes y contratos firmados | PRQ (buscar quote si no hay BSA) |
| **SharePoint/OneDrive** | Carpetas de skills y recursos (IBR con 200+ carpetas de BSAs) | Todas — ⚠️ URLs frágiles, ver [mejoras](../mejoras.md) |
| **GHX** | Portal EDI para recuperar POs | PRQ |
| **eubeosticket** | Ticketing non-EDI (credenciales FINANCE-SO, requiere VPN) | PRQ |
| **CDQ / EUCDQ** | Equipo de correcciones de datos/pricing (tickets OT…) | PRQ (⚠️ cierran tickets sin fix — reabrir con evidencia) |

## Públicos (licitaciones España)
| Sistema | Para qué | Skills |
|---|---|---|
| **PLACSP / perfiles del contratante** | Publicación de licitaciones y pliegos | [A2](../skills/analisis-pliegos.md) (input); detección = gap |
| **visor.registrodelicitadores.gob.es** | Importar/exportar y validar el [DEUC](../conceptos/deuc-espd.md) | [DEUC](../skills/deuc.md) |
| **ROLECE/ROLECSP** | Registro de licitadores (Hologic: nº 43522) | DEUC, [3.1](../skills/requerimientos-documentacion.md) |
| **AutoFirma / VALIDe** | Firma electrónica y validación criptográfica | [verificador](../skills/verificador-ofertas.md) (delega en ellos) |
| **Cajas de Depósitos CCAA / Estado** | Depósito de la [garantía definitiva](../conceptos/garantia-definitiva-aval.md) | [Check Aval](../skills/check-aval.md) |
