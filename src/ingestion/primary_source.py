"""Deterministic ingestion contract for verified primary-source bytes.

This module does not discover, scrape, translate, or invent corpus content.
It records provenance for bytes supplied by an already-registered source.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ingest_bytes(
    *,
    source_id: str,
    inventory_number: str,
    source_uri: str,
    content: bytes,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Create a provenance record for source bytes without transforming them."""
    if not source_id.strip():
        raise ValueError("source_id must not be empty")
    if not inventory_number.strip():
        raise ValueError("inventory_number must not be empty")
    if not source_uri.strip():
        raise ValueError("source_uri must not be empty")
    if not isinstance(content, bytes):
        raise TypeError("content must be bytes")
    if not content:
        raise ValueError("content must not be empty")

    return {
        "source_id": source_id,
        "inventory_number": inventory_number,
        "source_uri": source_uri,
        "retrieved_at": retrieved_at or _utc_now(),
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "content_length_bytes": len(content),
        "transformations": [],
        "status": "INGESTED_RAW",
    }


def ingest_file(
    *,
    source_id: str,
    inventory_number: str,
    source_uri: str,
    path: str | Path,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Read a local source file as bytes and return its provenance record."""
    content = Path(path).read_bytes()
    return ingest_bytes(
        source_id=source_id,
        inventory_number=inventory_number,
        source_uri=source_uri,
        content=content,
        retrieved_at=retrieved_at,
    )
