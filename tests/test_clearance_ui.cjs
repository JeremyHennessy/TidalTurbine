'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'site/index.html'),'utf8');
const code=fs.readFileSync(path.join(root,'site/clearance.js'),'utf8');
function boot(){
 const elements=new Map(),values={layout:'CF-LIFT-2',preset:'inline',ptoX:'0',sensorX:'.95',margin:'.1',hatch:'1.6'};
 function get(id){if(!elements.has(id))elements.set(id,{value:values[id.replace('clearance-','')]||'',innerHTML:'',textContent:'',disabled:false,dataset:{},listeners:{},addEventListener(k,f){this.listeners[k]=f;},replaceChildren(){this.innerHTML='';}});return elements.get(id);}
 const doc={readyState:'complete',getElementById:get};
 const ctx=vm.createContext({document:doc,TidalClearance:require('../site/clearance_model.js')});new vm.Script(code).runInContext(ctx);
 const change=(id,value,type='input')=>{const el=get('clearance-'+id);el.value=value;if(type==='input')get('clearance-lab').listeners.input({target:el});else el.listeners[type]({target:el});};
 return {get,change,status:()=>get('clearance-status').textContent};
}
test('new controls are labelled and scripts follow isolated model',()=>{for(const id of ['layout','preset','ptoX','sensorX','margin','hatch','status','details','diagram'])assert.ok(html.includes('id="clearance-'+id+'"'));assert.ok(html.indexOf('src="clearance_model.js"')<html.indexOf('src="clearance.js"'));assert.match(html,/aria-live="polite"/);});
test('UI default displays PTO obstruction and two projections',()=>{const u=boot();assert.match(u.status(),/Potential interference: PTO/);assert.equal((u.get('clearance-diagram').innerHTML.match(/<svg /g)||[]).length,2);});
test('preset switches sensor and unobstructed listed boxes',()=>{const u=boot();u.change('preset','sensor','change');assert.match(u.status(),/interference: sensor/);u.change('preset','outer','change');assert.match(u.status(),/No box interference among the listed objects only/);});
test('manual change marks inputs custom and recomputes deck interference',()=>{const u=boot();u.change('hatch','1.5');assert.equal(u.get('clearance-preset').value,'custom');assert.match(u.status(),/deck left/);});
test('empty input fails closed and erases diagram/details',()=>{const u=boot();u.change('hatch','');assert.match(u.status(),/No result/);assert.equal(u.get('clearance-diagram').innerHTML,'');assert.equal(u.get('clearance-details').textContent,'');});
test('out-of-range input fails closed',()=>{const u=boot();u.change('margin','-1');assert.match(u.status(),/No result/);});
test('both axial layouts erase stale diagrams and disable numerical controls',()=>{const u=boot();for(const layout of ['AX-POD-2','AX-DRY-2']){u.change('layout',layout,'change');assert.match(u.status(),/Indeterminate.*unknown/);assert.equal(u.get('clearance-diagram').innerHTML,'');assert.equal(u.get('clearance-ptoX').disabled,true);}});
test('return to CF reenables and computes, presets reset invalid values',()=>{const u=boot();u.change('layout','AX-DRY-2','change');u.change('layout','CF-LIFT-2','change');assert.equal(u.get('clearance-hatch').disabled,false);u.change('hatch','');u.change('preset','outer','change');assert.match(u.status(),/No box interference/);});
test('missing panel safely does nothing',()=>{new vm.Script(code).runInContext(vm.createContext({document:{readyState:'complete',getElementById:()=>null},TidalClearance:require('../site/clearance_model.js')}));});
test('generated drawings contain only finite coordinates',()=>{const u=boot();for(const p of ['inline','sensor','outer']){u.change('preset',p,'change');assert.doesNotMatch(u.get('clearance-diagram').innerHTML,/NaN|undefined|Infinity/);}});
if(process.env.EXPORT_CLEARANCE_SVGS){const u=boot();u.change('preset','outer','change');const svgs=u.get('clearance-diagram').innerHTML.match(/<svg[\s\S]*?<\/svg>/g);svgs.forEach((s,i)=>fs.writeFileSync(path.join(process.env.EXPORT_CLEARANCE_SVGS,'projection-'+i+'.svg'),s.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ')));}
