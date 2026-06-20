Insight Base INDEX Templates
=============================

Templates for the auto-maintained INDEX files. Per Q-b confirmed:
top-level INDEX.md + K_knowledge/INDEX.md + W_wisdom/INDEX.md.
D_data and I_information do NOT get sub-indexes (grep tags is
fast enough on flat lists).


Top-level: insights/INDEX.md
=============================

Auto-rebuilt by any layer skill on write. Sections in order:

```markdown
# Insight Base — <project>

Last rebuild: <ISO>


## By topic

### <topic-1>
- K03 — "<one-line claim>"                 [confidence: high]
- W01 — "<one-line rec>"                   [type: next_experiment]
- I02 — pattern across 3 D entries         [direction: mixed]
- D01, D02, D03 — observations             (3 entries)

### <topic-2>
...

(Group by frontmatter tags — most-frequent tag first. An entry with
 multiple tags appears under each.)


## By layer

| Layer | Count | Active | Stale | Superseded |
|-------|-------|--------|-------|------------|
| D     | 28    | 28     | 0     | 0          |
| I     | 6     | 6      | 0     | 0          |
| K     | 4     | 3      | 0     | 1          |
| W     | 3     | 3      | 0     | 0          |


## Recently changed (top 10)

| Date       | ID  | Layer | Title / Headline                                |
|------------|-----|-------|-------------------------------------------------|
| 2026-05-25 | K03 | K     | "FiLM overfits to seen patients..."             |
| 2026-05-23 | W01 | W     | "Param-matched FiLM re-test"                    |
| ...        | ... | ...   | ...                                             |


## All entries (flat — for grep)

D_data:  D01 .. D28
I_information:      I01 .. I06
K_knowledge:     K01 K02 K03 K04 K05 (K02 superseded by K05)
W_wisdom:        W01 W02 W03

(The flat list at the bottom helps `grep -A 1 K03 insights/INDEX.md`
 land cleanly on the entry's summary.)
```

Length budget: ≤ 300 lines for projects with ≤ 100 entries.


K-layer: insights/K_knowledge/INDEX.md
========================================

```markdown
# K_knowledge Layer Index

Last rebuild: <ISO>
Active: <N_active> | Stale: <N_stale> | Superseded: <N_super>


## Active

| ID  | Claim                                                  | Confidence | Tags                  |
|-----|--------------------------------------------------------|-----------|------------------------|
| K01 | "<one-line claim from frontmatter>"                    | high      | [lhm, val]             |
| K03 | "FiLM overfits to seen patients; no transfer to OD"    | high      | [film, conditioning]   |
| K04 | "<one-line claim>"                                     | medium    | [scaling, train]       |


## Superseded (kept for history)

| ID  | Claim                  | Superseded by | When        | Tags     |
|-----|------------------------|---------------|-------------|----------|
| K02 | "<old claim>"          | K04           | 2026-05-15  | [scale]  |


## Contested (claims with conflicting evidence)

| ID  | Claim                  | Conflict source       | Tags         |
|-----|------------------------|-----------------------|--------------|
| (none yet)                                                            |
```

Length budget: ≤ 80 lines for K layer with ≤ 15 entries.


W-layer: insights/W_wisdom/INDEX.md
=====================================

```markdown
# W_wisdom Layer Index

Last rebuild: <ISO>
Active: <N> | Acted-on: <N> | Stale: <N>


## Active

| ID  | Recommendation                                         | Type             | Cost     | Derived from |
|-----|--------------------------------------------------------|------------------|----------|--------------|
| W01 | "Param-matched FiLM re-test"                           | next_experiment  | medium   | K03          |
| W02 | "Pivot main figure 3 to FiLM generalization gap"       | paper_direction  | cheap    | K03          |
| W03 | "Stop chasing val-only improvements; require test-od"  | stop_doing       | cheap    | K03, K05     |


## Acted-on (recently)

| ID  | Recommendation         | Acted-on date | Result                |
|-----|------------------------|---------------|-----------------------|
| (none yet)                                                            |


## Stale (decayed without action)

| ID  | Recommendation       | When stale    | Reason                |
|-----|----------------------|---------------|-----------------------|
| (none yet)                                                            |
```

Length budget: ≤ 60 lines for W layer with ≤ 10 entries.


Rebuild semantics
==================

Any layer skill that writes/updates an entry rebuilds:
  - data / information writes  → top INDEX.md only
  - knowledge writes/updates   → top INDEX.md + K_knowledge/INDEX.md
  - wisdom writes/updates      → top INDEX.md + W_wisdom/INDEX.md

Manual rebuild: `/haipipe-insight rebuild-index` (umbrella verb).

Rebuild procedure (idempotent):
  1. Glob insights/{D,I,K,W}_*/*.md
  2. Read frontmatter of each (one YAML parse per file)
  3. Group by tags (topic), by layer, by status, by created date
  4. Render into the templates above
  5. Atomic write (tmp → mv)

The entries themselves are source of truth; INDEX files are derived
state. If they ever disagree, `rebuild-index` trusts the entries.


Don't hand-edit
================

These INDEX files are auto-maintained. Hand edits will be overwritten
on the next rebuild. If you want a section the rebuild doesn't
produce, add a frontmatter tag to the source entries and let the
rebuild pick it up via "By topic".
