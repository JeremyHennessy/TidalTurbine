'use strict';
const test=require('node:test'), assert=require('node:assert/strict');
const model=require('../site/service_energy_model.js');
function near(a,b){assert.ok(Math.abs(a-b)<1e-10, `${a} != ${b}`);}
test('Concept002 worked example retains negative net delta',()=>{
 const r=model.compare(model.example());near(r.recoveredKWh,1.5);near(r.extraMonitorKWh,1.68);near(r.deltaKWh,-.18);near(r.equalNetCandidateMonitorW,8.928571428571429);near(r.baseline.netKWh,36.65);near(r.candidate.netKWh,36.47);
});
test('net difference equals independent budget subtraction',()=>{
 for(const p of [0,100,250,1000])for(const m of [0,10,25]){const x=model.example();x.powerW=p;x.candidate.monitorW=m;const r=model.compare(x);near(r.deltaKWh,r.candidate.netKWh-r.baseline.netKWh);}
});
test('equal options return zero difference',()=>{const x=model.example();x.candidate={...x.baseline};const r=model.compare(x);near(r.deltaKWh,0);near(r.equalNetCandidateMonitorW,0);});
test('negative net import is not clamped away',()=>{const x=model.example();x.powerW=0;const r=model.compare(x);near(r.candidate.netKWh,-1.78);near(r.deltaKWh,-1.68);});
test('longer candidate service keeps a negative equality value and infeasible flag',()=>{const x=model.example();x.candidate.taskH=10;const r=model.compare(x);assert.ok(r.equalNetCandidateMonitorW<0);assert.equal(r.equalityAttainableWithNonnegativeMonitor,false);});
test('restart-import difference reduces monitor allowance',()=>{const x=model.example();x.candidate.restartWh=1600;const r=model.compare(x);near(r.equalNetCandidateMonitorW,0);near(r.extraRestartKWh,1.5);});
test('threshold is total candidate monitor power, not incremental',()=>{const x=model.example();x.baseline.monitorW=5;const r=model.compare(x);near(r.equalNetCandidateMonitorW,13.928571428571429);x.candidate.monitorW=r.equalNetCandidateMonitorW;near(model.compare(x).deltaKWh,0);});
test('access wait and recommissioning count equally as outage hours',()=>{const x=model.example();x.candidate.waitH+=3;x.candidate.recommissionH+=3;near(model.compare(x).recoveredKWh,0);});
test('whole-period outage valid, beyond period rejected',()=>{const x=model.example();x.candidate={waitH:0,taskH:168,recommissionH:0,monitorW:0,restartWh:0};near(model.compare(x).candidate.netKWh,0);x.candidate.taskH=168.00001;assert.throws(()=>model.compare(x),/exceeds/);});
test('period must be positive',()=>{for(const v of [0,-1,Infinity,NaN,'168',true,null]){const x=model.example();x.periodH=v;assert.throws(()=>model.compare(x));}});
test('every option field fails closed on missing, text, negative and nonfinite values',()=>{for(const side of ['baseline','candidate'])for(const k of Object.keys(model.example()[side]))for(const v of [undefined,'',-1,NaN,Infinity,true]){const x=model.example();x[side][k]=v;assert.throws(()=>model.compare(x));}});
test('power and numeric caps reject unreasonable overflow inputs',()=>{for(const v of [1e300,-1,'250',true]){const x=model.example();x.powerW=v;assert.throws(()=>model.compare(x));}const x=model.example();x.candidate.restartWh=1e300;assert.throws(()=>model.compare(x));});
test('example is fresh and compare does not mutate it',()=>{const x=model.example(), copy=JSON.stringify(x);model.compare(x);assert.equal(JSON.stringify(x),copy);x.baseline.taskH=1;assert.equal(model.example().baseline.taskH,8);});
test('missing inputs and option objects rejected',()=>{assert.throws(()=>model.compare());for(const side of ['baseline','candidate']){const x=model.example();x[side]=null;assert.throws(()=>model.compare(x));}});
