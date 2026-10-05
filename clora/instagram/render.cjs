// Genera las piezas de Instagram de Clora (posts 4:5, story 9:16, perfil y destacados).
// Uso: node instagram/render.cjs   (requiere playwright con Chromium)
// Salida: instagram/piezas.html (editable) y instagram/png/*.jpg|png
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const RAIZ = path.join(__dirname, '..');
const FUENTES = path.join(RAIZ, 'assets', 'fonts');
const OUT = path.join(__dirname, 'png');
fs.mkdirSync(OUT, { recursive: true });

const C = { clorofila: '#173F2A', hoja: '#2F6B45', menta: '#E3F0E6', papel: '#F8FAF6', flor: '#B9A9EA', florOsc: '#56459A', tinta: '#13261B', gris: '#53625A' };

// ---------- ilustraciones ----------
const bote = fs.readFileSync(path.join(RAIZ, 'assets', 'bote.svg'), 'utf8').replace(/<svg[^>]*>/, '').replace('</svg>', '');
const boteSVG = (w, extra = '') => `<svg viewBox="0 0 320 440" width="${w}" ${extra}>${bote}</svg>`;

const DEFS = `<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="hg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#5BA870"/><stop offset="1" stop-color="#2F6B45"/></linearGradient>
<linearGradient id="hg2" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#4A9461"/><stop offset="1" stop-color="#245A3B"/></linearGradient>
<symbol id="hoja" viewBox="0 -40 130 80"><path d="M2 0 C24 -34 76 -38 126 0 C76 38 24 34 2 0Z" fill="url(#hg)"/><path d="M4 0 L120 0 M30 0 L46 -16 M52 0 L70 -18 M76 0 L92 -14 M30 0 L46 16 M52 0 L70 18 M76 0 L92 14" stroke="#E3F0E6" stroke-opacity=".55" stroke-width="1.6" fill="none" stroke-linecap="round"/></symbol>
<symbol id="capsula" viewBox="0 0 80 32"><rect x="1" y="1" width="78" height="30" rx="15" fill="#3E8257"/><path d="M16 1 H40 V31 H16 A15 15 0 0 1 16 1Z" fill="#2F6B45"/><rect x="10" y="6" width="56" height="5" rx="2.5" fill="#FFFFFF" opacity=".35"/></symbol>
<symbol id="logo" viewBox="-20 -20 40 40"><circle r="17" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M-10 6 C-6 -6 4 -12 12 -12 C12 -2 6 8 -8 9 Z" fill="currentColor"/></symbol>
</defs></svg>`;

// Menta: tallo con pares de hojas opuestas que decrecen hacia arriba
function menta() {
  let g = `<path d="M300 760 C296 600 304 420 300 150" stroke="#2F6B45" stroke-width="7" fill="none" stroke-linecap="round"/>`;
  const pares = [[660, 1.25], [540, 1.1], [425, .95], [320, .78], [230, .6]];
  pares.forEach(([y, s], i) => {
    const a = 28 + i * 6;
    g += `<use href="#hoja" x="0" y="-40" width="130" height="80" transform="translate(302 ${y}) rotate(${-a}) scale(${s * 1.7})"/>`;
    g += `<use href="#hoja" x="0" y="-40" width="130" height="80" transform="translate(298 ${y}) scale(-1 1) rotate(${-a}) scale(${s * 1.7})"/>`;
  });
  g += `<use href="#hoja" x="0" y="-40" width="130" height="80" transform="translate(300 160) rotate(-90) scale(.75)"/>`;
  return `<svg viewBox="0 0 600 800" width="560">${g}</svg>`;
}

