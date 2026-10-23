"""Make a self-contained Pages artifact; no tools, API calls or paid hosting required."""
import argparse
from pathlib import Path
from shutil import copy2, rmtree
ROOT=Path(__file__).resolve().parents[1]
FILES=('index.html','site/index.html','site/artwork.js','site/app.js','site/clearance_model.js','site/clearance.js','site/clearance.css','site/service_energy_model.js','site/service_energy.js','site/service_energy.css','site/field_research.js','site/field_research.css','site/published_strain.js','site/published_strain.css','site/styles.css','site/assets/favicon.svg','reports/SCREEN-001.json','reports/RM2-OBS-001.json','reports/RM2-TRADEOFF-001.json','reports/RM2-CROSSSPEED-001.json','reports/RM2-RAW-LOADS-001.json','reports/FORCE-SLICE-QA-001.json','reports/FORCE-72H-QA-001.json','reports/FORCE-CAMPAIGN-QA-001.json','reports/RM1-OBS-001.json','research/ocean_datasets.json','research/mechanisms.json','research/catalogue.json','research/metrology_prereg_v1.json','research/field_strain_evidence_20261023.json','research/UNH_2023_PUBLISHED_STRAIN_001.json','research/UNH_2022_SOURCE_ACCESS_001.json')

def build(target:Path):
    target=target.resolve()
    if target==ROOT or ROOT in target.parents and target.name not in ('dist','build-site'):
        raise ValueError('Output must be a dedicated dist/build-site folder, not project source')
    target.mkdir(parents=True,exist_ok=True)
    for rel in FILES:
        f=ROOT/rel
        to=target/rel
        to.parent.mkdir(parents=True,exist_ok=True)
        copy2(f,to)
    (target/'.nojekyll').write_text('',encoding='utf8')
    print('Built static site:',target,f'; {len(FILES)} source-controlled files; source data remain in published research/ and reports/')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',default='dist');args=p.parse_args()
    build(ROOT/args.out)
if __name__=='__main__':main()
