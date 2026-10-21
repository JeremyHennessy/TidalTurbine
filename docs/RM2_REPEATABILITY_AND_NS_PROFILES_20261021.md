# Follow-on evidence: RM2 second-sweep original NI signals and Grand/Petit Passage seven-day current profiles

**21 October 2026 — measured historical source data, descriptive reduction only.** Base after merged RM2-A evidence: `62eec98e2fac3db421a4d1b6cbb28ec1e8b85198`. No turbine design, fatigue-life, lifetime-energy, physical test, permitted berth or environmental result is certified.

## Source capture and preserved negative results

Independent one-shot [source acquisition run 39604878791](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39604878791) acquired six **original second-sweep** UNH RM2 NI logger files and matching metadata via publisher Figshare source file IDs and verified publisher MD5 plus SHA-256; also acquired two bounded Nova Scotia/CMAR processed ADCP profile windows. Binary originals remain outside Git in seven-day artifact [12347937736](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39604878791/artifacts/12347937736). A first source attempt returned HTTP 404 for a nonexistent Figshare per-file metadata API URL; the completed attempt correctly recovered the file manifest from the official [raw article 1302029](https://doi.org/10.6084/m9.figshare.1302029) and pinned actual file bytes. Preserve this unsuccessful attempt in Actions history.

### RM2 mechanical source comparison

The original `Perf-0.4-b`, `Perf-1.0-b` and `Perf-1.2-b` NI logger files record 2-kHz laboratory rig shaft torque, angle, carriage position and support-force signals. `scripts/replay_rm2_sweep_b.py` replays six runs at nominal TSR 2.9 (source run 10) and TSR 3.1 (source run 12) using source-described tare drag, torque tare, fixed smoothing and original trimmed steady windows. Coefficients reproduce the upstream processed table to within an **absolute tolerance of 0.006** per run; the recorded remaining differences reflect approximate numerical source processing, not new experimental uncertainty bars. Exact checksums and results: `reports/RM2-RAW-B-001.json`; previous independent first-sweep source report: `reports/RM2-RAW-LOADS-001.json`.

| Nominal inflow | Sweep-B mechanical Cp change | Sweep-B mean support Cd change | Sweep-B rig shaft torque standard deviation | Sweep-B support drag standard deviation |
|---|---:|---:|---:|---:|
| 0.4 m/s | −28.47% | −8.14% | −4.32% | −1.72% |
| 1.0 m/s | −2.30% | −5.41% | **+1.14%** | −5.70% |
| 1.2 m/s | −0.04% | −6.38% | **+0.52%** | −10.01% |

A first sweep also gave **higher torque variation at 1.0 m/s** at the lower-TSR point (about +1.71%). These are useful falsifiers for a universal “less drag = less cyclic load” claim. They are **not paired statistical inference**: the two historical sweeps are not sufficiently characterized, randomized, replicated fatigue experiments. Neither includes calibrated blade-root strain, a material stress transfer, actual damage cycles, generator-side/control electricity, or net delivered power. No structural-life benefit is claimed.

### Grand/Petit Passage: bounded actual measured current profiles

[Official CMAR current-profile dataset](https://data.novascotia.ca/resource/is3b-ip8b.json) and [deployment information](https://data.novascotia.ca/resource/uban-q9i2.json) were reviewed. The first seven deployment days from each site were queried with source deployment IDs and exact time-window constraints. Each downloaded source file passed a frozen SHA-256 check; `scripts/qa_ns_passage_profiles.py` preserves the measured depth-bin axis, timestamp cadence and **all original source QC flags** without interpreting them as sensor-native beam validity.

| Field | Grand Passage DG012 | Petit Passage DG002 |
|---|---:|---:|
| Historical deployment period sampled | 2020 Aug 27–Sep 2 | 2010 Aug 4–10 |
| Original processed profile rows | 10,463 | 11,409 |
| Unique reported times | 897 | 934 |
| Height above seabed labels | 1.5–14.5 m, 14 bins | 5.7–53.7 m, 13 bins |
| Original speed-QC Pass | 9,523 | 10,274 |
| Original speed-QC Suspect/Of Interest | 820 | 907 |
| Original speed-QC Fail | 120 | 228 |
| Median published Pass-only speed **in these windows** | 0.722 m/s | 0.202 m/s |

These speeds describe different historical windows, elevations and geographic contexts. **They cannot be ranked as expected site electricity output.** Time strings in the source subset lack an explicit timezone offset; do not silently label them UTC without verifying publisher convention. Report: `reports/NS-PASSAGES-7D-SUMMARY-001.json`. CMAR's [data-governance guidance](https://cmar.ca/coastal-monitoring-program/data-governance/) identifies Pass/Suspect/Fail as QC signals for user review; they do **not** replace the original ADCP correlation, orientation, instrument-depth or beam-rejection metadata.

### Reproduction

From a Python environment with `numpy` and `h5py` as pinned in `requirements-ocean.txt`, using the **acquired source ZIP** downloaded separately from the Actions artifact:

```sh
python scripts/replay_rm2_sweep_b.py --archive /path/to/rm2-sweep-b-grand-petit-originals.zip --out /tmp/RM2-RAW-B-001.json
python scripts/qa_ns_passage_profiles.py --archive /path/to/rm2-sweep-b-grand-petit-originals.zip --out /tmp/NS-PASSAGES-7D-QA-001.json
python scripts/check_followon_gates.py
python -m unittest discover -s tests -v
```

Both source scripts **fail closed** if the original archived file hashes, row counts, expected fields or published RM2 coefficient check differ. Original acquired binaries must not enter normal Git history. Temporary Actions artifact retention does not constitute durable preservation; source identifiers, query windows, checksums and re-acquisition instructions do.

### Engineering hard gates and subsequent work

1. Obtain original FORCE Nortek native beam-quality and the source conversion mapping, or qualify independently documented CMAR depth bins including source QC algorithms and calibration before **any** site-specific turbine-power calculation. Current source-approved rotor inflow = **zero**.
2. For the observed RM2 mechanical tradeoff, measure synchronized blade/root/support strains plus generator/PTO/control electricity under randomized matched multi-speed, multi-direction and replicated conditions before inferring fatigue damage or delivered-electricity gains. No physical lab work is authorized by this study.
3. Preserve the existing 20-system [instrumented rig requirements](PROTOTYPE_TEST_RIG_ENGINEERING_20261020.md) as prospective only; a real lab facility, calibration plan, qualified safety review, written quote and independent access/ecology/Mi'kmaq/fisheries/permit gates remain missing. Existing TidalLab layouts and prior simulations were not modified in this research-only pass.
