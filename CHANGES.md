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
| 4. Gates shown failing | **Done.** Both checkers ship broken fixtures and a `--self-test` | [`reference/checks/fixtures/`](reference/checks/fixtures/) |
| 2. Bigger shelf | **Not yet.** Designed, not built — see *Next* below | — |
| 3. Business territory | **Not yet.** Designed, not built | — |
| Real walk recordings | **Not yet.** The recorder exists; recording costs API calls and has not been run. Until it is, the walk verdict reads `fail: 0 of 5 runs recorded` | [`walks/verdicts/`](walks/verdicts/) |

The last row is deliberate. The scorer could have been fed the old runs, but those survive only as
excerpts in [`cold-run-transcript.md`](reference/worked-example/cold-run-transcript.md), not as the
raw record. Rebuilding them by hand would be inventing evidence. An unrecorded walk is not a passing
one, so the verdict says so.

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
   agent is paid for. No card covers it, because no card covers the jobs — which is the judges'
   second note, seen from inside the territory.

## Next — designed, not built

- **A bigger map without breaking "one screen".** Change "seven cards per map" to "seven rows per
  catalog", and let a catalog row point to a sub-catalog. The catalog still fits on one screen; the
  shelf grows. The first new district is the engine and its jobs — where finding 2 lives. Three new
  gates: every card reached by exactly one row, no catalog over seven rows, and a staleness check
  against the territory's current commit.
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
| `reference/checks/score-walk.py` | new — the offline scorer |
| `reference/checks/cold-run.py` | rewritten as the recorder; same tools, same prompt, same configurations |
| `reference/checks/refusal-checks.py` | `--self-test` added; checks unchanged |
| `reference/checks/fixtures/` | new — broken cards and broken transcripts, each with its expected failure |
| `walks/` | new — the contract, the first question, and the verdicts it produces |
| `reference/worked-example/cold-run-transcript.md` | a note at the top: history, not scored evidence |
| `README.md` | an offline "check it yourself" section, links to this page and `EXPLAINED.md`, credits |
| `docs/index.html` | the self-test output in place of the unreproducible bad-card output, the offline scorer, credits; the sharing metadata and footer links now point to this repository and its page, with a separate link to the original repository |
| `LICENSE` | a second copyright line for the revision; the original line unchanged |
| `EXPLAINED.md`, `CHANGES.md` | new |

Nothing in `identity.md`, `rules.md`, `examples.md`, the other `reference/*.md` files, or the cards,
catalog, notes and verification log of the worked example was changed.
