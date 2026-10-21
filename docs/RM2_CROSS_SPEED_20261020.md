# RM2-CROSSSPEED-001 — does the published mechanical Cp / mean Cd tradeoff generalize across tow speeds?

**Research date: 20 October 2026 (Atlantic local). Status: additional source-derived processed-laboratory observations, NOT measured blade loads, fatigue or site-energy validation.**

## New question and fixed comparison

The earlier `RM2-TRADEOFF-001` documented 1 m/s means for a 1:6 cross-flow RM2 rotor. Here we **do not optimize or compare unlike turbine designs**. Instead, independently inspect all five published nominal tow speeds (0.4, 0.6, 0.8, 1.0, 1.2 m/s), first performance curve `Perf-N.csv` and second curve `Perf-N-b.csv`, 10 series total. For every series, compare the existing **nominal TSR 2.9 (source run 10)** against **nominal TSR 3.1 (source run 12)**. Their actual processed mean TSRs are near these values; source uncertainty fields are kept unchanged. Separately identify the **post-hoc maximum reported Cp point** from each full source file. In slower series that maximum lies at higher TSR, so do **not** call TSR 3.1 a universal peak.

Source: Bachant, Wosnik, Gunawan & Neary, [UNH RM2 tow-tank experiments](https://github.com/UNH-CORE/RM2-tow-tank), data [CC BY 4.0, DOI: 10.6084/m9.figshare.1373899](https://doi.org/10.6084/m9.figshare.1373899). Frozen upstream Git commit **`fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef`**. Reduced `research/benchmarks/RM2_CROSS_SPEED_SELECTED.csv` transcribes **three already processed published source rows per speed/sweep** (30 selections; may include repeated same run when Cp peak equals TSR 3.1), and pins the individual original source Git blob SHA and actual source row count. No 10 GB raw dataset, raw time-series processing or new experiment claimed. Source files contain both full parameter sweeps and previously processed means/uncertainty fields, not synchronized blade-root strain.

**Formula (descriptive point estimate only)**: percent decrease = `100 × (1 - mean_coefficient_at_TSR_2.9 / mean_coefficient_at_TSR_3.1)`. This compares Cp only with Cp, Cd only with Cd, under one tow-speed/sweep; it is **not** Cp divided by Cd, a load-versus-energy universal objective, confidence interval, net electrical power, a damage metric, or a normalized cross-device ranking.

## Processed published results — same rig, within each nominal speed/sweep

| Nominal tow speed | Sweep A: Cp decrease | Sweep A: Cd decrease | Sweep B: Cp decrease | Sweep B: Cd decrease |
|---|---:|---:|---:|---:|
| 0.4 m/s | 29.86% | 7.70% | 28.53% | 8.14% |
| 0.6 m/s | 13.76% | 7.55% | 13.55% | 7.09% |
| 0.8 m/s | 8.99% | 7.21% | 6.46% | 5.72% |
| 1.0 m/s | 1.85% | 5.51% | 2.32% | 5.42% |
| 1.2 m/s | 1.16% | 5.13% | 0.13% | 6.42% |

Every one of the ten processed *point estimate* comparisons gives **lower mean Cd** at 2.9 TSR, with a mean Cd decrease of roughly **5–8%**. But the mechanical **Cp penalty changes strongly with tow speed**: approximately **29% at 0.4 m/s, 14% at 0.6, 6–9% at 0.8, 2% at 1.0 and up to about 1% at 1.2**. This pattern is present across the two labeled sweeps (A and B), but **these are not ten independently selected turbines or a statistically powered study**. At low speeds the published Cp uncertainty fields are large relative to some differences. We have not estimated paired covariance, significance, scale laws, corrected Reynolds/blockage effects or lifetime energy.

The 1 m/s example (−1.85% mean Cp, −5.51% mean Cd) is therefore **not a reliable universal law that sacrificing little mechanical power always reduces drag across operating speeds**. A lower mean Cd in any sweep is not proof of lower peak bending, within-revolution stress-cycle amplitudes, accumulated fatigue, controller electricity, marine safety, availability or cost.

## Reproducibility and hard scientific gates

```sh
python scripts/rm2_cross_speed.py --check
python -m unittest discover -s tests -p 'test_rm2_cross_speed.py' -v
# Optional explicit network/source replay:
python scripts/rm2_cross_speed.py --verify-upstream --check
```

Default operation is **offline and source-fixture-only**; source replay is opt-in, reads **only ten pinned source-processed CSVs**, verifies each full original file's Git blob SHA and row count, 2.9/3.1 raw value strings and the series Cp-maximum record; no raw 10 GB records are requested or stored. `reports/RM2-CROSSSPEED-001.json` and its source hash establish exact numeric provenance. Existing 1 m/s `RM2-OBS-001`, `RM2-TRADEOFF-001`, `RM2-VARIABILITY-001`, the synthetic `SCREEN-001` and full FORCE/CMAR quality blockers remain unchanged.

**Next falsifier:** preregister selected operating states *and multiple mean speeds/turbulence conditions*, then measure rotor phase, torque, net delivered electricity and all actuator draw synchronously with blade/strut strain, peak loads and fatigue-relevant cycle spectra. Select common time/volume boundary and failure/uncertainty acceptance gates. The existing prospective 0.6/1.0/1.4 m/s bidirectional *tank setpoints* are assumptions, **not evidence of any achievable Nova Scotia site inflow**. Until actual controls and structural histories exist, maintain `NO_HARDWARE_WINNER`, `NO_FATIGUE_CLAIM`, `NO_SITE_ENERGY` and `ZERO_QUALIFIED_SITE_INFLOW`.
