# TidalTurbine

Evidence-led tidal-stream turbine research and reproducible engineering screening, with special attention to Nova Scotia and the Bay of Fundy.

**Status (2026-10-20): research prototype, not a validated turbine design.** No measured site current, structural loads, fatigue life, device reliability, ecological safety, or cost claims are established by this repository.

## Research objective

Compare established tidal-stream architectures and test falsifiable improvements in lifetime electricity delivered, serviceability, environmental performance and lifecycle economics. Do not assume floating/recoverable/modular is superior. Tidal stream is intermittent at slack water and cannot alone serve continuous electrical demand.

## Quick start

Python 3.10+ (standard library only):

```sh
python -m unittest discover -s tests -v
python -m tidal_screen.cli --config configs/synthetic_screen.json --out reports/latest.json
python scripts/check_catalogue.py
```

The first screen uses **synthetic** signed currents and a constant power coefficient. Electrical curtailment does **not** imply lower thrust or fatigue. Scripts, tests, and configurations are added in the foundation research branch; until merged, run these commands there.

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
