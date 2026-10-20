# SCREEN-001: synthetic export cap, not derating loads

Question: What *exported electricity* does a 20%-below-nameplate grid export cap sacrifice in an illustrative 14-day two-harmonic synthetic current? The test is a numerical screening subquestion of H-001; it does **not** test blade load reduction.

Baseline and comparison share **identical** 10m diameter, 1025 kg/m³ seawater density, Cp=0.4, eta=0.9, 0.7m/s cut-in, 200kW rated, and time-varying inflow. Only export limit changes from 200kW to 160kW. No component failure or downtime occurs, by assumption; no physical response to a capped export is modeled.

Local initial outcome (`Python 3.11+ standard library`, run on 2026-10-20; full input and runtime metadata in `SCREEN-001.json`):

| Metric | Synthetic screening output |
|---|---:|
| Baseline export, 14 days | 22,228.713 kWh |
| Capped export, 14 days | 21,155.828 kWh |
| Difference | 1,072.886 kWh (4.827%) |
| Midpoint timestep | 300 s |
| Convergence 150 vs 75 s relative difference | 0.00347% |
| Assumed sensitivity combinations | 81 |
| Sensitivity energy range | 6,307.174–50,600.430 kWh (parameter combinations vary; not uncertainty bounds) |

**Decision:** a tight grid export cap costs energy under these assumptions; do not assume benefits to equipment. Investigate physically valid Cp/Ct/rotor controller datasets before evaluating lifetime-benefit hypothesis H-001. Negative or zero-benefit cases remain part of the record. Limitations: synthetic inflow, idealized constant Cp, no bidirectional yaw penalty, turbulence, wakes, fatigue, marine ecology, maintenance, curtailment control or dissipative system, and no measured Nova Scotia resource.

Reproduce: `python -m tidal_screen.cli --config configs/synthetic_screen.json --out reports/SCREEN-001.json`. Tests: `python -m unittest discover -s tests -v`. The report JSON records provenance SHA256; view containing Git SHA after publication. No project or manufacturer simulation is claimed.
