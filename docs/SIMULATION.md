# SCREEN-001 model and reproduction

## Purpose
Determine the **electricity exported** under an electrical export cap, holding the **same synthetic inflow, assumed turbine power curve and rotor parameters**. This is not load-based derating: there is no pitch, torque, thrust, generator thermal or fatigue response.

## Model

Two synthetic signed currents (SI units):

`u(t) = 2.2*sin(2*pi*t/(12.42*3600)) + 0.35*sin(2*pi*t/(12.0*3600) + 0.4)` in m/s. This is illustrative only: **not an actual tide prediction or a Nova Scotia site**. Reverse flow uses `abs(u)` and assumes equivalent bidirectional capture. Discontinuous cut-in: zero below 0.7 m/s, otherwise:

`P_gen,kW = min(200, 0.5*rho*A*Cp*eta*abs(u)^3/1000)`;
`rho=1025 kg/m^3`, `A=pi*(10m/2)^2`, `Cp=0.4`, `eta=0.9`.

`P_export,kW = min(P_gen,kW, P_rated,kW * export_cap_fraction)`.

`E_kWh = sum(P_export,kW * delta_t_seconds / 3600)` via midpoint intervals (last partial interval supported). Duration: 14 days; base 300s step; 150s and 75s convergence. Comparison export cap=0.8 (160 kW) versus baseline cap=1.0 (200 kW). Power coefficient is constant even though real Cp is speed/control-dependent. Curtailment has *no physical control interpretation*; unused generated energy/dissipation unspecified.

## Reproduce (Python 3.10+, stdlib only)

```sh
python -m unittest discover -s tests -v
python scripts/check_catalogue.py
python -m tidal_screen.cli --config configs/synthetic_screen.json --out reports/SCREEN-001.json
```

Output JSON includes parameters, provenance, config/model/CLI SHA256, Python version, run command, code-revision resolution rule, baseline and capped energy, 81 sensitivity combinations, and time-step convergence. Provenance SHA256 is preferable to an in-file commit SHA (self-referential change). For publication revision use the commit that contains the report and compare hashes.

### Analytical checks and limitations

- `u=0` and below cut-in yield zero power; opposing signed flow is symmetric by assumption.
- Well below rated, power follows `u^3`; at high speed it caps at rated.
- An export cap cannot increase exported energy; 100% cap has no loss.
- With constant inflow *at fixed power* energy is exactly `P * duration`; the implementation integrates the same fixed power using midpoint quadrature. Tests cover analytic power, constant-flow integrated energy across several step sizes, cubic law, caps, partial final timestep and convergence.
- No measured velocity, turbulence spectrum, Ct(lambda), blade fatigue, cavitation, availability, cost, ecology, rotor control or electrical waste/dump load is modeled. Sensitivity bounds are assumptions, **not** a statistical confidence interval.
- Range test varies primary amplitude [1.6, 2.2, 2.8] m/s; Cp [0.3, 0.4, 0.5]; eta [0.85, 0.9, 0.95]; rated [150,200,300] kW; changing these does not simulate alternative architecture performance.

## Validation hierarchy
1. Analytic/unit checks and screening (CURRENT; not physically validated).
2. Reproduce published experiment such as Sandia RM1 measured Cp-versus-TSR using its actual geometry and experimental data (NOT started).
3. Calibrated rotor, control and load coefficients validated to independently measured cases.
4. Coupled fatigue, structure, wave/platform/mooring dynamics and uncertainty.
5. Maintenance windows/reliability, OPEX/CAPEX and lifecycle economics calibrated to records.
6. Independent controlled physical testing with environmental monitoring.

Do not substitute a zero-uncertainty software output for a real-world measurement.
