# Two walks

There are exactly two, they run in opposite directions, and **conflating them is the failure**. Say
which one you are on before the first command.

---

## Walk A — making the map

Seven steps, in order. Cards are step 7 and not before.

**1. Enumerate. Never guess a filename.**

    find . -path ./.git -prune -o -type f -print | xargs -I{} stat -f '%z %N' {}

Paths and sizes, all of them, before anything is opened. Guessed filenames are how a map acquires
entries for files that do not exist.

**2. Find the repeating unit.** Which shape occurs more than once? Same filenames under different
parents is the usual tell — visible in the enumeration, no file opened. No repeating unit means the
territory check in `identity.md` should have refused; go back and refuse.

**3. Classify by type.** Seven tests, first pass wins, from `card-types.md`. Nouns that fail all
seven go straight to `notes.md` — do not carry them forward hoping they turn into something.

**4. Mark state, with evidence.** `state.md`. Find the reader before you read the file. Every verdict
carries its command or `file:line` in the same line.

**5. Collision pass.** One word, two meanings, and you will not notice because both meanings are
obvious to you by now. `collisions.md`. **Before the cards** — a collision found afterwards rewrites
every card that used the word.

**6. Trace propagation: copy or reference.** For every blueprint-instance pair, run the grep. Copy
means your edit reaches nothing that exists; reference means it reaches everything. They look
identical from outside, and this is the step that decides half the Hits lines.

**7. Cards. Last.** Now the Hits lines are lookups (type table in `rules.md`), the state lines have
evidence, and the words mean one thing each. Writing cards before step 6 means writing them twice.
If one area has more cards than a row can carry, give it a district — a catalog one level down —
rather than an eighth row (`card-types.md` § The ceiling).

Then run [`checks/refusal-checks.py`](checks/refusal-checks.py) on every folder of cards and
[`checks/catalog-checks.py`](checks/catalog-checks.py) on the map. A map that fails its own checks
does not ship.

---

## Walk B — reading the map

Four steps. Most reads stop at two.

**1. Catalog.** One screen. Find the row your file lives under. If you are holding a file, the
*hand on a file* table sends you straight to its card.

**2. One card.** The one the catalog pointed at. Read *What it is*. If the row opened a district
instead, read that district's catalog — one more screen, same rule — and take the one card it
points at.

**3. Its Hits line — only if you are changing something.** If you are answering a question, you are
already done; the Hits line is about blast radius and costs you a paragraph you will not use.

**4. Stop.**

**Needing a second card means the first was mis-scoped.** That is a finding about the map, not a
reason to keep reading. Note it, answer from what you have, and fix the card's boundary later.

---

## Why they must stay apart

They differ in direction, in cost, and in what counts as done.

| | Walk A — making | Walk B — reading |
|---|---|---|
| Direction | whole territory → one card | one file → one card |
| Cost | every path enumerated, few opened | two files opened, both in the map |
| Done when | the checks pass | the question is answered |
| Failure | cards written before the collision pass | a survey where two hops would have done |

A reading step inside a map-making pass writes cards too early. A map-making step inside a read —
"let me just enumerate the folder first" — is how a two-hop answer becomes a tour. If you notice
yourself enumerating while answering a question, you switched walks; go back to the catalog.
