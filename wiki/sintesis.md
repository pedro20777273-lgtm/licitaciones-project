---
tipo: analisis
tags: [sintesis, vision-general]
fuentes: [todas]
actualizado: 2026-07-14
---

# Síntesis — El segundo cerebro de Pedro

## Qué es esto

Pedro Moronta, [Tender Specialist en Hologic Iberia](entidades/pedro-moronta.md), lleva ~1 año
construyendo **skills** (procedimientos operativos ejecutables por un LLM) que automatizan las dos
mitades de su trabajo:

1. **Licitaciones públicas españolas** (LCSP 9/2017): desde analizar pliegos hasta depositar el
   aval de la garantía definitiva. 8 skills cubren casi todo el ciclo.
2. **Order management** (CC&T Hologic): resolución de Price Queries (PRQ) en Oracle, con una skill
   madura (v1.5) y una base de conocimiento por cuenta que crece cada semana.

Esta wiki compila ese conocimiento en páginas interconectadas para que **no haya que redescubrirlo**
en cada sesión de chat, y para ver el sistema completo: qué existe, qué falta y cómo escalarlo.

## La tesis (estado a 2026-07-14)

Las skills de Pedro ya no son prompts sueltos: son un **sistema operativo personal** con patrones de
ingeniería reconocibles — versionado, logs de errores, progressive disclosure, datos fijos, scripts
empaquetados (ver [patrón de diseño de skills](conceptos/patron-diseno-skills.md)). Los tres hechos
más importantes que emergen al cruzar todas las fuentes:

1. **El ciclo de vida es el hilo conductor.** Cada skill es una fase del
   [ciclo de vida de una licitación](conceptos/ciclo-vida-licitacion.md) o de su continuación
   post-adjudicación (pedidos/PRQ). El [mapa de skills](skills/mapa-skills.md) lo muestra: la
   cobertura es alta en el centro del ciclo y débil en los extremos (detección de oportunidades y
   post-venta preventivo).

2. **Los PRQs son síntomas, no enfermedades.** La mayoría de los Price Queries de la
   [base de conocimiento](skills/prq-resolver.md) nacen aguas arriba: contratos expirados sin
   renovar (SEC), BSAs sin cargar o mal mapeados (PTBA/PTNP), KAMs que no responden. Quien controla
   el ciclo de tender controla la causa raíz de los PRQs. Esta conexión tender ↔ order management
   es la mayor oportunidad de automatización preventiva (ver [mejoras](mejoras.md)).

3. **El conocimiento está fragmentado en formatos y ubicaciones.** SharePoint/OneDrive con URLs
   frágiles, nombres inconsistentes (SKILL_5, SKILL_A1, 3_1…), datos fijos de empresa duplicados en
   4+ skills, archivos con extensión equivocada. Consolidar en este repo con formato estándar de
   Agent Skills es el paso natural (ver [mejoras](mejoras.md)).

## Cómo navegar

- **[index.md](index.md)** — catálogo completo de páginas.
- **[skills/mapa-skills.md](skills/mapa-skills.md)** — las 9 skills sobre el ciclo de vida.
- **[mejoras.md](mejoras.md)** — gaps, áreas de mejora y plan de escalado (lo que Pedro pidió).
- **[fuentes/catalogo-fuentes.md](fuentes/catalogo-fuentes.md)** — qué archivo de `row/` alimentó qué página.
