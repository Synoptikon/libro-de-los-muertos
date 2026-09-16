import hashlib

import pytest

from src.ingestion.acquisition_gate import validate_raw_acquisition


def make_record(content: bytes):
    return {
        "source_id": "MAN_ANI",
        "repository": "British Museum",
        "inventory_number": "EA10470",
        "source_uri": "https://example.org/source/EA10470",
        "retrieved_at": "2026-09-15T00:00:00Z",
        "media_type": "image/tiff",
        "content_length_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "acquisition_method": "manual_verified_download",
        "transformations": [],
        "verification_status": "VERIFIED",
    }


def test_matching_raw_content_is_accepted():
    content = b"raw-primary-source"
    result = validate_raw_acquisition(make_record(content), content)
    assert result["acquisition_status"] == "RAW_VERIFIED"


def test_hash_mismatch_is_rejected():
    content = b"raw-primary-source"
    record = make_record(content)
    record["sha256"] = "b" * 64
    with pytest.raises(ValueError, match="sha256 does not match supplied content"):
        validate_raw_acquisition(record, content)


def test_length_mismatch_is_rejected():
    content = b"raw-primary-source"
    record = make_record(content)
    record["content_length_bytes"] += 1
    with pytest.raises(ValueError, match="content_length_bytes does not match"):
        validate_raw_acquisition(record, content)


def test_unverified_identity_is_rejected():
    content = b"raw-primary-source"
    record = make_record(content)
    record["verification_status"] = "UNVERIFIED"
    with pytest.raises(ValueError, match="requires VERIFIED source identity"):
        validate_raw_acquisition(record, content)


def test_empty_content_is_rejected():
    content = b""
    record = make_record(b"non-empty")
    with pytest.raises(ValueError, match="non-empty bytes"):
        validate_raw_acquisition(record, content)
