# 4-edit — the paper edit stage

The **edit cycle** for a paper that already exists. You have a draft in
`0-sections/` and you improve it across rounds. Not writing from scratch
(`haipipe-paper-edit-write`), not responding to reviewers (`haipipe-paper-edit-weaving`).

> **How to run it → [`USAGE.md`](USAGE.md)** (recipes, the reply grammar, the effort dial).

## Two ideas define this stage

**1. Comment-first.** A skill's first pass changes **no prose**. It inserts
concise inline findings — `%% {<actor>-<topic>-vMMDD}: finding | suggestion` — and
you reply on the same line — `========> {<actor> vMMDD}: accept|reject|modify|discuss`.
`<actor>` is any short id: a tool tag (`CC`=Claude Code, `GPT`, `GEM`), your
initials, or a reviewer (`R1`). Only a later apply round acts on the comments you
accepted. Full contract:
`_shared/comment-protocol.md`.

**2. Fan-out.** Because annotation is comment-only, it is safe to run wide and in
parallel. The `haipipe-paper-edit` **orchestrator** knows the whole catalog plus the
stage **agents/**, and fans out one annotator per section.

## One edit-cycle = five stages

```
(1) format-check → (2) annotate → (3) human-AI feedback → (4) improve → (5) clean + diff
    layout only       comments        ========> replies       apply         strip + handoff
    [sequential]      [FAN OUT]       [human + AI]            [sequential]  [sequential]
```

Stages 2–5 are collaborative and scale to the human effort you spend (light =
reply fast, trust the apply; heavy = discuss + hand contested sections to
`haipipe-paper-edit-weaving`). Full definition: `_shared/edit-cycle.md`.

## Shape of this stage

```
4-edit/
├── README.md                  ← you are here
├── haipipe-paper-edit/                ← ORCHESTRATOR: catalog + agents + the 5-stage cycle
│   └── SKILL.md
│
├── agents/                    ← stage agents (fan out the annotator)
│   ├── paper-edit-format-checker.md   (1) normalize layout
│   ├── paper-edit-annotator.md        (2) comment-only — spawn many in parallel
│   ├── paper-edit-improver.md         (4) apply accepted comments
│   └── paper-edit-cleaner.md          (5) strip to clean version
│
├── _shared/                   ← contracts every sub-skill + agent obeys
│   ├── comment-protocol.md        %% {CC-…} ========> {XX}: — the review contract
│   ├── sentence-format.md         stage-1 layout: banners + %% ---- Pn.Sm ----
│   ├── tex-file-anatomy.md        what one .tex should look like
│   ├── paragraph-indexing.md      the paragraph banner + stable-id standard
│   └── edit-cycle.md              the 5-stage cycle + the grid
│
├── haipipe-paper-edit-content/        ← ① CONTENT  (focus now — fully written)
├── haipipe-paper-edit-values/         ← ② numeric values        (stub)
├── haipipe-paper-edit-citation/       ← ③ citations             (stub)
├── haipipe-paper-edit-consistency/    ← ④ terms / labels / refs  (stub)
├── haipipe-paper-edit-format/         ← ⑤ venue format / style   (stub)
├── haipipe-paper-edit-typeset/        ← ⑥ widow / orphan / boxes (stub)
└── haipipe-paper-edit-diffpdf/            ← Stage-5 tracked-changes handoff (tool, not a topic)
```

Upstream input: the section→paragraph→sentence map comes from
`1-lifecycle/haipipe-paper-edit-diagram` (produced in planning, consumed here as a
diagnostic). ⑥ typeset compiles via `components/compile/paper-compile` to detect widows/overfull.

## The six update topics

| # | Sub-skill | Concern | Status |
|---|-----------|---------|--------|
| ① | `haipipe-paper-edit-content` | prose: structure, one-point paragraphs, claims, flow | **active** |
| ② | `haipipe-paper-edit-values` | every number matches its `0-displays/` source | stub |
| ③ | `haipipe-paper-edit-citation` | every `\cite` resolves, is real, supports its claim | stub |
| ④ | `haipipe-paper-edit-consistency` | terminology, `\label`/`\ref` integrity, notation | stub |
| ⑤ | `haipipe-paper-edit-format` | venue style, headings, units, abbreviations | stub |
| ⑥ | `haipipe-paper-edit-typeset` | widows, orphans, overfull boxes, breaks | stub |

Each sub-skill is **self-contained** (it carries its own check logic) and
**comment-first** (Round 1 only comments). They run **one topic at a time**
across rounds, in this order:

```
content edit  ──changes──►  numbers, citations, labels, line breaks
① content → ② values → ③ citations → ④ consistency → ⑤ format → ⑥ typeset
```

Review wide in parallel; apply sequentially; advance topics in dependency order.

## Relationship to neighbors

| Need | Go to |
|------|-------|
| No draft yet — produce new sections | `haipipe-paper-edit-write` (here, the cold-start) |
| Reviewer comments to address (rebuttal-driven revision) | `haipipe-paper-edit-weaving` (here) |
| A formal audit report (do not change prose) | `haipipe-paper-edit-claim-audit` / audit skills (here) |
| Iteratively improve an existing draft via comment → reply → apply | **here** (`haipipe-paper-edit`) |
