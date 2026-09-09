# Minimal current Board

Use this only when a concrete source shape is useful. Normative rules remain
in `SKILL.md`, `board-form.md`, and `haipipe-page`.

## Source tree

```text
01-entry-criteria-260905/
├── board.md
├── 1-G1-eligibility/
│   └── G1-entry-rule/
│       ├── G1-entry-rule.md
│       └── outline/
│           ├── G1-entry-rule-outline-v0.1.md
│           ├── G1-entry-rule-files.md
│           └── G1-entry-rule-log.md
└── board/                         generated
```

## board.md

```markdown
# Analysis entry criteria
spine: make the eligibility rule explicit enough to implement and review.
close: G1 is settled and its accepted rule is ready for downstream use.

## Topic
This Board defines which records enter one analysis and why each condition is necessary.

## Pipeline
G1 settles the rule before downstream extraction begins.

## Pages
### G1 · Eligibility
Define and verify the entry rule.
G1-entry-rule.md
```

## G1-entry-rule.md

````markdown
# Verifiable entry rule
state: 🟡 PARTIAL
owner: CC

## Opening
The analysis needs one entry rule that a reader can understand and an executor can implement. This Page owns the conditions, their rationale, and the final review boundary; downstream extraction remains outside it.

## Content
### 1 · Conditions
**Division map:** how candidate records become the eligible set.

```text
📥 candidate records
   │ apply explicit conditions
   ▼
✅ eligible records
```

#### 1.1 · Executable conditions
(state each condition in a form that can be implemented and reviewed)
Each condition names its field, operator, threshold, and missing-value behavior.

## Aims
### A1 · Conditions
- 🔨 A1.1 · Every entry condition is executable.
  **Done when:** Each condition maps to one deterministic predicate.
  **Now:** The predicates exist; missing-value behavior still needs review.
- ⬜ A1.2 · Every condition has a stated rationale.
  **Done when:** A reader can connect each condition to the analysis boundary.
  **Now:** Not started.
````

## outline/G1-entry-rule-outline-v0.1.md

```markdown
# Outline v0.1
outline-version: v0.1
approved: ⬜

| Address | Bullet | Feedback | Evidence | Supporting Run | Local Run |
|---|---|---|---|---|---|
| C1.P1.B1 | State each executable condition. | — | E01-VALUE-condition-count | — | Page · Evidence Item · new-run · 1-G1-eligibility/G1-entry-rule |
```

The rendered Page generates its Outline from this plan. The Page source does
not contain an authored `## Outline`, and process history remains in the
Outline records rather than Page-level sections.
