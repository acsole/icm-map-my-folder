---
id: q04-outsider-showing-notes-storage
question: "Where do captured showing notes actually live between chats so later matching and pricing jobs can cite them, given that Claude Projects don't save chat output to project knowledge?"
author: outsider
configuration: catalog_in_context
catalog: reference/worked-example/CATALOG.md
expect_card: reference/worked-example/districts/engine/cards/1.5-the-output-templates.md
max_reads: 2
territory_reads_allowed: 0
must_mention: [["conversation", "paste", "same chat", "context"]]
runs_required: 5
spread_min: 4
bar_version: 1
---

**Where this question came from.** The second of the three an isolated session wrote after reading
only the territory's README — see `q03-outsider-template-wording.md` for all three and how they were
produced. Walked now, with its bar written before any run, because `q03`'s latest map fix was shaped
by `q03`'s own walks; this question and `q05` were shaped by nothing.

**What a right answer has to carry.** Nowhere persistent: the engine only checks whether prior
showing notes "are present in the conversation context" (`specialist/rules.md`, *Cross-job memory*),
so a note reaches a later job only if it is still in the chat or the agent pastes it back. The group
accepts any of the ways to say that.

**Why a budget of two, and which card.** The question names no file; the top catalog's engine row
opens the district, and the district routes templates — where the showing-note template and its
durable-input role live — to card 1.5. Whether card 1.5 carries the answer is what the walk tests.
It does not say it today in those words; that is expected to show.
