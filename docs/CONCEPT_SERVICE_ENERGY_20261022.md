# Concept 004: conditional service-energy accounting

2026-10-22. **ENGINEERING_ASSUMPTION / DESIGN_HYPOTHESIS / SYNTHETIC_ACCOUNTING_RESULT**. Local candidate only, not published or browser-accepted. This is a direct application port of the delivered Concept002 single-event model, not new tidal performance evidence.

## Useful design constraint

Saving six elapsed outage hours at an assumed constant 250W recovers1.5kWh. An extra continuous10W over168h consumes1.68kWh, so the net difference is−0.18kWh. Faster hands-on service alone is therefore insufficient to demonstrate better net energy. The equality point is8.92857W total candidate monitoring power when reference monitoring is0W and all other differences are held fixed. This is not an adopted acceptance threshold or measured requirement.

The app allows twelve explicit assumptions: shared terminal opportunity power/period; access wait, elapsed hands-on duration, recommissioning duration, separate monitoring power and restart import for each of two service options. It shows both complete accounting budgets and a signed difference. No turbine architecture is assigned either option.

## Equations and units

For each option, let P be assumed constant terminal opportunity power in W, T the modeled period in h, D access wait plus task plus recommissioning in h, M separate continuous monitoring power in W and R restart import in Wh.

E_net = [P(T−D) − MT − R] / 1000 kWh.

Delta = P(D_reference−D_candidate)/1000 − (M_candidate−M_reference)T/1000 − (R_candidate−R_reference)/1000.

Total candidate monitoring power giving equal net energy is:

M_candidate,equal = M_reference + [P(D_reference−D_candidate) − (R_candidate−R_reference)] / T.

A negative equality power is kept and described as unattainable with nonnegative monitoring consumption. It is not clamped to zero. Negative net budgets are retained as net import. No special tolerance is used to adopt a design decision. Display values have six significant digits; full double-precision values drive calculations.

## Boundary and missing evidence

Exactly one nonoverlapping service event per option. Task duration is elapsed clock time, not worker-hours. Monitoring is on throughout the whole period, including outage. Terminal opportunity power excludes the separately entered monitoring and restart imports. Do not also subtract these demands inside P. Both options must have matched initial/final stored energy; reconcile any battery or other stored-energy change before interpreting the accounting difference as net export. Inputs are bounded finite nonnegative numbers; T must be positive and every total outage must fit the period. Bounds are numerical UI limits, not engineering feasibility limits.

There is no annualization or measured service frequency, actual tidal phase/time series, weather/access distribution, power curve, blade loads, changing electrical efficiency, shared auxiliary power states, cost model or reliability prediction. Constant power misses the distinction between a slack-water outage and a high-output outage. The default12h access wait and1h recommissioning per option are illustrative, not observed operational durations.

Hypothesis: reduced outage can improve net export if the saved opportunity energy exceeds additional auxiliary and restart demand. Comparator: same hypothetical generator/period, alternate service option. Falsifier: qualified paired energy and task records show no net gain. Necessary evidence: permitted task timings, access/weather constraints and separately metered generation, monitoring and restart energy. No fieldwork, physical action or outreach is authorized by this software.

FORCE remains0 qualified inflow cells. RM2 target originals and physical encoder registration remain unresolved; frozen comparison remains unexecuted. Axial assembly dimensions remain unknown. No architecture winner or environmental benefit follows. Engineering, environmental, permitting, fisheries, marine-use and Mi'kmaq rights/engagement gates remain separate.

## Local verification and remaining gates

- `node --test tests/test_clearance.cjs tests/test_clearance_ui.cjs tests/test_service_energy.cjs tests/test_service_energy_ui.cjs`:48 pass (26 inherited Concept003 plus22 new).
- `python -m unittest discover -s tests`:125 run,112 pass,13 optional-source skips.
- `node tests/ui_smoke.cjs`: existing14-design smoke pass.
- `python scripts/build_site.py --out dist`:24 source files plus.nojekyll.
- A separate reproducibility cross-check compared the JS port against all108 delivered Concept002 scenarios, checking1,404 numeric equalities within1e−10. This is software consistency, not physical validation or independent engineering review.

The added DOM tests are stubs, not browser execution. Independent desk/code review found no math or static blocker and reran all 22 new tests. This is not professional engineering review. Actual Chromium desktop/mobile-view interaction, screenshots, exact pushed CI and live parity are still pending. Concept003's accepted browser images do not accept Concept004. The source is kept separate from reviewed PR30 head736d0bef8fd0a436667a06003c30cd2515d8b78a.
