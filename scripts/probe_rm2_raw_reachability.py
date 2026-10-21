"""Bounded, read-only reachability and format check for published UNH RM2 raw files.

The upstream Git repo locates 2015 raw files on figshare using an old HTTP domain.
A successful HTTP response never establishes calibration, correct alignment, or
a valid stress/energy comparison. The probe downloads at most 256 bytes/URL.
"""
import argparse
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

FILES = [
    ("metadata", 1914080, "Perf_1.0_10_metadata.json"),
    ("NI", 1914081, "Perf_1.0_10_nidata.h5"),
]
PATTERNS = [
    ("legacy_https", "https://files.figshare.com/{id}/{file}"),
    ("figshare_api", "https://api.figshare.com/v2/file/download/{id}"),
    ("figshare_downloader", "https://ndownloader.figshare.com/files/{id}"),
]

def probe(label, fmt, fileid, filename):
    url = fmt.format(id=fileid, file=filename)
    result = {"sample": label, "endpoint": url, "http_status": None,
              "first_bytes": None, "body_downloaded_bytes": 0, "validated_source": False}
    try:
        request = Request(url, headers={"Range": "bytes=0-255",
                                       "User-Agent": "TidalTurbine-SourceResearch/1.0"})
        with urlopen(request, timeout=15) as response:
            body = response.read(256)
            result.update(http_status=response.status, effective_host=response.url.split("/")[2],
                          final_url=response.url[:220], content_length=response.headers.get("Content-Length"),
                          content_range=response.headers.get("Content-Range"),
                          first_bytes=body[:16].hex(),
                          body_downloaded_bytes=len(body))
    except HTTPError as e:
        result["http_status"] = e.code
        result["exception"] = type(e).__name__
    except (URLError, ValueError, OSError) as e:
        result["exception"] = type(e).__name__
        result["detail"] = str(e)[:140]
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    if not args.probe:
        print(json.dumps({"mode":"DRY_RUN", "cases":len(FILES)*len(PATTERNS)},indent=2))
        return
    for label, fileid, filename in FILES:
        for name, pattern in PATTERNS:
            print(json.dumps({"route":name, **probe(label,pattern,fileid,filename)},sort_keys=True),flush=True)

if __name__=="__main__":
    main()
