"""Power bookkeeping for a heaving + pitching foil using *externally supplied* loads.

Not a hydrodynamic/structural solver. Forces [N], velocity [m/s], pitching
moment [N*m], angular speed [rad/s]; P = F_h * v_h + M * omega [W].
Positive means energy transferred FROM flow TO controlled mechanism. Sign convention
must match the instrument/kinematic dataset. Actuator and PTO losses are *not*
implicitly covered by measured power; the caller must supply them explicitly.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class FoilSample:
    time_s: float
    heave_force_n: float
    heave_velocity_m_s: float
    pitch_moment_n_m: float
    pitch_angular_rate_rad_s: float
    actuator_power_w: float
    conversion_losses_w: float


def instant_balance(row: FoilSample):
    for val in vars(row).values():
        if not isfinite(val):
            raise ValueError('Nonfinite input')
    if row.actuator_power_w < 0 or row.conversion_losses_w < 0:
        raise ValueError('Losses and actuator power must be nonnegative measured/assumed consumption')
    heave_w = row.heave_force_n * row.heave_velocity_m_s
    pitch_w = row.pitch_moment_n_m * row.pitch_angular_rate_rad_s
    gross_w = heave_w + pitch_w
    net_w = gross_w - row.actuator_power_w - row.conversion_losses_w
    return {'heave_w':heave_w,'pitch_w':pitch_w,'gross_mechanical_w':gross_w,
            'actuation_w':row.actuator_power_w,'conversion_loss_w':row.conversion_losses_w,
            'net_delivered_w':net_w}


def integrate(samples):
    """Trapezoidal integration; irregular timestamps acceptable with positivity check."""
    vals=list(samples)
    if len(vals)<2:raise ValueError('At least two samples are required')
    total={'gross_mechanical_j':0.0,'actuation_j':0.0,'conversion_loss_j':0.0,'net_delivered_j':0.0}
    for a,b in zip(vals,vals[1:]):
        dt=b.time_s-a.time_s
        if dt<=0 or not isfinite(dt):raise ValueError('Timestamps must be strictly increasing')
        aa,bb=instant_balance(a),instant_balance(b)
        for key,dest in (('gross_mechanical_w','gross_mechanical_j'),('actuation_w','actuation_j'),('conversion_loss_w','conversion_loss_j'),('net_delivered_w','net_delivered_j')):
            total[dest]+=0.5*(aa[key]+bb[key])*dt
    assert abs(total['gross_mechanical_j']-total['actuation_j']-total['conversion_loss_j']-total['net_delivered_j'])<1e-7*max(1.0,abs(total['gross_mechanical_j']))
    return total
