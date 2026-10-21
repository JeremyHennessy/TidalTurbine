"""Reproduce a bounded cross-speed RM2 Cp/Cd *point-estimate* comparison.

The archived input is a CC BY 4.0 selected subset of public UNH-CORE
processed performance CSV tables, at an immutable source commit. The original
RM2 1 m/s benchmark and SCREEN-001 are never changed.

No raw load time series, calibrated uncertainty test, controller parasitic
energy, blade/root stresses, device fatigue or field current is inferred.
"""
import argparse
import csv
from hashlib import sha1
from io import StringIO
import json
from math import isfinite
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIXTURE = ROOT / "research/benchmarks/RM2_CROSS_SPEED_SELECTED.csv"
OUTPUT = ROOT / "reports/RM2-CROSSSPEED-001.json"
UPSTREAM_COMMIT = "fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef"
UPSTREAM = "https://raw.githubusercontent.com/UNH-CORE/RM2-tow-tank/" + UPSTREAM_COMMIT + "/"
FIELDS = ("run", "tsr_nom", "mean_tow_speed_m_s", "mean_tsr", "mean_cp",
          "mean_cd", "exp_unc_cp", "exp_unc_cd", "n_revs")
ROLES = {"candidate_tsr_2p9", "reference_tsr_3p1", "series_max_reported_cp"}
CLASSIFICATION = "DESCRIPTIVE_PUBLISHED_PROCESSED_LAB_MULTISPEED_COMPARISON_NO_LOAD_VALIDATION"


def git_blob_sha(data):
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def series_rows():
    with SOURCE_FIXTURE.open(newline="", encoding="utf-8") as handle:
        raw = list(csv.DictReader(handle))
    if len(raw) != 30:
        raise ValueError("Expected 30 selected source rows (10 series x 3 roles)")
    groups = {}
    for row in raw:
        key = row["series_id"]
        groups.setdefault(key, []).append(row)
    expected = {f"RM2-{str(v).replace('.', 'p')}-{s}"
                for v in ("0.4", "0.6", "0.8", "1.0", "1.2")
                for s in ("A", "B")}
    if set(groups) != expected:
        raise ValueError("Missing/extra nominal speed series")
    for key, rows in groups.items():
        if len(rows) != 3 or {row["role"] for row in rows} != ROLES:
            raise ValueError("Each source series requires three observed roles")
        first = rows[0]
        path = first["source_path"]
        if not re.fullmatch(r"Data/Processed/Perf-(0[.]4|0[.]6|0[.]8|1[.]0|1[.]2)(-b)?[.]csv", path):
            raise ValueError("Unexpected upstream path")
        if not re.fullmatch("[0-9a-f]{40}", first["source_blob_sha"]):
            raise ValueError("Malformed upstream blob SHA")
        for row in rows:
            if any(row[x] != first[x] for x in
                   ("series_id", "source_path", "source_blob_sha",
                    "source_total_rows", "nominal_speed_m_s")):
                raise ValueError("Inconsistent metadata within source file")
            if any(not isfinite(float(row[x])) for x in FIELDS):
                raise ValueError("Unusable numeric field in source fixture")
            if int(float(row["source_total_rows"])) < 17:
                raise ValueError("Inconsistent upstream series size")
            if abs(float(row["mean_tow_speed_m_s"]) -
                   float(row["nominal_speed_m_s"])) > 0.05:
                raise ValueError("Source tow speed not close to label")
        a = next(row for row in rows if row["role"] == "candidate_tsr_2p9")
        b = next(row for row in rows if row["role"] == "reference_tsr_3p1")
        if (int(float(a["run"])), int(float(b["run"]))) != (10, 12):
            raise ValueError("Expected predeclared source run numbers 10 and 12")
        if abs(float(a["tsr_nom"]) - 2.9) > 1e-5 or abs(float(b["tsr_nom"]) - 3.1) > 1e-5:
            raise ValueError("Nominal TSR not matched")
        if abs(float(a["mean_tsr"]) - 2.9) > 0.02 or abs(float(b["mean_tsr"]) - 3.1) > 0.02:
            raise ValueError("Measured TSR deviates from the declared comparison")
    return groups


