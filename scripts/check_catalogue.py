"""Dependency-free schema checks: quality gates, not verification of citations."""
from pathlib import Path
from datetime import date
import json
import sys
from urllib.parse import urlparse

ALLOWED = {
    "PUBLISHED_EVIDENCE", "MANUFACTURER_OR_PROJECT_CLAIM", "ENGINEERING_ASSUMPTION",
    "DESIGN_HYPOTHESIS", "SIMULATION_RESULT", "EXPERIMENTALLY_VALIDATED_FINDING",
    "UNKNOWN_OR_CONFLICT",
}
DEPTH = {"metadata_only", "landing_page_review", "sections_reviewed", "full_content_review"}
REQUIRED = {"id", "title", "url", "publication_date", "access_date", "evidence_class",
            "review_depth", "reviewed_sections", "supported_claims", "limitations", "access_status"}


def check():
    path = Path(__file__).resolve().parents[1] / "research" / "catalogue.json"
    sources = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(sources, list) and sources, "catalogue must be a nonempty list"
    identifiers = set()
    for source in sources:
        missing = REQUIRED - source.keys()
        assert not missing, f"missing {missing} in {source.get('id')}"
        source_id = source["id"]
        assert source_id and source_id not in identifiers, f"duplicate/blank source ID {source_id}"
        identifiers.add(source_id)
        assert source["evidence_class"] in ALLOWED, f"invalid evidence class {source_id}"
        assert source["review_depth"] in DEPTH, f"invalid review depth {source_id}"
        parsed = urlparse(source["url"])
        assert parsed.scheme == "https" and parsed.netloc, f"invalid HTTPS URL {source_id}"
        reviewed_on = date.fromisoformat(source["access_date"])
        assert reviewed_on <= date.today(), f"future-dated source {source_id}"
        assert isinstance(source["reviewed_sections"], list)
        assert isinstance(source["supported_claims"], list)
        assert isinstance(source["limitations"], list) and source["limitations"]
        if source["review_depth"] == "metadata_only":
            assert not source["reviewed_sections"], f"metadata-only cannot claim sections {source_id}"
    print(f"Verified {len(sources)} unique catalogue records (structural checks only).")


if __name__ == "__main__":
    try:
        check()
    except (ValueError, AssertionError, OSError) as exc:
        print(f"Catalogue check failed: {exc}", file=sys.stderr)
        sys.exit(1)
