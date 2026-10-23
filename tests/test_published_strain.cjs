'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const ui=require('../site/published_strain.js');
const data=JSON.parse(fs.readFileSync(path.join(root,'research/UNH_2023_PUBLISHED_STRAIN_001.json')));
const original=JSON.parse(fs.readFileSync(path.join(root,'research/UNH_2022_SOURCE_ACCESS_001.json')));
assert.deepEqual(ui.verify(data,original),{gaugeCount:8,sourceDate:'2022-11-22',
 rotorBladeCount:4,frequencyRangeHz:[1.2,2.066667],powerAverageSeconds:1,authorized:false});
assert.deepEqual(['mean','max','std'].map(k=>ui.selectedRows(data,k)[2].value),[86.8,120.8,11.4]);
assert.equal(ui.selectedRows(data,'mean')[6].value,69.7);
assert.equal((ui.barsHTML(data,'mean').match(/class="strain-gauge-row/g)||[]).length,8);
assert.equal((ui.barsHTML(data,'mean').match(/strain-strut-focus/g)||[]).length,2);
assert.ok(!ui.barsHTML(data,'mean').includes('microstrain'));
assert.throws(()=>ui.selectedRows(data,'unqualified'),/Unknown/);
function reject(fn){const d=structuredClone(data),s=structuredClone(original);fn(d,s);assert.throws(()=>ui.verify(d,s));}
reject(d=>d.table.units='microstrain');
reject(d=>d.table.values[2].mean=88);
reject(d=>d.table.values.pop());
reject(d=>d.table.raw_trace_available=true);
reject(d=>d.source.visual_pdf_screenshot_confirmed=true);
reject(d=>d.source.original_sensor_archives_acquired=true);
reject(d=>d.experiment_system.instrumented_blade_operation='GRID_CONNECTED');
reject(d=>d.experiment_system.auxiliary_energy_meter_boundary_verified=true);
reject(d=>d.experiment_system.ADV_probes_near_rotor_induced_velocity=false);
reject(d=>d.project_scientific_boundary.project_physical_trials=1);
reject((d,s)=>s.scientifically_qualified_common_windows=1);
console.log('PASS: 8 published gauge bars, off-grid mode, unqualified units, 0 acquired sensor samples');
