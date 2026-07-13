**Versión:** 1.5 (final con catálogos completos) **Fecha:** 20/06/2026

📌 **3 URLs integradas.** Solo rellena Nº de cuenta + adjunta pantallazos.

## ✂️ COPY-PASTE PROMPT

Skill PRQ Resolver:  
[https://hologic-my.sharepoint.com/:f:/r/personal/pedro\_moronta\_hologic\_com/Documents/Habilidades%20Order%20Management/PRQ%20RESOLVER%20(URL%20CON%20CONOCIMIENTOS)?csf=1&web=1&e=gqbCNt](https://hologic-my.sharepoint.com/:f:/r/personal/pedro_moronta_hologic_com/Documents/Habilidades%20Order%20Management/PRQ%20RESOLVER%20\(URL%20CON%20CONOCIMIENTOS\)?csf=1&web=1&e=gqbCNt)  
  
Recursos (manual + reason codes + catálogos Breast/Surgical/Diagnostics + BSA rules):  
[https://hologic-my.sharepoint.com/:f:/r/personal/pedro\_moronta\_hologic\_com/Documents/Habilidades%20Order%20Management/PRQ%20RECURSOS?csf=1&web=1&e=v3YQxt](https://hologic-my.sharepoint.com/:f:/r/personal/pedro_moronta_hologic_com/Documents/Habilidades%20Order%20Management/PRQ%20RECURSOS?csf=1&web=1&e=v3YQxt)  
  
BSAs (IBR):  
[https://hologic.sharepoint.com/:f:/r/sites/commercialcontractsandtendersemea/Shared%20Documents/General/Iberia/Tenders/Test/IBR?csf=1&web=1&e=SfZn7E](https://hologic.sharepoint.com/:f:/r/sites/commercialcontractsandtendersemea/Shared%20Documents/General/Iberia/Tenders/Test/IBR?csf=1&web=1&e=SfZn7E)  
  
📋 Caso:  
\- Cuenta (Account ID): \_\_\_ (ej. 214505) ← OBLIGATORIO  
\- Cliente: \_\_\_  
\- Nº SO (opcional): \_\_\_  
\- Nº BSA conocido (opcional): \_\_\_  
  
📎 Adjuntos:  
\- Pantallazo Oracle del SO  
\- PO del cliente (PDF o imagen)  
  
Resuelve siguiendo SKILL\_PRQ\_RESOLVER\_v1.5.md.  
Detecta división del ítem por patrón del part number y carga SOLO el catálogo relevante.  
Usa el script find\_item.py si dudas — evita cargar PDFs grandes.  
NO inventes reason codes — solo usar los de reason\_codes.md.  

## ⚡ INVOCACIÓN ULTRA-CORTA (sesión con contexto previo)

PRQ. Cuenta 214505. Adjuntos: Oracle + PO. Resuelve.  

## 📝 EJEMPLO LLENO

Skill PRQ Resolver: [https://hologic-my.sharepoint.com/:f:/r/personal/pedro\_moronta\_hologic\_com/Documents/Habilidades%20Order%20Management/PRQ%20RESOLVER%20(URL%20CON%20CONOCIMIENTOS)?csf=1&web=1&e=gqbCNt](https://hologic-my.sharepoint.com/:f:/r/personal/pedro_moronta_hologic_com/Documents/Habilidades%20Order%20Management/PRQ%20RESOLVER%20\(URL%20CON%20CONOCIMIENTOS\)?csf=1&web=1&e=gqbCNt)  
Recursos: [https://hologic-my.sharepoint.com/:f:/r/personal/pedro\_moronta\_hologic\_com/Documents/Habilidades%20Order%20Management/PRQ%20RECURSOS?csf=1&web=1&e=v3YQxt](https://hologic-my.sharepoint.com/:f:/r/personal/pedro_moronta_hologic_com/Documents/Habilidades%20Order%20Management/PRQ%20RECURSOS?csf=1&web=1&e=v3YQxt)  
BSAs: [https://hologic.sharepoint.com/:f:/r/sites/commercialcontractsandtendersemea/Shared%20Documents/General/Iberia/Tenders/Test/IBR?csf=1&web=1&e=SfZn7E](https://hologic.sharepoint.com/:f:/r/sites/commercialcontractsandtendersemea/Shared%20Documents/General/Iberia/Tenders/Test/IBR?csf=1&web=1&e=SfZn7E)  
  
📋 Caso:  
\- Cuenta: 214505  
\- Cliente: CLISUR MADRID  
\- SO: 3127877  
\- BSA conocido: 3111881  
  
📎 Adjunto: pantallazo Oracle SO 3127877 + PDF del PO de CLISUR.  
  
Resuelve.  

## ❗ Recordatorios rápidos

| **✅** | **❌** |
| --- | --- |
| Nº cuenta SIEMPRE | Buscar sin cuenta |
| Pantallazo Oracle SIEMPRE | Inventar precios |
| PO del cliente SIEMPRE | Leer más de 1 BSA |
| Si tienes Nº BSA → ponlo | Cargar los 3 catálogos a la vez |
| Verificar Box of X | Inventar reason codes |
| Detectar división por patrón | Asumir owner — verificarlo |

## 🎯 Reason codes más usados (referencia rápida)

| **Code** | **Cuándo** | **Owner** |
| --- | --- | --- |
| **CWPP** ⚠️ | Precio PO ≠ Oracle (más común) | CS+CC&T |
| **CWPU** | Cliente pide en unidades vs cajas | CS+CC&T |
| **CWPV** | PO con VAT | CS+CC&T |
| **CWPI** | Item code obsoleto | CS+CC&T |
| **PTWP** | Pricing Team cargó mal | CC&T |
| **PTBA** | BSA no triggered | CC&T |
| **PTNP** | Pricing no setup | CC&T |
| **SEC** | Contrato expirado | CC&T |
| **SMI** | Item falta del contrato | CC&T |
| **SNC** | Sin contrato | CC&T |
| **SBC** | Sales debe confirmar | CS |

_Fin del prompt v1.5._