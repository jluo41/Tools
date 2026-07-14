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
0-seed -> 1-resource -> 1-claims -> venue -> 2-pitch -> 3-narrative -> 4-display
-> 5-section-edit -> review
```

(`1-resource` and `1-claims` share the number 1, deliberately, exactly as `2-venue`
and `2-pitch` already do. The number is decoration; the spine key is the bare name
`resource`, and `stage-strip.sh` strips the digit before matching.)

The frontier is the first stage whose disk predicate fails.

| Stage | Done when | Next action if frontier |
|---|---|---|
| `0-seed` | `0-lifecycle/0-seed/0-seed.md` has question / motivations / claim-shape content | `/haipipe-paper seed` |
| `1-resource` | `0-lifecycle/1-resource/1-resource.md` exists with its two sections (Demand, Questions); **`n/a` counts as a PASS** -- see the exemption below | `/haipipe-paper resource` |
| `1-claims` | `0-lifecycle/1-claims/1-claims.md` ledger non-empty, each row has a status (anchor `planned` still counts as a status; unmaterialized evidence is an open need, not a stage fail) | `/haipipe-paper claims` |
| `venue` | STATUS.md `venue:` pinned to a playbook pack | `/haipipe-paper venue` |
| `2-pitch` | `0-lifecycle/2-pitch/2-pitch.md` has a one-line pitch | `/haipipe-paper pitch` |
| `3-narrative` | `0-lifecycle/3-narrative/3-narrative.md` has an arc | `/haipipe-paper narrative` |
| `4-display` | `4-display.tex` maps claim -> display and display units exist | `/haipipe-paper figures` |
| `5-section-edit` | `0-lifecycle/5-section-edit/<section>/` scaffolds exist and `0-sections/*.tex` compile to PDF | `/haipipe-paper section-edit` |
| `review` | audits pass and venue checks pass | `/haipipe-paper review` |

Resource exemption (pre-resource papers):

```text
The resource stage was added on 2026-07-14. Every paper that already exists on
disk predates it, and none of them will ever have a 1-resource.md written
retroactively.

So `n/a` is an ACCEPTED PASS for the resource row: a paper whose seed was
approved BEFORE the stage existed passes the resource predicate by exemption,
and the frontier walks straight past it to claims.

Without the exemption, EVERY live paper's frontier would REGRESS to `resource`
and the console would report DRIFT on papers whose seeds JL personally approved.

The exemption is granted per-paper and only backwards: it applies when the
paper's seed gate was closed before the stage shipped. A paper seeded after
2026-07-14 gets no exemption -- an absent 1-resource.md is a real frontier.
```

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
5. Surface open needs from 1-claims GAP rows, 4-display missing units,
   5-section-edit open checklist items, section TODOs, and
   1-rounds/<round>/todo.md.
```

## Render Skeleton

Lead with a paper header, then a one-line Story, then the progress spine. This is
the panel a session sees on enter. Keep it tight; open needs follow below it.

```text
📄 <paper-folder-name>  ·  <venue>

  Story: <one plain sentence: the angle + the surprising mechanism + scope/caveat,
         compressed from 2-pitch.md (fallback 3-narrative). Append "(关联,非因果)"
         when 1-claims marks the claim observational.>

  进度  seed ─ resource ─ claims ─ venue ─ pitch ─ narrative ─ display ─ section-edit ─ review
         <g>    <g>        <g>      <g>     <g>     <g>         <g>       <g>            <g>
                                                       🔥 这里(<one-clause why this is the frontier>)
```

Per-stage glyph (derive-from-disk; show each stage's TRUE state, not a blanket
todo downstream):

```text
✅ done       the stage predicate passes AND the artifacts it references resolve
(草稿)         the artifact exists but is rough / incomplete (e.g. sections drafted but thin)
⬜ todo       absent, empty, or its referenced anchors do not resolve
🔥 frontier   the FIRST stage that is not ✅; overlay it and annotate "← 这里"
⚠️ drift      STATUS.md claims this stage done but the disk predicate fails
```

Worked example (MedJournal, derived from disk on 2026-06-22):

```text
📄 Paper-Personality-Opioid-MedJournal  ·  medical journal (IMRAD)

  Story: 患者感知的医生"可亲和性"(LLM 从评论里测)越高 → 腰背痛阿片处方强度越高,
         主要走"已开药者剂量"而非开药人数,双重资格人群更明显。(关联,非因果)

  进度  seed ─ resource ─ claims ─ venue ─ pitch ─ narrative ─ display ─ section-edit ─ review
         ✅     n/a        ✅       ✅      ✅      ✅          🔥        (草稿)          ⬜
                                                              ← 这里(0-displays 只有 display00,01-04 没建)
```

(`resource n/a` = the exemption above. This paper was seeded before 2026-07-14, so the
frontier walks past resource to claims; `n/a` is a PASS and is NOT drift.)

Frontier = display: `4-display.tex` names Display 01-04 but `0-displays/`
has only display00. section-edit shows (草稿) because `0-sections/*.tex` have
rough prose while their display anchors are unbuilt.
The Story line is the compressed 2-pitch one-liner; if the pitch is only a flat
summary (see the open pitch feedback), compress it but keep it one sentence.

Field sources:

```text
<venue>   STATUS.md  venue_frame   (fallback: venue_target, then 1-config.yaml)
<paper>   the paper folder name
Story     one sentence (may wrap ~2 lines), in the paper's working language;
          compressed from 2-pitch.md P1 + the mechanism + the scope clause;
          append "(关联,非因果)" iff 1-claims marks the claim observational
```

Open needs block (printed directly under the panel; short, it is "what to do
next", not a report). Route each per `delivery-need.md`:

```text
Open needs (from 1-rounds/<round>/todo.md + 1-claims planned/GAP rows + missing displays):
  - <gap> -> <route>     e.g. Materialize Display 01-04 -> /haipipe-task-for-display
  - <gap> -> <route>     e.g. Backfill C1-C5 evidence anchors -> /haipipe-paper probe "<need>"
                              (opens a question SECTION in 1-probes/; the PROBE phase MATCHes
                               the bank first, and commissions only if nothing answers it)
```

## Maturity (orthogonal)

Maturity is separate from the frontier and read from artifacts, not assumed:

```text
seed                  seed/pitch only
resource              1-resource settled: every demand HAVE+FIT, COMMISSIONED, or SCOPE CUT
resource-blocked      the demand is real, the resource is in flight or behind a DUA,
                      and there is nothing to do but wait (resource's `park` exit)
scaffold              lifecycle + sections + compile script
claim-ledger          1-claims has explicit claims
display-map           4-display maps claim -> display
section-edit          5-section-edit scaffolds with DPRC in progress
draft                 sections compile with prose
submission-candidate  audits/checks mostly pass
submitted             frozen PDF + submission metadata
revision              active 1-rounds round after external review
accepted/published    final external state
```

## Open Needs

Round todo items and claim/display gaps are first-class open needs, not
afterthoughts. The dashboard lists them with a suggested route
(probe/discovery/task/display/paper-edit) using the delivery-need
interface in `delivery-need.md`.
```
