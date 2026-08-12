# Displays inside a View: one reader job per acceptance unit
state: ✅ SETTLED · several Displays may share one View and keep separate gates
owner: JL
method: distinguish View-level meaning from renderer craft and Display-level acceptance

## Opening
How can one View own several Displays without turning each figure or table into another View?
A Display is one inspectable expression selected from the View body for a specific reader job.
Several Displays may express the same subject at different detail levels or in different forms.
They stay in one View while each keeps its own artifact and human acceptance.
This Page decides cardinality, panel grouping, and the boundary between View ownership and renderer ownership.

**Example**: one main-result table and one appendix detail table may remain two Displays inside the same result View.

**Not a second Page Type**: table, figure, diagram, illustration, text, and ledger are Display kinds selected by the View, not public View variants.

## Diagram

**One View, several outputs**: the shared body supplies meaning while each Display keeps one artifact gate.

```text
View body + Cards
├── Display1 · main table       · acceptance 1
├── Display2 · appendix detail  · acceptance 2
└── Display3 · evidence ledger  · acceptance 3
```

## Content

### 1 · Cardinality

**The output roster**: rendering may begin empty, while delivery names one or more Displays.

```text
draft 0..n rendered Displays ──▶ deliverable 1..n promised Displays
```

A draft View may begin with no rendered Display, but a deliverable View promises one or more Displays.
Adding another expression does not create another View when the subject and View-level acceptance remain shared.
Every Display uses `<PageID>-Display<n>-<slug>` and is declared in the View manifest.

### 2 · One Display or several

**The panel test**: reader job and acceptance decision determine the unit.

```text
same reader job + one gate ──▶ one multi-panel Display
different job or gate ───────▶ separate Displays
```

Keep several panels in one Display when they perform one reader job and receive one acceptance decision.
Split them when a panel has its own destination, level of detail, artifact history, or acceptance decision.
Main and appendix expressions may therefore be separate Displays even when they use the same evidence.

### 3 · Ownership

**Three owners**: meaning, craft, and placement do not overlap.

```text
View semantic brief ──▶ renderer artifact ──▶ consumer placement
```

The View owns the reader job, semantic brief, body/Card bindings, caption intent, and acceptance state recorded in `output.md` and the manifest.
The selected renderer owns `recipe/`, candidate production, and the promoted asset.
The consumer owns placement and downstream prose.
No renderer adapter Page is created between the View output folder and the generic Display contract.

## Aims

### A1 · Cardinality
- A1.1 · Permit several Displays under one View identity.
  **Done when:** each Display inherits the Page id and has an independent artifact and acceptance state.

### A2 · One Display or several
- A2.1 · Provide a stable panel split rule.
  **Done when:** reader job and acceptance decision, rather than file count, decide the Display boundary.

### A3 · Ownership
- A3.1 · Assign semantic judgment, rendering craft, and placement to one owner each.
  **Done when:** View, renderer, and consumer responsibilities do not overlap.

## States

### A1 · Cardinality
- ✅ A1.1 · QBt1 owns two Displays with one Page id and two independent gates.

### A2 · One Display or several
- ✅ A2.1 · Content 2 handles multi-panel and main-versus-appendix cases without changing the View boundary.

### A3 · Ownership
- ✅ A3.1 · Both QBt1 output folders directly satisfy the generic Display intake and output contracts.

## Files

- `../QBt-page-types/QBt1-for-view.md`
  The complete two-Display specimen.
- `../../display/ref/display-intake-contract.md`
  The provenance boundary used by each View-owned Display.
- `../../display/ref/display-unit-output-contract.md`
  The renderer-complete output contract.

## Log

- 260811 · [RULING-JL] View is a first-class hub and may contain several Displays, including main and appendix expressions of the same subject.
- 260811 · [REVISE-CC] Folded the retired value, literature, and illustration profiles into one Display contract instead of keeping separate public View types.
