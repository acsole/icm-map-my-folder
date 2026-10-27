# q01 under its first bar — failed, kept on purpose

Five walks through Claude Code (`claude-code-headless`), recorded 2026-10-27 against the first pass
bar of `q01-services`. Verdict: `fail: W6 failed on 4 of 5 runs` — see [`verdict.check.md`](verdict.check.md).

**What failed was the bar, not the reader.** All five runs opened card 04 and nothing else, stayed
out of the territory, stopped on their own, and answered correctly: Services is the agent's list of
other people's businesses, not the agent's own services — the collision the card exists for. The
first must-mention group asked for the word *slot*. That is the map's own vocabulary; four of the
five answers said the same thing in plain words ("one of the six standard files every market has").
The bar was testing whether the reader repeated the map's jargon, not whether it understood.

**What was done about it.** The bar was revised in
[`../../questions/q01-services.md`](../../questions/q01-services.md) to accept the plain-words form,
with the reason written there. These five runs were **not** re-scored under the new bar — passing
them now would be scoring the very answers that prompted the change. They stay here, unscored by the
current verdicts, and five new runs were recorded against the revised bar.

[`question.md`](question.md) is the question file as it stood when these runs were scored.

*Revision by Andrés Curcio (original Map My Folder by Gabriel Azoulay), with the original author's
permission.*
