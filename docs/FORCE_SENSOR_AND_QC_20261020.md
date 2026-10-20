# FORCE FAST3 ADCP: instrument geometry, quality masking and a bounded longer sample

**Scope and status (2026-10-20):** the original acquired two-hour CSV is preserved by its SHA-256 `1a19da1e3cd214fc904d8e821cc50c7e959693aaffa4dc9c8e84ee6c663ac4cb`. A new explicit one-time 72-hour download and numeric QA tool is supplied by `scripts/force_long_window.py`. **Longer data are not acquired, QC-cleared or integrated into the turbine model merely because this script/workflow exists.** Record the verified artifact and results after Actions completes. Raw current observations remain outside Git.

## Source instrument identification (new verified report evidence)

1. [FORCE / OERA fish-sensor final report](https://oera.ca/sites/default/files/2020-04/FISH%20FINDER%20Final%20Report%2031-03-2020_0.pdf), PDF p.7–8, section 3.2: bottom-mounted FAST3 autonomous platform equipped with **Nortek Signature 500 ADCP pointing upward**, ASL sensor, Aanderaa RCM and Simrad WBAT. The March–May 2018 Signature 500 acquisition used a **5-minute burst every 15 minutes, 2 samples/s within burst**. This agrees with the 15-minute processed ERDDAP cadence; the published product is *averaged* and cannot recover within-burst 2-Hz signals.
2. Same report PDF p.15–16, section 3.4.1: original Nortek files were converted using **Nortek Signature Deployment 3.4.17.0** to **speed-direction-up** (SDU), averaging five-minute bursts. The authors **estimated the surface from maximum echo backscatter and excluded the upper 10% of the water column** in their scientific analyses to limit acoustic sidelobe interference. They corrected reported compass directions using **−17.22°** local magnetic declination in that analysis. **Do not apply −17.22° again to published ERDDAP east/north values without independent transform-lineage verification.**
3. [FORCE/CIOOS ERDDAP variables](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html): instrument identifier `100258`, latitude **45.3631 N**, longitude **−64.4275 degrees east** (i.e., 64.4275° W); UTC 2018-03-30–2018-05-24, **50 range labels, 1.5–50.5 m, whose exact centre/edge mapping is unverified**. The `cell_size` field is available (published `actual_range` 0.0–1.0 m, which may include nonphysical zeros). Velocity components are labelled east/north/up, m/s. The metadata table **does not list per-vector quality flags, beam correlation or an explicit velocity `_FillValue`**.
4. This final report describes the *Simrad WBAT* transducer at **0.7 m** above the FAST3 platform; **the 2020 report alone does not state the Nortek face elevation**. Subsequent peer-reviewed Viehman et al. (2022), section 2.1, independently supplies the **Nortek** face at **0.7 m above seabed**, a 1-m blanking distance and 1-m cells, first *measurement centre* 2 m from the face. ERDDAP labels start at 1.5 m; this reference discrepancy is **unresolved**. Frame tilt, ERDDAP transformation lineage, source-specific fill/quality mask and correct pressure-to-depth conversion remain unresolved. See `docs/FORCE_72H_FINDINGS_20261020.md`. One known upward orientation does not make specific cells physically valid.

## Observed two-hour failure signature — reproducible, not a validated mask

Reproduce from the original, checksum-pinned acquired artifact with `python scripts/review_force_artifact.py --zip <original.zip>`.

- 2018-03-30, nine 15-minute bursts, **450 parsed cells**, **206 exact (0,0,0) vectors**.
- Cells **30.5–50.5 m**: **21/21 entirely zero** over all nine bursts. Cells **27.5–29.5 m**: partially zero, with the all-zero boundary changing over time. Cells **1.5–26.5 m**: numerically nonzero throughout this *short* sample, **not** individually certified by source QC.
- These patterns are **consistent with** out-of-water, near-surface or invalid-bin substitution; they are **not proof** of the exact encoding. An entire upper area of (0,0,0) triples across multiple tidal stages should not be assumed real zero-speed tidal slack. The observed nonzero cells are also not automatically beam-quality-valid.

## New 72-hour bounded acquisition and science gate

```sh
python scripts/force_long_window.py --input data/local/force_multiday/source.csv --out data/local/force_multiday_review
# or, on authorized networking, explicitly:
python scripts/force_long_window.py --fetch --out data/local/force_multiday
```

Run a **single, non-recurring** GitHub Actions acquisition from `research/force-rm1-design-gates-20261020`: `.github/workflows/force-72h-qa-one-shot.yml`. It requests 2018-04-01 00:00 to 2018-04-04 00:00 UTC, 9 selected variables including pressure and cell size, maximum **12 MiB**, and stores the raw response and numerical QA manifest in a **7-day Actions artifact**. No raw data are committed. Reacquire if the artifact expires; do not treat an expired temporary archive as a permanently curated dataset. Network errors must be reported, not filled by simulation.

The QA report enumerates per-cell exact-zero frequency and all-zero/partial-zero/nonzero **numeric** candidates, cadence, possible data gaps, pressure ranges, reported cell sizes, source CSV SHA-256, location and source URL. Pressure (dbar) is *not* a calibrated column-height measurement until atmospheric pressure, density, instrument elevation, hydrostatic offsets and pressure QC are established. The report does **not** designate any physically valid depth bins or claim a qualified site current series.

### Strict scientific acceptance before using any observed current in the power or fatigue model

1. Acquire native `*.ad2cp` or provenance-equivalent instrument/configuration data: serial, mounted head elevation above seabed, true upward beam tilt, time-varying surface estimates, water depth and transducer/bottom reference. Verify whether CIOOS processing already corrects magnetic declination and invalid-bin masking.
2. Obtain raw backscatter/quality diagnostics (beam correlation, amplitude, percent-good, error velocity or available Nortek equivalents). Recreate and independently check the surface-adjacent 10% sidelobe exclusion for each burst, rather than using a universal 30 m cutoff. Match near-bed blanking and temperature/salinity/sound-speed processing.
3. **Only** after cell masks are justified: identify continuous same-depth valid time series, fraction missing, uncertainty, instantaneous speed/direction and tidal phase; preserve excluded zeros as `missing`, never recode them as zero flow. For annual/intersessional estimates obtain substantially longer sampled coverage or validated site resource model.
4. Do not claim rotor swept-zone depth, usable energy, environmental safety or annual capacity factor based on this campaign. Indigenous rights, marine users, navigation, turbulence and ecology remain independent deployment gates.

**Current model_ingestion: BLOCKED_PENDING_NATIVE_QUALITY_METADATA_AND_VERIFIED_WATER_COLUMN.**

## Acquired multiday source follow-up

A **successfully acquired** three-day sample from the same dataset is separately documented in [`docs/FORCE_72H_FINDINGS_20261020.md`](FORCE_72H_FINDINGS_20261020.md). Its source SHA and reprocessing statistics are fixed in `reports/FORCE-72H-QA-001.json`. This new status **supersedes** any proposal-only text above, but does not upgrade unverified velocity cells into physical inflow observations.
