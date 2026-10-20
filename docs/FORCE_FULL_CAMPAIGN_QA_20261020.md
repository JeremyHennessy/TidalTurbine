# FORCE spring-2018 complete processed source: current + wave numerical QA

**Research date:** 2026-10-20. **Status:** `NUMERICAL_QA_ONLY_ZERO_SOURCE_APPROVED_ROTOR_INFLOW_BINS`.

This advances the earlier two-hour and 72-hour bounded snippets to **both complete, publisher-hosted processed NetCDF source files** from one physical ADCP deployment. It does **not** recover the original native Nortek `.ad2cp` beam measurements. Nothing in this study qualifies a vertical turbine inflow profile, engineering design current, fatigue exposure, annual resource, site suitability, or environmental safety. Prior `SCREEN-001` and `RM1/RM2` experimental results are unchanged.

## Sources, exact provenance, acquisition

- FORCE current NetCDF, full processed March–May 2018: https://cioosatlantic.ca/erddap/files/FORCE_Mar2018_ADCP_Currents/Burst.VTC.DSEL.AVER.classic.nc — **3,348,741 bytes**, SHA-256 `be8acb1802786a0db7f5c2952e4554fc25f03508550b7478a19a2f47d86864e2`.
- FORCE wave NetCDF, same campaign: https://cioosatlantic.ca/erddap/files/FORCE_Mar2018_ADCP_Waves/Burst.VTC.WAVES.classic.nc — **119,465 bytes**, SHA-256 `d538b46f4b702382386721a43d39ec253f281f48522a377bf456b5d3373001ee`.
- Publisher [current metadata](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html) and [wave metadata](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Waves/index.html) identify FORCE/CIOOS Atlantic, instrument serial **100258**, CC BY 4.0, processed 2022-01-13 using CIOOS's `convert_force_nc.py`, UTC timestamps and metres-per-second ENU components.
- Both `.classic.nc` files **actually have an HDF5/NetCDF4 signature**. Treating the suffix as reliable format detection previously produced a failed one-shot run; the corrected strict signature check also recognizes HDF5. The successful [GitHub Actions acquisition run](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39484948868) downloaded the two source files and preserved their SHA-256 manifest in [artifact 12292418917](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39484948868/artifacts/12292418917), with **7-day artifact retention**. The raw binary files remain **outside Git**. The original failure and fix are retained in the workflow history.
- Coordinates carried in NetCDF attributes are **45.3631389°N, −64.4274722°**, more precise than ERDDAP's rounded **45.3631°N, −64.4275°**. These are metadata, not an independent marine survey.

## Source processing verified locally (all source files and 72h archive available)

| Check | Source-derived finding | Restriction |
|---|---|---|
| Temporal samples | **5,265 bursts** between 2018-03-30 20:02:33 UTC and 2018-05-24 16:02:30 UTC, spanning **56 UTC calendar dates** | Short historical spring deployment, not an annual resource |
| Cadence | 5,263 intervals of 900 s; 1 transition of 897 s | Nominal 15-minute observed records, not original 2 Hz burst signals |
| Observed velocity array | **263,250** ENU triplets = 50 transducer-relative cells × 5,265 times | Cell labels are not certified height above bed or depth below surface |
| Zero triples | **97,911** (37.1932%) all components exactly zero | Cannot interpret exact zeros as hydrodynamic slack without source-native masking |
| Completely zero upper cells | **39.5–50.5 m**, all 12 cells zero at every timestamp | A genuine near-surface masking pattern is plausible, but not established at beam level |
| Pressure-collapse transition | **90** bursts with current pressure below arbitrary 20 dbar screen, including **88 final consecutive bursts** with all 50 velocity cells zero, from 2018-05-23 18:17:30 UTC | Strong **hypothesis** of instrument exit/recovery; deployment log not obtained, threshold not publisher QC |
| Nominal cell size | 1.0 m except **14** terminal bursts with reported cell size 0 | Additional end-of-deployment anomaly |
| Preterminal *screen* only | In 5,175 bursts with pressure ≥20 dbar, **26** cells (1.5–26.5 m) had no exact-zero triplets; **12** (27.5–38.5 m) intermittent zeros; **12** (39.5–50.5 m) all zero | **Not certified usable bins**. The ≥20-dbar screen is analyst chosen, not instrument manufacturer or publisher rule |
| Pressure / upper zero boundary | Pearson correlation **r≈0.99627** between pressure and highest numerically nonzero range on the comparison window | Descriptive evidence of surface/tide-linked availability only; not a physical cell-centre correction |
| Currents/waves timestamps | Same 5,265 positions, max timestamp disagreement ~0.000277 s | Compatible reporting windows; data-processing pipelines may differ |
| Two pressure streams | Median absolute current/wave pressure difference ~0.011 dbar; **one** deviation above 0.1 dbar, maximum ~0.765 dbar during suspected recovery | Must document before interpreting wave extremes or pressure as surveyed water level |
| Wave outputs | Significant wave-height field has **5,265 numeric entries** (one exact zero); maximum-period field has **431** `−9` fill sentinels and 4,834 positive numeric entries | No native wave QA was supplied; numbers do not establish trustworthy metocean extremes |
| Prior source agreement | All **14,400** velocity records in SHA-pinned April 1–4 ERDDAP CSV were re-matched by UTC + relative range to the complete NetCDF, max component difference **2.375×10⁻⁷ m/s** | Confirms processing-data consistency, **not** physical quality or annual validity |

