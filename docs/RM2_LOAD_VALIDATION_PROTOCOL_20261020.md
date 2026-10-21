# Measurement analyzer supplement to TT-EXPERIMENT-V1: does a small energy sacrifice reduce damaging loads?

**Authoritative prospective test specification:** [research/experiment_protocol_v1.json](../research/experiment_protocol_v1.json) and [docs/LOAD_AND_PROTOTYPE_TEST_PROTOCOL_20261020.md](LOAD_AND_PROTOTYPE_TEST_PROTOCOL_20261020.md), merged in PR #19. This note is an implementation supplement, NOT a competing test plan.\n\n**Status: NO synchronized structural-load + electrical-power experiment acquired.** A tool that can compare measured channels is implemented, but no manufactured success trace has been added to the evidence set. [UNH RM2 primary processed observations](https://github.com/UNH-CORE/RM2-tow-tank) are the source of the prior same-rig `RM2-TRADEOFF-001` and `RM2-VARIABILITY-001`; both describe coefficients, NOT blade stress or service life.

## Preregistered engineering question

For the same 1:6 RM2 class cross-flow test configuration in matched inflow: **Does control at measured TSR ≈2.90, compared with Cp-peak TSR ≈3.10, decrease fatigue-relevant bending/strut/bearing load spectra more than it sacrifices useful net electrical energy?** The processed tow tank runs show ~**−1.85% mean Cp** and **−5.51% mean streamwise Cd**, but do not establish net electrical losses under a real PTO. Lower mean Cd may coexist with greater peak cyclic stress: neither mean drag nor `std_cd_per_rev` is a blade-root fatigue load.

## Paired measurement channels required

- Inflow: synchronized source-verified 3-component velocity, turbulence intensity, shear, facility blockage and blockage correction, Reynolds number, temperature, directions/reversal, time-cadence and calibration uncertainty.
- Rotor/structure: rotor azimuth and angular speed, torque time history, blade-root bending in each relevant axis, strut reaction/strain, bearing thrust/radial forces, modal frequencies and transient/peak loads. Record structural calibration and material section modulus; preserve phase and frequency resolution.
- Electricity/control: measured generator-terminal W, active pitch/electronics W, hydraulic parasitics if applicable, auxiliaries W, grid-export if present; time-aligned before integration. Explicitly distinguish shaft mechanical vs net electrical energy.
- Repeat randomized operating-point order and identical control setup; preregister windows, sample rates, replicate counts and a method of estimating uncertainty and correlation. Avoid comparing only one 9-revolution run per condition.

**Data admission:** `tidal_screen/measured_load_gate.py` requires trace provenance, instrument calibration IDs, matched timebases, specified inflow-mismatch tolerances, and simultaneous blade-root bending and electrical-consumption channels. It calculates net electricity as terminal generator power minus measured control and auxiliary consumption, integrates signed power (J) and records alternating bending RMS/peak in N·m. It **rejects synthetic traces by default** and rejects unmatched inflows or absent channels. Synthetic unit-test fixtures test arithmetic only.

## Decision gates (no arbitrary winning score)

1. **Paired data availability:** two independent test IDs with original source hashes and synchronized calibrated signals. **Not met.** The public reduced RM2 CSV reports Cp/Cd statistics but not phase-resolved blade/strut bending and net electrical traces. The independent Sandia RM1 printed Appendix A Cp reproduction also lacks reliable thrust/structural spectra.
2. **Net energy:** quantify measured (not nominal) net electrical delivered energy and uncertainty under matched test window, including controller power. No paid or physical experiments authorized by this repository; data may come from appropriately licensed existing published records.
3. **Damage-relevant load:** quantify load extrema, harmonics and stress-cycle ranges from *verified* bending and material data; inspect fatigue material S–N curves, corrosion/environment and stress concentrations. A lower alternating-bending RMS is not itself validated fatigue life. If data do not show a statistically supported improvement, report the negative result.
4. **Field translation:** matched resource depth, turbulence, mooring/platform response, access windows, ecology, marine-user and Mi'kmaq involvement must independently pass their evidence gates. Do not extrapolate freshwater laboratory values to Fundy annual yield, survivability or fish safety.

The archived current status is `reports/LOAD-READINESS-001.json` (`MEASUREMENTS_REQUIRED`, no observed load-energy result). The first major result must be source-backed, signed, uncertainty-aware measurements—not another parameter sweep through an unsupported Cp curve.
