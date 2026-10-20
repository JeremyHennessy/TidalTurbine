# Decision log

| Date | ID | Decision | Basis | Reopen when |
|---|---|---|---|---|
| 2026-10-20 | D-001 | Use site-agnostic synthetic power screening first. | Real site data not acquired; avoid invented site/performance claims. | Documented, licensed measured time series exists. |
| 2026-10-20 | D-002 | Hold rotor geometry optimization and design-winner selection. | RM1 measured benchmark not reproduced; no validated loads/fatigue/cost. | Independent experiment reproduced and load model validated. |
| 2026-10-20 | D-003 | Separate electrical export limiting from rotor-load derating. | Fixed Cp alone gives no relationship between delivered kWh and thrust. | Validated Ct/Cp/control/load relationships available. |
| 2026-10-20 | D-004 | Use standard-library Python + fast GitHub CI. | Zero paid API and deterministic local/CI reproducibility. | Evidence demands specialist tools and licenses are verified. |
| 2026-10-20 | D-005 | Treat floating/recoverable as hypothesis, not invention or winner. | Existing commercial implementations and additional failure interfaces. | Comparable lifecycle data and tests support choice. |
| 2026-10-20 | D-006 | Keep data-centre integration as a distinct later workstream. | Primary bottleneck is physically benchmarked turbine performance. | Baseline validation established. |
