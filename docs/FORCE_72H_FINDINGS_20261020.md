# FORCE 72-hour observation — source replay, range-cell censoring and remaining QC

**Evidence class: measured-source observations with numerical QC ONLY, not qualified turbine inflow.** See the deterministic, small, shareable [`reports/FORCE-72H-QA-001.json`](../reports/FORCE-72H-QA-001.json). Original measured CSV is deliberately not committed to Git.

## Acquisition, source and replication

- GitHub Actions one-shot run [39482098852](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39482098852) succeeded; 7-day-retention artifact `12292085881` (`force-adcp-72h-raw-qa-ccby4.zip`) holds `source.csv` and original `qa.json`. **This artifact is temporary**, so the stable record includes exact source URL/UTC window and source SHA-256. No automatic recurring acquisition was configured.
- Original FORCE/CIOOS Atlantic [ERDDAP current product](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html), CC BY 4.0. Query UTC 2018-04-01 00:00:00 to 2018-04-04 00:00:00, `source.csv` 1,310,499 bytes, **SHA-256 `d05f2a1258d9908b04fc7017cdb818ca318ac47c38e6b40244eac8c378ec4c7a`**.
- Reproduce when the artifact is available: `python scripts/force_72h_summary.py --zip <zip-path>`, then independently run `python scripts/force_long_window.py --input <extracted-source.csv>`. The replay verifies the source hash, the archived numeric-QA counts and computes a descriptive pressure/range correlation. Re-fetch the same bounded source request after artifact expiry and note if its checksum differs; do **not** silently equate a changed product with the 2026-10-20 extract.

## Measured numeric signals and failure signatures

| Observation | Source-derived finding | What this means |
|---|---|---|
| Parsed east/north/up triplets | **14,400** with 0 numeric rejections | Arithmetic/parsing passed, not acoustic or ecological scientific QC |
| UTC ensembles | **288** exactly 900 s apart, 50 range cells per time | Three days of sampled *burst averages*, **not** raw 2 Hz turbulence/loads |
| Exactly (0,0,0) E/N/up triplets | **5,160 (35.83%)** | Suspected processor fill/surface masking, not proven real current slack |
| Entirely zero range labels | **39.5–50.5 m**, 12 cells | Cannot represent continuous zero-flow water column at all tidal stages |
| Intermittently zero range labels | **27.5–38.5 m**, 12 cells | Zero/nonzero boundary changes as the water column varies |
| Nonzero throughout three days | **1.5–26.5 m**, 26 cells | Merely **numeric candidates**; all acoustic-beam QC still missing |
| Pressure | **31.8128–44.4779 dbar** | Water pressure at sensor, **not** calibrated sea-surface elevation in metres |
| Highest *nonzero* range label | **26.5–38.5 m** | Descriptive only; not a verified physical air/water boundary |
| Pressure vs highest-nonzero label | **Pearson r=0.996882**, slope≈0.88809 m/dbar | Strong tide-dependent association **consistent with** upper-column clipping; no proof of encoded fill rule |

## Instrument geometry recovered in an independent primary publication

Viehman et al., *Frontiers in Marine Science* 9:851400 (2022), [doi:10.3389/fmars.2022.851400](https://doi.org/10.3389/fmars.2022.851400), sec. **2.1** and **2.2.2**, describes the matching FAST3 March–May 2018 deployment. It explicitly states:

- **Nortek Signature 500 upward-facing transducer face 0.7 m above seabed** (the *Nortek itself*, not just the Simrad echosounder), 1-m blanking interval, 1-m cells; **first measurement cell centred 2 m above transducer face**. It also documents 5-minute bursts every 15 minutes, 2 Hz native samples, and platform tilt/compass declination adjustment in original research data processing.
- The authors excluded **uppermost 10% of water column** in their analyses due to sidelobe interference. This is **not evidence** that the public ERDDAP *processed export* carries the identical mask, and a generic top-10% recipe without surface/tilt metadata is not a validated quality routine.
- There is a **source mapping discrepancy**: ERDDAP `cell_range` labels begin **1.5 m** whereas the paper reports the first cell centre **2 m from the face**. Whether this is cell edge/centre nomenclature, frame transform or a processing difference remains unresolved. **Do not apply `height_above_seabed=0.7+cell_range` as an engineering-grade geometry transform.** The nominal paper first-cell centre would be 2.7 m above seabed if definitions apply as written, but matching it to ERDDAP cells is not established.
- The published methods describe converting raw platform signals to averaged processed horizontal velocities. The public CSV does not contain original per-beam amplitude/correlation/percent-good, platform tilt, declared fill-value encoding, full beam/sidelobe masks or exact transformation lineage. Observational `0,0,0` values must not be used as physical current readings until verified against raw/native metadata.

## Decision and next experimental gates

**No velocity bins have been qualified for turbine predictions yet.** No measured FORCE reading was fed to SCREEN-001, RM1, RM2, an energy yield forecast or a physical design ranking. A **72-hour** window does not determine spring-neap variation, annual energy or extreme loads. The **next decisive acquisition** is the original .ad2cp/raw beam-quality/correlation files or the conversion pipeline's source QC rules and precise `cell_range` mapping; cross-check the masked native data against this pin with uncertainty. Only after independently confirmed valid water-column bins and time coverage should an engineering sampling envelope be defined. Site permissions, fisheries, navigation and Mi'kmaq interests remain separate stop gates.
