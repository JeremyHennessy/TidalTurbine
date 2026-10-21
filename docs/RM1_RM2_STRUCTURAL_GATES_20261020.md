# Two independent lab references; mean drag is not cyclic structural loading

Research date 2026-10-20. These are **published processed laboratory quantities** and arithmetic checks, not fully validated hydrodynamic or fatigue predictions.

## RM1 axial: the published reference is now tabulated, not merely cited

Source: Hill et al. **2014** [DOE/Sandia RM1 Experimental Results](https://www.sandia.gov/app/uploads/sites/273/dlm_uploads/RM1_Experimental_Results_Report_Final.pdf), PDF index p.19 (printed p.20), Appendix A. Reproduction: `python scripts/reproduce_rm1.py` --> `reports/RM1-OBS-001.json`, source `research/benchmarks/RM1_2014_APPENDIX_A_SELECTED.csv`.

**32 points** transcribed (16 for each rotor), each with rpm, TSR, mean torque [N m], reported shaft mechanical power [W], reported Cp and upstream mean U [m/s]. Model: 1:40 twin axial rotor (one rotor diameter 0.5 m), NACA 4415 *laboratory* blades (not full-size reference NACA 63(4)-24), freshwater/open-channel facility, water depth about 1 m, hub speed about 1.05 m/s. Do **not** add the two rotor Cp numbers or compare their Cp numerically to RM2's projected D×H area. Reported thrust and Ct are all `n/a` in Appendix A.

- **Right rotor:** tabulated max Cp **0.477** at TSR **4.87** (nominal RPM 192); near TSR 5.07, Cp **0.476**. **Left rotor:** max tabulated Cp **0.412** at TSR **4.57** and **5.15**. The report's narrative and Figure 5 give approximate peaks **0.48 right and 0.43 left** near TSR ≈5.1; *left table vs narrative discrepancy remains unresolved*. Do not silently change published values.
- Check `P ≈ mean_torque × 2π × nominal_rpm / 60` with an explicitly broad gross transcription tolerance. This is not independent validation of upstream `Cp`: `mean(P)` need not equal `mean(torque)×nominal RPM`, and `mean(P/available power)` differs from `mean(P)/mean(available power)` under variable inflow. No raw synchronized torque-speed-ADV series recalculated.
- Full study uses systematic torque calibration and estimates ~3.9% combined Cp measurement uncertainty. Tests were not corrected for ~14.3% facility blockage, approach-flow asymmetry affected rotors, and a motor controlled rotational velocity. Neither thrust nor blade-root cyclic bending is independently measured here. The confusing source introduction mislabels RM1 as RM2 once; independently preserve correct turbine identity.

**Status:** `PUBLISHED_TABLE_TRANSCRIPTION_AND_NOMINAL_SHAFT_POWER_CHECK`; *not a predictive benchmark validation*. Existing [issue #3](https://github.com/JeremyHennessy/TidalTurbine/issues/3) still owns source-data reprocessing/actual rotor solver comparison.

## RM2 cross-flow: fluctuations added, with strict semantics

Source: UNH-CORE [RM2-tow-tank](https://github.com/UNH-CORE/RM2-tow-tank/blob/master/Data/Processed/Perf-1.0.csv), upstream Git blob `1f284211d5c19593cf753e63727ae62a62356439`, [processing code](https://github.com/UNH-CORE/RM2-tow-tank/blob/master/pyrm2tt/processing.py). The six-point curated source `research/benchmarks/RM2_1MS_VARIABILITY_SELECTED.csv` preserves upstream precision and CC BY 4.0 attribution. Reproduce `python scripts/rm2_variability.py` --> `reports/RM2-VARIABILITY-001.json`.

Under nominal 1 m/s tow, operating **run 10** at TSR~2.90 relative to source **run 12** TSR~3.10:

| Published processed statistic | Run 12 baseline | Run 10 candidate | Relative change |
| --- | ---: | ---: | ---: |
| Mean Cp | 0.35460 | 0.34805 | −1.85% |
| Mean Cd | 0.84587 | 0.79930 | −5.51% |
| Std of instantaneous Cp | 0.12906 | 0.12419 | −3.77% |
| Std of instantaneous Cd | 0.16845 | 0.16009 | −4.97% |
| Std of *per-revolution mean* Cp | 0.004966 | 0.002595 | −47.76% |
| Std of *per-revolution mean* Cd | 0.005041 | 0.003271 | −35.12% |

**Crucial:** upstream `calc_perf_per_rev` takes each revolution's **mean** derived Cp/Cd and then computes standard deviation across revolutions (only 9–10 complete revolutions for these conditions). This is **not within-revolution torque ripple, phase-resolved blade load, support-strut alternating moment, blade-root stress or fatigue damage**. `std_cp` and `std_cd` are instantaneous coefficient spread over a tow, but likewise do not independently measure the frequency-domain stress spectrum. Differences cannot be declared statistically meaningful without repeated matched replicates and covariance analysis. The six runs are a source-data subset, *not* new experiments or a validated turbine control optimization.

**Next load experiment (issue #4):** preregister operating-point pair, acquire synchronous raw torque and rotor phase + blade-root strain/bending + hydrodynamic inflow/turbulence for matched tests, compute mechanical work, actuator consumption, stress-cycle counting, material S-N fatigue sensitivity with uncertainties and common baseline. Separate high-cycle from low-cycle and extreme loads; do not make up fatigue rates. Only then can test if modest mechanical energy loss yields lifetime benefit.


## Subsequent observation: one-speed RM2 drag tradeoff is not constant across the tested tow-speed series

The later [RM2-CROSSSPEED-001](RM2_CROSS_SPEED_20261020.md) report is an independent source-verified **processed-means** check of ten original UNH performance sweeps: speeds 0.4, 0.6, 0.8, 1.0 and 1.2 m/s, each first and second (`-b`) curve. At the same **fixed nominal TSR 2.9 versus 3.1** source runs, all ten mean Cd point estimates fall, but mean Cp loss is roughly **29% at 0.4 m/s, 14% at 0.6 m/s, 6–9% at 0.8 m/s, around 2% at 1.0 m/s and approximately 0.1–1.2% at 1.2 m/s**. Exact source coefficient tables, local maxima, upstream uncertainty fields and original full-file Git blob hashes are retained in the reported fixture and verified by [GitHub Actions 39522392577](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39522392577).

This limits the interpretation of the earlier 1-m/s illustrative derating. Source run 12 is **not universally each sweep's maximum Cp**, and the second curves do not constitute ten independent turbines or statistically proven paired benefit. Larger relative losses at low speed reinforce the need for a **measured, matched multi-speed controller/loads experiment**, not changing the old data, adjusting the SCREEN-001 electrical export cap, or claiming fatigue/durability. Measured cyclic blade-root stress and actuator/net electrical energy remain unacquired.
