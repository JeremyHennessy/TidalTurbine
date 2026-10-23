# TT-LAB-PILOT-01 — first physical proof-of-concept readiness (2026-10-23)

**Desk work product, not a hardware release, quotation, facility booking, permit, validated turbine or instruction to operate machinery.** Base reviewed: `4c40ca2547e741739259fdabbfa24049dcc75b7f`. This note documents checkable next decisions for a **small controlled tidal-stream-generator laboratory experiment**. It does not redesign or supersede approved TidalLab UI, published RM1/RM2 results, the source-gated FORCE work, or existing Concept003–006 studies.

Machine-readable source: [lab pilot gate register](../research/lab_pilot_readiness_20261023.json); fail-closed auditor: [read-only checker](../scripts/check_lab_pilot_readiness.py); research regression tests: [lab readiness tests](../tests/test_lab_pilot_readiness.py).

## Outcome and exact status

**Achieved now:** five external facility leads researched from published operator/university sources; one dated 2026 Canadian flume **list rate** discovered; all-in cost exclusions made explicit; updated October 2026 Nova Scotia permit guide deadline reconciled; a 15-gate executable readiness register tied to existing source records and tests.

**Still absent:** no source-approved FORCE rotor-height inflow, no qualified laboratory venue for this rig, no cost quote for this test, no signed operator acceptance, no calibrated blade stress/electricity data, no physical test or turbine winner documented by the repo. Current `research/shaft_support_006.json` has at least 17 unresolved sizing fields. No contact, procurement, deployment, physical test, source bypass or authorization is made here.

The existing laboratory protocol [experiment_protocol_v1](../research/experiment_protocol_v1.json), [rig architecture and BOM](PROTOTYPE_TEST_RIG_ENGINEERING_20261020.md), [RM2 load research](RM1_RM2_STRUCTURAL_GATES_20261020.md), [shaft-support requirements](SHAFT_SUPPORT_REQUIREMENTS_20261022.md) and [unranked three-family comparison](PROTOTYPE_COMPARISON_20261020.md) remain the authoritative technical starting points. Do not infer physical readiness from these desk documents.

## A. Separate three stages; none is automatically authorized

| Workstream | What it could demonstrate | What must happen before it proceeds |
| --- | --- | --- |
| Dry rig/sensor integration | Signal timestamps, sign conventions, strain/torque/force calibration, control-power accounting and guarded emergency stops | Venue or lab owner acceptance, independent mechanical/electrical risk review, equipment selection and certified calibration |
| Controlled water pilot (freshwater/tow/flume) | Measured matched-run *net electricity* and simultaneous cyclic structural load, with replicated operating settings | Qualified laboratory apparatus, reference flow measurement, guards, shutdown, metrology, frozen AB/BA plan and operator supervision |
| Permitted in-water coastal pilot | Site operation, ebb/flood effects, maintenance/retrieval, marine/ecological exposure | Qualified **site** inflow, documented device limits, legal access, all appropriate NS/federal/other authorizations and ecological/navigation acceptance |

**Important dependency correction:** native FORCE field ADCP QC is a hard blocker for **FORCE site-specific forecasting**, not a requirement to run a separately instrumented **controlled laboratory flume**. The flume must nevertheless measure its *own* inflow and uncertainty. Neither is a substitute for the other.

## B. Smallest defensible first experiment

Use the **same cross-flow rotor and generator boundary** for the first controlled test, with nominal TSR 3.1 baseline against approximately 2.9 candidate, inspired by historic RM2 processed mean Cp/Cd observations. These are **not** mechanically validated turbine settings or a demonstrated controller improvement. Do not compare three unrelated handmade machines in the first run.

The existing prospective setpoints 0.6, 1.0, 1.4 m/s and both flow directions are *planning assumptions* pending actual facility capability, safety and blockage assessment. Before manufacture or testing, have a competent reviewer freeze: true test-section dimensions, rotor envelopes/materials, expected worst-case thrust/torque/oscillating loads, scale/Reynolds/blockage limitations, synchronized acquisition rate/latency, reference calibration uncertainty, test length, sample-size/power justification, randomization, stop criteria, and a separately justified acceptable net-energy sacrifice. The illustrative two-replicate suggestion in the old protocol is **not** a powered sample-size calculation.

Every matched run must include measured 3-D upstream velocity/turbulence, density/temperature, rotor phase/speed, shaft torque, calibrated blade-root and support/strut strain/load, signed generator-side and load-side electrical power, separately accounted control/auxiliary energy, and trip/missing-data flags. Primary comparison should disclose peak/alternating blade stress and validated cycle statistics alongside *net* electrical energy, confidence intervals and all excluded/failed trials. If stresses improve but energy does not, report that separately. No generic fatigue-life extrapolation without material-specific validated stress/cycle response.

Use independent axial and oscillating-foil studies **after** this single-rotor measurement chain works; they have distinct capture-area definitions, powertrains, controls and moving-envelope safety gates. Do not sort RM1 axial Cp against RM2 D×H Cp as if the denominators are equal.

## C. Actual facility leads (no booking, price quote, or suitability confirmation)

