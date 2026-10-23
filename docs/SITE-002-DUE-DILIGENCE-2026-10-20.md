# SITE-002 — Halifax-accessible tidal project: parcel, resource and two-path feasibility screen

**Research date:** 2026-10-20. **Scope:** independent follow-up to `SITE-001`, focused on land and marine testing around Parrsboro/West Bay, Minas Passage/FORCE and Noel Bay. **Research only:** No offer, site visit, direct contact, zoning confirmation, physical survey, vessel charter or permit application has been made. **The turbine's synthetic experiment and its previously approved baseline are unchanged.**

**Evidence vocabulary:** `PUBLIC_PRIMARY` official government/provider data; `PUBLISHED_ANALYSIS` study findings subject to its conditions; `LISTING_CLAIM` property advertiser information, not registry/title verification; `ENGINEERING_HYPOTHESIS` assumption requiring measurement/design; `BLOCKED` verification not possible from reviewed public sources.

## 1. Tidal-current evidence and spatial comparison — partially achieved

### Newly established measured dataset and data-availability gate
- `PUBLIC_PRIMARY / metadata only`: FORCE March–May 2018 seabed ADCP 3D currents at **45.3631 N, -64.4275 W**, recorded **2018-03-30 to 2018-05-24 UTC**, with east/north/up velocity components (m/s), pressure and range cells **1.5–50.5 m *from instrument*, not water depths**. Public CIOOS Atlantic ERDDAP metadata describes **CC BY 4.0**. Upstream metadata: https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html . Corresponding waves: https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Waves/index.html .
- Active repository **PR #6** (`f72ea1eb9625137b8562dbe48809bde100dc335c` when reviewed) already registers this and nineteen additional ocean-source discovery entries, and offers a **dry-run default** download/hash script in `scripts/acquire_force_adcp.py`. This SITE-002 update **does not duplicate those files, merge that PR, or claim raw acquisition**. PR: https://github.com/JeremyHennessy/TidalTurbine/pull/6 .
- `BLOCKED`: NetCDF **raw numeric observations were not acquired, parsed, QC'd or ingested in this pass**. A trial network retrieval via this workspace failed DNS access, and the GitHub public reader cannot fetch non-UTF-8 binaries. Consequently, numeric measured speed percentiles, energy-yield ratios or depth/ebbflood comparisons cannot be generated defensibly. ERDDAP variable-attribute extrema are **not** rotor-height speeds.
- `PUBLISHED_ANALYSIS`: Karsten, Roc, Culina, O'Flaherty-Sproul and Trowse (2017), *High-resolution numerical model resource assessment of Minas Passage*, published by FORCE, compared regional FVCOM model predictions to data from **26 ADCP deployments (2008–2016)**. It reports pronounced local variation, differing ebb/flood resource and features near Black Rock and Cape Split. Its high-resolution model had approximately **20 m** grid spacing near FORCE. It reports **up to ~25% changes in *mean power density* over a model grid-scale (~20 m)**; do **not** interpret this as observed velocity or device performance for any listed land parcel. It also reports model speed bias/NRMSE and larger *power-density* errors (power-density NRMSE broadly 20–30% in its validation discussion). Report: https://fundyforce.ca/document-collection/high-resolution-numerical-model-resource-assessment-of-minas-passage-bay-of-fundy .
- Study coverage was asymmetric: its authors report **no ADCP observations in the southern portion of Minas Passage** in the 2008–2016 validation inventory, which reinforces the need for careful transfer assumptions when comparing shore sites.

### Explicit micro-area screening (no fabricated velocity values)
| Micro-area | Source-backed status | Depth-specific measured velocity at candidate lot? | Decision |
|---|---|---|---|
| FORCE northern corridor, offshore Black Rock | 2018 ADCP dataset coordinates published; 2017 model cross-checked with numerous ADCP sites | **No — raw 2018 file not QC'd; land parcel is not the deployment** | **First acquisition/QA location**; resource benchmark only, subject to berth authorization |
| South-side Minas Passage / Cape Split | 2017 modeled high variability and flow features; historical coverage gap | **No** | Alternative after independent measurements and access review; no property ranking |
| West Bay shore near advertised Bay Bluff lots | Listing water views; FORCE region nearby at regional scale | **No** | Upland base possibility only; no basis to assume offshore rotor flow from a lot |
| Noel / Cobequid Bay shore | Waterfront listing and regional tide data candidates only | **No** | Monitor flood/sediment/water levels; do not claim suitable submerged rotor conditions |

