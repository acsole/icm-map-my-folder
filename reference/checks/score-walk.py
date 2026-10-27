#!/usr/bin/env python3
"""Walk scorer — the offline half of the cold-run gate. Standard library only; no network, no key.

    python3 score-walk.py --walks walks/ --map . --territory ./your-market-realtor
    python3 score-walk.py --self-test

`cold-run.py` (the runner, which needs the API) records each walk as JSON in walks/transcripts/.
This script reads those transcripts and the question files in walks/questions/, and writes one
verdict per question to walks/verdicts/<id>.check.md, first line `pass` or `fail: <why>`.

Six gates per transcript:

  W1 integrity  the transcript is of THIS map: same question, same configuration, and every file it
                read (and the catalog it was given) hashes to the file on disk now
  W2 landed     it opened the card the question expects
  W3 budget     it opened no more files than the question allows
  W4 no slurp   it opened no more territory files than the question tolerates
  W5 stopped    it ended the turn itself instead of running out of turns
  W6 answer     its final answer names every must-mention group (any one term per group)

Per question: W1, W2, W5 and W6 must pass on every run; W3 and W4 are a spread and must pass on at
least `spread_min` runs. Fewer recorded runs than `runs_required` is a fail — an unrecorded walk is
not a passing one.

What this does not prove: that a transcript came from a real API call. It proves the transcript is
consistent with this map and with the rules. Message ids and token usage are recorded so that anyone
with a key can re-run and compare spreads.

Hashes are SHA-256 over the file's bytes with CRLF turned into LF, so a Windows checkout and a Unix
checkout of the same commit hash the same.

Exit 0 = every question passed. Exit 1 = at least one failed. Exit 2 = could not run (bad paths).
--self-test scores fixtures/walk/, where each transcript trips exactly the gate its filename prefix
names (`w1-` → W1, … `ok-` → none); exit 0 only if every one does.

Written by Andrés Curcio for the revision of Map My Folder (original by Gabriel Azoulay), from the
Comp #11 feedback, with the original author's permission. See CHANGES.md.
"""

import argparse
import glob
import hashlib
import json
import os
import posixpath
import sys

STRICT = ("W1", "W2", "W5", "W6")
SPREAD = ("W3", "W4")
GATES = STRICT[:2] + SPREAD + STRICT[2:]  # W1 W2 W3 W4 W5 W6, in reading order


def file_sha256(path):
    """Same function as in cold-run.py — keep the two in step."""
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def norm(path):
    path = posixpath.normpath(path.replace("\\", "/"))
    return "" if path == "." else path.lstrip("/")


