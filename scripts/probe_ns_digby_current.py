"""Bounded public Nova Scotia Digby County Current Data 3D ADCP API schema probe.

Official dataset is3b-ip8b, deployment identities from official uban-q9i2.
Never qualify numeric gross-range flags as native ADCP QC or coastal berth flow.
"""
import argparse
import json
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

BASE="https://data.novascotia.ca/resource/is3b-ip8b.json"
DEPLOYMENTS=("DG012","DG002","DG007","DG004")
MAX_BYTES=1_500_000

def ask(params):
    url=BASE+"?"+urlencode(params)
    request=Request(url,headers={"User-Agent":"TidalTurbine-DigbyADCP-Research/1.0"})
    with urlopen(request,timeout=30) as response:
        raw=response.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise ValueError("Unexpected large response")
    return json.loads(raw),url

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--probe",action="store_true")
    x=a.parse_args()
    if not x.probe:
        print(json.dumps({"mode":"DRY_RUN_NO_NETWORK","dataset":BASE,"deployments":DEPLOYMENTS}))
        return
    for deployment in DEPLOYMENTS:
        try:
            records,url=ask({"$where":f"deployment_id='{deployment}'","$limit":"3"})
            print(json.dumps({"id":deployment,"query":url,"sample_rows":len(records),"columns":sorted(records[0]) if records else [],
             "first_row":records[0] if records else None,"model_eligible":0}),flush=True)
        except (HTTPError,URLError,ValueError) as e:
            print(json.dumps({"id":deployment,"error":type(e).__name__,"detail":str(e)[:200],
                              "model_eligible":0}),flush=True)

if __name__=="__main__":main()
