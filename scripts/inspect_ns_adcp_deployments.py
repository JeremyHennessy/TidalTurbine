"""Read-only discovery of current-and-wave ADCP deployment *metadata* in Nova Scotia.

2026 official public CMAR/NSDFA deployment catalogue (Socrata uban-q9i2).
Proximity to a suggested test site does not mean currents qualify at a berth.
No quality-approved velocity, permitting, site ownership or physical work.
"""
import argparse,csv,json,io,math
from collections import Counter
from datetime import datetime,timezone
from urllib.request import Request,urlopen

SOURCE="https://data.novascotia.ca/api/views/uban-q9i2/rows.csv?accessType=DOWNLOAD"
SITE_REFERENCES={
 "Grand Passage regional reference":{"lat":44.270,"lon":-66.340},
 "Petit Passage regional reference":{"lat":44.370,"lon":-66.210},
 "Rocky Run bridge map reference":{"lat":44.644,"lon":-63.314},
 "Digby Gut regional reference":{"lat":44.685,"lon":-65.756}
}
MAX_BYTES=8_000_000

def distance_km(a,b,c,d):
    radius=6371.
    dlat=math.radians(c-a)
    dlon=math.radians(d-b)
    f=math.sin(dlat/2)**2+math.cos(math.radians(a))*math.cos(math.radians(c))*math.sin(dlon/2)**2
    return 2*radius*math.asin(min(1.,math.sqrt(f)))

def safe_float(x):
    try:
        if x not in (None,"","null"):
            v=float(x)
            if math.isfinite(v):return v
    except (ValueError,TypeError):pass
    return None

def inspect(path):
    raw=path.read_bytes()
    if len(raw)>MAX_BYTES:raise ValueError("Downloaded metadata exceeded explicit byte cap")
    content=raw.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(content))
    fields=reader.fieldnames or []
    rows=list(reader)
    if not fields or not rows:raise ValueError("No structured deployment records")
    coords=[]
    latkeys=[k for k in fields if "lat" in k.lower()]
    lonkeys=[k for k in fields if "lon" in k.lower()]
    for i,r in enumerate(rows):
        latitude=next((safe_float(r.get(k)) for k in latkeys if safe_float(r.get(k)) is not None),None)
        longitude=next((safe_float(r.get(k)) for k in lonkeys if safe_float(r.get(k)) is not None),None)
        if latitude is not None and longitude is not None and 40<=latitude<=49 and -71<=longitude<=-59:
            coords.append((i,latitude,longitude))
    hits={}
    for name,target in SITE_REFERENCES.items():
        located=sorted(((distance_km(target["lat"],target["lon"],y,z),idx,y,z) for idx,y,z in coords),key=lambda t:t[0])
        selected=[]
        for dist,idx,y,z in located[:7]:
            if dist>25:continue
            original=rows[idx]
            details={k:original[k] for k in fields
                     if any(term in k.lower() for term in
                            ("deployment","station","county","instrument","waterbody","current","quality","sensor","start","end","serial"))}
            selected.append({"distance_from_regional_reference_km":round(dist,3),
                             "source_table_row_index_zero_based":idx,
                             "lat_deg_n":y,"lon_deg_e":z,
                             "reported_metadata":details})
        hits[name]={"within_25_km_count":sum(x[0]<=25 for x in located),
                    "nearest_7_max_25km":selected}
    return {"id":"NS-ADCP-DEPLOYMENT-DISCOVERY-001",
        "classification":"OFFICIAL_DEPLOYMENT_METADATA_PROXIMITY_NOT_QUALIFIED_TURBINE_INFLOW",
        "official_source":SOURCE,
        "licence":"Nova Scotia Open Government Licence, attribute Nova Scotia / Centre for Marine Applied Research",
        "retrieved_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "raw_table_bytes":len(raw),"dataset_rows":len(rows),"fields":fields,
        "rows_with_basic_numeric_ns_coordinates":len(coords),
        "reference_note":"Approximate historical regional points only, not proposed turbine berth coordinates",
        "proximity":hits,
        "source_native_beam_flags_recovered":False,
        "candidate_rotor_depth_series_qualified":0,
        "model_eligible_rows":0,
        "required_next":["Verify original station/deployment identity, raw ADCP profile product, instrument heading/tilt/beam quality and vertical datum","Verify actual site candidate coordinates, depth, owner/operator, fisheries rights, authorized work and retrieval","Never use geographic proximity or wave/sensor-speed summaries as proof of a usable turbine inflow"]}

def main():
    from pathlib import Path
    a=argparse.ArgumentParser()
    a.add_argument("--acquire",action="store_true")
    a.add_argument("--out",default="data/local/ns-adcp-discovery")
    opts=a.parse_args()
    if not opts.acquire:
        print(json.dumps({"mode":"DRY_RUN_NO_NETWORK","official_source":SOURCE,"model_eligible_rows":0}));return
    root=Path(opts.out);root.mkdir(parents=True,exist_ok=True)
    req=Request(SOURCE,headers={"User-Agent":"TidalTurbineDeploymentDiscovery/1.0"})
    with urlopen(req,timeout=40) as response:
        raw=response.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise ValueError("Too many source bytes")
    source=root/"source_deployments.csv";source.write_bytes(raw)
    result=inspect(source)
    report=root/"deployment_discovery.json"
    report.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"dataset_rows":result["dataset_rows"],"fields":result["fields"],
                      "coordinates":result["rows_with_basic_numeric_ns_coordinates"],
                      "sites":{k:{"near":v["within_25_km_count"],
                                  "examples":v["nearest_7_max_25km"][:3]} for k,v in result["proximity"].items()},
                      "model_eligible_rows":0}))

if __name__=="__main__":main()
