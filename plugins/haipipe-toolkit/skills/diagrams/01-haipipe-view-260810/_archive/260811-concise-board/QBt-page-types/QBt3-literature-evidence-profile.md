# Literature evidence inside a View: citations become inspectable claims
state: 🟡 PARTIAL
owner: JL
method: test claim to citation bindings on definitions, prior findings, and absence-of-precedent statements

## Opening
What must a Literature Evidence Card show when a View relies on published knowledge rather than a project-produced result?
A citation key alone proves neither the proposition nor the job that the source performs in the View.
The Card must expose the supported statement, source scope, citation job, and any limit on novelty or validity language.
This page decides the Literature-specific additions inside the shared View contract without creating a separate Page Type, skill door, or workflow line.

**Where this page sits**: QA2 owns the shared Card fields, and QBt1 uses Literature Cards EC1 and EC2 for the trait description.

**Output distinction**: A literature matrix, citation ledger, prose packet, or `.bib` file is an output of the View, not the Evidence Card itself.

## Diagram

**The Literature binding**: a source supports one named proposition and one explicit job inside the View.

```text
📚 source ──▶ 🔑 key ──▶ 👀 VIEW · Literature profile
                         proposition · job
                         scope · boundary
                              │
                              ▼
                 View use + applicable boundaries
```

## Content

### 1 · Literature-specific fields
**The proposed additions**: the Card makes the citation's precise support inspectable.

```text
key          resolvable bibliography key
proposition  the statement the source supports
source place page, section, table, or bounded search scope
citation job define · establish · contrast · position · qualify
use form     direct fact · paraphrase · synthesis
strength     direct · adjacent · indirect
novelty      supported · threatened · broken · not tested
```

An absence-of-precedent statement must carry the search scope and may never become an unrestricted novelty claim.
The generated bibliography package may include only keys claimed or cited by accepted outputs.

## Aims

### A1 · Literature-specific fields
- A1.1 · Define a citation binding that states both proposition and job.
  **Done when:** A key cannot appear without saying what it supports and how the View uses it.
- A1.2 · Preserve bounded language for novelty and construct validity.
  **Done when:** Search limits and adjacent evidence cannot silently become universal claims.

## States

### A1 · Literature-specific fields
- 🔨 A1.1 · QBt1 now resolves a real bibliography Card and source link; proposition, source place, and citation job still need one unified profile payload.
- ✅ A1.2 · Content 1 forbids unrestricted novelty claims from bounded absence evidence.

## Files

- `QBt1-for-view.md`
  The base specimen and its two Literature Cards.

## Log

- 260810 · [RULING-JL] Kept Literature as an internal View evidence profile and removed the need for a separate `for-literature` Page Type or workflow line.
- 260810 · [DRAFT-CC] Opened as an Evidence Card profile, leaving table and bibliography forms in the output layer.
