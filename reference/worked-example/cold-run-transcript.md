# Cold-run gate — transcript

> **History, not scored evidence.** These runs were made before `cold-run.py` recorded raw JSON, so
> what survives is excerpts. The scored walks live in [`walks/`](../../walks/CONTEXT.md); this page
> stays because the first, failed run is why the door lines exist.

**Three transcripts, two configurations** — and the gate row repeated to **n = 5**, since a claim
measured once is an anecdote. One question against the shipped map, on `claude-opus-5`, in sessions
with **no** memory, no project instructions and no coaching: the system prompt names two
folders and offers a `list_dir` (free) and a `read_file` (metered). **A hop is a file opened.** That is why the gate row below reads *one*, not two: the reading walk's
"catalog, then one card" is two hops only when opening the catalog is one of them, and here the
catalog is already in the project, so it costs no open. Walk *steps* and metered *hops* are the same
number only in the unframed case — do not restate one as the other.

Runner: `reference/checks/cold-run.py`, and **the configuration is a flag on it** —

| Configuration | Command |
|---|---|
| catalog in the project — what the README tells a reader to load | `CATALOG_IN_CONTEXT=1 QUESTION="…" TERRITORY_DIR=… python3 reference/checks/cold-run.py` |
| no framing at all — the session must find the map itself | same line without `CATALOG_IN_CONTEXT` |

Both numbers below are real. They answer different questions, so every row names its flag.

> **What is Services?**

---

## Gate run — the configuration the README specifies

`README.md` tells a reader of an existing map to load its `CATALOG.md` and nothing else. So: the
catalog is in the project, everything else is behind the read tool.

**Result: PASS — one file opened, then stop.** Run repeatedly rather than once: **n = 5 on the
shipped command** (4 independent, research-claude; 1 builder reproduction) — **4 × 1 read / 0
territory files**, and **1 × 2 reads / 1 territory file**
(`case-studies/lisbon-portugal/region/services.md`, an instance opened to look at a filled example).
**All five landed on card 04 and all five stopped**, which is what the claim is: not a fixed
file-count, but the card it reaches and the fact that it ends. A single run that comes back 2/1 is
inside the spread, not a contradiction.

```
turn 0  stop_reason=tool_use  in=1842 out=278
  → read_file({"path": "reference/worked-example/cards/04-the-six-slots.md", "root": "map"})
  → list_dir({"path": ".", "root": "repo"})
turn 1  stop_reason=end_turn  in=3073 out=428
```

**The answer, verbatim:**

> **Services = `services.md`, one of the six slots inside a market.**

> It is the agent's **vetted list of other people's businesses** — inspectors, lenders, stagers,
> movers. Deliberately *not* the agent's own service offerings, which is what "services" means
> everywhere else in real estate. That inversion is the thing to remember; it's a known
> collision word in this repo.

> Mechanically:

> - It sits alongside the other five slots (`market.md`, `neighborhoods.md`, `regulations.md`,
> `contracts.md`, `glossary.md`) in the blueprint at `specialist/reference/region/` and in all
> four market instances under `case-studies/<slug>/region/`.
> - The engine addresses it by filename, via its own routing row in `specialist/rules.md` — the
> job is called "services lookup."
> - It's the newest slot: `specialist/README.md:26` calls it "new in v2."

> One wrinkle worth knowing if you touch this area: `specialist/identity.md:52` still says
> `reference/region/` holds **5 files**. Six exist. `services.md` arrived in v2, the routing
> table gained its row, and that counting sentence never got updated (`README.md`,
> `CONTRIBUTING.md`, and `docs/index.html` all correctly say six). Reported in the map, not
> repaired.

It named the collision (vendors, not the agent's own services), the routing row, the newest-slot
fact and the 5-vs-6 defect — all from one card — and stopped. It did not open a single file in the
territory.

---

## Harsher run — the map folder and the repo, with no framing at all

Same question, but nothing is loaded: the session sees two folder names and has to find its own way
in. This is stricter than the README's configuration, and it is the run that found a defect.

**Before the fix: 4 hops, and the catalog was never opened.**

```
turn 0  stop_reason=tool_use
  → list_dir({"path": ".", "root": "map"})
  → list_dir({"path": ".", "root": "repo"})
turn 1  stop_reason=tool_use
  → read_file({"path": "identity.md", "root": "map"})
  → read_file({"path": "rules.md", "root": "map"})
turn 2  stop_reason=tool_use
  → list_dir({"path": ".", "recursive": true, "root": "repo"})
turn 3  stop_reason=tool_use
  → read_file({"path": "specialist/reference/region/services.md", "root": "repo"})
  → read_file({"path": "specialist/README.md", "root": "repo"})
turn 4  stop_reason=end_turn
```

It read `identity.md` and `rules.md` — the *making* instrument — and then did what those files
describe: enumerated the territory and started mapping it, opening
`specialist/reference/region/services.md` and `specialist/README.md` directly. The answer was good
and it cost four reads plus a recursive walk of the repo, and it ended with *"I have not run
`grep -Fxf` …"* — a reader re-deriving a map that was sitting three directories away, unfound.

**The defect:** nothing in the folder told a cold reader which walk it was on. `identity.md` and
`rules.md` are the front of the tree and they are addressed to a map-*maker*.

**The fix:** a one-line door at the top of `README.md`, `identity.md` and `rules.md` — *reading a
map, not making one? go to the catalog, open one card, stop.* Nothing else changed in those files.

**After the fix: 4 hops, and it answered out of the map.**

```
turn 0  stop_reason=tool_use
  → list_dir({"path": ".", "root": "map"})
  → list_dir({"path": ".", "root": "repo"})
turn 1  stop_reason=tool_use
  → read_file({"path": "identity.md", "root": "map"})
  → read_file({"path": "rules.md", "root": "map"})
turn 2  stop_reason=tool_use
  → list_dir({"path": ".", "recursive": true, "root": "repo"})
turn 3  stop_reason=tool_use
  → list_dir({"path": "reference", "recursive": true, "root": "map"})
turn 4  stop_reason=tool_use
  → read_file({"path": "reference/worked-example/CATALOG.md", "root": "map"})
turn 5  stop_reason=tool_use
  → read_file({"path": "reference/worked-example/cards/04-the-six-slots.md", "root": "map"})
turn 6  stop_reason=end_turn
```

Still two reads spent on orientation — the price of a session with no framing whatsoever — but it
reached `CATALOG.md`, took exactly one card, opened **no** file in the territory, and said so
itself: *"That was one catalog plus one card — the budget for an answer."*

---

## What the transcripts together establish

| Run | `CATALOG_IN_CONTEXT` | Reads | Territory files opened | Landed on card 04 | Stopped |
|---|---|---|---|---|---|
| Gate run (catalog loaded), n=5 | `1` | 1 ×4, 2 ×1 | 0 ×4, 1 ×1 | yes, 5/5 | yes, 5/5 |
| No framing, before the fix | unset | 4 | 2 | no — never found the catalog | yes |
| No framing, after the fix | unset | 4 | 0 | yes | yes |

The gate is the first row. The other two are why the door exists.

## A second catalog defect this gate caught

The gate run initially took **two** files, not one: the catalog's routing row said *"→ 4 — and check
the collisions"*, and its collision section listed the five colliding words, one of which was
*services*. A reader who sees their own noun teased in a second file will open it. Both were catalog
bugs of the same kind — **a catalog that carries content instead of routing** — and both are fixed:
the row now says `4`, and the collision section says outright that it is not a stop on the read
path.
