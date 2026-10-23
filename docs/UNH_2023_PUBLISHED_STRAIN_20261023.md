# TT-UNH-STRAIN-OMAE2023 — eight actual *published* gauge statistics, not raw source strain

**Audit dated 2026-10-23. Published external experiment (2022-11-22), NOT a project device or laboratory test.** Source: Bharath et al., [*Open Water Blade Strain Measurements on a Vertical-Axis Tidal Turbine* (OMAE2023-101076)](https://tethys-engineering.pnnl.gov/sites/default/files/publications/Bharath_et_al_2023.pdf), a publicly accessible 10-page NREL/UNH conference article. Article text was extracted and inspected for table/sections; the PDF screenshot renderer was unavailable, so the extracted Table 1 numeric units could **not** be independently visually verified. No protected raw data, strain unit, sample timestamps or instrument calibration has been inferred. Machine-readable reproduction: [research/UNH_2023_PUBLISHED_STRAIN_001.json](../research/UNH_2023_PUBLISHED_STRAIN_001.json); read-only validator: [scripts/check_unh_2023_strain.py](../scripts/check_unh_2023_strain.py).

## What is genuinely new

The 2023 paper's **section 4.1, Table 1 (PDF page 8, zero-based index 7)** expressly identifies one real reported **22 November 2022** operating example and eight distinct strain gauges arranged down a blade between and beyond two struts. This is a better date anchor than the vague "late November" in the public preview of the *different later* [2025 Renewable Energy paper](https://www.sciencedirect.com/science/article/abs/pii/S0960148124020457). Crucially, **we have not established those are the same exact analyzed tidal interval**.

Here is the published *per-revolution peak-to-trough strain-difference statistic* table, transcribed from the searchable paper text. **The numerical Table 1 unit was not confirmed in the PDF text extract; therefore the values below are displayed as printed, without assuming they are microstrain (µε), pascals or a material fatigue law.** Do not interpret mean peak-to-trough differences as original raw-strain peaks or as material cycles.

| Gauge (top→bottom) | Position on blade | Mean | Max | Min | Standard deviation |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | Above upper strut | 8.1 | 12.1 | 4.3 | 1.1 |
| 2 | Above upper strut | 37.1 | 118.3 | 21.7 | 5.7 |
| **3** | **Near upper strut** | **86.8** | **120.8** | **51.0** | **11.4** |
| 4 | Between struts | 55.6 | 91.3 | 24.2 | 10.8 |
| 5 | Between struts | 21.5 | 37.3 | 9.7 | 4.5 |
| 6 | Between struts | 35.7 | 63.3 | 17.8 | 7.0 |
| **7** | **Near lower strut** | **69.7** | **100.1** | **40.6** | **8.0** |
| 8 | Below lower strut | 6.3 | 10.1 | 4.1 | 0.7 |

**Observed paper-specific pattern:** gauges 3 and 7 near the two struts show the two highest mean peak-to-trough differences. This makes local root/strut bending a sensible **hypothesis for instrumentation placement** in a future independent design, not an adopted rotor geometry or proof that support drag is a fatigue measure. The paper cautions that gauge placement, spanwise loading, and inflow nonuniformity require separate consideration. The table reports processed statistics; no sample count, common-clock source slices, source-native QC, applied-load calibration or strain-to-stress transfer has been independently acquired.

## Hardware and clock lesson from the same 2023 paper

The studied **different** turbine used a four-blade, 3.2m diameter, 1.7m high rotor (NACA 0021, 0.25m chord), with one blade fitted with eight bridge strain gauges. NREL/UNH describes two wireless V-LINK-200 nodes feeding WSDA-2000 and NI cRIO/MODAQ, and a GPS-based common time source at the main system. **After networking problems, ADCP and CTD records ran separately from MODAQ**: their clocks were preset against a reliable source and drift estimated. That is not physical common-clock proof for native unrecovered ADCP source files. The installed ADV probes were deliberately near the swept rotor and subject to turbine-induced deceleration, **not unmodified ambient/free-stream measurements**. At least one upstream ADV support pipe was damaged on November 27 and subsequently removed December 8, further changing availability. Nothing here licenses a date/time guess or a Nov22-to-Nov27 timing correction.

**Electrical boundary warning — especially important:** the paper explicitly describes using **off-grid operation** for the instrumented blade, with the rectifier controlling generator shaft load into a nominal 25kW resistor/dump bank instead of sending electricity to the grid. The published **1-second-averaged** turbine power figures therefore do not establish **net exported electricity after auxiliary draw**, and cannot resolve the turbine's individual blade-passage power variation or correlate it at raw strain sample frequency. Treat all control/battery/auxiliary and meter placements as independent unknowns, not benign losses that can be assumed away.

The paper separately reports **18–31rpm** and a turbine-wide thrust **mean around 6.4kN** and peaks up to **11.5kN**, described for the study/deployment, **not** as statistically matched values for the 22 November Table 1 strain sample. We must not pair these different summary figures into a fabricated strain-force-power observation.

### Simple, explicitly model-derived bandwidth warning

For four blades and a **hypothetical constant** speed corresponding to the reported 18–31rpm range, a nominal blade-passage frequency is (4\times\mathrm{rpm}/60\), about **1.2–2.07Hz**. This is only a dimensional identity using reported campaign-level rotor speeds; **not a measured frequency spectrum or sensor bandwidth selection**. Since electrical samples are reported as 1-second averages, the publication-level electrical series alone is insufficient to resolve each individual blade passage. This does not demonstrate the actual sampling or anti-alias capabilities of unrecovered native data.

## What this means for our prototype comparison

**Do not** reuse the external turbine's 3.2m rotor, NACA profile, strain units, fatigue coefficients, generator output, stress-transfer constants, support ratings, structural sensor ranges, 100Hz load-cell limits, or bearing/mast design as qualified *our* prototype specs. A research-lab pilot should explicitly measure strain near critical strut/blade interfaces, independent structural loads, 3D flow away from rotor induction plus local flow, phase/encoder zero, common-clock delays, and **two clear electrical boundaries** (generator/rectifier versus delivered load/grid, with controllers and auxiliaries separately accounted).

Original 2022 data ZIPs and READMEs on MHKDR remain inaccessible after ordinary HTTP429 and **zero source-native samples have been acquired**. The published table and previous author-reported late-November partial synchronized subset are additional literature evidence, not a scientific replacement for raw files, clocks, QC, a genuine source interval or independent predictive validation. The FORCE ocean 2018 site remains separately unqualified. No physical test, field experiment, outside contact, product purchase, authorization or fatigue-life claim occurs in this research pass.

**Next three research tasks:** (1) later obtain legitimate original 2022 strain/ADV/thrust/power READMEs and source clock/QC only through ordinary accessible routes, without rate-limit bypass; (2) prespecify which locations, filter spectra, source time boundaries and uncertainty distinguish strut stress from mean drag, with separate dump-load versus net-export accounting; (3) choose independent replicates and a controlled laboratory apparatus only after a qualified professional safety/measurement review. No lab or field authorization is implied.

Reproduce this *publication-transcription audit* offline: `python scripts/check_unh_2023_strain.py` and `python -m unittest discover -s tests -p test_unh_2023_strain.py -v`. Passing means the published-table numbers and evidence boundaries are reproducible, **not** that the turbine experiment was independently repeated.
