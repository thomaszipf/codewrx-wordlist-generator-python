#!/usr/bin/env python3
"""Combination generator.

Reads groups of token variants and writes every ordered concatenation
(the Cartesian product across groups), one per line. Streams to disk so
memory stays flat no matter how large the product gets.

Input is dynamic: pass one or more config files, each line a group whose
variants are comma-separated. An empty variant (a trailing comma, or two
commas in a row) means "this group may be skipped" and is written as an
empty slot. With no config file the built-in demo groups are used.

Config line example:
    Word1-V1, Word1-V2, Word1-V3,
The trailing comma adds the "skip this group" option.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from itertools import product
from pathlib import Path

# Built-in demo, used only when no config file is given.
DEMO_GROUPS = [
    ["Word1-V1", "Word1-V2", "Word1-V3", ""],
    ["Word2-V1", "Word2-V2", "Word2-V3", ""],
    ["Word3-V1", "Word3-V2", "Word3-V3", ""],
    ["Word4-V1", "Word4-V2", "Word4-V3", ""],
    ["Word5-V1", "Word5-V2", "Word5-V3", ""],
]


def read_groups(paths: list[Path]) -> list[list[str]]:
    """Read token groups from config files.

    Each non-empty, non-comment line is one group; variants are split on
    commas and stripped. Order is preserved (it drives the output order).
    """
    groups: list[list[str]] = []
    for path in paths:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            variants = [v.strip() for v in line.split(",")]
            groups.append(variants)
    return groups


def count_combinations(groups: list[list[str]]) -> int:
    """Total number of combinations (product of group sizes)."""
    total = 1
    for group in groups:
        total *= len(group)
    return total


def stream_combinations(groups: list[list[str]]):
    """Yield each concatenated combination.

    Empty concatenations (every group contributed its empty slot) are
    skipped, so the output never contains a blank line.
    """
    for combo in product(*groups):
        word = "".join(combo)
        if word:
            yield word


def timestamp() -> str:
    """Filename-safe timestamp: 2026-09-26_22-53-01."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def write_lines(path: Path, lines) -> int:
    """Write an iterable of strings to path, one per line. Returns count."""
    written = 0
    with path.open("w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(line)
            fh.write("\n")
            written += 1
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate every concatenation across groups of token variants.",
    )
    parser.add_argument(
        "config",
        nargs="*",
        type=Path,
        help="Config file(s): one group per line, variants comma-separated. "
        "Omit to use the built-in demo.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file (default: wordlist_<timestamp>.txt).",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Only print how many combinations would be generated, write nothing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.config:
        groups = read_groups(args.config)
    else:
        print("no config given, using built-in demo groups ...", file=sys.stderr)
        groups = [list(g) for g in DEMO_GROUPS]

    if not groups:
        print("error: no groups to combine", file=sys.stderr)
        return 1

    total = count_combinations(groups)
    print(f"{len(groups)} groups, {total} combinations before filtering", file=sys.stderr)

    if args.dry_run:
        return 0

    out_path = args.output or Path(f"wordlist_{timestamp()}.txt")
    written = write_lines(out_path, stream_combinations(groups))
    print(f"wrote {written} lines to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
