# 04 · The Six Slots

**Type + State:** SLOT · LIVE — the same six filenames appear in the blueprint and in all four
instances (`ls specialist/reference/region/ case-studies/*/region/`), and the engine addresses them
by name: five have a row in the routing table in `specialist/rules.md`, `glossary.md` is routed by
condition instead of by job (consulted whenever a term falls outside working English).

**What it is:** six named fields inside a market, one job each, the same job in every market.

| Slot | Its job |
|---|---|
| `market.md` | local conditions — buyer segments, price bands, working languages |
| `neighborhoods.md` | the areas, and who each one suits |
| `regulations.md` | what the law and the tax code do to a transaction here |
| `contracts.md` | how a deal is papered here |
| `glossary.md` | local-language terms → plain English |
| `services.md` | **the agent's vetted list of other people's businesses** — inspectors, lenders, stagers, movers. Not the agent's own services, which is what "services" means everywhere else in real estate. Routed as its own job ("services lookup"), and it is the newest slot: `specialist/README.md:26` calls it "new in v2" |

Each instance also carries a seventh file, `region/README.md`. It is not a slot — no blueprint
counterpart, no reader in the machinery.

**Why it is shaped that way:** the routing table addresses slots by filename, so populating a market
is filling names rather than inventing structure — and a new slot is not a new file, it is a new
routing row. *(Revision:)* filename is how a slot is **found**, not all the engine relies on — it
also names sections inside `market.md` and `regulations.md`. Editing a slot's sections in the blank
is card 02, which carries the complete list.

**Source path:** `specialist/reference/region/`

**Hits:** every instance, present and future. A slot's job is fixed by the engine, not by the market.

**Does not hit:** the engine's own count of itself. `specialist/identity.md:52` says
`reference/region/` holds **5 files**. Six exist. `services.md` arrived in v2, the routing table
gained its row, and the sentence that counts the files did not — while `README.md`, `CONTRIBUTING.md`
and `docs/index.html` all say six. Adding a slot hits the routing table and misses the prose that
counts them. *(Reported, not repaired — a map does not edit its territory.)*

**Done when:** you can name the slot and the routing row that consumes it. If the file you want is
not one of the six, you are adding a slot, which is an engine change — card 01. Stop there.
