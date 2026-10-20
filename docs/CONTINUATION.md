# CONTINUATION — verified foundation baseline 2026-10-20

Scope: `JeremyHennessy/TidalTurbine` **only**. Before every new change, fetch default-branch HEAD, PRs/issues and workflow statuses. **Do not assume this handoff's recorded SHA is still current.**

## Immutable verified publication checkpoint

- Initially empty repository; bootstrapped main README at `ecece2049bf8defec45bc912d316e1f4e98fd9c2`.
- Foundation branch `research/foundation-2026-10-20` committed at `f2fe7bb5aaa146223c9c8ae90f492b9645851f55`, then final README at `acfaac76215e5abf38c57437addd9450834d62fb`.
- [PR #1](https://github.com/JeremyHennessy/TidalTurbine/pull/1) was **merged** via squash, yielding main checkpoint **`79e62ee3620990955d41f293147df5b16aed932f`**. At this checkpoint, remote tree contains 23 files, including README, AGENTS, research, model, 13 tests, experiment and workflow.
- Exact-head PR and branch CI succeeded for Python 3.11 and 3.12. The [post-merge main Actions run](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39457324035) completed with `success`.
- Remote byte-for-byte readback versus local source was confirmed for `tidal_screen/model.py`, `tidal_screen/cli.py`, `tests/test_model.py`, `research/catalogue.json`, `reports/SCREEN-001.json`, `AGENTS.md` and workflow; remote report baseline and catalogue count were independently read back from main.
- This handoff itself is a **follow-up documentation change**; the merge SHA above is the verified *foundation checkpoint*, not necessarily the live head after this handoff merges.


## Actual local findings and state

- Reviewed sections of RealTide D1.1 FMEA (executive summary, FMEA method, sec. 7.1–7.2, conclusion); it prioritizes electrical systems, rotors and drivetrain across *generic concept decompositions*, NOT empirical MTBF estimates.
- Read Sandia Reference Model Project download index and portions of RM1 experimental report including its uncertainty analysis; full numerical validation/data acquisition still missing.
- Reviewed Gambuzza et al. passive-pitch paper introduction/discussion/conclusions and relevant methods; model-scale reduced fluctuations do not demonstrate commercial wear or service life.
- Reviewed DFO Bay of Fundy adaptive monitoring guide, province tidal overview/demonstration permit, FORCE project and Mi'kmaq research landing pages. Treat developer self-report and grant-project claims separately.
- `SCREEN-001`: dependency-free synthetic electrical export model. 14 days, midpoint 300s, 200-kW rated, 80% export cap; baseline ~22,228.713 kWh, capped ~21,155.828 kWh, difference ~4.827%. This is **no evidence of fatigue reduction**. Source hashes are recorded in `reports/SCREEN-001.json`.
- `python -m unittest discover -s tests -v`: 13/13 local passed on 2026-10-20; `python scripts/check_catalogue.py`: 21/21 structural records passed. The identical published source was tested in GitHub Actions on Python 3.11 and 3.12 at the verified foundation checkpoint. Always rerun after changes.

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

Do not edit approved historical experiment results merely to update a moving SHA. Preserve this verified foundation checkpoint, and add subsequent verified commit/CI checkpoints in new entries. No scheduled agent is running by virtue of this handoff.
