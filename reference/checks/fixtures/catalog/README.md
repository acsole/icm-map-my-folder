# Catalog-check fixtures

Small maps built to fail. `catalog-checks.py --self-test` passes only if each map trips exactly the
gate its folder prefix names.

| Map | Must trip | How it is broken |
|---|---|---|
| `ok-control` | nothing | a top catalog, one card, one district with one card |
| `e-orphan-card` | E | a card no catalog row reaches |
| `e-card-reached-twice` | E | the district also links the top catalog's card |
| `e-dead-row` | E | a row links a card that was never written |
| `f-eight-rows` | F | eight rows in one catalog |
| `f-nested-district` | F | a district opens another district |
| `f-carries-a-count` | F | the catalog states how many cards the map holds |

*Added by Andrés Curcio in the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission. See [`CHANGES.md`](../../../../CHANGES.md).*
