# Nova Scotia ocean-data acquisition / qualification — 2026-10-20

**Data readiness is not turbine readiness.** This pass located sources and documented variables, attribution, temporal coverage, coordinates and limitations; **no third-party ocean time-series was downloaded into this session's working source tree**, and no instrument reading has been passed to the turbine simulator. `research/ocean_datasets.json` has 20 **discovery records**, including an explicitly duplicated FORCE file access path; these are NOT 20 independent campaigns. `research/DATA_INVENTORY.csv` remains the existing lower-level research register.

## High-priority located field data

| ID | Evidence / dataset | Reviewed metadata | Data acquisition | Engineering limitation |
|---|---|---|---|---|
| OCEAN-001 | [FORCE March–May 2018 ADCP currents](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html) | Explicit lat=45.3631 lon=-64.4275 WGS84, velocity components east/north/up in m/s, range cells 1.5–50.5 m relative to instrument; start `2018-03-30T20:02:33Z`, end `2018-05-24T16:02:30Z`; CC BY 4.0 | NetCDF source file *listed*, not acquired or QC'd | Depth relative to transducer not seabed/chart datum. Read actual deployment metadata/quality flags/beam and frame conventions before use. |
| OCEAN-002 | [FORCE corresponding ADCP waves](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Waves/index.html) | Same instrument/site/dates; significant wave height (m), wave period (s), pressure (dbar); CC BY 4.0 | NetCDF listed but not acquired | Historical short campaign not extreme-condition design distribution. |
| OCEAN-003 | [FORCE meteorological tower](https://cioosatlantic.ca/erddap/info/force_meteorological_tower/index.html) | Tower at 45.3713, -64.403 per ERDDAP metadata | Metadata only | Wind/air conditions differ from subsea rotor and do not establish vessel availability. |
| OCEAN-004/005 | [CHS IWLS API](https://tides.gc.ca/en/web-services-offered-canadian-hydrographic-service) | Water-level observations, predictions, stations/datum, QC flags; some stations have other phenomena | *Service licence/terms gate*; not acquired | **Water-level height is not tidal stream speed**. Some station-specific current channels may exist; inspect individual station series. |
| OCEAN-006 | [CHS NONNA](https://open.canada.ca/data/en/dataset/d3881c4c-650d-4070-bf9b-1e00aabf0a1d) | 10 / 100 m raster bathymetry; modified Apr 2026 | Manual portal selection | **Non-navigational only**, check vertical datum, source survey date and uncertainty. |
| OCEAN-008 | [GEBCO 2026 grid](https://www.gebco.net/data-products/gridded-bathymetry-data) | 15 arc-second global bathymetry plus Type Identifier grid | Subset download needed | Grid is regional context, not engineering-level foundation clearance. |
| OCEAN-010 | [DFO AZMP Prince 5 1991–2020 climatology](https://open.canada.ca/data/en/dataset/b5e11d7e-7f76-4834-b5a4-292fc3503a94) | Temp/salinity/density climatology, outer Fundy, published Sep–Oct 2026; CSV & NetCDF | Not acquired | Not Minas Passage turbine-hub velocities. |
| OCEAN-012 | [DFO NW Fundy CTD](https://open.canada.ca/data/en/dataset/40619839-51e2-4151-9ea9-2e29d42aa948) | Moored temperature/conductivity/depth observations | Not acquired | Different sites and purposes. |
| OCEAN-013/014/015 | DFO benthoscape, right-whale likelihood, marine conservation network maps | Published discovery records | Not acquired | Ecological risk/rights/licensing require deeper studies and consultation. |

Registry additionally covers met buoys, DFO 2025 environmental monitoring report, provincial permits, AZMP Station 2, fish survey catalogue and alternate file routes. Every record contains a `next_action` and a material `limitations` field.

## Acquisition commands (opt-in network, do not commit raw data)

```sh
python scripts/check_ocean_catalogue.py
python scripts/acquire_force_adcp.py --dataset currents           # Dry-run only, no download
python scripts/acquire_force_adcp.py --dataset currents --download  # downloads original ~3.35 MB NetCDF
python scripts/acquire_force_adcp.py --dataset waves --download     # downloads original ~119 kB NetCDF
```

Acquisition tool writes to `data/raw/force-adcp-2018/` (Git-ignored). It enforces listed file byte sizes, bounds downloads and records a SHA-256 and timestamp in adjacent `.manifest.json`. The download itself does not QA data; upstream may change file size or location. Review FORCE/CIOOS attribution and licence, the instrument's sampling metadata, corrupt/invalid bins, coordinate frames and QC before processing. Data access is not guaranteed by a CI test because CI has no external data dependency.

For CHS IWLS, follow the [2026-10-15 API documentation](https://tides.gc.ca/en/web-services-offered-canadian-hydrographic-service) and accept its terms before collection. Limits reported: 3 requests/second and 30/minute, with 1-minute data up to 1 week/request, 3-minute data up to 3 weeks/request, coarser data up to 1 month/request. Preserve station IDs, datum, QC codes and UTC; never extrapolate a gauge height derivative into an unvalidated turbine-flow time series.

## Mandatory physical data QA gate before performance screening

1. Download immutable raw file; record provider URL, current service metadata, licence, retrieval UTC and SHA-256. Confirm the file format and original instrument frame, bin size, blanking distance, compass calibration and tidal flow sign.
2. Inspect measurement dates, sample cadence, gap duration, NaN/fill values and QA/QC flags. Map cell range to actual rotor swept interval only with verified mounting configuration and water-level datum. Record wave/current synchrony.
3. Reproduce current vectors and speed magnitudes at fixed **declared** heights (if known). Use directional distributions, depth shear, flood/ebb differences, turbulence characterization and epistemic uncertainty. Do not treat metadata min/max as operational percentiles.
4. Hold back an out-of-sample comparison against independent measurements or published site analysis; model uncertainty and deployment representativeness. Different campaigns must not be pooled without normalisation.
5. Use loads/control model only when turbine-dependent Cp, Ct and blade-moment curves have been validated. **Measured inflow alone does not validate the rotor model.**

## Coverage limit

This is a first, curated inventory, **not all existing ocean data**. Additional discovery targets: specific 2020–2026 FORCE instruments, historical long-duration ADCPs, tidal harmonics/hydrodynamic model outputs, higher-frequency turbulence, seasonal ecology/acoustic monitoring, moorings/cable/geotechnical measurements, sediment transport, marine traffic, fisheries effort and Mi'kmaq-led governance. Do not assume absence if a dataset wasn't located in a short search pass.
