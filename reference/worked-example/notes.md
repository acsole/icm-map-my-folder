# Notes — nouns that got no card

The map is 14 cards over 62 files (`find . -path ./.git -prune -o -type f -print | wc -l`, the same
at `702e79c` and `236aae0`) — Gabriel's seven, five more in the engine's district and two in the
public edge's, with cards 01 and 07 each reached from their district. This page is the rest, one line
each, and it is not an appendix: a map that cards everything has classified nothing.

## Failed all seven type tests

Classified from the enumeration — path and size — without opening them. That is the method working,
not a corner cut.

- `LICENSE` (1,085 B) — MIT text. No reader in the folder, no instance, no branch, no direction to
  anybody. Fails all seven.
- `.gitignore` (177 B) — tooling for git, not a noun in the territory.
- `WRITEUP.md` (1,314 B, added in commit `702e79c`) — a note *about* the repo, addressed to
  no run and read by no machinery. If `docs/index.html` ever links it, it becomes a question for
  card 07, not a card of its own.
- `case-studies/test-results.md` (16,745 B) — a record of a past test run. Not an instance (no market
  name an outsider would recognize), not a slot (no counterpart in any `region/`), and nothing
  branches on it. **The largest un-carded file in the territory, and it was classified without
  being opened** — nothing in the map depends on its contents. *(Revision:)* the classification
  stands — it still fails all seven types — but "nothing depends on its contents" did not survive a
  walk. The outsider's `q05` asks whether any regression check exists, and every run opened this
  file to answer: it is the only record of a test in the repo — six tests, Jerusalem and Novato,
  listing, matching and pricing only (`grep -n "^## Test" case-studies/test-results.md`), a written
  record, not something to rerun. A question can depend on a file that no card should carry; this line now says so.

## Inside another card's boundary — no card of their own

- `specialist/identity.md`, `examples.md`, `README.md` — card 01, now row 1.1 of the engine's
  district. `identity.md` lists the job set too (`:13-24`); that list is named on card 1.2 rather
  than carded twice. Whether a run reads `examples.md` depends on how the folder is loaded into a
  Project, not on any routing row: **UNVERIFIED**, settled by a walk that asks about an example.
- *Moved out of this section in the revision:* `specialist/reference/frameworks/`, `checklists/`,
  `templates/`, `welcome.md` and the job set in `rules.md` were classified as inside card 01. A
  question about any one of them needed card 01 plus the territory — the map's own sign of a
  mis-scoped card — so the engine's row became a district and each got its own card (1.2–1.6).
- `docs/og-image.png` — card 07, which is where the fact that it is *served* lives. The five `.md`
  files under `docs/` were here too; the revision gave them card 7.3, because one of them is served
  while no file in the repo names it.
- `case-studies/<slug>/region/README.md` (4 files) — named inside card 03 as the seventh file that is
  not a slot.

## Held at the ceiling

Passed a type test, got no card, because its catalog is full and the ceiling is a real one.

- **`[VERIFY]`** — 78 occurrences across 8 files, all under `case-studies/`. Passes the INSTRUCTION
  test (it directs a human to check a vendor contact; delete it and no run changes) and fails the
  MARKER test (nothing in `specialist/` branches on it). It is named in card 05's Does-not-hit line,
  which is more useful than an eighth card would have been.

## Checked and clean — nothing to report

- **Vendor honesty across all four instances.** Every `services.md` labels its entries as
  illustrative at line 3 ("**Illustrative example entries.** Real … agents should replace with their
  actual vendor list"), and contacts read `[VERIFY]` per entry — 8 in Jerusalem, 13 in Khao Lak, 19
  in Lisbon, 13 in Novato. No invented vendor is presented as real. No card, no defect, and it is
  recorded here so the next reader does not re-check it.
