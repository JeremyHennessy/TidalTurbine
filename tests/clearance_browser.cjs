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
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({result:'PASS',browser:'Chromium',viewports:[[1440,1000],[390,844]],checks:['default obstruction','sensor margin','parked configuration','hatch conflict','custom label','empty input erases stale diagram','both axial alternatives indeterminate','field enablement','14 existing artwork selectors','mobile controls and horizontal fit','zero uncaught page errors','detail contrast >=4.5:1','explicit dark SVG label color','all six controls pointer-reachable with normal navigation at both viewports'],capture:'Panel screenshots hide fixed navigation solely during capture. Separate normal full-page and viewport screenshots retain normal navigation. All six controls receive real pointer clicks with normal DOM at both viewports. Reduced-motion browser context.',scope:'Actual browser UI consistency only; not physics, lift, ecological or production deployment validation'},null,2)+'\n');
  console.log('PASS: actual Chromium desktop/mobile clearance interactions, fail-closed states, inherited artwork count and mobile fit. Screenshots saved for visual review.');
 } catch(e) {
  if(page)await page.screenshot({path:path.join(out,'failure.png'),fullPage:true}).catch(()=>{});
  throw e;
 } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1;});
