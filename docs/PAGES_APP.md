# TidalLab GitHub Pages research app — UX specification and boundaries

## Objective
A responsive, accessible *research workbench* for comparing established tidal-stream architectures and examining the verified SCREEN-001 numerical result. **A visualization of a device concept is not design engineering.** A synthetic power curve must remain visually differentiated from real measured ocean data.

## Routes (static, client-side hash)

- `#overview`: hero, research state, illustrative turbine SVG, archived experiment values, source discovery and six-stage validation progression.
- `#designs`: four SVG architecture **mockups** (seabed HAT, recoverable floating, cross-flow, tethered kite), choice selector, annotations, pros/cons and specific falsification evidence. No scored ranking/winner.
- `#experiments`: read `reports/SCREEN-001.json`. Replot two synthetic harmonics, baseline vs 80%-rated export cap, and archived 81-case sweep. Slider 50–100% runs **browser-only electrical** calculation; does not mutate report or infer blade load, Cp change, structural life, or ecological safety.
- `#ocean`: approximate labelled Fundy schematic with one precisely documented FORCE instrument coordinate marker (45.3631, -64.4275), curated metadata table, search/type filters, data access status and expanded provenance/source links. No invented current values, no false cartographic precision.
- `#research`: stages, actual evidence qualification status, source read path and three next gates.

**No subscription or build service:** static HTML, SVG, JS, CSS; Python stdlib for test/site copying; no third-party JavaScript or embedded external maps. Text is encoded before injection. Mobile single-column layout; nav expands on small viewports; accessible link/focus/section labels; prefers-reduced-motion respected.

## Hosting

Repository-root `index.html` redirects to `site/`. All static files and canonical experiment/metadata JSON are committed to the repo; Pages can publish directly from main/root. The `.nojekyll` sentinel avoids Jekyll transformations. The site fetches relative canonical paths `../reports/SCREEN-001.json` and `../research/ocean_datasets.json`; paths work both locally and with repository-subpath GitHub Pages. **Check live Pages settings and complete post-merge deployment before claiming a public URL**; GitHub Actions tests are not a substitute for browser inspection.

Local preview:

```sh
python scripts/build_site.py --out dist
python -m http.server 8000 --directory .
# Open http://localhost:8000/ (or /site/)
```

The `dist/` folder also contains the static artifact (root redirect + `site/`, archived JSON and registry), reproducibly copied by the builder. Build artifacts and raw datasets are not checked into Git.

## Visual regression / approval

This iteration introduces the first TidalLab visual language; no previously approved UI existed. After a screenshot is approved, lock that commit + screenshot and do not restyle the approved state for unrelated data/logic fixes. A design-review screenshot is not a scientifically calibrated illustration.

## Boundaries and next functionality

Not yet implemented: validated measured ADCP series visualization, RM1 benchmark overlays, physical blade/control model, solver visualization, authenticated collaborative edits, downloadable signed design files, grid-scale scheduling/battery dispatch and environmental risk prediction. Add each **only** when source and validation gates are met. GitHub Pages serves public files; sensitive Traditional Knowledge or restricted survey products must not be uploaded.

## Multidimensional mechanisms and observed-benchmark extension (2026-10-20)

**Do not replace approved foundational illustrations.** The original four conceptual diagrams (seabed HAT, floating recoverable, cross-flow, kite) and SCREEN-001 electrical-cap slider remain the same visual and numerical baselines. The explorer has ten additional labeled technical **concept** schematics and filters the fourteen configuration exemplars by capture mechanism, using the exact `research/mechanisms.json` canonical fields (source URL, PTO, support, motion, reference-area boundary, evidence depth, lack of validation). These are not CAD/CFD field results. The taxonomy is multidimensional: a fixed/variable pitch, seabed/floating support or duct is not a new fundamental energy mechanism.

