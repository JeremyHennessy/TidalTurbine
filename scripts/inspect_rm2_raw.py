"""Acquire ONLY six public UNH RM2 NI signals + calibration metadata.

Opt-in; raw binary is never committed, never used to claim turbine fatigue.
Pinned Figshare file identifiers come from the immutable UNH RM2 repo's
Config/raw_data_urls.json at fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef.
"""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
import h5py
import numpy as np

FILES = {
    ("0.4",10):(1913215,1913216),
    ("0.4",12):(1913225,1913226),
    ("1.0",10):(1914080,1914081),
    ("1.0",12):(1914090,1914091),
    ("1.2",10):(1915325,1915326),
    ("1.2",12):(1915335,1915336)
}
CAP_PER_FILE = 36_000_000

def fetch(file_id, localpath):
    url = f"https://api.figshare.com/v2/file/download/{file_id}"
    req = Request(url, headers={"User-Agent":"TidalTurbineRawArchiveResearch/1.0"})
    with urlopen(req,timeout=60) as response:
        length = response.headers.get("Content-Length")
        if length and int(length)>CAP_PER_FILE:
            raise ValueError(f"Refuse oversized file {file_id}")
        h=hashlib.sha256()
        size=0
        with localpath.open("wb") as output:
            while True:
                data=response.read(1024*1024)
                if not data:break
                size+=len(data)
                if size>CAP_PER_FILE:raise ValueError(f"Exceeded file cap {file_id}")
                h.update(data)
                output.write(data)
    if size<100:raise ValueError(f"Suspiciously short file {file_id}")
    return {"source_file_id":file_id,"source_url":url,"bytes":size,"sha256":h.hexdigest()}

def summarise_h5(path):
    result={"dataset_summary":[]}
    with h5py.File(path,"r") as h:
        def visit(name,obj):
            if isinstance(obj,h5py.Dataset):
                desc={"name":name,"shape":list(obj.shape),"dtype":str(obj.dtype)}
                if obj.ndim==1 and obj.size>=2 and obj.size<=3_000_000 and np.issubdtype(obj.dtype,np.number):
                    ar=np.asarray(obj[...],dtype=np.float64)
                    desc.update(nonfinite=int((~np.isfinite(ar)).sum()),
                                min=float(np.nanmin(ar)),max=float(np.nanmax(ar)))
                result["dataset_summary"].append(desc)
        h.visititems(visit)
    return result

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--fetch",action="store_true")
    a.add_argument("--out",default="data/local/rm2_six_raw")
    opts=a.parse_args()
    if not opts.fetch:
        print(json.dumps({"mode":"DRY_RUN_NO_DOWNLOAD","run_cases":[list(x) for x in FILES]},indent=2));return
    root=Path(opts.out);root.mkdir(parents=True,exist_ok=True)
    manifest={"status":"RAW_NI_ACQUIRED_NUMERICAL_FILE_INSPECTION_NOT_CALIBRATED_LOAD_STRESS",
      "source_upstream_commit":"fdf80fe355c659ec0e3b1dce2f1c9c9800a777ef",
      "original_raw_data_licence":"CC BY 4.0; UNH RM2 experimental reduced and raw files",
      "calibration_validated":False,"blade_root_stress_available":False,
      "net_electricity_available":False,"physical_run_validated":False,"trials":[]}
    for (speed,run),(meta_id,ni_id) in FILES.items():
        pfx=f"Perf-{speed}_{run}"
        meta=root/f"{pfx}_metadata.json"
        ni=root/f"{pfx}_nidata.h5"
        m=fetch(meta_id,meta); n=fetch(ni_id,ni)
        if ni.read_bytes()[:8]!=b"\x89HDF\r\n\x1a\n":raise ValueError(f"HDF signature wrong {pfx}")
        metadata=json.loads(meta.read_text(encoding="utf8"))
        if abs(float(metadata["Tow speed (m/s)"])-float(speed))>0.05 or abs(float(metadata["Tip speed ratio"])-(2.9 if run==10 else 3.1))>0.02:
            raise ValueError(f"Metadata mismatch {pfx}")
        trial={"speed_nominal_m_s":float(speed),"run":run,"id":pfx,
               "metadata_file":m,"ni_file":n,"meta_keys":sorted(metadata.keys()),**summarise_h5(ni)}
        manifest["trials"].append(trial)
        print(json.dumps({"trial":pfx,"raw_bytes":n["bytes"],"sha256":n["sha256"],
                          "signals":trial["dataset_summary"]}),flush=True)
    (root/"raw_source_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"run_count":len(manifest["trials"]),"status":manifest["status"]}))

if __name__=="__main__":
    main()
