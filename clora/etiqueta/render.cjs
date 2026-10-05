// Etiqueta envolvente del bote Clora (170 × 70 mm, tres paneles).
// Uso: node etiqueta/render.cjs  →  etiqueta/etiqueta.pdf (imprenta) y etiqueta/etiqueta.png (vista previa)
// Comprueba la altura de la «x» del texto obligatorio (Reg. UE 1169/2011, art. 13.2: ≥ 1,2 mm)
// y que ningún panel se desborde.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const F = path.join(__dirname, '..', 'assets', 'fonts');
const CUERPO_MM = 2.55; // tamaño del texto obligatorio

const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Etiqueta Clora</title><style>
@font-face{font-family:'Gloock';src:url('file://${F}/Gloock-400.woff2')}
@font-face{font-family:'Figtree';src:url('file://${F}/Figtree-var.woff2');font-weight:300 900}
@font-face{font-family:'IBM Plex Mono';src:url('file://${F}/IBMPlexMono-500.woff2');font-weight:500}
@page{size:170mm 70mm;margin:0}
*{box-sizing:border-box;margin:0}
html,body{width:170mm;height:70mm}
body{font-family:Figtree,sans-serif;color:#13261B;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.etq{display:grid;grid-template-columns:57mm 56mm 57mm;width:170mm;height:70mm;overflow:hidden}
.panel{padding:3.2mm 3.4mm;overflow:hidden;font-size:${CUERPO_MM}mm;line-height:1.16}
.lat{background:#F8FAF6}
.frente{background:#173F2A;color:#F8FAF6;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.6mm}
.frente .nombre{font:400 15mm/0.9 Gloock,serif}
.frente .ing{font:500 2.1mm/1.3 'IBM Plex Mono',monospace;letter-spacing:.08mm;color:#B9A9EA}
.frente .den{font-size:${CUERPO_MM}mm;line-height:1.2;max-width:46mm}
.frente .neto{font-size:${CUERPO_MM}mm;font-weight:600;border-top:.25mm solid rgba(248,250,246,.4);padding-top:1.4mm}
.frente .claim{font-size:2.3mm;color:#C9D8CE;max-width:46mm}
h4{font:700 ${CUERPO_MM}mm/1.1 Figtree,sans-serif;letter-spacing:.1mm;margin-top:1.3mm}
h4:first-child{margin-top:0}
table{width:100%;border-collapse:collapse;margin-top:.6mm;font-variant-numeric:tabular-nums}
td,th{border-bottom:.2mm solid #13261B;padding:.35mm 0;text-align:left;font-size:${CUERPO_MM}mm;line-height:1.1}
th{font-weight:700}
td+td,th+th{text-align:right;padding-left:1mm;white-space:nowrap}
.peq{font-size:${CUERPO_MM}mm}
.ean{margin-top:1.2mm;display:flex;gap:2mm;align-items:end}
.ean div{width:24mm;height:10mm;border:.25mm dashed #13261B;display:grid;place-items:center;font:500 1.8mm/1 'IBM Plex Mono',monospace}
.ph{background:#FFF1B8}
</style></head><body>
<div class="etq">
  <div class="panel lat" id="izq">
    <h4>INGREDIENTES</h4>
    <p>Extracto seco de hoja de menta (<i>Mentha × piperita</i> L.), hoja de perejil en polvo (<i>Petroselinum crispum</i>), cápsula vegetal (hidroxipropilmetilcelulosa), extracto de hoja de alfalfa (<i>Medicago sativa</i> L.), gluconato de zinc.</p>
    <table>
      <thead><tr><th>Por dosis diaria (2 cáps.)</th><th>Cantidad</th><th>%VRN*</th></tr></thead>
      <tbody>
        <tr><td>Extracto de menta</td><td>200 mg</td><td>–</td></tr>
        <tr><td>Perejil</td><td>200 mg</td><td>–</td></tr>
        <tr><td>Extracto de alfalfa</td><td>150 mg</td><td>–</td></tr>
        <tr><td>Zinc</td><td>10 mg</td><td>100 %</td></tr>
      </tbody>
    </table>
    <p class="peq">*VRN: valores de referencia de nutrientes.</p>
    <h4>MODO DE EMPLEO</h4>
    <p>Tomar 2 cápsulas al día con un vaso de agua, preferiblemente con el desayuno.</p>
  </div>
  <div class="panel frente" id="frente">
    <svg width="9mm" height="9mm" viewBox="-20 -20 40 40"><circle r="17" fill="none" stroke="#B9A9EA" stroke-width="2.2"/><path d="M-10 6 C-6 -6 4 -12 12 -12 C12 -2 6 8 -8 9 Z" fill="#E3F0E6"/></svg>
    <div class="nombre">clora</div>
    <div class="ing">MENTA · PEREJIL · CLOROFILA + ZINC</div>
    <div class="den">Complemento alimenticio con extractos de menta y alfalfa, perejil y zinc</div>
    <div class="claim">El zinc contribuye al mantenimiento de la piel en condiciones normales.</div>
    <div class="neto">60 cápsulas vegetales · <span class="ph" style="color:#13261B">[24]</span> g</div>
  </div>
  <div class="panel lat" id="der">
    <h4>ADVERTENCIAS</h4>
    <p>No superar la dosis diaria expresamente recomendada. Los complementos alimenticios no deben utilizarse como sustituto de una dieta equilibrada y variada y de un modo de vida sano. Mantener fuera del alcance de los niños más pequeños. No recomendado en embarazo y lactancia. Si toma anticoagulantes, consulte a su médico.</p>
    <h4>CONSERVACIÓN</h4>
    <p>En lugar fresco y seco, protegido de la luz.</p>
    <p style="margin-top:1mm">Consumir preferentemente antes del fin de: ver base. Lote: ver base.</p>
    <p style="margin-top:1mm"><span class="ph">[Razón social] · [Dirección] · [CP] Toledo · RGSEAA [26.XXXXX/TO]</span></p>
    <div class="ean"><div>EAN-13</div><span class="peq">Envase al contenedor amarillo.</span></div>
  </div>
</div>
</body></html>`;

const out = path.join(__dirname, 'etiqueta.html');
fs.writeFileSync(out, html);

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 460 }, deviceScaleFactor: 2 });
  await p.goto('file://' + out);
  await p.evaluate(() => document.fonts.ready);
  const chk = await p.evaluate((mm) => {
    const pxPorMm = 96 / 25.4;
    const c = document.createElement('canvas').getContext('2d');
    c.font = `${mm * pxPorMm * 10}px Figtree`;
    const xh = c.measureText('x').actualBoundingBoxAscent / 10 / pxPorMm;
    const desb = ['izq', 'frente', 'der'].filter(id => { const e = document.getElementById(id); return e.scrollHeight > e.clientHeight + 1; });
    return { xh: xh.toFixed(2), desb };
  }, CUERPO_MM);
  console.log(`Altura de la x del texto obligatorio: ${chk.xh} mm (mínimo 1,2 mm) → ${chk.xh >= 1.2 ? 'OK' : 'NO CUMPLE'}`);
  console.log(chk.desb.length ? `Paneles desbordados: ${chk.desb.join(', ')}` : 'Ningún panel desbordado');
  await p.screenshot({ path: path.join(__dirname, 'etiqueta.png'), clip: { x: 0, y: 0, width: 170 * 96 / 25.4, height: 70 * 96 / 25.4 } });
  await p.pdf({ path: path.join(__dirname, 'etiqueta.pdf'), width: '170mm', height: '70mm', printBackground: true });
  console.log('Generados etiqueta.pdf y etiqueta.png');
  await b.close();
})();
