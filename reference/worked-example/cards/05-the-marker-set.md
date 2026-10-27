# 05 · The Marker Set

**Type + State:** MARKER · LIVE — the machinery branches on `[PLACEHOLDER]` in four places:
`specialist/rules.md:59` (§ Empty-region handling — list the files, tell the user, refuse substantive
output without explicit acknowledgment), `specialist/welcome.md:40` (it *overrides* the first-turn
menu), `specialist/identity.md:52`, and `specialist/reference/region/services.md:60` (never recommend
from an unfilled category). It is still unresolved in shipped instances —
`case-studies/novato/region/services.md` lines 82, 85, 96, 99.

**What it is:** the small set of bracketed values the machinery reads as signal rather than content.
Two members, and they are not equally exercised:

- **`[PLACEHOLDER]`** — an unfilled slot. Four branch points; fires before anything else can.
- **`[N/A — English-monolingual market]`** — declared at `specialist/reference/region/glossary.md:8`
  as the value that makes the specialist skip a file. A live branch, **never exercised**: no instance
  uses it as a file value (Khao Lak's occurrence is the copied template line; Novato's `N/A` at
  `neighborhoods.md:11` is prose).

**Why it is shaped that way:** population is incremental and there is no build step, so the engine
needs to tell an empty slot from a filled one at read time. Brackets are the schema.

**Source path:** `specialist/rules.md`

**Hits:** whatever branches on the value, at read time — here, the first turn and every substantive
job.

**Does not hit:** `[VERIFY]`. It is the most visible bracketed token in the territory — 78
occurrences across 8 files — and nothing in `specialist/` reads it; every occurrence sits under
`case-studies/`, marking vendor contacts in illustrative entries. It directs a human, so it fails the
marker test, and with its catalog full it gets no card of its own (see `notes.md`). Visibility is
not a branch.

**Done when:** you can name the file and line that branches on the value. A bracketed token nothing
branches on is content wearing a marker's clothes. Stop there.
