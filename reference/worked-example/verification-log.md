# Verification log

Every state verdict on this map, with the command that decided it and the output that came back. Run
from a clone of `NFTYoginis/your-market-realtor` at `702e79c`, 2026-08-18.

    $ git ls-remote origin refs/heads/main
    702e79cdeed5c4b4b262d5456586cbccee4b0d3f    refs/heads/main
    $ git rev-parse HEAD
    702e79cdeed5c4b4b262d5456586cbccee4b0d3f
    $ git status --porcelain          # (empty — clean tree)

    $ find . -path ./.git -prune -o -type f -print | wc -l
    62

Clone level with origin, so every local check below is a check against the shared truth. 62 files
enumerated, 7 carded at first and 12 once the revision added the engine's district — the file count
this map states anywhere else comes from that command.

---

## a) The repeating unit is well-formed — card 03, card 04

    $ for d in case-studies/*/region/; do echo "== $d"; ls "$d"; done
    == case-studies/jerusalem/region/        README.md contracts.md glossary.md market.md
                                             neighborhoods.md regulations.md services.md
    == case-studies/khao-lak/region/         (same seven)
    == case-studies/lisbon-portugal/region/  (same seven)
    == case-studies/novato/region/           (same seven)
    $ ls specialist/reference/region/
    contracts.md glossary.md market.md neighborhoods.md regulations.md services.md

Four instances, six slots each, plus a seventh file the blueprint does not have. **Six slots, not
five** — see the Does-not-hit line on card 04.

## b) The blueprint propagates by COPY — card 02

    $ grep -Fxf specialist/reference/region/glossary.md case-studies/khao-lak/region/glossary.md
    # Region — Glossary
    > **Owner:** The agent populating this folder.
    > **What this is:** Local-language and technical terms an agent uses, …
    ## Skip-if-not-needed
    If your market is English-monolingual and the specialist's plain-English vocabulary …
    …  (19 exact lines in total)

The populated file still carries the template's own instruction lines, so editing the blueprint
cannot reach it. Per-file counts, blueprint ∩ instance:

| file | jerusalem | khao-lak | lisbon | novato |
|---|---|---|---|---|
| contracts | 5 | 10 | 1 | 5 |
| glossary | 14 | 19 | **0** | 1 |
| market | 9 | 19 | 1 | 9 |
| neighborhoods | 8 | 10 | **0** | 6 |
| regulations | 7 | 11 | **0** | 7 |
| services | 11 | 12 | 13 | 13 |

    $ git log --format='%ad %h' --date=iso   # first commit adding each instance
    2026-05-08 07:05:07 +0700 e8378f4   (lisbon-portugal)
    2026-05-08 06:45:10 +0700 fa80d1e   (jerusalem, khao-lak, novato)

Lisbon is the newest and shares the least.

## c) The GHOST, confirmed on origin — card 06

    $ grep -n "4\. Add" CONTRIBUTING.md
    12:4. Add `case-studies/[your-market-slug]/README.md` with:
    $ find case-studies -name README.md
    case-studies/jerusalem/region/README.md
    case-studies/khao-lak/region/README.md
    case-studies/novato/region/README.md
    case-studies/lisbon-portugal/region/README.md
    $ git ls-tree -r --name-only origin/main | grep -E '^case-studies/[^/]+/README\.md$'
    (no output — exit 1)

The path has never existed on origin. Local absence would have been a question; this is a verdict.

## d) `[PLACEHOLDER]` is a live sentinel — card 05

    $ grep -n "PLACEHOLDER" case-studies/novato/region/services.md
    82:[PLACEHOLDER — populate; Bay Area outflow moves often go SF → Marin or Marin → Sonoma/…]
    85:[PLACEHOLDER]
    96:[PLACEHOLDER — relevant for 1031 exchanges, capital-gains exclusions, …]
    99:[PLACEHOLDER — populate if you handle owner-investors]
    120:- If the category is `[PLACEHOLDER]`, the specialist says so and offers to help populate it.

Branch points in the engine: `specialist/rules.md:59` · `welcome.md:40` · `identity.md:52` ·
`reference/region/services.md:60`.

    $ grep -rl "VERIFY" --exclude-dir=.git .      # 8 files, all under case-studies/
    $ grep -rn "VERIFY" specialist/               # (no output)

`[VERIFY]` has no branch. It is not a marker.

## e) Vendor honesty — clean, no defect

    $ for m in jerusalem khao-lak lisbon-portugal novato; do sed -n '3p' \
        case-studies/$m/region/services.md; grep -c '\[VERIFY\]' …; done
    jerusalem       "**Illustrative example entries.** Real Jerusalem agents should replace…"   8
    khao-lak        "**Illustrative example entries.** Real Khao Lak / Phang Nga agents…"      13
    lisbon-portugal "**Illustrative example entries.** Real Lisbon agents should replace…"     19
    novato          "**Illustrative example entries.** Real Marin agents should replace…"      13

## f) The surface, and its two hazards — card 07

    $ curl -o /dev/null -w '%{http_code}' https://nftyoginis.github.io/your-market-realtor/
    200
    $ curl -o /dev/null -w '%{http_code}' https://nftyoginis.github.io/your-market-realtor/docs/
    404

    $ for p in press-kit.md v1-to-v2-spec.md cold-test-brief.md media-outreach-kit.md \
               research-handoff-launch-layer.md og-image.png index.html; do … done
    press-kit.md 200 · v1-to-v2-spec.md 200 · cold-test-brief.md 200 · media-outreach-kit.md 200
    research-handoff-launch-layer.md 200 · og-image.png 200 · index.html 200

    $ curl -s https://nftyoginis.github.io/your-market-realtor/ | wc -c ; wc -c < docs/index.html
    39722 / 39722
    $ curl -s https://…/ | shasum ; shasum docs/index.html
    ef9643e0b039… / ef9643e0b039…

    $ curl -o /dev/null -w '%{http_code}' https://nftyoginis.github.io/…/README.md
    404

Served bytes equal disk bytes, so there is no drift **at this commit** — that is a reading of a
moment, which is why card 07 records the movement (disk → origin → served) rather than the reading.

---

## g) The engine's district — cards 1.2 to 1.6

Added in the revision, run against the same commit (`git rev-parse --short HEAD` → `702e79c`).

    $ grep -n "three jobs\|five jobs\|Listing, matching, or pricing" specialist/rules.md
    7:- **Confirm the job first.** Listing, matching, or pricing? State which one before starting.
    18:- **No work outside the three jobs.** Politely redirect.
    83:You support five jobs. That is the contract. Common drift requests to redirect:
    85:- "Draft an email to my seller" → redirect to one of the five jobs or the agent's CRM.
    $ sed -n '11p' docs/v1-to-v2-spec.md
    … v1 shipped May 2026 with three jobs (listing description, buyer-property fit ranking,
      pricing with comps). v2 (also May 2026) expands to five jobs …

The routing table (`rules.md:27-31`) has five rows. Lines 7 and 18 count v1's three: **LEFTOVER**,
replaced by the five-row table, never removed. Card 1.2.

    $ grep -n "welcome.md" specialist/rules.md specialist/identity.md
    specialist/rules.md:35:`welcome.md` controls first-turn behavior …
    specialist/identity.md:36:Open every new conversation with the welcome menu defined in `welcome.md` …

Two readers in the engine: **LIVE**. Card 1.3.

    $ sed -n '4p' specialist/reference/frameworks/international-buyers.md
    > **Called by:** `templates/listing.md` Variant C …; `frameworks/buyer-fit.md` …; `frameworks/pricing.md` …
    $ sed -n '15p' specialist/reference/frameworks/pricing.md
    If any are missing, stop and use `checklists/listing-intake.md` to gather them before pricing:
    $ grep -n "Services lookup →" specialist/rules.md
    45:- Services lookup → no template; produce a 3–6 line response per the rules in `region/services.md`

Frameworks, templates and checklists are each named by routing rows (`rules.md:27-30`): **LIVE**.
The three lines above are the surprising reaches on cards 1.4, 1.6 and 1.5.

## h) The engine reads `market.md` by section heading — card 02, found by an outsider's walk

    $ grep -rnE 'region/market.md.{0,40}("|section)' specialist/reference/
    frameworks/international-buyers.md:82: … `region/market.md`'s foreign-buyer activity section.
    frameworks/pricing.md:46: … live in `region/market.md` under "Pricing Adjustment Magnitudes" …
    templates/listing.md:11: … check `region/market.md` for a **"Buyer-disclosure conventions"** section …

    $ grep -n "^#" specialist/reference/region/market.md        # the blank has all three
    38:## Foreign buyer activity
    50:## Buyer-disclosure conventions
    64:## Pricing adjustment magnitudes

    $ grep -niE "^#+ .*(adjust|magnitud|foreign|disclosure)" case-studies/*/region/market.md
    jerusalem:   35 Foreign buyer activity · 43 Pricing adjustment magnitudes
    khao-lak:    43 Foreign buyer activity · 53 Buyer-disclosure conventions · 64 Pricing adjustment magnitudes
    lisbon:      19 Adjustment magnitudes for pricing memos · 37 Foreign-buyer activity
    novato:      32 Foreign buyer activity · 38 Pricing adjustment magnitudes

Three engine lines name a `market.md` section by heading. Lisbon's two are headed differently from
the blank's, and only Khao Lak carries the disclosure section, which the listing template reads only
"if present". Not found by the first Walk A; found when a walk on a question the mapmaker did not
write left the map to look for it.

## What was reported, not repaired

- `specialist/identity.md:52` says `reference/region/` holds **5 files**; six exist, and
  `README.md` / `CONTRIBUTING.md` / `docs/index.html` all say six. Card 04, Does-not-hit.
- `CONTRIBUTING.md:12` names a path that has never existed. Card 06 — deliberately left open; it is
  the clearest ghost on the map.
- `specialist/rules.md:7` and `:18` still count three jobs where the engine routes five. Card 1.2 —
  left open for the same reason.