**Important:** During pressure-collapse samples the wave-height field also returns numeric values. They are **not** automatically credible waves. The numeric maximum wave-height value (3.421683 m) occurs at a pressure-disagreement/recovery-transition sample, so the report additionally records a *pressure-screened diagnostic* wave-height range without calling it a source-QC-cleared sea-state record.

## Reproducibility

The source files are not stored in Git. Download them again from the two stable FORCE/CIOOS links if the seven-day GitHub artifact expires. Validate exact SHA/length against the pinned manifest rather than silently accepting a changed provider file. To reproduce all compact derived records using the downloaded GitHub Actions ZIP:

```sh
python -m pip install -r requirements-ocean.txt
python scripts/process_force_campaign.py \
  --archive /path/to/force-spring2018-complete-processed-netcdf.zip \
  --prior-72h-archive /path/to/force-adcp-72h-raw-qa-ccby4.zip
python scripts/check_force_campaign_report.py
python -m unittest discover -s tests -p 'test_force_campaign.py' -v
```

If the optional older 72h artifact is unavailable, omit `--prior-72h-archive`, direct output to a **temporary location**, and explicitly note that the prior-data cross-check was not rerun. The tracked checksum-verified canonical report includes that independently completed cross-check.

Published compact derivatives: [`reports/FORCE-CAMPAIGN-QA-001.json`](../reports/FORCE-CAMPAIGN-QA-001.json) with all 50 per-cell status rows and 56 calendar-day summaries; [`research/observations/FORCE_CAMPAIGN_DAILY_QA_2018.csv`](../research/observations/FORCE_CAMPAIGN_DAILY_QA_2018.csv), dates, source counts, zero flags, sample pressure, descriptive wave diagnostics. No synthetic velocities were substituted for observations. No velocity series was passed to a turbine model.

## Scientific acceptance gates still blocking inflow

1. **Publisher-native ADCP quality:** Obtain authoritative original `.ad2cp` beams (percent-good/correlation/tilt/heading/echo-amplitude and source processing), fill/zero rules and original transformation algorithm. Neither source HDF5 includes those per-beam quantities. Do not infer all nonzero profiles are valid.
2. **True vertical geometry:** Independent reviewed Viehman et al. (2022), DOI `10.3389/fmars.2022.851400`, places the upward transducer 0.7 m above seabed, with 1 m blank and 1 m cells, and first centre 2 m above transducer; published NetCDF labels first range **1.5 m**, unresolved whether cell edge/centre convention differs. Confirm water level, magnetic/ENU, tilt, sidelobe and bathymetric depth using source configuration.
3. **Full interval:** Check phase/direction shifts, hydrodynamic turbulence spectra, instrument range quality, end-of-deployment log, and gap/observational censoring. One ~55-day period is better than 72 hours, but not independent spring-neap/seasonal/extreme design characterization.
4. **Independent cross-source:** Compare concurrently observed wave/pressure and CHS gauge height with matching tidal/vertical datum; do not treat water levels as currents or use pressure as absolute sea level without datum conversion.

**Decision:** The raw processed archives are **acquired**, source bytes are checksum verified and internally consistent, and candidate numerical regions are separated from suspect masks. **ZERO** velocity ranges are currently approved for physical turbine inflow modelling. Existing source discovery catalogue entries still count *sources*, not all acquired observations.
