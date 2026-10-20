# FORCE / CIOOS measurement acquisition gate (2026-10-20)

**Status: NOT ACQUIRED in this run.** The open CIOOS/FORCE source URL for the spring 2018 ADCP is discoverable. The local container cannot resolve the domain for direct curl, and an attempted source NetCDF download was unsuccessful. A failed access attempt is not a data result; no measured vectors were inserted into SCREEN-001 or RM2 reports. No current data histogram in Pages should be represented as observed.

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