def read_question(path):
    """Frontmatter between two `---` lines; each value is JSON if it parses, else a plain string."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: no frontmatter")
    q = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        try:
            q[key.strip()] = json.loads(value)
        except ValueError:
            q[key.strip()] = value
    for key in ("id", "question", "configuration", "expect_card", "max_reads",
                "territory_reads_allowed", "must_mention", "runs_required", "spread_min"):
        if key not in q:
            raise ValueError(f"{path}: frontmatter has no `{key}`")
    q["expect_card"] = norm(q["expect_card"])
    return q


def score_transcript(t, q, roots):
    """Return {gate: None if passed, else the reason it failed}."""
    out = {g: None for g in GATES}
    reads = [dict(r, path=norm(r["path"])) for r in t.get("file_reads", [])]

    # W1 — the transcript is of this question and this map
    problems = []
    if t.get("question") != q["question"]:
        problems.append("question text differs from the question file")
    if t.get("configuration") != q["configuration"]:
        problems.append(f"configuration {t.get('configuration')!r}, question wants {q['configuration']!r}")
    catalog = t.get("catalog")
    if q["configuration"] == "catalog_in_context":
        if not catalog:
            problems.append("no catalog recorded for a catalog_in_context run")
        else:
            problems.extend(hash_problems("map", norm(catalog["path"]), catalog.get("sha256"), roots))
    for r in reads:
        problems.extend(hash_problems(r["root"], r["path"], r.get("sha256"), roots))
    if problems:
        out["W1"] = "; ".join(problems)

    # W2 — it opened the expected card
    if not any(r["root"] == "map" and r["path"] == q["expect_card"] for r in reads):
        out["W2"] = f"never opened {q['expect_card']}"

    # W3 — budget
    if len(reads) > q["max_reads"]:
        out["W3"] = f"{len(reads)} files opened, budget {q['max_reads']}"

    # W4 — territory reads
    territory_reads = [r["path"] for r in reads if r["root"] == "repo"]
    if len(territory_reads) > q["territory_reads_allowed"]:
        out["W4"] = (f"{len(territory_reads)} territory file(s) opened, {q['territory_reads_allowed']} "
                     f"tolerated: {', '.join(territory_reads)}")

    # W5 — it stopped on its own
    if t.get("final_stop_reason") != "end_turn":
        out["W5"] = f"ended on {t.get('final_stop_reason')!r} after {t.get('turns')} turn(s)"

    # W6 — the answer names what matters
    answer = (t.get("final_answer") or "").casefold()
    missing = [group for group in q["must_mention"] if not any(term.casefold() in answer for term in group)]
    if missing:
        out["W6"] = "answer names none of: " + " | ".join(" / ".join(g) for g in missing)

    return out


def hash_problems(root, path, recorded, roots):
    base = roots.get(root)
    if base is None:
        return [f"{root}:{path} cannot be checked — no --{'territory' if root == 'repo' else root} given"]
    full = os.path.join(base, path)
    if recorded is None:  # the runner found nothing there; it must still be nothing
        return [f"{root}:{path} was missing when recorded and exists now"] if os.path.isfile(full) else []
    if not os.path.isfile(full):
        return [f"{root}:{path} was read but is not on disk now"]
    if file_sha256(full) != recorded:
        return [f"{root}:{path} has changed since the walk was recorded"]
    return []


def score_question(q, transcripts, roots):
    """Return (verdict line, per-run rows)."""
    rows = [(name, score_transcript(t, q, roots)) for name, t in transcripts]
    n = len(rows)
    if n < q["runs_required"]:
        return f"fail: {n} of {q['runs_required']} runs recorded", rows
    reasons = []
    for gate in STRICT:
        bad = sum(1 for _, r in rows if r[gate])
        if bad:
            reasons.append(f"{gate} failed on {bad} of {n} runs")
    for gate in SPREAD:
        good = sum(1 for _, r in rows if not r[gate])
        if good < q["spread_min"]:
            reasons.append(f"{gate} passed on {good} of {n} runs, needs {q['spread_min']}")
    return ("fail: " + "; ".join(reasons)) if reasons else "pass", rows


def load_transcripts(directory, qid):
    out = []
    for path in sorted(glob.glob(os.path.join(directory, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            t = json.load(fh)
        if t.get("question_id") == qid:
            out.append((os.path.basename(path), t))
    return out


def render_verdict(q, verdict, rows):
    lines = [verdict, "", f"# Walk verdict — {q['id']}", "",
             f"**Question:** {q['question']}  ",
             f"**Configuration:** `{q['configuration']}` · **expects:** `{q['expect_card']}` · "
             f"**budget:** {q['max_reads']} read(s), {q['territory_reads_allowed']} territory · "
             f"**runs required:** {q['runs_required']}, spread gates on at least {q['spread_min']}", "",
             "Generated by `reference/checks/score-walk.py`. Do not edit by hand.", ""]
    if rows:
        lines.append("| transcript | " + " | ".join(GATES) + " |")
        lines.append("|---|" + "---|" * len(GATES))
        for name, r in rows:
            lines.append(f"| `{name}` | " + " | ".join("pass" if not r[g] else "FAIL" for g in GATES) + " |")
        failures = [(name, g, r[g]) for name, r in rows for g in GATES if r[g]]
        if failures:
            lines += ["", "## Why"]
            lines += [f"- `{name}` {g}: {why}" for name, g, why in failures]
    else:
        lines.append("No transcripts recorded for this question yet. Record them with `cold-run.py`.")
    return "\n".join(lines) + "\n"


def self_test():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "walk")
    roots = {"map": os.path.join(base, "map"), "repo": os.path.join(base, "territory")}
    try:
        q = read_question(os.path.join(base, "question.md"))
    except (OSError, ValueError) as exc:
        print(f"FATAL  {exc}", file=sys.stderr)
        return 2
    paths = sorted(glob.glob(os.path.join(base, "transcripts", "*.json")))
    if not paths:
        print(f"FATAL  no fixture transcripts under {base}", file=sys.stderr)
        return 2

    wrong, shown, loaded = [], set(), {}
    print(f"{'fixture':<26} {'expected':<9} {'tripped':<12} result")
    print("-" * 60)
    for path in paths:
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            loaded[name] = json.load(fh)
        prefix = name.split("-", 1)[0]
        expected = set() if prefix == "ok" else {prefix.upper()}
        shown |= expected
        tripped = {g for g, why in score_transcript(loaded[name], q, roots).items() if why}
        ok = tripped == expected
        print(f"{name:<26} {','.join(sorted(expected)) or '-':<9} {','.join(sorted(tripped)) or '-':<12} "
              f"{'ok' if ok else 'WRONG'}")
        if not ok:
            wrong.append(name)

    # The aggregation rule has to be able to fail too.
    control = [(n, t) for n, t in loaded.items() if n.startswith("ok-")]
    broken = [(n, t) for n, t in loaded.items() if n.startswith("w2-")]
    one_run = dict(q, runs_required=1, spread_min=1)
    cases = [
        ("control alone, 1 run required", one_run, control, True),
        ("no runs recorded", one_run, [], False),
        ("control + a strict-gate failure", dict(one_run, runs_required=2), control + broken, False),
        ("fewer runs than required", dict(one_run, runs_required=len(control) + 1), control, False),
    ]
    print("-" * 60)
    for label, question, runs, should_pass in cases:
        verdict, _ = score_question(question, runs, roots)
        ok = (verdict == "pass") == should_pass
        print(f"aggregate: {label:<40} {'pass' if verdict == 'pass' else 'fail'}  {'ok' if ok else 'WRONG'}")
        if not ok:
            wrong.append(f"aggregate: {label}")

    print("-" * 60)
    unshown = set(GATES) - shown
    if unshown:
        print(f"\nSELF-TEST FAILED — no fixture shows {', '.join(sorted(unshown))} failing.")
        return 1
    if wrong:
        print(f"\nSELF-TEST FAILED — {len(wrong)} case(s) did not behave as named: {', '.join(wrong)}")
        return 1
    print("\nSELF-TEST PASSED — each of W1 to W6 was shown failing on its own fixture, the control "
          "passed all six, and the per-question rule failed every case it should.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--walks", help="folder holding questions/, transcripts/ and verdicts/")
    ap.add_argument("--map", help="root of the map the transcripts read (the 'map' root)")
    ap.add_argument("--territory", help="the repository the map describes (the 'repo' root)")
    ap.add_argument("--self-test", action="store_true", help="score fixtures/walk/ and expect failures")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.walks or not args.map:
        ap.error("--walks and --map are required unless --self-test is given")

    questions = sorted(glob.glob(os.path.join(args.walks, "questions", "*.md")))
    if not questions or not os.path.isdir(args.map):
        print(f"FATAL  no questions under {args.walks}/questions, or no map at {args.map}", file=sys.stderr)
        return 2
    roots = {"map": os.path.abspath(args.map)}
    if args.territory:
        if not os.path.isdir(args.territory):
            print(f"FATAL  territory not on disk: {args.territory}", file=sys.stderr)
            return 2
        roots["repo"] = os.path.abspath(args.territory)

    verdict_dir = os.path.join(args.walks, "verdicts")
    os.makedirs(verdict_dir, exist_ok=True)
    failed = 0
    for path in questions:
        q = read_question(path)
        transcripts = load_transcripts(os.path.join(args.walks, "transcripts"), q["id"])
        verdict, rows = score_question(q, transcripts, roots)
        with open(os.path.join(verdict_dir, f"{q['id']}.check.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_verdict(q, verdict, rows))
        print(f"{q['id']:<28} {len(rows)} run(s)   {verdict}")
        failed += verdict != "pass"

    print(f"\nVerdicts written to {verdict_dir}.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
