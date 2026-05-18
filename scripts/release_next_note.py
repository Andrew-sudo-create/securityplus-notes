#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move one hidden note set into the public notes folder."
    )
    parser.add_argument(
        "--hidden-dir",
        default=".hidden-notes",
        help="Directory that contains unreleased note sets.",
    )
    parser.add_argument(
        "--public-dir",
        default="notes",
        help="Directory where released note sets are published.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    hidden_dir = Path(args.hidden_dir)
    public_dir = Path(args.public_dir)

    if not hidden_dir.exists():
        print(f"Hidden notes directory does not exist: {hidden_dir}")
        return 0

    public_dir.mkdir(parents=True, exist_ok=True)

    entries = sorted(
        [path for path in hidden_dir.iterdir() if path.name not in {".gitkeep"}],
        key=lambda p: p.name.lower(),
    )

    if not entries:
        print("No hidden note sets available to release.")
        return 0

    next_entry = entries[0]
    target = public_dir / next_entry.name

    if target.exists():
        print(
            f"Skipping release because target already exists: {target}. "
            "Rename or remove the conflicting target and retry."
        )
        return 1

    shutil.move(str(next_entry), str(target))
    print(f"Released note set: {next_entry} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
