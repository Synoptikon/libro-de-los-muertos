import json
from pathlib import Path

from src.validacion.corpus_manifest import REQUIRED_SOURCE, REQUIRED_TOP_LEVEL, validate_manifest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "corpus" / "manifest.json"


def test_manifest_schema_contract():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert REQUIRED_TOP_LEVEL <= data.keys()
    assert data["sources"]
    assert all(REQUIRED_SOURCE <= source.keys() for source in data["sources"])


def test_manifest_policy_is_strict():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert validate_manifest(data) == []
    assert data["policy"]["no_invented_text"] is True
    assert data["policy"]["no_placeholder_as_source"] is True


def test_primary_source_is_reference_until_ingestion():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    primary = next(s for s in data["sources"] if s["id"] == data["primary_manifest"])
    assert primary["inventory_number"] == "EA10470"
    assert primary["ingestion_status"] == "not_ingested"
