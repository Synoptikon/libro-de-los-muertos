"""Validation for provenance-preserving source acquisition records.

An acquisition record describes how a registered source was obtained. It does
not assert that the source is authentic or complete; verification is explicit.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urlparse

REQUIRED_FIELDS = {
    "source_id",
    "repository",
    "inventory_number",
    "source_uri",
    "retrieved_at",
    "media_type",
    "content_length_bytes",
    "sha256",
    "acquisition_method",
    "transformations",
    "verification_status",
}

ALLOWED_VERIFICATION_STATUS = {"UNVERIFIED", "VERIFIED"}


def validate_acquisition_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a complete acquisition record and return it unchanged."""
    if not isinstance(record, dict):
        raise TypeError("record must be a dict")

    missing = sorted(REQUIRED_FIELDS - record.keys())
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    for field in ("source_id", "repository", "inventory_number", "media_type", "acquisition_method"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    parsed = urlparse(record["source_uri"])
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("source_uri must be an absolute HTTP(S) URI")

    try:
        datetime.fromisoformat(record["retrieved_at"].replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("retrieved_at must be an ISO-8601 timestamp") from exc

    length = record["content_length_bytes"]
    if isinstance(length, bool) or not isinstance(length, int) or length <= 0:
        raise ValueError("content_length_bytes must be a positive integer")

    sha256 = record["sha256"]
    if not isinstance(sha256, str) or len(sha256) != 64:
        raise ValueError("sha256 must be a 64-character hexadecimal digest")
    try:
        int(sha256, 16)
    except ValueError as exc:
        raise ValueError("sha256 must be a 64-character hexadecimal digest") from exc

    if record["transformations"] != []:
        raise ValueError("transformations must be [] for an untransformed acquisition")

    if record["verification_status"] not in ALLOWED_VERIFICATION_STATUS:
        raise ValueError("verification_status must be UNVERIFIED or VERIFIED")

    return record
