# TT-FIELD-POWER-001: independent field-data eligibility review

Review time: 2026-10-21 13:55 UTC. Status: DISCOVERED_METADATA_ONLY; ELIGIBILITY_UNRESOLVED.

Evidence classes: PUBLISHED_EVIDENCE for publisher landing-page metadata; UNKNOWN_OR_CONFLICT for unresolved source eligibility. No raw samples were downloaded. This is not an acquired dataset, model input or physical test. No existing source results, application files or eligibility gates were modified.

## Verified project boundary

TidalTurbine main was bd24c6d86201801e28e8366406d4fe9bfafd7cc4 at the initial read. PR #25 merged the 14-design artwork refresh at 13:51 UTC. The illustration release is separate from this research record. Only open PR at review was separately owned #8 (historical parcel/site economics); do not incorporate or modify it. Current main preserves zero FORCE-approved inflow cells and independent RM1/RM2 limitations.

## New primary-source lead

Source: https://mhkdr.openei.org/submissions/394 ; DOI https://doi.org/10.15473/1973860 . Landing page read successfully. Its licence link resolves to https://creativecommons.org/licenses/by/4.0/ .

Publisher metadata describes 2021 UNH tidal-estuary observations of a modified EVG-025 cross-flow machine, not RM2 or a Nova Scotia turbine. Available channels include current profiles/point velocities, reaction-arm support loading, rotational speed, electrical meters and platform motion. It reports differing QC depth by instrument. Relevant advertised files: ADCP1_Stern.zip (11.56 MB), ADCP2_Bow.zip (10.97 MB), Load_Cell.zip (8.53 GB), Shark_Meter.zip (196.46 MB), and Voltsys.zip (128.74 MB). Advertised load-cell sampling is 100 Hz; Voltsys is mostly 1 Hz. The complete package is 25.44 GB and was not requested.

Companions linked by the source: ADCP #489, load cells #494, Shark electricity #492. The #492 landing page was readable and advertises original meter data and processing scripts: https://mhkdr.openei.org/submissions/492 . No companion bytes were acquired. This source is not in the inspected current research/catalogue.json.

## Access evidence and stopping condition

At approximately 13:54 UTC, ADCP_READ_ME.txt, LOAD_CELL_READ_ME.txt and VOLTSYS_READ_ME.txt returned HTTP 429 through the web tool. Retry-After was not exposed. After a cooldown exceeding 60 seconds, one bounded same-URL retry returned 429 for ADCP and Voltsys, and UnexpectedStatusCode for load cells. Dependent reads stopped; no alternate-domain or alternate-route rate-limit bypass was attempted.

SHARK_METER_READ_ME.txt returned unsupported application/octet-stream, not readable text, through the web tool. A bounded public curl fetch for that unsupported-content case returned an HTML Site Unavailable page, not the requested document. A later web read still reported unsupported content. No contents or successful transport were inferred from curl exit code zero.

Exact attempted source paths all use https://mhkdr.openei.org/files/394/ followed by ADCP_READ_ME.txt, LOAD_CELL_READ_ME.txt, SHARK_METER_READ_ME.txt or VOLTSYS_READ_ME.txt.

## Evidence needed before selecting a sample

These are proposed acceptance checks, not publisher facts or completed checks:

1. Read each instrument's original README and units file; record hashes, licence, calibration, data version, clock epoch, timezone, synchronization corrections, drift and missing-data encodings.
2. Establish actual common instrument availability from the source timeline and test log. Do not choose dates merely from broad campaign coverage.
3. Verify which ADCP is upstream for each flow direction, its coordinate transformation, cell heights, sidelobe/near-bed exclusion, valid-beam rules and motion treatment. Do not transfer these rules to FORCE.
4. Identify what the electrical measurement includes: generator-side versus grid-side, sign convention, import/export and auxiliary/control consumption. Do not label meter output complete net-system electricity without this reconciliation.
5. Establish support-load calibration and inertial/platform-motion effects. Never call reaction-arm loading blade-root strain, structural stress or fatigue damage.
6. Pin a short interval with concurrent accepted samples, preferably one stable operating period, before calculating results. Predeclare resampling, anti-aliasing, gap rejection and allowable clock uncertainty; no interpolation across invalid gaps. A precise UTC interval cannot yet be responsibly selected.

## Next legitimate access and decision gates

Do not repeatedly retry the blocked files or route around rate limits. Resume through the same public source only after a later permitted access window or a publisher-restored endpoint. Read the exact original instrument documents before selecting an acquisition interval. If a necessary source remains unavailable, retain UNKNOWN_OR_CONFLICT; any publisher outreach requires separate approval.

Keep this source classified as DISCOVERED_METADATA_ONLY, not downloaded, reprocessed or benchmark-ready. No numeric replacement for missing records is permitted. Do not acquire the complete 25.44 GB package by default. First scope a small, reproducible sample with source hashes and a documented reason for every required channel, then retain raw data outside Git.

This review does not close the independent RM1 validation, FORCE native-QC, blade-stress, ecological, maintenance, manufacturing, site-access or legal gates.
