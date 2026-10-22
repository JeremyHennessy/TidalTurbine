/* Isolated Concept 003 UI. Existing experiment and artwork rendering is unchanged. */
(function () {
  'use strict';
  function init() {
    const panel=document.getElementById('clearance-lab');
    if (!panel || !globalThis.TidalClearance) return;
    const get=id=>document.getElementById('clearance-'+id);
    const fields=['ptoX','sensorX','margin','hatch'];
    const number=id=>{const s=get(id).value.trim();return s===''?NaN:Number(s);};
    function rect(b,mode,color,label) {
      const plan=mode==='plan', scale=plan?85:48, cx=200, cy=plan?190:252;
      const left=cx+b[0]*scale, top=cy-(plan?b[3]:b[5])*scale;
      const width=(b[1]-b[0])*scale, height=(plan?b[3]-b[2]:b[5]-b[4])*scale;
      return `<rect x="${left}" y="${top}" width="${width}" height="${height}" fill="${color}" fill-opacity=".22" stroke="${color}" stroke-width="2"><title>${label}</title></rect>`;
    }
    function diagram(r) {
      const figures=['plan','side'].map(mode=>{
        let shapes=rect(r.swept,mode,'#1493bd','Full swept envelope plus horizontal margin');
        shapes+=rect(r.initial,mode,'#496b7e','Assembly at rest');
        for(const [name,b] of Object.entries(r.obstacles)) shapes+=rect(b,mode,name==='PTO'?'#ba6427':name==='sensor'?'#925bb8':'#8c999f',name);
        const raised=r.initial.slice();raised[4]+=r.dz;raised[5]+=r.dz;
        if(mode==='side') shapes+=rect(raised,mode,'#1493bd','Raised assembly');
        return `<figure><svg viewBox="0 0 400 380" role="img" aria-label="${mode==='plan'?'Plan projection of listed objects and the vertical swept corridor':'Side projection of initial and raised assembly, deck, PTO and sensor'}"><text x="16" y="25" fill="currentColor">${mode==='plan'?'PLAN · x / y':'SIDE · x / z'} · metres</text>${shapes}<text x="16" y="365" fill="currentColor">${mode==='plan'?'Projection, not a second collision test':'Vertical translation only: 2.60 m'}</text></svg><figcaption>${mode==='plan'?'Plan projections can overlap even when z differs.':'Whole shaft-inclusive module, not rotor alone.'}</figcaption></figure>`;
      }).join('');
      get('diagram').innerHTML=figures;
    }
    function update() {
      const input={layout:get('layout').value};fields.forEach(k=>input[k]=number(k));
      const axial=input.layout!=='CF-LIFT-2';fields.forEach(k=>get(k).disabled=axial);
      get('diagram').replaceChildren();get('details').textContent='';
      try {
        const r=globalThis.TidalClearance.evaluate(input);
        panel.dataset.result=r.status;
        if(r.status==='UNRESOLVED_MISSING_ENVELOPE') {get('status').textContent='Indeterminate: '+r.reason;return;}
        get('status').textContent=r.conflicts.length ? 'Potential interference: '+r.conflicts.join(', ')+'.' : 'No box interference among the listed objects only. This is not approval.';
        get('details').textContent='Calculated from assumptions: minimum square opening '+r.minimumHatch.toFixed(2)+' m; positive-x PTO centre at least '+r.minimumPtoCenter.toFixed(2)+' m. Full module height 2.65 m; swept top z = 3.55 m. Exact mathematical tangency is accepted; no fabrication tolerance or safety reserve is established.';
        diagram(r);
      } catch(e) {panel.dataset.result='INVALID_INPUT';get('status').textContent='No result: '+e.message;}
    }
    panel.addEventListener('input',event=>{if(event.target && (fields.some(k=>event.target===get(k)) || event.target===get('layout'))) get('preset').value='custom';update();});get('layout').addEventListener('change',update);
    get('preset').addEventListener('change',()=>{
      get('layout').value='CF-LIFT-2';get('margin').value='0.10';get('hatch').value='1.60';
      const p=get('preset').value;get('ptoX').value=p==='inline'?'0':'1.15';get('sensorX').value=p==='sensor'?'0.80':'0.95';update();
    });
    update();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);else init();
})();
