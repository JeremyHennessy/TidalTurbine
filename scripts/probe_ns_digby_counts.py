"""Read-only row counts for source-confirmed Digby/Grand/Petit ADCP deployments."""
import argparse,json
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

BASE="https://data.novascotia.ca/resource/is3b-ip8b.json"
SITES=("DG012","DG002","DG007","DG004")

def fetch(params):
    url=BASE+"?"+urlencode(params)
    req=Request(url,headers={"User-Agent":"TidalTurbineRawADCPDiscovery/1.0"})
    with urlopen(req,timeout=40) as r:
        body=r.read(100000)
    if len(body)>=100000:raise ValueError("Too large for a count")
    return json.loads(body)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--counts",action="store_true")
    x=p.parse_args()
    if not x.counts:
        print(json.dumps({"mode":"DRY_RUN_NO_NETWORK","source":BASE,"sites":SITES}));return
    for name in SITES:
        try:
            rows=fetch({"$select":"count(*) as row_count, min(datetime) as min_datetime, max(datetime) as max_datetime","$where":f"deployment_id='{name}'"})
            print(json.dumps({"deployment":name,"socrata_aggregate":rows,"model_eligible":0}),flush=True)
        except (ValueError,HTTPError,URLError) as e:
            print(json.dumps({"deployment":name,"error":str(e)[:180],"model_eligible":0}),flush=True)

if __name__=="__main__":main()
