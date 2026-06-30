# 4-edit — how to use it

Concrete recipes for running the edit-cycle. Paths below use the real example
manuscript:

```
PAPER=examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025
SECS=$PAPER/0-sections
```

## TL;DR

```
1. Ask paper-edit to run a content review over the draft   → it fans out annotators
2. Open the .tex files; you now see  %% {CC-content-v0531}: … ========>  comments
3. Reply on each line:               ========> {JL v0531}: accept | reject | modify: …
4. Ask paper-edit to improve         → it applies only what you accepted
5. Ask paper-edit to clean           → annotations stripped, clean .tex remains
```

That is one edit-cycle. Repeat for the next topic (values, citations, …).

---

## A. Whole-draft cycle (the normal path)

You talk to Claude Code; it invokes the **`haipipe-paper-edit`** orchestrator, which runs
the five stages and fans out the annotator at stage 2. **It first asks for your
initials and the pass date** — your replies are tagged with those; nothing is
assumed.

**Kick off a content review across all sections:**

> Run a 4-edit **content** review over `0-sections/` of the npjDM paper. Format-check
> first, then fan out annotators — comment only, don't change any text.

What happens:
- Stage 1 — `paper-edit-format-checker` normalizes each leaf (banners + `Pn.Sm`).
- Stage 2 — one `paper-edit-annotator` per section runs **in parallel**, inserting
  `%% {CC-content-v0531}: finding | suggestion ========>` lines.
- You get a per-section digest of how many comments landed.

**Then you review (stage 3)** — open the files and append your verdicts:

```latex
%% ---- P3.S1 ----
Agreeableness showed the strongest positive correlation ($r = 0.62$).
%% {CC-content-v0531}: states correlation as if causal. | hedge to "associated with". ========> {JL v0531}: accept
%% {CC-values-v0531}: 0.62 here vs 0.747 in Table 2. | reconcile to source. ========> {JL v0531}: modify: use 0.747
```

**Then apply (stage 4):**

> Improve `02-05_trait-rating-correlation.tex` from my replies.

`paper-edit-improver` applies `accept`/`modify`, drops `reject`, leaves anything
you didn't answer. Run it section by section.

**Then clean (stage 5), when you're happy:**

> Clean `02-05…tex` at keep-index level.

`paper-edit-cleaner` strips the `%% {CC-…} ========>` threads, keeps the `Pn.Sm`
index and banners.

**Then build the handoff diff (end of stage 5):**

> Build the tracked-changes PDF of this cycle vs the last baseline.

`haipipe-paper-edit-diffpdf` (now inside `4-edit/`) produces a latexdiff-style PDF showing
exactly what this cycle changed — for co-author / advisor sign-off before the
next cycle.

---

## B. One section, one topic (manual / low-effort)

When you just want to work a single file:

> Use `haipipe-paper-edit-content` to review `0-sections/01_introduction.tex` — comment only.

This skips the orchestrator and runs one topic's checklist as a stage-2 pass on
one file. You then reply and ask for improve/clean as above.

---

## C. Run a single stage agent directly

Each stage is a callable agent in `agents/`. Useful for tight control:

| You want | Say |
|----------|-----|
| Just normalize layout | "Run `paper-edit-format-checker` on `02-05…tex`." |
| Just annotate one file/topic | "Run `paper-edit-annotator` on `02-05…tex`, topic=values, date=v0531." |
| Just apply my replies | "Run `paper-edit-improver` on `02-05…tex`." |
| Just strip annotations | "Run `paper-edit-cleaner` on `02-05…tex`, level=full." |

---

## D. Your part: the reply grammar (stage 3)

Append to the **same line**, after `========>`:

| Reply | Meaning | Stage 4 does |
|-------|---------|--------------|
| `========> {JL v0531}: accept` | take the suggestion as-is | applies it |
| `========> {JL v0531}: modify: <how>` | apply, but my way | applies your amendment |
| `========> {JL v0531}: reject` | no | drops the comment |
| `========> {JL v0531}: discuss: <question>` | talk first | leaves it; AI answers in a new line |
| *(no reply)* | undecided | **left untouched** — silence ≠ consent |

`{JL}` is the **actor id** — your initials here, but any short id works: a
coauthor (`RA`, `GG`), a numbered reviewer (`R1`), or another tool (`GPT`). The
annotating tool likewise stamps its own (`CC` = Claude Code). See
`_shared/comment-protocol.md` → *Actor ids*. `v0531` = pass tag (MMDD).

---

## E. The effort dial

Same five stages, scaled to how much you want to do:

- **Light** — let it fan out, skim, reply `accept`/`reject` fast, let improve apply
  everything. Minutes per section.
- **Medium** — reply with `modify:` notes; spot-check the apply.
- **Heavy** — open `discuss:` threads and run multiple dated rounds, dropping to
  sentence-level annotate → improve passes on contested sections.

---

## F. Order to run topics

Do **content** fully (cycle through stages 1–5) before the rest, then:

```
① content → ② values → ③ citations → ④ consistency → ⑤ format → ⑥ typeset
```

Applying a content edit moves numbers, citations, labels, and line breaks — so the
later topics are reviewed against settled prose, not text about to change. (Today
only `content` is fully written; the other five are stubs.)

---

## G. Safety rules (always true)

- **Stage 2 changes no prose** — if an annotation pass altered body text, it's a bug.
- **Fan out only stage 2** — format-check, improve, clean run one file at a time.
- **Nothing is applied without your reply** — `OPEN` comments are never acted on.
- **Stable `[id]` and `\label` keys never change**, in any stage.
- **Commit between stages** so each stage's diff is easy to inspect/revert.
