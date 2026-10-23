# TT-METROLOGY-01 — lab measurement and preregistration acceptance gates

**23 October 2026 — SOURCE-BACKED PROSPECTIVE TEST DESIGN, UNFROZEN, NOT EXECUTED.** The purpose is to make the first instrumented cross-flow comparison scientifically interpretable, without fabricating physical results, rates, sensor selections or safety approvals. Reviewed exact project baseline `6031d2788c5293c9811ec2cb50a810867df340d6`. Nothing here constitutes an engineered rotor, a booking, a work instruction for operating machinery, or authorization to contact anyone.

This document is backed by a [12-channel machine-readable preregistration](../research/metrology_prereg_v1.json), an [offline fail-closed checker and synthetic-energy audit](../scripts/check_metrology_protocol.py), and [mutation/arithmetic tests](../tests/test_metrology_protocol.py). The [2026 prototype-rig scope](PROTOTYPE_TEST_RIG_ENGINEERING_20261020.md), [original historical RM2 comparator](../research/experiment_protocol_v1.json), [readiness register](../research/lab_pilot_readiness_20261023.json), and [short-tow rotor opportunity bound](ROTOR_EXPOSURE_BOUND_20261023.md) are preserved, not reinterpreted as validated physical evidence.

## 1. The specific falsifiable question

Compare **the same cross-flow rotor** at a reference operating point near source RM2 run 12 (nominal TSR 3.0993495) and candidate near source run 10 (nominal TSR 2.8999618), under actually **measured matched flow, turbulence and test-cell conditions**. The published ~1.85% mean mechanical Cp penalty and ~5.51% mean Cd reduction at one laboratory speed are **historical processed means**, not confirmed lower blade stress, improved fatigue life or net exported electricity.

**Null:** the candidate does not show a credible reduction in damaging *calibrated cyclic loads* alongside an acceptable *measured signed net electrical-energy* result. A favorable support-drag mean, fewer theoretical rotor turns or smaller torque ripple cannot overturn the null alone.

**Predefined falsifiers:** blade/strut peak stress or cycle distributions worsen; the electrical penalty exceeds an independently justified frozen bound; uncertainty/repeated-trial evidence does not support the effect; pump/tow flow, encoder phase, stress transfer or power meter boundary is not qualified. No numerical load-benefit threshold, energy penalty, sample count or test-tolerances are selected in this desk proposal.

## 2. Measurement chain: twelve existing mandatory channels

| Source channel | Quantity & units | What must be documented before physical acceptance |
| --- | --- | --- |
| `inflow_3d` | 3D velocity, m/s | Probe frame and position, volume/quality flags, flow direction, shear, turbulence, upstream representativeness |
| `fluid_state` | density kg/m³, temperature °C, depth m | Density/viscosity method, immersion, free surface, blockage, independent datum and calibration |
| `rotor_position` | angular phase, rad | Signed rotation, physical index zero, encoder wiring, clock offsets, missed pulse policy |
| `rotor_speed` | angular speed, rad/s | Derivation/independent comparison, sign, phase lag, target versus actual TSR |
| `shaft_torque` | torque, N·m | Range and peak/dynamic calibration, tare, sign, shaft location, uncertainty |
| `blade_root_strain` | microstrain (µε) | Material, bending axes, exact bridge topology, excitation, remote sensing, temperature, shunt/physical calibration, waterproofing |
| `strut_strain` | microstrain (µε) | Independent structural load path, calibration, drift and crosstalk; not interchangeable with blade strain |
| `mean_streamwise_drag` | actual time-resolved force, N | Calibrated support-cell signal, load path, cross-axis sensitivity, transient peaks; do not infer from mean Cd |
| `generator_power` | signed W | Actual electrical boundary, DC/AC phase/power factor and time alignment to shaft |
| `delivered_electrical_power` | signed W | Load/grid-side meter with explicit positive-export/negative-import convention and conversion losses |
| `control_and_actuator_power` | signed W | Independent positive-consumption/negative-regeneration boundary; document overlap with delivered meter |
| `rig_status` | event enum | Time-stamped starts/stops, saturation, missing samples, trips, overspeed, emergency stop; preserve bad runs |

Sensor manuals and original source metadata do **not** select actual instruments. Every numerical channel needs its specific serial/configuration, coordinate/sign mapping, reference chain and associated calibration uncertainty, plus pre/post checks and original raw-data provenance. `rig_status` needs witnessed/logged event mapping rather than the numeric calibration requirements. All are still missing.

