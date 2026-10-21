# Coverage and evidence-gap matrix — 2026-10-20

`Reviewed` means documented relevant sections examined; `Partial` means metadata or limited sections reviewed; `Missing` means not acquired or not evaluated. Coverage is progressive, not a claim to 'all papers.' See `catalogue.json` for exact depth and citations.

| Topic | Coverage | Current evidence / next needed |
|---|---|---|
| Architecture families | Partial | 14 multidimensional exemplars in `mechanisms.json`, covering axial, cross-flow, drag, foil, free-stream axial screw, kite, duct, pressure-coupled, piezoelectric flag, vortex oscillator; independent normalization and field measurements missing. |
| RM1 geometry and test | Partial | Sandia RM1 Appendix A right/left 16-point Cp/TSR printed tables reproduced (RM1-OBS-001); raw signal, Ct/thrust and predictive-physics validation MISSING. |
| Current and bathymetric resource | Partial (acquisition only) | Complete 5,265-burst FORCE current/wave processed files SHA-verified, with 263,250 cell records and quality-state classification; 97,911 exact-zero triplets and unverified beam QC/geometry BLOCK turbine inflow. Independent CMAR DG013 has 531 sensor observations but no rotor-depth 3-D inflow. See `docs/INGESTION_GATE_20261020.md`. |
| Turbulence, shear, wave-current interaction | Missing | Need measured spectra and calibrated hydrodynamics. |
| Rotor Cp/TSR / thrust Ct | Partial | RM2 23 processed Cp/Cd/TSR observations and RM1 32 printed Cp/TSR observations reproduced (data reproduction only); independently calibrated load spectra, thrust/Ct and predictive solver validation MISSING. |
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

## New validation study — 2026-10-20: not a design selection

- **RM1 axial published quantities:** inspected Sandia original printed Appendix A, 16 tabulated operating points per rotor; `RM1-OBS-001` transcribes Cp/TSR and checks nominal shaft-power consistency. This is **source-table reproduction**, not independent predictive rotor or fatigue validation. Left max Cp 0.412 in table versus 0.43 approximate in narrative remains a recorded conflict.
- **RM2 cross-flow cyclic proxy:** six additional published processed points (`RM2-VARIABILITY-001`) reproduce instantaneous coefficient spread and across-revolution *mean* spread; **neither is blade fatigue or blade-root cyclic loading**. No causal lifetime claim.
- **FORCE instrument:** publisher-identified upward-looking FAST3 Nortek Signature 500 and 5-min/15-min acquisition, upper 10% surface interference exclusion used in source analyses; exact per-cell quality and height unresolved. One-time **72-hour acquisition/NUMERICAL QA requested**, not scientific qualification until source artifact checked and native masks/geometry obtained.
- **Three prototype candidates:** axial rotor, cross-flow rotor, nonrotating oscillating foil; explicit nonnumeric, independent hydrodynamic, net power, structural, environmental, manufacture and access gates. No winner, not a common-Cp fit. See `research/prototype_gates.json`.

## Subsequent 72-hour FORCE QC + sensor primary-source correction (2026-10-20)

- **Acquired**: 14,400 archived FORCE 2018 processed current vectors across 288 timestamps; raw 72-hour SHA256 pinned in `reports/FORCE-72H-QA-001.json`, source retained outside Git in one-shot Actions artifact. 5,160 exact all-zero vectors, 12 all-zero and 12 partial-zero range bins; 26 all-nonzero bins remain **numeric candidates only**, not physically quality-qualified. Pressure/highest-nonzero-boundary Pearson r≈0.996882 (descriptive).
- **Instrument geometry partially recovered**: Viehman et al. 2022 confirms Nortek transducer face at 0.7m above seabed, blanking 1m, first sample centre 2m from face, but public ERDDAP starts range labels 1.5m. Cell label/geometry mismatch and native acoustic quality masks unresolved.
- **Still missing before site energy**: raw beam correlation/amplitude and converter flags, calibrated depth/time mask, seasonal/annual representative vector coverage, instrumentation uncertainty, loads, fisheries/permission gates. No FORCE measured velocities fed to turbine models.

## Current audit supersession — 2026-10-20

Historical paragraphs above describing **20 source records**, a **two-hour-only** FORCE acquisition, or RM1 as not reproduced refer to earlier checkpoints. They are superseded by the 21-entry source registry, complete FORCE processed 2018 and CMAR DG013 acquisition, and RM1-OBS-001. Preserve them as research chronology, not present status. See `docs/INGESTION_GATE_20261020.md` and `docs/FORCE_NATIVE_QC_RECOVERY_20261020.md`. The dataset's 56-day × 50-cell QA grid is arithmetic screening **only**. The paired load/electricity protocol remains measurement blocked.
