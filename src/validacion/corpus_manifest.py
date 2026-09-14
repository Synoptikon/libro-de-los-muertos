"""Validación determinista del manifiesto canónico del corpus."""
from __future__ import annotations

import json
from pathlib import Path

REQUIRED_TOP_LEVEL = {"corpus_id", "version", "status", "primary_manifest", "sources", "policy"}
REQUIRED_SOURCE = {"id", "work", "repository", "inventory_number", "role", "ingestion_status", "content_claim"}


def load_manifest(path: str | Path) -> dict:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    missing = REQUIRED_TOP_LEVEL - data.keys()
    if missing:
        raise ValueError(f"Manifest missing keys: {sorted(missing)}")
    if not isinstance(data["sources"], list) or not data["sources"]:
        raise ValueError("Manifest must contain at least one source")
    if not isinstance(data["policy"], dict):
        raise ValueError("Manifest policy must be an object")
    return data


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    sources = data["sources"]
    ids = set()
    for source in sources:
        missing = REQUIRED_SOURCE - source.keys()
        if missing:
            errors.append(f"source missing keys: {sorted(missing)}")
        source_id = source.get("id")
        if source_id in ids:
            errors.append(f"duplicate source id: {source_id}")
        ids.add(source_id)
    if data.get("primary_manifest") not in ids:
        errors.append("primary_manifest does not reference a declared source")
    policy = data["policy"]
    for key in ("no_invented_text", "no_placeholder_as_source", "provenance_required_for_ingested_units", "translation_requires_source_trace"):
        if policy.get(key) is not True:
            errors.append(f"policy must explicitly enable: {key}")
    return errors


def main() -> int:
    path = Path(__file__).resolve().parents[2] / "corpus" / "manifest.json"
    data = load_manifest(path)
    errors = validate_manifest(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {data['corpus_id']} / {data['primary_manifest']}")
    print(f"STATUS: {data['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
