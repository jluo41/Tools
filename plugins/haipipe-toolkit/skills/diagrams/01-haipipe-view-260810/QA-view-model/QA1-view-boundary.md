# What makes one View
state: ✅ SETTLED · one named reading unit, not one claim or one file
owner: JL
method: separate the semantic boundary from evidence, Display, Board, and consumer mechanics

## Opening
What makes several materials one View, and when must they become separate Views?
A View is one named reading unit that a person can understand and inspect as a whole.
Its boundary follows the reader's subject rather than a claim count, file type, data level, or paper placement.
Different evidence forms may stay together when they answer the same reading job.
This Page decides the semantic boundary; QA2 through QA6 own the mechanics around it.

**Example**: a sample funnel, its row counts, and the reason for each exclusion can form one View even when they come from several Probes and produce more than one Display.

**Covered elsewhere**: QA2 owns Cards, QA3 owns Displays, QA4 owns the Board, QA5 owns consumer distribution, and QA6 owns gates.

## Diagram

**The boundary test**: one reader job may gather many inputs and outputs without becoming many Views.

```text
many inputs ──▶ one named reading job ──▶ one View
                         │
                         ├── same subject, another expression ──▶ same View
                         └── independently useful reading job ──▶ another View
```

## Content

### 1 · Unit of meaning

**The semantic unit**: varied material is grouped by one reader job.

```text
data · method · literature · result · limitation ──▶ one readable subject
```

A View is the smallest separately named body that a person may inspect, accept, and hand to a consumer.
It may describe data, method, literature, a result, a limitation, a construct boundary, or a combination that belongs to one reading job.
It is not required to contain one claim, one Probe, one data object, or one Paper section.

### 2 · Split and merge rule

**The split test**: independent usefulness or acceptance creates another View.

```text
shared reading job + shared View gate ──▶ merge
independent reading job or View gate ───▶ split
```

Keep material in one View when it shares one subject, one readable body, and one acceptance decision at View level.
Split it when either part is useful to a consumer without the other, needs a different substantive acceptance decision, or would force the title to name two unrelated reading jobs.
A different Display, panel, source, or Paper placement alone does not force a split.

### 3 · Identity

**The owner chain**: one Page id names the resource unit and every Display.

```text
<PageStem>.md ──▶ views/<PageStem>/ ──▶ <PageID>-Display1..n
```

The canonical Page stem is the View identity.
The same-named resource folder carries authored resources, and every Display inherits the Page id.
Do not mint a second View index in `view.md`, a local output sequence, or a parallel claim id.

## Aims

### A1 · Unit of meaning
- A1.1 · Define a View without classifying its subject matter.
  **Done when:** data, method, literature, result, and limitation Views all fit the same boundary.

### A2 · Split and merge rule
- A2.1 · Give a reader-facing test for one View versus two.
  **Done when:** claim count, source count, Display count, and Paper placement cannot split a View by themselves.

### A3 · Identity
- A3.1 · Preserve one owner index across Page, resources, and Displays.
  **Done when:** the Page stem names the View folder and its Page id prefixes every Display.

## States

### A1 · Unit of meaning
- ✅ A1.1 · The contract names one readable and independently acceptable subject without imposing a topic taxonomy.

### A2 · Split and merge rule
- ✅ A2.1 · Content 2 separates a true reading-job boundary from differences in source, expression, or destination.

### A3 · Identity
- ✅ A3.1 · QBt1, QV1 in cmsreg, the builder, and the Page Type all use one owner-index chain.

## Files

- `../QBt-page-types/QBt1-for-view.md`
  The complete specimen governed by this boundary.
- `../../view/haipipe-view/SKILL.md`
  The shipped View workflow.
- `QA2-evidence-card-contract.md`
  The next question, which defines how evidence is inspected inside the boundary.

## Log

- 260811 · [REVISE-CC] Narrowed QA1 to the semantic split-and-merge boundary after QA3 through QA6 received Display, Board, consumer, and lifecycle mechanics.
- 260810 · [RULING-JL] A View may cover any subject and is not restricted to one claim, one data level, or one Paper placement.