def verify_upstream(groups):
    """Optional one-time network verification, not needed by normal tests."""
    for name, rows in sorted(groups.items()):
        first = rows[0]
        url = UPSTREAM + first["source_path"]
        request = Request(url, headers={"User-Agent": "TidalTurbineResearchSourceReplay/1.0"})
        with urlopen(request, timeout=20) as response:
            data = response.read(1_000_000)
        if len(data) >= 1_000_000:
            raise ValueError("Source unexpectedly large: " + name)
        actual = git_blob_sha(data)
        if actual != first["source_blob_sha"]:
            raise ValueError(f"Upstream source blob mismatch for {name}: {actual}")
        upstream_rows = list(csv.DictReader(StringIO(data.decode("utf-8"), newline="")))
        if len(upstream_rows) != int(float(first["source_total_rows"])):
            raise ValueError("Upstream row count changed: " + name)
        for selected in rows:
            run = int(float(selected["run"]))
            matches = [r for r in upstream_rows if int(float(r["run"])) == run]
            if len(matches) != 1:
                raise ValueError("Upstream source run missing or duplicated: " + name)
            source = matches[0]
            for local, remote in (
                ("tsr_nom", "tsr_nom"), ("mean_tow_speed_m_s", "mean_tow_speed"),
                ("mean_tsr", "mean_tsr"), ("mean_cp", "mean_cp"), ("mean_cd", "mean_cd"),
                ("exp_unc_cp", "exp_unc_cp"), ("exp_unc_cd", "exp_unc_cd"),
                ("n_revs", "n_revs")):
                if selected[local] != source[remote]:
                    raise ValueError(f"Upstream raw value mismatch: {name} {run} {local}")
            if selected["role"] == "series_max_reported_cp":
                max_row = max(upstream_rows, key=lambda r: float(r["mean_cp"]))
                if int(float(max_row["run"])) != run:
                    raise ValueError("Incorrect post-hoc Cp maximum: " + name)
        print(f"Source verified: {name} ({len(data)} bytes, {actual})")


def row_values(row):
    return {
        "source_run": int(float(row["run"])),
        "nominal_tsr": float(row["tsr_nom"]),
        "observed_mean_tsr": float(row["mean_tsr"]),
        "observed_mean_tow_speed_m_s": float(row["mean_tow_speed_m_s"]),
        "mean_cp": float(row["mean_cp"]),
        "mean_cd": float(row["mean_cd"]),
        "upstream_exp_unc_cp": float(row["exp_unc_cp"]),
        "upstream_exp_unc_cd": float(row["exp_unc_cd"]),
        "n_complete_revolutions": int(float(row["n_revs"])),
    }


