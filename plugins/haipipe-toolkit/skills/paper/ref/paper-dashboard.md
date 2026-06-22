# Paper Dashboard

This defines the behavior of `/haipipe-paper` with no arguments inside a paper
and the panel rendered by the Paper Console.

The dashboard is a derive-from-disk preflight. It orients the session before the
Console or any lifecycle stage acts.

## Golden Rule

```text
Never report a stage as done because STATUS.md says so.
A stage is done only when its expected artifact resolves on disk with real
content (not the scaffold stub).
When stored status and disk disagree, disk wins and the gap is flagged DRIFT.
```

## Lifecycle Frontier

The dashboard uses the paper lifecycle spine:

```text
0-seed -> 1-pitch -> 2-claims -> 3-narrative -> 4-figures-tables -> 5-minimap
-> write/edit -> review
```

The frontier is the first stage whose disk predicate fails.

| Stage | Done when | Next action if frontier |
|---|---|---|
| `0-seed` | `0-lifecycle/0-seed/0-seed.tex` has question / evidence / kill content | `/haipipe-paper seed` |
| `1-pitch` | `0-lifecycle/1-pitch/1-pitch.tex` has a one-line pitch | `/haipipe-paper pitch` |
| `2-claims` | `0-lifecycle/2-claims/2-claims.tex` ledger non-empty, each row has a status (anchor `planned` still counts as a status; unmaterialized evidence is an open need, not a stage fail) | `/haipipe-paper claims` |
| `3-narrative` | `0-lifecycle/3-narrative/3-narrative.tex` has an arc | `/haipipe-paper narrative` |
| `4-figures-tables` | `4-figures-tables.tex` maps claim -> display and display units exist | `/haipipe-paper figures` |
| `5-minimap` | `5-minimap.tex` maps paragraph jobs + evidence anchors | `/haipipe-paper minimap` |
| `write/edit` | `0-sections/*.tex` exist and `0-*.tex` compiles to PDF | `/haipipe-paper write` |
| `review` | audits pass and venue checks pass | `/haipipe-paper review` |

Glyphs:

```text
OK       done on disk
ACTIVE   current frontier
TODO     not reached
DRIFT    STATUS.md claims progress but the disk predicate fails
BLOCKED  explicit blocker (open need / failed gate)
```

## Shallow Check

For each paper:

```text
1. Read STATUS.md (current_layer, maturity, active_round) as a hint only.
2. For each stage, test its disk predicate above.
3. Set current_layer to the first failing stage (the frontier).
4. If STATUS.md current_layer is ahead of the disk frontier, flag DRIFT.
5. Surface open needs from 2-claims GAP rows, 4-figures-tables missing units,
   5-minimap empty slots, section TODOs, and 1-rounds/<round>/todo.md.
```

## Render Skeleton

Lead with a paper header, then a one-line Story, then the progress spine. This is
the panel a session sees on enter. Keep it tight; open needs follow below it.

```text
📄 <paper-folder-name>  ·  <venue>

  Story: <one plain sentence: the angle + the surprising mechanism + scope/caveat,
         compressed from 1-pitch.tex (fallback 3-narrative). Append "(关联,非因果)"
         when 2-claims marks the claim observational.>

  进度  seed ─ pitch ─ claims ─ narrative ─ figures ─ minimap ─ write ─ review
         <g>    <g>     <g>      <g>         <g>       <g>       <g>      <g>
                                            ▶️ 这里(<one-clause why this is the frontier>)
```

Per-stage glyph (derive-from-disk; show each stage's TRUE state, not a blanket
todo downstream):

```text
✅ done       the stage predicate passes AND the artifacts it references resolve
(草稿)         the artifact exists but is rough / incomplete (e.g. sections drafted but thin)
⬜ todo       absent, empty, or its referenced anchors do not resolve
▶️ frontier   the FIRST stage that is not ✅; overlay it and annotate "← 这里"
⚠️ drift      STATUS.md claims this stage done but the disk predicate fails
```

Worked example (MedJournal, derived from disk on 2026-06-22):

```text
📄 Paper-Personality-Opioid-MedJournal  ·  medical journal (IMRAD)

  Story: 患者感知的医生"可亲和性"(LLM 从评论里测)越高 → 腰背痛阿片处方强度越高,
         主要走"已开药者剂量"而非开药人数,双重资格人群更明显。(关联,非因果)

  进度  seed ─ pitch ─ claims ─ narrative ─ figures ─ minimap ─ write ─ review
         ✅     ✅      ✅       ✅         ▶️        ⬜        (草稿)   ⬜
                                          ← 这里(0-displays 只有 display00,01-04 没建)
```

Frontier = figures: `4-figures-tables.tex` names Display 01-04 but `0-displays/`
has only display00. minimap shows ⬜ because its paragraph anchors point at those
unbuilt displays; write shows (草稿) because `0-sections/*.tex` have rough prose.
The Story line is the compressed 1-pitch one-liner; if the pitch is only a flat
summary (see the open pitch feedback), compress it but keep it one sentence.

Field sources:

```text
<venue>   STATUS.md  venue_frame   (fallback: venue_target, then 1-config.yaml)
<paper>   the paper folder name
Story     one sentence (may wrap ~2 lines), in the paper's working language;
          compressed from 1-pitch.tex P1 + the mechanism + the scope clause;
          append "(关联,非因果)" iff 2-claims marks the claim observational
```

Open needs block (printed directly under the panel; short, it is "what to do
next", not a report). Route each per `delivery-need.md`:

```text
Open needs (from 1-rounds/<round>/todo.md + 2-claims planned/GAP rows + missing displays):
  - <gap> -> <route>     e.g. Materialize Display 01-04 -> /haipipe-task-for-display
  - <gap> -> <route>     e.g. Backfill C1-C5 evidence anchors -> /haipipe-probe / /haipipe-task
```

## Maturity (orthogonal)

Maturity is separate from the frontier and read from artifacts, not assumed:

```text
prospectus            seed/pitch only
scaffold              lifecycle + sections + compile script
claim-ledger          2-claims has explicit claims
display-map           4-figures-tables maps claim -> display
section-map           5-minimap maps paragraph jobs
draft                 sections compile with prose
submission-candidate  audits/checks mostly pass
submitted             frozen PDF + submission metadata
revision              active 1-rounds round after external review
accepted/published    final external state
```

## Open Needs

Round todo items and claim/display gaps are first-class open needs, not
afterthoughts. The dashboard lists them with a suggested route
(probe/discovery/task/display/insight/paper-edit) using the delivery-need
interface in `delivery-need.md`.
```
