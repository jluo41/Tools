# One View Page, many Views on a Board
state: 🟡 PARTIAL · skill-design Board fixed; standalone application Board awaits a specimen
owner: JL
method: separate one View unit from the Board that manages a collection of Views

## Opening
What does a View Board manage, and how is it different from the single View Page it contains?
One View is one canonical Page with same-named resources; it is never a Board by itself.
A View Board manages several such Pages, their shared intake, acceptance, and consumer handoffs.
The current folder is the View Skill Board, while cmsreg remains an application that embeds one QV group.
This Page decides those levels and leaves a standalone application Board open for proof.

**Skill-design Board**: QA decides the reusable contract, QBt proves it, and QCskill mirrors the units that ship it.

**Application Board**: QV Pages organize real project evidence and distribute accepted fixtures to Paper or another consumer.

## Diagram

**Two Board roles**: design ships the mechanism; application accumulates the project Views.

```text
VIEW SKILL BOARD                         APPLICATION BOARD
QA contract                              QV1 real View
  └── QBt specimen ── ships skill ──▶    QV2 real View
        └── QCskill mirrors              QV3 real View
                                             └── accepted fixtures ──▶ consumers
```

## Content

### 1 · Unit and collection

**The two levels**: Pages hold View meaning; the Board holds the roster.

```text
one View Page ── many times ──▶ one View Board
```

One View Page owns one readable body, its Cards, its Displays, and its consumers.
A View Board owns the roster across many View Pages: why the collection exists, which Views are open, which are accepted, and which consumers are waiting.
Board state never replaces the independent state inside a View or Display.

### 2 · Embedded and standalone application modes

**The mode choice**: dependency scope decides where the QV roster lives.

```text
one upstream Board ──▶ embedded QV group
several upstreams or consumers ──▶ standalone View Board
```

An upstream Task or Discovery Board may carry a `QV` group when the Views remain tightly bound to that Board's answered material.
A standalone View Board is warranted when Views draw from several upstream Boards, serve several applications, or need a close condition independent of one task.
Both modes use the same View Page and resource contract.

### 3 · This Board

**The design pipeline**: contract, specimen, and shipped mirrors stay separate.

```text
QA1–QA6 ──▶ QBt1 ──▶ QCskill
```

`01-haipipe-view-260810` is the View Skill Board under the toolkit's `skills/diagrams/` home.
It has only three groups: six QA decisions, one QBt specimen with its consumer fixture, and QCskill mirrors.
It is not the cmsreg Board and does not adopt cmsreg's evidence or application state.

## Aims

### A1 · Unit and collection
- A1.1 · Keep one View equal to one Page, while allowing one Board to manage many Views.
  **Done when:** no resource folder, Display, or individual View is mistaken for a Board.

### A2 · Embedded and standalone application modes
- A2.1 · Preserve one Page contract across both application modes.
  **Done when:** moving a View collection does not change the internal View schema.
- A2.2 · Prove the standalone mode in one real application.
  **Done when:** a Board with several Views closes independently and hands accepted fixtures to a consumer.

### A3 · This Board
- A3.1 · Make the View Skill Board visibly distinct from cmsreg.
  **Done when:** its Topic, Pipeline, Map, roster, and session strip all point here.

## States

### A1 · Unit and collection
- ✅ A1.1 · QA1 and the View Page Type define one View as one Page/resource identity; this Page defines the collection above it.

### A2 · Embedded and standalone application modes
- ✅ A2.1 · cmsreg QV1 uses the same schema as QBt1 without changing the skill contract.
- ⬜ A2.2 · No standalone application View Board with several accepted Views has been reviewed yet.

### A3 · This Board
- ✅ A3.1 · The compact roster is QA, QBt, and QCskill; cmsreg is named only as an application.

## Files

- `../board.md`
  The View Skill Board roster and close condition.
- `../QBt-page-types/QBt1-for-view.md`
  One View Page, not one Board.
- `../../../../../../examples/Project-Personality-OpioidRx/diagram/02-cmsreg-260725/QV-views/QV1-data-lbp-analysis-sample.md`
  The current embedded application specimen.

## Log

- 260811 · [RULING-JL] The active Board is the View Skill Board rather than cmsreg.
- 260811 · [REVISE-CC] Distinguished the existing embedded QV application from the still-unproven standalone application mode.
