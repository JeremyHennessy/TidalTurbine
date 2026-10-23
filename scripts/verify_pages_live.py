"""Check GitHub Pages public HTTP asset byte-parity with the checked-out commit.

Read-only, opt-in and bounded. This proves that the public CDN serves the
specific released static artifacts; it does not execute JavaScript or prove
physical tidal-turbine performance.
"""
import argparse
from hashlib import sha1
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jeremyhennessy.github.io/TidalTurbine/"
ASSETS = (
    "index.html",
    "site/index.html",
    "site/styles.css",
    "site/artwork.js",
    "site/app.js",
    "site/field_research.js",
    "site/field_research.css",
    "site/published_strain.js",
    "site/published_strain.css",
    "research/UNH_2023_PUBLISHED_STRAIN_001.json",
    "research/UNH_2022_SOURCE_ACCESS_001.json",
    "research/metrology_prereg_v1.json",
    "research/field_strain_evidence_20261023.json",
    "reports/RM2-RAW-LOADS-001.json",
    "reports/RM2-CROSSSPEED-001.json",
)
MAX_BYTES_PER_ASSET = 1_500_000


def git_blob_sha(content: bytes) -> str:
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()


def check_once(path: str):
    if path not in ASSETS:
        raise ValueError("Unexpected untrusted asset path")
    expected = (ROOT / path).read_bytes()
    if len(expected) > MAX_BYTES_PER_ASSET:
        raise ValueError("Source controlled file too large")
    url = SITE if path == "index.html" else SITE + path
    request = Request(url, headers={
        "User-Agent": "TidalTurbinePagesReadOnlyValidation/1.0",
        "Accept": "text/html,application/json,text/css,application/javascript,*/*;q=0.5",
        "Cache-Control": "no-cache",
    })
    with urlopen(request, timeout=17) as response:
        status = response.status
        content = response.read(MAX_BYTES_PER_ASSET + 1)
    if status != 200 or len(content) > MAX_BYTES_PER_ASSET:
        raise ValueError(f"Bad Pages status/content size for {path}: status={status}, bytes={len(content)}")
    if content != expected:
        raise ValueError(f"Public asset byte mismatch for {path}: expected={git_blob_sha(expected)} live={git_blob_sha(content)}")
    return {"path": path, "http_status": status, "bytes": len(content), "git_blob_sha": git_blob_sha(content)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Explicitly access the published site via bounded HTTP")
    parser.add_argument("--tries", type=int, default=3, choices=(1, 2, 3))
    args = parser.parse_args()
    if not args.check:
        print("DRY RUN; no network. Expected public assets:", *ASSETS)
        return
    for path in ASSETS:
        for attempt in range(args.tries):
            try:
                result = check_once(path)
                print("LIVE PAGES BYTE VERIFIED:", result, flush=True)
                break
            except (HTTPError, URLError, TimeoutError, ValueError) as error:
                if attempt == args.tries - 1:
                    raise
                print(f"Pages CDN propagation check {attempt + 1}/{args.tries} for {path}: {type(error).__name__}", flush=True)
                sleep(6)
    print(f"LIVE PAGES HTTP SOURCE PARITY PASS: all {len(ASSETS)} published artifacts match the committed source; not an in-browser JS test.")


if __name__ == "__main__":
    main()
