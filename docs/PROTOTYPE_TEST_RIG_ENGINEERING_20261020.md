# TT-RIG-01 — Instrumented tidal-stream prototype flume test-rig engineering package

**Status: PROSPECTIVE ENGINEERING DESIGN, NO BUILD OR PURCHASE AUTHORIZATION.** 21 October 2026 UTC. Intended for the approved goal of comparing axial, cross-flow and reciprocating heave/pitch power converters under a contained, permitted professional laboratory flume or tow tank. It is not a ready-to-fabricate structural drawing, a certified electrical design, a supplier quote or authorization for coastal deployment. Machine-readable preliminary BOM: [prototype_test_rig_bom_v1.json](../research/prototype_test_rig_bom_v1.json).

## 1. Measurement boundary and apparatus layout

The core hypothesis and required measurements are in [experiment_protocol_v1.json](../research/experiment_protocol_v1.json). The test cell must be protected, recoverable and supplied with actual upstream vector velocity/turbulence observations. Match the same incoming control volume, exposure time and laboratory confinement across mechanisms while retaining mechanism-specific capture areas.

~~~mermaid
flowchart LR
    Flow["Measured laboratory current<br/>ADV 3D, shear & QC"] --> Cell["Guarded, interchangeable test cell<br/>axial / cross-flow / foil"]
    Cell --> Strain["Blade & strut strain<br/>two-axis support forces"]
    Cell --> Shaft["Torque + phase<br/>or foil force/velocity/moment"]
    Shaft --> PTO["Generator / PTO / programmable load<br/>independent overspeed shutdown"]
    PTO --> Meter["Independent electrical meter<br/>load side + controller and actuators"]
    Flow --> DAQ["Single-clock DAQ<br/>timestamps, QC and trips"]
    Strain --> DAQ
    Shaft --> DAQ
    Meter --> DAQ
    Cell --> EStop["Safety interlock / hardwired stop<br/>guarded de-energized recovery"]
    DAQ --> Records["Immutable source traces and checksums<br/>cycle/uncertainty reporting"]
~~~

This is a **conceptual signal and containment architecture**, not approved wiring or equipment dimensions. Qualified structural/electrical designers must select fuses, isolation, shaft guards, load bank thermal protection, lifting points, load limits and emergency stop. Confirm instrumented test-section cross-section, blockage, safe swept clearances, tank depth, worst credible force and protected access before choosing any rotor diameter or manufacturing article.

## 2. Channels, sample rates and calibration

Minimum synchronized channels: 3D upstream fluid velocity, shear/turbulence and scientific QC; water density/temperature and depth; rotor angular phase, shaft torque and velocity (or foil heave force×velocity plus pitch moment×rate); calibrated blade-root strain in critical bending axes and support/strut load paths; separate direct calibrated support drag and lateral forces; generator-side and *signed load-side* electrical energy; independent actuator/control/PTO auxiliary electricity; start/stop, fault, dropout, instrument saturation and emergency-stop states. Use upstream flow and uncertainty at each actual tested position, not a fixed assumed tide speed or generator clipping proxy.

Preregister anti-alias filtering, sampling frequencies from expected load harmonics, timing jitter budget, source channel latency and independently measured calibration error. **The recovered 2015 RM2 NI logger used 2 kHz**, per original metadata; this is not an automatic minimum for a new rig. New timebase, bridge gauges, reference load-cell capacities and stress calibration must be specified only after actual apparatus design review.

Before and after every test block, record serial numbers, source calibration documents, zero offsets, temperature effects and drift, then preserve immutable original signals and calibration metadata outside Git with hashes. Record any force sensor saturation, missing samples, encoder failures, transducer alignment, cross-talk, fluid turbulence and electrical grounding issues without retrospective erasure.

## 3. Prospectively test the observed RM2 operating-point question

The newly recovered original NI files contain *rig* drag, shaft torque, turbine angle and carriage position for six historical tow-tank trials at 0.4, 1.0 and 1.2 m/s and nominal TSR 2.9/3.1. Original source calibrated units are N, N m, degrees and metres; the repository has not independently recalibrated its equipment. The raw data can be used to compare descriptive support-force/shaft-torque time histories, but **not blade-root stresses, validated strain-cycle damage, controller electricity or net delivered electrical energy**.

