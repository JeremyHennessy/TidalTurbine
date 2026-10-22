'use strict';
// Real Chromium regression against the built static candidate served over HTTP.
// This is UI/geometry consistency, not physical or environmental validation.
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../dist'),out=path.resolve(__dirname,'../browser-artifacts');
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const server=http.createServer((req,res)=>{
  const url=new URL(req.url,'http://127.0.0.1');
  const p=path.resolve(root,'.'+decodeURIComponent(url.pathname));
  if(!p.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
  fs.readFile(p,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});res.end(e?'Not found':b);});
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 let browser,page;
 try {
  browser=await chromium.launch({headless:true});
  page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await page.goto(`http://127.0.0.1:${server.address().port}/site/index.html#designs`,{waitUntil:'networkidle'});
  await page.locator('#clearance-lab').waitFor({state:'visible'});
  const status=()=>page.locator('#clearance-status').innerText();
  const contrast=await page.evaluate(()=>{
   const rgb=s=>s.match(/[\d.]+/g).slice(0,3).map(Number);
   const lum=a=>a.map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;}).reduce((a,n,i)=>a+n*[.2126,.7152,.0722][i],0);
   const fg=lum(rgb(getComputedStyle(document.getElementById('clearance-details')).color));
   const bg=lum(rgb(getComputedStyle(document.getElementById('clearance-lab')).backgroundColor));
   return (Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);
  });assert.ok(contrast>=4.5,'detail text contrast must be at least 4.5:1');
  assert.equal(await page.locator('#clearance-diagram svg').first().evaluate(el=>getComputedStyle(el).color),'rgb(23, 52, 66)');
  const captureStyle='#sidebar,.topbar{visibility:hidden!important}'; // Isolate panel; do not alter interaction tests.
  async function normalPageEvidence(label) {
   for(const id of ['layout','preset','ptoX','sensorX','margin','hatch']) {
    const control=page.locator('#clearance-'+id);await control.scrollIntoViewIfNeeded();await control.click();await page.keyboard.press('Escape');
   }
   await page.locator('#clearance-title').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,label+'-normal-full.png'),fullPage:true,animations:'disabled'});
   await page.screenshot({path:path.join(out,label+'-normal-viewport.png'),animations:'disabled'});
  }

  assert.match(await status(),/Potential interference: PTO/);
  assert.equal(await page.locator('#clearance-diagram svg').count(),2);
  await page.selectOption('#clearance-preset','sensor');assert.match(await status(),/Potential interference: sensor/);
  await page.selectOption('#clearance-preset','outer');assert.match(await status(),/No box interference among the listed objects only/);
  await page.fill('#clearance-hatch','1.50');assert.match(await status(),/deck left, deck right, deck front, deck back/);
  assert.equal(await page.inputValue('#clearance-preset'),'custom');
  await page.fill('#clearance-hatch','');assert.match(await status(),/No result/);assert.equal(await page.locator('#clearance-diagram svg').count(),0);
  await page.fill('#clearance-hatch','1.60');
  for(const layout of ['AX-POD-2','AX-DRY-2']) {
   await page.selectOption('#clearance-layout',layout);assert.match(await status(),/Indeterminate.*unknown/);
   assert.equal(await page.locator('#clearance-ptoX').isDisabled(),true);assert.equal(await page.locator('#clearance-diagram svg').count(),0);
  }
  await page.selectOption('#clearance-layout','CF-LIFT-2');assert.equal(await page.locator('#clearance-ptoX').isDisabled(),false);assert.match(await status(),/No box interference/);
  assert.equal(await page.locator('#design-selector button').count(),14);
  await normalPageEvidence('desktop');
  await page.locator('#clearance-lab').screenshot({path:path.join(out,'desktop-1440.png'),animations:'disabled',style:captureStyle});
  await page.setViewportSize({width:390,height:844});
  await page.selectOption('#clearance-preset','inline');assert.match(await status(),/Potential interference: PTO/);
  await page.selectOption('#clearance-preset','outer');assert.match(await status(),/No box interference/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'mobile page must not overflow horizontally');
  const box=await page.locator('#clearance-lab').boundingBox();assert.ok(box.x>=0 && box.x+box.width<=390,'mobile panel fits viewport');
  await normalPageEvidence('mobile');
  await page.locator('#clearance-lab').screenshot({path:path.join(out,'mobile-390.png'),animations:'disabled',style:captureStyle});
  // Concept004 assertions are separate from the already reviewed clearance results.
  for (const [width,height,label] of [[1440,1000,'desktop'],[390,844,'mobile']]) {
   await page.setViewportSize({width,height});
   const serviceStatus=()=>page.locator('#service-energy-status').innerText();
   const reset=()=>page.locator('#service-energy-reset').click();
   await reset();assert.match(await serviceStatus(),/-0.18 kWh/);
   assert.equal(await page.locator('#service-energy-lab input').count(),12);
   for(const control of await page.locator('#service-energy-lab input').all()) {
    await control.scrollIntoViewIfNeeded();await control.click();
   }
   await page.fill('#service-energy-candidate-monitorW','0');assert.match(await serviceStatus(),/1.5 kWh/);
   await reset();await page.fill('#service-energy-powerW','0');assert.match(await serviceStatus(),/-1.68 kWh/);
   assert.match(await page.locator('#service-energy-candidate-budget').innerText(),/-1.78 kWh/);
   await reset();await page.fill('#service-energy-candidate-taskH','20');
   assert.match(await page.locator('#service-energy-threshold').innerText(),/No nonnegative.*reaches equal/);
   for(const [id,value] of [['candidate-taskH',''],['periodH','1']]) {
    await reset();await page.fill('#service-energy-'+id,value);assert.match(await serviceStatus(),/No result/);
    for(const output of ['baseline-budget','candidate-budget','threshold','balance']) assert.equal(await page.locator('#service-energy-'+output).innerText(),'');
   }
   await reset();
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'service page must fit viewport');
   const serviceBox=await page.locator('#service-energy-lab').boundingBox();
   assert.ok(serviceBox.x>=0 && serviceBox.x+serviceBox.width<=width,'service panel fits viewport');
   const serviceContrast=await page.evaluate(()=>{
    const lum=s=>s.match(/[\d.]+/g).slice(0,3).map(Number).map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;}).reduce((a,n,i)=>a+n*[.2126,.7152,.0722][i],0);
    const fg=lum(getComputedStyle(document.getElementById('service-energy-balance')).color),bg=lum(getComputedStyle(document.getElementById('service-energy-lab')).backgroundColor);
    return (Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);
   });assert.ok(serviceContrast>=4.5,'service explanatory text contrast >=4.5:1');
   await page.locator('#service-energy-title').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,'service-'+label+'-normal-inputs.png'),animations:'disabled'});
   await page.locator('#service-energy-status').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,'service-'+label+'-normal-result.png'),animations:'disabled'});
   await page.locator('#service-energy-lab').screenshot({path:path.join(out,'service-'+label+'-panel.png'),animations:'disabled',style:captureStyle});
  }

  // Dated Research progress and the source-backed component candidate.
  for (const [width,height,label] of [[1440,1000,'desktop'],[390,844,'mobile']]) {
   await page.setViewportSize({width,height});
   await page.goto(`http://127.0.0.1:${server.address().port}/site/index.html#research`,{waitUntil:'networkidle'});
   await page.locator('#research-progress').waitFor({state:'visible'});
   assert.match(await page.locator('#research-gates').innerText(),/DESK STUDY IN PROGRESS.*FIELD EVIDENCE PENDING/);
   assert.match(await page.locator('#research-status-boundary').innerText(),/No physical gate promoted/);
   assert.match(await page.locator('#research-next-evidence').innerText(),/Zero qualified cells/);
   for(const id of ['research-progress']) {
    const box=await page.locator('#'+id).boundingBox();assert.ok(box.x>=0&&box.x+box.width<=width,'research panel fits');
    await page.locator('#research-progress-title').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(out,'research-'+label+'-normal.png'),animations:'disabled'});
    await page.locator('#'+id).screenshot({path:path.join(out,'research-'+label+'-panel.png'),animations:'disabled',style:captureStyle});
   }
   await page.locator('#research-open-designs').scrollIntoViewIfNeeded();await page.locator('#research-open-designs').click();
   await page.locator('#component-interface-lab').waitFor({state:'visible'});
   assert.match(await page.locator('#component-displacement').innerText(),/15 mm hub displacement/);
   assert.match(await page.locator('#component-boundary').innerText(),/Not a complete service envelope/);
   const link=page.locator('#component-ktr-source');await link.scrollIntoViewIfNeeded();
   assert.ok(await link.evaluate(el=>{const r=el.getBoundingClientRect();return el.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));}),'source link is pointer reachable with normal navigation');
   for(const id of ['component-interface-lab','research-progress']) {
    const c=await page.locator('#'+id).evaluate(el=>{
     const lum=s=>s.match(/[\d.]+/g).slice(0,3).map(Number).map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;}).reduce((a,n,i)=>a+n*[.2126,.7152,.0722][i],0);
     const bg=lum(getComputedStyle(el).backgroundColor);return [...el.querySelectorAll('p,li,a,h2,h3')].map(x=>{const fg=lum(getComputedStyle(x).color);return (Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);});
    });assert.ok(c.every(n=>n>=4.5),'new explanatory text contrast >=4.5:1');
   }
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'component page fits');
   await page.locator('#component-interface-title').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,'component-'+label+'-normal.png'),animations:'disabled'});
   await page.locator('#component-interface-lab').screenshot({path:path.join(out,'component-'+label+'-panel.png'),animations:'disabled',style:captureStyle});
   const support=page.locator('#shaft-support-details');
   assert.equal(await support.getAttribute('open'),null);
   await support.locator('summary').click();assert.notEqual(await support.getAttribute('open'),null);
   assert.match(await page.locator('#shaft-surface-finish').innerText(),/0.4 micrometres Ra/);
   assert.match(await page.locator('#shaft-selection-boundary').innerText(),/No bearing or shaft selected/);
   const requirements=page.locator('#shaft-requirements-source');await requirements.scrollIntoViewIfNeeded();
   assert.equal(await requirements.evaluate(e=>{const b=e.getBoundingClientRect();const target=document.elementFromPoint(b.x+b.width/2,b.y+b.height/2);return e===target||e.contains(target);}),true,'requirements link reachable');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'support requirements fit');
   await page.locator('#shaft-support-update').screenshot({path:path.join(out,'shaft-'+label+'-panel.png'),animations:'disabled',style:captureStyle});
   await support.locator('summary').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,'shaft-'+label+'-normal.png'),animations:'disabled'});
   await support.locator('summary').click();assert.equal(await support.getAttribute('open'),null);
   await support.locator('summary').click();assert.notEqual(await support.getAttribute('open'),null);
   await support.locator('summary').click();assert.equal(await support.getAttribute('open'),null);

  }
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({result:'PASS',browser:'Chromium',viewports:[[1440,1000],[390,844]],shaftChecks:['native disclosure repeat open/close','source-link hit testing','source finish and selection boundary','horizontal fit at both viewports'],researchChecks:['direct Research deep-link','dated completed source/software milestones','service stage remains pending','zero qualified FORCE cells visible','real pointer navigation to Designs','manufacturer dimension and bounded envelope','source link pointer reachability','desktop/mobile horizontal fit and text contrast'],serviceChecks:['12 pointer-reachable number controls and reset at both viewports','default negative delta','monitoring-free gain','negative net import','infeasible equality','empty input clears all budgets','outage beyond period clears all budgets','panel and page horizontal fit','text contrast >=4.5:1'],checks:['default obstruction','sensor margin','parked configuration','hatch conflict','custom label','empty input erases stale diagram','both axial alternatives indeterminate','field enablement','14 existing artwork selectors','mobile controls and horizontal fit','zero uncaught page errors','detail contrast >=4.5:1','explicit dark SVG label color','all six controls pointer-reachable with normal navigation at both viewports'],capture:'Panel screenshots hide fixed navigation solely during capture. Separate normal full-page and viewport screenshots retain normal navigation. All six controls receive real pointer clicks with normal DOM at both viewports. Reduced-motion browser context.',scope:'Actual browser UI consistency only; not physics, lift, ecological or production deployment validation'},null,2)+'\n');
  console.log('PASS: actual Chromium desktop/mobile clearance interactions, fail-closed states, inherited artwork count and mobile fit. Screenshots saved for visual review.');
 } catch(e) {
  if(page)await page.screenshot({path:path.join(out,'failure.png'),fullPage:true}).catch(()=>{});
  throw e;
 } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1;});
