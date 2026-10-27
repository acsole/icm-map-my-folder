#!/usr/bin/env python3
"""Heading references — which machinery lines reach inside a blueprint file by section heading.

    python3 heading-refs.py --territory <folder> --blank <blueprint dir> --engine <machinery dir>
    python3 heading-refs.py --self-test

A blueprint's files are found by filename, and a map can say so from the routing table. What the
routing table does not show is the machinery naming a *section* inside one of those files. Rename
that heading in the blueprint and new copies stop matching; rename it in the machinery too and the
existing copies stop matching instead. A card that answers "what depends on this wording?" has to
carry the complete list, and this is the command that makes the list complete and checkable.

For every section heading (##, ###, …) of every file in --blank, it looks at every line under
--engine (outside --blank) that names that file, and reports the line when it names the heading:

  exact  the whole heading appears in the line (case, spaces and hyphens ignored)
  topic  the heading's distinctive word (seven letters or more) appears, without the whole heading

A line that never names the file is not reported, so a common word that happens to match a heading
("transaction", "categories") is not a reference. That is the rule, and it is also the limit: a
line that relies on a section without naming its file is not found. Say so wherever the list is used.

Exit 0 always on a real run (it reports, it does not judge). --self-test runs fixtures/heading-refs/
and exits 0 only if it finds exactly the references the fixture plants, and nothing it should not.

Written by Andrés Curcio for the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission. See CHANGES.md.
"""

import argparse
import glob
import os
import re
import sys

HEADING_RE = re.compile(r"^#{2,}\s+(.*?)\s*$")
STOP = {"section", "sections", "general", "current", "pricing", "buyers", "market"}


def headings(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = HEADING_RE.match(line.rstrip("\r\n"))
            if m:
                text = re.split(r"\s+[—(]", m.group(1))[0].strip()
                if len(text) >= 4:
                    out.append(text)
    return out


def phrase_re(text):
    words = re.findall(r"[A-Za-z0-9]+", text)
    return re.compile(r"\b" + r"[\s\-]+".join(map(re.escape, words)) + r"\b", re.I)


def distinctive(text):
    words = [w.lower() for w in re.findall(r"[A-Za-z]+", text)]
    return [w for w in words if len(w) >= 7 and w not in STOP]


def scan(territory, blank, engine):
    """Return [(blank_file, heading, kind, engine_path, line_no, line)]."""
    blank_abs = os.path.normpath(os.path.join(territory, blank))
    engine_files = []
    for p in sorted(glob.glob(os.path.join(territory, engine, "**", "*.md"), recursive=True)):
        if os.path.commonpath([blank_abs, os.path.normpath(p)]) != blank_abs:
            engine_files.append(p)
    found = []
    for bf in sorted(glob.glob(os.path.join(blank_abs, "*.md"))):
        name = os.path.basename(bf)
        for h in headings(bf):
            exact, words = phrase_re(h), distinctive(h)
            for ef in engine_files:
                with open(ef, encoding="utf-8") as fh:
                    for n, line in enumerate(fh, 1):
                        if name not in line:
                            continue
                        if exact.search(line):
                            kind = "exact"
                        elif words and any(re.search(rf"\b{w}\b", line, re.I) for w in words):
                            kind = "topic"
                        else:
                            continue
                        rel = os.path.relpath(ef, territory).replace(os.sep, "/")
                        found.append((name, h, kind, rel, n, line.strip()))
    return found


def self_test():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "heading-refs")
    expected_path = os.path.join(base, "expected.txt")
    if not os.path.isfile(expected_path):
        print(f"FATAL  no fixture at {base}", file=sys.stderr)
        return 2
    with open(expected_path, encoding="utf-8") as fh:
        expected = {l.strip() for l in fh if l.strip() and not l.startswith("#")}
    got = {f"{b} | {h} | {k} | {p}:{n}" for b, h, k, p, n, _ in scan(base, "blank", "engine")}
    missing, extra = sorted(expected - got), sorted(got - expected)
    for line in sorted(expected | got):
        mark = "ok" if line in expected and line in got else ("MISSED" if line in expected else "EXTRA")
        print(f"{mark:<7} {line}")
    if missing or extra:
        print(f"\nSELF-TEST FAILED - {len(missing)} planted reference(s) missed, {len(extra)} found that "
              "should not be.")
        return 1
    print("\nSELF-TEST PASSED - every planted reference was found, as exact or topic, and the decoys "
          "(a common word on a line that names no file, a heading in a file outside the engine) were not.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--territory", help="the folder the map describes")
    ap.add_argument("--blank", help="the blueprint folder, relative to the territory")
    ap.add_argument("--engine", help="the machinery folder, relative to the territory")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.territory and args.blank and args.engine):
        ap.error("--territory, --blank and --engine are required unless --self-test is given")
    found = scan(args.territory, args.blank, args.engine)
    for b, h, k, p, n, line in found:
        print(f"{b} | {h} | {k} | {p}:{n}  {line[:110]}")
    print(f"\n{len(found)} line(s) name a section of a blueprint file. Lines that rely on a section "
          "without naming its file are outside this search.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
