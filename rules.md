# Rules

> **Which walk are you on?** These are the checks for **making** a map. If you are **reading** one,
> the only rule you need is in [`reference/walks.md`](reference/walks.md) § Walk B: catalog, one
> card, stop — start at
> [`reference/worked-example/CATALOG.md`](reference/worked-example/CATALOG.md).

Checks, not advice. Each one either passes or the card does not get written.

## Before anything: the territory check

- [ ] You were given a **path**, not a description. `ls` it. If it does not resolve, stop and ask for
      the path. Never map a folder from a description of it.
- [ ] The folder is empty, or holds fewer than three files → **stop**. Say: *"Three files is a
      listing, not a territory. `ls` is cheaper than I am."*
- [ ] The folder fails the territory class in `identity.md` → **refuse in the words given there** and
      stop. Do not downgrade a refusal into a partial map.

## The noun test — does this thing get a card at all?

A noun is mappable only if all three hold:

- [ ] **It has a path.** You can type it. Not "the validation logic" — `lib/validate.py`.
- [ ] **It has a boundary.** You can say what is inside it and what is next to it.
- [ ] **Someone can change it.** There is an edit that would alter it.

A noun that passes all three is then tested against the seven types in
[`reference/card-types.md`](reference/card-types.md).

- [ ] **It fails all seven types → it gets NO card.** One line in `notes.md`, naming the path and why
      it failed. This is not a shortfall in the map; it is the map doing its job.
- [ ] **It passes a type but its catalog is full → it gets NO card**, unless its area already
      holds enough real nouns to open a district (`reference/card-types.md` § The ceiling). Otherwise
      name it in the Does-not-hit line of the nearest card and record it in `notes.md` under *held
      at the ceiling*.
- [ ] **Every catalog, top or district, passes its own check.** Seven rows at most, one card per
      row, every card reached by exactly one row, no counts in a catalog —
      [`reference/checks/catalog-checks.py`](reference/checks/catalog-checks.py).

## The movement test — is this a movement or a wish?

Before writing any sentence that says something *happens*:

- [ ] **Start state** — named.
- [ ] **End state** — named.
- [ ] **Actor** — who or what performs it.

Missing any one of the three and it is a wish, not a movement. Cut it.

*"Regions get populated"* — no actor, no start state. Wish.
*"An unfilled slot (`[PLACEHOLDER]`) becomes a filled one when the agent who owns the folder edits it
by hand"* — three of three. Movement.

## Hits is derived from type. Never intuited.

Look the line up. Do not reason about it per card.

| Type | Hits | Reaches |
|---|---|---|
| **ENGINE** | every instance that reads it | immediately, in place |
| **BLUEPRINT** | **future copies only** | never backwards |
| ↳ *blueprint that is also a read-path* | + whatever reads it, now | derive each half from its own role |
| **INSTANCE** | nothing — it is a leaf | — |
| **SLOT** | every instance, present and future | wherever the machinery names it |
| **MARKER** | whatever branches on it | at read time |
| **INSTRUCTION** | the human who reads it | once, at their next action |
| **SURFACE** | people who never opened the folder | after publish |

- [ ] **Blueprint hits future instances only** — and before you write that line, **verify copy vs.
      reference**. From outside they look identical.

      grep -Fxf <blueprint-file> <instance-file>

      Shared exact lines that include the blueprint's own instruction text = **copy**. Propagation
      already happened and is finished; your edit reaches nothing that exists. An instance that
      shares nothing has drifted off the blueprint entirely — say so, with the count.

## Does-not-hit is the hardest line. It is also the one that earns the card.

- [ ] It names **a noun the reader reaches for first and wrongly** — not a list of unrelated things.
- [ ] It is **mildly surprising**. If it reads as obvious, you named the wrong noun.
- [ ] **If you cannot name a plausible wrong reach, leave the card unwritten.** A card whose
      Does-not-hit line is filler is a card that has not been thought about.

## Every card ships with three lines or it does not ship

- [ ] **Hits** — from the table above.
- [ ] **Does not hit** — per the checks above.
- [ ] **Done when** — a stop condition phrased as an instruction a cold model can act on. Not
      *"once you understand X"*; something it can check and then stop.

Their presence is check **D** in [`reference/checks/refusal-checks.py`](reference/checks/refusal-checks.py) —
mechanical, so a card cannot ship one line short by accident.

## Every state verdict ships with the evidence that decided it

- [ ] The command, path, or line number that decided LIVE / LEFTOVER / GHOST is in the same line as
      the verdict. No verdict travels alone. Full axis: [`reference/state.md`](reference/state.md).

## Refusal 1 — no photocopy

Three checks, all runnable, all in
[`reference/checks/refusal-checks.py`](reference/checks/refusal-checks.py):

- [ ] **A. Every card is smaller than what it cites.** Card bytes < bytes of its Source path (a file's
      size; a folder's total).
- [ ] **B. No run of more than 200 consecutive characters appears verbatim in both a card and a file
      it cites.**
- [ ] **C. Every card cites at least one path that resolves in the territory.**

And the line that governs both artifacts:

> **If a card and the file disagree, the file wins and the card is wrong.**

- [ ] **Pre-ship count sweep.** Grep every surface — cards, catalog, notes, README, landing page,
      scripts, their docstrings — for counts, and check each one **twice**: against every other
      statement of it, *and against its own definition*. A count is allowed to appear once, where it
      is derived; everywhere else, name the thing instead of the number.

      grep -rnoiE "\b(one|two|three|[0-9]{1,3}) (runs?|cards?|files?|hops?|reads?|types?|steps?)\b" .

      This build produced **six** defects of that class and every one read as helpful in isolation:
      a summary restating a card's own count, a heading left over from an earlier count, a page
      quoting a number in a different unit than the log defined, a term used in the sentence after
      the one defining it. **The sweep is cheap and the habit is not reliable — run the grep.**

Say it on the map, not just here. A map that is trusted over its territory has stopped being a map.

## Refusal 2 — no slurping

Both directions.

**Reading a map:**

- [ ] Answering a question costs **the catalog plus one card**. That is the budget.
- [ ] **Needing a second card means the first was mis-scoped.** Fix the card; do not read on. Record
      it — two cards for one question is the strongest signal a map gives you about itself.
- [ ] Read a card's Hits line only if you are changing something. If you are only answering, stop at
      *What it is*.

**Making a map:**

- [ ] **Enumerate paths and sizes before opening anything.**

      find . -path ./.git -prune -o -type f -print | xargs -I{} stat -f '%z %N' {}

- [ ] **Open a file only when a state verdict or a Hits line depends on its contents.** Type, path,
      boundary, and most notes lines are decidable from the enumeration.
- [ ] If you have opened a file and it changed no line of the map, that read was the map's cost and
      nobody's benefit. Note it and stop reaching.

## Walk order

- [ ] You are running **one** of the two walks in [`reference/walks.md`](reference/walks.md), and you
      can say which. Conflating them is the failure mode: a map-making step inside a read turns a
      two-hop answer into a survey; a reading step inside a map-making pass writes cards before the
      collision pass and they all have to be rewritten.
