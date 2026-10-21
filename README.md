# TidalTurbine

Evidence-led tidal-stream turbine research and reproducible engineering screening, with special attention to Nova Scotia and the Bay of Fundy.

**Status (2026-10-20): research prototype, not a validated turbine design.** No measured site current, structural loads, fatigue life, device reliability, ecological safety, or cost claims are established by this repository.

## Research objective

Compare established tidal-stream architectures and test falsifiable improvements in lifetime electricity delivered, serviceability, environmental performance and lifecycle economics. Do not assume floating/recoverable/modular is superior. Tidal stream is intermittent at slack water and cannot alone serve continuous electrical demand.

## Quick start

Python 3.10+ (standard library only):

```sh
python -m unittest discover -s tests -v
python -m tidal_screen.cli --config configs/synthetic_screen.json --out reports/SCREEN-001.json
python scripts/check_catalogue.py
```

The first screen uses **synthetic** signed currents and a constant power coefficient. Electrical curtailment does **not** imply lower thrust or fatigue. The model, test suite and reproducible report are in this repository; see `docs/SIMULATION.md` for assumptions and `docs/CONTINUATION.md` for the next research gate.

## Scope, boundaries and provenance

- Tidal **stream** (horizontal-axis, cross-flow, ducted, floating, bottom-fixed, kite, powertrains, blade control, arrays) is the primary scope; wave-energy and barrages/lagoons remain separate.
- Tag records as: published evidence, manufacturer/project claim, engineering assumption, design hypothesis, simulation result, experimentally validated finding, or unknown/conflict.
- Track the depth of each review and its access gaps; prefer primary reports and reproducible experimental datasets.
- **Do not** treat software checks, analytical limiting cases, unvalidated simulations or vendor claims as full-scale validation.
- Do not deposit copyrighted works or unapproved large datasets into Git history.
- Respect Mi'kmaq interests, fisheries, ocean users and regulators; current speed is not site suitability.

## Repository layout

See `AGENTS.md` and `docs/CONTINUATION.md` for custodian rules and precise next actions, `research/` for evidence, `tidal_screen/` for Python models, `configs/` and `reports/` for reproducible experiments, `tests/` for verification, and `.github/workflows/` for CI.

## Initial public references

Sandia Reference Model Project: https://energy.sandia.gov/programs/renewable-energy/hydrodynamic-energy-systems/projects/reference-model-project-rmp/

RealTide Deliverable 1.1: https://tidalenergydata.org/media/documents/RealTide_Deliverable_1.1.pdf

DFO Bay of Fundy monitoring guide: https://www.dfo-mpo.gc.ca/publications/pnw-ppe/tidal-energy-energie-maremotrice/bay-fundy-aeemp-baie-fundy-pasee-eng.html

This repository is for research; it provides no engineering certification, environmental authorization, grid-interconnection approval, or construction specification.

## TidalLab — GitHub Pages research viewer

