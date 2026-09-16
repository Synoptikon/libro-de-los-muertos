import pytest

from src.ingestion.source_verification import verify_source_identity


def record():
    return {
        "source_id": "LM-CORPUS-001",
        "repository": "British Museum",
        "inventory_number": "EA10470",
        "source_uri": "https://example.org/ea10470",
        "identified_source_id": "LM-CORPUS-001",
        "identified_inventory_number": "EA10470",
        "verification_method": "catalogue_identity_match",
    }


def test_matching_identity_is_verified():
    result = verify_source_identity(record())
    assert result["verification_status"] == "VERIFIED"


def test_mismatched_inventory_is_rejected():
    item = record()
    item["identified_inventory_number"] = "EA99999"
    with pytest.raises(ValueError, match="identified_inventory_number"):
        verify_source_identity(item)


def test_invalid_uri_is_rejected():
    item = record()
    item["source_uri"] = "example.invalid/ea10470"
    with pytest.raises(ValueError, match="HTTP\(S\)"):
        verify_source_identity(item)
