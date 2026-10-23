# UNH 2022 original sensor/clock overlap — access and eligibility findings
23 October 2026 · PUBLISHED_METADATA / UNKNOWN_OR_CONFLICT · Not a measured turbine finding

**Result: original data unavailable; scientifically qualified common intervals = 0.** Verified official [Data.gov dataset](https://catalog.data.gov/dataset/in-situ-blade-strain-measurements-of-a-crossflow-turbine-operating-in-a-tidal-flow), DOI [10.15473/2481243](https://doi.org/10.15473/2481243), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) licence. Publisher metadata lists 17 resources across 2022-10-25 through 2022-12-12, including eight blade strain gauges, ADCP/ADV velocities, reaction-arm thrust, Voltsys rectifier measurements and an IMU. **Seventeen catalogue links are not seventeen acquired/qualified time-series.** The broad campaign dates are not valid evidence of simultaneous sensor operation.

Source: [2022 resource/README access register](../research/UNH_2022_SOURCE_ACCESS_001.json), which stores original official `/files/569/` resource URLs, DOI, licence, access attempts and null source hashes/operating intervals. Standard bounded reads of original STRAIN, THRUST and VOLTSYS READMEs and the deployment-schedule PNG returned **HTTP 429**; the original ADCP README had likewise returned 429. Reads stopped without bypass, mirror, further retry, email, purchase or bulk request. Original archives acquired **0**, native READMEs acquired **0**, confirmed original sample timestamp counts **0**, qualified common windows **0**. Their absence prevents actual source/native QC, calibrations, clock/drift offsets, sample coverage, flow direction, load-path and meter-boundary validation.

**Do not conflate** the 2022 field campaign with the different 2021 MHKDR 394/492 turbine observations or the much smaller original 2015/2016 RM2 1:6 tow-tank experiment. Voltsys **rectifier** readings are not automatically signed net exported energy; eight strain-gauge channels are not automatically material-calibrated blade-root stress or a validated fatigue life.

## Deliverable — real-file eligibility without inventing measurements

The offline `scripts/qualify_unh_2022_overlap.py` has two explicit paths:

1. No arguments: verify the actual blocked source register and print `BLOCKED_NO_ORIGINAL_2022_SENSOR_FILES_OR_CLOCK_QC`; no physically qualified interval is inferred.
2. With a *separately obtained, lawful, bounded local* manifest: inspect actual local CSV records for **STRAIN**, **THRUST**, **VOLTSYS**, and exactly one of **FLOW_ADCP/FLOW_ADV**, using [the empty local template](../research/UNH_2022_LOCAL_CLIPS_TEMPLATE.json). Source ZIP/README/calibration/QC/clock/processing SHA-256 evidence fields, and flow-geometry and electric-meter-boundary evidence hashes, are required but not automatically authenticated. Source CSV bytes must match their own pinned SHA-256. A user must explicitly map timestamp, quality and measurement columns, SI units, allowable gaps and independently sourced clock uncertainties.

The checker uses exact **UTC offset-aware** time labels within the 2022 campaign and preserves source quality rejections and time gaps. It **never interpolates** missing samples, assumes 2021 and 2022 streams are interchangeable, or equates normal source time labels with a qualified common physical clock. It trims each stream's contiguous time segments by its declared clock error, intersects only those segments, and prints at most `LOCAL_TIMESTAMP_OVERLAP_CANDIDATES_REVIEW_REQUIRED` — **never a scientific acceptance verdict**. Source files must be local, relative, non-symlink, smaller than 8 MB and at most 100,000 rows per stream; the script does no network access and writes no files. A local manifest with false documentation hashes can **only** yield a provisional timing candidate; it can never prove scientific validity or authentic source calibration.

An independent reviewer must establish genuine source identities/document authenticity, native QC and units, actual clock offset/drift, instrument configuration and upstream flow geometry, blade/strut stress conversion, platform-motion compensation, and meter sign, rectifier location and separate auxiliary draw before examining a validated load-versus-net-electricity claim. The sample-duration filter is computational, **not a preregistered scientific acceptance tolerance**. Synthetic unittest fixtures intentionally supply dummy data and dummy evidence hashes to exercise validation, not to represent any UNH sample.

## Reproduce without any source downloads

```sh
python scripts/qualify_unh_2022_overlap.py
python -m unittest discover -s tests -p test_unh_2022_overlap.py -v
python -m unittest discover -s tests -v
```

After future independent lawful source acquisition only: `python scripts/qualify_unh_2022_overlap.py --manifest /path/to/private/local-clip-manifest.json`. Preserve raw files outside Git and retain every failure and negative result. A nonzero exit on invalid metadata is a **scientific stop gate**. An exit-0 blocked source-status audit does **not** mean a synchronized experiment.

**Next three gates:** (1) obtain original 2022 READMEs/schedule through ordinary restored access or lawful user-held copies without circumventing 429; (2) map one actual source-QC'd, clock/geometry/power-boundary-qualified interval and independently review it; (3) test calibrated blade stress against measured net electricity under preregistered repeated conditions. FORCE Nova Scotia field-current QA, environmental monitoring, Mi'kmaq/fisheries, maintenance, navigation and permits remain separate mandatory gates. **No external contact authorized.**
