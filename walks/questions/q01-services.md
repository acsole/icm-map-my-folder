---
id: q01-services
question: "What is Services?"
author: builder
configuration: catalog_in_context
catalog: reference/worked-example/CATALOG.md
expect_card: reference/worked-example/cards/04-the-six-slots.md
max_reads: 1
territory_reads_allowed: 0
must_mention: [["slot", "one of the six", "six standard files", "six files"], ["other people", "third-party", "third party", "vendor"]]
bar_version: 2
runs_required: 5
spread_min: 4
---

The question behind the gate run in `reference/worked-example/cold-run-transcript.md`, now with its
pass bar written down before any run is scored.

**Why these terms.** The first group checks that the reader knows what Services *is* here: one of
the six files every market carries, which the map calls a slot. The second group is the collision:
here "services" means other people's businesses, not the agent's own — an answer that misses it has
the word's industry meaning, which is the wrong one.

**Bar revised once, in the open (version 2, 2026-10-27).** Version 1 required the word *slot* in the
first group. Under it, five walks through Claude Code failed W6 four times while answering correctly
in plain words ("one of the six standard files"). Requiring the map's jargon tests repetition, not
understanding, so the group now accepts the plain-words form. Those five runs, the version-1 file
and their failing verdict are kept in [`../archive/q01-bar-v1/`](../archive/q01-bar-v1/README.md),
and were not re-scored: the runs scored under version 2 were recorded after the change.

**Why 4 of 5 on the spread gates.** The earlier n = 5 run came back 1 read four times and 2 reads
once (an instance opened to look at a filled example). Landing on card 04 and stopping happened every
time; those are the strict gates.
