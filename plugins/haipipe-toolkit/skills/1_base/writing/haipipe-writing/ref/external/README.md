# External writing skills · what we call, what we only read

Two treatments, decided 2026-09-22. A skill we **call** is vendored as an adapted copy
into a numbered folder beside `haipipe-writing/` and named in
[`../writing-methods.yaml`](../writing-methods.yaml). A skill we only **read** stays
in `references/` (its upstream checkout) and is digested here; whatever rule of
it we wanted is already inside `../anti-slop-rules.json` or `../ai-tells.md`; each
digest below says what was taken and what was left on purpose. Nothing in this folder is a runtime import, and
no `SKILL.md` lives here, so the installers never see it.

## The map

| Treatment | Skill | Upstream | Commit | Licence | Where it lives now |
|---|---|---|---|---|---|
| call · style | `writing-dna-skill` | larashero3-dotcom/writing-dna-skill | `ee3d97ee` | MIT | `../../../1_style/writing-dna-skill/` |
| call · evaluator | `academic-humanizer` | AIScientists-Dev/academic-humanizer 0.3.2 | `02281d83` | MIT | `../../../2_evaluate/academic-humanizer/` |
| call · evaluator | `humanizer` (blader) | blader/humanizer 3.0.0 | `9862685f` | MIT | `../../../2_evaluate/humanizer/` |
| read · taken | `humanize` (soundshuman) | aashaexo/soundshuman | `a45cfbba` | MIT | rules + scanner design → `../anti-slop-rules.json`, `../../cli/anti_slop.py` |
| read · taken | `humanizer` (Adam) | Aboudjem/humanizer-skill | `a58df065` | MIT | fact comparison → `../../cli/anti_slop.py`; guardrail lists → `../ai-tells.md` §3 |
| read · taken | `stop-slop` | hardikpandya/stop-slop | `8da1f030` | MIT | structural vocabulary → `../anti-slop-rules.json` |
| read | `no-ai-slop` | petergyang/no-ai-slop | `000650b1` | MIT | digest below |
| read | `slopbeth` | ehmo/slopkit | `b33718bb` | MIT | digest below |
| read · taken | `deslop` | stephenturner/skills | `48287d80` | MIT | "do not dilute", "match register" → `../ai-tells.md` §3 and §4 |
| read | `unslop` | cursor/plugins (pstack) | `27e2a62f` | MIT | digest below |
| read | `anti-slop` | elithrar/dotfiles | `c821fc7f` | MIT | digest below |
| read | `anti-ai-slop-writing` | jalaalrd/anti-ai-slop-writing | `63255f9b` | unknown | digest below; licence unknown, so nothing is copied from it |
| read · taken | `stop-slop-zh` | VincentOld/stop-slop-zh | `42305b6f` | MIT | rules 1, 2, 3, 6 → `lang: zh` entries in `../anti-slop-rules.json` |
| read · off-register | `sepia` | sepia (fiction + professional prose) | `4c8d782f` | MIT | fiction architecture; not our register |
| not writing | `stop-that-shit` | lennney/stop-that-shit | `6a7c0de6` | MIT | an agent scope guard, shelved with writing by mistake; nothing to take |

`references/anti-ai-writing-skills.md` keeps the original ten-item shelf as the
provenance record; this file is the working view from inside the writing skill.
Nine of these submodules are marked `update = none` in `.gitmodules` on purpose:
they are read when someone digests them, not fetched on every clone.

## What each read-only source is, and what is worth taking

### soundshuman `humanize` · taken
Thirty-four patterns in five families (content, language, style, communication,
filler and hedging), a voice-calibration step, and a rule-driven scanner with
`rules/slop-rules.json`. That JSON, which itself records adaptations from blader,
stop-slop and brandonwise, is the base of `../anti-slop-rules.json`, and the
pattern-density score is the design of `../../cli/anti_slop.py`. Nothing left to take.

### humanizer (Adam) · taken
Fifty-five patterns in six families, five voice profiles, a 0 to 100 AI-tell score,
and two guardrail lists: what NOT to flag (false positives) and signs of human
writing to preserve. The deterministic, preservation-sensitive fact comparison is
already ported into `anti_slop.py`. Taken 2026-09-22: both guardrail lists, adapted
into `../ai-tells.md` §3. Its five voice profiles and 0 to 100 score are not used; the
shared rubric has its own axes.

### stop-slop · taken
Sixty-eight lines: core rules, quick checks, a scoring rubric, examples. Its
structural anti-pattern vocabulary is in `../anti-slop-rules.json`. Its scoring
rubric is not used; `../evaluation-rubric.md` has its own four axes.

### no-ai-slop · read
Two explicit jobs, edit and detect-without-rewriting, which is the same split as
our writer and evaluator roles. Keeps the writer's personal voice and pushes
prose toward direct and opinionated. Adds a words-to-cut and patterns-to-cut list.
Worth taking: nothing structural; the cut lists overlap the rules JSON.

### slopbeth (slopkit) · read
A workflow with reference routing and script routing, hard rules on preserving
meaning, voice and density, and a benchmark harness (most of its 222 files).
Worth taking if we ever want scores: the benchmark shape. Not needed for rules.

### deslop (stephenturner) · taken
Ten core rules; the two we did not state anywhere were "match register to context"
and "do not dilute" (an anti-slop pass must not flatten specifics or soften claims).
Taken 2026-09-22 into `../ai-tells.md` §3 and §4; `../plain-rules.md` stays JL's own
rulings and was not touched.

### unslop (cursor pstack) · read
A compact taxonomy: content, language, style, communication artifacts, filler,
jargon, plain speech, under a "must always apply" rule. Same families as
soundshuman; nothing new to take.

### anti-slop (elithrar) · read
Fourteen lines: an editorial pass that preserves voice and does not trigger on
ordinary drafting. Its one contribution is the trigger discipline, which
`haipipe-writing` already has (no method is selected by default).

### anti-ai-slop-writing (jalaalrd) · read only
A before-writing checklist, structural and punctuation rules, formatting rules,
voice calibration and a self-check. The repository states no licence, so nothing
is copied; it is read for comparison only.

### stop-slop-zh · taken, the Chinese register
Eight rewrite rules for Chinese AI prose (虚词与程度副词, 排比三件套, 名词化,
金句收尾, 抽象主语, 元评论与八股连接词, 具体化, 八股结构), a five-dimension
rubric and a delivery checklist. Taken 2026-09-22: rules 1, 2, 3 and 6 are the
`lang: zh` phrase and regex entries in `../anti-slop-rules.json` (38 phrases, 4
patterns), matched by substring because a word boundary means nothing between
Chinese characters. Rules 4, 5, 7 and 8 (金句收尾, 抽象主语, 具体化, 八股结构) are
judgment rules with no fixed surface form and stay as reading; the sentence
statistics in `../../cli/anti_slop.py` remain English-tuned.

### sepia · off-register
Repairs narrative architecture in fiction (StoryScope, arXiv:2604.03136) and
routes professional prose separately, across three skills (sepia, sepia-review,
sepia-recreate). Fiction is not a register this family writes; kept for reference.
