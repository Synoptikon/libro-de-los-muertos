import hashlib

from src.ingestion.primary_source import ingest_bytes


def test_ingestion_preserves_raw_bytes_by_hash():
    payload = b"verified source bytes"
    record = ingest_bytes(
        source_id="MAN_ANI",
        inventory_number="EA10470",
        source_uri="https://example.invalid/primary-source",
        content=payload,
        retrieved_at="2026-09-15T00:00:00Z",
    )

    assert record["source_id"] == "MAN_ANI"
    assert record["inventory_number"] == "EA10470"
    assert record["content_sha256"] == hashlib.sha256(payload).hexdigest()
    assert record["content_length_bytes"] == len(payload)
    assert record["transformations"] == []
    assert record["status"] == "INGESTED_RAW"


def test_ingestion_rejects_empty_content():
    try:
        ingest_bytes(
            source_id="MAN_ANI",
            inventory_number="EA10470",
            source_uri="https://example.invalid/primary-source",
            content=b"",
            retrieved_at="2026-09-15T00:00:00Z",
        )
    except ValueError as exc:
        assert str(exc) == "content must not be empty"
    else:
        raise AssertionError("empty content must be rejected")
