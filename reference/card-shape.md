# Card shape

Eight lines. Same eight, same order, every card. A cold model that has read one card can read any
card without re-learning the format.

```markdown
# NN · Name

**Type + State:** TYPE · STATE — <the evidence that decided the state, in this line>
**What it is:** <one or two sentences. What a stranger would need to not misidentify it.>
**Why it is shaped that way:** <the constraint that produced this shape, not its history>
**Source path:** `path/in/the/territory`
**Hits:** <derived from type — look it up in rules.md, do not intuit>
**Does not hit:** <the noun a reader reaches for first and wrongly, with why it is wrong>
**Done when:** <a stop condition a cold model can act on>
```

## Line by line

**Name.** A noun phrase with a number. `03 · A Market`, not `Case Studies Overview`. The number is
the catalog's row.

**Type + State.** Both axes on one line, and the evidence in the same line. `state.md` governs what
counts as evidence. If the evidence does not fit on the line, the verdict is not settled yet.

**What it is.** Enough to prevent a misidentification. Not a summary of the contents — if a reader
needs the contents, they open the file, and the Source path is right there.

**Why it is shaped that way.** The constraint, not the chronology. *"One engine over N markets, so
the market-specific half has to be a folder it reads rather than code it contains"* — that stays true.
*"It was refactored in May"* — that is history, and it rots.

**Source path.** One path. It is what refusal-check A measures the card against, so a card whose
Source path is a 200-byte file has 199 bytes to work with — which is the correct outcome for a
200-byte file.

**Hits.** A lookup from the type table in `rules.md`. If you are reasoning about this line, you have
the type wrong.

**Does not hit.** The hardest line and the one that earns the card. The noun a reader reaches for
**first and wrongly**, and mildly surprising. *"Does not hit the tests"* when nobody would have
thought it did is filler. **If you cannot name a plausible wrong reach, do not write the card.**

**Done when.** A stop condition, phrased as an instruction. *"You can name the routing row that
consumes this slot, and you have not opened a case study"* — actionable, checkable, and it ends the
read. *"When you understand the architecture"* — unactionable; a cold model will keep going.

Two shapes of question a card must expect, both learned from walks *(added in the revision)*:

- **A card that quotes the territory.** A reader who sees `rules.md:18` quoted will open `rules.md`
  to check it, unless the stop condition says the quote is from the pinned commit and where its
  command is. Say so, and say not to re-open the file.
- **An audit — "what depends on this?"** A careful reader will not stop on a partial list; it will
  read the territory until it believes the list is complete. A card may answer an audit only if it
  carries the **complete** list, names the **command** that produced it and the **commit** it ran
  at, and its stop condition says to answer from the list. If the list is too long for a card, the
  card names the command and the count and the reader is told to run it — a map that pretends to be
  complete is worse than one that hands over the search.

## What a card is not

- Not longer than what it points at. Ever. (Refusal 1, check A.)
- Not a copy of the file's own words. (Check B: no verbatim run over 200 characters.)
- Not path-free. (Check C.)
- Not a narration of how anything works. That is a tour.

> If a card and the file disagree, **the file wins and the card is wrong.**