**Reproducible next test:** After PR #6's acquisition script is available, download publicly reusable original files into ignored `data/raw`, record source URL, retrieval UTC, exact bytes, SHA-256, licence and transducer metadata. Validate time axis, coordinate vector rotation, orientation, fill/quality flags and bins, and stratify *flood vs ebb* at stated height and dates. Validate 2017 model comparison at *coincident time/position/depth* only if its numerical output and pairing metadata are obtained. Compute speed percentiles and `mean(|u|^3)` (not `mean(|u|)^3`), then explicitly state the short spring campaign's insufficiency for annual yield, turbulence, extreme loads or full-season availability. No changes to `SCREEN-001` without separately reviewed data provenance and a tested measured-data model.

Bathymetry sources: CHS NONNA non-navigational 10/100m raster https://open.canada.ca/data/en/dataset/d3881c4c-650d-4070-bf9b-1e00aabf0a1d ; GEBCO 2026 grid https://www.gebco.net/data-products/gridded-bathymetry-data . Neither has yet been clipped, georeferenced to exact parcels, datum-verified or surveyed. Thus no defensible shore access, cable route or rotor clearance can be concluded.

## 2. Exact publicly advertised parcel identifiers / covenants / zoning — partly achieved

Listing pages below provide **MLS-advertised PIDs**, not certified title identifiers. See companion `research/site-002-property-gates.csv` for machine-readable status.

| Site | Advertised PID | MLS | Ask CAD | Evidence and decision gate |
|---|---|---|---:|---|
| Bay Bluff **Lot 2** | **25514878** | 202528000 | **$30,000** | `LISTING_CLAIM` 1.76 ac ocean view; **protective covenants**; electrical power at lot line claimed in text but details say **“Utilities: None”**. No well/septic. Workshop use **unverified**. |
| Bay Bluff **Lot 3** | **25514886** | 202528002 | **$30,000** | Same type of restrictive covenants and power text-vs-field discrepancy; no well/septic. Not confirmed superior to Lot 2. |
| Bay Bluff **Lot 6** | **25514910** | 202528005 | **$75,000** | Drilled well and garage advertised. Royal LePage explicitly lists **Land Survey and Restrictive Covenants as documents on file**; originals **not inspected**. Workshop, garage permit and electrical service **unverified**. |
| **Diligent River Hwy 209** | **25376526** | 202607350 | **$49,900** | 13.3-acre upland option; advertised electricity/telephone but no water/septic. **Important: SITE-001 displayed $39,900, direct current REMAX listing displays $49,900**; do not carry forward older price. |
| **Noel Lot 3a Hwy 215** | **45347440** | 202608832 | **$50,000** | ~0.80 ac and ~126 ft waterfront advertised. Listing calls zoning **RU-2**, but no independent zoning/PID-specific municipal confirmation. It advertises electricity/high-speed internet “to be verified.” |
| **West Bay Road Lot 03-1** | **25450644** | 202520692 | **$169,000** | 26.81-ac **cliff-front** oceanfront listing; no water/septic/utilities; direct listing $169,000 versus cached older $159,900. Not cleared for cable landing. |

**Direct listing sources:** Lot 2 https://www.remaxnova.com/vacant-land/west-bay-real-estate/lot-2-bay-bluff-road-west-bay-mls-202528000 ; Lot 3 https://www.remaxnova.com/vacant-land/west-bay-real-estate/lot-3-bay-bluff-road-west-bay-mls-202528002 ; Lot 6 https://www.royallepage.ca/en/property/nova-scotia/west-bay/lot-6-bay-bluff-road/26757521/mls202528005/ ; Diligent River https://www.remaxnova.com/vacant-land/diligent-river-real-estate/highway-209-diligent-river-mls-202607350 ; Noel https://www.remaxnova.com/vacant-land/noel-real-estate/lot-3a-highway-215-noel-mls-202608832 ; West Bay https://www.remaxnova.com/vacant-land/west-bay-real-estate/lot-03-1-west-bay-road-west-bay-mls-202520692 .

