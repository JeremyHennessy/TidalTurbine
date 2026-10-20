# FORCE and CMAR measured-observation ingestion gate — 20 October 2026

**Classification:** observed *processed* ocean data and reproducible numerical QA. **No scientific approval for turbine inflow, fatigue loading, site resource, environmental safety or a design comparison.** This extension preserves historical SCREEN-001, RM1/RM2 and the approved TidalLab UI. See `research/ocean_datasets.json` for the updated acquisition states and original discovery IDs.

## 1. FORCE spring 2018: all observation cells, safely segregated

- Physical provenance: FORCE seabed-mounted, upward-looking **Nortek Signature 500**, serial 100258. At about 45.3631389°N, 64.4274722°W. Native raw instrument `*.ad2cp` file / deployment config and processing transform are required to recover correlation, beam rejection, orientation/tilt and the zero/missing-velocity mapping. The public processed product **does not** contain those native flags. Per-publisher 1.5 m range label and 2 m first-cell-centre literature interpretation conflict; do not map the range cells to certified elevation above seabed.
- Downloaded source archives **already exist** in GitHub Actions acquisition [#39484948868](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39484948868), external to Git, with both original processed HDF5-backed NetCDFs and signed-by-checksum manifest. Source current SHA-256: `be8acb1802786a0db7f5c2952e4554fc25f03508550b7478a19a2f47d86864e2`, companion wave SHA-256: `d538b46f4b702382386721a43d39ec253f281f48522a377bf456b5d3373001ee`; source licence CC BY 4.0 (attribute FORCE/CIOOS Atlantic). Not original raw AD2CP.
- Generated `scripts/export_force_inflow_v0.py` records one row per **5,265 times × 50 instrument-relative range cells = 263,250 records**, UTC, ENU m/s, transducer range m, pressure dbar and explicit mutually exclusive numeric quality state. It writes a gzip file **outside Git** and source/checksum/count manifest committed as `research/observations/FORCE_INFLOW_V0_MANIFEST_2018.json`. The original values are retained **only** in unapproved measurement columns; suspect zeros / terminal screen have blanks, not misleading 0 m/s current.
- Of these, **165,323** nonzero records have `PENDING_NATIVE_QC_AND_GEOMETRY`, **93,427** are `SUSPECT_EXACT_ZERO_ALL_COMPONENTS`, and **4,500** fall under `SUSPECT_LOW_PRESSURE_TRANSITION` (pressure below **analyst-chosen** 20 dbar threshold; this does *not* mean FORCE approved that threshold or that the instrument was definitely retrieved). The 4,500 includes all cell-time records from 90 terminal times, regardless of whether individual values were zero. This partitions all 263,250 observations, rather than overlapping counts; approximately **97,911** raw zeros remain a separate source diagnostic.
- `model_eligible=0` for every output row, `model_eligible_rows=0` and `science_approved_cells=0` in the manifest. No selected depth subset is represented as valid because native quality, zero conversion, vertical datum and near-surface/near-bed masks remain unverified. No representative inflow-product claim, site-specific power, annual resource or extreme event can be made.

### Native file discovery and access gate

The CIOOS [current metadata](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html) and [wave metadata](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Waves/index.html) state that native `*.ad2cp` forms exist. The CIOOS discovery listing links the [FORCE native-data archive](https://data.fundyforce.ca/forceCloud/index.php/s/TAEz9gwARDDXCTD?path=%2F) and [metadata archive](https://data.fundyforce.ca/forceCloud/index.php/s/85etc2wCZt7K9FA). Both returned **HTTP 500 on public HEAD requests** in the bounded Github Actions run [#39495696237](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39495696237). This is a confirmed *access blocker*, not proof the files do not exist or that they are unusable. Do not impersonate access, automate contacts, assert native QC, or infer the instrument's data transformation rules from generic Nortek documentation.

## 2. Independent Nova Scotia station: CMAR Digby County, Long Beach

Acquired independently from [CMAR's Digby County Wave Data](https://cioosatlantic.ca/erddap/info/7iig-p4yk/index.html), specifically deployment **DG013** near **Long Beach, St. Marys Bay**, **44.40473°N, −66.1627°**. Source licence **Nova Scotia Open Government Licence**, attribute CMAR. [One-shot acquisition #39496314263](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39496314263), source artifact ID `12298006905` (temporary retention, **not a permanent data mirror**). Original exact selection is in `research/observations/CMAR_DIGBY_DG013_2022_QA.json`, CSV **60,480 bytes** SHA-256 `27bd18b64f2c71fb1502a663ede62f1d04b47a019dbb2fc5191190e028493ee8`.

- **531** publisher-reported time series observations between **2022-09-13 16:00 UTC and 2022-11-19 01:00 UTC**. 529 three-hour intervals, one six-hour gap.
- Variables include sea-water **sensor** speed and direction, significant wave height, reported instrument depth below surface, station coordinates/time and publisher's per-variable **gross-range quality flags**. All four selected variables have **531 flags `Pass`**, meaning they passed a publisher's *gross-range* outlier screen, **not native beam/velocity/pressure/rotation QC**.
- Observed source numerical range: speed **0.011–0.473 m/s**, sample arithmetic mean **~0.192 m/s**; significant wave height **0–1.6 m**, mean **~0.384 m**. These are descriptive statistics at this station in this period, **not grid/turbine resource**, another FORCE validation observation, or annual extremes.
- `scripts/process_cmar_dg013.py` produces `research/observations/CMAR_DIGBY_DG013_2022_QA.csv` annotated with gross-range scope and model eligibility zero; and `CMAR_DIGBY_DG013_2022_QA.json` with pinned source hash, counts/intervals and attribution. This product is not a 3D rotor-swept current profile and **must never be merged positionally with FORCE**.

## 3. Reproduction, stop conditions, and acceptance tests

For a local science installation, install 
`pip install -r requirements-ocean.txt` 
and use **separate** original source ZIPs (not committed):

```sh
python scripts/export_force_inflow_v0.py --archive force-spring2018-complete-processed-netcdf.zip --out data/local/force-inflow-v0
python scripts/process_cmar_dg013.py --archive cmar-digby-dg013-measured-wave-current-2022.zip --out data/local/cmar-dg013
python scripts/check_ingestion_reports.py
python -m unittest discover -s tests -p 'test_ingestion_gates.py' -v
```

`check_ingestion_reports.py` fails on altered source/derived SHA, missing FORCE per-cell flags, unexpected source-observation counts, or any prematurely model-eligible record. The manifests/CMAR compact derived CSV can be reviewed without raw third-party archive access. The gzip FORCE matrix is intentionally not committed to ordinary Git history; its logical CSV SHA is recorded for exact reproduction.

**Status and blockers:** source byte provenance **verified**; numerical and publisher gross-range QA **recorded**; native FORCE beam data/masks/tilt/heading **not obtained**; CMAR 3D current profile **not obtained**; hence **0 physically qualified turbine inflow observations**. Steps to advance: obtain licensed native AD2CP and deployment sheets and documented conversion/masks; adjudicate range-cell geometry and invalid bins with source-specific evidence; collect independent current-profile deployments and longer qualified coverage; only then design rotor swept-area velocity aggregation and validate energy/load predictions against independent experiments.
