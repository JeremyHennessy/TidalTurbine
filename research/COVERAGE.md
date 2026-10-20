# Coverage and evidence-gap matrix — 2026-10-20

`Reviewed` means documented relevant sections examined; `Partial` means metadata or limited sections reviewed; `Missing` means not acquired or not evaluated. Coverage is progressive, not a claim to 'all papers.' See `catalogue.json` for exact depth and citations.

| Topic | Coverage | Current evidence / next needed |
|---|---|---|
| Architecture families | Partial | Sandia index; RealTide sec 7; manufacturer pages; physical comparison missing. |
| RM1 geometry and test | Partial | Sandia index/report uncertainty sections; dataset & Cp curve reproduction MISSING. |
| Current and bathymetric resource | Missing | No georeferenced licensed ADCP/bathymetry ingested. |
| Turbulence, shear, wave-current interaction | Missing | Need measured spectra and calibrated hydrodynamics. |
| Rotor Cp/TSR / thrust Ct | Partial | General experimental methodology, not replicated/model-calibrated. |
| Cavitation / tip vortex / debris | Missing | Site-specific pressure, blade surface and impacts. |
| Cyclic loading, structural fatigue | Partial | Passive-pitch model test reviewed; S-N data and load spectrum missing. |
| Blade materials/manufacturing | Missing | Qualified laminates, environmental aging, supply and inspection. |
| Bearings and seals | Partial | RealTide generic FMEA; failure distributions missing. |
| Corrosion / biofouling | Missing | Site-specific inspection and materials. |
| Geared versus direct-drive | Partial | Nova CORDIS project self-report; neutral comparative lifecycle missing. |
| Fixed/active/passive blade pitch | Partial | Gambuzza model-scale test reviewed; full-size validation absent. |
| Floating recoverable platforms | Partial | Orbital description and RealTide generic FMEA; wave-load model missing. |
| Moorings / foundations / export cables | Partial | RealTide taxonomy and hypothesized failures; metocean/access records missing. |
| Array interactions and wake losses | Missing | Independent array measurement and cable-redundancy work. |
| Power electronics and converter reliability | Partial | RealTide electrical ranking; empirical reliability missing. |
| Maintenance/weather windows | Missing | Measured MTTR/incident and vessel availability. |
| Reliability statistics and lifetime energy | Missing | No trustworthy component distributions. |
| Lifecycle capital, OPEX, decommission | Partial | Sandia cost methodology index; no costs extracted/validated. |
| Nova Scotia policy / project status | Reviewed | Province and FORCE pages incl 2026 program; deployment facts require refresh. |
| Fish monitoring / marine ecology | Reviewed | DFO full online guide; OES metadata only; quantified collision risk missing. |
| Mi'kmaq participation and interests | Partial | CMM/FORCE study landing reviewed; project-specific engagement not complete. |
| Marine users, navigation, fishing | Missing | Local spatial use and consent/license analysis. |
| DNV-ST-0164 certification | Partial | Public metadata only; paid full text not reviewed. |
| QBlade capabilities / licensing | Partial | MHK tutorial and APL license FAQ; no benchmark trial. |
| Seawater cooled AI centre integration | Missing | Separate roadmap only, no dispatch or cooling simulation. |

**Priority order:** measured RM1 benchmark > load/control validation > downtime/lifecycle model > NS resource+environment qualification > data-centre integration. Do not declare design improvements ahead of physical evidence.

## Ocean-data registry 2026-10-20 (second pass)

20 structured **source-discovery records** in `research/ocean_datasets.json`, with unique IDs, source and access links, provenance, variable/unit metadata, source/metadata review status, datum and QC gaps, reuse terms and exact next action. Two entries represent the same 2018 FORCE current campaign through distinct metadata/file URLs and must not be counted as independent measurements. Measured ocean time-series ingested into the repo or simulator: **zero**. First priority is acquisition and QA of FORCE 2018 ADCP, followed by published RM1 benchmarking. See `docs/OCEAN_DATA.md`. The catalogue does not exhaust regional records or include all 2026 deployments.
