/* Concept 003: synthetic axis-aligned packaging screen, never lift approval. */
(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TidalClearance = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function finite(n) { return typeof n === 'number' && Number.isFinite(n); }
  function box(b) {
    if (!Array.isArray(b) || b.length !== 6 || !b.every(finite) || [0,2,4].some(i => b[i] >= b[i+1])) throw new Error('Six finite bounds with positive extents required.');
    return b.slice();
  }
  function sweep(initial, dz, margin) {
    const b = box(initial);
    if (![dz, margin].every(n => finite(n) && n >= 0)) throw new Error('Finite nonnegative lift and clearance required.');
    return [b[0]-margin,b[1]+margin,b[2]-margin,b[3]+margin,b[4],b[5]+dz];
  }
  function intersects(a,b) {
    a=box(a); b=box(b);
    return [0,2,4].every(i => Math.min(a[i+1],b[i+1]) > Math.max(a[i],b[i]));
  }
  function screen(initial,dz,margin,obstacles) {
    if (initial === null || dz === null) return {status:'UNRESOLVED_MISSING_ENVELOPE', conflicts:null};
    const swept=sweep(initial,dz,margin);
    const conflicts=Object.entries(obstacles).filter(([,b]) => intersects(swept,b)).map(([name]) => name);
    return {status:conflicts.length ? 'POTENTIAL_INTERFERENCE':'NO_BOX_INTERFERENCE_FOR_LISTED_OBJECTS_ONLY', conflicts, swept};
  }
  function evaluate(input) {
    if (!input || !['CF-LIFT-2','AX-POD-2','AX-DRY-2'].includes(input.layout)) throw new Error('Choose a listed architecture.');
    if (input.layout !== 'CF-LIFT-2') return {status:'UNRESOLVED_MISSING_ENVELOPE',conflicts:null,reason:'Axial streamwise assembly length is unknown. No clearance result can be calculated.'};
    const bounds={ptoX:[0,1.6],sensorX:[0.65,1.25],margin:[0,0.3],hatch:[1.4,2]};
    for (const [k,[lo,hi]] of Object.entries(bounds)) if (!finite(input[k]) || input[k]<lo || input[k]>hi) throw new Error(k+' must be a finite value from '+lo+' to '+hi+' m.');
    const h=input.hatch/2, p=input.ptoX, s=input.sensorX;
    const obstacles={
      'deck left':[-2,-h,-2,2,.65,.75], 'deck right':[h,2,-2,2,.65,.75],
      'deck front':[-h,h,-2,-h,.65,.75], 'deck back':[-h,h,h,2,.65,.75],
      PTO:[p-.25,p+.25,-.25,.25,1.05,1.45], sensor:[s-.05,s+.05,-.1,.1,-.9,-.7]
    };
    const initial=[-.7,.7,-.7,.7,-1.7,.95], dz=2.6;
    return Object.assign(screen(initial,dz,input.margin,obstacles),{initial,dz,obstacles,minimumHatch:1.4+2*input.margin,minimumPtoCenter:.95+input.margin});
  }
  return Object.freeze({box,sweep,intersects,screen,evaluate});
});