| Venue / source | Why investigate | Limit that must remain visible |
| --- | --- | --- |
| [Dalhousie Aquatron, Halifax](https://www.dal.ca/dept/aquatron/about.html); [historic tidal-turbine/fish study](https://tethys.pnnl.gov/publications/tidal-turbine-marine-life-interaction-study-fish) | The facility exists; a **historical** experimental programme described a guarded vertical-axis tidal turbine and fish-interaction trial at Aquatron. This is a stronger local precedent than an ordinary water tank. | Past approval/test geometry says nothing about a 2026 opening, available flow speed, price, staff, metering or acceptance of our proposed rotor. Live fish experimentation is **out of scope** for the first pilot. |
| [COVE Stella Maris, Dartmouth](https://covesolutions.com/programs-services/stella-maris-testing-solution/) | Operator describes dockside/subsea equipment and a shore operations/data capability; plausible first step for seals, telemetry and wet instrumentation. | **Not** established as a rotating generator's calibrated tidal-flume venue. |
| [Memorial University engineering towing tank, St. John's](https://www.mun.ca/engineering/ona/research/research-facilities/towing-tank/) | University explicitly lists tests relevant to current/wave-driven power devices; candidate for controlled mechanical/power comparison. | Rig compatibility, device safety, current/tow conditions, instrumentation, access and price unresolved. |
| [Marine Institute CSAR flume, St. John's](https://www.mi.mun.ca/departments/centreforsustainableaquaticresources/services/) | Flume serves ocean-technology as well as fisheries testing; **official posted rate effective April 1, 2026: CAD $5,000/day**. | No confirmation it will host our moving turbine, provide required speeds/metrology or be available. Posted list rate is not a quote. |
| [NRC towing tank, St. John's](https://nrc.canada.ca/en/research-development/nrc-facilities/towing-tank-research-facility) | Government facility lists open-water propeller, hydrodynamic-force and precision towing tests. | [NRC says fees depend on project](https://nrc.canada.ca/en/research-development/products-services/technical-advisory-services/physical-modelling-services); suitability, instruments, dates and cost remain unconfirmed. |

The [Dalhousie/NRC research collaboration](https://cnrc.canada.ca/en/stories/current-affairs-harnessing-renewable-energy-bay-fundys-tides) and [Ocean Frontier Institute tidal-loading research topic](https://www.ofi.ca/ogen-opportunities/risk-and-cost-mitigation-through-determination-of-tidal-turbine-loading-under-real-turbulent-tidal-flow-conditions) provide **relevant technical expertise** to investigate only if specific outreach is later approved. They do not represent partnership or acceptance.

## D. Cost that we can actually support

One published 2026 source supports **the Marine Institute flume daily list rate alone**:

| Illustrative reserved days | Published-rate multiplication, CAD | Not included |
| --- | ---: | --- |
| 1 day | $5,000 | All non-venue and extra venue costs |
| 2 days | $10,000 | All non-venue and extra venue costs |
| 3 days | $15,000 | All non-venue and extra venue costs |

This is **not** an estimated project total or a claim that any day count is adequate. The daily rate could exclude operators, test preparation, model hardware, calibrated instrumentation, metrology, software/data reduction, local safety engineering, consumables, additional facility time, travel/shipping, insurance, taxes and contingency. Final facility quote and exact inclusions are unknown; most critical component prices and loads are still unsized. There are currently **zero verified written component/venue quotes**, **no spending authorization**, and no identified compatible timeslot. Any budget approval should require at least two independent quotations for high-cost instrumentation/fabrication where practicable, a named venue, reviewed geometry/loads, clarified test schedule and full inclusion/exclusion reconciliation.

**Information to request only if external outreach is expressly approved:** maximum test-section dimensions and actual controllable velocity envelope with turbulence/blockage data; permissible moving-rotor loads/failures; upstream velocity, torque, strain and independent electricity/auxiliary metering availability; sample clocks/calibration; guarding and emergency-stop responsibility; operator support; current scheduling; daily versus setup/equipment/calibration rates, overtime, taxes, cancellation/data ownership and confidentiality; allowed battery/low-voltage electrical architectures; staffing and transport rules. A user-approved inquiry is not authority to book a day or purchase components.

## E. Current regulatory update; no urgency for the wrong permit

The [Nova Scotia tidal demonstration permit page](https://novascotia.ca/programs/tidal-demonstration-permit/) was checked October 23, 2026. It explicitly notes **application-guide Version 2 published October 21** (interconnection sections revised), and displays an **October 30, 2026, 11:59 p.m.** application deadline. The July 31 press release gave a September 30 closing date; the live programme page is the newer source for the published deadline. **This does not imply our project is eligible.** The programme concerns grid-connected Bay of Fundy demonstration generators, not general permission for bridge-mounted or ad hoc small devices and not approval of a laboratory experiment. Do not rush to apply with a non-existent qualified turbine or confuse filing with permission. Before any site work, independently assess applicable NS, DFO, Transport, property/berth, fisheries, Mi'kmaq rights and ecological requirements for the *particular* apparatus/site.

## F. The decision that unlocks the next phase

1. **Choose a plausible *venue for review*, not a winning device.** Aquatron is a particularly relevant historic near-Halifax research lead; COVE suits wet electronics; university/NRC towing or flumes suit controlled flow. Operator/technical acceptance unknown for all.
2. **Freeze the tested apparatus and metrology:** real rig envelope, professionally reviewed worst-case loads and fail-safe guard, calibrated sensors, AB/BA replicate/protocol, uncertainty and signed net-electricity boundary.
3. **Get real written venue/instrument/material quotes and professional review** after explicit authorization for outside communication, then run a guarded instrumented small pilot only if the applicable safety and permission gates pass. In parallel, resolve FORCE native QC/geometry or obtain an independently qualified current series for a *later* field forecast; no bypass of HTTP restrictions.

Run `python scripts/check_lab_pilot_readiness.py` and `python -m unittest tests.test_lab_pilot_readiness -v` from repo root for an offline machine-readable snapshot. A successful program exit means the **BLOCKED** facts agree with upstream records. It never means the hardware is safe or tested.
