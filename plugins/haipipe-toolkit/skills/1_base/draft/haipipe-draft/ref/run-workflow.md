This file holds the Page Run Workflow (which Run Spec holds authority), the Writing DNA handoff and the authority test, moved from `SKILL.md`.

## 🎭 Page Run Workflow, independent of Folder kind

A Page Face persists while its Page Run Workflow authority changes. The page
workflow (`haipipe-draft-workflow`) is a directed graph of Runs; each Run has one
owner page or skill (the plan's steps live in `haipipe-draft-logic`), independent of the domain workflow that owns
the Folder kind:

```text
run        step              skill                          gate
────────────────────────────────────────────────────────────────────────────────────
context    PREPARE           haipipe-draft-logic                     ⚙ resolved context
structure  SHAPE             haipipe-draft-logic                     👤 approved:
           SURVEY            haipipe-draft-logic                     👤 Decide per item
scratch    Save · Finish     haipipe-draft-logic                     👤 Finish Scratch
evidence   LAND              haipipe-evidence ref/page-evidence     ⚙ local work exhausted; external gates named
           EMBED             haipipe-evidence ref/page-evidence     ⚙ v0 → SHAPE · G>=1 → writing
writing    WRITE             haipipe-draft-writing      ⚙ cold pre-check ready
revise     compare · decide  haipipe-draft-writing ref/revise.md 👤 every change decided
delivery   build             haipipe-delivery ref/page-delivery     ⚙ build receipt current
check      CHECK             haipipe-draft-review (page check)       👤 accepted:
```

The evidence loop law: SHAPE specifies typed Evidence Items; SURVEY
plans zero-to-many Execution/Discovery Supporting Runs plus exactly one Page
`RE` lineage per item; LAND produces one ready local Result/Card; EMBED
interprets it. The ledger is `evidence/cards.yaml` (a Page made before 2026-10-16: `draft/<stem>-evidence-items.md`)
(`workbench-task-draft/ref/item-table.md`).

Collaborative writing uses persistent `RP` Runs across one Page under
`../haipipe-draft-workflow/ref/interactive-writing-run.md`.
A Structure Run (`run-structure-…`) settles, through its SHAPE and SURVEY cycles,
Structure, Outline Bullets, Point roles, paragraph jobs, and typed
evidence decisions; it does not write full prose or execute evidence work.
Several people may contribute Steps to the same Structure Run; record
`participants` and per-Step `contributors` rather than creating one Run per
person. A Section Run (`run-section-…`) covers one named Section drafting/revision session.
A Paragraph Run (`run-paragraph-…`) covers one fixed paragraph or contiguous paragraph
group. A complete Section draft → review/rating → diagnose → revise cycle is
one Step inside its Section Run, not a new Run. If the person later
commissions another independent Section drafting/revision session, allocate a
new Section Run. For the same paragraph target, reopen the existing Run in a
new Version unless the target or goal materially changes. Closing one Run
does not modify Page Content or delivery. After all planned RP Runs and
required evidence Results are complete, one Page-level CONTENT pass adopts the
agreed wording. It then reruns the fixed Delivery Run of each declared lane
(`page.py export`) without commissioning an additional delegated Task Run for
every accepted paragraph. A Delivery Run is a build, not a second CONTENT or
check gate.
The historical/explicitly delegated single-paragraph profile remains in
`haipipe-draft-writing/ref/paragraph-run.md`. Neither path adds a workbench.

### 🧬 Writing DNA handoff

The Page has one style authority: the resolved Context and its authored
requirements. When the external `writing-dna-skill` supplies a profile, the
Page carries a frozen, style-only packet into CONTENT; it does not copy the
corpus into the Page, create a second Outline, or treat DNA as Evidence.

```text
CONTEXT/PREPARE  resolve policy + profile id/status/version
OUTLINE/SHAPE    freeze the reader job, Bullet order, claim contract, and any
                 declared paragraph-level Narrative Decision
EVIDENCE         land and fold factual Results; DNA has no evidence authority
WRITING RUN      freeze applicable Decision + style packet; reload only on drift
CONTENT/WRITE    adopt agreed wording; preserve its recorded style decisions
CHECK            judge the built Page and the Run's recorded style application
```

If a named style is required but its profile or required exemplars cannot be
resolved, CONTEXT/HOLD owns the block. If the style is optional, CONTENT may
write under the Page owner's policy without DNA. A profile can change wording,
rhythm, and compatible structure only after the content contract is stable;
claim strength, evidence order, topic, and reader promise remain Page-owned.
A declared `Narrative Decision` is the approved reason for a paragraph's
organization; it is consumed by CONTENT, is not an Evidence Item, and is never
minted or rewritten by Writing DNA. If it conflicts with the approved Outline,
route back to OUTLINE.
The HAI-side adapter and three-pass realization rules are
[`haipipe-draft-writing/ref/writing-dna-adapter.md`](../../haipipe-draft-writing/ref/writing-dna-adapter.md).

Resolve one invocation as: Folder → base Page Face → Run Workflow/Run Spec-owned
Folder kind or declared Page Type → current Run Spec → Run Spec-selected and
page-local workbenches.
The cycles form a routing grammar, not a conveyor belt: each may repeat,
SURVEY and LAND are skipped when the page promises nothing it cannot already
support, and CHECK may route to any earlier cycle. When the visible operation
is ambiguous, the authority test decides:

```text
governing policy/context is stale              → PREPARE
the section list itself is being agreed        → SHAPE
an item has no valid Run graph or Decide        → SURVEY
a decided item has no ready local Result        → LAND
a ready item is not yet in the plan             → EMBED
approved purpose, Aim promise, or structure changes → OUTLINE / SHAPE
prose realization changes under the same promise → CONTENT / WRITE
a concrete version is judged                   → CHECK
```

`RUN` is the router verb, deliberately not `ADVANCE`; it is owned by
`haipipe-draft-workflow`, whose `ref/page-run-contract.md` holds
the packet, receipt, version, role-separation and stop rules, and whose
`ref/run-cards.md` states every Run in the same six fields. A pass may run
inside a person's session (the page chat, which resolves Run owners and controller operations and reads the
strip: `haipipe-studio/ref/chat.md` §🔁) or as that Run's agent; both leave the same
trace (the artifact, one log record, the receipt).
