'use strict';
// Isolated real-Chromium verification of the new Research evidence panel.
// This is not scientific testing or permission to contact/acquire original files.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const root=path.resolve(__dirname,'../dist');
const shots=path.resolve(__dirname,'../browser-artifacts');
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
(async()=>{
 fs.mkdirSync(shots,{recursive:true});
 const server=http.createServer((req,res)=>{
  const u=new URL(req.url,'http://127.0.0.1');
  const file=path.resolve(root,'.'+decodeURIComponent(u.pathname));
  if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
  fs.readFile(file,(e,buf)=>{
   res.writeHead(e?404:200,{'Content-Type':types[path.extname(file)]||'text/plain'});
   res.end(e?'Missing':buf);
  });
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 let browser;
 try{
  browser=await chromium.launch({headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  for(const [width,height,label] of [[1440,1000,'desktop'],[390,844,'mobile']]){
   await page.setViewportSize({width,height});
   await page.goto('http://127.0.0.1:'+server.address().port+'/site/index.html#research',{waitUntil:'networkidle'});
   await page.waitForFunction(()=>document.getElementById('field-evidence-lab')?.dataset.status==='BLOCKED',null,{timeout:20000});
   assert.equal(await page.locator('#field-channel-list .field-channel').count(),12);
   assert.equal(await page.locator('#field-evidence-papers .field-paper').count(),3);
   assert.match(await page.locator('#field-evidence-counts').innerText(),/11 numeric channels without calibration records/);
   assert.match(await page.locator('#field-evidence-state').innerText(),/0 qualified original source intervals/);
   assert.match(await page.locator('#field-source-discovery').innerText(),/0 original instrument archives acquired/);
   assert.match(await page.locator('#field-source-discovery').innerText(),/Paper-reported late-November ebb subset/);
   assert.match(await page.locator('#field-source-discovery').innerText(),/upstream ADCP data lost/);
   assert.match(await page.locator('#field-source-discovery').innerText(),/Voltsys coincidence remain UNKNOWN/);
   assert.match(await page.locator('#field-source-discovery a').nth(1).getAttribute('href'),/^https:\/\/www\.sciencedirect\.com\//);
   await page.locator('[data-channel-filter="electric"]').click();
   assert.equal(await page.locator('#field-channel-list .field-channel').count(),3);
   assert.equal(await page.locator('[data-channel-filter="electric"]').getAttribute('aria-pressed'),'true');
   await page.locator('[data-channel-filter="structure"]').click();
   assert.equal(await page.locator('#field-channel-list .field-channel').count(),2);
   await page.locator('[data-channel-filter="all"]').click();
   assert.equal(await page.locator('#field-channel-list .field-channel').count(),12);
   const box=await page.locator('#field-evidence-lab').boundingBox();
   assert.ok(box.x>=0&&box.x+box.width<=width+1,'evidence panel fits viewport');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no horizontal overflow');
   const external=page.locator('#field-source-discovery a').first();
   assert.match(await external.getAttribute('href'),/^https:\/\/catalog\.data\.gov\//);
   assert.equal(await external.getAttribute('rel'),'noopener noreferrer');
   await page.locator('#field-evidence-title').scrollIntoViewIfNeeded();
   await page.locator('#field-evidence-lab').screenshot({path:path.join(shots,'field-evidence-'+label+'.png'),animations:'disabled'});
  }
  await page.route('**/research/field_strain_evidence_20261023.json',route=>route.abort());
  await page.reload({waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.getElementById('field-evidence-lab')?.dataset.status==='UNAVAILABLE');
  assert.match(await page.locator('#field-evidence-state').innerText(),/unavailable or inconsistent/);
  assert.equal(await page.locator('#field-channel-list .field-channel').count(),0);
  assert.equal(await page.locator('#field-evidence-papers .field-paper').count(),0);
  assert.deepEqual(errors,[],'no uncaught browser exceptions even when data is unavailable');
  console.log('PASS: TidalLab Research panel desktop/mobile, publication limits, channel filters, failure state');
 }finally{
  if(browser)await browser.close();
  await new Promise(resolve=>server.close(resolve));
 }
})().catch(error=>{console.error(error);process.exitCode=1;});
