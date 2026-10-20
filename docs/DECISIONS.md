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

### 2026-10-20 / QA-HOLD-001 — acquired does not mean usable

- The one-shot public FORCE CSV acquisition **succeeded**, unlike earlier local network attempts: original 30,276 B with pinned SHA-256 in `reports/FORCE-SLICE-QA-001.json` and provenance log. Basic numeric-screen acceptance (450/450) was not a quality approval. **206/450** velocity triples equal exact zero, with **21 full range cells zero**. Whether those are masked/no-return/out-of-water data cannot be determined from the downloaded subset; zero may be physical in other contexts. Mark all such vectors **unresolved**, not silently removed or accepted as true still-water.
- Do not feed either zero or nonzero vectors from this slice into energy estimates until transducer geometry, heading/tilt, water level and source QC are qualified. Preserve only SHA-linked derived reports in normal Git. A two-hour sample cannot support annual design-site resource decisions.

### 2026-10-20 / RM2-TRADEOFF-001 — examine measured drag along with mechanical power

- In the one nominal-1m/s RM2 test matrix, derive a bounded **mean Cp vs mean Cd** descriptive operating-point comparison from previously processed source measurements. A lower-TSR choice shows lower mean Cd and lower mechanical Cp, not a proved fatigue/maintenance benefit. The experiment is meaningful for choosing the next simultaneous structural-load/control measurement, **not** selecting a turbine winner, a deployment site, or a synthetic reliability law.
