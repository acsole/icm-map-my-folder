#!/usr/bin/env python3
"""Refusal 1 — no photocopy — plus the card-shape requirement. Run against a map and its territory.

    python3 refusal-checks.py --map <dir containing cards/> --territory <folder the map describes>
    python3 refusal-checks.py --self-test

A. Every card is smaller than what it cites (its Source path: a file's bytes, a folder's total).
B. No run of more than 200 consecutive characters appears verbatim in both a card and a file it cites.
C. Every card cites at least one path that resolves in the territory.
D. Every card carries Hits, Does not hit, and Done when. A card missing one does not ship.

Exit 0 = all checks passed. Exit 1 = at least one failed. Exit 2 = could not run (bad paths).
A territory that is not on disk yields SKIPPED for A and B and a failure for C — a map whose paths
cannot be resolved is not a map that has been checked.

--self-test runs the checks against fixtures/refusal/, a map built to fail: every card there trips
exactly the gate its filename prefix names (`a-` → A, … `ok-` → none). A green on the real map means
something only once this has shown each gate going red. Exit 0 = every fixture behaved as named.

Checks A–D by Gabriel Azoulay. --self-test and its fixtures added by Andrés Curcio, from the
Comp #11 feedback, with the original author's permission; the checks themselves are unchanged.
"""

import argparse
import glob
import os
import re
import sys

RUN = 200  # characters; a shared run LONGER than this is a photocopy
SOURCE_RE = re.compile(r"^\*\*Source path:\*\*\s*(.+?)\s*$", re.M)
REQUIRED = ("Hits:", "Does not hit:", "Done when:")
TICKED_RE = re.compile(r"`([^`\n]+)`")


def looks_like_path(tok):
    tok = tok.strip()
    if not tok or " " in tok.rstrip("/"):
        return False
    return "/" in tok or re.search(r"\.(md|py|html|json|ya?ml|txt|sh|toml|png)$", tok)


def expand(territory, tok):
    """Resolve a cited path, expanding <placeholder> and [placeholder] segments into a glob.

    A placeholder that expands to nothing is a real answer, not an error: that is what a cited
    path which does not exist in the territory looks like (see the ghost on card 06).
    """
    tok = tok.strip().strip("`").rstrip(",.;")
    pattern = re.sub(r"<[^>/]+>|\[[^\]/]+\]", "*", tok)
    try:
        return sorted(glob.glob(os.path.join(territory, pattern)))
    except re.error:  # a literal bracket the caller did not intend as a glob class
        return []


def files_under(paths):
    out = []
    for p in paths:
        if os.path.isfile(p):
            out.append(p)
        elif os.path.isdir(p):
            for root, _dirs, names in os.walk(p):
                if ".git" in root.split(os.sep):
                    continue
                out.extend(os.path.join(root, n) for n in names)
    return out


def size_of(paths):
    return sum(os.path.getsize(f) for f in files_under(paths))


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def shared_run(card_text, file_text):
    """Return the first >RUN-character run present verbatim in both, or None."""
    if len(card_text) <= RUN or not file_text:
        return None
    windows = {card_text[i:i + RUN + 1] for i in range(len(card_text) - RUN)}
    for w in windows:
        if w in file_text:
            return w
    return None


def check_card(card, territory, have_territory):
    """Run A–D on one card. Returns the printed row and a list of (gate, finding) pairs."""
    name = os.path.basename(card)
    text = read_text(card)
    nbytes = len(text.encode("utf-8"))
    findings = []

    ticked = [t for t in TICKED_RE.findall(text) if looks_like_path(t)]
    m = SOURCE_RE.search(text)
    source_tok = TICKED_RE.search(m.group(1)).group(1) if m and TICKED_RE.search(m.group(1)) else None

    # C — at least one cited path resolves in the territory
    resolved = []
    for tok in ticked:
        resolved.extend(expand(territory, tok))
    c_ok = bool(resolved)

    # A — card smaller than its Source path
    if not have_territory:
        a_state, a_size = "SKIP", 0
    elif source_tok is None:
        a_state, a_size = "FAIL", 0
        findings.append(("C", f"{name}: no **Source path:** line"))
    else:
        src = expand(territory, source_tok)
        a_size = size_of(src)
        if not src:
            a_state = "FAIL"
            findings.append(("C", f"{name}: Source path does not resolve: {source_tok}"))
        elif nbytes < a_size:
            a_state = "pass"
        else:
            a_state = "FAIL"
            findings.append(("A", f"{name}: {nbytes} B card >= {a_size} B cited ({source_tok})"))

    # B — no shared run longer than RUN characters
    if not have_territory:
        b_state = "SKIP"
    else:
        b_state = "pass"
        for f in files_under(resolved):
            hit = shared_run(text, read_text(f))
            if hit:
                b_state = "FAIL"
                findings.append(("B", f"{name}: {RUN}+ char run shared with {os.path.relpath(f, territory)}: "
                                      f"{hit[:60]!r}…"))
                break

    if not c_ok:
        findings.append(("C", f"{name}: cites no path that resolves in the territory"))

    # D — the three lines a card may not ship without
    missing = [r for r in REQUIRED if f"**{r}**" not in text]
    d_ok = not missing
    if missing:
        findings.append(("D", f"{name}: missing required line(s): {', '.join(m.rstrip(':') for m in missing)}"))

    row = (f"{name:<28} {nbytes:>7}  {a_size:>9}  {a_state:<7} {b_state:<7} "
           f"{'pass' if c_ok else 'FAIL':<7} {'pass' if d_ok else 'FAIL':<7}")
    return row, findings


