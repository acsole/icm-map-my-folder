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
*Added in the revision, after an outsider's walk found the gap:* the engine reaches inside
`market.md` by **section heading**, not only by filename — `frameworks/pricing.md:46` ("Pricing
Adjustment Magnitudes"), `frameworks/international-buyers.md:82` (foreign-buyer activity),
`templates/listing.md:11` ("Buyer-disclosure conventions", used only if present). Rename one here and
new copies stop matching the engine; rename it in the engine too and the existing markets stop
matching instead. Lisbon already differs: "Adjustment magnitudes for pricing memos",
"Foreign-buyer activity".

**Does not hit:** the instance you would assume was closest to it. Per-file `grep -Fxf` against the
blueprint: Khao Lak still shares 10–19 exact lines, Novato 1–13, Jerusalem 5–14 — but Lisbon, added
twenty minutes *after* the other three (`e8378f4`, 07:05, vs. `fa80d1e`, 06:45), shares **0** in
glossary, neighborhoods and regulations. The most fully-populated instance is the one that kept
none of the template. Newer does not mean closer to the blueprint; it usually means further.

**Done when:** you have run `grep -Fxf <blueprint-file> <instance-file>` for the pair you care about
and read the shared lines. If they are the template's own instructions, propagation already happened
and is finished — your edit reaches nobody. Stop there; do not open the instance to read its market
content. Renaming a heading in `market.md`: the three engine lines above are the ones to change with
it. Stop there.
