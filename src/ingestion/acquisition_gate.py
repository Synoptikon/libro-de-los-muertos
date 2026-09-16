"""Deterministic gate for provenance-preserving raw acquisitions."""

from __future__ import annotations

from typing import Any

from src.ingestion.acquisition_record import validate_acquisition_record


def validate_raw_acquisition(
    record: dict[str, Any],
    content: bytes,
) -> dict[str, Any]:
    """Validate that a supplied raw artifact matches its acquisition record."""
    if not isinstance(content, bytes) or not content:
        raise ValueError("content must be non-empty bytes")

    validate_acquisition_record(record)

    import hashlib

    digest = hashlib.sha256(content).hexdigest()
    if record["content_length_bytes"] != len(content):
        raise ValueError("content_length_bytes does not match supplied content")
    if record["sha256"].lower() != digest:
        raise ValueError("sha256 does not match supplied content")
    if record["transformations"] != []:
        raise ValueError("raw acquisition cannot contain transformations")
    if record["verification_status"] != "VERIFIED":
        raise ValueError("raw acquisition requires VERIFIED source identity")

    return {**record, "acquisition_status": "RAW_VERIFIED"}
