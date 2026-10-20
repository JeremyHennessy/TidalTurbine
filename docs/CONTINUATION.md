# CONTINUATION — authoritative checkpoints and current research gates

Repository scope: `JeremyHennessy/TidalTurbine` **only**. Re-fetch the exact live `main` head, open PRs/issues, Actions and `AGENTS.md` before making changes. This file is a chronology, not permission to overwrite later work or to force-push. Do not infer deployed Pages from passing CI.

## Immutable foundation publication checkpoint — verified 2026-10-20

The following historical state is preserved verbatim in substance from `main` at `45ca55c2ce8a2be08de7c0e331f660e5548343b0`, **not** replaced by PR #6's earlier prepublication draft:

- Initially empty repository; bootstrapped README on `main` in `ecece2049bf8defec45bc912d316e1f4e98fd9c2`.
- Foundation branch `research/foundation-2026-10-20`: `f2fe7bb5aaa146223c9c8ae90f492b9645851f55`, then `acfaac76215e5abf38c57437addd9450834d62fb`.
- [PR #1](https://github.com/JeremyHennessy/TidalTurbine/pull/1) merged via squash to `79e62ee3620990955d41f293147df5b16aed932f`: the first **23** files. Local **13/13** Python tests, **21** original catalogue records; remote byte-for-byte readback of model, CLI, tests, evidence, experiment, instructions and workflow. Exact-head two-version PR CI and subsequent [main CI](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39457324035) completed successfully.
- Subsequent documentation PR #2 merged, establishing `main` **`45ca55c2ce8a2be08de7c0e331f660e5548343b0`**. [Post-merge Actions](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39457931706) passed on Python 3.11 and 3.12.
- Historical `reports/SCREEN-001.json` is an unchanged synthetic 14-day, 300s midpoint, 200kW-rated export-cap comparison: baseline **22,228.713 kWh**, 80%-capped **21,155.828 kWh**, difference approximately **4.827%**. Its **electrical energy penalty proves no change in blade loads, fatigue, availability, ecology or service costs**. Preserve the original report bytes and accompanying assumptions.

## Ocean-data and first TidalLab PR — reconciled historical checkpoint

[PR #6](https://github.com/JeremyHennessy/TidalTurbine/pull/6) began from `main` `45ca55c2ce8a2be08de7c0e331f660e5548343b0`; reviewed PR head `f72ea1eb9625137b8562dbe48809bde100dc335c`, [exact-head CI 39463308157](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39463308157) **success** for Python 3.11/3.12. This is a premerge checkpoint; check live PR status afresh. PR #6 contributes **20 ocean source/discovery records, not 20 measured datasets**, and the original approved four illustrative turbine drawings plus responsive Pages research UI. Its initial local test count rose from **13 foundation tests** to **25 on reviewed PR head**; counts refer to **different commits**, not contradictions. The original continuation draft in that PR accidentally dropped the immutable foundation history; this document explicitly repairs that regression.

## Mechanism and alternative-benchmark pass — working scope until verified publication

- `research/mechanisms.json`: **14 configuration exemplars** across multidimensional primary capture mechanisms (axial, cross-flow, drag, oscillating foil, axial screw, kite, duct, secondary pressure, flexible piezoelectric, vortex-induced vibration). Configurations mix independent choices; their count does **not** equal a count of mutually exclusive inventions. The original four visual designs are preserved; additional **illustrative** schematics are added.
- `research/CLAIM_AUDIT.csv`: 14 marketing/physics claim audits. Coverage expanded in `research/MECHANISM_EVIDENCE.md` and `research/COVERAGE.md`; research bibliography grows from 21 to **30** entries. Distinguish source inspection depth and vendor/partner testimony.
- `reports/RM2-OBS-001.json`: repeatable reproduction of **23 previously processed measured** cross-flow tow-tank observations from UNH `Data/Processed/Perf-1.0.csv` at immutable source Git blob `1f284211d5c19593cf753e63727ae62a62356439`. Peak reported Cp **0.3546025** at TSR **3.0993495**, using published processed columns rounded to seven places. It is **not** raw-sensor reprocessing, independently validated hydrodynamic prediction, net electrical power, full-scale certification, or a Nova Scotia tidal-site model. Source CC BY 4.0; MIT code.
- `tidal_screen/foil_balance.py`: dimensions-checked force×heave-velocity + moment×pitch-angular-velocity energy balance, subtracting actuation and conversion losses. Not a fitted hydrodynamic performance curve. Maintains a separate standard from the SCREEN-001 open-rotor cubic equation.
- FORCE ADCP metadata and bounded two-hour QA request are documented in `docs/FORCE_QA_GATE.md`. **Real-world FORCE current observations NOT YET ACQUIRED** due local DNS/network access failure. The code's passing fixture-based QA tests do not mean the real dataset passed scientific QC. `cell_range` is not vertical height above bottom until instrument metadata verifies the geometry.
- Sandia RM1 dual-axial experimental reports and metadata have been located, but the actual experimental Cp/TSR quantity has **NOT been reproduced**; do not present RM2 as satisfying RM1 issue #3.
- Updated UI uses canonical mechanism records and separately charts measured processed RM2 coefficient points. Do not display an unsupported output ranking, an RM2 Nova Scotia energy forecast or physical load improvements. Keep the original SCREEN-001 slider behavior and four foundational diagrams.

### Reproducible verification commands

```sh
python -m unittest discover -s tests -v
python scripts/check_catalogue.py
python scripts/check_ocean_catalogue.py
python scripts/check_mechanisms.py
python scripts/reproduce_rm2.py
python scripts/qa_force_slice.py                 # defaults to dry run, no download
python scripts/build_site.py --out dist
node --check site/app.js
python -m tidal_screen.cli --config configs/synthetic_screen.json --out reports/local-check.json
```

For SOURCE acquisition, review FORCE terms and use `python scripts/qa_force_slice.py --fetch` **only** in an environment with external network access. A saved source slice must record raw file SHA, UTC timestamps, missing/rejected values, coordinate/range-cell metadata and QC limitations; do not feed it to energy simulation absent publisher sensor geometry/QC and justified vertical sampling.

### Prioritized decision gates — not a broad speculative backlog

1. **Reproduce RM1 quantitatively** — continue [issue #3](https://github.com/JeremyHennessy/TidalTurbine/issues/3): exact experimental runs, measured datum, blade count, Cp/TSR denominator, source figure/table precision, digitization/measurement uncertainty. Distinguish transcribing published values from validating a predictive model. Reuse RM2 for the first cross-flow solver holdout once an appropriate actual model is available.
2. **Acquire/QA a measured FORCE ADCP sample, then longer suitable coverage** — record time, site coordinates, instrument deployment/tilt and upward cell geometry, flags/gaps/ensemble cadence, vector convention, sample and licence checksums. Never infer annual currents, extremes or site suitability from a two-hour slice. See `docs/FORCE_QA_GATE.md`.
3. **Net power + reliability falsifiers** — continue [issues #4](https://github.com/JeremyHennessy/TidalTurbine/issues/4) and [#5](https://github.com/JeremyHennessy/TidalTurbine/issues/5): measured pitch/torque/actuator consumption, blade loads, access windows and retrieval incidents for representative architectures. No synthetic failure rates, Cp ranking or unsupported ecological safety claims.

## Publication checkpoint after this work

Before reporting completion, append the *verified* merged head and remote post-merge Actions status; if publication still in progress, state the exact open PR and head instead. A successful branch CI does **not** mean Pages is live. Verify the actual Pages URL independently and preserve an immutable visual baseline only after user approval. No recurring agent is operating because this file exists.
