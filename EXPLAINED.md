# Map My Folder, explained from zero

The rest of this repo is written for someone who already knows what it is for. This page is for
someone who does not. It starts with the problem, then the example, and only then the names. If you
already know the method, [`README.md`](README.md) is the faster door.

---

## 1. The problem, with no technology in it

You inherit an old house and want to replace one socket in the kitchen. Before you cut a wire, you
need to know what else goes dark when you do.

You have two ways to find out:

- **Follow every wire through the walls.** Hours of work, and you can still get it wrong.
- **Look at the fuse box,** where someone wrote *"switch 3: kitchen and fridge"*. Ten seconds.

**Map My Folder makes that labelled fuse box — for a folder of files.**

## 2. Why that matters when the reader is an AI

Every new conversation with a model like Claude is a new electrician who has never seen the house and
remembers nothing from yesterday. It cannot ask "which of these files matter?" before it starts.

If it has to follow every wire each time, it is slow, expensive, and wrong more often, because
reading everything crowds out the reasoning. With a labelled fuse box it reads one label and stops.

## 3. One real example

The worked example in this repo maps
[`your-market-realtor`](https://github.com/NFTYoginis/your-market-realtor), an assistant for real-estate
agents. Inside it there is:

- a **blank form** of six files that describes a city — prices, neighborhoods, regulations…
- **four cities** already filled in from that form — Jerusalem, Khao Lak, Lisbon, Novato.

Someone asks: *"If I fix the blank form, do the four cities get fixed too?"*

Intuition says yes. The answer is **no**. The cities are **photocopies that were already filled in**:
fixing the original changes no copy that already exists. You cannot see that by looking — from
outside, a copy and a link look the same. It takes one command (`grep -Fxf`), which finds the blank
form's own instructions still sitting inside the filled cities.

That answer is one card on the map:
[`02-the-region-blueprint.md`](reference/worked-example/cards/02-the-region-blueprint.md). The next
model reads that card and answers correctly without opening any of the territory's files.

## 4. What the project physically is

Three things:

1. **The instructions** — [`identity.md`](identity.md), [`rules.md`](rules.md) and the files in
   [`reference/`](reference/). They teach a model how to make a fuse box for *your* folder.
2. **One fuse box already made** — the map of `your-market-realtor`, in
   [`reference/worked-example/`](reference/worked-example/): one index, a handful of cards.
3. **Scripts that check the fuse box is honest** — in [`reference/checks/`](reference/checks/). For
   example: every label must be shorter than what it describes, or it is not a label, it is a copy.

## 5. Where ICM is in all this

ICM (Interpretable Context Methodology, Van Clief & McDermott, arXiv:2603.16021) says: **arrange the
folders so that a model reads the least it can and the right path is the obvious one.** It is built
from three pieces, and all three are here:

| ICM piece | In the house | In this repo |
|---|---|---|
| An index at the door that only says "go there" | the fuse box | [`CATALOG.md`](reference/worked-example/CATALOG.md) |
| A shelf of files that all have the same shape | the labels | [`cards/`](reference/worked-example/cards/), each with the same eight lines |
| Steps in order, each ending at a check | how the fuse box gets made without mistakes | *Walk A* in [`walks.md`](reference/walks.md), and the scripts that refuse a bad card |

## 6. The words the rest of the repo uses

Now the names, each on top of an idea you already have.

| Word | What it means here |
|---|---|
| **Territory** | the folder being mapped — the house |
| **Map** | the index plus the cards — the fuse box |
| **Card** | one label: what a thing is, what a change to it reaches, and what it does *not* reach |
| **Does not hit** | the wire you would cut by mistake. The most useful line on a card |
| **Type** | what kind of thing it is — the blank form is a BLUEPRINT, a city is an INSTANCE, and so on |
| **State** | whether anything still uses it: LIVE, LEFTOVER (replaced and never removed), GHOST (named but missing) |
| **Walk A / Walk B** | making a map / reading one. Kept apart, because mixing them is how a two-step read becomes a tour |
| **Gate** | a check a script runs. A card that fails one does not ship |
| **Cold run** | asking a model with no memory one question, and recording what it opened |

## 7. What this revision added, in one paragraph

The judges of the competition this was built for said two things: the one check that tests a real
reader needed an API key, so nobody else could run it; and nothing showed that the checks can fail.
This revision splits that check in two — one part records a walk once, the other scores it for free
and offline — and ships broken examples that every check must reject. The full account, decision by
decision, is in [`CHANGES.md`](CHANGES.md).

---

*Map My Folder was built by Gabriel Azoulay (Gabe — Your AI Specialist,
[@NFTYoginis](https://github.com/NFTYoginis)). This page and the revision it describes are by Andrés
Curcio, working from the competition's feedback with the original author's permission.*
