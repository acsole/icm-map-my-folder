# q02 against card 1.2 before its stop condition was tightened — failed, kept on purpose

Five walks through Claude Code, 2026-10-27. Verdict: `fail: W4 passed on 0 of 5 runs, needs 4` —
see [`verdict.check.md`](verdict.check.md).

Every run reached card 1.2 straight from the top catalog's *hand on a file* table, answered yes, and
named both leftover sentences (`rules.md:7` and `:18`). Then every run opened `specialist/rules.md`
in the territory to re-read the lines the card had just quoted. The card's *Done when* said not to
open a framework or a template, and said nothing about the file it quotes — so the reader verified.

**What was done.** The stop condition on card 1.2 now says the line numbers are quoted from the
pinned commit, with the command in `verification-log.md` § g, and not to re-open `rules.md`. The
bar of `q02-showing-notes` was not touched. Five new runs were recorded against the fixed card.

*Revision by Andrés Curcio (original Map My Folder by Gabriel Azoulay), with the original author's
permission.*
