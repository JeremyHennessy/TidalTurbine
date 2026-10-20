# Decision log

| Date | ID | Decision | Basis | Reopen when |
|---|---|---|---|---|
| 2026-10-20 | D-001 | Use site-agnostic synthetic power screening first. | Real site data not acquired; avoid invented site/performance claims. | Documented, licensed measured time series exists. |
| 2026-10-20 | D-002 | Hold rotor geometry optimization and design-winner selection. | RM1 measured benchmark not reproduced; no validated loads/fatigue/cost. | Independent experiment reproduced and load model validated. |
| 2026-10-20 | D-003 | Separate electrical export limiting from rotor-load derating. | Fixed Cp alone gives no relationship between delivered kWh and thrust. | Validated Ct/Cp/control/load relationships available. |
| 2026-10-20 | D-004 | Use standard-library Python + fast GitHub CI. | Zero paid API and deterministic local/CI reproducibility. | Evidence demands specialist tools and licenses are verified. |
| 2026-10-20 | D-005 | Treat floating/recoverable as hypothesis, not invention or winner. | Existing commercial implementations and additional failure interfaces. | Comparable lifecycle data and tests support choice. |
| 2026-10-20 | D-006 | Keep data-centre integration as a distinct later workstream. | Primary bottleneck is physically benchmarked turbine performance. | Baseline validation established. |

### 2026-10-20 / DATAVIEW-001 — evidence-first public research interface

- Choose a self-contained GitHub Pages static app over paid hosting or a simulation-backed 3D engine. Scope: research viewer, illustrative architectural SVGs and the archived SCREEN-001 electrical comparison. No new turbine designs, load claims or deployment permissions are approved.
- A source inventory counts discovery metadata separately from acquired/QA-vetted field data; FORCE 2018 ADCP is available for acquisition with CC BY 4.0 attribution, but raw files remain excluded from normal Git.
- Preserve existing synthetic baseline/experiment and its test semantics. Measured velocity data must pass instrument-frame/depth/time/QC checks before any physically responsible modelling; measured inflow alone does not calibrate rotor Cp/Ct or fatigue.
- Host at the existing Pages destination if settings permit; never claim live deployment from local screenshots alone.
