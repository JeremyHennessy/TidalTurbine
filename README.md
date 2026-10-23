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

The [ocean-source registry](research/ocean_datasets.json) currently catalogs 20 source-discovery records, **not 20 acquired datasets**. This includes the publicly listed [FORCE March–May 2018 ADCP currents](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html), corresponding waves, CHS tides, NONNA, GEBCO 2026, DFO hydrography, habitat and ecological monitoring. A bounded two-hour FORCE 2018 ADCP source CSV was **actually acquired** in GitHub Actions run 39470715965 and numerically screened, but 206 of 450 three-component vectors are exact zero (21 range cells entirely zero). Instrument geometry and source QC remain unresolved; no measured currents have entered the simulator. See [FORCE observed-slice QA](reports/FORCE-SLICE-QA-001.md). See [data provenance and acquisition gates](docs/OCEAN_DATA.md).

```sh
python scripts/check_ocean_catalogue.py
python scripts/acquire_force_adcp.py --dataset currents   # dry-run only
python scripts/build_site.py --out dist
python -m http.server 8000 --directory .                # open /site/
```

The original 14-day synthetic SCREEN-001 power model, its report and its assumptions remain unchanged. Export curtailment never demonstrates less thrust, fatigue or repair cost.

## 2022 UNH native sensor-clock eligibility — October 23, 2026

The [original UNH 2022 source and synchronization audit](docs/UNH_2022_CLOCK_OVERLAP_GATE_20261023.md) recovered exact publisher source URLs/DOI/licence and documented **HTTP 429** for original STRAIN/THRUST/VOLTSYS/ADCP README access and the operational schedule. **Zero original archives, source-verified timestamps or qualified common intervals** were acquired. The new offline, bounded `python scripts/qualify_unh_2022_overlap.py` refuses to invent them and can later screen *locally supplied, SHA-pinned and source-QC documented* CSV timestamps for **provisional overlap candidates** only. No physical stress/fatigue/net electricity claim, outreach, source restriction bypass or UI redesign follows.

## Independent field strain and electrical measurement evidence (2026-10-23)

