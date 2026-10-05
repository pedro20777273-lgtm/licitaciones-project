# Clora · tienda y lanzamiento

Marca nueva de complemento alimenticio: menta, perejil, clorofila de alfalfa y zinc. 60 cápsulas vegetales, 2 al día.

| Carpeta | Contenido |
|---|---|
| `web/index.html` | Landing-tienda (prelanzamiento con lista de espera → venta con enlaces de pago) |
| `web/build.sh` | Genera `web/dist/index.html` listo para Netlify / Vercel / GitHub Pages |
| `kit/index.html` | Kit de lanzamiento: proveedores, Instagram, embudo, calculadora de márgenes, checklist legal |
| `instagram/render.cjs` | Genera las piezas de Instagram (`node instagram/render.cjs`, requiere Playwright) |
| `instagram/png/` | 9 posts 4:5 (orden de publicación 01 → 09), story, foto de perfil y 5 portadas de destacados |
| `assets/` | Bote en SVG y fuentes (Gloock, Figtree, IBM Plex Mono · licencia OFL) |

## Configurar la tienda

En `web/index.html`, bloque `CONFIG`:

- `modo`: `'prelanzamiento'` (botones abren la reserva) o `'venta'` (botones van al pago).
- `pagos`: enlace de Stripe Payment Link o checkout de Shopify para los packs 1, 2 y 3.
- `formEndpoint`: URL que recibe `{ email, pack, origen }` por POST (Klaviyo, Formspree, Shopify Flow…). Sin ella el formulario muestra un aviso y no guarda datos.

Antes de publicar: rellenar responsable, NIF, domicilio y nº RGSEAA del pie, y enlazar las páginas legales.

## Decisiones clave

- **Clorofila de alfalfa** en lugar de clorofilina cúprica (E141ii): la EFSA (2015) no pudo evaluar su seguridad y aporta cobre.
- **Zinc 10 mg (100 % VRN)**: único ingrediente con declaraciones de salud autorizadas (Reg. UE 432/2012).
- **Sin claims de olor corporal ni aliento**: no existen declaraciones autorizadas en la UE.
- **Validar antes de fabricar**: 300 altas en la lista verde a ≤ 1,50 € por alta antes de encargar el lote.

Las cifras de costes son estimaciones hasta tener presupuestos de fabricante.