def generate():
    groups = series_rows()
    comparisons = []
    for series_id in sorted(groups):
        rows = groups[series_id]
        by_role = {r["role"]: r for r in rows}
        a = row_values(by_role["candidate_tsr_2p9"])
        b = row_values(by_role["reference_tsr_3p1"])
        peak = row_values(by_role["series_max_reported_cp"])
        if b["mean_cp"] <= 0 or b["mean_cd"] <= 0 or peak["mean_cp"] <= 0:
            raise ValueError("Expected positive reference coefficients")
        comparisons.append({
            "series_id": series_id,
            "nominal_tow_speed_m_s": float(rows[0]["nominal_speed_m_s"]),
            "source_path": rows[0]["source_path"],
            "source_git_blob_sha": rows[0]["source_blob_sha"],
            "source_full_table_rows": int(float(rows[0]["source_total_rows"])),
            "candidate_tsr_2p9": a,
            "reference_tsr_3p1": b,
            "posthoc_source_series_max_cp": {
                "source_run": peak["source_run"],
                "observed_mean_tsr": peak["observed_mean_tsr"],
                "mean_cp": peak["mean_cp"],
            },
            "candidate_relative_to_tsr3p1": {
                "mechanical_cp_point_decrease_percent":
                    round(100 * (1 - a["mean_cp"] / b["mean_cp"]), 4),
                "mean_streamwise_cd_point_decrease_percent":
                    round(100 * (1 - a["mean_cd"] / b["mean_cd"]), 4),
            },
            "candidate_relative_to_posthoc_series_max_cp": {
                "mechanical_cp_point_decrease_percent":
                    round(100 * (1 - a["mean_cp"] / peak["mean_cp"]), 4),
            },
        })
    nc = sum(x["candidate_tsr_2p9"]["mean_cp"] < x["reference_tsr_3p1"]["mean_cp"]
             for x in comparisons)
    nd = sum(x["candidate_tsr_2p9"]["mean_cd"] < x["reference_tsr_3p1"]["mean_cd"]
             for x in comparisons)
    return {
        "id": "RM2-CROSSSPEED-001",
        "classification": CLASSIFICATION,
        "source": {
            "repository": "UNH-CORE/RM2-tow-tank",
            "source_immutable_commit": UPSTREAM_COMMIT,
            "original_processed_file_license": "CC BY 4.0; Bachant, Wosnik, Gunawan, Neary",
            "doi": "10.6084/m9.figshare.1373899",
            "reduced_fixture_git_blob_sha": git_blob_sha(SOURCE_FIXTURE.read_bytes()),
            "selected_raw_numeric_fields": "3 published processed rows per each of 10 original tables; 2 comparison runs + observed series Cp maximum",
        },
        "question": "How sensitive is the published same-rotor mechanical mean Cp-versus-mean streamwise Cd point-estimate change at nominal TSR 2.9 versus 3.1 to different controlled tow speeds?",
        "comparison_protocol": {
            "candidate_tsr_nominal": 2.9,
            "reference_tsr_nominal": 3.1,
            "selection": "predeclared comparison of nominal runs 10 vs 12 in each speed/series; no curve fit or reoptimization",
            "series": "Published first and second performance curves (A and B) are not assumed independent population replicates.",
            "posthoc_maximum_caveat": "Each series' observed point-estimate Cp maximum is descriptive and was selected from the full file, not a validated true optimum.",
        },
        "series_count": len(comparisons),
        "nominal_tow_speeds_m_s": [0.4, 0.6, 0.8, 1.0, 1.2],
        "descriptive_sign_count": {
            "candidate_cp_lower_than_reference": nc,
            "candidate_cd_lower_than_reference": nd,
        },
        "series": comparisons,
        "observed_finding": "All ten source-series point estimates show lower Cp and Cd at nominal TSR 2.9 than at 3.1, but the relative Cp penalty changes strongly with tow speed. A near-2% Cp cost at 1 m/s is not a universal derating rule.",
        "uncertainty_and_limits": [
            "Values copied from upstream previously processed freshwater laboratory means; no raw torque, blade or support strain reprocessing.",
            "The original exp_unc_cp and exp_unc_cd fields are reproduced verbatim and are NOT recomputed or interpreted here as paired-difference confidence intervals.",
            "Series A and B are two tow-tank performance sweeps with varying Reynolds number and possibly uncorrected tank blockage, not independent turbines or generalized sea-state statistics.",
            "None of the observed coefficient differences establishes statistical significance, net delivered electricity, controller energy, alternating structural load, fatigue damage, lifecycle benefit or field extrapolation.",
            "The comparison at fixed nominal TSR 3.1 is not necessarily the observed Cp maximum in each speed series; a distinct post-hoc maximum is reported as context only.",
            "No scientifically qualified FORCE/CMAR site-specific inflow was used; do not feed the table into site energy/loads or equate unlike RM1 and RM2 Cp denominators.",
        ],
        "decision": "Reject universal low-cost mechanical derating inference from the single 1 m/s RM2 series. Preregister matched-speed and turbulence-controlled cyclic-load, power and actuator-energy tests before recommending a controller or design winner.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-upstream", action="store_true",
                        help="Opt-in: network-fetch 10 pinned source files and compare selected values and source Git blobs")
    parser.add_argument("--check", action="store_true",
                        help="Compare generated report with committed JSON without editing the source tree")
    args = parser.parse_args()
    if args.verify_upstream:
        verify_upstream(series_rows())
    result = generate()
    if args.check:
        previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if previous != result:
            raise ValueError("Archived report differs from reproducible selected source values")
    else:
        OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"RM2 cross-speed report: {result['series_count']} processed series, "
          f"Cp lower in {result['descriptive_sign_count']['candidate_cp_lower_than_reference']}, "
          f"Cd lower in {result['descriptive_sign_count']['candidate_cd_lower_than_reference']}; "
          "NO structural, statistical, field or net-electricity validation")


if __name__ == "__main__":
    main()
