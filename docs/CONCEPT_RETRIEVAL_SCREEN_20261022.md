# Concept 003: parametric retrieval interference screen

Date: 2026-10-22. Classification: **ENGINEERING_ASSUMPTION / DESIGN_HYPOTHESIS / SYNTHETIC GEOMETRY RESULT**. This extends the dimensioned Concept 002 desk study, not an experimentally validated device. It is not build-ready CAD, a lift plan or environmental approval.

## Useful design finding

An inline dry PTO can avoid the assembly at rest yet obstruct the whole assembly during vertical extraction. Moving that PTO outside the assumed corridor removes that particular box intersection, but an independently placed sensor can still consume the assumed maintenance margin. Checking the rotor alone would miss the shaft-inclusive extraction envelope.

Comparator: the same crossflow assembly and deck with inline versus parked PTO. Mechanism: clearing the vertically swept assembly envelope. Falsifier: real packaging, connections or the relocation trajectory obstruct the corridor or prevent maintainable disconnection. Required evidence: qualified interface CAD, actual supplier dimensions, surveyed host/deck geometry and professional access/lifting review. No architecture is selected and no energy, cost, ecological or reliability advantage is inferred.

## Reproduce and explore

Run `python scripts/build_site.py --out dist`, serve `dist` with an HTTP server, then open `site/#designs`. The new panel is below the existing design comparison. It has three example configurations, three architecture choices and four numeric assumption controls. The 14 existing drawings and scientific evidence displays are unchanged.

- `node --test tests/test_clearance.cjs tests/test_clearance_ui.cjs`: 26 deterministic model/DOM tests.
- `node tests/ui_smoke.cjs`: existing artwork/evidence UI regression check.
- `python -m unittest discover -s tests -v`: 125 inherited tests, 112 pass and 13 optional-source skips in the current local environment.
- `node --check site/clearance_model.js` and `node --check site/clearance.js`.

DOM tests use a stub, not a browser. A separate `clearance-browser` Actions job installs pinned [official Playwright v1.56.1](https://github.com/microsoft/playwright/releases/tag/v1.56.1), serves the exact built candidate over local HTTP and runs real Chromium at 1440 × 1000 and 390 × 844. It tests interactions, error/unknown states and horizontal fit, and preserves screenshots for visual review. `node tests/clearance_browser.cjs` runs that job's test when its browser dependency is available. This is not a production Pages parity check. Actual browser rendering, mobile interaction and hosted parity remain a separate **pending** gate. Local Chromium launch was blocked by the runner; no browser success or visual approval is claimed. Remote exact-commit Actions status must be checked separately. Do not merge before independent code review and actual browser/mobile validation.

## Explicit assumed geometry, metres

Coordinates: x streamwise, y transverse, z upward. z = 0 is an illustrative datum, not a qualified water level.

| Item | Assumed bounds / dimensions |
|---|---|
| Whole CF-LIFT-2 module | x,y each −0.70 to +0.70; z −1.70 to +0.95; height 2.65 |
| Straight vertical translation | +2.60; raised top z +3.55 |
| Horizontal service margin | default 0.10; selectable 0–0.30; no vertical margin added |
| Square hatch | default 1.60; selectable 1.40–2.00; deck z +0.65 to +0.75 |
| PTO | 0.50 × 0.50 × 0.40; y centred at zero; z +1.05 to +1.45; x centre variable |
| Sensor | 0.10 × 0.20 × 0.20; y centred at zero; z −0.90 to −0.70; x centre variable |
| Axial submerged/dry PTO alternatives | Streamwise assembly lengths UNKNOWN. Return indeterminate; do not substitute CF geometry. |

Default inline PTO x centre = 0; parked example = 1.15. Outer sensor x centre = 0.95; near sensor = 0.80. These are illustrative packaging inputs only, not manufacturer dimensions or site observations.

For horizontal margin c, the model minimum square opening is 1.40 + 2c. With PTO half-width 0.25, positive-x centre must be at least 0.70 + c + 0.25. At c = 0.10 these are 1.60 m and 1.05 m. Minimum centre does not establish an accessible parking position or relocation route.

## Algorithm and limits

The swept box spans the initial module bottom through the translated top; x/y extents are expanded by the selected margin. Each listed obstacle is tested for strict positive overlap in all three dimensions. Exact tangency at the padded boundary is accepted by this mathematical model, with no demonstrated fabrication tolerance or safety reserve. Tiny positive intersections remain flagged; no hidden tolerance is introduced. Box overlap is conservative potential interference, not exact CAD contact. A no-interference result covers the listed boxes only.

Excluded: real shapes; rigging, crane and hook envelope; guide contacts; hatch doors; cables and disconnects; PTO relocation path; people and rescue access; deformation; manufacturing tolerances; wave/tide motion; load, strength, fatigue and corrosion; sensor field of view; ecological effects. Plan/side figures are projections of the same three-dimensional calculation, not independent two-dimensional collision tests.

FORCE still has zero qualified inflow cells. Required native configuration/beam QC/export lineage is absent. RM2 original target records and physical encoder registration remain unresolved; the frozen comparison is unexecuted. No denied raw source was retried. Separate environmental/permit/rights and engineering gates remain intact.

## Design continuation, not permission

1. Replace assumed boxes with qualified component/interface envelopes, including cables and disconnect tooling, without claiming unknown dimensions are measurements.
2. Model the entire PTO relocation and crane/rigging path only once those envelopes and host geometry are known.
3. Independently review access, load cases, uncertainty and environmental monitoring before any physical programme. This software grants no construction, lifting, site-access or wildlife authorization.

## Acceptance update, 2026-10-22 11:53 UTC

The earlier pending-browser paragraph records the initial draft state. Subsequently, exact reviewed head `736d0bef8fd0a436667a06003c30cd2515d8b78a` passed all six push/PR checks. Actual Chromium at 1440×1000 and 390×844 exercised normal-navigation pointer access, fail-closed states, contrast and horizontal fit. Initial screenshots failed contrast review; corrected screenshots were rerun and inspected, with independent bounded new-panel visual acceptance. PR CI run: https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39767419817. The reviewed source was merged as `6118db4ac1a6748575171d07f8a3cd69c70c6ed7`. Main CI/Pages/live-byte verification is separate. This acceptance covers Concept003, not the subsequently added Concept004 service-energy panel; neither implies Safari/device or engineering/ecological validation.
