/* Conditional single-service-event accounting, not a tidal performance model.
 * Assumes matched initial/final stored energy and no auxiliary double counting. */
(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TidalServiceEnergy = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const CLASSIFICATION = 'ENGINEERING_ASSUMPTION / SYNTHETIC_ACCOUNTING_RESULT';
  function quantity(value, name, max, nonzero) {
    if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > max || (nonzero && value === 0)) {
      throw new RangeError(name + ' must be a finite ' + (nonzero ? 'positive' : 'nonnegative') + ' number <= ' + max);
    }
    return value;
  }
  function option(powerW, periodH, input) {
    if (!input || typeof input !== 'object') throw new TypeError('Service option is required');
    const waitH = quantity(input.waitH, 'Access wait (h)', 87600);
    const taskH = quantity(input.taskH, 'Elapsed hands-on task (h)', 87600);
    const recommissionH = quantity(input.recommissionH, 'Recommissioning (h)', 87600);
    const monitorW = quantity(input.monitorW, 'Separate continuous monitoring (W)', 1000000);
    const restartWh = quantity(input.restartWh, 'Restart import (Wh)', 1000000000);
    const outageH = waitH + taskH + recommissionH;
    if (outageH > periodH) throw new RangeError('Service outage exceeds modeled period');
    const potentialKWh = powerW * periodH / 1000;
    const lostKWh = powerW * outageH / 1000;
    const monitorKWh = monitorW * periodH / 1000;
    const restartKWh = restartWh / 1000;
    return {outageH, potentialKWh, lostKWh, monitorKWh, restartKWh,
      netKWh: potentialKWh - lostKWh - monitorKWh - restartKWh};
  }
  function compare(input) {
    if (!input || typeof input !== 'object') throw new TypeError('Inputs are required');
    const powerW = quantity(input.powerW, 'Assumed terminal opportunity power (W)', 1000000);
    const periodH = quantity(input.periodH, 'Modeled period (h)', 87600, true);
    const baseline = option(powerW, periodH, input.baseline);
    const candidate = option(powerW, periodH, input.candidate);
    const recoveredKWh = baseline.lostKWh - candidate.lostKWh;
    const extraMonitorKWh = candidate.monitorKWh - baseline.monitorKWh;
    const extraRestartKWh = candidate.restartKWh - baseline.restartKWh;
    const deltaKWh = recoveredKWh - extraMonitorKWh - extraRestartKWh;
    // This is total candidate monitor power at equality, not extra power.
    const equalNetCandidateMonitorW = input.baseline.monitorW + (recoveredKWh - extraRestartKWh) * 1000 / periodH;
    return {classification: CLASSIFICATION, baseline, candidate, recoveredKWh,
      extraMonitorKWh, extraRestartKWh, deltaKWh, equalNetCandidateMonitorW,
      equalityAttainableWithNonnegativeMonitor: equalNetCandidateMonitorW >= 0};
  }
  function example() {
    return {powerW: 250, periodH: 168,
      baseline: {waitH: 12, taskH: 8, recommissionH: 1, monitorW: 0, restartWh: 100},
      candidate: {waitH: 12, taskH: 2, recommissionH: 1, monitorW: 10, restartWh: 100}};
  }
  return Object.freeze({compare, example});
}));
