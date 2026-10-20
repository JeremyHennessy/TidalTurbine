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


## Subsequent research pass — FORCE acquired-data QA and RM2 operating points (2026-10-20)

**Historical continuity:** Immutable foundation checkpoint `79e62ee3620990955d41f293147df5b16aed932f` and approved synthetic SCREEN-001 report are unchanged. Ocean/app merged `main` baseline `dd864309536bfa7a93edf6fd765e753c90372ebf` via PRs #6 and #7; its Actions #39470275812 passed Python 3.11/3.12 and Pages **build/deploy job** #39470274731 returned success. **An independent live URL browser verification is not recorded; do not claim it.** The prior paragraph saying no measured FORCE currents were acquired was true at the *earlier local-development checkpoint*, but has been superseded as follows.

1. **Actual bounded FORCE slice acquired** on GitHub Actions [run #39470715965](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39470715965) at probe commit `3a3ffa54998c2a24428c87cf0f22ab7c1392b659`. Two-hour original CSV source size 30,276 B; SHA-256 `1a19da1e3cd214fc904d8e821cc50c7e959693aaffa4dc9c8e84ee6c663ac4cb`, 450 numeric rows across 9 times and 50 ADCP range cells. One-day-retention artifact ID 12286987076 contained source.csv + qc.json. A previously invisible scientific QA issue was discovered: **206 exactly (0,0,0) vectors** and **21 range cells entirely zero**, possibly masked/fill values. No physical depth or valid water-column profile established. **Zero source measurements fed to turbine model.** See `reports/FORCE-SLICE-QA-001.md` and `docs/FORCE_QA_GATE.md`. Corrected ERDDAP comparator encoding and zero-mask warnings are in `scripts/qa_force_slice.py`; replay from original bytes with `scripts/review_force_artifact.py` and pinned SHA. Do not commit raw data.
2. **Measured RM2 within-one-rotor Cp/Cd operational tradeoff**: `reports/RM2-TRADEOFF-001.json`/`.md`, derived deterministically from the unchanged 23-row published processed cross-flow laboratory fixture at nominal 1.0 m/s. Candidate run TSR≈2.90 has measured-processed mean Cp ~1.85% below Cp-peak and Cd ~5.51% lower. This is **not** direct evidence of cyclic structural-load, fatigue or long-term-energy benefit, nor a controller or field model. Original [PLOS study](https://doi.org/10.1371/journal.pone.0163799) sections Uncertainty / Data Processing / Performance / Strut loss reviewed: ~10% uncorrected tank blockage and Reynolds/strut effects matter. PLOS paper overall Cp=0.37 at another Reynolds condition does not contradict the subset peak Cp≈0.3546.
3. **Other branches owned by independent concurrent work:** [site PR #8](https://github.com/JeremyHennessy/TidalTurbine/pull/8) and [test-site PR #9](https://github.com/JeremyHennessy/TidalTurbine/pull/9) are separate; do not overwrite, rebase or merge their unrelated files while advancing physics. No approved visual components of TidalLab were changed during this pass.

**Run/check commands** (all dependency-free Python standard library; numerical report reproduction does not need raw ADCP):

```sh
python -m unittest discover -s tests -v
python scripts/check_catalogue.py
python scripts/check_ocean_catalogue.py
python scripts/check_mechanisms.py
python scripts/reproduce_rm2.py
python scripts/rm2_operating_points.py
python scripts/qa_force_slice.py                    # dry run; no network
python scripts/review_force_artifact.py --zip <original-acquired-artifact.zip>  # optional offline replay; SHA-pinned, not CI-required
python scripts/build_site.py --out dist
node --check site/app.js
```

**Three decision gates, not a claim of new design superiority:** (1) **FORCE sensor geometry and publisher QC**: resolve all-zero values, beam/sidelobe boundaries, water-column masks before a longer representative series may enter hydrodynamics; (2) **measure time-resolved loads/control energy for RM2-like operating-point alternatives** while respecting uncertainties and Reynolds/blockage, and continue the RM1 source reproduction (issue #3 and #4); (3) **maintenance/recovery/weather-window evidence and site permit/Indigenous interests** (issue #5; separate site PRs #8/#9), with matched lifetime energy and environmental conditions. Later data-centre grid dispatch is separate.

**Publication handoff:** This section documents the new *proposed research work*, not a claim that it is merged. Verify exact PR head, remote file readback, Python 3.11/3.12 Actions checks and main post-merge status; append a later checkpoint after GitHub confirms merge. Never infer app live status solely from workflow success.

## Verified merged checkpoint — FORCE zero-mask / RM2 tradeoff (2026-10-20)

This later checkpoint **supersedes the immediately preceding proposal-only publication note**; it does not remove or alter the immutable historical foundation checkpoint.

- [PR #10](https://github.com/JeremyHennessy/TidalTurbine/pull/10) was merged into `main` as **`fbf446c56aeba04b7429f036496459c718c5429a`**, with the reviewed PR head `bde8112e1fd8d2e7ba081905986be2d89b5109f7` (20 October 2026 UTC).
- Source content remote readback matched **19/19** transferred project files; four additional narrow readme/app status/build/inventory edits independently verified; original `reports/SCREEN-001.json` and `reports/RM2-OBS-001.json` Git blobs confirmed unchanged.
- Local standard-library verification: **51/51 Python tests**, source bibliography (30) / mechanism (14) / ocean discovery (20) structural checks, original RM2 processed-data reproduction, new RM2 operating-point report, SHA-verified FORCE raw-artifact replay (no raw CSV in Git), static Pages build and Node syntax check passed.
- [PR exact-head CI 39475854905](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39475854905), [post-merge main CI 39476202319](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39476202319) both **success** on Python 3.11 and 3.12. [Pages deployment workflow 39476199324](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39476199324) **success** for that merge commit; independent live browser navigation still **not verified** and must not be asserted.
- Current model gate: acquired FORCE 2-hour sample has **450 numeric vectors, 206 exact all-zero triples, 21 entirely zero range cells**; no source-validated depth bins. **No measured FORCE velocity was fed into any turbine model.** RM2 descriptive Cp/Cd result demonstrates an observed mean power-versus-drag tradeoff **only**, not fatigue or lifetime advantage.
- Concurrent site-specific [PR #8](https://github.com/JeremyHennessy/TidalTurbine/pull/8) and [PR #9](https://github.com/JeremyHennessy/TidalTurbine/pull/9) remain separately owned/open as of this verification and may need normal rebase/reconciliation with this newer main. Do **not** overwrite their work or claim site selection/deployment.
- Next decisive task: resolve FORCE zero-mask/bathymetric geometry with primary instrument metadata; then measure or identify time-resolved RM2/HAT structural loads with controlled operating-point experiments and exact uncertainty. Preserve original SCREEN-001 and all negative/unknown records.


## Later validation pass — RM1 printed table and three-day FORCE study (2026-10-20)

This is additive to the **immutable** foundation, SCREEN-001, and merged FORCE/RM2 work above. Starting main **3d940ffe604c763f3ae4b1157411db49f7e9a195** was read before changing anything. Design/site PRs #8 and #9 were open and independently owned; none of their files were changed.

- Research branch \`research/force-rm1-design-gates-20261020\` first commit **\`6ca16b301692764cd72fab657633c7dfb5161fa9\`**. Exact-head deterministic CI [39482098783](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39482098783) passed, Python 3.11 and 3.12, after **61 local tests** with warnings treated as errors. Core historical experiments, original README, AGENTS and UI are unchanged.
- The branch-only, one-shot acquisition [run 39482098852](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39482098852) **succeeded**. It downloaded the 2018-04-01–2018-04-04 UTC FORCE current product into temporary [artifact 12292085881](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39482098852/artifacts/12292085881) with **7-day retention**, not the Git repository. Original CSV **1,310,499 bytes**, SHA-256 **\`d05f2a1258d9908b04fc7017cdb818ca318ac47c38e6b40244eac8c378ec4c7a\`**. Independent offline readback passed the source SHA and archived QA comparison.
- **14,400** numerically parseable velocity triplets at 288 time bursts and 50 instrument-relative ranges, 900s uniform published cadence; **5,160** exactly all-zero triplets; **12** range cells entirely zero (39.5–50.5m), **12** intermittently zero (27.5–38.5m), and **26** consistently nonzero (1.5–26.5m). The latter are **NOT** scientifically QC-approved. Recorded sensor pressure **31.8128–44.4779 dbar** and highest nonzero range **26.5–38.5m** yield descriptive **Pearson r≈0.996882** over 288 bursts. This strongly suggests tide-dependent upper-cell masking, but does **not** decode producer zero/fill rules. \`reports/FORCE-72H-QA-001.json\` stores compact reproducible results; \`scripts/force_72h_summary.py --zip <source-artifact.zip>\` checks full SHA, raw QA counts, pressure-boundary correlation.
- Newly reviewed peer-reviewed **Viehman et al., 2022** \`https://doi.org/10.3389/fmars.2022.851400\`, sec 2.1/2.2.2, confirms the **Nortek** ADCP upward-facing transducer **0.7m above seabed**, blanking **1m**, cell size **1m**, first cell centre **2m above face**, 5-min/2Hz bursts every 15 min, near-surface sidelobe masking in published study. The public ERDDAP range labels nevertheless begin **1.5m**, an unresolved **cell centre vs label** mapping discrepancy. Original native beam-quality, fill rules, tilt/frame correction and producer masks are still missing. **ZERO current bins qualified for turbine inflow; NO measured FORCE velocity entered any power or structural simulation.**
- \`reports/RM1-OBS-001.json\`: first **32** Sandia 2014 RM1 printed Appendix A rows reproduced separately for **16 right** and **16 left** rotor tests; right table maximum \`Cp=0.477\`, left max \`Cp=0.412\`. Report narrative describes approximate left \`0.43\`; preserve mismatch. Coarse \`P≈torque × 2π nominal rpm/60\` transcription sanity only, **NOT** raw time-resolved validation; thrust and \`Ct\` unavailable, no fatigue evidence.
- \`reports/RM2-VARIABILITY-001.json\`: source processed runs 10 versus 12 describe mean drag/power and instantaneous derived-coefficient spread plus between-revolution **mean** spread; just **9–10 revolutions**, not blade stress/torque spectra, no paired significance or life-cycle benefit. Do not rank it across rotor families.
- \`research/prototype_gates.json\`: three **unranked** candidate mechanisms (axial, cross-flow, oscillating foil) under prospective **assumed** test conditions, with independent hydrodynamic, site data, electrical export, fatigue, ecology, manufacture, and access gates. **No prototype winner, physical certification, commercial conclusion, or authorized field experiment**.

Run \`python -m unittest discover -s tests -v\`, \`python scripts/check_catalogue.py\`, \`python scripts/check_ocean_catalogue.py\`, \`python scripts/check_mechanisms.py\`, \`python scripts/check_prototypes.py\`, \`python scripts/reproduce_rm1.py\`, and \`python scripts/rm2_variability.py\`. Local follow-up validation after the 72h artifact included **64 Python tests**, some of which intentionally skip original artifact replays when the ZIP is unavailable in remote CI. Investigate generated reports by pinned hash, not parameter changes to historical results.

**Next gates:** (1) acquire native .ad2cp/beam correlation or publisher masking and resolve 1.5m vs 2m range mapping, then construct explicitly qualified bins/time masks across a longer period; (2) obtain synchronized cyclic blade/strut load histories and paired controller/PTO measurements for the RM2 operating-point question; (3) advance prototype environmental, maintenance/access, manufacturing and cost evidence under identical inflow conditions, without score-based winning.

**Publication state:** new research branch contains proposed work; verify its final PR merge and exact postmerge main CI before claiming final integration. GitHub Pages UI and physical designs were not changed.
