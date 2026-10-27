# Walks — the evidence that a cold reader can use the map

Two steps, run in order. The first needs the API and is run once, by whoever made the map. The second
needs nothing and is run by anyone, as often as they like.

    questions/  ──►  cold-run.py  ──►  transcripts/  ──►  score-walk.py  ──►  verdicts/
    (factory)        (online)          (product)           (offline)          (check)

## Inputs

- **Reference, every run:** `questions/*.md` — one question per file. Stable; changing one invalidates
  every transcript recorded against it (W1 catches that).
- **Working, this run:** the map at this commit, and the territory at the commit the map pins.

## Step 1 — record (online)

    pip install anthropic
    QUESTION_FILE=walks/questions/<id>.md RUNS=5 TERRITORY_DIR=<territory> \
        python3 reference/checks/cold-run.py

Writes `transcripts/<id>.<timestamp>.r<n>.json`. Never edit a transcript by hand; a walk that went
badly is recorded as it went.

**Or record through Claude Code, with a subscription instead of a key:**

    QUESTION_FILE=walks/questions/<id>.md RUNS=5 TERRITORY_DIR=<territory> \
        python3 reference/checks/cold-run-claude-code.py

Same question, same system prompt, same transcript format; the reader runs inside `claude -p` with
only `Read` and `Glob`. Writes `transcripts/<id>.cc.<timestamp>.r<n>.json`, marked
`"harness": "claude-code-headless"`. The scorer judges each harness apart and writes its own verdict
(`verdicts/<id>.claude-code-headless.check.md`); it never pools them. Run with `ISOLATION_PROBE=1`
first to see what context the reader was given.

## Step 2 — score (offline)

    python3 reference/checks/score-walk.py --walks walks/ --map . --territory <territory>

Writes `verdicts/<id>.check.md`. The first line is `pass` or `fail: <why>`. Generated, never edited.

## Check

The scorer itself is checked first: `python3 reference/checks/score-walk.py --self-test` must exit 0,
showing each gate W1–W6 failing on its own fixture. A verdict from a scorer that has not been shown
failing is taken on trust.

## A question file

```
---
id: q01-services                    # also the transcript prefix
question: "What is Services?"       # sent verbatim, as the user's only message
author: builder                     # builder | outsider — who wrote the question
configuration: catalog_in_context   # catalog_in_context | unframed
catalog: reference/worked-example/CATALOG.md
expect_card: reference/worked-example/cards/04-the-six-slots.md
max_reads: 1                        # files opened, catalog in context not counted
territory_reads_allowed: 0
must_mention: [["slot"], ["vendor", "third-party"]]   # every group; any term in a group
runs_required: 5
spread_min: 4                       # W3 and W4 must pass on at least this many runs
---
```

Values after the colon are read as JSON when they parse, so lists are written as JSON. Decide what
counts as passing **before** recording any run; a bar set after seeing the answers is not a bar.

## Not loaded here

The making instrument (`identity.md`, `rules.md`) and the cards themselves. Neither step needs them
in context: the runner hands the model folders, and the scorer reads files only to hash them.

---

*Added by Andrés Curcio in the revision of Map My Folder (original by Gabriel Azoulay), from the
Comp #11 feedback, with the original author's permission. Why each choice was made:
[`CHANGES.md`](../CHANGES.md).*
