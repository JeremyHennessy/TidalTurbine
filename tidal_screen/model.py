"""Screen tidal-stream *electricity* without pretending to predict turbine loads.

The current is explicitly synthetic, reversible and not site-specific. `Cp` is
assumed constant over speed: unsuitable for control, thrust, fatigue, or blades.
"""

from dataclasses import dataclass
from math import isfinite, pi, sin


@dataclass(frozen=True)
class Turbine:
    diameter_m: float = 10.0
    seawater_density_kg_m3: float = 1025.0
    power_coefficient: float = 0.40
    conversion_efficiency: float = 0.90
    cut_in_m_s: float = 0.70
    rated_power_kw: float = 750.0

    def __post_init__(self):
        positive = (self.diameter_m, self.seawater_density_kg_m3,
                    self.rated_power_kw)
        if not all(isfinite(x) and x > 0 for x in positive):
            raise ValueError("diameter, density, and rated power must be positive finite")
        if not (isfinite(self.power_coefficient) and 0 < self.power_coefficient <= 0.593):
            raise ValueError("open-rotor constant Cp must be in (0, 0.593]")
        if not (isfinite(self.conversion_efficiency) and 0 < self.conversion_efficiency <= 1):
            raise ValueError("conversion efficiency must be in (0, 1]")
        if not (isfinite(self.cut_in_m_s) and self.cut_in_m_s >= 0):
            raise ValueError("cut-in speed must be non-negative and finite")

    @property
    def swept_area_m2(self):
        return pi * (self.diameter_m / 2) ** 2


@dataclass(frozen=True)
class SyntheticCurrent:
    primary_amplitude_m_s: float = 2.2
    secondary_amplitude_m_s: float = 0.35
    primary_period_hours: float = 12.42
    secondary_period_hours: float = 12.0
    secondary_phase_rad: float = 0.4

    def __post_init__(self):
        values = (self.primary_amplitude_m_s, self.secondary_amplitude_m_s,
                  self.primary_period_hours, self.secondary_period_hours,
                  self.secondary_phase_rad)
        if not all(isfinite(x) for x in values):
            raise ValueError("synthetic current parameters must be finite")
        if min(self.primary_amplitude_m_s, self.secondary_amplitude_m_s) < 0:
            raise ValueError("amplitudes must be non-negative")
        if min(self.primary_period_hours, self.secondary_period_hours) <= 0:
            raise ValueError("periods must be positive")

    def velocity_m_s(self, time_s: float) -> float:
        return (self.primary_amplitude_m_s * sin(2 * pi * time_s / (3600 * self.primary_period_hours))
                + self.secondary_amplitude_m_s * sin(2 * pi * time_s / (3600 * self.secondary_period_hours)
                                                    + self.secondary_phase_rad))


def electrical_power_kw(turbine: Turbine, velocity_m_s: float) -> float:
    """P=min(P_rated, eta * 0.5*rho*A*Cp*|u|^3) [W], /1000 for kW.

    This is a generic assumed rotor. There is no thrust coefficient, torque,
    control, wave/wake interaction, generator loss map or failure/repair model.
    """
    if not isfinite(velocity_m_s):
        raise ValueError("velocity must be finite")
    speed = abs(velocity_m_s)
    if speed < turbine.cut_in_m_s:
        return 0.0
    raw_kw = (0.5 * turbine.seawater_density_kg_m3 * turbine.swept_area_m2
              * turbine.power_coefficient * turbine.conversion_efficiency
              * speed ** 3 / 1000)
    return min(raw_kw, turbine.rated_power_kw)


def integrate(turbine: Turbine, inflow: SyntheticCurrent, days: float,
              timestep_s: float, export_cap_fraction: float = 1.0) -> dict:
    """Midpoint quadrature of *export* energy; cap only changes delivered kWh.

    A cap below rated power is modeled downstream of the fixed, assumed power
    curve. The destination/dissipation of non-exported energy is unspecified.
    It must not be interpreted as a feasible rotor-control or fatigue strategy.
    """
    if not (isfinite(days) and days > 0 and isfinite(timestep_s) and timestep_s > 0):
        raise ValueError("duration and time step must be positive and finite")
    if not (isfinite(export_cap_fraction) and 0 < export_cap_fraction <= 1):
        raise ValueError("export cap fraction must be in (0, 1]")
    duration_s = days * 86400
    cap_kw = turbine.rated_power_kw * export_cap_fraction
    energy_kwh = 0.0
    unconstrained_export_kwh = 0.0
    samples = 0
    t = 0.0
    while t < duration_s:
        dt = min(timestep_s, duration_s - t)
        speed = inflow.velocity_m_s(t + dt / 2)
        generation_kw = electrical_power_kw(turbine, speed)
        unconstrained_export_kwh += generation_kw * dt / 3600
        energy_kwh += min(generation_kw, cap_kw) * dt / 3600
        t += dt
        samples += 1
    return {
        "energy_kwh": energy_kwh,
        "uncapped_energy_kwh": unconstrained_export_kwh,
        "export_curtailment_kwh": unconstrained_export_kwh - energy_kwh,
        "capacity_factor_fraction": energy_kwh / (turbine.rated_power_kw * days * 24),
        "samples": samples,
        "duration_days": days,
        "timestep_s": timestep_s,
        "export_cap_kw": cap_kw,
    }
