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