// Perejil: ramillete con foliolos lobulados
function lobulo(x, y, r, rot) {
  // foliolo de perejil: hojitas apuntadas en abanico
  const k = r / 70;
  let s = `<g transform="translate(${x} ${y}) rotate(${rot})">`;
  [[-90, 1], [-50, .85], [-130, .85], [-18, .62], [-162, .62]].forEach(([a, e]) => {
    s += `<use href="#hoja" x="0" y="-40" width="130" height="80" transform="rotate(${a}) scale(${k * e * 1.05})"/>`;
  });
  return s + '</g>';
}
function perejil() {
  const tallos = [
    ['M300 780 C300 640 290 520 300 400', 300, 360, 62, 0],
    ['M300 640 C250 560 200 500 170 430', 160, 395, 52, -28],
    ['M300 640 C350 560 400 500 430 430', 440, 395, 52, 28],
    ['M300 520 C240 430 220 330 200 250', 195, 215, 48, -14],
    ['M300 520 C360 430 380 330 400 250', 405, 215, 48, 14],
    ['M300 700 C220 660 150 640 100 600', 85, 575, 44, -52],
    ['M300 700 C380 660 450 640 500 600', 515, 575, 44, 52],
    ['M300 420 C300 330 300 250 300 160', 300, 120, 50, 0]
  ];
  let g = '';
  tallos.forEach(([d]) => { g += `<path d="${d}" stroke="#2F6B45" stroke-width="6" fill="none" stroke-linecap="round"/>`; });
  tallos.forEach(([d, , , r, rot]) => { const [x, y] = d.trim().split(/\s+/).slice(-2).map(Number); g += lobulo(x, y, r, rot); });
  return `<svg viewBox="0 0 600 800" width="560">${g}</svg>`;
}

// Alfalfa: tallo con hojas trifoliadas y racimo de flores lilas
function trifolio(x, y, s, rot) {
  return `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">
    <path d="M0 0 L0 -40" stroke="#2F6B45" stroke-width="4"/>
    <ellipse cx="0" cy="-78" rx="20" ry="38" fill="url(#hg)"/>
    <ellipse cx="-30" cy="-46" rx="18" ry="34" transform="rotate(-58 -30 -46)" fill="url(#hg2)"/>
    <ellipse cx="30" cy="-46" rx="18" ry="34" transform="rotate(58 30 -46)" fill="url(#hg2)"/>
    <path d="M0 -44 L0 -110 M0 -44 L-52 -66 M0 -44 L52 -66" stroke="#E3F0E6" stroke-opacity=".5" stroke-width="2" fill="none"/>
  </g>`;
}
function alfalfa() {
  let g = `<path d="M300 780 C310 620 290 460 300 230" stroke="#2F6B45" stroke-width="7" fill="none" stroke-linecap="round"/>`;
  [[300, 690, 1.3, -55], [300, 600, 1.25, 55], [300, 500, 1.1, -50], [300, 410, 1, 50], [300, 330, .85, -40]].forEach(a => { g += trifolio(...a); });
  const flores = [[300, 200], [276, 222], [324, 222], [288, 176], [312, 176], [300, 152], [266, 196], [334, 196], [300, 128]];
  flores.forEach(([x, y], i) => { g += `<ellipse cx="${x}" cy="${y}" rx="15" ry="11" fill="${i % 2 ? '#9C88DA' : '#B9A9EA'}"/>`; });
  return `<svg viewBox="0 0 600 800" width="560">${g}</svg>`;
}

const marca = (color) => `<div class="firma" style="color:${color}"><svg width="40" height="40"><use href="#logo"/></svg>clora</div>`;

// ---------- piezas ----------
const lamina = (n, nombre, latin, detalle, ilu, fondo = C.papel) => `
<div class="pieza" style="background:${fondo}">
  <div class="marco"></div>
  <div class="esq tl">LÁMINA ${n} / IV</div><div class="esq tr">CLORA · LA FÓRMULA</div>
  <div class="ilu">${ilu}</div>
  <div class="pie-lam">
    <h2 class="d" style="font-size:104px">${nombre}</h2>
    <p class="m" style="font-size:30px;color:${C.florOsc};margin-top:14px">${latin}</p>
    <p style="font-size:32px;color:${C.gris};margin-top:20px">${detalle}</p>
  </div>
</div>`;

