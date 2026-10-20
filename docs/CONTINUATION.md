# CONTINUATION — initial tranche 2026-10-20

Scope: `JeremyHennessy/TidalTurbine` only. **Reconcile remote reality FIRST** before editing: default-branch SHA, PRs/issues, files, action runs and this document. This first-tranche handoff was written before remote publication; never treat the working SHA as a verified remote SHA until checked. See branch `research/foundation-2026-10-20` and PR, when created. The initial main commit was `ecece2049bf8defec45bc912d316e1f4e98fd9c2` (README only), not necessarily current after review/merge.

## Actual local findings and state

- Reviewed sections of RealTide D1.1 FMEA (executive summary, FMEA method, sec. 7.1–7.2, conclusion); it prioritizes electrical systems, rotors and drivetrain across *generic concept decompositions*, NOT empirical MTBF estimates.
- Read Sandia Reference Model Project download index and portions of RM1 experimental report including its uncertainty analysis; full numerical validation/data acquisition still missing.
- Reviewed Gambuzza et al. passive-pitch paper introduction/discussion/conclusions and relevant methods; model-scale reduced fluctuations do not demonstrate commercial wear or service life.
- Reviewed DFO Bay of Fundy adaptive monitoring guide, province tidal overview/demonstration permit, FORCE project and Mi'kmaq research landing pages. Treat developer self-report and grant-project claims separately.
- `SCREEN-001`: dependency-free synthetic electrical export model. 14 days, midpoint 300s, 200-kW rated, 80% export cap; baseline ~22,228.713 kWh, capped ~21,155.828 kWh, difference ~4.827%. This is **no evidence of fatigue reduction**. Source hashes are recorded in `reports/SCREEN-001.json`.
- `python -m unittest discover -s tests -v`: 13 local tests passed at creation. `python scripts/check_catalogue.py` and Action runs must be independently checked before claiming their status. Conditions may have changed; always rerun.

## Three next high-value actions

1. **RM1 measured benchmark**: acquire Sandia primary data tables / raw flume files and test geometry/license, build reproducible Cp-versus-TSR reproduction with digitization uncertainty if raw data unavailable; register checksums, domain and test case. First structural validation gate.
2. **Hydrodynamic loads with controls**: identify independently measured Cp/Ct and blade bending moment versus tip-speed, pitch and turbulence, including Gambuzza et al. dataset; make an explicit null/control comparison and prove/disprove whether controlled derating trades lifetime load for energy. No synthetic fatigue rates.
3. **Serviceability case**: obtain public maintenance/retrieval incident histories and weather-window distributions (MeyGen, FORCE/Orbital where available) to compare fixed/geared, direct-drive and recoverable designs with quantified uncertainty. Include connector/mooring and access failures, ecosystem effects and Indigenous priorities as gating constraints.

## Known blockers / cautions

- No verified public Fundy ADCP series ingested; no bathymetry, tidal extremes, operational downtime, ecological collision evidence, or engineering-certified cost/life model.
- DNV-ST-0164 public summary states edition 2015-10 amended 2021-11; full standard requires access; do not claim compliance.
- QBlade docs support marine mode but project licensing is APL non-commercial; commercial use requires separate permission. Specialist tool adoption is not approved by a tutorial alone.
- Original SAE MeyGen URL currently redirects to a corporate home page. Independent current project status should be rechecked before using vendor numbers.
- External URLs/access dates and all 'reviewed' statuses live in `research/catalogue.json`.

Run:
```sh
python scripts/check_catalogue.py
python -m unittest discover -s tests -v
python -m tidal_screen.cli --config configs/synthetic_screen.json --out reports/SCREEN-001.json
```

After merge, append exact merged SHA and Actions conclusion only once independently verified, preferably in a follow-up PR to avoid ambiguous in-flight self-references. No scheduled agent is running by virtue of this handoff.

## Second pass — TidalLab and Nova Scotia data discovery (working baseline 2026-10-20)

- Work started after confirming remote `main` `45ca55c2ce8a2be08de7c0e331f660e5548343b0`, existing issues #3–#5, no unknown active PR, and matching `AGENTS.md`. **This SHA is a starting checkpoint only**; re-fetch default head and PRs before changing files.
- New `research/ocean_datasets.json` catalogs 20 source/discovery entries, including FORCE 2018 ADCP currents/waves with explicit instrument metadata and CC BY licence, CHS IWLS, NONNA, GEBCO_2026, DFO hydrography/habitat/species, weather/monitoring/regulatory discovery. `docs/OCEAN_DATA.md` defines QA and acquisition. **No measured time series has been downloaded or passed into the simulator**.
- `scripts/acquire_force_adcp.py` has an opt-in source file download with SHA256, file-size bound and out-of-Git manifest, default no-network dry run. CI must never depend on availability of the external ERDDAP service.
- `site/` has five hash-routed research views, 4 conceptual technical SVGs, mobile UI, dataset searching, archived SCREEN-001 display and ephemeral export-cap what-if. Root `index.html` supports existing branch-based GitHub Pages; `scripts/build_site.py` stages a self-contained site. No structural or environmental predictions. `docs/PAGES_APP.md` records the UI limitations.
- Local creation checks: `python -m unittest discover -s tests -v` (24), `python scripts/check_catalogue.py` (21 records), `python scripts/check_ocean_catalogue.py` (20), `node --check site/app.js`, `python scripts/build_site.py`. Desktop/mobile screenshots rendered with Chromium using in-memory source data because HTTP/file browsing in this sandbox returned ERR_BLOCKED_BY_ADMINISTRATOR; actual remote Pages behavior remains a separate verification gate.
- **Next three actions:** (1) Download original FORCE NetCDF and scientifically QA geometry, UTC cadence, bins and QC gaps with exact SHA, no model run yet. (2) Reproduce published Sandia RM1 measured Cp/TSR benchmark with uncertainty. (3) Obtain validated Cp/Ct/loads and paired access/maintenance histories before evaluating power derating, floating versus fixed or cost/lifetime claims.
- Publishing status of this pass must be verified separately from these notes. After merge, record the exact remote SHA and Pages status in the handoff; never infer from passing local checks.
