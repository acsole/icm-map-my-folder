# Changes — the revision made from the Comp #11 feedback

**Original:** Map My Folder by Gabriel Azoulay (Gabe — Your AI Specialist,
[@NFTYoginis](https://github.com/NFTYoginis)), submitted to *Comp #11: The Cartographer* at commit
`d58a746` of [`NFTYoginis/map-my-folder`](https://github.com/NFTYoginis/map-my-folder).
**Revision:** Andrés Curcio ([@acsole](https://github.com/acsole)), from the judges' feedback on that
commit, with the original author's permission. Everything below `d58a746` is the original work and
is unchanged unless this page names it.

Plain-language version of the whole project: [`EXPLAINED.md`](EXPLAINED.md).

---

## What the judges said

Three notes, from the feedback on `d58a746`:

1. **Make the cold run work offline.** It needed the `anthropic` package and an API key, so the one
   check that tests a real reader was the one a judge could not run. Their suggestion: split it into
   a runner and a scorer, where the scorer reads a saved transcript.
2. **Seven cards is a small shelf.** The territory has more nouns than seven, and the gates would
   hold at three times the size.
3. **To move up a tier:** a bigger map, or a territory with a business behind it.

The feedback to other entrants added a fourth, which applied here too: **a gate nobody has seen fail
is taken on trust.** The landing page showed two bad cards failing, but those cards were not in the
repo, so nobody could reproduce it.

## What this revision does — and does not — do

| Note | Status | Where |
|---|---|---|
| 1. Offline cold run | **Done.** Runner and scorer are separate; the scorer needs nothing installed | [`score-walk.py`](reference/checks/score-walk.py), [`cold-run.py`](reference/checks/cold-run.py), [`walks/`](walks/CONTEXT.md) |
| 4. Gates shown failing | **Done.** All three checkers ship broken fixtures and a `--self-test` | [`reference/checks/fixtures/`](reference/checks/fixtures/) |
| 2. Bigger shelf | **Done in part.** The district rule, its checks, and the engine's district: 12 cards where there were 7. Not yet three times the size — see *Next* | [`districts/engine/`](reference/worked-example/districts/engine/CATALOG.md), [`catalog-checks.py`](reference/checks/catalog-checks.py) |
| 3. Business territory | **Not yet.** Designed, not built | — |
| Walks recorded through Claude Code | **Done.** Three questions, five runs each: `q01` **pass**, `q02` **pass**, `q03` (an outsider's) **fail** — see § 6 | [`walks/verdicts/`](walks/verdicts/) |
| Walks recorded through the API | **Not yet.** The recorder exists; recording needs a key and has not been run. That verdict reads `fail: 0 of 5 runs recorded` | [`q01-services.check.md`](walks/verdicts/q01-services.check.md) |

The last row is deliberate. The scorer could have been fed the old API runs, but those survive only
as excerpts in [`cold-run-transcript.md`](reference/worked-example/cold-run-transcript.md), not as
the raw record. Rebuilding them by hand would be inventing evidence. An unrecorded walk is not a
passing one, so the verdict says so — and the Claude Code pass is not counted in its place.

---

## The changes, one at a time

### 1. The cold run became two steps

**Before.** `cold-run.py` asked a fresh model one question, printed what it did, and left the judging
to whoever read the output. To check it you had to run it, and to run it you needed a key.

**After.** Two steps, the output of the first being the input of the second:

    walks/questions/  →  cold-run.py  →  walks/transcripts/  →  score-walk.py  →  walks/verdicts/
                         (online, once)                          (offline, anyone)

- [`cold-run.py`](reference/checks/cold-run.py) — the **runner**. It still needs the API. It now
  writes each run to `walks/transcripts/` as JSON: the question, the configuration, the model and
  effort, both commits, **every file opened with its SHA-256**, the final answer, why it stopped,
  and the API message ids.
- [`score-walk.py`](reference/checks/score-walk.py) — the **scorer**. Standard-library Python, no
  network. It reads the transcripts and writes one verdict per question, first line `pass` or
  `fail: <why>`.
- [`walks/questions/`](walks/questions/) — one file per question, carrying its **pass bar, written
  before any run is scored**: which card it should reach, how many files it may open, how many of
  them may be territory, and which words the answer must contain.

**The six gates the scorer runs on every transcript:**

| Gate | The question it answers | It fails when… |
|---|---|---|
| W1 integrity | Is this a walk of *this* map? | a file it read has changed since — its hash no longer matches |
| W2 landed | Did it reach the right card? | the expected card is not among the files it opened |
| W3 budget | Did it keep to "catalog plus one card"? | it opened more files than the question allows |
| W4 no slurp | Did it wander into the territory? | it opened more territory files than the question tolerates |
| W5 stopped | Did it finish on its own? | it ran out of turns instead |
| W6 answer | Did it say what mattered? | a required term is missing — for *Services*, that it means other people's businesses |

**Per question:** W1, W2, W5 and W6 must pass on every run. W3 and W4 must pass on at least four of
five. That rule is the one the original transcript already applied by hand — *"a single run that
comes back 2/1 is inside the spread"* — now written down and enforced.

### 2. Every gate is shown failing

- `python3 reference/checks/refusal-checks.py --self-test` runs the photocopy checks against
  [`fixtures/refusal/`](reference/checks/fixtures/refusal/README.md): one sound card and four broken
  ones, each broken in a single way. It passes only if each broken card fails **exactly** the gate
  its filename names, and the sound one fails none.
- `python3 reference/checks/score-walk.py --self-test` does the same for walks with
  [`fixtures/walk/`](reference/checks/fixtures/walk/): six broken transcripts, one per gate, and one
  sound one. It also checks that the per-question rule fails when it should — no runs, too few runs,
  one strict failure among good runs.

`refusal-checks.py` itself checks exactly what it checked before. Its loop moved into a function so
the self-test can see which gate each card trips; the output against the real map is unchanged.

### 3. A second way to record walks — through Claude Code, without an API key

The API runner needs a key and pays per token. [`cold-run-claude-code.py`](reference/checks/cold-run-claude-code.py)
records the same walk through the Claude Code CLI (`claude -p`), signed in with a Claude subscription.
Same question files, same system prompt, same transcript format, so the same scorer judges it. The
reader gets only Claude Code's `Read` (a hop) and `Glob` (a listing, free).

**It is a different harness, and it is labelled as one.** Every transcript carries
`"harness": "claude-code-headless"`, and the scorer writes a separate verdict for each harness
(`walks/verdicts/<id>.claude-code-headless.check.md`) and never pools them. A pass here is real
evidence that a cold Claude can use the map; it is not the API run under another name.

**Making the reader cold took three findings.** Tested with a probe that asks the reader what
context it was given (`ISOLATION_PROBE=1`):

1. Out of the box, the CLI loaded the operator's own global `CLAUDE.md` into the reader's context.
   `--bare` would stop that, but `--bare` requires an API key, which is what this harness avoids.
   `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` stop it without one.
2. Run from inside another Claude session, the CLI inherits that session's variables (its working
   folders, its scratchpad). The runner drops every inherited `CLAUDE*` variable except the ones
   sign-in needs.
3. The signed-in account's email still reaches the reader, and nothing short of an API key removes
   it. It says nothing about the map, so it cannot help a walk; and any email address the reader
   repeats is replaced with `[email redacted]` before the transcript is written, with the count kept
   in `"redactions"`.

### 4. The first local walks failed — on the bar, not on the map

Five walks under the first pass bar of `q01-services` failed W6 on four runs. All five landed on card
04, opened nothing else, stopped, and answered correctly; the bar demanded the word *slot*, the map's
own term, and four answers said "one of the six standard files" instead. A bar that requires the
map's jargon tests repetition, not understanding.

The bar was revised once, in the open, with the reason written in the question file. The five runs,
the old question file and their failing verdict are kept in
[`walks/archive/q01-bar-v1/`](walks/archive/q01-bar-v1/README.md) and were **not** re-scored — passing
them now would be scoring the answers that prompted the change. Five new runs were recorded against
the revised bar.

**Result under the revised bar: pass.** All five runs landed on card 04 and stopped; all five named
the collision. Four opened only the card. One also opened the blank template's `services.md` in the
territory, which fails W3 and W4 for that run and is inside the four-of-five spread. That is the same
spread the original API evidence reported — four runs at one read, one at two with a territory file —
measured again, by a different harness, without a key. No email address appeared in any transcript.

### 5. A bigger map that still fits on one screen — the district rule

**The problem.** The judges asked for a bigger shelf; the instrument said "no eighth card". Deleting
the ceiling would break the best thing about the map — a catalog you read on one screen.

**The rule now.** Seven *rows per catalog*, not seven cards per map. A row may open a **district**: a
catalog one level down, under the same rule — seven rows at most, routing only, one card per row.
Districts are one level deep. Written into [`identity.md`](identity.md),
[`rules.md`](rules.md), [`card-types.md`](reference/card-types.md) § The ceiling and
[`walks.md`](reference/walks.md), with the cost declared where the rule is: browsing by concept
costs one more file (catalog, district, card); arriving with a file in hand costs none, because the
top catalog's *hand on a file* table routes straight to the card.

**The checks.** [`catalog-checks.py`](reference/checks/catalog-checks.py), offline:

| Gate | It fails when… |
|---|---|
| E one card, one row | a card no row reaches, a card two rows reach, or a row that links to nothing |
| F thin catalog | a catalog over seven rows, a district inside a district, or a catalog stating a count of cards, rows or files |

Its `--self-test` runs seven small maps in [`fixtures/catalog/`](reference/checks/fixtures/catalog/README.md),
six broken one way each. On its first run against the real map, F failed: the top catalog said
"Seven cards, and the ceiling was reached" — a count that the district would have made false. It
now names the rule instead of the number.

**The district.** The first map held the engine in one card. A question about its jobs, frameworks,
templates or checklists needed card 01 *and* the territory — by the map's own rule, the sign of a
mis-scoped card. Row 1 of the top catalog now opens
[`districts/engine/`](reference/worked-example/districts/engine/CATALOG.md), Walk A run again on
`specialist/` at the same commit, `702e79c`:

| Card | Type · State | What it carries that the map lacked |
|---|---|---|
| 1.1 The Engine | ENGINE · LIVE | unchanged — card 01, now reached from the district |
| 1.2 The Job Set | MARKER · LIVE, two LEFTOVER sentences | `rules.md:7` and `:18` still count v1's three jobs; the table routes five |
| 1.3 The First Turn | ENGINE · LIVE | the menu reads each market's `region/market.md`, and an empty region pack replaces it |
| 1.4 The Frameworks | ENGINE · LIVE | the method is here; the numbers it applies are in each market's `region/market.md` |
| 1.5 The Output Templates | ENGINE · LIVE | showing notes are durable input, cited by tag later; Services lookup has no template |
| 1.6 The Intake Checklists | ENGINE · LIVE | Pricing asks from `listing-intake.md` though its routing row lists no checklist |

Each verdict's command and output is in [`verification-log.md`](reference/worked-example/verification-log.md)
§ g. The collision pass ran first and found one new word, **template** — a blank copied once, or the
output shape every run follows — now in [`collisions.md`](reference/collisions.md).
[`notes.md`](reference/worked-example/notes.md) records what moved out of card 01 and why, and one
new **UNVERIFIED**: whether a run reads `examples.md` at all.

Gabriel's seven cards are unchanged in substance. One line on card 05 said "at the seven-card
ceiling"; it now says "with its catalog full", because the old phrasing stated the rule this
revision replaced.

**Walking the bigger map.** Changing the top catalog changed what every catalog-in-context walk had
in its context, so the five `q01` runs recorded before it fail W1 now — W1 working as designed. They
were archived ([`walks/archive/q01-map-before-district/`](walks/archive/q01-map-before-district/README.md))
and `q01` was recorded again. Two questions were added: `q02`, written by the builder for the new
district, and `q03`, written by **an outsider** — a fresh, isolated session given only the
territory's public README and asked what a new maintainer would ask (the first of its three
questions was taken, by order). Results are in § 6.

**Rejected.** Raising the ceiling to twenty-one cards on one catalog (no longer one screen); one
card per engine file (most would fail the Does-not-hit test — no plausible wrong reach); and
re-pinning the map to the territory's newest commit (the three later commits touch only
`docs/index.html`; re-pinning would re-verify every card for no change in `specialist/`).

### 6. Three questions walked through Claude Code — two pass, the outsider's does not

| Question | Written by | Verdict | What the walks showed |
|---|---|---|---|
| `q01` What is Services? | builder | **pass** | unchanged by the district: card 04, stop |
| `q02` Can the specialist write showing notes? | builder | **pass**, second attempt | all five reached card 1.2 straight from the *hand on a file* table and named both leftover sentences |
| `q03` If I rename a section in a `region/` template file, what depends on that wording…? | outsider | **fail**, twice | it found a gap no builder walk had; the fix closed the gap in the answers but not the reading |

**`q02`, first attempt: a stop condition too loose.** Every run answered correctly, then opened
`rules.md` to re-read the lines the card had just quoted — the card's *Done when* did not say not to.
The card was fixed, the bar was not; four of five new runs stayed on the map, inside the spread.
Archived: [`walks/archive/q02-map-before-done-when-fix/`](walks/archive/q02-map-before-done-when-fix/README.md).

**`q03`, first attempt: a gap in the map.** Every run left the map for eleven to fourteen territory
files, and was right to. Three engine lines name sections *inside* `market.md` by heading
(`frameworks/pricing.md:46`, `frameworks/international-buyers.md:82`, `templates/listing.md:11`),
and Lisbon's headings already differ from the blank's. No card said so; the question file, written
by the builder, claimed the opposite. Card 02 now says it, with the evidence in
[`verification-log.md`](reference/worked-example/verification-log.md) § h, and the question file
keeps its wrong claim with the correction beneath it. Archived:
[`walks/archive/q03-map-before-heading-fix/`](walks/archive/q03-map-before-heading-fix/README.md).

**`q03`, second attempt: still a fail, and it is reported as one.** All five answers now cite the
three heading lines and Lisbon's drift, so the gap is closed in what the reader *knows*. But every run
still opened ten to twenty-one territory files, and three of five took card 04 instead of card 02.
Two findings, both about the map, taken up in § 7:

1. **The question routes to two cards.** "A `region/` template file" matches card 02's row (the blank
   `region/` folder) and card 04's *hand on a file* row (`market.md` and the other five filenames).
   By the map's own rule, a question that needs two cards means one of them is mis-scoped.
2. **"What depends on this exact wording?" is an audit, and readers treat it as one.** A card can
   name the dependencies; it cannot make a careful reader stop before checking that the list is
   complete. Whether a map should answer that question at all, or point at the `grep` that does, is
   an open design question — not one to settle by loosening the bar after seeing the runs.

The bar for `q03` was not changed. The verdict on disk reads `fail`, and that is the honest reading.

### 7. The second round on `q03` — four defects in the map, one rule for audits

**What the second attempt's answers said.** The transcripts do not record why a reader picks a card,
but the answers say why they kept reading. Four causes, all in the map:

1. **One file, two rows.** The top catalog's *hand on a file* table sent `market.md` to card 04 by
   name and `specialist/reference/region/` to card 02 by folder. The blank's `market.md` matched
   both. Three of five runs took card 04.
2. **Two cards disagreed.** Card 04 said the engine addresses slots by filename; card 02 now said it
   also reads sections by heading. Runs that took card 04 believed it and went to look (r1, r3).
3. **The list was incomplete.** Card 02 named `international-buyers.md:82`; a run found the same
   section named at `:13` too (r4). A careful reader was right not to trust it.
4. **The reader cannot search.** Both harnesses give `Read` and a listing, nothing else. One run said
   it outright: "A full-text search of `specialist/` … would settle it" (r2). Without search, an
   audit is reading every file.

**Which card owns the question — decided from the types, not from the bar.** "A `region/` template
file" is a file of the blank: a BLUEPRINT, and what an edit to the blank reaches is card 02's *Hits*.
Card 04 is the role a filename plays in every market. The expected card stayed 02; the map was
made to agree with that, not the other way round.

**How the map answers an audit — a rule in the instrument.** A card may answer "what depends on
this?" only if it carries the complete list, the command that produced it and the commit it ran at,
and its stop condition says to answer from the list. If the list is too long, the card hands over
the command and the count instead. Written into [`card-shape.md`](reference/card-shape.md) and the
*Done when* check in [`rules.md`](rules.md).

**The command.** [`heading-refs.py`](reference/checks/heading-refs.py) lists every engine line that
names a blank region file *and* one of that file's section headings — whole, or by its distinctive
word. Its limit is stated where it is used: a line that relies on a section without naming the file
is not found. Its `--self-test` plants three references and two decoys; it was also shown failing
when a decoy was added to the expected list. Run on the territory, it found more than the card had:
four sections of `market.md`, not three, and two sections of `regulations.md` — and Lisbon has no
seasonality section at all, though `pricing.md:80` applies seasonality from it. The mapmaker's
classification is in [`verification-log.md`](reference/worked-example/verification-log.md) § h,
which now says its first version was incomplete.

**The fixes, all to the map.** The two hand-table rows are disjoint; card 04 says filename is how a
slot is found, not all the engine relies on, and points to card 02; card 02 carries the complete,
classified list with the command and the commit, and a stop condition for audits.

**Result of the third attempt — still `fail`, and the remaining cause is named.**

| Attempt | Card reached | Territory files per run | Answer correct |
|---|---|---|---|
| 1 | 02, five of five | 11–14 | yes, with a map that lacked the dependency |
| 2 | 02 twice, 04 three times | 10–21 | two of five missed "copy" |
| 3 | **02, five of five** | **1–5** | four of five pass W6 |

The audit rule worked: one run wrote "I didn't re-read the engine files; the card says its list is
complete at commit `702e79c`." What is left:

- **Every run opened the territory's `README.md`**, to check the question's own premise — that the
  upgrade path tells users to keep their region packs (`README.md:270-272`, and the v1 note at
  `:217`). No card carries the upgrade path. That is a real noun missing from the map, and it
  belongs to the public edge — the district planned next. It is not added here: changing the map
  round after round against one question until it passes is fitting the map to the test. It will be
  carded where it belongs, and `q03` walked again then.
- **Three of five still re-read the two verbatim lines** the card quotes, the same habit `q02` showed
  once in five. The card says not to; some readers check anyway. Measured, not hidden.

The bar for `q03` was not changed at any point. All three rounds are in [`walks/archive/`](walks/archive/).

---

## Decisions, and what was rejected

| Decision | Rejected alternative | Why |
|---|---|---|
| Hash every file a walk opens | Trust the transcript as written | Without hashes, a transcript of an older map would score against the new one. W1 is what ties a walk to a version |
| Hash with CRLF turned into LF | Hash raw bytes | Git on Windows rewrites line endings on checkout. Raw hashes would fail every walk recorded on another system |
| Pass bar in the question file, before any run | Judge each run by eye afterwards | A bar set after seeing the answers is not a bar |
| Strict gates every run, spread gates 4 of 5 | All gates every run | The original evidence already had one run open an extra file and still land and stop. Failing that would punish the variance the original page reported honestly |
| Keyword check for the answer (W6) | A second model as judge | A model judge needs a key again, which is the problem this change exists to remove. The keyword check is cruder, and that is said here |
| No automatic fallback to another model in the runner | The API's fallback option | A fallback can switch the model silently mid-measurement. If the model declines, the run is recorded as declined and W5 fails |
| Default model `claude-opus-5-5`, effort `high`, both recorded | Keep the hard-coded `claude-opus-5` | The original model string was fixed in the code. Both are now settings, and every transcript says which was used |
| Old runs kept as history, not scored | Reconstruct their JSON | They survive as excerpts. Reconstructing them would be fabricating the record |
| A separate verdict per harness | One verdict over every transcript of a question | Claude Code adds its own system context and tools around the model. Pooling its runs with API runs would let one stand in for the other |
| A bar that failed for the wrong reason is revised in the open, and the runs it judged are archived, not re-scored | Quietly loosen the bar and re-score the same five answers | Re-scoring the answers that prompted a change is fitting the bar to the result. Archiving keeps the failure visible and makes the pass come from runs recorded after the change |
| Plain-language page added | Rewrite the existing docs | The original files are written for someone already inside the method, and they do that well. A newcomer needs a different door, not a different house |

## What the scorer does not prove

It proves a transcript is consistent with this map and with the rules. It does not prove the
transcript came from a real API call: a JSON file can be written by hand. The message ids and token
usage are recorded so that anyone with a key can re-run the question and compare the spread.

---

## Found while doing this — reported, not repaired

The map does not edit its territory, and neither does this revision. Both findings are against
`your-market-realtor` at `236aae0`, today's `origin/main`.

1. **The territory has moved.** The map is pinned at `702e79c`. Three commits later, `docs/index.html`
   has grown (`git diff --stat 702e79c HEAD` → 8 lines added), so card 07's byte evidence describes a
   page that is no longer served. The photocopy checks still pass; nothing yet notices staleness.
2. **The engine contradicts itself on how many jobs it does.** `specialist/rules.md:18` says
   *"No work outside the three jobs"*. The routing table in the same file (lines 27–31) lists five,
   and line 83 says *"You support five jobs"*. A model that obeys line 18 could refuse two jobs the
   agent is paid for. When this was first found, no card covered it, because no card covered the
   jobs — the judges' second note, seen from inside the territory. It is now card 1.2 of the
   engine's district (§ 5), together with a second v1 sentence it led to, `rules.md:7`.

## Next — designed, not built

- **`q03`, after the public edge district.** Card the upgrade path (`README.md:270-272`, `:217`)
  where it belongs, then walk `q03` again, bar unchanged — and walk the outsider's other two
  questions, so the next fix is tested on questions it was not shaped by.
- **The rest of the bigger map.** The district rule and the engine's district are built (§ 5). Still
  to do: a district for the public edge — the working documents `docs/` serves, the root README —
  and a staleness gate that compares the map's pinned commit with the territory's current one and
  names the cards whose cited files changed.
- **A second territory with a business behind it,** mapped with the instrument unchanged. Two
  territories under the same gates show that the instrument generalizes; one shows that it worked
  once.
- **More walks,** at least half of them asked by someone who did not make the map.

## Check it yourself

    git clone https://github.com/NFTYoginis/your-market-realtor.git
    python3 reference/checks/refusal-checks.py --self-test
    python3 reference/checks/refusal-checks.py --map reference/worked-example --territory ./your-market-realtor
    python3 reference/checks/score-walk.py --self-test
    python3 reference/checks/score-walk.py --walks walks/ --map . --territory ./your-market-realtor

## Files

| File | Change |
|---|---|
| `reference/checks/score-walk.py` | new — the offline scorer; one verdict per harness |
| `reference/checks/cold-run-claude-code.py` | new — the recorder through the Claude Code CLI, with the isolation above |
| `reference/checks/catalog-checks.py` | new — gates E and F for catalogs and districts, with `fixtures/catalog/` |
| `reference/checks/heading-refs.py` | new — the audit command for section-heading dependencies, with `fixtures/heading-refs/` |
| `reference/card-shape.md` | how a card answers a question that quotes the territory, and an audit |
| `identity.md`, `rules.md`, `reference/card-types.md`, `reference/walks.md` | the district rule: seven rows per catalog, a row may open a district one level down |
| `reference/collisions.md` | a sixth collision, **template** |
| `reference/worked-example/districts/engine/` | new — the engine's district: its catalog and cards 1.2–1.6 |
| `reference/worked-example/CATALOG.md`, `notes.md`, `verification-log.md`, `cards/05-the-marker-set.md` | row 1 opens the district; the count removed from the catalog; what moved out of card 01; § g evidence; one phrase on card 05 |
| `reference/checks/cold-run.py` | rewritten as the recorder; same tools, same prompt, same configurations |
| `reference/checks/refusal-checks.py` | `--self-test` added; checks unchanged |
| `reference/checks/fixtures/` | new — broken cards and broken transcripts, each with its expected failure |
| `walks/` | new — the contract, the first question, its transcripts and verdicts, and `archive/q01-bar-v1/` with the runs scored under the first bar |
| `reference/worked-example/cold-run-transcript.md` | a note at the top: history, not scored evidence |
| `README.md` | an offline "check it yourself" section, links to this page and `EXPLAINED.md`, credits |
| `docs/index.html` | the self-test output in place of the unreproducible bad-card output, the offline scorer, credits; the sharing metadata and footer links now point to this repository and its page, with a separate link to the original repository |
| `LICENSE` | a second copyright line for the revision; the original line unchanged |
| `EXPLAINED.md`, `CHANGES.md` | new |

Nothing else in the instrument or the worked example was changed: `examples.md`, `state.md`, and
cards 01, 03, 06 and 07 are as Gabriel wrote them. Cards 02 and 04 keep every line he wrote; what
the revision added to them is marked as added, with the walk that found it.