const PIEZAS = [
  // orden de publicación: 01 se publica primero (queda abajo a la derecha del perfil)
  { id: '01-alfalfa', w: 1080, h: 1350, html: lamina('III', 'Clorofila de alfalfa', 'Medicago sativa L.', 'Extracto de hoja · 150 mg por dosis diaria', alfalfa()) },
  { id: '02-ritual', w: 1080, h: 1350, html: `
<div class="pieza oscura">
  <p class="m eyebrow" style="color:${C.flor}">CÓMO SE TOMA</p>
  <h2 class="d" style="font-size:120px;color:${C.papel};margin-top:28px">Diez segundos<br>al día.</h2>
  <div class="pasos">
    <div><span class="d n">1</span><b>Con el desayuno</b><p>2 cápsulas con un vaso de agua.</p></div>
    <div><span class="d n">2</span><b>Un bote, un mes</b><p>60 cápsulas = 30 días exactos.</p></div>
    <div><span class="d n">3</span><b>Déjalo a la vista</b><p>Junto a la cafetera. La constancia es el ritual.</p></div>
  </div>
  <div class="caps"><svg viewBox="0 0 80 32" width="230"><use href="#capsula"/></svg><svg viewBox="0 0 80 32" width="230" style="transform:rotate(-14deg)"><use href="#capsula"/></svg></div>
  ${marca(C.papel)}
</div>` },
  { id: '03-perejil', w: 1080, h: 1350, html: lamina('II', 'Perejil', 'Petroselinum crispum (Mill.) Fuss', 'Hoja en polvo · 200 mg por dosis diaria', perejil()) },
  { id: '04-packs', w: 1080, h: 1350, html: `
<div class="pieza oscura">
  <p class="m eyebrow" style="color:${C.flor}">PACKS DE LANZAMIENTO</p>
  <h2 class="d" style="font-size:96px;color:${C.papel};margin-top:28px">Cuantos más días,<br>menos pagas por bote.</h2>
  <div class="tabla-packs">
    <div class="fila"><div class="bt">${boteSVG(70)}</div><div><b>1 bote</b><span>30 días</span></div><div class="pr">27,90 €</div></div>
    <div class="fila dest"><div class="bt">${boteSVG(70)}${boteSVG(70)}</div><div><b>2 botes</b><span>23,95 € / bote · envío gratis</span></div><div class="pr">47,90 €</div></div>
    <div class="fila"><div class="bt">${boteSVG(70)}${boteSVG(70)}${boteSVG(70)}</div><div><b>3 botes</b><span>20,97 € / bote · envío gratis</span></div><div class="pr">62,90 €</div></div>
  </div>
  <p class="aviso-l">Lista verde: <b>−15 %</b> el día del lanzamiento. Enlace en la bio.</p>
  ${marca(C.papel)}
</div>` },
  { id: '05-menta', w: 1080, h: 1350, html: lamina('I', 'Menta piperita', 'Mentha × piperita L.', 'Extracto seco de hoja · 200 mg por dosis diaria', menta()) },
  { id: '06-cuatro', w: 1080, h: 1350, html: `
<div class="pieza oscura">
  <p class="m eyebrow" style="color:${C.flor}">LA FÓRMULA COMPLETA</p>
  <h2 class="d" style="font-size:118px;color:${C.papel};margin-top:28px">Cuatro<br>ingredientes.<br><span style="color:${C.flor}">Ni uno más.</span></h2>
  <div class="ingr">
    <div><span>Menta piperita</span><i>hoja · extracto</i><b>200 mg</b></div>
    <div><span>Perejil</span><i>hoja · polvo</i><b>200 mg</b></div>
    <div><span>Clorofila de alfalfa</span><i>hoja · extracto</i><b>150 mg</b></div>
    <div><span>Zinc</span><i>gluconato · 100 % VRN</i><b>10 mg</b></div>
  </div>
  <p class="m" style="position:absolute;left:96px;bottom:150px;font-size:24px;color:#9DB5A6;letter-spacing:.08em">POR DOSIS DIARIA DE 2 CÁPSULAS</p>
  ${marca(C.papel)}
</div>` },
  { id: '07-zinc', w: 1080, h: 1350, html: `
<div class="pieza" style="background:${C.menta}">
  <div class="marco"></div>
  <div class="esq tl">LÁMINA IV / IV</div><div class="esq tr">CLORA · LA FÓRMULA</div>
  <div class="zn"><span class="z">30</span><span class="sym d">Zn</span><span class="nom">Zinc</span><span class="masa">65,38</span></div>
  <div class="pie-lam">
    <p class="d" style="font-size:60px;line-height:1.12;color:${C.clorofila}">El zinc contribuye al mantenimiento de la piel en condiciones normales.</p>
    <p class="m" style="font-size:28px;color:${C.florOsc};margin-top:22px">GLUCONATO DE ZINC · 10 MG · 100 % VRN</p>
  </div>
</div>` },
  { id: '08-manifiesto', w: 1080, h: 1350, html: `
<div class="pieza oscura">
  <p class="m eyebrow" style="color:${C.flor}">POR QUÉ CLORA</p>
  <h2 class="d" style="font-size:112px;line-height:1.04;color:${C.papel};margin-top:36px">No te prometemos milagros.</h2>
  <h2 class="d" style="font-size:112px;line-height:1.04;color:${C.flor};margin-top:30px">Te contamos lo que lleva cada cápsula.</h2>
  ${marca(C.papel)}
</div>` },
  { id: '09-lanzamiento', w: 1080, h: 1350, html: `
<div class="pieza" style="background:${C.papel}">
  <div class="disco"></div>
  <svg class="hj" viewBox="0 -40 130 80" width="300" style="left:40px;top:860px;transform:rotate(-20deg)"><use href="#hoja"/></svg>
  <svg class="hj" viewBox="0 -40 130 80" width="260" style="right:40px;top:560px;transform:rotate(160deg)"><use href="#hoja"/></svg>
  <svg class="hj" viewBox="0 0 80 32" width="130" style="left:250px;top:1180px;transform:rotate(-20deg)"><use href="#capsula"/></svg>
  <svg class="hj" viewBox="0 0 80 32" width="120" style="right:230px;top:1200px;transform:rotate(16deg)"><use href="#capsula"/></svg>
  <div style="position:absolute;left:50%;top:470px;transform:translateX(-50%);filter:drop-shadow(0 30px 40px rgba(19,38,27,.25))">${boteSVG(560)}</div>
  <div style="position:absolute;left:96px;right:96px;top:96px;text-align:center">
    <p class="m eyebrow" style="color:${C.hoja}">PRÓXIMAMENTE</p>
    <h2 class="d" style="font-size:124px;color:${C.clorofila};margin-top:20px">Tu ritual verde.</h2>
    <p class="m" style="font-size:26px;letter-spacing:.12em;color:${C.florOsc};margin-top:18px">MENTA · PEREJIL · CLOROFILA + ZINC</p>
  </div>
</div>` },
  // anuncios de Meta: 3 ángulos × feed 4:5 y stories/reels 9:16 (zonas seguras: 250 px arriba, 340 px abajo)
  ...anuncios(),
  // story de captación
  { id: 'story-lista', w: 1080, h: 1920, html: `
<div class="pieza oscura" style="height:1920px">
  <div style="position:absolute;left:96px;right:96px;top:220px">
    <p class="m eyebrow" style="color:${C.flor}">LA LISTA VERDE</p>
    <h2 class="d" style="font-size:132px;color:${C.papel};margin-top:30px">Sé de los primeros.</h2>
    <p style="font-size:44px;color:#C9D8CE;margin-top:36px;line-height:1.35">Te avisamos del lanzamiento con un <b style="color:${C.flor}">15 %</b> de descuento.</p>
  </div>
  <div style="position:absolute;left:50%;top:800px;transform:translateX(-50%)"><div style="width:500px;height:500px;border-radius:50%;background:${C.flor};position:absolute;left:-20px;top:60px"></div><div style="position:relative">${boteSVG(460)}</div></div>
  <p class="m" style="position:absolute;left:0;right:0;bottom:330px;text-align:center;font-size:30px;letter-spacing:.14em;color:${C.flor}">TOCA EL ENLACE ↓</p>
</div>` },
  // perfil
  { id: 'perfil', w: 1080, h: 1080, png: true, html: `
<div class="pieza" style="width:1080px;height:1080px;background:${C.clorofila};display:grid;place-items:center">
  <svg width="560" height="560" style="color:${C.menta}"><use href="#logo"/></svg>
  <div style="position:absolute;width:760px;height:760px;border-radius:50%;border:10px solid ${C.flor};left:160px;top:160px"></div>
</div>` },
  // portadas de destacados
  ...[
    ['formula', 'Fórmula', '<path d="M28 5 L48 16.5 V39.5 L28 51 L8 39.5 V16.5 Z" fill="none" stroke="currentColor" stroke-width="2.4"/><text x="28" y="34" text-anchor="middle" font-family="IBM Plex Mono" font-size="14" fill="currentColor">4</text>'],
    ['ritual', 'Ritual', '<rect x="8" y="21" width="40" height="15" rx="7.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M28 21 V36" stroke="currentColor" stroke-width="2.4"/>'],
    ['preguntas', 'Preguntas', '<circle cx="28" cy="28" r="21" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M21 22 C21 14 35 14 35 22 C35 28 28 28 28 33" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><circle cx="28" cy="40" r="1.8" fill="currentColor"/>'],
    ['envios', 'Envíos', '<path d="M6 18 H34 V38 H6 Z M34 24 H43 L50 31 V38 H34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><circle cx="15" cy="40" r="4" fill="#B9A9EA" stroke="currentColor" stroke-width="2.4"/><circle cx="42" cy="40" r="4" fill="#B9A9EA" stroke="currentColor" stroke-width="2.4"/>'],
    ['lista', 'Lista verde', '<path d="M10 44 C14 24 30 10 48 8 C48 28 34 44 12 46 Z" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M12 45 L42 14" stroke="currentColor" stroke-width="2"/>']
  ].map(([id, , ico]) => ({ id: 'destacado-' + id, w: 1080, h: 1080, png: true, html: `
<div class="pieza" style="width:1080px;height:1080px;background:${C.flor};display:grid;place-items:center">
  <svg viewBox="0 0 56 56" width="440" style="color:${C.clorofila}">${ico}</svg>
</div>` }))
];