The experiment page separates two different epistemic categories: the unchanged **synthetic SCREEN-001** electrical cap model and **observed processed experimental RM2** Cp/CD-v-TSR tow-tank points, copied as a bounded CC BY 4.0 seven-decimal subset of a pinned source. `reports/RM2-OBS-001.json` has exact configuration and code to reproduce; only 23 observed runs at nominal 1.0 m/s for a 1:6 cross-flow model. No prediction of Bay of Fundy generation, structural life or physical superiority. Instrument FORCE data remains a **source-discovery** atlas, not a chart of downloaded current measurements. The app must not claim it is a site simulator.

After any merge, verify the remote `main` commit, publication of `research/mechanisms.json` and `reports/RM2-OBS-001.json`, and successful current-run Actions. Independently navigate `https://jeremyhennessy.github.io/TidalTurbine/` on desktop/mobile before saying the live Pages site is updated. A Pages build job's success alone is insufficient to prove the new JavaScript and data load in a browser.

## Verified measured-source update — no physical predictions (2026-10-20)

One short FORCE ADCP CSV was **acquired** in GitHub Actions run 39470715965 and analyzed independently, unlike the preceding metadata-only status. There were 450 numeric entries, but **206 exact all-component zero vectors** (21 entirely zero instrument range cells). The QA report is now a small provenance-linked **observational warning** in `reports/FORCE-SLICE-QA-001.json`, linked from the existing *Ocean data* panel. Pages must not chart these vectors as depth-corrected flow or treat them as validated resource or power output until source masking, instrument geometry and QC have been verified. This is a small content/link correction; no approved design diagrams, layout, sizing, filters or experimental-scenario logic are restyled. `scripts/build_site.py` includes only the derived QA report JSON (not third-party raw observations) in the self-contained site build.

## Additive design-comparison and observed-drag UX pass (2026-10-20)

The design explorer retains its original primary drawing and explanation, and adds a two-architecture study board with the same canonical `research/mechanisms.json` capture/motion/support/PTO details, limitations, evidence questions and primary links. The second selector compares illustrations and outstanding evidence, **not numerical device winners**. It uses existing SVGs, without CAD or new physics assumptions.

The experiment viewer adds a companion `RM2-TRADEOFF-001` graphic using the unchanged published-processed means and selection budgets from `reports/RM2-TRADEOFF-001.json`. Separate Cp and Cd bar lanes use **within-coefficient** reference normalization; no cross-quantity magnitude comparison, fatigue benefit, field effect, validated controller or physical-load inference is implied. The original 23-point RM2 Cp chart and synthetic SCREEN-001 chart/slider/report remain unchanged. The static build now copies the derived tradeoff report and exercises the new DOM rendering in a dependency-free Node smoke test.

The research status text now reports the actual **two-hour acquired FORCE sample with unresolved zero-vector masks and instrument QC**, without presenting those velocities as quality-approved. This additive change is submitted for review, not assumed to be an approved visual baseline or verified Pages deployment.

## Reconciliation with merged FORCE 72h and RM1 study (2026-10-20)

After independent research PR #13 merged as main `682afa7a2d6d32af0a7eb251235b14c5e32f4e63`, TidalLab's displayed evidence-status copy was reconciled: the FORCE panel now describes a **numerically acquired 72-hour sample** with 14,400 numeric vectors, 5,160 exact all-zero triples and 12 wholly zero range cells, while scientific native beam/mask QC and the discrepancy between source range label 1.5 m and reported first-cell-centre 2 m remain unresolved. It links both the derived 72-hour QA report and historical 2-hour QA JSON; the build copies the derived `reports/FORCE-72H-QA-001.json`, never raw sensor observations. No measured currents have entered any rotor/load model.

Stage 2 and the next-step copy acknowledge the separately reproduced **RM1 axial published 32-row table** but explicitly retain the missing predictive-solver, thrust and time-resolved fatigue validations. The two architecture comparison diagrams and RM2 processed mean tradeoff remain illustrative and descriptive, respectively. These are data-backed content/packaging corrections, not a new site performance model, layout redesign or physical validation. UI rendering was visually checked from the Git-blob-matched static source using offline Chromium (network navigation unavailable). Live Pages and visual user approval remain separate checkpoints.
