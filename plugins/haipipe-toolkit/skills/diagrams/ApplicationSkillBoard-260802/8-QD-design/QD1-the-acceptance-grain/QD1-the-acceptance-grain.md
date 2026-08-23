# The acceptance grain: one signature covers one division, not the page

state: ✅ SETTLED · per-division acceptance ruled 260820
owner: JL

## Opening

When a reviewer approves a message, what exactly has been approved?

One division, not the page it sits on. Acceptance used to sit on the Page, so a single signature covered every message at once. Since 260820 it sits on each `R<n>` division, which is what let the artifact Page Type retire. One message can be accepted while the one beside it is still being revised, and a changed handoff clears only the rows that depended on it.

### Writing Style

Name what a signature covers and what it leaves untouched. Vague wording here produces a page approved as a whole while half of it was never read.

## Diagram

```text
🎨 D01-young-male-refill                             page-type: design
│
├── R1 · first nudge      accepted: JL 260815 · handoff I01@v2 · render v3
├── R2 · reminder day 3   accepted: JL 260815 · handoff I01@v2 · render v3
├── R3 · escalation       🔨 in revision, no row
└── R4 · abtest arm       accepted: JL 260818 · handoff I03@v1 · render v5

  I01 refreshes to v3  ──▶  clears R1 and R2 only
                            R3 was never accepted · R4 cites I03 and stands
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Every accepted division carries one row naming reviewer, date, handoff version, and render version. A division with no row is not accepted, and absence is the only way to say so.

#### 2 · What clears a row

Four inputs clear it: a changed Insight handoff the division cites, an edit to the division's own content, a changed venue constraint, and a re-render. Clearing is scoped by citation, so a refreshed handoff touches only the divisions that named it. Siblings are left alone, and that scoping is the whole point of moving the signature down.

#### 3 · Why this replaced a Page Type

`page-type: artifact` held six Content roles. Five already existed inside a unit division: unit contract, authored content, variants, trace, and render. The sixth, acceptance, differed only in where a name and a date got written. A Page Type that relocates one signature is a field, and QBt3 records the full comparison.

#### 4 · What the page-level state still says

The Page's own `state:` line reports the system: whether the set coheres, whether the rails hold, whether the whole thing is reviewable. Each division's row reports the unit. Both are needed, because a set of individually accepted messages can still fail as a sequence.

#### 5 · The failure this prevents

Page-level acceptance forces re-approval of unchanged content whenever one message moves, which trains a reviewer to sign without rereading. Division-level acceptance keeps each signature small enough to mean something.

## Aims

### A1 · Contract
- A1.1 · One unit can be accepted while a sibling is not, without a second Page.
  **Done when:** acceptance lives on the division and clears per division.

#### A2 · Scoping
- A2.1 · A refreshed handoff clears only the divisions that cite it.
  **Done when:** clearing is driven by citation rather than by page.

#### A3 · Coverage
- A3.1 · The case the retired artifact type existed for still works.
  **Done when:** an independently shipped arm is expressible as one division row.

## States

### A1 · Contract
- ✅ A1.1 · Design Page Type 0.3.0 carries the per-division `accepted:` row.

#### A2 · Scoping
- ✅ A2.1 · Stated in the Design contract and in the public door's acceptance gates.

#### A3 · Coverage
- ✅ A3.1 · The SMS-R4 A/B holdout arm, the motivating case, is one division with its own row.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-design/SKILL.md`
  The acceptance-per-division section and the closing checks that enforce it.
- `../../../../application/haipipe-application/fn/design.md`
  The procedure that writes the row.

### 🧪 Checks
- `../../6-QBt-page-types/QBt3-for-artifact/QBt3-for-artifact.md`
  The six-role comparison that retired the second Page Type.

## Law

A signature covers exactly what it can be checked against. One division, one row, cleared by citation.

## Log

260820 · Moved acceptance from the Page to the division and retired `page-type: artifact` (JL: "I think we only need to keep one conception").
