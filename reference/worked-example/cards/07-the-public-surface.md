# 07 · The Public Surface

**Type + State:** SURFACE · LIVE — `curl -o /dev/null -w '%{http_code}'
https://nftyoginis.github.io/your-market-realtor/` → **200**, and what it serves is byte-identical to
`docs/index.html` on disk (both 40,323 B, sha1 `404a502fcd3…`) with the clone level with origin at
`236aae0` (`git ls-remote`). *(Re-verified when the map was re-pinned; at `702e79c` the same check
read 39,722 B, sha1 `ef9643e0b039…`.)*

**What it is:** the folder GitHub Pages publishes. **`docs/` on disk is the site *root* on the web** —
the folder name appears in no URL: `/your-market-realtor/` → 200, `/your-market-realtor/docs/` → 404.

**Why it is shaped that way:** Pages will serve a `docs/` folder off the default branch, so the repo
carries its own website with no second repo and no build step — at the price of a folder whose name
means one thing on disk and another on the web.

**Source path:** `docs/`

**Hits:** anyone who never opened the repo — and **the whole folder, not just `index.html`**. Every
working document in there answers 200: `press-kit.md`, `media-outreach-kit.md`,
`research-handoff-launch-layer.md`, `v1-to-v2-spec.md`, `cold-test-brief.md`. Anything dropped into
`docs/` is published. The movement is disk → origin → served: a file becomes public when it is pushed
*and* the site rebuilds, so a clone behind origin shows bytes the web is not serving and a clone
ahead shows bytes it is not serving yet. Settle it with `git ls-remote` plus a `curl` of the URL —
never with `git status`, which compares against a cached ref.

**Does not hit:** the repo root. `README.md` and `CONTRIBUTING.md` — the two files a visitor actually
reads on GitHub, and the ones a reader assumes *are* the site — both return **404** on the Pages URL.
The public site and the public repo are two surfaces with different contents and different readers.

**Done when:** you have a status code for the URL and a byte comparison against disk. Presence in
`docs/` is not evidence that a file is served; absence from the site is not evidence that it is
private. Stop there.
