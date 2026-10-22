(function () {
  'use strict';
  function boot() {
    const panel = document.getElementById('service-energy-lab');
    if (!panel) return;
    const byId = id => document.getElementById('service-energy-' + id);
    const fields = ['waitH', 'taskH', 'recommissionH', 'monitorW', 'restartWh'];
    const fmt = value => String(Number(value.toPrecision(6)));
    function read(id) {
      const raw = byId(id).value;
      if (raw.trim() === '') throw new Error('Every assumption requires a number');
      return Number(raw);
    }
    function budget(value) {
      return 'Outage: ' + fmt(value.outageH) + ' h\nPotential terminal energy: ' + fmt(value.potentialKWh) + ' kWh\nLost during outage: ' + fmt(value.lostKWh) + ' kWh\nContinuous monitoring: ' + fmt(value.monitorKWh) + ' kWh\nRestart import: ' + fmt(value.restartKWh) + ' kWh\nNet accounting result: ' + fmt(value.netKWh) + ' kWh';
    }
    function update() {
      try {
        const input = {powerW: read('powerW'), periodH: read('periodH'), baseline: {}, candidate: {}};
        for (const side of ['baseline', 'candidate']) for (const field of fields) input[side][field] = read(side + '-' + field);
        const result = TidalServiceEnergy.compare(input);
        panel.dataset.result = 'SYNTHETIC_ACCOUNTING_RESULT';
        byId('status').textContent = 'Candidate minus reference: ' + fmt(result.deltaKWh) + ' kWh under these assumptions. No architecture ranking.';
        for (const side of ['baseline', 'candidate']) byId(side + '-budget').textContent = budget(result[side]);
        byId('balance').textContent = 'Recovered outage energy ' + fmt(result.recoveredKWh) + ' kWh, minus extra monitoring ' + fmt(result.extraMonitorKWh) + ' kWh, minus extra restart import ' + fmt(result.extraRestartKWh) + ' kWh.';
        byId('threshold').textContent = result.equalityAttainableWithNonnegativeMonitor
          ? 'Equal-net threshold: total candidate monitoring power ' + fmt(result.equalNetCandidateMonitorW) + ' W, with every other input unchanged. This is not an adopted acceptance target.'
          : 'No nonnegative candidate monitoring power reaches equal net energy under these inputs. Mathematical equality would require ' + fmt(result.equalNetCandidateMonitorW) + ' W.';
      } catch (error) {
        panel.dataset.result = 'INVALID_INPUT';
        byId('status').textContent = 'No result: ' + error.message + '.';
        for (const id of ['baseline-budget', 'candidate-budget', 'balance', 'threshold']) byId(id).textContent = '';
      }
    }
    byId('reset').addEventListener('click', function () {
      const values = TidalServiceEnergy.example();
      for (const id of ['powerW', 'periodH']) byId(id).value = String(values[id]);
      for (const side of ['baseline', 'candidate']) for (const field of fields) byId(side + '-' + field).value = String(values[side][field]);
      update();
    });
    panel.addEventListener('input', update);
    update();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}());
