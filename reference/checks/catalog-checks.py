#!/usr/bin/env python3
"""Catalog checks — the map's index, as opposed to its cards. Standard library only.

    python3 catalog-checks.py --map <dir containing CATALOG.md>
    python3 catalog-checks.py --self-test

A catalog's main table is the first Markdown table whose header has a `Card` column. Each of its
rows links either to a card or to a district — a catalog one level down (a link ending CATALOG.md).

E. Every card under the map (`cards/*.md` at the top and in each district) is reached by exactly
   one catalog row, and every row's link resolves. An orphan card cannot be found by a reader who
   follows the catalog; a card reached twice has two boundaries; a dead row sends a reader nowhere.
F. Every catalog stays thin: seven rows at most, districts one level deep (a district never opens
   another), and no counts — a number of cards, rows or files belongs where it is derived, not in
   the file a reader holds while choosing. "One card" is the reading rule, not a count, so the
   check looks for numbers from two up.

Exit 0 = both pass. Exit 1 = a finding. Exit 2 = could not run.
--self-test runs fixtures/catalog/, where each map trips exactly the gate its folder prefix names
(`e-` → E, `f-` → F, `ok-` → none); exit 0 only if every one does.

Written by Andrés Curcio for the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission. See CHANGES.md.
"""

import argparse
import glob
import os
import re
import sys

MAX_ROWS = 7
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)\)")
NUM = r"(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|[2-9]|[1-9]\d+)"
COUNT_RE = re.compile(rf"\b{NUM} (cards?|rows?|files?|districts?)\b", re.I)


def main_table(text):
    """Rows of the first table whose header has a Card column, as lists of cell strings."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and any(c.lower() == "card" for c in cells):
            col = [c.lower() for c in cells].index("card")
            rows = []
            for row in lines[i + 2:]:
                if not row.lstrip().startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return col, rows
    return None, []


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check_map(map_dir):
    """Return a list of (gate, finding)."""
    findings = []
    top = os.path.join(map_dir, "CATALOG.md")
    if not os.path.isfile(top):
        return [("E", f"no CATALOG.md in {map_dir}")]

    reached = {}       # card path -> catalogs whose rows reach it
    districts = []

    def walk_catalog(path, depth):
        col, rows = main_table(read(path))
        name = os.path.relpath(path, map_dir)
        if col is None:
            findings.append(("F", f"{name}: no table with a Card column"))
            return
        if len(rows) > MAX_ROWS:
            findings.append(("F", f"{name}: {len(rows)} rows, at most {MAX_ROWS}"))
        for m in COUNT_RE.finditer(read(path)):
            findings.append(("F", f"{name}: carries a count — \"{m.group(0)}\""))
        for row in rows:
            cell = row[col] if col < len(row) else ""
            links = LINK_RE.findall(cell)
            if not links:
                findings.append(("E", f"{name}: a row with no link in its Card cell: {cell[:60]!r}"))
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), links[0]))
            if not os.path.isfile(target):
                findings.append(("E", f"{name}: row links to a file that does not exist: {links[0]}"))
            elif os.path.basename(target) == "CATALOG.md":
                if depth >= 1:
                    findings.append(("F", f"{name}: a district opens another district: {links[0]}"))
                else:
                    districts.append(target)
                    walk_catalog(target, depth + 1)
            else:
                reached.setdefault(os.path.abspath(target), []).append(name)

    walk_catalog(top, 0)

    folders = [map_dir] + [os.path.dirname(d) for d in districts]
    cards = {os.path.abspath(p) for f in folders for p in glob.glob(os.path.join(f, "cards", "*.md"))}
    for card in sorted(cards):
        n = len(reached.get(card, []))
        rel = os.path.relpath(card, map_dir)
        if n == 0:
            findings.append(("E", f"{rel}: no catalog row reaches this card"))
        elif n > 1:
            findings.append(("E", f"{rel}: reached by {n} rows ({', '.join(reached[card])})"))
    return findings


def self_test():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "catalog")
    maps = sorted(d for d in glob.glob(os.path.join(base, "*")) if os.path.isdir(d))
    if not maps:
        print(f"FATAL  no fixtures under {base}", file=sys.stderr)
        return 2
    wrong, shown = [], set()
    print(f"{'fixture':<22} {'expected':<9} {'tripped':<9} result")
    print("-" * 52)
    for m in maps:
        name = os.path.basename(m)
        prefix = name.split("-", 1)[0]
        expected = set() if prefix == "ok" else {prefix.upper()}
        shown |= expected
        tripped = {g for g, _ in check_map(m)}
        ok = tripped == expected
        print(f"{name:<22} {','.join(sorted(expected)) or '-':<9} {','.join(sorted(tripped)) or '-':<9} "
              f"{'ok' if ok else 'WRONG'}")
        if not ok:
            wrong.append(name)
    print("-" * 52)
    if {"E", "F"} - shown:
        print(f"\nSELF-TEST FAILED - no fixture shows {', '.join(sorted({'E', 'F'} - shown))} failing.")
        return 1
    if wrong:
        print(f"\nSELF-TEST FAILED - {len(wrong)} fixture(s) did not trip what their name says: {', '.join(wrong)}")
        return 1
    print("\nSELF-TEST PASSED - E and F were each shown failing on their own fixtures, and the "
          "control map passed both.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", help="directory holding the top CATALOG.md")
    ap.add_argument("--self-test", action="store_true", help="run fixtures/catalog/ and expect failures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.map or not os.path.isdir(args.map):
        ap.error("--map must be a directory, unless --self-test is given")

    findings = check_map(args.map)
    if findings:
        print(f"FAILED - {len(findings)} finding(s):")
        for gate, f in findings:
            print(f"  {gate}  {f}")
        return 1
    print("PASSED - every card is reached by exactly one catalog row, every row resolves, no catalog "
          f"has more than {MAX_ROWS} rows or carries a count, and districts are one level deep.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
