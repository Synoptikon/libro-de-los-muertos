import pytest

from src.ingestion.acquisition_record import validate_acquisition_record


@pytest.fixture
def valid_record():
    return {
        "source_id": "MAN_ANI",
        "repository": "British Museum",
        "inventory_number": "EA10470",
        "source_uri": "https://example.org/source/EA10470",
        "retrieved_at": "2026-09-15T00:00:00Z",
        "media_type": "image/tiff",
        "content_length_bytes": 1234,
        "sha256": "a" * 64,
        "acquisition_method": "manual_verified_download",
        "transformations": [],
        "verification_status": "UNVERIFIED",
    }


def test_valid_record_is_returned_unchanged(valid_record):
    assert validate_acquisition_record(valid_record) == valid_record


def test_missing_field_is_rejected(valid_record):
    del valid_record["sha256"]
    with pytest.raises(ValueError, match="missing required fields: sha256"):
        validate_acquisition_record(valid_record)


def test_invalid_sha256_is_rejected(valid_record):
    valid_record["sha256"] = "not-a-digest"
    with pytest.raises(ValueError, match="sha256 must be a 64-character hexadecimal digest"):
        validate_acquisition_record(valid_record)


def test_transformed_acquisition_is_rejected(valid_record):
    valid_record["transformations"] = ["ocr"]
    with pytest.raises(ValueError, match="transformations must be \[\]"):
        validate_acquisition_record(valid_record)


def test_unverified_status_is_allowed_until_external_verification(valid_record):
    valid_record["verification_status"] = "UNVERIFIED"
    assert validate_acquisition_record(valid_record)["verification_status"] == "UNVERIFIED"
