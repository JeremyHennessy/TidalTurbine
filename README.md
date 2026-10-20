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

## Measured cross-flow operating-point research

[RM2-TRADEOFF-001](reports/RM2-TRADEOFF-001.md) compares **published laboratory processed means** of Cp and streamwise Cd at different tip-speed ratios on the same 1:6 cross-flow rotor and nominal inflow. It identifies an experimentally observed *mean* power-versus-drag tradeoff; cyclic loads, controller energy, fatigue, lifetime economics and field validity remain untested. Replay with `python scripts/rm2_operating_points.py`.
