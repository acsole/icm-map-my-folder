# Refusal-check fixtures

A map and a territory built to fail. `refusal-checks.py --self-test` runs the checks against
`map/` and `territory/` and passes only if each card trips **exactly** the gate its filename names.

| Card | Must trip | How it is broken |
|---|---|---|
| `ok-control.md` | nothing | a sound card — proves the checks do not fail everything |
| `a-larger-than-source.md` | A | cites `small.txt`, and is bigger than it |
| `b-photocopy.md` | B | carries a run of more than 200 characters copied from `big.md` |
| `c-dead-path.md` | C | its only cited path has never existed |
| `d-missing-line.md` | D | ships without a **Done when** line |

The filename prefix is the expectation: `ok-` means no gate, a letter means that gate alone. Add a
fixture by adding a card whose prefix names the gate it should trip.

Nothing here is a real territory. Do not add this folder to a Claude Project.

*Added by Andrés Curcio in the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission. See [`CHANGES.md`](../../../../CHANGES.md).*