`BLOCKED`: Exact registered covenants, deed/survey, easements, legal subdivision road rights and zoning for the West Bay PIDs were **not publicly verified**. Official Cumberland [zoning map](https://www.plancumberland.ca/zoning-map) is an embedded, interactive GIS service requiring parcel selection; published [land-use definitions](https://www.cumberlandcounty.ns.ca/land-use-regulations.html) distinguish residential, rural resource and industrial classes. None can be inferred merely from “rural” or “ocean view.” Nova Scotia [Property Online](https://www.novascotia.ca/sign-property-online) / registered restrictive covenant is the appropriate title-document route, possibly requiring access or professional review. Local permissions for land workshop, storage, equipment shed, research instrumentation, discharge, electrical load and year-round vehicle access must be checked in writing before commitment. **No municipality, property owner, utility or seller was contacted.**

**Important finding outside the earlier property screen:** Cumberland [By-law 26-11 adoption notice](https://cumberlandcounty.ns.ca/public-hearing-and-notices/), adopted Sept 23 and published Sept 29 2026, describes a **temporary pause on accepting applications for AI data-centre development permits** during plan review. An instrument workshop is not demonstrated to fall within that ban, but **do not treat a potential future data-centre use as approved**.

## 3. Noel waterfront vs West Bay cliff — completed desk-level hazard/rights gates, NOT an engineered assessment

| Criterion | Noel Lot 3a | West Bay Lot 03-1 | Consequence |
|---|---|---|---|
| Coastal frontage | ~126 ft Noel Bay claimed | Oceanfront cliff explicitly described | **Different shore types**; no usable landing verified |
| Indicative hazard | `ENGINEERING_HYPOTHESIS` shallow intertidal sediment, exposure and flood at Noel Bay; **parcel specifics unknown** | `LISTING_CLAIM` cliff elevation; `ENGINEERING_HYPOTHESIS` stability, erosion, safe lifting and cable route | Require site geotechnical, tidal datum / sediment and slope/erosion studies |
| Survey/title | “surveyed” claimed, actual survey not read | survey/title not read | Do not rely on boundary/flood elevations |
| Rotor current / low-tide depth | **Unknown** | **Unknown** | Neither qualifies as water turbine site |
| Coastal mapping | [NS coastal hazard map](https://nsgi.novascotia.ca/chm) available; no PID-specific overlay completed | Same | Public map is preliminary screening only |
| Site-specific government hazard report | [Province offers free Coastal Hazard Assessment Report](https://novascotia.ca/coastal-climate-change/request-coastal-hazard-assessment-report/) for any parcel | Same | **No report was requested** (requires user-approved external contact) |
| Marine rights | [Province controls most submerged coastal land from mean high-water mark](https://novascotia.ca/natr/land/submerged-land.asp); leases/permits for tidal generation, cable landings and structures | Same | Neither owning waterfront nor deeded beach access conveys marine turbine authorization |
| Grid, fibre, construction | Advertised electricity/Internet only, “to be verified” | No utilities advertised | Quote and interconnect studies pending |

**Decision:** Noel is the less expensive *waterfront monitoring/instrument* question but does not have verified submerged rotor clearance; cliff-front West Bay is a poor **first** purchase candidate until an independent safe landing and shore erosion screen has been completed. This is *risk-ranked, not a quantified geotechnical finding*. Do not order a coastal hazard report, submit a form, request zoning determinations or engage sellers unless the user separately authorizes external contact.

## 4. Dual-track economics — cost structure established, not a market-quote NPV

**Scenario A — Upland lab base + access through an existing authorized marine operator:** illustration uses **Bay Bluff Lot 2 $30,000 advertised** and a *hypothetical* hosted/leased permitted berth. Neither parcel usability nor berth access is assured. Could substitute Diligent River $49,900 if fewer residential restrictions after verification.

**Scenario B — Own shoreline base + independently authorized deployment:** illustration uses **cliff-front West Bay Road Lot 03-1 $169,000 advertised**, a *hypothetical* new marine rights package, own safe marine landing/cable/mobilization. This is NOT licensed; there is no assumption that the cliff lot can obtain a safe landing or berth.

**Known, like-for-like *asking-price-only* difference:** **B costs $139,000 more in advertised land price** (`169000 - 30000`), before acquisition tax, legal, foundation, equipment, shore works, permits, grid, vessel, insurance, monitoring, operations or teardown. This alone does *not* prove A lower total lifecycle cost. Using Diligent River as A changes only the land-price component to a **$119,100** difference.

**External cost evidence:**
- Official **Marine Renewable-energy Fees Regulations** (2024 consolidated) lists a **$2,000 demonstration-permit application** under clause 35(1)(c) and **$2,500 licence application** (different routes; verify applicable legal treatment). These are *application fees, not project permitting/monitoring budgets*: https://novascotia.ca/just/regulations/regs/mrefees.htm .
- The **2025 tidal procurement documents** say **FORCE berth fee schedule is released only to registered applicants subject to an NDA**; no public berth rent, vessel or interconnection price was obtainable from those materials: https://nstidalprocurement2025.com/nova-scotia-tidal-procurement-updates/ . An existing berth is **not free or automatically available**.
- The separate **2026 demonstration-permit window** is stated on the current provincial program page as **Aug 7–Oct 30 2026 11:59pm**, **<2 MW/project**, **up to 7.7 MW total**, and **outside the FORCE marine renewable-electricity area**. The July 31 provincial news release gave **Sep 30** as a deadline, so it appears the live program page updated the date; reconfirm if applying. No application was made: https://novascotia.ca/programs/tidal-demonstration-permit/ .
- The Province says submerged Crown land leases for tidal generation and utility cable landings use **market-value-based rent** and possible easements. No quoted amount applies to these plots: https://novascotia.ca/natr/land/submerged-land.asp .

**Decision test (values require actual quotes):**

Let `shared` = device engineering, instruments, manufacturing, validated tests and common O&M that apply regardless of site.
```
A_total = $30,000 + A_acquisition_close + A_build_and_utilities + A_host_berth_access
        + A_marine_vessel + A_cabling_or_telemetry + A_specific_legal_environmental
        + A_annual_O&M_NPV + A_decommission_NPV + shared
B_total = $169,000 + B_acquisition_close + B_build_and_utilities + B_new_marine_rights
        + B_own_landing_and_cable + B_marine_vessel + B_specific_legal_environmental
        + B_annual_O&M_NPV + B_decommission_NPV + shared
```
No NPV, electricity revenue, capacity factor or LCOE output is defensible until occupancy legality, actual site energy, berth access, meaningful tariffs, contract terms and developer-sized vessel/environmental quotes exist. **A is preferred for *next-stage due diligence*, not declared commercially cheaper or executable.** See `research/site-002-dual-track-cost-gates.csv` for the audit-ready list of missing quotes. A fixed permit fee is a small subset of the cost stack; it must never be substituted for environmental authorization.

## Priority actions for the next scientifically useful pass

1. **Finish marine data QA**: land PR #6 on a verified baseline when approved and green; obtain original March–May 2018 currents/waves, SHA256, metadata and quality masks, then benchmark at measured coordinates. **Do not compare land PIDs by synthetic flows.**
2. **Legal gate before purchasing anything**: obtain actual filed restrictive covenants and parcel-specific zoning for Bay Bluff **25514878 / 25514886 / 25514910**, garage/well permit status for Lot 6 and realistic Nova Scotia Power service quote; if denied for test-lab use, drop subdivision as candidate. A suitably zoned upland industrial space near Parrsboro may be preferable.
3. **Physical shore gate**: request (only with approval) free coastal hazard reports for Noel PID **45347440** and West Bay PID **25450644**, and obtain appropriate low-water, cliff stability, protected habitat and marine access engineering reconnaissance before any shore deal.
4. **Economic gate**: seek, only if authorized, whether FORCE or another permitted operator can host a *non-export research demonstrator*, and the associated contractual/insurance/environmental and vessel costs. Compare against a separate new-berth consent package; reject both if they lack lawful access.
5. **Separate the AI-centre location decision**: Cumberland's data-centre application pause requires monitoring. Do not treat a small tidal test base or the 2026 demonstration window as permission for AI infrastructure.

## Repository and verification note

- Baseline read during this pass: `main` **`45ca55c2ce8a2be08de7c0e331f660e5548343b0`**; PR #6 **open** when checked. No source, approved UI, historical `SCREEN-001`, simulator, measurement registry or existing test files modified by SITE-002.
- Research classification: `LISTING_CLAIM`, `PUBLISHED_ANALYSIS`, `PUBLIC_PRIMARY`, `ENGINEERING_HYPOTHESIS`, `BLOCKED`. No title instrument, verified zoning, parcel ocean data or published actual equipment quotation was obtained.
- Source reviewed: dates/URLs above. Listing values and official web pages can change; recheck before financial decision. The report is **not engineering, permitting, legal or surveying advice**.
