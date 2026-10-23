"""Fail-closed, read-only overlap screen for *locally supplied* 2022 UNH sensor slices.

No network, remote retries, zip downloads, file mutations or physical claims.
The only possible positive output is TIMESTAMP CANDIDATES, subject to separate
human verification of README, calibration, QC, drift, geometry and meter boundary.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/UNH_2022_SOURCE_ACCESS_001.json"
MAX_MANIFEST_BYTES = 512_000
MAX_CSV_BYTES = 8_000_000
MAX_ROWS_PER_STREAM = 100_000
EXPECTED_UNITS = {
    "STRAIN": "microstrain", "FLOW_ADCP": "m/s", "FLOW_ADV": "m/s",
    "THRUST": "N", "VOLTSYS": "W",
}
REQUIRED_ROLE_BASE = {"STRAIN", "THRUST", "VOLTSYS"}
FLOW_ROLES = {"FLOW_ADCP", "FLOW_ADV"}
DOC_FIELDS = (
    "original_archive_sha256", "source_readme_sha256",
    "calibration_evidence_sha256", "quality_evidence_sha256",
    "clock_evidence_sha256", "processing_manifest_sha256",
)
FIRST_CAMPAIGN_DAY = datetime(2022, 10, 25, tzinfo=timezone.utc)
DAY_AFTER_CAMPAIGN = datetime(2022, 12, 13, tzinfo=timezone.utc)


class SourceEligibilityError(ValueError):
    """No scientific authorization can be inferred from deficient metadata."""


def require(ok: bool, message: str):
    if not ok:
        raise SourceEligibilityError(message)


def source_registry(data=None):
    """Check publisher resources independently of any candidate measurement."""
    if data is None:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(data.get("schema") == "TT-UNH-2022-ACCESS-GATE-001"
            and data.get("dataset_id") == "DOE-UNH-STRAIN-CATALOG-008",
            "Unexpected source registry or campaign")
    require(data.get("publisher_doi") == "10.15473/2481243"
            and data.get("catalog_resource_count") == 17
            and data.get("campaign_start_date") == "2022-10-25"
            and data.get("campaign_end_date") == "2022-12-12",
            "2022 source provenance does not match catalogued metadata")
    require(data.get("source_differentiation", "").find("2021") >= 0,
            "Do not mistake this field campaign for 2021 UNH or older RM2")
    require(data.get("verified_original_archives") == 0
            and data.get("verified_original_readmes") == 0
            and data.get("verified_utc_sensor_timestamps") == 0
            and data.get("scientifically_qualified_common_windows") == 0
            and data.get("qualified_blade_stress_runs") == 0
            and data.get("qualified_net_electricity_runs") == 0
            and data.get("current_status") == "BLOCKED_ORIGINAL_SOURCE_HTTP_429"
            and data.get("contact_authorized") is False
            and data.get("source_bypass_authorized") is False
            and data.get("automated_original_downloads") is False,
            "No original measured time-series or authorization exists")
    expected = {"STRAIN", "FLOW_ADCP", "FLOW_ADV", "THRUST", "VOLTSYS", "IMU"}
    streams = data.get("streams")
    require(isinstance(streams, list) and len(streams) == 6
            and {s.get("id") for s in streams} == expected,
            "Six original instrument families required")
    for s in streams:
        require(s.get("source_archive_url", "").startswith(
                "https://mhkdr.openei.org/files/569/")
            and s.get("source_readme_url", "").startswith(
                "https://mhkdr.openei.org/files/569/")
            and all(s.get(k) is None for k in (
                "source_archive_sha256", "source_readme_sha256",
                "source_clock_epoch", "source_calibration", "source_native_qc",
                "instrument_specific_operating_intervals"))
            and s.get("raw_samples_acquired") == 0,
            "Original instrument bytes or clocks must not be asserted")
    require(len(data.get("access_checks", [])) >= 4
            and all(x.get("result") == "HTTP_429"
                    and x.get("original_bytes_acquired") is False
                    for x in data["access_checks"]),
            "Blocked source access evidence must be preserved")
    return data


def blocked_status(data=None):
    source = source_registry(data)
    return {
        "status": "BLOCKED_NO_ORIGINAL_2022_SENSOR_FILES_OR_CLOCK_QC",
        "source_class": source["classification"],
        "dataset_id": source["dataset_id"],
        "publisher_doi": source["publisher_doi"],
        "catalogued_resources": source["catalog_resource_count"],
        "original_archives_acquired": 0,
        "scientifically_qualified_windows": 0,
        "candidate_timestamp_windows": [],
        "instrument_specific_operating_windows_known": False,
        "source_native_calibration_qc_clocks_known": False,
        "contact_authorized": False,
        "physical_validation": False,
        "reason": "Publisher original READMEs/schedule returned HTTP429. "
                  "Campaign start/end dates are NOT simultaneous measured samples."
    }


def _sha256_string(value, field):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
            "Missing/invalid pinned SHA-256 evidence: " + field)
    return value


def _real(value, label, positive=False):
    require(type(value) in (int, float) and math.isfinite(value),
            "Invalid finite real: " + label)
    require(value > 0 if positive else value >= 0, "Negative/zero value: " + label)
    return float(value)


def _safe_file(root: Path, path: str, max_bytes: int) -> bytes:
    require(isinstance(path, str) and path.strip() != "",
            "Missing local source path")
    relative = Path(path)
    require(not relative.is_absolute() and ".." not in relative.parts,
            "Unsafe absolute or parent-traversing source path")
    root = root.resolve(strict=True)
    location = root.joinpath(relative)
    require(location.resolve(strict=True).is_relative_to(root),
            "Source path escapes local manifest directory")
    # Symlinks are disallowed even if they happen to resolve inside root.
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), "Symlink source paths not accepted")
    require(location.is_file() and 0 < location.stat().st_size <= max_bytes,
            "Source missing/empty or exceeds bounded input bytes")
    data = location.read_bytes()
    require(0 < len(data) <= max_bytes, "Bounded read failed")
    return data


def _utc_timestamp(raw):
    require(isinstance(raw, str) and (
            raw.endswith("Z") or raw.endswith("+00:00")),
            "Timestamp requires explicit UTC Z or +00:00; never infer timezone")
    try:
        stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SourceEligibilityError("Malformed explicit UTC timestamp") from exc
    require(stamp.utcoffset() == timedelta(0)
            and FIRST_CAMPAIGN_DAY <= stamp < DAY_AFTER_CAMPAIGN,
            "Timestamp is outside 2022 deployment date range or non-UTC")
    return stamp.astimezone(timezone.utc)


def _segments(records, gap_s, clock_error_s):
    segments = []
    left = previous = None

    def flush():
        if left is None or previous is None:
            return
        # Clock-error budget trims BOTH edges rather than creating fake overlap.
        first = left + timedelta(seconds=clock_error_s)
        last = previous - timedelta(seconds=clock_error_s)
        if last > first:
            segments.append((first, last))

    for timestamp, is_good in records:
        if not is_good:
            flush()
            left = previous = None
        elif previous is None:
            left = previous = timestamp
        elif (timestamp - previous).total_seconds() > gap_s:
            flush()
            left = previous = timestamp
        else:
            previous = timestamp
    flush()
    return segments


def _intersect(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        left = max(a[i][0], b[j][0])
        right = min(a[i][1], b[j][1])
        if right > left:
            out.append((left, right))
        if a[i][1] <= b[j][1]:
            i += 1
        else:
            j += 1
    return out


def _parse_stream(entry, allowed_url, root):
    role = entry["role"]
    require(entry.get("source_archive_url") == allowed_url,
            "Archive identity mismatch, or prohibited 2021/other source mixing")
    for field in DOC_FIELDS:
        _sha256_string(entry.get(field), role + "." + field)
    if role.startswith("FLOW_"):
        _sha256_string(entry.get("flow_geometry_evidence_sha256"),
                       role + ".flow_geometry_evidence_sha256")
    if role == "VOLTSYS":
        _sha256_string(entry.get("meter_boundary_evidence_sha256"),
                       role + ".meter_boundary_evidence_sha256")
    require(entry.get("declared_si_unit") == EXPECTED_UNITS[role],
            "SI unit mismatch for " + role + ": no guessed conversions")
    for key in ("timestamp_column", "quality_column", "good_quality_token",
                "bad_quality_token"):
        require(isinstance(entry.get(key), str) and entry[key].strip() != "",
                "Missing explicit source column/QC mapping for " + role + "." + key)
    good, bad = entry["good_quality_token"], entry["bad_quality_token"]
    require(good != bad, "Accepted and rejected quality tokens must differ")
    columns = entry.get("value_columns")
    require(isinstance(columns, list) and len(columns) >= (
                3 if role.startswith("FLOW_") else 1)
            and all(isinstance(s, str) and s.strip() for s in columns)
            and len(set(columns)) == len(columns),
            "Missing/duplicate source measurement columns for " + role)
    names = [entry["timestamp_column"], entry["quality_column"], *columns]
    require(len(names) == len(set(names)), "Measurement/QC/timestamp column overlap")
    gap = _real(entry.get("max_contiguous_gap_seconds"),
                role + ".max_contiguous_gap_seconds", positive=True)
    clock = _real(entry.get("clock_uncertainty_seconds"),
                  role + ".clock_uncertainty_seconds")
    data = _safe_file(root, entry.get("csv_relative_path"), MAX_CSV_BYTES)
    actual_hash = hashlib.sha256(data).hexdigest()
    require(actual_hash == _sha256_string(entry.get("csv_sha256"), role + ".csv_sha256"),
            "Local CSV hash does not match its pinned provenance for " + role)
    try:
        decoded = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SourceEligibilityError("CSV encoding is not UTF-8") from exc
    reader = csv.DictReader(io.StringIO(decoded, newline=""))
    require(reader.fieldnames is not None
            and len(reader.fieldnames) == len(set(reader.fieldnames))
            and set(names) <= set(reader.fieldnames),
            "CSV missing required or duplicate columns for " + role)
    records = []
    valid = rejected = 0
    last_time = None
    for index, row in enumerate(reader, start=1):
        require(index <= MAX_ROWS_PER_STREAM, "Sample count exceeds short local slice bound")
        require(None not in row, "CSV row has extra columns")
        time = _utc_timestamp(row[entry["timestamp_column"]])
        require(last_time is None or time > last_time,
                "Duplicate/reordered source timestamps for " + role)
        last_time = time
        flag = row[entry["quality_column"]]
        require(flag in (good, bad),
                "Undeclared/missing native quality marker for " + role)
        accepted = flag == good
        if accepted:
            try:
                values = [float(row[name]) for name in columns]
            except (TypeError, ValueError) as exc:
                raise SourceEligibilityError("Unparseable accepted source value") from exc
            require(all(math.isfinite(v) for v in values),
                    "Nonfinite accepted source value")
            valid += 1
        else:
            rejected += 1
        records.append((time, accepted))
    require(records, "No samples in selected local slice for " + role)
    return {
        "role": role, "total_samples": len(records),
        "accepted_sample_count": valid, "rejected_sample_count": rejected,
        "candidate_segments": _segments(records, gap, clock),
        "raw_local_clip_sha256_verified": True,
        "original_source_calibration_reviewed_by_program": False
    }


def candidate_intersections(manifest, source_root: Path, registry=None):
    """Return PROVISIONAL time-label intersections, never source qualification."""
    source = source_registry(registry)
    require(manifest.get("schema") == "TT-UNH-2022-LOCAL-CLIPS-V1"
            and manifest.get("dataset_id") == source["dataset_id"]
            and manifest.get("classification") ==
                "USER_SUPPLIED_SOURCE_SLICES_NOT_SCIENTIFICALLY_VALIDATED",
            "User-held short-slice manifest identity/classification required")
    minimum = _real(manifest.get("screen_minimum_seconds"),
                    "screen_minimum_seconds", positive=True)
    entries = manifest.get("streams")
    require(isinstance(entries, list) and len(entries) == 4,
            "Exactly four source families needed: strain, one flow, thrust, Voltsys")
    roles = [entry.get("role") for entry in entries]
    require(set(roles) >= REQUIRED_ROLE_BASE and len(set(roles)) == 4
            and len(set(roles) & FLOW_ROLES) == 1
            and set(roles) <= REQUIRED_ROLE_BASE | FLOW_ROLES,
            "Wrong source roles or multiple flow instruments")
    originals = {x["id"]: x["source_archive_url"] for x in source["streams"]}
    parsed = [_parse_stream(entry, originals[entry["role"]], source_root)
              for entry in entries]
    windows = parsed[0]["candidate_segments"]
    for stream in parsed[1:]:
        windows = _intersect(windows, stream["candidate_segments"])
        if not windows:
            break
    windows = [(a, b) for a, b in windows
               if (b - a).total_seconds() >= minimum]
    out = []
    for a, b in windows:
        out.append({
            "candidate_start_utc": a.isoformat().replace("+00:00", "Z"),
            "candidate_end_utc": b.isoformat().replace("+00:00", "Z"),
            "time_label_overlap_seconds": (b - a).total_seconds(),
            "clock_and_native_qc_independently_confirmed": False
        })
    return {
        "status": ("LOCAL_TIMESTAMP_OVERLAP_CANDIDATES_REVIEW_REQUIRED"
                   if out else "NO_TIMESTAMP_OVERLAP_IN_SUPPLIED_BOUNDED_SLICES"),
        "dataset_id": source["dataset_id"],
        "candidate_timestamp_windows": out,
        "scientifically_qualified_windows": 0,
        "original_source_readmes_verified_by_program": False,
        "calibration_and_clock_evidence_reviewed_by_program": False,
        "flow_geometry_and_representativeness_verified": False,
        "platform_inertial_load_compensation_verified": False,
        "signed_net_system_electricity_verified": False,
        "physical_fatigue_or_power_validation": False,
        "external_contact_authorized": False,
        "minimum_screen_seconds_is_not_a_scientific_acceptance_threshold": minimum,
        "stream_counts": [{
            "role": x["role"], "total_samples": x["total_samples"],
            "accepted": x["accepted_sample_count"],
            "rejected": x["rejected_sample_count"],
            "separate_candidate_segments": len(x["candidate_segments"])
        } for x in parsed],
        "warning": "At most overlapping user-supplied UTC labels. Pinned evidence strings "
                   "do NOT authenticate source documentation or establish clock physics; "
                   "independent calibration, source QC, load transfer, electrical boundary "
                   "and review remain mandatory."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, help="Explicit local short-slice manifest; no network")
    args = parser.parse_args()
    try:
        if args.manifest is None:
            output = blocked_status()
        else:
            require(args.manifest.is_file() and not args.manifest.is_symlink()
                    and args.manifest.stat().st_size <= MAX_MANIFEST_BYTES,
                    "Missing/unsafe or oversized manifest")
            manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
            output = candidate_intersections(manifest, args.manifest.parent)
        print(json.dumps(output, indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("SOURCE QUALIFICATION BLOCKED: " + str(exc), file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
