"""Run a deterministic, labelled, synthetic electricity screening experiment."""

import argparse
from dataclasses import asdict, replace
from datetime import date
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
import sys

from .model import SyntheticCurrent, Turbine, integrate


def run(config: dict) -> dict:
    if config.get("inflow_kind") != "synthetic_two_harmonic":
        raise ValueError("only clearly-labelled synthetic_two_harmonic inflow is supported")
    turbine = Turbine(**config["turbine"])
    inflow = SyntheticCurrent(**config["current"])
    days = float(config["duration_days"])
    step = float(config["timestep_s"])
    cap = float(config["comparison_export_cap_fraction"])
    baseline = integrate(turbine, inflow, days, step)
    comparison = integrate(turbine, inflow, days, step, cap)
    sensitivity = []
    axes = config["sensitivity"]
    for amp, cp, efficiency, rated in product(
        axes["primary_amplitude_m_s"], axes["power_coefficient"],
        axes["conversion_efficiency"], axes["rated_power_kw"]
    ):
        case = integrate(replace(turbine, power_coefficient=cp,
                                 conversion_efficiency=efficiency,
                                 rated_power_kw=rated),
                         replace(inflow, primary_amplitude_m_s=amp), days, step)
        sensitivity.append({"primary_amplitude_m_s": amp, "power_coefficient": cp,
                            "conversion_efficiency": efficiency, "rated_power_kw": rated,
                            "energy_kwh": round(case["energy_kwh"], 5)})
    half = integrate(turbine, inflow, days, step / 2)
    quarter = integrate(turbine, inflow, days, step / 4)
    return {
        "experiment_id": config["experiment_id"],
        "classification": "SIMULATION_RESULT_SYNTHETIC_NOT_VALIDATED",
        "question": "How much synthetic export energy is lost by an electrical export cap?",
        "inflow_kind": config["inflow_kind"],
        "inflow_provenance": "Two assumed sinusoidal components; NOT measured; NOT a Fundy or RM1 reconstruction",
        "turbine_provenance": "All nominal turbine values are engineering assumptions, not a product specification",
        "equation": "P_export=min(P_rated * cap_fraction, min(P_rated, (rho*A*Cp*eta*abs(u)^3)/(2*1000))) above cut-in; otherwise 0 kW",
        "turbine": {**asdict(turbine), "swept_area_m2": turbine.swept_area_m2},
        "synthetic_current": asdict(inflow),
        "baseline": baseline,
        "comparison": comparison,
        "difference_export_energy_kwh": baseline["energy_kwh"] - comparison["energy_kwh"],
        "difference_export_energy_percent": 100 * (baseline["energy_kwh"] - comparison["energy_kwh"]) / baseline["energy_kwh"] if baseline["energy_kwh"] else 0,
        "time_step_convergence": {
            "timestep_s": step, "energy_kwh": baseline["energy_kwh"],
            "half_timestep_s": step / 2, "half_energy_kwh": half["energy_kwh"],
            "quarter_timestep_s": step / 4, "quarter_energy_kwh": quarter["energy_kwh"],
            "relative_error_half_vs_quarter": abs(half["energy_kwh"] - quarter["energy_kwh"]) / quarter["energy_kwh"] if quarter["energy_kwh"] else 0,
        },
        "sensitivity": sensitivity,
        "sensitivity_ranges_are_assumed": True,
        "uncertainty": "Parameter ranges are assumed sensitivities, not confidence bounds, calibrated measurement errors or predictions.",
        "supported_decision": "Quantify electrical export-cap energy penalty for the *assumed* power curve and synthetic inflow.",
        "cannot_establish": ["thrust or changes in rotor loads", "fatigue life or device availability", "economic benefit", "physical feasibility of the curtailed operating state", "environmental safety", "site resource or grid adequacy"],
        "software": {"python": platform.python_version(), "implementation": platform.python_implementation(), "stdlib_only": True},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/synthetic_screen.json")
    parser.add_argument("--out", default="reports/latest.json")
    args = parser.parse_args(argv)
    config_path = Path(args.config)
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    report = run(config)
    report["run_provenance"] = {
        "config_path": args.config,
        "config_sha256": sha256(config_bytes).hexdigest(),
        "model_sha256": sha256(Path(__file__).with_name("model.py").read_bytes()).hexdigest(),
        "cli_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "code_revision": "See commit containing this report; source-file hashes above uniquely identify run code",
        "command": f"python -m tidal_screen.cli --config {args.config} --out {args.out}",
        "report_generation_date_utc": date.today().isoformat(),
    }
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(f"Synthetic baseline: {report['baseline']['energy_kwh']:.3f} kWh; "
          f"capped: {report['comparison']['energy_kwh']:.3f} kWh; "
          f"export energy reduction: {report['difference_export_energy_percent']:.3f}%")
    print(f"Wrote {output} (NOT a load/fatigue prediction)")


if __name__ == "__main__":
    main()
