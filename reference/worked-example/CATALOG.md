# Catalog — `NFTYoginis/your-market-realtor`

**Territory:** https://github.com/NFTYoginis/your-market-realtor · mapped at commit `702e79c`
(`git ls-remote origin refs/heads/main`, 2026-08-18).
**Class:** a blueprint copied into named instances, shared machinery reading them, a public edge.

**Read the row, then one card. Stop.** If you need a second card, the first was mis-scoped — say so
rather than reading on.

| # | Card | Source path | Type | State |
|---|---|---|---|---|
| 1 | [The Engine and its Jobs](districts/engine/CATALOG.md) — a district | `specialist/` | ENGINE and its parts | LIVE |
| 2 | [The Region Blueprint](cards/02-the-region-blueprint.md) | `specialist/reference/region/` | BLUEPRINT | LIVE |
| 3 | [A Market](cards/03-a-market.md) | `case-studies/<slug>/region/` | INSTANCE | LIVE ×4 |
| 4 | [The Six Slots](cards/04-the-six-slots.md) | the six filenames inside any `region/` | SLOT | LIVE |
| 5 | [The Marker Set](cards/05-the-marker-set.md) | `[PLACEHOLDER]`, `[N/A — …]` | MARKER | LIVE |
| 6 | [The Contributor Path](cards/06-the-contributor-path.md) | `CONTRIBUTING.md` | INSTRUCTION | LIVE → aims at a GHOST |
| 7 | [The Public Surface](cards/07-the-public-surface.md) | `docs/` | SURFACE | LIVE |

## If your hand is already on a file

| You are holding | Go to |
|---|---|
| `contracts.md` · `glossary.md` · `market.md` · `neighborhoods.md` · `regulations.md` · `services.md` | **4** |
| `specialist/rules.md` | [**1.2**](districts/engine/cards/1.2-the-job-set.md) |
| `specialist/welcome.md` | [**1.3**](districts/engine/cards/1.3-the-first-turn.md) |
| `specialist/reference/frameworks/` | [**1.4**](districts/engine/cards/1.4-the-frameworks.md) |
| `specialist/reference/templates/` | [**1.5**](districts/engine/cards/1.5-the-output-templates.md) |
| `specialist/reference/checklists/` | [**1.6**](districts/engine/cards/1.6-the-intake-checklists.md) |
| anything else under `specialist/` that is not `reference/region/` | [**1.1**](cards/01-the-engine.md) |
| `specialist/reference/region/` | **2** |
| anything under `case-studies/` | **3** |
| a bracketed value — `[PLACEHOLDER]`, `[N/A]`, `[VERIFY]` | **5** |
| `CONTRIBUTING.md` · `README.md` | **6** |
| `docs/` · a live URL · anything you are about to publish | **7** |
| a file in none of these rows | [`notes.md`](notes.md) — it may already be there, with the reason it got no card |

## Collisions

Some words in this repo carry two meanings each. **This is not a stop on the read path** — every
card states the sense it needs, so answering a question never requires the list. Open
[`../collisions.md`](../collisions.md) only when you are about to *write* one of those words for
someone else to read.

## What this map does not carry

This catalog is full, and the engine's row opens a district rather than an eighth row. Nouns that
got no card — with the test each one failed — are one line each in [`notes.md`](notes.md). Evidence
for every state verdict is in [`verification-log.md`](verification-log.md), commands and output.

> If a card and the file disagree, **the file wins and the card is wrong.**
