# 4-edit / shared — the edit cycle (5 stages)

One edit-cycle takes a draft through five stages. Stages 2–5 are **collaborative**:
AI and human share the work, and you choose how much human effort to spend at
each. The `paper-edit` orchestrator drives the cycle and fans out the per-stage
agents in `../agents/`.

## The five stages

```
(1) FORMAT-CHECK   normalize the file: paragraph banners + one-sentence-per-line
    │              with %% ---- Pn.Sm ---- separators   (agent: paper-edit-format-checker)
    │              → same words, new layout. No wording change.
    ▼
(2) ANNOTATE       AI inserts findings as comments, NO text change
    │              %% {CC-<topic>-vMMDD}: finding | suggestion ========>
    │              fan-out: many annotators, one per (section[,topic])  (agent: paper-edit-annotator)
    ▼
(3) FEEDBACK       human + AI converse on each comment, in place
    │              human appends ========> {XX vMMDD}: accept|reject|modify|discuss
    │              AI may answer a `discuss:` or refine a suggestion
    ▼
(4) IMPROVE        apply accepted comments, one section at a time   (agent: paper-edit-improver)
    │              accept/modify → edit; reject → drop; OPEN/discuss → leave
    ▼
(5) CLEAN          strip annotations to the clean version   (agent: paper-edit-cleaner)
                   human-gated; levels: keep-comments / keep-index / full clean
```

### Mapping to the comment protocol

Stages 2–4 are the comment protocol's rounds (`comment-protocol.md`): stage 2 =
Round 1 (comment-only), stage 3 = Round 1.5 (reply), stage 4 = Round 2 (apply).
Stage 1 is a pre-round normalization; stage 5 is the post-apply teardown.

## Effort dial (how much human to spend)

The same five stages scale from light to heavy:

| Effort | Stage 3 (feedback) | Stage 4 (improve) |
|--------|--------------------|-------------------|
| **Light** | skim; reply `accept` to most, `reject` a few | AI applies all accepted |
| **Medium** | reply per comment with `modify:` notes | AI applies; human spot-checks |
| **Heavy** | discuss threads; multiple `vMMDD` rounds | drop to sentence-level annotate→improve passes on contested sections |

Low-effort still runs all five stages — the human just replies faster and trusts
the AI apply more.

## Fan-out is stage 2 only

Stage 2 (annotate) is read + comment with no shared writes, so it is
embarrassingly parallel: dispatch **one annotator per section** (each owns its
file), or **read-only annotators + a single writer** when many topics hit the
same files. Stage 1 (format-check), stage 4 (improve), and stage 5 (clean) all
mutate files and run **sequentially, one section at a time**.

## The TODO grid

Rows = leaf `.tex` files. Columns = the six topics. Track each cell's furthest
stage reached.

```
section \ topic          ① content   ② values   ③ cites   ④ consist  ⑤ format  ⑥ typeset
00_abstract              s1          s0          s0        s0         s0        s0
01_introduction          s2          s0          s0        s0         s0        s0
02-05_trait-rating-corr  s4          s0          s0        s0         s0        s0

legend: s0 untouched · s1 formatted · s2 annotated · s3 replied · s4 improved · s5 cleaned
```

Track it in a scratch table or the harness task list. **Current focus:** column ①
content. Other columns stay `s0` until content reaches `s4`/`s5` for a section.

## Topic order is a dependency, not a preference

```
① content → ② values → ③ citations → ④ consistency → ⑤ format → ⑥ typeset
```

You may annotate (stage 2) many topics and sections at once, but topics
**advance through improve (stage 4) in this order across cycles**: applying a
content edit moves numbers, citations, labels, and breaks, so improving those
before content is settled just redoes the work.

## Stop conditions

- Content `s5` for every section → content cycle complete; start topic ②, or run a
  fresh content cycle if new issues surfaced.
- A comment keeps re-opening across cycles → the issue is structural (wrong
  section job or paragraph split); fix at section level before continuing.