**Metrological traceability is a property of measurement results**, not just a purchase certificate: NIST requires a documented uninterrupted chain of comparisons and their uncertainties, and warns that traceability alone does not guarantee fitness for a particular measurement decision. [NIST traceability policy](https://www.nist.gov/metrology/metrological-traceability); [NIST TN1297 uncertainty guidance](https://www.nist.gov/pml/nist-technical-note-1297). This register is a *procurement-neutral checklist*, not a calibration result.

## 3. Synchronization, bandwidth and strain conditioning

Freeze, **before** seeing future outcomes: timebase/UTC anchor, hardware/shared clock topology, per-channel transducer and software latency, encoder index/phase mapping, anti-alias filter amplitude and phase response, actual flow/turbulence fluctuation spectrum, structural resonance and load-event bandwidth, logger saturation limits, and the chosen sample frequency and uncertainty budget. Do not blindly reuse 2015 RM2 NI's historical **2 kHz** recording rate. A blade-passing frequency calculated from assumed TSR does not cover harmonics, wave/turbulence content, braking/startup events or bridge resonances.

For strain, choose a valid bridge topology **based on the bending/axial measurand**, not a generic 'full bridge' claim. Document gauge factor, excitation limits, heat/temperature effects, shielding, bridge completion, remote sensing where applicable, offset/null, shunt *electronics gain* check, independent applied-load transfer, moisture ingress and long-run drift. A shunt check is not proof of actual structural force calibration. [NI strain-sensor manufacturer guidance](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-strain-with-strain-gages.html) is guidance, not approval of any specific system.

**Acceptance cannot be frozen today:** actual strain-transfer constants and material properties, allowable phase/timing uncertainty, sample rate, sensor range, filters, percentage of valid samples and stop limits are presently **UNKNOWN**. A future competent independent reviewer must justify them against the real rig and chosen measurement question.

## 4. Signed electrical accounting — no double counting

Let `P_load(t)` be signed metered delivery at a specified boundary (export positive, import negative). Let `P_aux(t)` be **separately** metered consumption (positive) or recovered energy (negative). Decide *before the experiment* whether the auxiliary loads are **outside** or **already inside** that delivered load meter boundary:

- **External auxiliaries:** `E_net = integral(P_load dt) - integral(P_aux dt)`.
- **Already included in delivered meter:** `E_net = integral(P_load dt)`; report `P_aux` diagnostically but **do not subtract it again**.
- **Mechanical work:** `E_shaft = integral(torque(t) × angular_speed(t) dt)`, with independently documented torque/speed signs. This is not load-side electricity.

Reconcile transient/restart imports, any stored electrical energy and whether control regeneration is already in the meter. Do not clamp negative electric results to zero; do not infer generator efficiency or fatigue benefit from the toy calculation below. Generator-side, load-side, auxiliaries and shafts are different quantities. The published [IEC TS 62600-200:2013 listing](https://webstore.iec.ch/en/publication/7242) gives a real-world power-performance reporting *context*, but this proposal is **not IEC 62600-200 compliant or certified** and the full normative text was not inspected.

An **entirely synthetic unit-test fixture**, not a lab trace, uses 0,1,2 s, torque 2 N·m, angular speed 3 rad/s, signed delivered 4 W and separately metered auxiliaries 1 W: mechanical work **12 J**, load-side energy **8 J**, externally supplied auxiliaries **2 J** and synthetic net **6 J**. If auxiliaries were already reflected inside the delivered meter, net is **8 J** instead. The checker verifies both cases, negative net energy, irregular time increments and rejects mismatched clocks, invalid units, nonfinite values and missing channels. **It does not analyze original raw NI traces or qualify future physical samples.**

## 5. Independent matched trials and cycle interpretation

Define the experimental unit as an **independently prepared run**, not individual time steps, individual blade passages or revolutions in one tow. Preserve entire physical runs, common calibrations and randomized paired AB/BA assignments as groups. Pre-register matched speed and turbulence windows, transients and failure exclusions, target sample size with statistical-power rationale, the true stress/load primary metric and phase bins, uncertainty including within-run autocorrelation, the acceptable electrical trade-off, all safety stopping conditions and independent frozen review **before** the apparatus is operated. The previously computed ~53–57 *hypothetical* rotations in an ideal 1 m/s tow cannot be treated as 53–57 independent statistical replicates.

A cycle-counting method such as rainflow can summarize a **calibrated strain/stress history**, but cannot establish life without correct stress transfer, material S–N/other fatigue evidence, exposure and validation. [ASTM E1049-85(2023) official public scope](https://store.astm.org/standards/e1049) identifies such procedures; its full paywalled methodology was not accessed or implemented here. No fatigue cycle counts or material laws are claimed.

**No pass/fail effect size, confidence result, source-trained predictor, trial scheduling, sample-rate selection, relative unit prices, ecological assessment or manufacturing approval is inferred.** Retain and report all failures, dropouts and emergency events.

## 6. Machine-checkable stopping point and next actions

Run `python scripts/check_metrology_protocol.py` to verify **12 channels and 9 unresolved acceptance gates**, with the original experiment and source catalogue. Run `python scripts/check_metrology_protocol.py --toy` for **synthetic-only** signed mechanical and electrical arithmetic. Run `python -m unittest discover -s tests -p test_metrology_protocol.py -v` and the full unit suite. These commands do **no network, no email, no equipment control and no input mutation**. They deliberately report **BLOCKED**, even when unit tests pass.

The first true readiness milestone requires: (1) independently reviewed qualified rig and venue dimensions/safety; (2) calibrated, uncertainty-bounded synchronized measurements and frozen statistically defensible AB/BA conditions; (3) explicit authorization for a physical lab test. Any marine deployment also separately requires native/qualified site flow, rights/fisheries/environment and applicable permissions. **The user's no-contact instruction is in force.**
