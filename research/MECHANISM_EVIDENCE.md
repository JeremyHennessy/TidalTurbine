# Tidal-stream conversion mechanisms — comparative evidence gate (2026-10-20)

**Do not rank or declare a winner.** Canonical machine-readable design dimensions, one row per *configuration example*, are in [`mechanisms.json`](mechanisms.json). Technologies are combinations across independent axes; support, gearbox, blade pitch and diffuser are **not** separate primary mechanisms. The 14 rows do not assert that the space is exhausted. Cross-cutting support and control variants may be combined without multiplying the count of fundamental mechanisms.

## Classification and the correct comparison boundary

| Primary mechanism | Motion / harvesting | Suitable denominator | Verified status at this pass | Important unknown |
|---|---|---|---|---|
| Axial lifting rotor (open, annular, counter-rotating) | axial rotation; pitch fixed/active/passive | flow disk; annular area and count of rotors specified | Sandia RM1 public dual-axial laboratory report identified; **curve not reproduced** | source raw measurements, thrust, controller and fatigue |
| Cross-flow lifting rotor (Darrieus/H-rotor) | transverse rotating blades; shaft vertical or horizontal | projected diameter × rotor height (RM2) | **23 published processed RM2 tow-tank Cp/CD rows reproduced**; not a predictive model | loads, torque ripple, independently calculated Cp, tidal environment |
| Helical cross-flow (Gorlov blade geometry) | transverse shaft rotation with helically twisted blades | projected frontal area | mechanism described; no independently ingested curve | actual comparative torque ripple, manufacture, wet lifetime |
| Savonius / drag rotor | transverse shaft rotation of drag cups | projected frontal area | taxonomy only | net output, drag and material longevity |
| Oscillating foil, active/passive | heave plus pitch, may drive hydraulic/linear PTO | foil span × travel stroke (definition explicit) | force×velocity + moment×angular-rate balance implemented, **not calibrated** | force/moment history, controls and actuator power |
| Free-stream helical *axial screw* | helical screw surface parallel to current rotates shaft | full interception envelope, pressure/volume flux if confinement | EMEC's Flumill history; Spiralis engineering-partner 2.50kW point at 21 RPM **self-reported** | inflow, net electrical boundary, full curve, fatigue, environmental effects |
| Kite with onboard axial rotor | tethered cross-current flight and onboard rotor | instantaneous onboard rotor area and relative flow **plus flight envelope** | Minesto developer reports grid generation and eventual retrieval | tether/cable power losses, annual yield, controller reliability and environment |
| Ducted rotor | pressure change and speed-up through duct + rotor | *both* duct inlet and rotor swept areas; hydrodynamic capture area | class established, no independent curve acquired | blockage / expansion losses, fair denominator, cavitation, ecology |
| Secondary pressure-coupled water/air | differential pressure powers separate air or hydraulic PTO | total control-volume energy flux; pressure × volumetric flow | EMEC education describes mechanism, performance unverified | losses, vent/pump loads, whole-boundary accounting |
| Flexible piezoelectric flag/eel | repeated vortex-induced bending creates charge | physical wake/capture corridor and device-specific electrical load | Allen & Smits 2001 peer-reviewed abstract located; full text / numerical electrical data unavailable | waterproof electronics, measured µW/W scale, fatigue and LCA |
| Vortex-induced oscillator | cross-current mechanical oscillation | projected wake interference region + tested cylinder/oscillator geometry | candidate in discovery queue; test data missing | conversion damping, structural fatigue, ecology |

Power coefficients from different rows are **not** comparable without common energy accounting, flow blockage, area definition, scaling and test uncertainty. Report mechanical rotor power and net grid-exported electrical energy separately. Unknown ≠ zero. Report any adverse ecological outcomes and access failures rather than treating silence as safety.

## Evidence audit — what changed this pass

