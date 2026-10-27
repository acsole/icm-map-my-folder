# The seven card types

Closed set. Seven, and no eighth. Each one carries its own proof test — a thing you can check, not a
feeling about the file. Run the tests in order; first pass wins.

| # | Type | Proof test |
|---|---|---|
| 1 | **ENGINE** | Two or more instances read it. Change it and all of their behavior changes. |
| 2 | **BLUEPRINT** | Instances **contain** its text rather than reference it. A change reaches future copies only. |
| 3 | **INSTANCE** | It has a name an outsider recognizes — a market, a client, a product. |
| 4 | **SLOT** | A named field inside an instance, doing the same job in every instance. |
| 5 | **MARKER** | A value the machinery branches on. Signal, not content. |
| 6 | **INSTRUCTION** | It directs a human. Delete it and no run changes. |
| 7 | **SURFACE** | Someone who never opened the folder can encounter it. |

## Running the tests

**ENGINE — count the readers.** Two is the floor. One reader is not an engine, it is a file that
thing uses. The test is not "does it look central"; it is "name the second instance."

**BLUEPRINT — grep for its own text inside an instance.**

    grep -Fxf <blueprint-file> <instance-file>

If the shared exact lines include the blueprint's *own instruction lines* — the ones addressed to
whoever is filling it in — the instance is a **copy** and your edit will not reach it. A reference
would carry a path, not the instructions. **This is the check people skip**, because copy and
reference look identical from outside the file.

**INSTANCE — say the name to someone outside the project.** If they recognize it (a city, a client,
a SKU) it is an instance. If the name only means something inside the folder, it is probably a slot
or a leftover.

**SLOT — check it appears in every instance doing the same job.** Same name, same role. A field that
exists in one instance is that instance's business, not a slot. A file that exists in every instance
but has no counterpart in the blueprint and no reader in the machinery is also not a slot — say so.

**MARKER — find the branch.** Name the file and line where the machinery reads the value and does
something different because of it. **No branch, no marker.** A bracketed token that only a human
reads is content wearing a marker's clothes — that is the most common false positive in the set.

**INSTRUCTION — delete it in your head.** If no run changes, it is an instruction. This is the only
type defined by what happens when it is absent.

**SURFACE — reach it from outside.** A status code, a URL, a shared link. "It's in a public repo" is
not the test; the test is that someone who never opened the folder can encounter it.

## The refusal

**A noun that fails all seven gets no card.** It gets one line in `notes.md` — path, and which test
it failed last. That line is the point. Seven types applied to forty nouns should produce a handful
of cards and a page of one-liners; if everything got a card, the tests were not run.

## The ceiling

**Seven rows per catalog.** Not seven types each with a card — seven rows on one screen, and a small
territory may deserve three. A noun that passes a type after the catalog is full does not force an
eighth row: it goes in the nearest card's Does-not-hit line, where it is more useful anyway, and gets
a notes line saying it was held at the ceiling.

**A row may open a district.** When one area of the territory has more real nouns than one row can
carry, that row points to a **district**: a catalog one level down, under the same rule — seven rows
at most, routing only, one card per row. The top catalog still fits on one screen, and so does every
district. Open one only when the nouns are there and each has passed its type test; a district built
to hold a bigger number is a fake city with a second floor.

The reading cost is one more file when a reader browses by concept (catalog, district, card), and
none when they arrive holding a file: the top catalog's *hand on a file* table routes straight to
the card. Districts are one level deep; a district never opens another.

Three real cards beat a fake city.

## Type is not state

These seven answer *what kind of thing is this*. Whether it is still alive is a **separate axis** —
see [`state.md`](state.md). A BLUEPRINT can be a GHOST. An INSTRUCTION can be LIVE and point at a
GHOST. Never fold the two together; the moment you do, "important-looking" starts deciding both.
