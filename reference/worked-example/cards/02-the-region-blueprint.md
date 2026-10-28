# 02 · The Region Blueprint

**Type + State:** BLUEPRINT · LIVE — instances contain its text, they do not reference it:
`grep -Fxf specialist/reference/region/glossary.md case-studies/khao-lak/region/glossary.md` returns
19 exact lines, among them the template's own instruction to whoever is filling it in
(`> **Owner:** The agent populating this folder.`) and its `## Skip-if-not-needed` heading. A
reference would have carried a path; a copy carries the instructions. LIVE because the engine's
routing table resolves `region/*.md` here — this folder is the template *and* the read-path.

**What it is:** six files of prompts and empty tables, one per slot, that an agent overwrites with
their own market. Its double duty is the point: template for the next market, live data for the
current one.

**Why it is shaped that way:** populating a market means overwriting this folder in place, so a
finished market cannot stay here — which is why the four completed ones are parked outside the read
path, in `case-studies/`, where the engine never looks.

**Source path:** `specialist/reference/region/`

**Hits:** two things, because the folder has two roles — and only the first is the blueprint's.
As a **blueprint**: future copies only; no case study on disk changes, ever. As the **engine's
read-path**: the running specialist, immediately — `specialist/rules.md:27-33` routes `region/*.md`
here and `:59` branches on what it finds, so an edit changes what a specialist answers for any
market not yet populated over it. Derive each half from the role it belongs to; do not average them.
*Added in the revision, after an outsider's walks found it:* the engine also leans on **sections
inside** two of these files. The complete list at `236aae0` (identical at `702e79c`) is the output of
`reference/checks/heading-refs.py`, classified in `verification-log.md` § h:
**quoted verbatim, breaks if the heading is reworded** — `frameworks/pricing.md:46` ("Pricing
Adjustment Magnitudes"), `templates/listing.md:11` ("Buyer-disclosure conventions", used only if
present). **Named by topic, breaks if the section goes** — in `market.md`: seasonality
(`pricing.md:3`, `:80`; `pricing-memo.md:45`), foreign-buyer activity (`international-buyers.md:3`,
`:13`, `:82`; `pricing.md:82`), adjustment magnitudes (`pricing.md:3`, `:7`; `pricing-memo.md:39`);
in `regulations.md`: ownership (`pricing.md:65`, `listing.md:103`, `pricing-memo.md:52`) and
foreign-buyer rules (`international-buyers.md:3`, `:59`). Rename a heading here and new copies stop
matching the engine; rename it in the engine too and existing markets stop matching instead — the
packs users keep on every upgrade (`README.md:272`, card 7.2). Lisbon
already differs: two headings reworded, and no seasonality or disclosure section at all.

**Does not hit:** the instance you would assume was closest to it. Per-file `grep -Fxf` against the
blueprint: Khao Lak still shares 10–19 exact lines, Novato 1–13, Jerusalem 5–14 — but Lisbon, added
twenty minutes *after* the other three (`e8378f4`, 07:05, vs. `fa80d1e`, 06:45), shares **0** in
glossary, neighborhoods and regulations. The most fully-populated instance is the one that kept
none of the template. Newer does not mean closer to the blueprint; it usually means further.

**Done when:** you have run `grep -Fxf <blueprint-file> <instance-file>` for the pair you care about
and read the shared lines. If they are the template's own instructions, propagation already happened
and is finished — your edit reaches nobody. Stop there; do not open the instance to read its market
content. Asked what depends on a section's wording: the list above is complete for every heading of
these files at the pinned commit — answer from it; do not re-audit the engine by reading it. Stop
there. To re-check after the territory moves, run the command, not a read.
