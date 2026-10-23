# Laboratory venue and idealized tow-time feasibility (2026-10-23)

**Internal research only. No emails, calls, bookings, purchases or physical testing authorized.** Reviewed against main `6b7da10462bc35f730f06ce81ee1a183ef4fdb92`. This note advances venue compatibility research without altering any TidalLab display or approved physical/synthetic/scientific outputs. Scientific source classifications remain distinct.

Source and status registry: [lab_venue_screen_20261023.json](../research/lab_venue_screen_20261023.json); deterministic **offline** validator: [check_lab_venue_screen.py](../scripts/check_lab_venue_screen.py); scientific load/electricity requirements: [previous lab readiness package](LAB_PILOT_READINESS_20261023.md).

## Findings, with source boundaries

### Dalhousie Aquatron — historical turbine study, not current authorization

MacNeill et al., *Tidal Turbine-Fish Interaction Pilot Study in the Aquatron Controlled Lab Space* (EWTEC 2017), [full primary paper](https://tethys.pnnl.gov/sites/default/files/publications/MacNeill_et_al_2017.pdf), pp. 1–6, documents use of a ~15.24-m-diameter pool tank (4-m test depth) for a 0.9-m diameter three-blade cross-flow turbine. The *2017 project* modified four 75-hp water-pump returns; nominal test series used 0.6, 1.2, 1.8 and 2.4 m/s pump/flow settings. Flow was probed with a Nortek Vectrino and trial small turbine during setup. This is **historical evidence of capability, not a modern facility acceptance or assured test uniformity**.

The source contains an unresolved **reporting difference**: its abstract describes about 2 m/s for the fish-study phase, while its methods page states three pumps at 85% with a fixed 1.5 m/s throughout that study. Preserve both, not a fictional reconciled speed. The tested mechanical output was inferred from external motor-drive power and estimated losses; neither direct **signed delivered turbine electricity** nor calibrated **blade-root stress cycles** meets our target evidence boundary. Fish testing is not part of our first laboratory experiment. This precedent should therefore be used for access/safety/flow discussions **only when the user later approves contact**, not as proof we can reproduce its experiment today.

### Memorial University OERC towing tank — dimensioned public bounds and rate, not guaranteed test duration

The [official Ocean and Naval Architectural Engineering facility page](https://www.mun.ca/engineering/ona/research/research-facilities/towing-tank/) reports a **35-m usable travel length**, 4.5-m tank width, maximum 3.04-m depth, maximum **5.0 m/s carriage speed** and maximum **2.0 m/s² carriage acceleration**. The page explicitly mentions research with current/wave-driven power devices. Those are **published facility specifications**; they do not establish a safe design envelope for our turbine, a guaranteed tow interval, a braking curve, ambient turbulence, usable clearance or acceptance of oscillatory strain/electrical measurement.

The [official OERC user policy](https://www.mun.ca/engineering/research/centres-and-facilities/research-centres/oerc/user-policy/) lists **$1,000 per day** as the *typical external-user towing tank rate*, says technician support is included, and notes complexity-dependent rates and the need for a final quotation. **The page does not explicitly identify the currency.** Do not silently compare it as a confirmed CAD cost until clarified. No reservation, quotation or special equipment coverage has been obtained. The university states scheduling priority and a suggested lead time; it is not an available slot.

#### Why the usable travel length matters

Assume, *optimistically*, symmetric acceleration and braking each at 2.0 m/s², stationary ends, all 35 m available and zero clearance/stabilization distance. At a target carriage speed `v`:

- acceleration distance = `v²/(2a)`, braking distance = `v²/(2b)`;
- idealized constant-speed distance = `35 - v²/(2a) - v²/(2b)`;
- idealized constant-speed time = remaining distance / `v`.

| Assumed speed (m/s) | Combined ramps (m) | **Optimistic ceiling** for constant-speed time (s) |
|---:|---:|---:|
| 0.6 | 0.18 | 58.03 |
| 1.0 | 0.50 | 34.50 |
| 1.4 | 0.98 | 24.30 |

These are **mathematical upper bounds under an idealized acceleration model**, not certified test durations, guaranteed flow-quality windows, actual rotor steady-state operation or a physical load spectrum. Real usable time can be much shorter (or zero) because of safety zones, motor settling, instrument stabilization, rotor run-up, wave return, turbulence, endpoint deceleration, repeat preparation and on-site constraints. The maximum published acceleration is **not** a confirmed matching braking value. Replacing the assumed acceleration/braking or reserving even 5 m of total margin changes the estimates. A long continuous operation/fatigue campaign cannot be inferred from one tow, and laboratory staff must determine if repeated passes or another facility offer a statistically adequate load-cycle record.

Reproduce these bounds, without network or writes: `python scripts/check_lab_venue_screen.py`. Python tests deliberately reject cost, timing, permission or measurement promotions.

### Marine Institute CSAR flume — different lab, different rate

The [Marine Institute official services page](https://www.mi.mun.ca/departments/centreforsustainableaquaticresources/services/) publishes **CAD $5,000/day effective April 1, 2026** for its flume tank. No confirmed test-specific current range, signed electrical metrology, available schedule, project price or operator acceptance has been obtained. Continuous recirculating flow might simplify long repeated observations relative to a short towing run, but that is a **test concept**, not a demonstrated available capability for this rotor.

### COVE Stella Maris — wet electronics, not proven hydrodynamic flow test

The [operator's facility page](https://covesolutions.com/programs-services/stella-maris-testing-solution/) describes subsea/dockside testing and instrument integration. Treat as a potential wet sealing/telemetry facility, **not a documented calibrated moving-turbine power-and-fatigue test venue**. Price unknown.

## Next engineering decision (without contact)

The laboratory test must compare **simultaneously and repeatedly** calibrated time-resolved blade and support loads, shaft torque/speed, measured flow and its quality, independent generator/load-side electricity and separately metered controller/actuator consumption. For the existing RM2-style single-rotor comparison, whether a 24–58 s optimistic single-tow ceiling provides sufficient independent cycles remains **UNKNOWN** until real rotor dimensions/rpm, sample synchronization, facility flow stabilization, protection boundaries and preregistered statistical power are reviewed.

**Decision for now:** keep both Aquatron and the OERC towing tank as viable *research leads*, not accepted test venues. Prioritize a paper-only acceptance matrix: steady inflow/turbulence, usable model envelope, strain/torque/phase DAQ and independent load-side power, guarding/E-stop, price inclusions, replication/day schedule, data rights. Do not select a turbine/shaft or rank facilities by unconfirmed all-in price. Retain the 15 original blocked gates unchanged.

**Next three actions:** (1) internally bound allowable rotor diameter/height only after a defined rig safety and blockage envelope; (2) freeze metrology/calibration and statistically justified paired AB/BA trial length and replicates, including true electrical-energy accounting; (3) seek current operator acceptance and complete quotations **only after later explicit user authorization for external outreach**. FORCE 3-D native QC remains a separate blocker for field-specific energy modeling and is not fixed by these lab calculations.

## Evidence classification and preservation

- Facility dimensions, historic methods and posted rates: **PUBLISHED_EVIDENCE** limited to dates/pages and scopes cited.
- Ideal steady-window arithmetic: **ENGINEERING_ASSUMPTION / SYNTHETIC_ACCOUNTING_RESULT**.
- Test design preference and needed channels: **DESIGN_HYPOTHESIS**.
- Current facility access, quote, safety certification and laboratory performance: **UNKNOWN_OR_CONFLICT**.
- No field authorization, fabricated prototype, measured net electricity, validated stress cycles or selected turbine exists. No external communications initiated.
