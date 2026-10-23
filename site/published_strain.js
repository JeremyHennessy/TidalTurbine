/* Isolated research-only illustration of OMAE2023 published descriptive statistics.
   Never acquires source instruments or certifies tidal device fatigue or electricity. */
(function(root){
 'use strict';
 const labels=[
  ['mean','Mean peak-to-trough'],
  ['max','Maximum reported difference'],
  ['std','Reported variability']
 ];
 const known=[
  [1,8.1,12.1,4.3,1.1],[2,37.1,118.3,21.7,5.7],
  [3,86.8,120.8,51.0,11.4],[4,55.6,91.3,24.2,10.8],
  [5,21.5,37.3,9.7,4.5],[6,35.7,63.3,17.8,7.0],
  [7,69.7,100.1,40.6,8.0],[8,6.3,10.1,4.1,0.7]
 ];
 function assert(ok,message){if(!ok)throw new Error(message);}
 function escaped(input){return String(input).replace(/[&<>"']/g,c=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
 }[c]));}
 function verify(d,source){
  assert(d&&d.schema==='TT-UNH-2023-PUBLISHED-STRAIN-V1'&&
   d.classification==='PUBLISHED_TABLE_TRANSCRIPTION_AND_BOUNDARY_REVIEW_NOT_ORIGINAL_SENSOR_DATA',
   'Published source table classification invalid');
  assert(d.source?.id==='UNH-2023-OMAE-BLADE-010'&&
   d.source.url==='https://tethys-engineering.pnnl.gov/sites/default/files/publications/Bharath_et_al_2023.pdf'&&
   d.source.source_text_extracted===true&&d.source.visual_pdf_screenshot_confirmed===false&&
   d.source.original_sensor_archives_acquired===false&&
   d.source.original_raw_strain_SI_units_confirmed===false,'Original source measurement unavailable');
  assert(source?.schema==='TT-UNH-2022-ACCESS-GATE-001'&&
   source.verified_original_archives===0&&source.verified_original_readmes===0&&
   source.scientifically_qualified_common_windows===0&&source.contact_authorized===false,
   'Unverified underlying 2022 original data');
  const table=d.table;
  assert(table?.source_date==='2022-11-22'&&table.units===null&&
   table.unit_status==='NOT_PRESENT_IN_EXTRACTED_TABLE_1_TEXT_DO_NOT_ASSIGN_MICROSTRAIN_OR_PASCAL'&&
   table.raw_trace_available===false&&table.stress_transfer_calibrated===false&&
   table.material_fatigue_curve===null&&table.observed_cycles_count===null&&
   JSON.stringify(table.source_highest_mean_gauges)==='[3,7]', 'Strain unit/source must remain unqualified');
  assert(Array.isArray(table.values)&&table.values.length===8,'All eight source gauges required');
  for(let i=0;i<8;i++){
   const x=table.values[i],expected=known[i];
   assert(x.gauge===expected[0]&&
     [x.mean,x.max,x.min,x.std].every((v,j)=>Number.isFinite(v)&&v===expected[j+1])&&
     x.min<=x.mean&&x.mean<=x.max&&x.std>=0,
     'Published Table 1 numeric values altered');
   assert(typeof x.position==='string'&&x.position.length>=10,'Strut location undefined');
  }
  const sys=d.experiment_system,camp=d.published_campaign_context,b=d.project_scientific_boundary;
  assert(d.published_device.blade_count===4&&
   sys.instrumented_blade_operation==='OFF_GRID_DUMP_LOAD'&&
   sys.rectifier_to_dump_resistor_capacity_kW===25&&
   sys.grid_energy_delivery_in_described_test==='NOT_A_NET_GRID_EXPORT_MEASUREMENT'&&
   sys.power_data_average_duration_seconds===1&&
   sys.ADCP_and_CTD_linked_to_main_DAQ_during_paper==='NO'&&
   sys.ADV_probes_near_rotor_induced_velocity===true&&
   sys.phase_resolved_electric_power_validated===false&&
   sys.auxiliary_energy_meter_boundary_verified===false,
   'Off-grid generator/flow/time measurements not qualified');
  assert(camp.rpm_min===18&&camp.rpm_max===31&&
   camp.thrust_mean_kN===6.4&&camp.thrust_peak_kN===11.5&&
   camp.thrust_and_rpm_are_full_deployment_descriptions_not_paired_Table1_samples===true&&
   camp.late_november_2025_analysed_ebb_same_as_Nov22_not_proven===true&&
   camp.sample_specific_undisturbed_upstream_speed_qualified===false,
   'Published November table is not a matched full-study interval');
  assert(b&&Object.entries(b).every(([key,value])=>{
    if(key==='cross_turbine_winner')return value===null;
    return value===false||value===0;
  }), 'No project prototype/load/grid current validation established');
  return {gaugeCount:8,sourceDate:table.source_date,
   rotorBladeCount:d.published_device.blade_count,
   frequencyRangeHz:[1.2,2.066667],
   powerAverageSeconds:sys.power_data_average_duration_seconds,
   authorized:false};
 }
 function selectedRows(d,stat){
  assert(labels.some(x=>x[0]===stat),'Unknown published-statistic selector');
  return d.table.values.map(x=>({gauge:x.gauge,location:x.position,value:x[stat],
    highlighted:x.gauge===3||x.gauge===7}));
 }
 function barsHTML(d,stat){
  const values=selectedRows(d,stat),max=Math.max(...values.map(x=>x.value));
  const meaning=labels.find(x=>x[0]===stat)[1];
  return values.map(x=>{
    const width=(x.value/max*100).toFixed(3);
    const number=x.value.toFixed(1);
    const nearest=x.highlighted?' strain-strut-focus':'';
    const location=x.location.replaceAll('_',' ').toLowerCase();
    return '<div class="strain-gauge-row'+nearest+'" data-published-gauge="'+x.gauge+'">'+
      '<span class="strain-gauge-number">Gauge '+x.gauge+'</span>'+
      '<div class="strain-bar-track" role="img" aria-label="Gauge '+x.gauge+', '+escaped(meaning)+
      ' '+number+' as printed, original numerical units not verified, '+escaped(location)+'">'+
      '<div class="strain-bar-fill" style="width:'+width+'%"></div></div>'+
      '<span class="strain-gauge-value">'+number+'</span>'+
      '</div>';
  }).join('');
 }
 async function mount(doc,fetcher){
  const panel=doc.getElementById('published-strain-lab');
  if(!panel)return;
  const get=id=>doc.getElementById(id);
  const status=get('published-strain-status'),bars=get('published-strain-bars'),
    controls=get('published-strain-controls'),cap=get('published-strain-caption'),
    facts=get('published-strain-facts');
  panel.dataset.status='LOADING';
  try {
   const [a,b]=await Promise.all([
    fetcher('../research/UNH_2023_PUBLISHED_STRAIN_001.json',{cache:'no-cache'}),
    fetcher('../research/UNH_2022_SOURCE_ACCESS_001.json',{cache:'no-cache'})
   ]);
   assert(a.ok&&b.ok,'Published table or source-blocking metadata unavailable');
   const [d,source]=await Promise.all([a.json(),b.json()]);
   const meta=verify(d,source);
   let selected='mean';
   controls.innerHTML=labels.map(([key,label])=>
    '<button type="button" data-published-stat="'+key+
    '" aria-pressed="'+String(key===selected)+'">'+escaped(label)+'</button>'
   ).join('');
   function redraw(){
    bars.innerHTML=barsHTML(d,selected);
    bars.dataset.statistic=selected;
    controls.querySelectorAll('[data-published-stat]').forEach(button=>
     button.setAttribute('aria-pressed',String(button.dataset.publishedStat===selected)));
    cap.textContent=labels.find(x=>x[0]===selected)[1]+
      ' as printed in Table 1; original numeric units not verified. These are processed per-revolution differences, not calibrated stress or original sample traces.';
   }
   controls.addEventListener('click',event=>{
    const button=event.target.closest('[data-published-stat]');
    if(!button||!controls.contains(button))return;
    const name=button.dataset.publishedStat;
    if(!labels.some(x=>x[0]===name))return;
    selected=name;redraw();
   });
   redraw();
   facts.innerHTML='<div><strong>22 Nov 2022</strong><small>Table 1 example — a different field turbine</small></div>'+
     '<div><strong>Gauge 3 &amp; 7</strong><small>Largest reported mean cycle differences, near struts</small></div>'+
     '<div><strong>OFF GRID</strong><small>Rectifier to resistor load — NOT net grid export</small></div>'+
     '<div><strong>1-second</strong><small>Published power averages; not phase-resolved blade-passage power</small></div>'+
     '<div><strong>18–31 rpm</strong><small>Wider deployment context, NOT necessarily this same Nov22 interval</small></div>';
   status.textContent='Published source statistics only: 8 gauge positions. Units and original time-series unverified; 0 qualified project blade-stress/net-electricity results.';
   panel.dataset.status='PUBLISHED_TABLE_ONLY';
  }catch(err){
   panel.dataset.status='UNAVAILABLE';
   status.textContent='Published strain table unavailable or inconsistent; no strain bars or measurements are verified.';
   for(const item of [bars,controls,cap,facts])item.replaceChildren();
   if(root.console?.warn)root.console.warn('Published strain research failed closed:',err.message);
  }
 }
 const api={verify,selectedRows,barsHTML,mount};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
 root.TidalPublishedStrain=api;
 if(root.document&&typeof root.fetch==='function')
  root.document.addEventListener('DOMContentLoaded',()=>mount(root.document,root.fetch.bind(root)));
})(typeof window!=='undefined'?window:globalThis);