def self_test():
    """Every fixture card must trip exactly the gate its filename prefix names, and the control none."""
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "refusal")
    cards = sorted(glob.glob(os.path.join(base, "map", "cards", "*.md")))
    territory = os.path.join(base, "territory")
    if not cards or not os.path.isdir(territory):
        print(f"FATAL  fixtures missing under {base}", file=sys.stderr)
        return 2

    wrong = []
    print(f"{'fixture':<28} {'expected':<9} {'tripped':<9} result")
    print("-" * 60)
    for card in cards:
        name = os.path.basename(card)
        prefix = name.split("-", 1)[0]
        expected = set() if prefix == "ok" else {prefix.upper()}
        _row, findings = check_card(card, territory, True)
        tripped = {gate for gate, _ in findings}
        ok = tripped == expected
        print(f"{name:<28} {','.join(sorted(expected)) or '—':<9} {','.join(sorted(tripped)) or '—':<9} "
              f"{'ok' if ok else 'WRONG'}")
        if not ok:
            wrong.append(name)

    gates_shown = {name.split("-", 1)[0].upper() for name in map(os.path.basename, cards)} - {"OK"}
    unshown = set("ABCD") - gates_shown
    print("-" * 60)
    if unshown:
        print(f"\nSELF-TEST FAILED — no fixture shows gate(s) {', '.join(sorted(unshown))} failing.")
        return 1
    if wrong:
        print(f"\nSELF-TEST FAILED — {len(wrong)} fixture(s) did not trip what their name says: {', '.join(wrong)}")
        return 1
    print("\nSELF-TEST PASSED — each of A, B, C and D was shown failing on its own fixture, and the "
          "control card passed all four.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", help="directory containing cards/")
    ap.add_argument("--territory", help="the folder the map describes")
    ap.add_argument("--self-test", action="store_true", help="run against fixtures/refusal/ and expect failures")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.map or not args.territory:
        ap.error("--map and --territory are required unless --self-test is given")

    cards_dir = os.path.join(args.map, "cards")
    if not os.path.isdir(cards_dir):
        print(f"FATAL  no cards/ under {args.map}", file=sys.stderr)
        return 2
    cards = sorted(glob.glob(os.path.join(cards_dir, "*.md")))
    if not cards:
        print(f"FATAL  no cards in {cards_dir}", file=sys.stderr)
        return 2

    territory = os.path.abspath(args.territory)
    have_territory = os.path.isdir(territory)
    if not have_territory:
        print(f"NOTE   territory not on disk: {territory} — A and B will be SKIPPED, C will FAIL\n")

    print(f"map        {os.path.abspath(args.map)}")
    print(f"territory  {territory}")
    print(f"cards      {len(cards)}   run limit  {RUN} chars\n")

    failures = []
    tripped = set()
    print(f"{'card':<28} {'bytes':>7}  {'A cites':>9}  {'A':<7} {'B':<7} {'C':<7} {'D':<7}")
    print("-" * 80)

    for card in cards:
        row, findings = check_card(card, territory, have_territory)
        for gate, finding in findings:
            failures.append(finding)
            tripped.add(gate)
        print(row)

    print("-" * 80)
    if failures:
        print(f"\nFAILED — {len(failures)} finding(s):")
        for f in failures:
            print(f"  · {f}")
        # Name the fix for the checks that actually tripped. A single trailer sends the reader to
        # the wrong repair whenever the failure was C or D.
        guidance = {
            "A": "A — the card is not smaller than what it cites: cite the file instead of restating it.",
            "B": f"B — a run over {RUN} characters is shared verbatim with a cited file: that is a "
                 "photocopy, quote less and point more.",
            "C": "C — a cited path is missing or does not resolve in the territory: fix the path, or add "
                 "the **Source path:** line. A card pointing at nothing cannot be checked against anything.",
            "D": "D — a required line is missing: every card ships Hits, Does not hit and Done when.",
        }
        for key in ("A", "B", "C", "D"):
            if key in tripped:
                print(f"\n{guidance[key]}")
        return 1
    print("\nPASSED — every card is smaller than what it cites, shares no verbatim run over "
          f"{RUN} characters with it, cites at least one path that resolves, and carries Hits, "
          "Does not hit and Done when.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
