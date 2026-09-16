"""Deterministic gate for verifying a registered primary-source identity.

This module validates metadata supplied by an acquisition/discovery adapter. It
never treats a URI alone as proof of provenance and never downloads content.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

REQUIRED_FIELDS = {
    "source_id",
    "repository",
    "inventory_number",
    "source_uri",
    "identified_source_id",
    "identified_inventory_number",
    "verification_method",
}


def verify_source_identity(record: dict[str, Any]) -> dict[str, Any]:
    """Return a verified record only when registered identity matches exactly."""
    if not isinstance(record, dict):
        raise TypeError("record must be a dict")

    missing = sorted(REQUIRED_FIELDS - record.keys())
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    parsed = urlparse(record["source_uri"])
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("source_uri must be an absolute HTTP(S) URI")

    for field in REQUIRED_FIELDS - {"source_uri", "verification_method"}:
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    if record["identified_source_id"] != record["source_id"]:
        raise ValueError("identified_source_id does not match registered source_id")
    if record["identified_inventory_number"] != record["inventory_number"]:
        raise ValueError("identified_inventory_number does not match registered inventory_number")

    return {**record, "verification_status": "VERIFIED"}
