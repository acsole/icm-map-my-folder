#!/usr/bin/env python3
"""Freshness — which cards cite a file that has changed since the map was pinned. Needs only git.

    python3 freshness-check.py --map <dir with CATALOG.md> --territory <git checkout> [--against REV]
    python3 freshness-check.py --self-test

A map is pinned to one commit of its territory (the top catalog says `mapped at commit `<sha>``).
The territory keeps moving. A card whose evidence was read at the pin can be wrong today, and nothing
in the card says so. This check asks git which files changed between the pin and --against (default:
the territory's HEAD; use `origin/main` to compare with what the world sees) and names every card
that cites one of them. It does not decide that a card is wrong — only that it must be re-verified
before the map is re-pinned. The cards it does not name need nothing.

What counts as citing a file: every backticked token on the card that looks like a path, with any
`:line` suffix dropped and `<slug>`/`[slug]` placeholders read as wildcards. A token that does not
resolve from the territory's root (`frameworks/pricing.md`) is matched against every file that ends
with it — `market.md` matches all five. That is conservative on purpose: it can flag a card that did
not need it, never miss one that did.

Exit 0 = no card is stale. Exit 1 = at least one is. Exit 2 = could not run (no pin, no git).
--self-test builds a small git territory in a temporary folder, changes one file after the pin, and
passes only if exactly the card citing that file is named — and none when compared with the pin.

Written by Andrés Curcio for the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission. See CHANGES.md.
"""

import argparse
import fnmatch
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

PIN_RE = re.compile(r"mapped at commit `([0-9a-f]{7,40})`")
TICKED_RE = re.compile(r"`([^`\n]+)`")


