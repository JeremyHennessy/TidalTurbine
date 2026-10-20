/* TidalLab — static, dependency-free research front end.
 * Never convert source metadata into fabricated measured series.
 * Browser cap experiments compare electricity only, NOT blade loads or fatigue.
 */
'use strict';
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const safe = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const numeric = (v, digits = 1) => Number(v).toLocaleString('en-CA', {minimumFractionDigits:digits, maximumFractionDigits:digits});
let report = null;
let ocean = [];
let selected = 'seabed';
let annotations = true;
const VALIDATION = [
  ['Analytical checks & screening', 'Analytical limiting cases, deterministic code and the synthetic SCREEN-001 baseline.', 'SOFTWARE CHECKS PASSED', 'complete'],
  ['Reproduce published benchmark', 'Reproduce independently measured Sandia RM1 geometry, Cp/Ct curves and documented uncertainty.', 'NOT YET REPRODUCED', 'pending'],
  ['Validated rotor & control', 'Turbulence, validated thrust/pitch maps, cavitation and measured blade-load distributions.', 'NOT STARTED', 'pending'],
  ['Coupled structure and moorings', 'Fatigue damage, foundation/cable stresses and floating-platform response under real conditions.', 'NOT STARTED', 'pending'],
  ['Serviceability & lifecycle cost', 'Maintenance histories, realistic weather access windows, failure and repair uncertainty.', 'NOT STARTED', 'pending'],
  ['Independent physical review', 'Independently reviewed testing and ecological evaluation before a site claim.', 'NOT STARTED', 'pending']
];
const DESIGNS = {
  seabed:{short:'Seabed HAT',name:'Seabed horizontal-axis turbine',index:'01',sub:'Fixed-bottom reference architecture · horizontal-axis rotor',caption:'Fixed foundation / submerged nacelle / open rotor',desc:'Conventional architecture for a comparison baseline. No novel rotor geometry or validated structure is asserted.', pros:['Simpler stationary support geometry than a moored surface platform','Existing horizontal-axis performance literature provides benchmark opportunities','No surface hull exposed to waves'],risks:['Subsea retrieval and repair may require specialized vessels','Foundation, scour, cable and pressure-sealing requirements','Flow reversal, shear and fatigue loads remain unresolved'],evidence:'Measured Cp/Ct, hub-height flow profiles, foundation geology, access windows and failure/repair records.'},
  floating:{short:'Recoverable',name:'Floating recoverable turbine',index:'02',sub:'Surface access / recoverable submerged modules',caption:'Surface structure / submerged drivetrain / anchored moorings',desc:'Known floating/retractable concepts suggest an access advantage, but introduce moorings, joints, connectors and wave-exposed components.',pros:['Potential dry or surface-level service access','Recoverable modules could shorten some repair operations','Less dependence on heavy underwater foundation retrieval'],risks:['Added mooring and platform loads','Dynamic cable or electrical connector fatigue','Surface interactions, storm access and navigation conflicts'],evidence:'Matched access-window simulations, mooring response, connector cycles and documented service duration/cost from deployed devices.'},
  crossflow:{short:'Cross-flow',name:'Cross-flow vertical-axis turbine',index:'03',sub:'Bidirectional cross-flow architecture',caption:'Vertical-axis rotor / alternative powertrain configuration',desc:'A cross-flow rotor may handle directional changes differently, but efficiency, torque variation and fatigue must be established.',pros:['Orientation may be less dependent on active yaw','Rotor layout can offer alternative packaging and recovery','Potentially suitable for some shallow/reversing regimes'],risks:['Strong cyclic blade loading and torque ripple can occur','Support-arm and blade bending stresses require evaluation','Comparative power coefficient remains unverified here'],evidence:'Reproducible Cp/CT versus TSR with turbulence, torque ripple, structural and maintenance measurements.'},
  kite:{short:'Tidal kite',name:'Tethered tidal kite',index:'04',sub:'Moving wing / tether / subsea power path',caption:'Swept trajectory / flying wing / tether anchor',desc:'A moving wing uses a large effective swept path. Its controls, tether loads, entanglement and retrieval introduce distinct failure modes.',pros:['Dynamic motion can increase relative flow at rotor','Device altitude can be adapted within suitable water columns','Some subsystems could potentially be retrieved'],risks:['Complex flight control and fault-response requirements','Tether wear, swept area, fishing activity and marine life interactions','Navigation and flight envelope require explicit environmental constraints'],evidence:'Measured trajectory and effective velocity, tether force/fatigue, control fault behavior and independently reviewed ecology.'}
};
function go(view) {
  if (!['overview','designs','experiments','ocean','research'].includes(view)) view = 'overview';
  $$('.view').forEach(el=>el.classList.toggle('current',el.id==='view-'+view));
  $$('.nav-link').forEach(el=>{const active=el.dataset.go===view;el.classList.toggle('active',active);if(active) el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');});
  const rail=$('#sidebar'); rail.classList.remove('open'); $('#menu-toggle').setAttribute('aria-expanded','false');
  if(location.hash!=='#'+view) history.replaceState(null,'','#'+view);
  window.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
}
function initNavigation() {
  $$('[data-go]').forEach(btn=>btn.addEventListener('click',()=>go(btn.dataset.go)));
  $('#menu-toggle').addEventListener('click',()=>{const rail=$('#sidebar');const open=rail.classList.toggle('open');$('#menu-toggle').setAttribute('aria-expanded',String(open));});
  document.addEventListener('keydown',(e)=>{if(e.key==='Escape'){ $('#sidebar').classList.remove('open');$('#menu-toggle').setAttribute('aria-expanded','false');}});
  window.addEventListener('hashchange',()=>go(location.hash.slice(1)));
  go(location.hash.slice(1)||'overview');
}
function renderStats(){
  const stats=[['▤','21','Core research references','From the foundation catalogue'],['⚗',report?'1':'—','Synthetic experiment', 'SCREEN-001 · repeatable'],['≋',ocean.length?String(ocean.length):'—','Ocean-data records','Source metadata · not raw files'],['◇','0','Validated turbine concepts','Physical validation pending']];
  $('#stats').innerHTML=stats.map(([icon,val,name,desc])=>`<div class="stat"><span class="stat-icon" aria-hidden="true">${icon}</span><div><strong>${val}</strong><span class="stat-label">${name}</span><small>${desc}</small></div></div>`).join('');
}
function chartSvg(cap=0.8, overview=false){
  if(!report) return '<p class="empty">Archived report unavailable. Check static site build.</p>';
  const t=report.turbine,c=report.synthetic_current, maxP=t.rated_power_kw;
  const width=680,height=overview?260:300,L=48,R=16,T=17,B=34, plotW=width-L-R,plotH=height-T-B;
  const series=[];
  for(let j=0;j<=384;j++){
    const hrs=j*48/384;
    const phase1=2*Math.PI*hrs/c.primary_period_hours;
    const phase2=2*Math.PI*hrs/c.secondary_period_hours+c.secondary_phase_rad;
    const v=Math.abs(c.primary_amplitude_m_s*Math.sin(phase1)+c.secondary_amplitude_m_s*Math.sin(phase2));
    const p=v<t.cut_in_m_s?0:Math.min(maxP,.5*t.seawater_density_kg_m3*t.swept_area_m2*t.power_coefficient*t.conversion_efficiency*v**3/1000);
    series.push([hrs,p,Math.min(p,maxP*cap)]);
  }
  const xx=h=>L+h/48*plotW,yy=p=>T+plotH*(1-p/maxP);
  const points=i=>series.map(d=>`${xx(d[0]).toFixed(2)},${yy(d[i]).toFixed(2)}`).join(' ');
  let grid='';for(let i=0;i<=4;i++){const v=maxP*i/4,y=yy(v);grid+=`<line x1="${L}" y1="${y}" x2="${width-R}" y2="${y}" stroke="#315365" opacity=".65" stroke-dasharray="3 6"/><text x="${L-10}" y="${y+4}" fill="#90adb8" font-size="11" text-anchor="end">${numeric(v,0)}</text>`;}
  for(let i=0;i<=4;i++){const hr=i*12;grid+=`<text x="${xx(hr)}" y="${height-9}" fill="#8faeba" text-anchor="middle" font-size="11">${hr}h</text>`;}
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Synthetic power profile over 48 hours. Cyan baseline and amber export-capped curves; values generated from assumed current, not observations."><g font-family="Arial, sans-serif">${grid}<text transform="translate(13 ${height/2+15}) rotate(-90)" fill="#8faeba" text-anchor="middle" font-size="11">Export power (kW)</text><polyline fill="none" stroke="#52d9fb" stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" points="${points(1)}"/><polyline fill="none" stroke="#ffc475" stroke-linejoin="round" stroke-linecap="round" stroke-width="2.25" points="${points(2)}"/></g></svg>`;
}
function energyFor(cap){
  // Deliberately replicates the Python midpoint algorithm for an ephemeral browser illustration.
  // Cap is downstream of the fixed Cp power curve and has NO physical-load interpretation.
  const t=report.turbine,c=report.synthetic_current,dt=report.baseline.timestep_s,seconds=report.baseline.duration_days*86400;
  let sum=0;
  for(let ts=0;ts<seconds;ts+=dt){
    const step=Math.min(dt,seconds-ts),hrs=(ts+step/2)/3600;
    const v=Math.abs(c.primary_amplitude_m_s*Math.sin(2*Math.PI*hrs/c.primary_period_hours)+c.secondary_amplitude_m_s*Math.sin(2*Math.PI*hrs/c.secondary_period_hours+c.secondary_phase_rad));
    const p=v<t.cut_in_m_s?0:Math.min(t.rated_power_kw,.5*t.seawater_density_kg_m3*t.swept_area_m2*t.power_coefficient*t.conversion_efficiency*v**3/1000);
    sum+=Math.min(p,t.rated_power_kw*cap)*step/3600;
  }
  return sum;
}
function experimentRender(){
  if(!report)return;
  const cap=Number($('#export-slider').value)/100;
  const base=report.baseline.energy_kwh;
  const comparison=Math.abs(cap-.8)<1e-10?report.comparison.energy_kwh:energyFor(cap);
  const pct=base?100*(base-comparison)/base:0;
  $('#export-value').textContent=Math.round(cap*100)+'%';
  $('#experiment-chart').innerHTML=chartSvg(cap);
  $('#experiment-kpis').innerHTML=`<div><span>Baseline / 14 days</span><strong>${numeric(base)} <small>kWh</small></strong></div><div><span>Export-limited energy</span><strong>${numeric(comparison)} <small>kWh</small></strong></div><div><span>Export energy penalty</span><strong>${numeric(pct,2)}%</strong></div>`;
  $('#experiment-note').textContent=cap===.8?'Archived 80% cap case from published SCREEN-001.json. Chart is a reconstructed 48-hour subset.':'Unarchived browser-only what-if; Python report not modified. Neither calculation predicts blade loads or fatigue.';
}
function miniOverview(){
  if(report){
    $('#overview-chart').innerHTML=`<div class="legend" style="padding:0 0 3px"><span><i class="line-swatch cyan"></i>Baseline</span><span><i class="line-swatch amber"></i>80% export cap</span></div>${chartSvg(.8,true)}`;
    const base=report.baseline.energy_kwh,cmp=report.comparison.energy_kwh;
    $('#overview-results').innerHTML=`<div class="result-cell"><span>Baseline / 14 days</span><strong>${numeric(base)} kWh</strong></div><div class="result-cell"><span>80% export cap</span><strong>${numeric(cmp)} kWh</strong></div><div class="result-cell"><span>Energy penalty</span><strong class="accent">${numeric(report.difference_export_energy_percent,2)}%</strong></div>`;
  }else {$('#overview-chart').innerHTML='<p class="empty">Archived experiment unavailable</p>';}
  const names=[['01','FORCE ADCP currents','Measured 2018 profiles, not ingested','≋'],['02','CHS water levels','Gauge observations and predictions, not current speed','◉'],['03','Fundy bathymetry','NONNA / GEBCO terrain records','▦'],['04','DFO ecology','Habitats, marine use and monitoring','♧']];
  $('#mini-data-list').innerHTML=names.map(([id,title,desc,icon])=>`<div class="mini-data-row"><span class="data-icon">${icon}</span><span><strong>${title}</strong><small>${desc}</small></span><span class="arrow">›</span></div>`).join('');
  $('#mini-gates').innerHTML=VALIDATION.map(([title,subtitle,state,kind],i)=>`<div class="gate-row"><span class="gate-num ${kind==='complete'?'complete':''}">${i+1}</span><span class="gate-text"><strong>${safe(title)}</strong><small>${safe(subtitle.slice(0,67))}${subtitle.length>67?'…':''}</small></span><span class="gate-check">${kind==='complete'?'✓':'○'}</span></div>`).join('');
  $('#research-gates').innerHTML=VALIDATION.map(([title,desc,state,kind],i)=>`<div class="research-gate"><span class="research-gate-num ${kind==='complete'?'active':''}">${i+1}</span><div class="research-gate-content"><h3>${safe(title)}</h3><p>${safe(desc)}</p><small>${safe(state)}</small></div></div>`).join('');
}
function sensitivityRender(){
  if(!report||!report.sensitivity)return;
  const arr=report.sensitivity;const min=Math.min(...arr.map(x=>x.energy_kwh)),max=Math.max(...arr.map(x=>x.energy_kwh));
  const w=900,h=210,L=69,R=15,T=21,B=34,px=x=>L+(x-1.5)/(3-1.5)*(w-L-R),py=y=>T+(max-y)/(max-min)*(h-T-B);
  const areas=[1.5,2,2.5,3];
  const circles=arr.map((x,i)=>{const cx=px(x.primary_amplitude_m_s),cy=py(x.energy_kwh);const color=x.power_coefficient>.4?'#53e2cf':x.power_coefficient<.4?'#6d93b6':'#ffc476';return `<circle cx="${cx}" cy="${cy.toFixed(2)}" r="3.8" fill="${color}" fill-opacity=".72" stroke="#0a2432" stroke-width=".7"><title>Assumed amplitude ${x.primary_amplitude_m_s} m/s, Cp ${x.power_coefficient}; ${numeric(x.energy_kwh)} kWh</title></circle>`;}).join('');
  const axes=areas.map(a=>`<line x1="${px(a)}" x2="${px(a)}" y1="${T}" y2="${h-B}" stroke="#315564" stroke-dasharray="3 6"/><text x="${px(a)}" y="${h-12}" text-anchor="middle" fill="#8fadb7" font-size="11">${a.toFixed(1)}</text>`).join('');
  $('#sensitivity-plot').innerHTML=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="81 archived sensitivity cases: assumed primary tidal amplitude against synthetic 14-day electrical energy. Colored points distinguish assumed power coefficients."><g font-family="Arial">${axes}<line x1="${L}" x2="${w-R}" y1="${h-B}" y2="${h-B}" stroke="#4e7b89"/><text x="${L-6}" y="${T+5}" text-anchor="end" font-size="10" fill="#9eb4c0">${Math.round(max/1000)} MWh</text><text x="${L-6}" y="${h-B}" text-anchor="end" font-size="10" fill="#9eb4c0">${Math.round(min/1000)} MWh</text>${circles}<text x="${w/2}" y="${h-1}" text-anchor="middle" font-size="11" fill="#a1c1ca">Assumed primary current amplitude (m/s)</text></g></svg>`;
}
// Drawings are design-language mockups (not physics-based engineering geometry).
function designDefs(){return `<defs><radialGradient id="oceanGlow"><stop stop-color="#164e63"/><stop offset="1" stop-color="#071b2a"/></radialGradient><linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#79dbe8"/><stop offset=".24" stop-color="#225f76"/><stop offset=".58" stop-color="#164456"/><stop offset=".79" stop-color="#3da2b6"/><stop offset="1" stop-color="#092c42"/></linearGradient><linearGradient id="blade" x1="0" y1="0" x2="1" y2=".9"><stop stop-color="#9df4fa"/><stop offset=".27" stop-color="#38a9c5"/><stop offset=".63" stop-color="#0e4f72"/><stop offset="1" stop-color="#041b2c"/></linearGradient><linearGradient id="sand" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#174354"/><stop offset="1" stop-color="#081724"/></linearGradient><pattern id="diagramGrid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#2a6071" stroke-width=".65" opacity=".4"/></pattern><filter id="glow"><feGaussianBlur stdDeviation="7"/></filter></defs>`;}
function seabedSvg(){return `<path d="M-30 315 75 297 139 312 205 296 265 310 320 304 365 313 450 291 576 311 690 295V500H-30Z" fill="url(#sand)" stroke="#32657a"/><path d="M-10 353 138 328 229 345 369 330 560 365 682 335" fill="none" stroke="#275567"/><path d="M336 315V175H360V315" fill="url(#metal)" stroke="#5eabbc" stroke-width="2"/><path d="M302 324h95l-17 24h-65z" fill="url(#metal)" stroke="#398199" stroke-width="2"/><path d="M318 348v13m60-13v13m-41-10v15m42-13 65 21" fill="none" stroke="#439cad" stroke-width="3"/><ellipse cx="358" cy="355" rx="70" ry="11" fill="#0c354c" opacity=".7"/><rect x="337" y="153" width="102" height="49" rx="23" fill="url(#metal)" stroke="#6daabb" stroke-width="2"/><path d="M377 154v47m38-39v34" stroke="#a7e3e4" stroke-width="2" opacity=".55"/><ellipse cx="337" cy="177" rx="17" ry="28" fill="#2d889f" stroke="#89dce2"/><g transform="translate(328 177)"><path d="M0-2Q-17-58-7-124Q-4-145 4-142Q16-124 14-90L14-11Z" fill="url(#blade)" stroke="#8dcddd" stroke-width="1.6"/><path d="M0-2Q-17-58-7-124" fill="none" stroke="#a4f6ee" opacity=".6" stroke-width="1.4"/><path d="M0-2Q-17-58-7-124Q-4-145 4-142Q16-124 14-90L14-11Z" fill="url(#blade)" stroke="#8dcddd" stroke-width="1.6" transform="rotate(120)"/><path d="M0-2Q-17-58-7-124Q-4-145 4-142Q16-124 14-90L14-11Z" fill="url(#blade)" stroke="#8dcddd" stroke-width="1.6" transform="rotate(240)"/><circle r="17" fill="url(#metal)" stroke="#a5f9e9" stroke-width="2"/><circle r="5" fill="#b4faf2"/></g><path d="M439 182q70 26 77 111l44 67" fill="none" stroke="#52bfd0" stroke-width="4" stroke-linecap="round"/>`;}
function floatingSvg(){return `<g><path d="M0 122 Q70 116 140 123T280 122T420 122T560 122T700 122" fill="none" stroke="#63cae3" stroke-width="3"/><path d="M-20 129Q88 139 180 128T350 133T570 132T690 140" fill="none" stroke="#167d8b" stroke-width="2"/><path d="M202 103q-8 26 28 33h254q30-9 16-33z" fill="url(#metal)" stroke="#9bd7d8" stroke-width="2"/><rect x="260" y="75" width="169" height="30" rx="5" fill="#2d7282" stroke="#6fc0c8"/><rect x="295" y="62" width="75" height="15" rx="3" fill="#60b5c3"/><path d="M240 137v97m217-97v97" stroke="#68bdd1" stroke-width="11"/><rect x="218" y="203" width="73" height="45" rx="21" fill="url(#metal)" stroke="#63c7d5"/><rect x="416" y="203" width="75" height="45" rx="21" fill="url(#metal)" stroke="#63c7d5"/><g transform="translate(217 225)"><path d="M0-10Q-18-59-8-82Q10-84 12-62L7-5Z" fill="url(#blade)" stroke="#8bdfdf" stroke-width="1.5"/><path d="M0-10Q-18-59-8-82Q10-84 12-62L7-5Z" fill="url(#blade)" stroke="#8bdfdf" transform="rotate(120)"/><path d="M0-10Q-18-59-8-82Q10-84 12-62L7-5Z" fill="url(#blade)" stroke="#8bdfdf" transform="rotate(240)"/><circle r="13" fill="url(#metal)" stroke="#91eeee"/></g><g transform="translate(415 225)"><path d="M0-10Q-16-52-9-78Q7-84 12-58L8-5Z" fill="url(#blade)" stroke="#8bdfdf"/><path d="M0-10Q-16-52-9-78Q7-84 12-58L8-5Z" fill="url(#blade)" stroke="#8bdfdf" transform="rotate(120)"/><path d="M0-10Q-16-52-9-78Q7-84 12-58L8-5Z" fill="url(#blade)" stroke="#8bdfdf" transform="rotate(240)"/><circle r="13" fill="url(#metal)" stroke="#91eeee"/></g><path d="M206 126C184 253 117 329 99 368M484 125C540 242 577 319 615 366" stroke="#6ebdc7" stroke-width="3" fill="none"/><path d="m68 374 31-24 32 24zM581 374l34-24 32 24z" fill="url(#metal)" stroke="#59aeba"/><path d="M-10 371q140-30 260-7t230-4 220 17" fill="none" stroke="#2e6178" stroke-width="3"/></g>`;}
function crossflowSvg(){return `<path d="M-15 353q140-26 283-12t262 0 180-6v75H-15Z" fill="url(#sand)" stroke="#346579"/><path d="M222 335v-212m222 212V123" stroke="#4a92a7" stroke-width="8"/><path d="M211 122h244m-244 218h244" stroke="#5ac0cf" stroke-width="8"/><g><path d="M308 144C393 169 261 243 352 322" stroke="url(#blade)" stroke-width="30" fill="none"/><path d="M348 144C261 169 393 243 304 322" stroke="url(#blade)" stroke-width="30" fill="none"/><path d="M323 135v195" stroke="#8ad2d5" stroke-width="7"/></g><ellipse cx="327" cy="132" rx="60" ry="13" fill="url(#metal)" stroke="#86d1cf"/><ellipse cx="327" cy="329" rx="60" ry="12" fill="url(#metal)" stroke="#86d1cf"/><path d="M302 341v18m50-18v18" stroke="#7dc9ce" stroke-width="5"/><rect x="290" y="356" width="81" height="22" rx="5" fill="#1d5c71" stroke="#3c9db0"/>`;}
function kiteSvg(){return `<path d="M-10 354q135-17 270 2t242-3 195-10v60H-10Z" fill="url(#sand)" stroke="#3a6476"/><rect x="338" y="341" width="100" height="27" rx="7" fill="url(#metal)" stroke="#7dcbd3"/><path d="M386 345 333 180" stroke="#89e9e6" stroke-width="2.5" stroke-dasharray="8 4"/><path d="M334 179 246 161 180 175 274 131 348 121 418 162 498 174 410 182z" fill="url(#blade)" stroke="#8af0e5" stroke-width="2"/><path d="m264 162 66 15 84-15m-149-13 57-13 83 16" fill="none" stroke="#95dadb" opacity=".7"/><circle cx="335" cy="174" r="15" fill="url(#metal)" stroke="#adfff2"/><circle cx="335" cy="174" r="5" fill="#97e3e1"/><path d="M185 185c-55-8-88-38-118-23" fill="none" stroke="#56c9ce" stroke-width="2" stroke-dasharray="5 9"/><path d="M494 198c32 35 41 58 35 91" fill="none" stroke="#56c9ce" stroke-width="2" stroke-dasharray="5 9"/><path d="M95 285Q324 43 556 284" fill="none" stroke="#64a7b6" stroke-dasharray="5 8" opacity=".7"/><text x="483" y="289" fill="#7abcc4" font-size="12">Flight envelope?</text>`;}
function labelSvg(name,large){
  if(!large)return '';
  const configs={seabed:[['Rotor','Assumed 10 m only',104,121,311,158],['Nacelle','Generator housing',502,132,410,172],['Support','Fixed frame',503,281,357,282],['Cable','Indicative route',533,349,487,307]],floating:[['Surface access','Possible service route',74,58,286,106],['Recoverable modules','Retrieval mechanisms TBD',508,192,453,222],['Moorings','Loads unverified',515,312,552,321]],crossflow:[['Cross-flow rotor','Performance unverified',74,155,310,175],['Supports','Cyclic stress TBD',500,130,448,151],['Base','Installation dependent',507,350,359,364]],kite:[['Moving wing','Aerodynamics unverified',81,83,285,143],['Tether','Wear and fatigue unknown',501,278,354,240],['Anchor','Seabed assessment pending',83,332,357,351]]};
  return (configs[name]||[]).map(([t,d,x,y,tx,ty])=>{const right=x>400,joinX=right?x-12:x+140;return `<g class="diagram-annotations"><circle cx="${tx}" cy="${ty}" r="4" fill="#66f0e1"/><path d="M${tx} ${ty} ${joinX} ${y-10}" stroke="#5de9e0" stroke-width="1.2" fill="none"/><rect x="${x}" y="${y-32}" width="${right?167:146}" height="49" rx="7" fill="#081d2d" opacity=".87" stroke="#36748a"/><text x="${x+10}" y="${y-14}" font-size="11" font-weight="bold" fill="#93f7e8">${safe(t)}</text><text x="${x+10}" y="${y+2}" font-size="9" fill="#b1d1d5">${safe(d)}</text></g>`;}).join('');
}
function designSvg(name,large=false){
  const drawing={seabed:seabedSvg,floating:floatingSvg,crossflow:crossflowSvg,kite:kiteSvg}[name]();
  const waves=Array.from({length:7},(_,i)=>`<path d="M-12 ${126+i*28}q90-15 170 0t180 0t180 0t180 0" fill="none" stroke="#27899a" stroke-width="1" opacity="${.11+i*.02}"/>`).join('');
  return `<svg viewBox="0 0 700 410" role="img" aria-label="Illustrative technical drawing of ${safe(DESIGNS[name].name)}. Not to scale and not a tested engineering design.">${designDefs()}<rect width="700" height="410" fill="url(#oceanGlow)"/><rect width="700" height="410" fill="url(#diagramGrid)" opacity=".42"/>${waves}<g opacity=".85"><path d="M0 80H700" stroke="#25768c" stroke-dasharray="2 9"/><text x="20" y="32" fill="#6ba7b8" font-size="11" font-family="Arial" letter-spacing="2">TIDAL / LAB — ${DESIGNS[name].index} · CONCEPT</text><text x="675" y="32" text-anchor="end" fill="#6ba7b8" font-size="11">ILLUSTRATIVE / NOT TO SCALE</text></g>${drawing}${(annotations||!large)?labelSvg(name,large):''}<g stroke="#5e94a2" opacity=".65" stroke-width="1"><path d="M24 383h90m-90-6v12m90-12v12"/></g><text x="127" y="388" font-size="10" fill="#6aabba">Not a calibrated scale</text></svg>`;
}
function renderDesign(){
  const d=DESIGNS[selected];
  $('#overview-design').innerHTML=designSvg(selected);
  $('#overview-design-caption').textContent=d.caption;
  $('#design-viewport').innerHTML=designSvg(selected,true);
  $('#design-title').textContent=d.name;
  $('#design-subtitle').textContent=d.sub;
  $('#design-context').textContent=d.desc;
  $('#design-pros').innerHTML=d.pros.map(x=>`<li>${safe(x)}</li>`).join('');
  $('#design-risks').innerHTML=d.risks.map(x=>`<li>${safe(x)}</li>`).join('');
  $('#design-evidence').textContent=d.evidence;
  $$('.design-choice').forEach(e=>e.classList.toggle('active',e.dataset.design===selected));
}
function setupDesign(){
  $('#design-selector').innerHTML=Object.entries(DESIGNS).map(([key,d])=>`<button class="design-choice ${key===selected?'active':''}" data-design="${key}"><small>CONCEPT ${d.index}</small><strong>${d.short}</strong><span>${d.sub}</span></button>`).join('');
  $$('.design-choice').forEach(btn=>btn.addEventListener('click',()=>{selected=btn.dataset.design;renderDesign();}));
  $('#toggle-annotation').addEventListener('click',()=>{annotations=!annotations;const b=$('#toggle-annotation');b.classList.toggle('on',annotations);b.setAttribute('aria-pressed',String(annotations));b.textContent=annotations?'◈ Labels on':'◇ Labels off';renderDesign();});
  renderDesign();
}
const CATEGORY_LABELS={current:'Currents',waves:'Waves',weather:'Weather',water_level:'Tide heights',bathymetry:'Bathymetry',seabed:'Seabed',discovery:'Discovery',hydrography:'Hydrography',habitat:'Habitat',species:'Species',marine_use:'Marine use',environment:'Monitoring',regulation:'Regulation'};
function statusLabel(s){return ({downloadable_not_acquired:'File available · not ingested',metadata_only:'Metadata only',permission_gate:'Terms/access gate',portal_manual_download:'Portal download required',discovery_portal:'Discovery only',report_not_machine_read:'Report only',source_reviewed:'Web page reviewed'})[s]||'Needs review';}
function oceanRender(){
  $('#catalogue-heading').textContent=ocean.length+' source records catalogued';
  const cat=[...new Set(ocean.map(x=>x.category))].sort();
  $('#type-filter').innerHTML='<option value="all">All categories</option>'+cat.map(x=>`<option value="${safe(x)}">${safe(CATEGORY_LABELS[x]||x)}</option>`).join('');
  const paint=()=>{
    const q=$('#data-search').value.toLowerCase().trim(),typ=$('#type-filter').value;
    const filtered=ocean.filter(x=>(typ==='all'||x.category===typ)&&(!q||[x.title,x.provider,x.region,x.id,x.category].join(' ').toLowerCase().includes(q)));
    $('#dataset-body').innerHTML=filtered.map(x=>`<tr><td><strong>${safe(x.title)}</strong><small>${safe(x.id)} · ${safe(x.provider)}</small></td><td>${safe(CATEGORY_LABELS[x.category]||x.category)}</td><td><span class="tag ${x.access_status==='downloadable_not_acquired'?'tag-green':'tag-grey'}">${safe(statusLabel(x.access_status))}</span></td><td><a href="${safe(x.source_url)}" target="_blank" rel="noopener noreferrer">Primary source ↗</a><br><button class="plain-link dataset-detail" data-detail="${safe(x.id)}" aria-expanded="false">Metadata ↓</button></td></tr><tr class="detail-row" id="detail-${safe(x.id)}" hidden><td colspan="4"><div class="detail-grid"><div><b>Observation / variables</b><p>${safe(x.variables.join(', '))}</p><b>Units / depth</b><p>${safe(x.units.join(' · '))}; ${safe(x.depth_reference)}</p></div><div><b>Period / cadence</b><p>${safe(x.temporal_coverage)}; ${safe(x.sampling_interval)}</p><b>Reuse / quality</b><p>${safe(x.license)}. ${safe(x.quality_flags)}</p></div><div><b>Limitations</b><p>${safe(x.limitations)}</p><b>Next acquisition step</b><p>${safe(x.next_action)}</p>${x.download_url?`<a href="${safe(x.download_url)}" target="_blank" rel="noopener noreferrer">Source download ↗</a>`:''}</div></div></td></tr>`).join('');
    $('#dataset-empty').hidden=!!filtered.length;
    $$('.dataset-detail').forEach(b=>b.addEventListener('click',()=>{const row=$('#detail-'+b.dataset.detail);const now=row.hidden;row.hidden=!now;b.setAttribute('aria-expanded',String(now));b.textContent=now?'Metadata ↑':'Metadata ↓';}));
  };
  $('#data-search').addEventListener('input',paint);$('#type-filter').addEventListener('change',paint);paint();
}
function enhanceStyles(){const style=document.createElement('style');style.textContent='.detail-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;background:#0e2a38;padding:16px;border-radius:8px}.detail-grid b{font-size:11px;color:#7de8dd}.detail-grid p{font-size:11px;color:#aac4ca;line-height:1.6;margin:5px 0 14px}.detail-grid a{font-size:11px}.dataset-table .detail-row td{padding:0}.detail-row[hidden]{display:none}@media(max-width:760px){.detail-grid{grid-template-columns:1fr}}';document.head.appendChild(style);}
async function init(){
  initNavigation();enhanceStyles();setupDesign();miniOverview();renderStats();
  try{const r=await fetch('../reports/SCREEN-001.json',{cache:'no-cache'});if(!r.ok)throw Error('Report fetch '+r.status);report=await r.json();if(report.inflow_kind!=='synthetic_two_harmonic'||report.classification!=='SIMULATION_RESULT_SYNTHETIC_NOT_VALIDATED')throw Error('Invalid provenance classification');}catch(e){console.warn('Archive unavailable',e);}
  try{const r=await fetch('../research/ocean_datasets.json',{cache:'no-cache'});if(!r.ok)throw Error('Inventory fetch '+r.status);ocean=await r.json();if(!Array.isArray(ocean))throw Error('Inventory not a list');}catch(e){console.warn('Data registry unavailable',e);}
  renderStats();miniOverview();sensitivityRender();experimentRender();oceanRender();
  $('#export-slider').addEventListener('input',experimentRender);
  $('#reset-experiment').addEventListener('click',()=>{$('#export-slider').value='80';experimentRender();});
}
document.addEventListener('DOMContentLoaded',init);
