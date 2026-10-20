# RM2-TRADEOFF-001 — measured laboratory operating-point tradeoff

**Classification:** descriptive comparison of *published processed experimental means*; **NOT** calibrated rotor-control simulation, predictive hydrodynamics, validated structural-load reduction or lifetime-energy improvement. Review date: 2026-10-20.

**Question:** For the **same** RM2 1:6 cross-flow turbine at nominal 1.0 m/s tow speed, do operating points with lower mean mechanical power coefficient also exhibit lower *mean streamwise drag coefficient*? This is an investigation of whether load-aware operation is worth instrumenting, not a claim that electrical curtailment reduces loads.

**Source and study:** Bachant et al. (2016), *Experimental Study of a Reference Model Vertical-Axis Cross-Flow Turbine*, PLOS ONE, [DOI:10.1371/journal.pone.0163799](https://doi.org/10.1371/journal.pone.0163799), sections **Uncertainty Analysis**, **Data Processing**, **Performance**, **Strut drag losses**, Figures 6–11. Original dataset [UNH-CORE/RM2-tow-tank](https://github.com/UNH-CORE/RM2-tow-tank), `Data/Processed/Perf-1.0.csv`, Git blob `1f284211d5c19593cf753e63727ae62a62356439`; curated seven-decimal fixture `research/benchmarks/RM2_PERF_1MS_REDUCED.csv` and its SHA-256 in the JSON report. The paper describes 95% expanded uncertainty intervals and notes an **uncorrected ~10% test-section blockage**, Reynolds-number sensitivity and force resonance at some operating points. The paper's overall maximum **Cp 0.37** applies to a different higher-Re condition, and is not contradictory with the **Cp 0.3546025** peak of the specific nominal 1.0 m/s subset reviewed here.

**Geometry and denominators:** RM2 diameter 1.075 m, height 0.8067 m, frontal area **D×H = 0.8672025 m²**. Freshwater nominal density 1000 kg/m³ and uniform reference U = 1 m/s are source-study normalizations. To clarify dimensions only, `P_mech,ref = ½ ρ A U³ Cp` [W] and `F_mean,ref = ½ ρ A U² Cd` [N]. The nominal W and N below are *coefficient reconstructions*, not extra independent instrument measurements. Each real towing run has a slightly different recorded actual inflow. The coefficient values and uncertainties remain authoritative; no Ocean/Fundy extrapolation is performed.

## Results — fixed descriptive thresholds chosen during this review (not preregistered)

| Rule for minimum fraction of recorded peak Cp | Selected run / measured TSR | Cp | Cd | Mean-Cp loss vs peak | Mean-Cd reduction vs peak |
|---|---|---|---|---|---|
| Baseline observed peak | 12 / 3.0993495 | 0.3546025 | 0.8458717 | — | — |
| ≥90% of peak Cp | 9 / 2.7995145 | 0.3294381 | 0.7682874 | 7.0965% | 9.1721% |
| ≥95% of peak Cp | 10 / 2.8999618 | 0.3480504 | 0.7992956 | 1.8477% | 5.5063% |
| ≥98% of peak Cp | 10 / 2.8999618 | 0.3480504 | 0.7992956 | 1.8477% | 5.5063% |
| ≥99% of peak Cp | 11 / 2.9996617 | 0.3520155 | 0.8221283 | 0.7295% | 2.8070% |

At the nominal 1 m/s reference condition, baseline corresponds to approx. **153.76 W reconstructed mechanical rotor power** and **366.77 N reconstructed mean drag**. These are *not* net grid output, useful lifetime energy, blade bending moments, fatigue loads, or annual field power. All 23 run points (not the entire experiment) were considered, and the observed point-estimate Pareto set is recorded in `reports/RM2-TRADEOFF-001.json`.

**Uncertainty and caution:** Upstream `exp_unc_cp`/`exp_unc_cd` fields were preserved; no covariance-aware comparison, uncertainty on differences, matched turbine structural measurements or replication under turbulence has been established. A lower mean *rotor drag* does not guarantee lower unsteady loads, bearing forces, rotor torque ripple, fatigue, cost, or fish risk. Measured Cp and Cd were conditioned on a speed-controlled tow rig; an actual generator's torque controller and parasitic power could change the operating point. The paper warns about support strut drag and Reynolds effects. This cannot be used to rank axial turbines, helical screws, foils or kites on a universal Cp basis.

**Decision supported:** Advance [loads and pitch/control issue #4](https://github.com/JeremyHennessy/TidalTurbine/issues/4) with a **same-device, same-inflow, simultaneous measurements of mechanical power, mean rotor drag, azimuth-resolved bending moment, torque ripple, controller consumption and uncertainty**. It is worth testing whether reduced mean drag is accompanied by reduced damaging *cyclic* loads. Until such a test exists, H-001/H-006 lifetime benefit is **unresolved**, not supported.

**Replay:** `python scripts/rm2_operating_points.py` (uses the *unchanged* curated primary-source fixture); `python -m unittest discover -s tests -v`. Reproduction checks only processed published means. Never overwrite `RM2-OBS-001` or historical `SCREEN-001` to force a changed conclusion.
