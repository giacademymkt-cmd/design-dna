#!/usr/bin/env python3
"""Inspect an external Design DNA reference corpus without redistributing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov", ".webm"}


def resolve_root(explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env_root = os.environ.get("DESIGN_DNA_REFERENCE_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser())
    candidates.append(Path(__file__).resolve().parents[2] / "referencias-instagram" / "por-estilo")

    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()

    attempted = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Reference corpus not found. Tried: {attempted}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, include_hashes: bool) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    by_style: dict[str, Counter[str]] = defaultdict(Counter)

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        relative = path.relative_to(root)
        style = relative.parts[0] if relative.parts else "unclassified"
        source = relative.parts[1] if len(relative.parts) > 2 else "unknown"
        record: dict[str, Any] = {
            "path": relative.as_posix(),
            "style": style,
            "source": source,
            "extension": path.suffix.lower(),
            "bytes": path.stat().st_size,
        }
        if include_hashes:
            record["sha256"] = sha256(path)
        records.append(record)
        by_style[style][path.suffix.lower()] += 1

    styles = {
        style: {
            "files": sum(types.values()),
            "types": dict(sorted(types.items())),
            "sources": len({record["source"] for record in records if record["style"] == style}),
            "bytes": sum(record["bytes"] for record in records if record["style"] == style),
        }
        for style, types in sorted(by_style.items())
    }
    return {
        "schema_version": 1,
        "root_hint": "DESIGN_DNA_REFERENCE_ROOT or sibling referencias-instagram/por-estilo",
        "rights": "reference-only; verify redistribution rights before publishing media",
        "total_files": len(records),
        "total_bytes": sum(record["bytes"] for record in records),
        "styles": styles,
        "files": records,
    }


def print_summary(manifest: dict[str, Any]) -> None:
    total_mb = manifest["total_bytes"] / 1_000_000
    print(f"Reference corpus: {manifest['total_files']} files, {total_mb:.1f} MB")
    for style, stats in manifest["styles"].items():
        types = ", ".join(f"{ext}={count}" for ext, count in stats["types"].items())
        print(
            f"- {style}: {stats['files']} files, {stats['sources']} sources, "
            f"{stats['bytes'] / 1_000_000:.1f} MB ({types})"
        )

    counts = [stats["files"] for stats in manifest["styles"].values()]
    if counts and max(counts) >= max(2, sum(counts) * 0.4):
        leader = max(manifest["styles"], key=lambda key: manifest["styles"][key]["files"])
        print(f"Warning: {leader} dominates the corpus; do not treat frequency as a global default.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", help="Optional corpus root")
    parser.add_argument("--json", action="store_true", help="Print the portable manifest as JSON")
    parser.add_argument("--hash", action="store_true", help="Include SHA-256 hashes (slower)")
    args = parser.parse_args()

    try:
        root = resolve_root(args.root)
        manifest = build_manifest(root, args.hash)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 1

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print_summary(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
