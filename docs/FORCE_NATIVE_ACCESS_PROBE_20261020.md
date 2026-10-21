# TT-NATIVE-QC-ACCESS-01 — bounded read-only FORCE native archive check

**Checked 2026-10-21 00:02 UTC** (2026-10-20 Atlantic local), using [one-shot GitHub Actions 39518864052](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39518864052). This is a transport/access check, **not source-byte acquisition, beam-quality recovery, sensor calibration, site-resource qualification or a turbine-model run**.

## What was directly verified

The publicly advertised [FORCE native-data share](https://data.fundyforce.ca/forceCloud/index.php/s/TAEz9gwARDDXCTD?path=%2F) and [corresponding metadata share](https://data.fundyforce.ca/forceCloud/index.php/s/85etc2wCZt7K9FA) were checked using the standard-library `scripts/probe_force_native_access.py --probe` in a clean GitHub-hosted runtime. The tool made four concurrent **read-only HTTP GET** requests with Range `bytes=0-127`, a 12-second timeout, same-host redirect restriction, read-at-most-128-byte body and immediate close. The two public listing URLs and their conventional Nextcloud `/download` endpoints **all returned HTTP 500**.

| Public access path | Method | Observed HTTP status | Original contents acquired? |
|---|---|---:|---|
| Native archive public share index | Bounded GET | 500 | No |
| Native archive share download route | Bounded GET | 500 | No |
| Deployment metadata share index | Bounded GET | 500 | No |
| Metadata share download route | Bounded GET | 500 | No |

The preceding [GitHub Actions 39495696237](https://github.com/JeremyHennessy/TidalTurbine/actions/runs/39495696237) recorded **HEAD HTTP 500** for the public links. The new GET check demonstrates that simply switching to GET or the documented share download route does **not** presently resolve access from the GitHub runner. External web tools were also unable to open the share pages. This is an **observed public-access HTTP server error**, not proof the original Nortek files are lost or were never recorded. **No login bypass, crawling of private paths, contact, file download or artificial raw reconstruction was attempted.**

## Sources needed and strict scientific decision

The user-public [Nortek Signature recorder file reference](https://support.nortekgroup.com/hc/en-us/articles/27060689928348-Data-files) distinguishes the **single-ping .ad2cp** file, optionally **averaged _avgd.ad2cp** file with instrument QC, and **.deploy/.hdr/.cfg** records. A complete 2018 instrument-specific package for **Signature 500 serial 100258**, exact deployment intervals, tilt/heading/magnetic-frame processing, quality/correlation/percent-good/echo, fill/zero conversion and source file format lineage is needed. The 2022 FORCE/CIOOS processed NetCDF pipeline **does not contain those native QC fields**. The processed source 1.5-m range label versus independently published 2-m first-cell centre remains an unresolved geometry conflict.

Separate 2023 [Naberezhnykh et al. open-access turbulence study](https://doi.org/10.3390/en16041881) examined other FORCE/EMEC campaigns and showed that default shear/spectra/coherence assumptions depart from measured site conditions; its underlying third-party data are explicitly **restricted**. Its FORCE 2022/2018 campaigns **cannot be silently substituted** for 2018 FAST3 serial 100258 native beam QC or the first-cell mapping.

Current state remains **0 scientifically source-approved FORCE inflow rows / 0 qualified rotor-depth time series**, despite 263,250 numerically classified source observations. The independent CMAR DG013 531 source readings passed only publisher gross-range QC and are not a 3-D turbine-swept current profile.

## Safe continuation

1. Preserve this failed-access evidence and wait for a public, authorized native-source path or explicit user-approved publisher/regulator outreach. No automated mass retries or speculative fill/tilt corrections.
2. If authoritative source files become accessible, **first** checksum the acquired byte stream, record licensing/metadata and identify exact original `.ad2cp/.deploy` geometry and source processing. Independently compare native beam flags to publisher processed vectors and clarify the 1.5 vs 2 m range mapping. Exclude all invalid/sidelobe/above-surface/retrieval bursts.
3. Validate the proposed mask on a holdout interval and preferably an independent campaign; only then review a new `QUALIFIED_INFLOW_V1` with per-cell source QCs, site/time/vertical references, coverage, uncertainty and predeclared stop conditions. Keep model eligibility **zero** until an explicit scientifically reviewed, independently checked acceptance. No annual energy, structural loads or field suitability can be asserted from data access alone.

This note records a reproducible negative result, not a repaired server or completed scientific QC.