- [UNH-CORE RM2 processed data](https://github.com/UNH-CORE/RM2-tow-tank): 1:6 scale H-rotor, freshwater laboratory tow tank, 1.075 m diameter, 0.8067 m height. The upstream processed `Perf-1.0.csv` contains 23 nominal-1.0-m/s runs. Peak observation of its preprocessed `mean_cp` is 0.3546025 at `mean_tsr` 3.0993495 (as transcribed to seven decimals). `exp_unc_cp` field at that point is 0.0080504; interpretation/coverage is **not independently revalidated**. No raw torque, tare adjustment or electrical output reproduced. Reproduction: `python scripts/reproduce_rm2.py`; report `reports/RM2-OBS-001.json`. Source Git blob SHA `1f284211d5c19593cf753e63727ae62a62356439`. Bachant, Wosnik, Gunawan and Neary, 2016, CC BY 4.0, doi:10.6084/m9.figshare.1373899.
- [Sandia RM1 experimental report](https://www.sandia.gov/app/uploads/sites/273/dlm_uploads/RM1_Experimental_Results_Report_Final.pdf) is specifically a **different** 1:40 dual-rotor axial laboratory reference; its Cp-vs-TSR curve still awaits source-data digitization with uncertainty. A Sandia page describing 'RM1 (RM2)' is internally inconsistent; do not propagate that mislabel.
- [Spiralis/Cape Horn Engineering](https://www.cape-horn-eng.com/cfd-analysis-tidal-energy-structure-spiralis-energy/) (2024-08-21) reports a Poole Harbour quarter-scale 6 m Axial Skelter 2.50 kW physical point vs 2.59 kW CFD at 21 rpm. This is a **developer/engineering-partner** account of one condition, not independent repeated Cp, electrical yield, fish-impact or lifecycle validation. Helical axial screw is not a Gorlov transverse helical blade.
- [EMEC OpenHydro retrospective](https://www.emec.org.uk/about-us/our-tidal-clients/open-hydro/) records a 250 kW-rated 6 m open-centre trial, over 10,000 running hours for a seventh-generation unit, 2018 liquidation and 2024 platform decommissioning. Past use is not audited MTBF, availability or lifetime economics. This history is retained because discontinued technology is important negative context.
- [EMEC Flumill history](https://www.emec.org.uk/about-us/our-tidal-clients/flumill/): first non-grid Shapinsay test in 2011, solid screw geometry; **no field electrical performance measurement reviewed**.
- [Minesto March 2026 report](https://www.minesto.com/news/project-update-on-minesto-dragons-in-the-faroe-islands-microgrid-scale-powerplant-dragon-4-in-electricity-production/) describes Dragon 4 (100 kW nameplate) grid operation and Dragon 12 (1.2 MW nameplate) recovery after ten months. **Project-reported**, not an audited denominator-comparable annual plant factor.
- [Allen & Smits 2001](https://doi.org/10.1006/jfls.2000.0355): bluff-body wake excites a flexible piezoelectric membrane. Only institutional abstract/publication metadata examined here; no measured energy/output or durability asserted.
- [EMEC tidal-device types](https://www.emec.org.uk/marine-energy/tidal-devices/) distinguishes oscillating hydrofoils, ducted devices and pressure-driven secondary air turbines; descriptions are **not** measurements or endorsement.

## Dedicated applications — avoid false equivalence

**Near-term grid-scale:** devices with operating grid-connected demonstrations warrant site-specific resource, cost, environmental and maintenance assessment; vendor nameplate is not audited annual energy.

**Experimental grid-scale:** hydrodynamic-lift cross-flow, oscillating foils, ducted and screw designs require matching test boundaries/uncertainty before plant-level projections.

**Instrumentation:** piezoelectric eels/membranes, vortex/vibration and very small rotors could be investigated as **sensor power** if measured microwatt/milliwatt/continuous mean electrical loads permit; don't extrapolate to MW or label unmeasured power scale as proven.

**Data centres:** separate dispatch/storage/grid and cooling constraints; tidal slack/maintenance do not disappear. Don't use a generic turbine Cp plot as a continuous-data-centre electricity forecast.

## Discovery and stop/defer queue

- Confirm independent peer-reviewed flexible flag/VIV measured net electrical output and fatigue life (currently metadata-only).
- Resolve free-stream helical screw tests and source files; defer quantitative ranking until full upstream power boundary and repeated data exist.
- Independently reproduce RM1 axial benchmark; follow existing issue #3.
- Review active/passive foil dynamics with net actuator/PTO measurements before any numerical turbine prediction.
- Treat barrage/lagoons (tidal **head**), waves, OTEC and salinity-gradient as **adjacent categories**, not tidal-stream measurements.

## Newly inspected primary-paper detail and what it changes (2026-10-20)

Bachant et al. (2016), [PLOS ONE full paper](https://doi.org/10.1371/journal.pone.0163799), sections **Uncertainty Analysis**, **Data Processing**, **Performance**, **Strut drag losses**, Figures 6–11: 1:6 RM2 cross-flow reference, tow-tank area `D*H`, nominal freshwater density, uncorrected ~10% test-section blockage, physical Reynolds-number sensitivity and significant support-strut drag losses. The processed 1.0 m/s subset previously reproduced as `RM2-OBS-001` is now analyzed for a **within-the-same-rig mean Cp–Cd tradeoff** as `RM2-TRADEOFF-001` rather than pretending a new rotor geometry is superior. The paper reports a **different** overall max Cp≈0.37 at higher Reynolds number; the subset peak is ≈0.35460. An observed mean Cd reduction at lower TSR is not a blade-bending/fatigue result. Source uncertainty is preserved; no statistical significance on differences or life forecast is claimed. This evidence motivates issue #4 to measure loads and parasitic rotor support effects, not to approve an optimized design.
