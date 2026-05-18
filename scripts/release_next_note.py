#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


IGNORED_NAMES = {".gitkeep", ".DS_Store"}
IGNORED_TOP_LEVEL_DIRS = {"downloadables"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move one hidden note file into the public notes folder."
    )
    parser.add_argument(
        "--hidden-dir",
        default=".hidden-notes",
        help="Directory that contains unreleased note files/folders.",
    )
    parser.add_argument(
        "--public-dir",
        default="notes",
        help="Directory where released note sets are published.",
    )
    return parser.parse_args()


def iter_note_files(hidden_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in hidden_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name in IGNORED_NAMES:
            continue
        relative = path.relative_to(hidden_dir)
        if relative.parts and relative.parts[0].lower() in IGNORED_TOP_LEVEL_DIRS:
            continue
        candidates.append(path)

    def sort_key(path: Path) -> tuple[int, int, str]:
        relative = path.relative_to(hidden_dir)
        match = re.match(r"^(\d+)", path.name)
        if match:
            return (0, int(match.group(1)), str(relative).lower())
        return (1, 0, str(relative).lower())

    return sorted(
        candidates,
        key=sort_key,
    )


def remove_empty_parents(path: Path, stop_dir: Path) -> None:
    current = path.parent
    while current != stop_dir and current.exists():
        if any(current.iterdir()):
            break
        current.rmdir()
        current = current.parent


def main() -> int:
    args = parse_args()
    hidden_dir = Path(args.hidden_dir)
    public_dir = Path(args.public_dir)

    if not hidden_dir.exists():
        print(f"Hidden notes directory does not exist: {hidden_dir}")
        return 0

    public_dir.mkdir(parents=True, exist_ok=True)

    entries = iter_note_files(hidden_dir)

    if not entries:
        print("No hidden notes available to release.")
        return 0

    next_entry = entries[0]
    relative_path = next_entry.relative_to(hidden_dir)
    target = public_dir / relative_path

    if target.exists():
        print(
            f"Skipping release because target already exists: {target}. "
            "Rename or remove the conflicting target and retry."
        )
        return 1

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(next_entry), str(target))
    remove_empty_parents(next_entry, hidden_dir)
    print(f"Released note: {next_entry} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
