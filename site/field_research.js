/* Source-backed Research view only. Not an instrumentation or data-acquisition client. */
(function(root){
 'use strict';
 const categories={inflow_3d:'flow',fluid_state:'flow',rotor_position:'mechanics',
 rotor_speed:'mechanics',shaft_torque:'mechanics',mean_streamwise_drag:'mechanics',
 blade_root_strain:'structure',strut_strain:'structure',generator_power:'electric',
 delivered_electrical_power:'electric',control_and_actuator_power:'electric',rig_status:'status'};
 const titles={inflow_3d:'Upstream velocity',fluid_state:'Water state',
 rotor_position:'Rotor phase',rotor_speed:'Rotor speed',shaft_torque:'Shaft torque',
 mean_streamwise_drag:'Support drag',blade_root_strain:'Blade-root strain',
 strut_strain:'Strut strain',generator_power:'Generator-side power',
 delivered_electrical_power:'Delivered electricity',control_and_actuator_power:'Auxiliary power',
 rig_status:'Fault / safety events'};
 const filters=[['all','All'],['flow','Flow'],['mechanics','Rotor loads'],
 ['structure','Strain'],['electric','Electric'],['status','Safety']];
 function guard(ok,message){if(!ok)throw new Error(message);}
 function encode(value){return String(value).replace(/[&<>"']/g,function(c){
   return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
 });}
 function validURL(value){guard(typeof value==='string'&&/^https:\/\/[a-z0-9.-]+\//i.test(value)
   && !/[<>"']/.test(value),'Invalid publication URL');return value;}
 function verify(e,p){
   guard(e&&e.schema==='TT-FIELD-STRAIN-EVIDENCE-001'&&
    e.classification==='PUBLISHED_SOURCE_DISCOVERY_NO_PROJECT_LOAD_OR_ELECTRICAL_VALIDATION',
    'Unqualified field-source classification');
   guard(p&&p.schema==='TT-METROLOGY-PREREG-V1'&&
    p.status==='BLOCKED_REQUIRES_INDEPENDENT_METROLOGY_AND_STATISTICAL_REVIEW',
    'Unqualified laboratory metrology data');
   guard(e.project_measurements&&Object.values(e.project_measurements).length===5
     &&Object.values(e.project_measurements).every(x=>x===0),'Project physical evidence not acquired');
   const d=e.field_dataset;
   guard(d&&d.status==='CATALOG_METADATA_ONLY'&&d.original_archives_acquired===0
    &&d.qualified_joint_intervals===0&&d.resource_count===17,'Raw files not science qualified');
   validURL(d.url);
   const caseEvidence=e.publication_reported_case;
   guard(caseEvidence &&
    caseEvidence.source_id==='UNH-STRAIN-PAPER-2025-008' &&
    caseEvidence.evidence_class==='PUBLISHED_EVIDENCE_PREVIEW_EXCERPT_NOT_SOURCE_SENSOR_VALIDATION' &&
    caseEvidence.interval_description==='LATE_NOVEMBER_2022_EBB_TIDE_UNDATED' &&
    JSON.stringify(caseEvidence.reported_synchronized_families)===
      JSON.stringify(['STRAIN','THRUST','ADV_UPSTREAM','ADV_DOWNSTREAM']) &&
    caseEvidence.reported_upstream_adcp==='LEAK_DAMAGE_DATA_UNRECOVERABLE_IN_PAPER_ANALYZED_EVENT' &&
    caseEvidence.electrical_power_same_analyzed_event==='UNKNOWN_NOT_STATED_IN_RESULTS_EXCERPT' &&
    caseEvidence.rectifier_power_boundary==='UNVERIFIED_NOT_NET_DELIVERED' &&
    caseEvidence.exact_interval_start_utc===null &&
    caseEvidence.exact_interval_end_utc===null &&
    caseEvidence.original_source_bytes_acquired===0 &&
    caseEvidence.original_overlap_utc_verified===false &&
    caseEvidence.results_excerpt_not_full_methods===true &&
    caseEvidence.qualification==='AUTHOR_REPORTED_SOME_SYNCHRONIZATION_NOT_INDEPENDENTLY_REPRODUCED',
    'Publication preview cannot become qualified exact source interval or net electricity');
   validURL(caseEvidence.publisher_preview_url);
   guard(Array.isArray(d.families)&&d.families.length===5
    &&new Set(d.families.map(x=>x.key)).size===5,'Instrument families missing');
   guard(Array.isArray(e.studies)&&e.studies.length===3
    &&new Set(e.studies.map(x=>x.id)).size===3,'Three source-scoped studies required');
   e.studies.forEach(s=>{validURL(s.url);guard(s.title&&s.finding&&s.limitation&&s.scope,
    'Research study must show evidence and limitation');});
   const gates=e.hard_gates;
   guard(gates&&gates.calibration_channels_unverified===11
    &&gates.measurement_gates_unresolved===9&&gates.contact_authorized===false
    &&gates.physical_test_authorized===false&&gates.prototype_winner===null,
    'Physical or user approval not earned');
   guard(p.measured_results&&p.measured_results.project_physical_test_count===0
    &&p.measured_results.project_net_electricity_measured===false
    &&p.measured_results.physical_blade_stress_measured===false
    &&p.measured_results.qualified_force_site_inflow_rows===0
    &&p.contact_and_physical_boundaries.contact_anyone_authorized===false,
    'Existing measurement data must remain unexecuted');
   const c=p.channels;
   guard(Array.isArray(c)&&c.length===12&&new Set(c.map(x=>x.id)).size===12
    &&c.every(x=>categories[x.id]&&x.calibration_record===null&&x.raw_signal_sha256===null),
    'All original channels still require source calibration');
   guard(c.filter(x=>x.calibration_required).length===11,'Eleven numeric channels not calibrated');
   guard(Array.isArray(p.independent_acceptance_gates)
    &&p.independent_acceptance_gates.length===9
    &&p.independent_acceptance_gates.every(x=>x.state==='UNRESOLVED'),
    'Physical acceptance gates not qualified');
   return {channels:12,numericUnqualified:11,gatesUnresolved:9,studies:3};
 }
 function subset(channels,filter){
  guard(filters.some(f=>f[0]===filter),'Invalid filter');
  return channels.filter(x=>filter==='all'||categories[x.id]===filter);
 }
 function channelCards(channels,filter){
  return subset(channels,filter).map(c=>
    '<article class="field-channel" data-channel-id="'+encode(c.id)+'">'+
    '<div class="field-channel-head"><strong>'+encode(titles[c.id])+'</strong><small>'+
    (c.id==='rig_status'?'LOG UNKNOWN':'NO CALIBRATION')+'</small></div>'+
    '<p>'+encode(c.role.replaceAll('_',' ').toLowerCase())+'</p>'+
    '<span>Source unit: '+encode(c.units)+' · Approved trace: none</span></article>'
  ).join('');
 }
 function paperCards(studies){
  return studies.map(s=>
   '<article class="field-paper" data-paper-id="'+encode(s.id)+'">'+
   '<small>'+encode(s.year+' · '+s.scope)+'</small>'+
   '<h4>'+encode(s.title)+'</h4><p>'+encode(s.finding)+'</p>'+
   '<p class="field-limitation"><b>Limit:</b> '+encode(s.limitation)+'</p>'+
   '<a href="'+encode(validURL(s.url))+'" target="_blank" rel="noopener noreferrer">Read published abstract ↗</a></article>'
  ).join('');
 }
 async function boot(doc,fetcher){
  const panel=doc.getElementById('field-evidence-lab');
  if(!panel)return;
  const get=id=>doc.getElementById(id);
  const state=get('field-evidence-state'),list=get('field-channel-list');
  const controls=get('field-channel-filters'),papers=get('field-evidence-papers');
  const discovery=get('field-source-discovery'),counts=get('field-evidence-counts');
  panel.dataset.status='LOADING';
  try {
   const responses=await Promise.all([
    fetcher('../research/field_strain_evidence_20261023.json',{cache:'no-cache'}),
    fetcher('../research/metrology_prereg_v1.json',{cache:'no-cache'})
   ]);
   guard(responses.every(x=>x.ok),'Required same-site registry unavailable');
   const [e,p]=await Promise.all(responses.map(x=>x.json()));
   const result=verify(e,p);
   let selected='all';
   controls.innerHTML=filters.map(([key,label])=>
    '<button type="button" data-channel-filter="'+key+'" aria-pressed="'+String(key==='all')+'">'+
    encode(label)+' ('+subset(p.channels,key).length+')</button>'
   ).join('');
   function repaint(){
    list.innerHTML=channelCards(p.channels,selected);
    list.dataset.visibleCount=String(subset(p.channels,selected).length);
    controls.querySelectorAll('[data-channel-filter]').forEach(button=>{
     button.setAttribute('aria-pressed',String(button.dataset.channelFilter===selected));
    });
   }
   controls.addEventListener('click',event=>{
    const b=event.target.closest('[data-channel-filter]');
    if(!b||!controls.contains(b))return;
    const key=b.dataset.channelFilter;
    if(!filters.some(f=>f[0]===key))return;
    selected=key;repaint();
   });
   repaint();
   papers.innerHTML=paperCards(e.studies);
   discovery.innerHTML='<strong>'+encode(e.field_dataset.title)+'</strong>'+
    '<p>DOE catalogue lists '+e.field_dataset.resource_count+
    ' resource entries; 0 original instrument archives acquired or qualified here.</p>'+
    '<p>'+encode(e.field_dataset.physical_scope)+'</p>'+
    '<p><strong>Paper-reported late-November ebb subset:</strong> '+encode(
       'upstream/downstream ADV, blade strain and thrust synchronized by the authors; upstream ADCP data lost after leak damage in that experiment.')+'</p>'+
    '<p>'+encode('Exact source UTC and Voltsys coincidence remain UNKNOWN. This is a paper preview, not independently qualified raw sensor data.')+'</p>'+
    '<a href="'+encode(validURL(e.field_dataset.url))+'" target="_blank" rel="noopener noreferrer">Explore DOE data catalogue ↗</a> · '+
    '<a href="'+encode(validURL(e.publication_reported_case.publisher_preview_url))+'" target="_blank" rel="noopener noreferrer">See paper results preview ↗</a>';
   counts.textContent=result.channels+' required channels · '+result.numericUnqualified+
    ' numeric channels without calibration records · '+result.gatesUnresolved+
    ' unresolved independent metrology gates';
   state.textContent='Catalogue / publication evidence only. 0 qualified original source intervals, 0 project blade-stress and net-electricity trials. No contact or field work authorized.';
   panel.dataset.status='BLOCKED';
  } catch(error){
   panel.dataset.status='UNAVAILABLE';
   state.textContent='Research source unavailable or inconsistent; no instruments or studies are presented as verified.';
   [list,controls,papers,discovery,counts].forEach(e=>e.replaceChildren());
   if(root.console&&root.console.warn)root.console.warn('Field research fail-closed:',error.message);
  }
 }
 const api={verify,subset,channelCards,paperCards,boot};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
 root.TidalFieldResearch=api;
 if(root.document&&typeof root.fetch==='function')
  root.document.addEventListener('DOMContentLoaded',()=>boot(root.document,root.fetch.bind(root)));
})(typeof window!=='undefined'?window:globalThis);
