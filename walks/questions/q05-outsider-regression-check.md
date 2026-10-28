---
id: q05-outsider-regression-check
question: "Is docs/cold-test-brief.md (or anything else) a regression check I should rerun against the four case studies before changing the universal files in specialist/?"
author: outsider
configuration: catalog_in_context
catalog: reference/worked-example/CATALOG.md
expect_card: reference/worked-example/districts/public-edge/cards/7.3-the-working-documents.md
max_reads: 1
territory_reads_allowed: 0
must_mention: [["agent", "human", "manual", "by hand", "person"]]
runs_required: 5
spread_min: 4
bar_version: 1
---

**Where this question came from.** The third of the three an isolated session wrote after reading
only the territory's README — see `q03-outsider-template-wording.md`. Bar written before any run.

**What a right answer has to carry.** `docs/cold-test-brief.md` is a brief for practicing agents who
test the specialist by hand (the README lists it as "for practicing agents running validation") —
not a suite anything runs. The group checks the answer says a person runs it. Whether the map also
mentions the only test record in the repo (`case-studies/test-results.md`, a notes line, no card) is
not required.

**Why a budget of one.** The question names a file under `docs/`, and the top catalog's *hand on a
file* table sends any file under `docs/` other than the page straight to card 7.3.
