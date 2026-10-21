"""Independent, source-hash-pinned seven-day processed ADCP profile QC.
No source-native beam validation; zero approved turbine-inflow rows.
Original source files remain outside Git in a short-lived Actions artifact.
"""
import argparse
import hashlib
import json
import math
import statistics
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

SOURCES = {
    "DG012": {"sha256": "c7c3cf3863816e710d61c8079b8fa0ee2a17702917f2f30047bd9f07a4a1bb0d",
              "rows": 10463, "station": "Grand Passage", "label": "Grand Passage",
              "wgs84": [44.27359, -66.3424], "year": 2020},
    "DG002": {"sha256": "70a36f119439d5c1bddedb318b819001d3c8b517eb92cfa85ff3ec8dd60658fb",
              "rows": 11409, "station": "Petite Passage", "label": "Petit Passage",
              "wgs84": [44.3662, -66.2083], "year": 2010},
}
FIELDS = {"deployment_id", "station", "datetime", "bin_height_above_sea_floor_m",
          "bin_depth_below_surface_m", "sea_water_speed_m_s",
          "sea_water_to_direction_degree", "qc_flag_sea_water_speed_m_s",
          "qc_flag_sea_water_to_direction_degree", "qc_flag_sensor_depth_below_surface_m"}
ALLOWED_FLAGS = {"Pass", "Suspect/Of Interest", "Fail", "Not Evaluated"}

def summarize(original_bytes, deployment):
    info = SOURCES[deployment]
    assert hashlib.sha256(original_bytes).hexdigest() == info["sha256"], "Source hash changed"
    rows = json.loads(original_bytes)
    assert len(rows) == info["rows"], "Source row count changed"
    assert all(FIELDS <= r.keys() for r in rows)
    assert all(r["deployment_id"] == deployment and r["station"] == info["station"] for r in rows)
    flags = {k: Counter() for k in ("speed", "direction", "depth")}
    bin_counts, times, seen, pass_speeds = Counter(), set(), set(), []
    for r in rows:
        t = datetime.fromisoformat(r["datetime"])
        assert t.tzinfo is None, "Source timestamp format changed"
        height = float(r["bin_height_above_sea_floor_m"])
        numeric = [height, float(r["bin_depth_below_surface_m"]),
                   float(r["sea_water_speed_m_s"]), float(r["sea_water_to_direction_degree"])]
        assert all(math.isfinite(v) for v in numeric)
        assert numeric[2] >= 0 and 0 <= numeric[3] <= 360
        key = (r["datetime"], height)
        assert key not in seen, "Duplicate observation/time-bin"
        seen.add(key)
        times.add(t)
        bin_counts[height] += 1
        for label, field in [("speed", "qc_flag_sea_water_speed_m_s"),
                             ("direction", "qc_flag_sea_water_to_direction_degree"),
                             ("depth", "qc_flag_sensor_depth_below_surface_m")]:
            flag = r[field]
            assert flag in ALLOWED_FLAGS, "Unknown source quality flag"
            flags[label][flag] += 1
        if r["qc_flag_sea_water_speed_m_s"] == "Pass":
            pass_speeds.append(numeric[2])
    intervals = Counter(int((b-a).total_seconds()) for a,b in zip(sorted(times), sorted(times)[1:]))
    pass_speeds.sort()
    return {
        "deployment_id": deployment, "site": info["label"], "source_year": info["year"],
        "metadata_position_wgs84_approx": info["wgs84"],
        "source_sha256": info["sha256"], "source_rows": len(rows),
        "original_time_range": [min(r["datetime"] for r in rows), max(r["datetime"] for r in rows)],
        "source_datetime_offset_unverified": True,
        "n_unique_times": len(times),
        "interval_counts_seconds": {str(k): v for k,v in sorted(intervals.items())},
        "heights_above_sea_floor_m": sorted(bin_counts),
        "samples_per_height": {str(k):v for k,v in sorted(bin_counts.items())},
        "quality_flag_counts": {k:dict(sorted(v.items())) for k,v in flags.items()},
        "publisher_speed_pass_rows": len(pass_speeds),
        "publisher_pass_speed_descriptive_m_s": {
            "median": round(statistics.median(pass_speeds), 6),
            "p95_nearest_rank": round(pass_speeds[math.ceil(.95*len(pass_speeds))-1],6)},
        "native_beam_qc_verified": False, "model_eligible_rows": 0
    }

def analyze(archive):
    with zipfile.ZipFile(archive) as z:
        result=[]
        for deployment in SOURCES:
            name=deployment+"_7d_profiles.json"
            assert name in z.namelist()
            assert z.getinfo(name).file_size < 10000000
            result.append(summarize(z.read(name), deployment))
    return {"id":"NS-PASSAGES-7D-QA-001",
      "evidence_class":"PUBLISHED_PROCESSED_MEASURED_OCEAN_DATA_NUMERICAL_QC_ONLY",
      "source_url":"https://data.novascotia.ca/resource/is3b-ip8b.json",
      "licence":"Nova Scotia Open Government Licence; attribute CMAR/Nova Scotia",
      "sites":result,"records":sum(x["source_rows"] for x in result),
      "model_eligible_rows":0,"site_energy_prediction":"NOT_AUTHORIZED",
      "limitations":["Different sites, years, depth bins and short historical windows",
                     "Publisher Pass flag is not source-native correlation/beam/orientation QC",
                     "Source datetime offset must be independently confirmed",
                     "No verified rotor-depth aggregation or site authorization"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--out",default="reports/NS-PASSAGES-7D-QA-001.json")
    args=p.parse_args()
    result=analyze(args.archive)
    dest=Path(args.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("Verified processed profiles:",result["records"],"model eligible:",result["model_eligible_rows"])

if __name__=="__main__":
    main()
