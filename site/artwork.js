(function tidalArtwork(root) {
  "use strict";
  const KEYS = ["seabed","floating","counter","rim","crossflow","helical","savonius","foil","screw","kite","duct","pressure","eel","viv"];
  const META = {
    seabed:["Three-blade axial rotor","Seabed support","Axial flow"],
    floating:["Recoverable axial pods","Surface platform","Mooring system"],
    counter:["Opposed axial rotors","Independent hubs","Common support"],
    rim:["Annular rotor","Open centre","Generator rim"],
    crossflow:["Straight lift blades","Cross-flow shaft","Blade struts"],
    helical:["Twisted lift blades","Vertical rotor","Shaft / PTO"],
    savonius:["Curved drag scoops","Cross-flow rotation","Drive shaft"],
    foil:["Heave + pitch foil","Vertical guide","Actuator / PTO"],
    screw:["Continuous helix","Axial shaft","Support bearings"],
    kite:["Flying wing","Onboard rotors","Anchored tether"],
    duct:["Duct / diffuser","Internal rotor","Generator"],
    pressure:["Immersed intake","Secondary circuit","Air / water PTO"],
    eel:["Flexible foil / flag","Piezo strips","Rectifier link"],
    viv:["Vortex wake","Oscillating cylinder","Linear PTO"]
  };
  function escapeText(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
  function id(key,variant){return "tla-"+key+"-"+variant;}
  function defs(prefix){
    const i=s=>prefix+"-"+s;
    return `<defs>
      <linearGradient id="${i("sea")}" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#14526a"/><stop offset=".48" stop-color="#0a3045"/><stop offset="1" stop-color="#061926"/></linearGradient>
      <radialGradient id="${i("halo")}"><stop stop-color="#1b7083" stop-opacity=".53"/><stop offset="1" stop-color="#0b3e59" stop-opacity="0"/></radialGradient>
      <linearGradient id="${i("metal")}" x1="0" x2="1" y1="0" y2=".75"><stop stop-color="#d7f0ea"/><stop offset=".22" stop-color="#83aeb9"/><stop offset=".53" stop-color="#284d60"/><stop offset=".78" stop-color="#588c9b"/><stop offset="1" stop-color="#1a3848"/></linearGradient>
      <linearGradient id="${i("dark")}" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#28566b"/><stop offset=".55" stop-color="#102f46"/><stop offset="1" stop-color="#091e31"/></linearGradient>
      <linearGradient id="${i("blade")}" x1="0" x2="1" y1="0" y2=".85"><stop stop-color="#e1fff7"/><stop offset=".15" stop-color="#9ce6df"/><stop offset=".48" stop-color="#46adbe"/><stop offset=".78" stop-color="#176582"/><stop offset="1" stop-color="#0b354e"/></linearGradient>
      <linearGradient id="${i("edge")}" x1="0" x2="1"><stop stop-color="#a1fff0"/><stop offset=".55" stop-color="#62cde5"/><stop offset="1" stop-color="#1b8299"/></linearGradient>
      <linearGradient id="${i("gold")}" x1="0" x2="1"><stop stop-color="#ffe8af"/><stop offset=".6" stop-color="#eabb76"/><stop offset="1" stop-color="#8c613e"/></linearGradient>
      <linearGradient id="${i("ground")}" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#235769"/><stop offset="1" stop-color="#081e2b"/></linearGradient>
      <pattern id="${i("grid")}" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" stroke="#5db9c3" stroke-width=".6" opacity=".23" fill="none"/></pattern>
      <filter id="${i("shadow")}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
    </defs>`;
  }
  const B=p=>`url(#${p}-blade)`,M=p=>`url(#${p}-metal)`,K=p=>`url(#${p}-dark)`,E=p=>`url(#${p}-edge)`,G=p=>`url(#${p}-gold)`;
  function ground(p){
    return `<path d="M0 361 Q80 343 165 360 T330 352 T505 364 T700 357V410H0Z" fill="url(#${p}-ground)" stroke="#447b85" stroke-width="2"/>
      <path d="M0 379q115-17 190-5t181-8 219 7 130-11" fill="none" stroke="#497e7b" stroke-width="1.5" opacity=".46"/>
      <g fill="#2c6877" opacity=".60"><ellipse cx="128" cy="377" rx="28" ry="5"/><ellipse cx="538" cy="376" rx="32" ry="6"/><ellipse cx="606" cy="362" rx="16" ry="4"/></g>`;
  }
  function ambient(p,waterline=false){
    const beams=[0,1,2,3,4].map(i=>`<path d="M${50+i*146} 66l-95 307 148-2z" fill="#77b9c3" opacity="${.015+i*.004}"/>`).join("");
    const current=[0,1,2,3].map(i=>`<path class="art-flow-line" d="M${38+i*6} ${155+i*57} Q165 ${141+i*57} 275 ${155+i*57}T535 ${153+i*57}" fill="none" stroke="#6ac6d9" stroke-width="1.5" opacity=".14" stroke-dasharray="9 13"/>`).join("");
    return `<rect width="700" height="410" fill="url(#${p}-sea)"/><rect width="700" height="410" fill="url(#${p}-grid)" opacity=".65"/>
      <ellipse cx="356" cy="212" rx="304" ry="205" fill="url(#${p}-halo)"/>${beams}${current}
      <path d="M0 65 Q175 62 350 67 T700 64" stroke="#75e9ec" stroke-width="2.2" opacity=".47" fill="none"/>
      <path d="M0 74 Q175 71 350 76 T700 73" stroke="#7dd7d9" stroke-width=".7" opacity=".18" fill="none"/>
      ${waterline?`<path d="M0 115 Q80 110 160 115 T320 115 T480 115 T700 115" fill="none" stroke="#84e5e3" stroke-width="2" opacity=".78"/>`:""}
      <path d="M50 176h82m-10-7 10 7-10 7 M564 190h78m-10-7 10 7-10 7" stroke="#7ee2e7" stroke-width="2.3" fill="none" opacity=".68"/>
      <g fill="#a3e6e6" opacity=".26"><circle cx="98" cy="130" r="2"/><circle cx="602" cy="259" r="2.1"/><circle cx="169" cy="259" r="1.5"/><circle cx="575" cy="126" r="1.4"/><circle cx="452" cy="325" r="2"/></g>
      ${ground(p)}`;
  }
  function pile(p,x=354,top=240){
    return `<ellipse cx="${x}" cy="351" rx="66" ry="10" fill="#051a29" opacity=".55"/><path d="M${x-30} 341v-22h60v22l26 15h-112z" fill="${K(p)}" stroke="#62abb5" stroke-width="2"/>
      <path d="M${x-13} 329V${top}h26v${329-top}z" fill="${M(p)}" stroke="#85ccd4" stroke-width="1.7"/>
      <path d="M${x-6} ${top+10}v${319-top}" stroke="#d4fffc" stroke-width="2" opacity=".33"/>
      <path d="M${x-49} 356v9m${x+49} -9v9" stroke="#6faeb8" stroke-width="4"/>`;
  }
  function fan(p,x,y,r=95,rot=0){
    const one=`<path d="M-10 -8 C-14 -34 -29 ${-r*.78} -8 ${-r} C8 ${-r-9} 23 ${-r*.74} 14 ${-r*.42} L12 -8Z" fill="${B(p)}" stroke="#b7fff3" stroke-width="1.6"/>`;
    const blades=[0,120,240].map(deg=>`<g transform="rotate(${deg+rot})">${one}</g>`).join("");
    return `<g transform="translate(${x} ${y})"><circle r="${r*1.03}" stroke="#7adbe8" fill="none" stroke-width="1" stroke-dasharray="4 13" opacity=".27"/>
      <ellipse cx="0" cy="0" rx="${r*.38}" ry="${r*.38}" fill="#061d2c" opacity=".5" filter="url(#${p}-shadow)"/>
      ${blades}<circle r="20" fill="${M(p)}" stroke="#d4fff0" stroke-width="2"/><circle r="8" fill="${G(p)}" stroke="#f8efd5"/></g>`;
  }
  function nacelle(p,x,y,w=126){
    return `<g><rect x="${x}" y="${y-24}" width="${w}" height="48" rx="23" fill="${M(p)}" stroke="#a9e7e5" stroke-width="1.8"/><path d="M${x+20} ${y-19}h${w-36}" stroke="#e2fff8" opacity=".56" stroke-width="3"/><path d="M${x+64} ${y-23}v46m${x+82} -42v38" stroke="#234d61" opacity=".45" stroke-width="2"/><ellipse cx="${x+7}" cy="${y}" rx="12" ry="22" fill="${K(p)}" stroke="#91dde5"/></g>`;
  }
  function gen(p,x,y,w=70){
    return `<g><rect x="${x}" y="${y}" width="${w}" height="38" rx="8" fill="${K(p)}" stroke="#7bc5cf" stroke-width="1.8"/><path d="M${x+8} ${y+10}h${w-16}" stroke="#cbf9ea" opacity=".5"/><circle cx="${x+w-15}" cy="${y+23}" r="5" fill="${G(p)}"/><text x="${x+12}" y="${y+27}" fill="#d2f6e9" font-size="11" font-weight="700">PTO</text></g>`;
  }
  function sceneSeabed(p){
    return `${pile(p,368,229)}<path d="M386 330Q426 335 469 363L516 386" fill="none" stroke="#58d1d8" stroke-width="4" stroke-linecap="round"/>
      ${nacelle(p,309,227,144)}${fan(p,306,227,103,13)}<path d="M374 252v62" fill="none" stroke="#d3f7ed" stroke-width="2" opacity=".3"/>`;
  }
  function sceneFloating(p){
    return `<path d="M155 105q7 30 43 34h308q40-3 45-34L155 105Z" fill="${M(p)}" stroke="#baf0e9" stroke-width="2.1"/>
      <rect x="230" y="83" width="206" height="28" rx="9" fill="${K(p)}" stroke="#76c7d1"/><rect x="313" y="67" width="77" height="20" rx="5" fill="${M(p)}" stroke="#b2fff0"/>
      <path d="M215 136L162 326l-23 27M497 136l54 190 25 28" fill="none" stroke="#81d1d9" stroke-width="3.4"/>
      <path d="M125 357l18-20 26 18zM557 357l20-20 25 18z" fill="${M(p)}" stroke="#89d6d9"/>
      <path d="M270 140v92m181-92v92" stroke="#a7d7dc" stroke-width="10"/>
      ${nacelle(p,258,237,72)}${nacelle(p,437,237,72)}${fan(p,258,238,66,20)}${fan(p,436,238,66,-11)}
      <path d="M156 104h393" stroke="#a3efed" stroke-width="3" opacity=".6"/>`;
  }
  function sceneCounter(p){
    return `${pile(p,350,250)}<path d="M252 237h202" stroke="${M(p)}" stroke-width="16"/>
      ${nacelle(p,311,238,84)}${fan(p,243,228,91,13)}${fan(p,459,228,86,48)}
      <path d="M211 103Q245 68 279 103l-6-20m6 20-20-9M425 103Q459 68 494 103l-16-1m16 1-2-18" fill="none" stroke="#ffd39a" stroke-width="2.8"/>`;
  }
  function sceneRim(p){
    return `${pile(p,350,322)}<ellipse cx="348" cy="223" rx="123" ry="124" fill="${K(p)}" stroke="#5faebf" stroke-width="6"/>
      <ellipse cx="348" cy="223" rx="101" ry="101" fill="${B(p)}" stroke="#bcfff1" stroke-width="4"/>
      <ellipse cx="348" cy="223" rx="74" ry="76" fill="#0a2d43" stroke="#48a9b5" stroke-width="3"/>
      ${Array.from({length:9},(_,i)=>`<path d="M337 146Q389 150 391 192" transform="rotate(${i*40} 348 223)" fill="none" stroke="${E(p)}" stroke-width="8" stroke-linecap="round"/>`).join("")}
      <ellipse cx="348" cy="223" rx="49" ry="52" fill="#102b3d" stroke="#85cad2" stroke-width="3"/>
      <path d="M235 229h-18m262 0h18" stroke="${G(p)}" stroke-width="4"/>
      <circle cx="471" cy="223" r="8" fill="${G(p)}"/>`;
  }
  function sceneCrossflow(p){
    return `${pile(p,347,319)}
      <path d="M331 129v200" stroke="${M(p)}" stroke-width="18"/>
      <ellipse cx="349" cy="127" rx="111" ry="22" fill="${K(p)}" stroke="#7acbd2" stroke-width="3"/>
      <ellipse cx="349" cy="324" rx="111" ry="19" fill="${K(p)}" stroke="#79c0cd" stroke-width="3"/>
      <path d="M245 145l2 162 22 10-2-184zM427 143l-1 167 24-7 3-153z" fill="${B(p)}" stroke="#b5ffee" stroke-width="2.1"/>
      <path d="M347 134v185" stroke="#bde3e2" stroke-width="2.5" opacity=".65"/>
      <path d="M247 215h202M247 285h202" stroke="${M(p)}" stroke-width="6" stroke-linecap="round"/>
      ${gen(p,459,301,65)}`;
  }
  function sceneHelical(p){
    const ribbons = Array.from({length:3},(_,a)=>{
      const phase=a*2*Math.PI/3,points=[];
      for(let j=0;j<=52;j++){const f=j/52;const x=346+82*Math.sin(phase+f*2.7*Math.PI),y=117+f*213;points.push(x.toFixed(2)+","+y.toFixed(2));}
      return `<polyline points="${points.join(" ")}" fill="none" stroke="${a===1?M(p):B(p)}" stroke-width="${a===1?15:20}" opacity="${a===1?.71:1}" stroke-linejoin="round" stroke-linecap="round"/>`;
    }).join("");
    return `${pile(p,345,325)}
      <path d="M344 105v231" stroke="${M(p)}" stroke-width="14"/>
      <ellipse cx="346" cy="112" rx="86" ry="16" fill="${K(p)}" stroke="#77cad2" stroke-width="3"/>
      ${ribbons}<ellipse cx="346" cy="335" rx="84" ry="16" fill="${K(p)}" stroke="#77c8d6" stroke-width="3"/>
      ${gen(p,467,310,70)}`;
  }
  function sceneSavonius(p){
    return `${pile(p,345,328)}
      <path d="M344 120v212" stroke="${M(p)}" stroke-width="12"/>
      <ellipse cx="344" cy="120" rx="101" ry="23" fill="${K(p)}" stroke="#9cd6da" stroke-width="3"/>
      <path d="M344 139C217 129 228 237 317 226C409 218 400 326 343 324L327 327C461 350 498 228 375 223C273 217 288 159 361 152Z"
        fill="${B(p)}" stroke="#d8fff0" stroke-width="3" opacity=".96"/>
      <path d="M337 145C435 151 460 188 383 232C292 283 293 305 364 319" fill="none" stroke="${G(p)}" stroke-width="4" opacity=".55"/>
      <ellipse cx="345" cy="330" rx="102" ry="22" fill="${K(p)}" stroke="#91d3d7" stroke-width="3"/>
      ${gen(p,469,323,74)}`;
  }
  function sceneFoil(p){
    return `${pile(p,348,335)}
      <path d="M348 108v213" stroke="#83b8c0" stroke-width="5" stroke-dasharray="9 12"/>
      <path d="M347 116v47m-10-12 10 12 10-12M347 255v52m-10-12 10 12 10-12" fill="none" stroke="#ffd39e" stroke-width="3"/>
      <path d="M209 212Q329 173 494 223Q367 258 209 212Z" fill="${B(p)}" stroke="#bcfff4" stroke-width="3"/>
      <path d="M231 216Q339 208 465 222" stroke="#eafff9" stroke-width="3" opacity=".63" fill="none"/>
      <circle cx="339" cy="217" r="17" fill="${M(p)}" stroke="#f3fff0" stroke-width="2"/>
      <path d="M339 237v66h119" stroke="${M(p)}" fill="none" stroke-width="9" stroke-linejoin="round"/>
      <path d="M412 169q44 17 19 59m16-12-16 12-8-14" stroke="${G(p)}" stroke-width="3" fill="none"/>
      ${gen(p,458,286,85)}`;
  }
  function sceneScrew(p){
    const paths = Array.from({length:3},(_,k)=>{
      const phase=k*Math.PI*2/3,pts=[];
      for(let i=0;i<=84;i++){
        const t=i/84,angle=phase+t*4.7*Math.PI;
        pts.push((205+t*309).toFixed(1)+","+(224+84*Math.sin(angle)).toFixed(1));
      }
      return `<polyline points="${pts.join(" ")}" fill="none" stroke="${k===1?M(p):B(p)}" stroke-width="22" stroke-linecap="round" opacity="${k===1?.78:1}"/>`;
    }).join("");
    return `${pile(p,344,337)}<path d="M178 223h388" stroke="${M(p)}" stroke-width="14"/>
      <ellipse cx="209" cy="224" rx="24" ry="84" fill="${K(p)}" stroke="#a5e0da" stroke-width="3"/>
      ${paths}<ellipse cx="515" cy="224" rx="22" ry="80" fill="${K(p)}" opacity=".75" stroke="#77ccd8" stroke-width="3"/>
      ${gen(p,525,200,86)}`;
  }
  function sceneKite(p){
    return `<path d="M343 344v17m-49-15h98" stroke="#74afbc" stroke-width="5"/>
      <path d="M331 348Q309 296 355 203" fill="none" stroke="${G(p)}" stroke-width="3" stroke-dasharray="8 6"/>
      <path d="M158 269Q334 63 542 272" fill="none" stroke="#5cc7d4" stroke-width="2.8" stroke-dasharray="5 9" opacity=".73"/>
      <path d="M347 193L266 163 188 178Q289 116 346 137Q402 118 510 181l-91-18z" fill="${B(p)}" stroke="#bdfff3" stroke-width="3"/>
      <path d="M266 163l81 30 72-30m-130-8 55-17 56 17" fill="none" stroke="#e6fff5" stroke-width="3" opacity=".47"/>
      ${fan(p,275,180,31,17)}${fan(p,425,180,31,-16)}
      <circle cx="350" cy="188" r="13" fill="${M(p)}" stroke="#f0fff0" stroke-width="2"/>
      <path d="M346 202Q339 275 344 350" stroke="#ffd39b" stroke-width="2" fill="none" stroke-dasharray="7 8"/>`;
  }
  function sceneDuct(p){
    return `${pile(p,346,315)}
      <path d="M180 125Q257 151 330 151H400Q480 150 536 116L523 305Q473 277 401 276H326Q244 279 180 313Z" fill="${K(p)}" stroke="#86d8d7" stroke-width="4"/>
      <path d="M189 148Q265 178 330 177H404Q477 178 527 150" stroke="#84c2ce" opacity=".66" stroke-width="2" fill="none"/>
      <path d="M191 288Q258 254 330 254H404Q480 259 527 286" stroke="#93d8d8" opacity=".7" stroke-width="2" fill="none"/>
      <ellipse cx="351" cy="214" rx="81" ry="86" fill="#0b3045" stroke="#57acb7" stroke-width="7"/>
      ${fan(p,348,214,74,16)}
      <path d="M230 131h-25m0 0 14-10m-14 10 14 10M504 303h31" fill="none" stroke="${G(p)}" stroke-width="3"/>
      ${gen(p,469,310,79)}`;
  }
  function scenePressure(p){
    return `<path d="M178 235Q265 199 345 221Q429 239 479 209L482 277Q436 267 344 273Q253 256 184 279Z" fill="${K(p)}" stroke="#8de2dc" stroke-width="3"/>
      <path d="M206 241Q288 245 345 238T463 235" fill="none" stroke="${E(p)}" stroke-width="3" stroke-dasharray="9 5"/>
      <path d="M354 239V120Q354 98 381 98H481" fill="none" stroke="${M(p)}" stroke-width="15" stroke-linejoin="round"/>
      <path d="M357 237V123Q359 106 382 106H480" stroke="#c2fff4" opacity=".48" stroke-width="3" fill="none"/>
      <rect x="482" y="77" width="120" height="70" rx="14" fill="${K(p)}" stroke="#95dfdc" stroke-width="3"/>
      ${fan(p,533,111,29,23)}
      <path d="M454 99h25m-8-8 8 8-8 8M311 206v-25m-8 8 8-8 8 8" stroke="${G(p)}" stroke-width="2.7" fill="none"/>
      <path d="M356 246v109" stroke="${M(p)}" stroke-width="11"/><path d="M308 353h95" stroke="#8ed0d5" stroke-width="5"/>`;
  }
  function sceneEel(p){
    const fins = [0,1,2,3,4,5].map(i=>`<path d="M${276+i*38} ${214+(i%2)*12}l24 -15" stroke="${G(p)}" stroke-width="3" opacity=".8"/>`).join("");
    return `<path d="M211 174v169" stroke="${M(p)}" stroke-width="23"/>
      <path d="M180 337h63v18h-63z" fill="${K(p)}" stroke="#8acbd2" stroke-width="2"/>
      <path d="M227 225C263 136 317 297 363 212S462 134 517 223" fill="none" stroke="${B(p)}" stroke-width="22" stroke-linecap="round"/>
      <path d="M227 225C263 136 317 297 363 212S462 134 517 223" fill="none" stroke="#b6fff6" stroke-width="3" opacity=".8"/>
      ${fins}<path d="M481 229Q515 280 550 297" fill="none" stroke="${E(p)}" stroke-width="4" stroke-dasharray="6 7"/>
      ${gen(p,537,289,78)}`;
  }
  function sceneViv(p){
    return `<path d="M332 350v-18h80v18" fill="none" stroke="${M(p)}" stroke-width="7"/>
      <path d="M317 318Q288 304 317 288Q347 272 315 255Q282 239 318 220" fill="none" stroke="${G(p)}" stroke-width="4"/>
      <path d="M404 318Q433 304 404 288Q376 272 407 255Q438 239 402 220" fill="none" stroke="${G(p)}" stroke-width="4"/>
      <rect x="334" y="127" width="57" height="209" rx="28" fill="${M(p)}" stroke="#d4fff1" stroke-width="3"/>
      <path d="M350 145v170" stroke="#f6fffa" stroke-width="5" opacity=".51"/>
      <path d="M331 143q-54 28 0 65t0 69m69-134q51 28 0 65t0 69" fill="none" stroke="#62d6e1" stroke-width="3" stroke-dasharray="7 8"/>
      <path d="M391 224h91v-17h28v60h-28v-17h-91" fill="none" stroke="${M(p)}" stroke-width="8"/>
      ${gen(p,506,203,79)}`;
  }
  const SCENES={seabed:sceneSeabed,floating:sceneFloating,counter:sceneCounter,rim:sceneRim,crossflow:sceneCrossflow,helical:sceneHelical,savonius:sceneSavonius,foil:sceneFoil,screw:sceneScrew,kite:sceneKite,duct:sceneDuct,pressure:scenePressure,eel:sceneEel,viv:sceneViv};
  const points={
    seabed:[[291,180],[367,306],[409,228]],
    floating:[[431,237],[336,94],[538,286]],
    counter:[[282,165],[434,216],[347,290]],
    rim:[[405,168],[344,226],[460,238]],
    crossflow:[[246,209],[344,274],[451,286]],
    helical:[[410,178],[361,239],[449,326]],
    savonius:[[423,210],[331,302],[351,143]],
    foil:[[340,220],[346,150],[490,319]],
    screw:[[338,155],[255,225],[527,256]],
    kite:[[326,146],[420,181],[341,301]],
    duct:[[207,171],[355,221],[497,335]],
    pressure:[[250,243],[369,110],[526,112]],
    eel:[[374,214],[430,239],[554,306]],
    viv:[[302,204],[362,220],[497,226]]
  };
  const boxes=[["left",19,99],["left",19,279],["right",505,77]];
  function annotations(key){
    const labels=META[key],targets=points[key];
    if(!labels||!targets)return "";
    return labels.map((label,i)=>{
      const [edge,x,y]=boxes[i],tx=targets[i][0],ty=targets[i][1],startX=edge==="left"?x+145:x;
      const yy=y+16;
      return `<g class="art-annotation"><path d="M${tx} ${ty}L${startX} ${yy}" fill="none" stroke="#86d7db" opacity=".83" stroke-width="1.4"/>
        <circle cx="${tx}" cy="${ty}" r="3.8" fill="#fed79a" stroke="#062437" stroke-width="1.5"/>
        <rect x="${x}" y="${y}" width="150" height="32" rx="7" fill="#092333" fill-opacity=".93" stroke="#407a8a" stroke-width="1.1"/>
        <rect x="${x+1}" y="${y+1}" width="3" height="30" rx="1.5" fill="#f6c680"/>
        <text x="${x+13}" y="${y+20}" font-family="Arial,sans-serif" font-weight="600" font-size="12" fill="#dbfaf3">${escapeText(label)}</text></g>`;
    }).join("");
  }
  function render(key,options={}){
    if(!KEYS.includes(key))throw Error("Unknown TidalLab concept illustration "+key);
    const variant=options.variant||(options.large?"main":"overview"),p=id(key,variant);
    const index=String(options.index||KEYS.indexOf(key)+1).padStart(2,"0");
    const name=escapeText(options.name||key);
    const alt=`Illustrative underwater mechanical schematic of ${name}, concept ${index}; not a manufactured drawing or validated performance model.`;
    const labels=options.annotations===false?"":annotations(key);
    const title=options.thumb?"":`<g font-family="Arial,sans-serif"><text x="22" y="30" fill="#a8ebea" font-size="11" letter-spacing="2" font-weight="700">TIDAL / LAB · CONCEPT ${index}</text>
      <text x="680" y="30" text-anchor="end" fill="#afd7da" font-size="10" letter-spacing="1.2">TECHNICAL CONCEPT • NOT TO SCALE</text></g>`;
    const footer=options.thumb?"":`<g font-family="Arial,sans-serif"><path d="M23 383h75" stroke="#75b6c1" stroke-width="2"/><path d="M23 377v12m75-12v12" stroke="#75b6c1" stroke-width="1"/><text x="108" y="388" fill="#a2cbd2" font-size="10">SCHEMATIC GEOMETRY / NO DIMENSION CLAIM</text><text x="674" y="388" fill="#98cbd5" font-size="10" text-anchor="end">FLOW DIRECTION →</text></g>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${options.thumb?"112 62 475 305":"0 0 700 410"}" preserveAspectRatio="xMidYMid meet" role="${options.thumb?"presentation":"img"}" ${options.thumb?'aria-hidden="true"':`aria-label="${alt}"`} class="tidal-artwork tidal-artwork-${key}">
      ${defs(p)}${ambient(p,key==="floating"||key==="pressure")}${SCENES[key](p)}${title}${labels}${footer}</svg>`;
  }
  function thumb(key){return render(key,{thumb:true,annotations:false,variant:"thumb"});}
  root.TidalArtwork = Object.freeze({
    version:"2.0.0",
    keys:Object.freeze([...KEYS]),
    has:key=>KEYS.includes(key),
    render,thumbnail:thumb
  });
})(typeof window === 'undefined' ? this : window);
