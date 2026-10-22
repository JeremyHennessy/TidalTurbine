'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'site/index.html'),'utf8'),code=fs.readFileSync(path.join(root,'site/service_energy.js'),'utf8');
const model=require('../site/service_energy_model.js');
function boot(){
 const values=model.example(),elements=new Map();
 function get(id){if(!elements.has(id)){const key=id.replace('service-energy-',''),parts=key.split('-');const value=parts.length===2?values[parts[0]]?.[parts[1]]:values[key];elements.set(id,{value:value===undefined?'':String(value),textContent:'',dataset:{},listeners:{},addEventListener(k,f){this.listeners[k]=f;}});}return elements.get(id);}
 new vm.Script(code).runInContext(vm.createContext({document:{readyState:'complete',getElementById:get},TidalServiceEnergy:model}));
 return {get,change(id,value){get('service-energy-'+id).value=value;get('service-energy-lab').listeners.input();},reset(){get('service-energy-reset').listeners.click();},status(){return get('service-energy-status').textContent;}};
}
test('12 number assumptions and explicit model-first script order',()=>{assert.equal((html.match(/id="service-energy-[^"]+" type="number"/g)||[]).length,12);assert.ok(html.indexOf('src="service_energy_model.js"')<html.indexOf('src="service_energy.js"'));assert.match(html,/No architecture|No maintenance/);assert.match(html,/id="service-energy-boundary"[^>]*>Assume one service event[\s\S]*?matched initial\/final stored energy/);});
test('default labels negative delta and readable budgets',()=>{const u=boot();assert.match(u.status(),/-0.18 kWh.*No architecture ranking/);assert.match(u.get('service-energy-baseline-budget').textContent,/36.65 kWh/);assert.match(u.get('service-energy-threshold').textContent,/8.92857 W/);});
test('empty assumption invalidates and clears every stale output',()=>{const u=boot();u.change('candidate-taskH','');assert.match(u.status(),/No result/);for(const id of ['baseline-budget','candidate-budget','threshold','balance'])assert.equal(u.get('service-energy-'+id).textContent,'');});
test('outage exceeding period fails closed and reset restores defaults',()=>{const u=boot();u.change('periodH','1');assert.match(u.status(),/No result.*exceeds/);u.reset();assert.match(u.status(),/-0.18 kWh/);assert.equal(u.get('service-energy-periodH').value,'168');});
test('negative threshold is described as infeasible, not free energy',()=>{const u=boot();u.change('candidate-taskH','20');assert.match(u.get('service-energy-threshold').textContent,/No nonnegative.*reaches equal/);});
test('zero power preserves net import and changes live status',()=>{const u=boot();u.change('powerW','0');assert.match(u.status(),/-1.68 kWh/);assert.match(u.get('service-energy-candidate-budget').textContent,/-1.78 kWh/);});
test('NaN and negative text fail closed',()=>{const u=boot();for(const v of ['nope','-1','Infinity']){u.change('powerW',v);assert.match(u.status(),/No result/);}});
test('missing panel does nothing',()=>{new vm.Script(code).runInContext(vm.createContext({document:{readyState:'complete',getElementById:()=>null},TidalServiceEnergy:model}));});
