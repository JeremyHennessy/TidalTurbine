# Coverage and evidence-gap matrix — 2026-10-20

`Reviewed` means documented relevant sections examined; `Partial` means metadata or limited sections reviewed; `Missing` means not acquired or not evaluated. Coverage is progressive, not a claim to 'all papers.' See `catalogue.json` for exact depth and citations.

| Topic | Coverage | Current evidence / next needed |
|---|---|---|
| Architecture families | Partial | 14 multidimensional exemplars in `mechanisms.json`, covering axial, cross-flow, drag, foil, free-stream axial screw, kite, duct, pressure-coupled, piezoelectric flag, vortex oscillator; independent normalization and field measurements missing. |
| RM1 geometry and test | Partial | Sandia index/report uncertainty sections; dataset & Cp curve reproduction MISSING. |
| Current and bathymetric resource | Partial (acquisition only) | One 2-hour FORCE ADCP 2018 slice **acquired and numerically screened**, not quality-approved. 206/450 exact-zero triples and unknown transducer geometry block model ingestion. No usable annual resource or bathymetric assessment. See `reports/FORCE-SLICE-QA-001.md`. |
| Turbulence, shear, wave-current interaction | Missing | Need measured spectra and calibrated hydrodynamics. |
| Rotor Cp/TSR / thrust Ct | Partial | RM2 cross-flow processed tow-tank 23-run Cp/CD-v-TSR series reproduced in `RM2-OBS-001`; independently recomputed rotor torque, a predictive cross-flow solver and RM1 axial-rotor curves still MISSING. |
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

**Priority order:** reproduce RM1 axial experimental quantity + independently challenge RM2 predictive modelling > real FORCE ADCP acquisition/QC > measured load/control and access windows > site/environment gates > data-centre dispatch integration. No single mechanism is the approved winner. Do not declare design improvements ahead of physical evidence.

## Ocean-data registry 2026-10-20 (second pass)

20 structured **source-discovery records** in `research/ocean_datasets.json`, with unique IDs, source and access links, provenance, variable/unit metadata, source/metadata review status, datum and QC gaps, reuse terms and exact next action. Two entries represent the same 2018 FORCE current campaign through distinct metadata/file URLs and must not be counted as independent measurements. A short FORCE 2018 observation slice has been downloaded to a temporary Actions artifact and checked outside Git (**450 records; 206 all-zero triples**); it has **not** been quality approved or ingested into the simulator. Next priority is resolving the suspected mask/fill and obtaining a defensible time/depth profile alongside RM1 benchmarking. See `docs/OCEAN_DATA.md`. The catalogue does not exhaust regional records or include all 2026 deployments.

## Broader mechanism audit (third pass; 2026-10-20)

- **Reviewed primary processed experimental data:** UNH-CORE RM2 1:6 cross-flow tow-tank `Perf-1.0.csv` (23 data points, published `mean_cp`, `mean_cd`, `mean_tsr` and uncertainty fields). See `reports/RM2-OBS-001.md`; this is measured *processed experimental data reproduction*, not hydrodynamic model validation. Raw signals/10GB reprocessing remain missing.
- **Limited primary / institutional:** EMEC device-family explanations; EMEC Flumill and OpenHydro historic test reports; Sandia RM1 public metadata/report index (quantitative reproduction missing); published abstract-only Allen/Smits piezoelectric flag (electrical output, load and fatigue unverified).
- **Manufacturer/engineering-partner reports only:** Spiralis/Cape Horn axial skelter partial field point and CFD; Minesto Dragon rated power and recovery. Neither proves grid-scale mean energy, life, fish safety, net costs, fair aerodynamic comparison or availability.
- **Concepts with no independently ingested performance curves:** helical Gorlov geometry, Savonius, pressure-coupled secondary air, Venturi augmentation, direct-drive foil, piezoelectric flag, VIV; these remain **mechanism discovery and modelling eligibility**, not performance-zero entries or rejected architectures.
- **Claim audit:** 14 statements recorded in `research/CLAIM_AUDIT.csv`, including 'bladeless', 'fish safe', 'one moving part', 'much cheaper', 'recyclable', 'continuous power', awards, Venturi energy conservation and exposure/cumulative effects.
- **FORCE acquisition:** `qa_force_slice.py` and synthetic fixture tests exist, but measured current source slice **acquired** later via GitHub probe; **scientific QA-passed: 0** due unknown quality and 206/450 zero triples; see `docs/FORCE_QA_GATE.md`.

**Priority exclusion:** Numerical Cp comparisons across different denominators, including foil swept envelope, duct inlet and rotor disk, transverse frontal area and kite trajectory, are **not valid rankings** without a matched control-volume and duty/parasite accounting. Avoid arbitrarily weighted maturity/performance scores.

## Evidence-based operating-point experiment — RM2-TRADEOFF-001 (2026-10-20)

Observed *processed* 1:6 laboratory cross-flow Cp/Cd operating points now support a same-rig descriptive mean-drag tradeoff (`reports/RM2-TRADEOFF-001.md`). It shows loss of mechanical Cp alongside lower mean Cd when changing measured TSR, but **no cyclic bending/torque, fatigue, environmental, control-power, or lifetime evidence**. Do not use to rank different energy-harvesting mechanisms. Full source paper inspected through Uncertainty, Processing, Performance and Strut losses sections; existing source ID `RM2-DATA-001` retained, no artificial new bibliography count.
