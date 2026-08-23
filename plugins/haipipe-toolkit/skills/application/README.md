# Application skill family

An Application is TWO boards. One understands the data; the other designs what gets sent. It ends at accepted.

```text
🔎 InsightBoard                                    🎨 DesignBoard
Meta + Question registers → D→I→K→W  ── PageX ──▶  Brief → Principle → Design → ✅ accepted
MT00 says what EXISTS                              only P reads the InsightBoard
MT01-MT04 say what is ASKED of each rung           render/ plugin projects accepted divisions
```

## Ownership

| Layer | Owns | Does not own |
|---|---|---|
| Task/Discovery | execution and source evidence | Application framing |
| InsightBoard · Meta | source inventory, grain, freshness | any interpretation, any question |
| InsightBoard · Question registers | what is asked of each rung, raiser, state, the board rollup (on MT04) | any answer, any probe |
| InsightBoard · D/I/K/W | Task-backed Probe, observations → patterns → claims → counsel, Design Handoff (W only) | final message copy |
| DesignBoard · Brief | opportunity, audience, outcome, venue scope, needs raised | the answers to those needs |
| DesignBoard · Principle | because-<W>-do-<move>-within-<rail> warrants · the ONLY DesignBoard reader of the InsightBoard | raw Task/Discovery inspection |
| DesignBoard · Design | PageX selection, message system, per-division acceptance | probing anything |

Folder ownership does not transfer evidence authority. A D page lives in the Application folder but follows Task source/run/staleness rules.

## Page Types

```text
application/page-types/
├── haipipe-page-for-meta/         one InsightBoard head · what data exists · NO question
├── haipipe-page-for-question/     four registers MT01-MT04 · what is asked of each rung
├── haipipe-page-for-data/         D · observed, run-bound, uninterpreted
├── haipipe-page-for-information/  I · rates and contrasts derived from named D rows
├── haipipe-page-for-knowledge/    K · a proposition with strength, rivals, boundary
├── haipipe-page-for-wisdom/       W · counsel + Design Handoff · the only bindable level
├── haipipe-page-for-brief/        one DesignBoard head · what is being built, for whom
├── haipipe-page-for-principle/    P · why this will work · the only crossing
└── haipipe-page-for-design/       DS · one audience × job × venue message system
```

`page-type: insight` is TASK-ONLY (the whole chain in one consumer-neutral page, `task/page-types/`). Retired 2026-08-20: `intervention` became `design`; `artifact` was absorbed into a per-division `accepted:` row. Split 2026-08-21: the Meta page's Insight Roster became the four question registers.

## Target runtime

A board's folder name says its subject: the data for an InsightBoard, the topic for a DesignBoard. PascalCase subject, literal kind, so `ls *-DesignBoard` finds them all.

```text
<application-root>/
├── InsightBoard-<Cohort>/                e.g. InsightBoard-SMSR2Full
│   ├── board.md
│   ├── 0-MT-meta/
│   │   ├── MT00-meta/                    sources · grain · freshness · limits
│   │   ├── MT01-question-data/           QD<n> · asks of 1-D-data/
│   │   ├── MT02-question-information/    QI<n> · asks of 2-I-information/
│   │   ├── MT03-question-knowledge/      QK<n> · asks of 3-K-knowledge/
│   │   └── MT04-question-wisdom/         QW<n> · asks of 4-W-wisdom/ + board rollup
│   ├── 1-D-data/D<NN>-<slug>/            observed · run-bound
│   ├── 2-I-information/I<NN>-<slug>/     derived · cites D
│   ├── 3-K-knowledge/K<NN>-<slug>/       claimed · cites I
│   └── 4-W-wisdom/W<NN>-<slug>/          counsel + handoff · cites K
└── DesignBoard-<Program>/                e.g. DesignBoard-RefillFraming
    ├── board.md
    ├── 0-BR-brief/BR00-brief/            outcome · venue scope · audience set · needs
    ├── 1-P-principle/P<NN>-<slug>/       cites W · the only crossing
    └── 2-DS-design/DS<NN>-<slug>/        units as divisions · render/ plugin projections
```

Because the subjects are named independently, the count is free: several InsightBoards when the Application reads distinct data, several DesignBoards when it designs for distinct topics, and any DesignBoard may PageX-bind any InsightBoard.

A project using the `<Letter><NN>_<slug>` folder grammar may prefix runtime boards for ordering — `A<NN>_` InsightBoards, `B<NN>_` DesignBoards, as in `A01_InsightBoard-SMSR2Full` — a project-local prefix that never appears inside pages.

The MT group law: **nothing in MT concludes**. Meta describes, the registers ask, and neither owns `probe/` or `display/`, because a probe brings back an answer and a figure is one. Only D/I/K/W pages own `probe/`. Each Design Page owns `pagex/` bindings to exact Brief and W-handoff material, and PageX crosses boards unchanged because it binds by path.

## The Application ends at accepted

Deciding that an exact version may go is a design judgment and stays on the DesignBoard. Building it, shipping it, running the experiment, and collecting what came back are task-layer work. There is no `deploy/` folder and no round folder; the loop closes back through a source refresh reopening D pages, not through a stage on this board.

## Router

```text
/haipipe-application meta              inventory the data this board reads
/haipipe-application question          register one question on the rung register it faces
/haipipe-application chain             open or extend one D→I→K→W chain for one question
/haipipe-application brief             frame what is being built and the needs it raises
/haipipe-application design            author one audience/job/venue message system
/haipipe-application render            project an accepted division through the render/ plugin
/haipipe-application review | accept   exact-version gates, per division
/haipipe-application retarget          re-pin venue or audience, reopen dependent Design
```

## Compatibility

Legacy stage skills under `_old/` remain readers during migration. New work does not copy the descriptions/themes/claims/advice ladder, a flat `1-probes/`, a `4-deploy/`, or a `5-rounds/`. An existing page carrying `page-type: intervention` has its key renamed to `design`; one carrying `page-type: artifact` folds into its Design Page as a division. A Meta page still carrying an Insight Roster moves those rows to the four registers, keeping each question's raiser. External settled Insight Pages remain valid PageX inputs and are never moved automatically.
