#!/usr/bin/env python3
"""
Audit which media files are used in index.html.

Usage:
  python3 scripts/media_audit.py
  python3 scripts/media_audit.py --building "7455 Union Park Ave"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MEDIA_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".pdf",
    ".heic",
    ".svg",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare media files in project folders against references in index.html."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root folder (default: current directory).",
    )
    parser.add_argument(
        "--index",
        default="index.html",
        help="Path to index file relative to root (default: index.html).",
    )
    parser.add_argument(
        "--building",
        default=None,
        help="Optional top-level folder or filename prefix to filter output.",
    )
    return parser.parse_args()


def is_media(path: Path) -> bool:
    return path.suffix.lower() in MEDIA_EXTENSIONS


def collect_used_media(index_text: str) -> set[str]:
    used: set[str] = set()

    for match in re.finditer(r'src="([^"]+)"', index_text):
        src = match.group(1).strip()
        if src.startswith("data:"):
            continue
        ext = Path(src).suffix.lower()
        if ext in MEDIA_EXTENSIONS:
            used.add(src)

    for match in re.finditer(r'data-gallery="([^"]+)"', index_text):
        gallery_items = match.group(1).split(",")
        for item in gallery_items:
            candidate = item.strip()
            if candidate:
                used.add(candidate)

    return used


def collect_all_media(root: Path) -> set[str]:
    media: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if is_media(path):
            media.add(str(path.relative_to(root)))
    return media


def filter_set(values: set[str], building_filter: str | None) -> list[str]:
    items = sorted(values)
    if not building_filter:
        return items

    needle = building_filter.lower()
    return [item for item in items if item.lower().startswith(needle)]


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    index_path = (root / args.index).resolve()

    if not index_path.exists():
        print(f"ERROR: index file not found: {index_path}")
        return 1

    index_text = index_path.read_text(encoding="utf-8")
    used = collect_used_media(index_text)
    all_media = collect_all_media(root)

    missing_refs = used - all_media
    unused = all_media - used

    used_filtered = filter_set(used, args.building)
    all_filtered = filter_set(all_media, args.building)
    missing_filtered = filter_set(missing_refs, args.building)
    unused_filtered = filter_set(unused, args.building)

    label = args.building if args.building else "ALL"
    print(f"Media audit for: {label}")
    print("-" * 60)
    print(f"Total media files: {len(all_filtered)}")
    print(f"Referenced in index: {len(used_filtered)}")
    print(f"Unused media files: {len(unused_filtered)}")
    print(f"Broken references: {len(missing_filtered)}")

    if unused_filtered:
        print("\nUNUSED MEDIA")
        for item in unused_filtered:
            print(f"- {item}")

    if missing_filtered:
        print("\nBROKEN REFERENCES (in index.html, file not found)")
        for item in missing_filtered:
            print(f"- {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
