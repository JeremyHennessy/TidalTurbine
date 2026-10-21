"""Bounded, read-only health probe for public FORCE native-file share indexes.

The response is a transport observation, never a proof of data contents, ADCP QC,
instrument geometry or permission to download. Default is offline listing.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import socket
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

HOST = "data.fundyforce.ca"
BASE = "https://" + HOST + "/forceCloud/index.php/s/"
SHARES = {
    "native_data": "TAEz9gwARDDXCTD",
    "metadata": "85etc2wCZt7K9FA",
}


class SameHostRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlparse(newurl).hostname != HOST:
            raise ValueError("Cross-host redirect refused without review")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def endpoints():
    return [
        (name + "_index", BASE + token + "?path=%2F")
        for name, token in SHARES.items()
    ] + [
        (name + "_range_get", BASE + token + "/download")
        for name, token in SHARES.items()
    ]


def attempt(item):
    label, url = item
    request = Request(url, headers={
        "User-Agent": "TidalTurbineReadOnlySourceHealth/1.0",
        "Range": "bytes=0-127",
        "Accept": "text/html,application/zip,application/octet-stream;q=0.8",
    }, method="GET")
    opener = build_opener(SameHostRedirect())
    result = {"name": label, "transport_status": "UNKNOWN",
              "http_status": None, "content_type": None,
              "content_range": None, "verified_complete_native_source": False,
              "native_beam_quality_available": False}
    try:
        # Never save source bytes, enumerate private files, authenticate, or
        # retrieve the full download. Close even when Range is ignored.
        with opener.open(request, timeout=12) as response:
            result.update(transport_status="HTTP_RESPONSE",
                          http_status=response.status,
                          content_type=response.headers.get("Content-Type"),
                          content_range=response.headers.get("Content-Range"))
            head = response.read(128)
            result["body_prefix"] = (
                "ZIP_HEADER_ONLY" if head.startswith(bytes.fromhex('504b0304'))
                else "HTML_OR_OTHER_UNVERIFIED"
            )
    except HTTPError as exc:
        result.update(transport_status="HTTP_ERROR", http_status=exc.code)
    except (URLError, OSError, ValueError, ssl.SSLError, socket.timeout) as exc:
        result.update(transport_status="NETWORK_OR_REDIRECT_ERROR",
                      error_type=type(exc).__name__)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", action="store_true",
                        help="Explicitly permit bounded public read-only GET requests")
    args = parser.parse_args()
    targets = endpoints()
    if not args.probe:
        print(json.dumps({"mode": "DRY_RUN_NO_NETWORK",
                          "public_labels": [x[0] for x in targets],
                          "qualified_current_bins": 0}, indent=2))
        return
    with ThreadPoolExecutor(max_workers=4) as executor:
        responses = list(executor.map(attempt, targets))
    print(json.dumps({"mode": "PUBLIC_READ_ONLY_BOUNDED_GET",
                      "results": responses,
                      "qualified_current_bins": 0,
                      "decision": "Native raw files, source QC and geometry NOT ACQUIRED OR VALIDATED by a transport probe"}, indent=2))


if __name__ == "__main__":
    main()
