# board

`board/` is the first-class HAI-Pipe family for turning one topic into a
reviewable set of question pages or lifecycle stages.

## Entry points

- `haipipe-board/` is the callable skill and owns the Board format, actions,
  renderer, local service, write-back, checks, and the reply-ending session
  status strip. It is the family's one DOOR.
- `haipipe-page/` is a loadable SPEC: what a Page is, its six Page Types over
  one base, its sections in their fixed order, and how it resolves a stable
  Page Type plus a current Page Phase. Its `RUN` verb uses a shared raw-material
  packet and auditable phase receipt rather than a fixed phase sequence. A
  Page's `Files › Related Board Pages` rows add checked, phase-scoped context;
  the engine reads them once through `cli/pagecontext.py`, never recursively.
- `page-types/` holds the FIVE variants this skill set owns. A variant ships
  under the `page-types/` folder of the skill set that owns it (JL 260809), so
  the six paper- and labeling-specific variants live with their own families:
  `paper/page-types/` and `subjective-label/skills/page-types/`.
  - `haipipe-page-for-stage/` is the VARIANT for `S-<Family>-<unit>` lifecycle
    pages. It owns the persistent chain and gate shape, not the active phase. It
    stays here because a stage page is a BOARD mechanism that both the paper and
    application families instantiate.
  - `haipipe-page-for-skill/` is the VARIANT for the two mirror kinds,
    `Skill-<n>` and `Agent-<n>`. A skill page mirrors a unit that ships elsewhere
    and decides nothing, so its Opening introduces the unit instead of asking a
    question.
  - `haipipe-page-for-meeting/` is the VARIANT for `Meeting-<n>`: talk is
    recorded there and ruled elsewhere, and it is never counted as settled.
  - `haipipe-page-for-slide/` is the VARIANT for a deck, one division per slide,
    each embedding the one deck file live.
  - `haipipe-page-for-design/` is the VARIANT for a design brief: candidates side
    by side, closing on a SELECTION record.
  ⚠️ Moving a variant between skill sets does not move its installed symlink.
  Re-run `Tools/install.sh --global` afterwards or the skill stops resolving.
- `page-phases/` holds the four host-agnostic phase contracts:
  `haipipe-page-draft`, `haipipe-page-probe`,
  `haipipe-page-revise`, and `haipipe-page-check`.
  They are selected by authority rather than by edit operation or a rigid order.
- `haipipe-sentence/` is a loadable SPEC: the atomic unit, the `>` lanes,
  the evidence card, and the archive-never-delete record lifecycle.
- `haipipe-board-routing/` is the WRITE VERB, at both altitudes. Board and group:
  propose a board's structure before any file exists, materialize it after
  approval, and keep the per-group lane blocks current (`src/lanes.py`). Page:
  one input, find the owning page and section, append an anchored write. It
  proposes rather than creates, and it closes only the boxes you have already
  answered. (`haipipe-board-digest`, the transcript-scale fan-out, is named on
  the roster and not yet shipped.)
- `haipipe-board-index/` was retired on 260802 and merged into
  `haipipe-board-routing`: three of its five verbs were the door's own `open`,
  `regroup.py` and `check.py` written a second time, and its one unique script
  moved with it.
- `agents/haipipe-board-creator-agent.md` produces one target Page in a fresh
  context. It supports batch creation plus exactly one DRAFT, PROBE, or REVISE
  phase for RUN; it never rebuilds or performs CHECK.
- `agents/haipipe-board-reviewer-agent.md` is the read-only, fresh-context
  CHECK. It judges one source/render version and returns CLOSE, REVISE, PROBE,
  DRAFT, or HOLD; it never repairs the Board it judges.
- `agents/haipipe-page-orchestrator-agent.md` is the non-interactive RUN
  target. It invokes the bounded Workflow, stores `_runs/page/` receipts, and
  calls the deterministic auditor without editing Page prose.

## Layout

```text
board/
├── README.md
├── CHANGELOG.md
├── agents/
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── haipipe-board-creator-agent.md
│   ├── haipipe-board-reviewer-agent.md
│   └── haipipe-page-orchestrator-agent.md
├── haipipe-page/
│   └── ref/page-run-contract.md
├── page-types/          the five variants THIS skill set owns
│   ├── haipipe-page-for-stage/
│   ├── haipipe-page-for-skill/
│   ├── haipipe-page-for-meeting/
│   ├── haipipe-page-for-slide/
│   └── haipipe-page-for-design/
├── page-phases/
│   ├── haipipe-page-draft/
│   ├── haipipe-page-probe/
│   ├── haipipe-page-revise/
│   └── haipipe-page-check/
├── haipipe-sentence/
├── haipipe-board-routing/
│   └── src/lanes.py
└── haipipe-board/
    ├── SKILL.md
    ├── CHANGELOG.md
    ├── status.py        ← the ONLY script at the top level
    ├── cli/             ← every other runnable script lives here
    ├── src/
    ├── live/
    ├── ref/
    ├── assets/
    ├── checks/
    ├── tests/
    └── vendor/
```

The Board engine's `src/page_context.py` plus `cli/pagecontext.py` implement
bounded cross-Page reads. `ref/page-lifecycle.workflow.js`,
`src/page_lifecycle.py`, `cli/pageflow.py`, and lifecycle tests are the
executable and auditable side of the Page-owned RUN contract.

The design Board remains a working artifact at
`../diagrams/01-boardform-260722/`. It does not ship inside the skill.

`page-types/` and `page-phases/` are organization folders, not skills of their
own. The installer discovers every nested `SKILL.md` recursively, while each
skill keeps its globally unique name.

Every Board-attached session makes its attachment public at the end of each
reply: Board, page-group queue, board/group/page focus, work mode, next action,
and deep link. `status.py` derives a concise three-line block from Board files
and never writes a shared status ledger.