def git(territory, *args):
    return subprocess.run(["git", "-C", territory, *args], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def card_files(map_dir):
    top = sorted(glob.glob(os.path.join(map_dir, "cards", "*.md")))
    districts = sorted(glob.glob(os.path.join(map_dir, "districts", "*", "cards", "*.md")))
    return top + districts


def cited_tokens(text):
    out = []
    for tok in TICKED_RE.findall(text):
        tok = re.sub(r":[\d,\-–]+$", "", tok.strip()).rstrip("/,.;")
        if " " in tok or not tok:
            continue
        if "/" in tok or re.search(r"\.(md|py|html|json|ya?ml|txt|sh|toml|png)$", tok):
            out.append(tok)
    return out


def resolve(token, tracked):
    """Tracked files (repo-relative, '/'-separated) the token refers to."""
    pattern = re.sub(r"<[^>/]+>|\[[^\]/]+\]", "*", token).lstrip("./")
    if pattern.endswith("/") or not os.path.splitext(pattern)[1]:
        prefix = pattern.rstrip("/") + "/"
        under = [f for f in tracked if fnmatch.fnmatch(f, prefix + "*") or f.startswith(prefix)]
        if under:
            return under
    exact = [f for f in tracked if fnmatch.fnmatch(f, pattern)]
    if exact:
        return exact
    return [f for f in tracked if fnmatch.fnmatch(f, "*/" + pattern)]


def check(map_dir, territory, against):
    """Return (pin, against_sha, changed files, {card: [changed files it cites]})."""
    catalog = os.path.join(map_dir, "CATALOG.md")
    with open(catalog, encoding="utf-8") as fh:
        m = PIN_RE.search(fh.read())
    if not m:
        raise ValueError(f"no `mapped at commit` pin in {catalog}")
    pin = m.group(1)
    target = git(territory, "rev-parse", "--short", against).strip()
    changed = set(git(territory, "diff", "--name-only", pin, against).split())
    tracked = git(territory, "ls-tree", "-r", "--name-only", against).split()
    stale = {}
    for card in card_files(map_dir):
        with open(card, encoding="utf-8") as fh:
            text = fh.read()
        hits = sorted({f for tok in cited_tokens(text) for f in resolve(tok, tracked) if f in changed})
        if hits:
            stale[os.path.relpath(card, map_dir).replace(os.sep, "/")] = hits
    return pin, target, changed, stale


def report(pin, target, changed, stale, n_cards):
    print(f"pinned at {pin}, compared with {target}: {len(changed)} file(s) changed in the territory")
    for f in sorted(changed):
        print(f"  changed  {f}")
    print()
    if not stale:
        print(f"FRESH - none of the {n_cards} cards cites a file that changed.")
        return 0
    for card, files in stale.items():
        print(f"STALE  {card}  <- {', '.join(files)}")
    print(f"\n{len(stale)} of {n_cards} card(s) must be re-verified before the map is re-pinned to {target}. "
          "The others need nothing.")
    return 1


def self_test():
    if not shutil.which("git"):
        print("FATAL  git is not on PATH", file=sys.stderr)
        return 2
    root = tempfile.mkdtemp(prefix="freshness-")
    try:
        terr, mp = os.path.join(root, "territory"), os.path.join(root, "map")
        os.makedirs(os.path.join(terr, "engine"))
        os.makedirs(os.path.join(mp, "cards"))
        os.makedirs(os.path.join(mp, "districts", "d", "cards"))
        for path, text in {"engine/rules.md": "rules v1\n", "engine/welcome.md": "hello\n",
                           "docs/index.html": "<p>v1</p>\n"}.items():
            os.makedirs(os.path.dirname(os.path.join(terr, path)), exist_ok=True)
            with open(os.path.join(terr, path), "w", encoding="utf-8") as fh:
                fh.write(text)
        g = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid"]
        subprocess.run(["git", "init", "-q", terr], check=True)
        subprocess.run(["git", "-C", terr, "add", "-A"], check=True)
        subprocess.run(["git", "-C", terr, *g, "commit", "-qm", "pin"], check=True)
        pin = git(terr, "rev-parse", "--short", "HEAD").strip()
        with open(os.path.join(terr, "docs/index.html"), "w", encoding="utf-8") as fh:
            fh.write("<p>v2</p>\n")
        subprocess.run(["git", "-C", terr, *g, "commit", "-qam", "after the pin"], check=True)

        with open(os.path.join(mp, "CATALOG.md"), "w", encoding="utf-8") as fh:
            fh.write(f"# Catalog\n\n**Territory:** fixture · mapped at commit `{pin}`\n")
        cards = {"cards/01-surface.md": "Cites `docs/` and `docs/index.html`.",
                 "cards/02-rules.md": "Cites `engine/rules.md:3`.",
                 "districts/d/cards/1.1-welcome.md": "Cites `welcome.md:2` by its short name."}
        for path, text in cards.items():
            with open(os.path.join(mp, path), "w", encoding="utf-8") as fh:
                fh.write(f"# {path}\n\n{text}\n")

        ok = True
        _, _, _, stale = check(mp, terr, "HEAD")
        print(f"after the pin:  stale = {sorted(stale) or '-'}")
        if sorted(stale) != ["cards/01-surface.md"]:
            ok = False
        _, _, _, stale = check(mp, terr, pin)
        print(f"at the pin:     stale = {sorted(stale) or '-'}")
        if stale:
            ok = False
        if ok:
            print("\nSELF-TEST PASSED - the one card citing the changed file was named, the two citing "
                  "unchanged files (one by a short path, inside a district) were not, and nothing was "
                  "stale at the pin itself.")
            return 0
        print("\nSELF-TEST FAILED - the stale set was not exactly what the fixture planted.")
        return 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", help="directory holding the top CATALOG.md")
    ap.add_argument("--territory", help="a git checkout of the territory")
    ap.add_argument("--against", default="HEAD", help="revision to compare the pin with (default HEAD)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.map and args.territory):
        ap.error("--map and --territory are required unless --self-test is given")
    try:
        pin, target, changed, stale = check(args.map, args.territory, args.against)
    except (ValueError, subprocess.CalledProcessError, OSError) as exc:
        print(f"FATAL  {exc}", file=sys.stderr)
        return 2
    return report(pin, target, changed, stale, len(card_files(args.map)))


if __name__ == "__main__":
    sys.exit(main())