The static [TidalLab workbench](https://jeremyhennessy.github.io/TidalTurbine/) is an interactive *research prototype*, not a validated device or site resource forecast. It includes desktop/mobile architectural visualizations of four established turbine concepts, the archived **synthetic** SCREEN-001 experiment with a browser-only electrical export-cap slider, a source-backed Nova Scotia ocean-data atlas, and the staged validation roadmap. The Pages URL only becomes usable after GitHub Pages publishes the updated `main` branch; see [Pages application notes](docs/PAGES_APP.md).

### Data discovery and local preview

The [ocean-source registry](research/ocean_datasets.json) has **21 source/discovery records, not 21 independent deployments**. Complete processed [FORCE spring-2018 currents](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html) and companion waves, plus independent CMAR Digby DG013 data, are acquired and source-checksum verified. OCEAN-020 is a duplicate file-access route for OCEAN-001, not an additional campaign. FORCE has **263,250** processed velocity records, including **97,911** exact all-component zeros; the new **56-day × 50-cell numeric quality grid** is NOT source-native beam QC. CMAR has **531** observations with gross-range flags. **Zero observations are scientifically qualified for tidal turbine modelling.** See [ingestion gates](docs/INGESTION_GATE_20261020.md), [native source QC recovery](docs/FORCE_NATIVE_QC_RECOVERY_20261020.md) and [source-pinned grid](research/observations/FORCE_DAILY_CELL_QUALITY_V1_2018.json).

```sh
python scripts/check_ocean_catalogue.py
python scripts/acquire_force_adcp.py --dataset currents   # dry-run only
python scripts/build_site.py --out dist
python -m http.server 8000 --directory .                # open /site/
```

The original 14-day synthetic SCREEN-001 power model, its report and its assumptions remain unchanged. Export curtailment never demonstrates less thrust, fatigue or repair cost.

## Measured cross-flow operating-point research

[RM2-TRADEOFF-001](reports/RM2-TRADEOFF-001.md) compares **published laboratory processed means** of Cp and streamwise Cd at different tip-speed ratios on the same 1:6 cross-flow rotor and nominal inflow. It identifies an experimentally observed *mean* power-versus-drag tradeoff; cyclic loads, controller energy, fatigue, lifetime economics and field validity remain untested. Replay with `python scripts/rm2_operating_points.py`.

## Complete spring-2018 FORCE observed-data screening (acquired, **not engineering qualified**)

Both complete FORCE/CIOOS Atlantic **processed** NetCDF sources—currents and companion waves—are acquired, checksum-pinned and reproducibly audited in [FORCE full-campaign QA](docs/FORCE_FULL_CAMPAIGN_QA_20261020.md). The analysis covers 5,265 timestamps × 50 instrument-relative bins; **zero** bins have passed native instrument/source QC for turbine-energy prediction. Review the [compact per-cell/daily QA](reports/FORCE-CAMPAIGN-QA-001.json), [daily source-derived table](research/observations/FORCE_CAMPAIGN_DAILY_QA_2018.csv) and [acquisition run](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39484948868). Original binaries are in a time-limited GitHub Actions artifact, **not** Git. No visual/UI changes accompany this ingestion.

```sh
python -m pip install -r requirements-ocean.txt
python scripts/process_force_campaign.py --archive /path/to/force-spring2018-complete-processed-netcdf.zip --prior-72h-archive /path/to/force-adcp-72h-raw-qa-ccby4.zip
python scripts/check_force_campaign_report.py
```


## Prototype testing readiness — October 2026

**No in-water device has been built or validated.** The 2018 FORCE processed campaign contains 263,250 records but **zero** source-approved turbine-inflow records. CMAR DG013 provides 531 independent wave/sensor-speed readings with gross-range QA, not a qualified 3-D rotor-height inflow profile.

The original native FORCE archive and metadata share still return server errors: four independent bounded public GET requests gave HTTP 500 in [Actions 39518864052](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39518864052). See [native archive access gate](docs/FORCE_NATIVE_ACCESS_PROBE_20261020.md). No original Nortek beams, geometry/quality masks, or approved inflow has been recovered.

The [seven-site, tidal-prototype-only Nova Scotia shortlist](docs/TIDAL_TEST_SITE_SELECTION_2026-10-20.md) and [site evidence table](research/TIDAL_TEST_SITE_SCREEN_2026-10-20.csv) separate early remote reconnaissance (Rocky Run), historical open-water precedent (Grand Passage) and extreme-load later tests (FORCE). The previous Grand Passage PLAT-I installation was decommissioned and removed in 2023: no accessible berth is proven. The October 2026 demonstration permit is for eligible grid-connected projects at least TRL 4 within designated Fundy areas; this project has not demonstrated those criteria and has no permit.

A [falsifiable load-versus-energy and three-prototype test plan](docs/LOAD_AND_PROTOTYPE_TEST_PROTOCOL_20261020.md) and [machine-readable protocol](research/experiment_protocol_v1.json) specify required synchronized phase/torque/strain/control electricity and independent ecological, manufacturing, maintenance and permit gates. [Fail-closed validation checks](scripts/check_validation_readiness.py) prevent mistaking this research plan for physical validation. Original TidalLab and SCREEN-001 simulations are unchanged.


## Current quality inspector and physical load admission (October 20, 2026)

The TidalLab ocean atlas adds an independent 56-day-by-range **numerical QA inspector**, below the existing FORCE cell overview and without changing historical turbine designs, SCREEN-001, RM1 or RM2 plots. Check the pinned file with `python scripts/check_force_daily_quality.py` or regenerate from the original FORCE archive using `python -m scripts.build_force_quality_grid --archive /path/to/source.zip`. `tidal_screen/measured_load_gate.py` computes descriptive net electricity and bending metrics **only for physically sourced synchronized load and power channels**; no actual such trace has been acquired. See [load protocol](docs/RM2_LOAD_VALIDATION_PROTOCOL_20261020.md) and the newer canonical [prospective experiment specification](research/experiment_protocol_v1.json). No validated fatigue or design winner is claimed.