The [TidalLab Research panel](https://jeremyhennessy.github.io/TidalTurbine/site/index.html#research) now groups **12 unqualified lab measurement channels** and three separately limited recent published studies. The [source review](docs/FIELD_STRAIN_COMPARISON_20261023.md) identifies DOE public metadata for 17 possible 2022 UNH field instrument resources (blade strain, ADCP/ADV, thrust, Voltsys, IMU), not original acquired samples. The field turbine differs from RM2 and no source-validated overlap, fatigue, net-electricity or local FORCE inflow is established. The panel is a strictly additive Research view; prior UI and scientific models are unchanged.

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

The [October 23 measurement preregistration and metrology gate](docs/LAB_METROLOGY_PREREG_20261023.md) specifies all 12 synchronized source channels and 9 unresolved calibration/statistical/physical acceptance requirements, including unambiguous signed net-electricity metering. The **offline** `python scripts/check_metrology_protocol.py --toy` checks synthetic arithmetic and explicitly refuses physical validation. No instruments, thresholds, test frequency, sample count, contacts or purchases are selected.

The [October 23 rotor-exposure bound](docs/ROTOR_EXPOSURE_BOUND_20261023.md) explains how little idealized towing time may be available, and how to calculate *hypothetical* rotor turns/blade passages from explicitly assumed dimensions. These are **not fatigue cycles, electrical measurements or a real rotor design**. Offline: `python scripts/screen_rotor_exposure.py --assumed-diameter-m 0.6 --assumed-blades 3` (0.6 m/three blades are examples only).

The [offline October 23 lab venue and idealized tow-window study](docs/LAB_VENUE_SCREEN_20261023.md) verifies historic Aquatron research and Memorial towing-tank dimensions and published external list rates without authorizing contact. Its upper-bound steady-tow windows are assumptions, **not available test durations**; no instrumented prototype or confirmed facility exists. Run `python scripts/check_lab_venue_screen.py` for an offline blocked-source screen.

The [October 23, 2026 lab pilot readiness package](docs/LAB_PILOT_READINESS_20261023.md) adds source-backed local/Canadian test-venue leads (including historic Dalhousie Aquatron turbine experiments), one **published CAD $5,000/day Marine Institute flume list rate** and a fail-closed 15-gate physical readiness register. That rate is **not a project estimate, quotation, booking or approval**, and the site-specific FORCE data remains unusable for engineering forecasts. Run `python scripts/check_lab_pilot_readiness.py` for the currently blocked status. The laboratory venue can be qualified independently of later field ADCP site QC; **no physical test is documented or authorized**.

**No in-water device has been built or validated.** The 2018 FORCE processed campaign contains 263,250 records but **zero** source-approved turbine-inflow records. CMAR DG013 provides 531 independent wave/sensor-speed readings with gross-range QA, not a qualified 3-D rotor-height inflow profile.

The original native FORCE archive and metadata share still return server errors: four independent bounded public GET requests gave HTTP 500 in [Actions 39518864052](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39518864052). See [native archive access gate](docs/FORCE_NATIVE_ACCESS_PROBE_20261020.md). No original Nortek beams, geometry/quality masks, or approved inflow has been recovered.

The [seven-site, tidal-prototype-only Nova Scotia shortlist](docs/TIDAL_TEST_SITE_SELECTION_2026-10-20.md) and [site evidence table](research/TIDAL_TEST_SITE_SCREEN_2026-10-20.csv) separate early remote reconnaissance (Rocky Run), historical open-water precedent (Grand Passage) and extreme-load later tests (FORCE). The previous Grand Passage PLAT-I installation was decommissioned and removed in 2023: no accessible berth is proven. The October 2026 demonstration permit is for eligible grid-connected projects at least TRL 4 within designated Fundy areas; this project has not demonstrated those criteria and has no permit.

A [falsifiable load-versus-energy and three-prototype test plan](docs/LOAD_AND_PROTOTYPE_TEST_PROTOCOL_20261020.md) and [machine-readable protocol](research/experiment_protocol_v1.json) specify required synchronized phase/torque/strain/control electricity and independent ecological, manufacturing, maintenance and permit gates. [Fail-closed validation checks](scripts/check_validation_readiness.py) prevent mistaking this research plan for physical validation. Original TidalLab and SCREEN-001 simulations are unchanged.


## RM2 mean power-versus-drag sensitivity across tow speeds (processed laboratory data)

The [RM2 cross-speed research pass](docs/RM2_CROSS_SPEED_20261020.md) compares the original UNH's published processed **mean** Cp and Cd near tip-speed ratios **2.9 versus 3.1** across five nominal 0.4–1.2 m/s towing speeds and their second-sweep series (**10 source tables**, all pinned to immutable upstream Git blobs). [Reproducible selected data](research/benchmarks/RM2_CROSS_SPEED_SELECTED.csv), [frozen source-backed report](reports/RM2-CROSSSPEED-001.json), and [offline replay plus opt-in pinned-source check](scripts/rm2_cross_speed.py) show that the candidate has lower descriptive mean Cd and lower mechanical Cp throughout, but the Cp tradeoff changes strongly with tow speed. All ten source files passed independent GitHub Actions blob and value readback ([run 39522392577](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39522392577)). **This does not validate net electricity, measured structural loads, statistical significance, a controller, a field current or fatigue.** The earlier 1-m/s-only result and all historical models/reports remain unchanged.


## Updated fourteen-mechanism visual design explorer (2026-10-21)

The [TidalLab design explorer](https://jeremyhennessy.github.io/TidalTurbine/site/index.html#designs) has 14 independent, source-indexed tidal-converter **concept** illustrations, now drawn as crisp, self-contained SVG technical artwork with thumbnail browsing, per-mechanism component callouts, existing search/comparison functionality and a **Download drawing** SVG export. Nothing is a dimensioned fabrication drawing, certified hydrodynamic flow model, measured site-specific power result or validated prototype. See [artwork design and scientific disclaimers](docs/DESIGN_ARTWORK_20261021.md). The original mechanical and ocean-data research datasets and synthetic SCREEN-001 remain unchanged.