function anuncios() {
  const ficha = (ancho) => `<div class="ficha-ad" style="width:${ancho}px">
    <b>Por dosis diaria · 2 cápsulas</b>
    <div><span>Extracto de hoja de menta</span><span>200 mg</span></div>
    <div><span>Hoja de perejil</span><span>200 mg</span></div>
    <div><span>Extracto de hoja de alfalfa</span><span>150 mg</span></div>
    <div><span>Zinc · 100 % VRN</span><span>10 mg</span></div>
  </div>`;
  const tres = `<div class="tres">${boteSVG(250)}${boteSVG(290)}${boteSVG(250)}</div>`;
  const A = (h) => `
<div class="pieza" style="background:${C.papel};height:${h}px">
  <div style="position:absolute;left:96px;right:96px;top:${h > 1400 ? 260 : 96}px">
    <p class="m eyebrow" style="color:${C.hoja}">LA FÓRMULA COMPLETA</p>
    <h2 class="d" style="font-size:${h > 1400 ? 112 : 96}px;color:${C.clorofila};margin-top:24px">Cuatro ingredientes.<br><span style="color:${C.florOsc}">Cantidades a la vista.</span></h2>
  </div>
  <div style="position:absolute;left:96px;bottom:${h > 1400 ? 400 : 96}px">${ficha(560)}</div>
  <div style="position:absolute;right:60px;bottom:${h > 1400 ? 370 : 70}px;filter:drop-shadow(0 24px 30px rgba(19,38,27,.2))">${boteSVG(400)}</div>
</div>`;
  const B = (h) => `
<div class="pieza" style="background:${C.menta};height:${h}px">
  <div style="position:absolute;left:96px;right:96px;top:${h > 1400 ? 260 : 96}px">
    <p class="m eyebrow" style="color:${C.hoja}">TU RITUAL VERDE</p>
    <h2 class="d" style="font-size:${h > 1400 ? 124 : 110}px;color:${C.clorofila};margin-top:24px">Diez segundos<br>cada mañana.</h2>
  </div>
  <div class="cifras" style="top:${h > 1400 ? 720 : 520}px">
    <div><b class="d">2</b><span>cápsulas</span></div><div><b class="d">30</b><span>días</span></div><div><b class="d">1</b><span>bote</span></div>
  </div>
  <div style="position:absolute;left:50%;bottom:${h > 1400 ? 360 : 60}px;transform:translateX(-50%)">
    <div style="position:absolute;width:520px;height:520px;border-radius:50%;background:${C.flor};left:-90px;top:120px"></div>
    <div style="position:relative">${boteSVG(h > 1400 ? 440 : 340)}</div>
  </div>
</div>`;
  const Cc = (h) => `
<div class="pieza oscura" style="height:${h}px">
  <div style="position:absolute;left:96px;right:96px;top:${h > 1400 ? 260 : 96}px">
    <p class="m eyebrow" style="color:${C.flor}">LA LISTA VERDE</p>
    <h2 class="d" style="font-size:${h > 1400 ? 120 : 104}px;color:${C.papel};margin-top:24px">Sé de los primeros.</h2>
    <p class="d" style="font-size:${h > 1400 ? 340 : 300}px;line-height:.9;color:${C.flor};margin-top:30px">−15 %</p>
    <p style="font-size:40px;color:#C9D8CE;margin-top:18px">en tu primer pedido el día del lanzamiento</p>
  </div>
  <div style="position:absolute;left:0;right:0;bottom:${h > 1400 ? 360 : 70}px">${tres}</div>
</div>`;
  return [
    ['anuncio-a-feed', A, 1350], ['anuncio-a-story', A, 1920],
    ['anuncio-b-feed', B, 1350], ['anuncio-b-story', B, 1920],
    ['anuncio-c-feed', Cc, 1350], ['anuncio-c-story', Cc, 1920]
  ].map(([id, f, h]) => ({ id, w: 1080, h, html: f(h) }));
}

