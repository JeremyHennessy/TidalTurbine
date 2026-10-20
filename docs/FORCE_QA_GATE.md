# FORCE / CIOOS measurement acquisition gate (2026-10-20)

**Updated evidence status — source acquired; scientific QC blocked (2026-10-20).** An initial local container had no CIOOS DNS access, but a subsequently completed one-shot GitHub Actions run 39470715965 retrieved a real two-hour CSV slice (450 rows) and preserved it as a short-lived artifact. Independent local replay found 206 exact-zero velocity triples, including 21 entirely zero range cells, suspected fill/mask values. The original script counted all 450 as *numerically parseable*; this does not mean physically valid. See [`reports/FORCE-SLICE-QA-001.md`](../reports/FORCE-SLICE-QA-001.md) and its SHA-linked JSON. No measurements were ingested into the turbine simulator and no quality-approved depth profile exists.

Verified [ERDDAP variable metadata](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html): UTC 2018-03-30 20:02:33 to 2018-05-24 16:02:30, WGS84 position 45.3631/-64.4275, transducer-relative `cell_range` 1.5 to 50.5 m, 50 range bins, velocity components E/N/up in m/s; sea-water pressure dbar and temp °C; CC BY 4.0 credit FORCE and CIOOS Atlantic. Instrument head height, pointing/tilt, manufacturer QC filters, blind zones, surface sidelobe masking and near-bottom blockage not established. Metadata *actual_range* is not a design current limit or clean sample.

## Safe bounded first read

```
python scripts/qa_force_slice.py                         # dry run, no network
python scripts/qa_force_slice.py --fetch                # explicitly fetch a UTC 2-hour CSV subset to ignored data/local/
python scripts/qa_force_slice.py --input data/local/force_adcp_slice/source.csv
```

The URL selects only selected velocity variables and a 2-hour UTC window and enforces 8 MiB maximum download. Saves raw CSV and a hash-linked QC manifest outside Git. QA checks UTC parse, finite vectors, coordinate/range bounds, timestamps, duplicate time/range pairs, per-cell gaps, cadence, geographic coordinates and basic extreme-value arithmetic filtering. **It does not** establish physically valid cells, vertical datum, rotor depth, annual recurrence or velocity shear representativeness. A source lacking published flags is explicitly marked as such rather than silently marked quality-cleared.

## Acceptance gate before observed-data simulation

1. Retain exact source URL, retrieval UTC, original SHA256, licence, file format/units, timezone.
2. Inspect instrument frame, tilt, transducer elevation above bottom, bathymetric and pressure datum, signal correlation and manufacturer QC. Identify blade-relevant depth bins and dynamically submerged bins.
3. Apply source-correct masks and assess gaps, noise, directional rotation, near-surface aliasing and bursts independently; publish only a small aggregated *QA*-cleared derivative with full uncertainty, keeping the raw file ignored.
4. Do not treat a 2-hour slice or even the two-month deployment as annual resource, slack duration, storm extremes, full site assessment or environmental approval.
5. Compare alternative operating envelopes only after that gate; avoid placing a kite across unverified depth/navigation corridors.

The existing source downloader `scripts/acquire_force_adcp.py` remains available for the complete 3,348,741-byte NetCDF, but successful byte-level download/signature checks also do not equal scientific quality control.

## Reconciliation of evidence state / next test

- Original acquisition: GitHub Actions artifact [12286987076](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39470715965/artifacts/12286987076); source bytes SHA256 `1a19da1e3cd214fc904d8e821cc50c7e959693aaffa4dc9c8e84ee6c663ac4cb`. Artifact retention 1 day, so keep an authorized private original if needed; do not commit raw CSV.
- The **request URL encoding** must use `time%3E=` and `time%3C=`, not encode the comparison `=` as part of the key. A successful acquired artifact confirms endpoint selection and source data.
- Corrected `scripts/qa_force_slice.py` now explicitly flags exact triples `(0,0,0)` without deciding their physical validity; arithmetic bounds alone are NOT publisher QC. Replay `python scripts/review_force_artifact.py --zip <artifact.zip>` or `--csv <original-source.csv>` and compare report SHA.
- Resolve whether upper range cells were outside water, side-lobe masked, zero-filled or otherwise invalid via instrument orientation, water level, acoustic quality, transducer height and documentation. Until then, **do not use the 244 nonzero points either** as a validated resource distribution. This campaign is short relative to a tidal or seasonal cycle.

## Instrument-evidence update — 2026-10-20

The earlier statement that instrument **orientation** was unverified is superseded by published FORCE/OERA final-report sections 3.2.2 and 3.4.1: the March-May 2018 Nortek Signature 500 on FAST3 was **upward looking**, with five-minute bursts every 15 minutes, 2 Hz within bursts; the report describes excluding upper 10% after estimating surface backscatter. It does **not** determine actual instrument height, source ERDDAP invalid-bin/zero semantics, calibrated pressure depth or per-bin acoustic quality. The reported 0.7 m height applies to the *WBAT*, not this Nortek ADCP. See [new source-backed QA and longer-window acquisition](FORCE_SENSOR_AND_QC_20261020.md). Preserve prior 2-hour acquisition history and model hold.
