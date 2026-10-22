# Concept 004: conditional service-energy accounting

2026-10-22. **ENGINEERING_ASSUMPTION / DESIGN_HYPOTHESIS / SYNTHETIC_ACCOUNTING_RESULT**. Published app; acceptance is limited to software consistency and Chromium viewports, not physical validation. This is a direct application port of the delivered Concept 002 single-event model, not new tidal performance evidence.

## Useful design constraint

Saving six elapsed outage hours at an assumed constant 250 W recovers1.5 kWh. An extra continuous 10 W over 168 h consumes 1.68 kWh, so the net difference is −0.18 kWh. Faster hands-on service alone is therefore insufficient to demonstrate better net energy. The equality point is 8.92857 W total candidate monitoring power when reference monitoring is 0 W and all other differences are held fixed. This is not an adopted acceptance threshold or measured requirement.

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

There is no annualization or measured service frequency, actual tidal phase/time series, weather/access distribution, power curve, blade loads, changing electrical efficiency, shared auxiliary power states, cost model or reliability prediction. Constant power misses the distinction between a slack-water outage and a high-output outage. The default 12 h access wait and 1 h recommissioning per option are illustrative, not observed operational durations.

Hypothesis: reduced outage can improve net export if the saved opportunity energy exceeds additional auxiliary and restart demand. Comparator: same hypothetical generator/period, alternate service option. Falsifier: qualified paired energy and task records show no net gain. Necessary evidence: permitted task timings, access/weather constraints and separately metered generation, monitoring and restart energy. No fieldwork, physical action or outreach is authorized by this software.

FORCE remains 0 qualified inflow cells. RM2 target originals and physical encoder registration remain unresolved; frozen comparison remains unexecuted. Axial assembly dimensions remain unknown. No architecture winner or environmental benefit follows. Engineering, environmental, permitting, fisheries, marine-use and Mi'kmaq rights/engagement gates remain separate.

## Verification and acceptance scope

- `node --test tests/test_clearance.cjs tests/test_clearance_ui.cjs tests/test_service_energy.cjs tests/test_service_energy_ui.cjs`: 48 pass (26 inherited Concept 003 plus 22 new).
- `python -m unittest discover -s tests`: 125 run, 112 pass, 13 optional-source skips.
- `node tests/ui_smoke.cjs`: existing 14-design smoke pass.
- `python scripts/build_site.py --out dist`: 24 source files plus `.nojekyll`.
- A separate reproducibility cross-check compared the JS port against all 108 delivered Concept 002 scenarios, checking 1,404 numeric equalities within 1e−10. This is software consistency, not physical validation or independent engineering review.

The added DOM tests are stubs, not browser execution. Independent desk/code review found no math or static blocker and reran all 22 new tests. This is not professional engineering review. Actual Chromium at 1440×1000 and 390×844 passed the dedicated Concept 004 interactions, contrast, normal-navigation pointer access and invalid-state checks. All six new images were inspected; independent bounded panel visual review found no blocker. Both exact-head push/PR workflows passed for `e1f5a5af374bbb3d14137c1b3ce1c3e4d5479918`, subsequently merged as `8f9d779de15eca73d27029b7e630e9bc9c0a6728` in PR31. Pages deployment 39774716288 passed and all 13 checked public HTTP assets matched source bytes. Final main CI status is recorded in the release checkpoint in `docs/CONTINUATION.md`. These are Chromium viewport and HTTP byte-parity checks, not Safari/WebKit, physical-device or live-browser verification. Concept 003 acceptance was not substituted for this panel's own tests.