Freeze a primary null hypothesis: no credible damaging-load reduction for the lower-TSR mode while preserving an acceptable net electricity result under matched actual inflow. Include low-speed conditions since the previously acquired 10 published performance sweeps show a much higher Cp penalty at 0.4 than 1.0 m/s. Use independently randomized paired AB/BA sequences, measured inflow/turbulence, source-constrained blockage/Reynolds corrections, predeclared structural-load and delivered-energy tolerances, and sample-size/power justification **before** seeing future test outcomes. One historical trial per setting is not a powered replicated experiment.

Compute true mechanical work from synchronized torque×omega; *net* electrical energy from load-side watts minus non-double-counted actuator/auxiliary/control draw; phase-specific peak and alternating stress from **independently measured calibrated strain**, material stress transfer, cycle counting and uncertainty. Separate shutdown transients and condition/ambient flags from steady measurements. Do not treat relative decrease in mean Cd or even lower support-force SD as independently measured fatigue improvement.

## 4. Three unranked converter families

| Gate | Axial (RM1 reference) | Cross-flow (RM2 reference) | Nonrotating heave/pitch foil |
|---|---|---|---|
| Motion / capture | Axial rotor, disk area per rotor | Transverse H-rotor, frontal D × H | Foil heave envelope and full corridor |
| Synchronised mechanics | Shaft torque, axial thrust, blade-root strain | Shaft torque, phase, strut/root strain and support drag | Heave force/speed and pitch moment/rate |
| Electrical accounting | Load-side after drivetrain/yaw/pitch losses | Load-side after TSR and PTO control losses | Load-side minus active heave/pitch or hydraulic controls |
| Independent stop gate | Bearing seals, retrieval, fish strike, access | Blade/strut cyclic loading, entanglement, bearings | Joint/foil fatigue, trapping, storm parkability |
| Authorization | Facility safety and DFO/NS/marine rights if field | Same, separately | Same, separately |

Never sort dissimilar mechanical Cp denominators as a device winner. Compare matched measured upstream control-volume energy over a common time period, a documented installation corridor and actual delivered electricity, while retaining all individual mechanism acceptance tests. UNKNOWN does not count as zero-cost or satisfactory.

## 5. Planning BOM, expenses and manufacturing readiness

The [JSON BOM](../research/prototype_test_rig_bom_v1.json) contains **20 functional categories** for a modular frame, shaft/foil sensors, independently measured mechanical forces and strain, upstream velocity, shaft encoder, synchronized DAQ, PTO/generator and actuator meters, load-bank protections, guarding/emergency stop, loggers, ecological instrumentation and trial articles. All tentative quantities are **planning assumptions**. None are purchase orders or actual commercial component selections; nominal load capacities, structural safety margins, water ingress protection, electrical configuration and local supplier prices remain UNKNOWN until a qualified engineer reviews the lab environment and expected forces.

**Verified CAD price quotes: 0. Current approved budget: NONE.** Do not invent Canadian-dollar costs or give a numerical grand total. Before any procurement, obtain facility acceptance, independent mechanical/electrical risk analyses, applicable test standards, third-party calibration availability, witnessed E-stop response and at least two written offers for critical torque/force/DAQ systems.

## 6. Safety, environmental and release gates

- No field current generator or bridge-mounted trial may proceed without explicit operator/venue consent, tested containment/safe stop, scientific source-qualified inflow and applicable NS/DFO/Transport, Mi'kmaq rights and fisheries/eco navigation acceptance.
- Independent acoustic/marine monitoring and reliable recovery/lifting must be approved; site access and maintenance are hard gates separate from energy.
- Lab water tests require trained professionals and a guarded de-energized recovery protocol; no unsupervised operation or physical construction is authorized by this Markdown plan.
- The lab's first documented pass must prove metrology and calibration, not assert positive electricity or fatigue benefits. Save failures, trip events and invalid runs without deleting negative observations.

**Completed here:** review-ready test-rig scope, measurement chain, phase-coupled mechanics/electricity plan and function-oriented BOM. **Not completed:** physical prototype, confirmed test facility, quotes, calibrated structural instrumentation, permits or empirical stress/electricity evidence.
