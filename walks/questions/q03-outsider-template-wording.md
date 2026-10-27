---
id: q03-outsider-template-wording
question: "If I rename or restructure a section in a region/ template file, what in rules.md or the framework files depends on that exact wording, and would it break users' existing region packs, which the upgrade path tells them to keep?"
author: outsider
configuration: catalog_in_context
catalog: reference/worked-example/CATALOG.md
expect_card: reference/worked-example/cards/02-the-region-blueprint.md
max_reads: 1
territory_reads_allowed: 0
must_mention: [["copy", "copies", "copied"], ["filename", "file name", "by name", "placeholder"]]
runs_required: 5
spread_min: 4
bar_version: 1
---

**Where this question came from.** Not from whoever made the map. A fresh Claude Code session —
isolated as `cold-run-claude-code.py` isolates a walk, given only the territory's public `README.md`
and no map — was asked for three questions a new maintainer would ask before changing something.
It wrote:

1. *If I rename or restructure a section in a `region/` template file, what in `rules.md` or the
   framework files depends on that exact wording, and would it break users' existing region packs,
   which the upgrade path tells them to keep?*
2. *Where do captured showing notes actually live between chats so later matching and pricing jobs
   can cite them, given that Claude Projects don't save chat output to project knowledge?*
3. *Is `docs/cold-test-brief.md` (or anything else) a regression check I should rerun against the
   four case studies before changing the universal files in `specialist/`?*

**Why this one.** The first, by order, chosen before any walk — so the choice could not favour the
question the map answers best. The other two are kept here; the second asks something no card
answers yet, and is the next question to walk.

**What a right answer has to carry.** Existing region packs are copies, so editing the blank changes
none of them (card 02); and the engine finds region files by their filenames and branches on the
`[PLACEHOLDER]` marker, not on a section's wording (cards 04 and 05). The groups ask for the first
and for either form of the second. Written before any run is scored.

**Correction, kept in the open.** The paragraph above was wrong in part, and the walks are what
showed it. The engine does not only find region files by filename: three engine lines name sections
*inside* `market.md` by heading, so a renamed section can stop matching. Under the first map, all five
walks went into the territory to find that out — eleven to fourteen files each — because no card
carried it. That was a gap in the map, not in the bar, so the **map** was fixed (card 02, *Hits*) and
the bar was left exactly as written. The five runs against the old card are kept in
[`../archive/q03-map-before-heading-fix/`](../archive/q03-map-before-heading-fix/README.md).

**Why a budget of one.** The question names a `region/` template file, and the top catalog's *hand
on a file* table sends `specialist/reference/region/` straight to card 02.
