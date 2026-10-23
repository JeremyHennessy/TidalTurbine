# TT-FIELD-SUBSET-02 — paper-reported late-November ADV/strain/thrust subset

**Research status: bounded additional publication evidence, not original measured sensor acquisition.**
Reviewed on 23 October 2026 against repository `c7345521baafe8865a206391a9446b96a90f9e36`. All user no-contact, no-purchase, no-field and no-source-bypass restrictions remain active. The verified baseline includes **zero original 2022 sensor archives, zero READMEs, zero independently qualified sensor UTC intervals and zero validated blade-fatigue or net electrical results**.

## Specific new evidence from the 2025 primary publication

The [Renewable Energy paper preview](https://www.sciencedirect.com/science/article/abs/pii/S0960148124020457) for Bichanich et al. (2025, DOI [10.1016/j.renene.2024.121977](https://doi.org/10.1016/j.renene.2024.121977)) now exposes a *Results and discussion* excerpt beyond the previously inspected abstract. It states that its analysed measurements were taken during **an ebb tide in late November 2022**, when **upstream and downstream ADVs**, **thrust load cells** and **strain sensors** were operating, and that their measurements were **successfully synchronized by the authors**. It also states that the **upstream ADCP suffered leak damage and its data could not be recovered** for the described investigation.

The accessible excerpt does **not** disclose the exact UTC date/time, original time-series sample records, calibrated strain or load uncertainty, the full physical synchronizer procedure or the original instrument operating schedule. The paper abstract separately reports electrical output being recorded during the study, but the publicly accessible *Results* excerpt **does not establish** that the original Voltsys electrical samples were usable in this particular late-November synced subset. Do not infer missing simultaneous electricity simply because both signals were used somewhere in the wider campaign.

**Resulting practical prioritization:** When original lawful source files eventually become available, inspect **ADV+strain+thrust** from the paper's analysed late-November ebb case as a *candidate partial mechanical/flow study* first. Treat the upstream ADCP as **author-reported unrecoverable in that event** rather than a default chosen upstream velocity source; other ADCP files should not be ruled out universally without instrument-specific records. Examine rectifier meter timebase and signed auxiliary boundary independently before attempting any four-family strain/flow/thrust/power claim. No exact time window has been selected.

## Independent reason not to invent source alignment

The public abstract/highlights of [Strain gauge measurements on a full scale tidal turbine blade (2021)](https://www.sciencedirect.com/science/article/pii/S0960148121001506) discuss clock skew in physically separate sensor systems and describe cross-correlation to recover alignment for that **different** turbine study. They also caution that high-frequency blade-strain components are not necessarily visible in more averaged thrust/torque records.

This is a **methodological warning, not a measured 2022 offset**. If clocks ever need retrospective alignment in the 2022 data, offset methods, max error, calibration and train/test leakage checks must be registered before evaluating load/energy effects. No arbitrary phase shift, fitted delay, sample-rate convention or interpolation is accepted.

## Reproducible source-state model and TidalLab display

The new `publisher_reported_case` object in both [original source-access register](../research/UNH_2022_SOURCE_ACCESS_001.json) and [Research viewer's source-limited registry](../research/field_strain_evidence_20261023.json) distinguishes **author-described partially synchronized measurements** from **independently reviewed original time series**. It retains exact UTC start/end as null, electric coincidence as UNKNOWN, one damaged source instrument as a case-specific negative finding, and scientific source acceptance as FALSE. The original checker and UI must reject any mutation that promotes a paper preview into four-stream native-clock qualification.

The existing TidalLab Research panel may display a small *publication-reported subset* note with its own source link and uncertainty. The original 12 source channels, three comparison papers, all artwork/designs, existing historical RM1/RM2/SIM reports, the UNH no-originals status, and the 2018 FORCE QA blockage must remain unchanged. Any rendered notes must not be framed as a qualifying measured experimental interval.

**No one was contacted; no emails, purchases, downloads of blocked sources or fieldwork.**

## Next decisions

1. Seek source-original ADV, strain, thrust and applicable test-log/clock calibration through restored normal public access or already legally held material; do not bypass previous HTTP 429 or guess the exact November tide.
2. Before interpreting source readings, independently validate native QC, geometry, offsets and precise source electric boundaries. Electrical coincidence in the reported partial subset stays UNKNOWN.
3. Compare load/energy hypotheses only with preregistered matched observations, material-specific cyclic stress metrics and **independent** physical replicates; keep Nova Scotia FORCE native-QC, ecology, rights and permits separate.