const CSS = `
@font-face{font-family:'Gloock';src:url('../assets/fonts/Gloock-400.woff2')}
@font-face{font-family:'Figtree';src:url('../assets/fonts/Figtree-var.woff2');font-weight:300 900}
@font-face{font-family:'IBM Plex Mono';src:url('../assets/fonts/IBMPlexMono-400.woff2');font-weight:400}
@font-face{font-family:'IBM Plex Mono';src:url('../assets/fonts/IBMPlexMono-500.woff2');font-weight:500}
*{box-sizing:border-box;margin:0}
body{background:#888;font-family:Figtree,sans-serif;color:${C.tinta};display:grid;gap:40px;padding:40px;justify-content:center}
.pieza{width:1080px;height:1350px;position:relative;overflow:hidden;padding:96px}
.oscura{background:${C.clorofila};color:${C.papel}}
.d{font-family:Gloock,Georgia,serif;font-weight:400;line-height:1.02;letter-spacing:-.005em}
.m{font-family:'IBM Plex Mono',monospace;font-weight:500}
.eyebrow{font-size:26px;letter-spacing:.16em}
.firma{position:absolute;left:96px;bottom:84px;display:flex;align-items:center;gap:14px;font:400 46px/1 Gloock,serif}
.marco{position:absolute;inset:48px;border:2px solid ${C.tinta};opacity:.85}
.esq{position:absolute;top:76px;font:500 22px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;color:${C.tinta}}
.esq.tl{left:84px}.esq.tr{right:84px}
.ilu{position:absolute;left:0;right:0;top:120px;display:flex;justify-content:center}
.pie-lam{position:absolute;left:96px;right:96px;bottom:110px}
.disco{position:absolute;width:900px;height:900px;border-radius:50%;left:90px;top:400px;background:radial-gradient(circle at 35% 30%,#D6CCF5 0,${C.flor} 62%,#A493E0 100%)}
.hj{position:absolute}
.pasos{display:grid;gap:44px;margin-top:80px;max-width:640px}
.pasos div{display:grid;grid-template-columns:90px 1fr;column-gap:20px}
.pasos .n{grid-row:span 2;font-size:96px;color:${C.flor}}
.pasos b{font-size:44px;font-weight:600}
.pasos p{font-size:34px;color:#C9D8CE;margin-top:6px}
.caps{position:absolute;right:70px;bottom:250px;display:grid;gap:30px;transform:rotate(-30deg)}
.tabla-packs{margin-top:70px;display:grid;gap:22px}
.tabla-packs .fila{display:grid;grid-template-columns:230px 1fr auto;align-items:center;gap:26px;background:#1F4C34;border-radius:28px;padding:26px 34px}
.tabla-packs .fila.dest{background:${C.papel};color:${C.tinta};box-shadow:0 0 0 6px ${C.flor}}
.tabla-packs .bt{display:flex;justify-content:center}
.tabla-packs .bt svg{margin-inline:-10px}
.tabla-packs b{display:block;font-size:46px;font-weight:600}
.tabla-packs span{font-size:28px;opacity:.8}
.tabla-packs .pr{font:400 64px/1 Gloock,serif}
.aviso-l{position:absolute;right:96px;bottom:92px;font-size:30px;color:#C9D8CE;text-align:right;max-width:560px}
.aviso-l b{color:${C.flor}}
.ingr{margin-top:70px;border-top:2px solid #3C6B50}
.ingr div{display:grid;grid-template-columns:1fr auto;grid-template-rows:auto auto;padding:24px 0;border-bottom:2px solid #3C6B50}
.ingr span{font-size:46px;font-weight:600}
.ingr i{font:400 26px/1.3 'IBM Plex Mono',monospace;font-style:normal;color:${C.flor};grid-row:2}
.ingr b{grid-row:span 2;align-self:center;font:400 64px/1 Gloock,serif;color:${C.papel}}
.zn{position:absolute;left:50%;top:170px;transform:translateX(-50%);width:560px;height:560px;background:${C.clorofila};color:${C.papel};border-radius:36px}
.zn .z{position:absolute;left:44px;top:40px;font:500 52px/1 'IBM Plex Mono',monospace}
.zn .sym{position:absolute;left:0;right:0;top:120px;text-align:center;font-size:280px}
.zn .nom{position:absolute;left:0;right:0;bottom:84px;text-align:center;font-size:44px;font-weight:600}
.zn .masa{position:absolute;right:44px;top:44px;font:400 30px/1 'IBM Plex Mono',monospace;color:${C.flor}}
.ficha-ad{background:#fff;border:5px solid ${C.tinta};padding:28px 32px;font-size:30px}
.ficha-ad b{display:block;font-size:34px;font-weight:700;border-bottom:12px solid ${C.tinta};padding-bottom:10px;margin-bottom:6px}
.ficha-ad div{display:flex;justify-content:space-between;gap:20px;padding:12px 0;border-bottom:2px solid ${C.tinta}}
.ficha-ad div:last-child{border-bottom:0}
.ficha-ad div span:last-child{font-weight:700;font-variant-numeric:tabular-nums}
.cifras{position:absolute;left:96px;right:96px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.cifras b{display:block;font-size:150px;line-height:1;color:${C.clorofila}}
.cifras span{font:500 28px/1 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:${C.hoja}}
.tres{display:flex;justify-content:center;align-items:flex-end}
.tres svg{margin-inline:-30px}
.tres svg:nth-child(2){position:relative;z-index:1}
`;

const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Clora · piezas Instagram</title><style>${CSS}</style></head><body>${DEFS}
${PIEZAS.map(p => `<div id="p-${p.id}" style="width:${p.w}px;height:${p.h}px">${p.html}</div>`).join('\n')}
</body></html>`;
const htmlPath = path.join(__dirname, 'piezas.html');
fs.writeFileSync(htmlPath, html);

(async () => {
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1200, height: 1400 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + htmlPath);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  for (const p of PIEZAS) {
    const el = await page.$('#p-' + p.id);
    const file = path.join(OUT, p.id + (p.png ? '.png' : '.jpg'));
    await el.screenshot(p.png ? { path: file } : { path: file, type: 'jpeg', quality: 90 });
    console.log('ok', path.relative(RAIZ, file));
  }
  if (errs.length) console.log('ERRORES:', errs.join(' | '));
  await b.close();
})();
