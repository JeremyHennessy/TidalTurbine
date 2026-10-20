# RM2-OBS-001 — experimental *processed-data reproduction*, not predictive validation

**Question:** Can we recover a published cross-flow Cp/CD vs TSR curve from inspectable primary processed data, without inventing an alternative architecture power curve?

- **Baseline:** UNH-CORE/RM2-tow-tank `Data/Processed/Perf-1.0.csv`, immutable Git blob `1f284211d5c19593cf753e63727ae62a62356439` on inspected upstream master tree `fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef`.
- **Changed variable:** None. Re-present exact published processed run records, transcribed to seven decimal places for a bounded curated fixture. **This is not an independently estimated hydrodynamic coefficient.**
- **Test model:** RM2 experimental 1:6 *cross-flow* turbine, diameter 1.075 m, height 0.8067 m. Approximately 1.0 m/s laboratory carriage speed. Upstream uses `A=D*H` and fresh water 1000 kg/m³ in processing code; not a Nova Scotia turbine.
- **Acceptance:** 23 unique run IDs; positive finite numeric fields; observed reported peak Cp≈0.35460 at reported TSR≈3.09935; original source location, Git blob identity, CC BY 4.0 attribution included. Pass/fail deterministic. Unit tests intentionally fail for an incomplete fixture.
- **Run:** `python scripts/reproduce_rm2.py`; output `reports/RM2-OBS-001.json`. `python -m unittest discover -s tests -v`.
- **Result:** 23 reproduced processed rows, peak `mean_cp=0.3546025` at `mean_tsr=3.0993495`; `mean_cd=0.8458717`, source field `exp_unc_cp=0.0080504`. Uncertainty column preserved **as named**, not automatically interpreted as a 95% interval.
- **What it supports:** Select RM2 data as an experimental *target* for a future independent cross-flow predictive model. Construct observational chart in TidalLab.
- **What it does NOT support:** Calibration-independent Cp prediction, blade fatigue, full-scale energy, net electrical export, environmental safety, real-site suitability or comparison against Sandia RM1 efficiency. Original raw signals (~10GB), calibration files, tare corrections and repeated sensor processing have not been independently rerun. The subset truncates source precision to seven decimals; users requiring precision should obtain original Git blob.
- **Citation:** Bachant, P., Wosnik, M., Gunawan, B., Neary, V. S. (2016). *UNH RM2 tow tank experiment: Reduced dataset and processing code*. DOI: 10.6084/m9.figshare.1373899. Source data CC BY 4.0. Code MIT.
