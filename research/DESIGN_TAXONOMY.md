# Design taxonomy / comparison matrix (2026-10-20)

Evidence status: **qualitative candidate characteristics** only, not verified cross-design numerical rankings. The separate RealTide FMEA [RT-001] compares four *generic assemblies*, not identical tested prototype configurations, and is not a measured platform availability comparison.

| Architecture / decision | Potential mechanism | Distinct added risks or limits | Evidence needed before choosing |
|---|---|---|---|
| Seabed HATT, fixed foundation | Structural station-keeping, established reference geometry | Subsea service/lift complexity, access weather/current windows, seabed interaction | RM1 performance benchmark; lift/vessel time; site/geotechnical study |
| Floating HATT, recoverable rotors | Access components near surface; tow for major maintenance | Wave, mooring, tether and connector fatigue; navigation; biofouling; moving platform | Coupled load histories, access window distribution, unavailability model |
| Cross-flow / vertical-axis | Orientation tolerance; alternative bearing/shaft arrangements | Cyclic torque, start-up, support drag, rotor structural loading | Measured C_p(lambda), C_t(lambda), cyclic stress and reliability |
| Ducted horizontal-axis | Flow augmentation potentially at rotor | Duct drag, structural mass, cavitation, debris, marine-habitat effects | Net device power per overall frontal area, velocity/shear profile, thrust |
| Open rotor | Fewer duct structures; comparability to RM1 baseline | Blade tip/debris impact, performance loss in wakes | Rotor maps, turbulence, wake recovery, blade FEA |
| Tethered tidal kite | Higher apparent blade inflow from cross-current motion | Tether/control/steering fault, swept volume, seabed/traffic interaction | Actual net export, trajectory controls, mooring loads, safety cases |
| Direct-drive generator | Eliminates gearbox; fewer geared parts | Large generator and bearings; seal/electrical failures; heavier lift | Component MTBF/MTTR sourced, specific loads, converter losses, lifecycle cost |
| Geared drivetrain | Higher shaft-speed generator, possible mass benefit | Gear lubrication, failure/repair, seals, parasitic losses | Comparative component test and published maintenance histories |
| Fixed pitch | Minimal pitch mechanisms | Less ability to regulate loads away from design point | Actual turbine Cp/Ct, control and fatigue maps |
| Active pitch | Load/power regulation via actuation | Actuator, seals, power loss and sensor failure | Closed-loop load spectra and actuator reliability |
| Passive pitch | Passive reaction to time-varying flow loads | Spring preload, friction, wear, jamming, uncontrolled mean loads | Paper [PP-001] replay with own experimental uncertainty and wear |
| Arrays | Shared collection and possible wake steering | Wake deficit, layout constraints, cable failures, habitat cumulative effects | Measured wakes, cable N-1, ecological/cost-scale evidence |

**Excluded from stream-device comparisons:** tidal barrages and lagoons alter impoundment/head; wave energy converters respond to waves. Keep independent classification, economics, permits, impacts and benchmarks.

First five questions: load reduction vs net lifetime energy [H-001]; direct drive [H-002]; recoverable modules [H-003]; floating [H-004]; passive pitch [H-005]. No architecture is designated a winner.
