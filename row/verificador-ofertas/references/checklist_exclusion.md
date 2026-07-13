# Causas de exclusión y defectos subsanables vs. no subsanables (LCSP 9/2017)

Criterio de experto para clasificar la gravedad de cada hallazgo. La distinción
subsanable / no subsanable es la más importante: evita alarmar de más (un defecto subsanable
NO es "no enviar") y evita confiar de más (un defecto no subsanable SÍ es exclusión).

## Principio general (art. 141 LCSP y doctrina de los Tribunales de Recursos Contractuales)
- Es **subsanable** el defecto **formal** o de **acreditación** de un requisito que **ya se cumplía**
  en plazo (p. ej. falta una firma, falta un sello, no se adjuntó un certificado que existe). El
  órgano concede normalmente 3 días hábiles para subsanar.
- Es **NO subsanable** lo que afecta al **fondo** de la oferta o a un requisito **inexistente** al
  cierre del plazo: modificar el precio, completar una oferta técnica incompleta, aportar una
  solvencia de la que se carecía, o cualquier cosa que altere la igualdad de licitadores.

## NO SUBSANABLE → 🔴 (NO ENVIAR / exclusión segura)
- **Precio que supera el PBL** (total o de un lote al que se licita). Exclusión automática.
- **Precio unitario que supera el máximo unitario** fijado en el pliego.
- **Oferta económica fuera del modelo/Anexo obligatorio** cuando el pliego lo impone como esencial,
  o con el importe en blanco.
- **Incumplimiento de una prescripción técnica MÍNIMA del PPT** (no es mejorable: o se cumple o se
  excluye).
- **Contaminación de sobre** que revela la oferta económica en el sobre técnico de juicio de valor
  (rompe el secreto de la evaluación → exclusión). Ver `taxonomia_sobres.md`.
- **Plazo de entrega/ejecución o garantía ofertados por debajo del mínimo** exigido.
- **Falta de un documento esencial de la oferta** cuyo contenido no puede aportarse después sin
  alterar la oferta (memoria técnica inexistente, no la incompleta-formal).
- **Condiciones especiales de ejecución o requisitos de obligado cumplimiento** declarados no
  asumidos.

## SUBSANABLE → 🟠 / 🟡 (corregir antes; si se escapa, se requerirá subsanación)
- Falta de **firma** en un documento, o firmante que se acredita después.
- **DEUC** mal cumplimentado o no aportado, siendo subsanable la mera acreditación.
- Falta de un **certificado** (AEAT, SS, ROLECE) que existe y solo no se adjuntó.
- **Errores materiales aritméticos** evidentes y coherentes con el resto (no los que cambian el
  precio ofertado).
- **Domicilio/CIF/razón social** con error tipográfico evidente y subsanable.
- Falta de **traducción jurada** de un catálogo cuando se exige (subsanable aportándola).
- **Paginación, índice o sello** ausentes.

## ZONA GRIS (juzgar según pliego y doctrina) → marcar 🟠 y advertir
- Mejora ofertada redactada como "declaración de intenciones" no verificable: puede no puntuar o,
  si es criterio de admisión, excluir.
- Información marcada (o no) como confidencial con contradicciones internas.
- Discrepancia PCAP/PPT/CR: aplicar prelación (PCAP > PPT; CR concreta) e indicar efecto.

## Regla de oro para el estado general
- Cualquier hallazgo 🔴 → estado **🔴 NO ENVIAR** (de ese lote).
- Solo hallazgos 🟠/🟡 → **⚠️ CORREGIR ANTES**.
- Solo 🟢 o ninguno → **✅ LISTO PARA ENVIAR**.
