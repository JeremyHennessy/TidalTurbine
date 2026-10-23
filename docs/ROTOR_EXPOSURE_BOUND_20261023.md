# TT-LAB-CYCLES-01 — hypothetical rotor-cycle exposure under an ideal short tow

**2026-10-23. DESK / ENGINEERING ASSUMPTION ONLY. Not a lab result, a build drawing, fatigue-life estimate, equipment selection or an authorization to contact facilities.** Starting checkpoint: verified main `c812e830106cc44e2eed53fcfa27ffb3ee6fd707` (PR #37). No existing scientific data, TidalLab UI/artwork, shaft selection or test-venue readiness is modified.

## Why this matters

The [Memorial University towing tank's published specifications](https://www.mun.ca/engineering/ona/research/research-facilities/towing-tank/) provide **35 m usable carriage travel** and **2 m/s² maximum carriage acceleration**. Earlier [venue review](LAB_VENUE_SCREEN_20261023.md) used a separately *assumed* equal 2 m/s² braking magnitude, zero added clearance and zero stabilization to calculate optimistic constant-speed windows of 58.03, 34.50 and 24.30 s at 0.6, 1.0 and 1.4 m/s. These values do **not** establish that a turbine or laboratory can actually use the windows. The originally published tank specs do not qualify rotor start-up, safe braking, flow turbulence, electrical wiring or sensor mounting.

Even a recorded 30 seconds can represent different numbers of rotor revolutions depending on rotor diameter and tip-speed ratio (TSR). This can change how many phase-dependent blade-load passages an instrument might capture. The nominal count is *not* measured independent fatigue cycles, independently repeated experiments or scientifically adequate sample size. A meaningful structural-load versus net-electricity test still needs measured strain/force histories, electrical metering, repeatability, source-qualified laboratory flow and statistical uncertainty.

## Read-only reproducible math

For the assumed **rotor diameter** `D` [m], carriage/inflow speed `U` [m/s], rotor tip-speed ratio `lambda` [dimensionless] and assumed constant-speed interval `T` [s]:

- angular speed `omega = 2 * lambda * U / D` [rad/s], **assuming rotor tracks the target TSR throughout**;
- nominal revolutions `N = lambda * U * T / (pi * D)`;
- for a *hypothetical* `B` blade rotor, total **aggregate passages at one fixed azimuth** = `B*N`. These are **not** blade-root stress cycles for any individual blade. Harmonics and transient stresses may differ;
- blade-passing frequency `f_B = B * lambda * U / (pi * D)` [Hz] is an expected mechanical frequency, *not* a justified strain/DAQ sampling frequency.

Run the completely offline test with an **explicit what-if geometry** (these inputs are not a rotor specification or selected design):

```sh
python scripts/screen_rotor_exposure.py --assumed-diameter-m 0.6 --assumed-blades 3
python scripts/screen_rotor_exposure.py --assumed-diameter-m 0.6 --assumed-blades 3 --assumed-reserved-travel-m 5
python -m unittest discover -s tests -p test_rotor_exposure.py -v
```

The tool inherits and re-checks the scientific and outreach prohibitions from the existing venue checker and the original `research/experiment_protocol_v1.json`. It writes no file, accesses no network and cannot output 'physically tested'. No parameter has been adopted as an actual rotor diameter/blade count. It never chooses a finite sample rate, number of required replicates, adequate fatigue exposure or purchase cost.

### Example — one **fictional 0.6 m, three-blade rotor**

| Hypothetical tow speed (m/s) | Assumed TSR ~2.90 rotor turns | Assumed TSR ~3.10 rotor turns | Optimistic steady travel time (s) |
| ---: | ---: | ---: | ---: |
| 0.6 | ~53.6 | ~57.3 | 58.03 |
| 1.0 | ~53.1 | ~56.7 | 34.50 |
| 1.4 | ~52.3 | ~55.9 | 24.30 |

*Values use published processed RM2 source nominal TSR 2.8999618 (run 10) and 3.0993495 (run 12), an illustrative D=0.6m and the previous unverified 2m/s² braking assumption. Under these assumptions, number of revolutions changes little with speed for a **fixed-distance** tow, even though shaft RPM and strain frequency rise with speed. Count only ideal target-TSR revolution estimates, not start/stop cycles. Real counts could be zero.*

## Consequence for experiment design

1. **Do not mistake one towing pass for a fatigue test.** Even tens of nominal turns cannot establish material fatigue life or any reliability benefit. A one-rev-periodic strain record may still support *descriptive load modulation* after actual calibration and validity review.
2. **Pair the two operating regimes fairly.** TSR 2.9 and 3.1 imply different revolutions per equal-duration tow, even on the same model. Report calibrated loads per revolution/phase and per time at matched inflow; separately report **net delivered electrical energy** per actual test exposure. Preserve transient loads, bad data and failures rather than deleting them. A larger nominal blade-passage count is not independent trial replication.
3. **Freeze actual measurement requirements first.** Rotor blade-root/strut stress (calibrated), synchronized torque/angle, laboratory inflow/turbulence, separately metered generation and control draw, uncertainty and robust paired replicates are all needed. No sampling frequency can be approved from f_B alone because blade harmonics, accelerations, structural resonances, anti-alias and clocks must be characterized.
4. **Select neither venue nor rotor yet.** A continuous-flow flume or verified long-run setup might ultimately deliver many more valid cycles, but no verified suitable venue, full quote, authorized physical rig or signed electricity record exists. Aquatron's historical flow project is a lead only. The FORCE native-QC blocker pertains to site-specific ocean predictions and is not solved by this laboratory maths.

**Falsifiable next decision:** Can a particular real venue plus instrumented rotor provide an independently preregistered, repeatable matched load-versus-electricity dataset with enough valid structural cycles and uncertainties for a justified statistical inference? The answer remains UNKNOWN. Source: [original measurement protocol](../research/experiment_protocol_v1.json), [prototype readiness gates](../research/lab_pilot_readiness_20261023.json). No external outreach is permitted at the user's current instruction.
