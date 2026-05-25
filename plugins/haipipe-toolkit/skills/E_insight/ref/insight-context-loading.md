Insight Base Context Loading — Strategy
========================================

How Claude (or any caller) should load context from
`examples/<project>/insights/` efficiently.


Principles
==========

  1. **Frontmatter first.** Never read body before reading frontmatter.
  2. **Tag-based filtering.** `tags:` is the primary index, not full-text.
  3. **Layer-cascading.** Start from K (highest signal), descend only if needed.
  4. **Lazy traversal.** Follow `sources` / `ref_by` only when asked.
  5. **INDEX.md as gateway.** The 200-300 line top-level INDEX is the
     fastest first read.


File layout (recap)
====================

```
insights/
├── INDEX.md                       ← master gateway (auto-maintained)
├── K_knowledge/
│   ├── INDEX.md                   ← K-layer sub-index (auto-maintained)
│   └── K01_<slug>.md, K02_*, ...
├── W_wisdom/
│   ├── INDEX.md                   ← W-layer sub-index (auto-maintained)
│   └── W01_*.md, ...
├── I_information/
│   └── I01_*.md, ...              (no sub-INDEX; grep tags is enough)
└── D_data/
    └── D01_*.md, ...              (no sub-INDEX; grep tags is enough)
```

Why K and W get sub-INDEX but D and I don't:
  - K and W are HIGH-SIGNAL entry points for most queries
  - D and I are SUPPORT layers — usually reached by traversal, not lookup
  - K/W counts stay small (3-15 entries) so sub-INDEX is cheap
  - D/I counts can grow (20-90+) so a sub-INDEX would be expensive to maintain;
    `grep tags:.*<topic> D_data/*.md` is fast enough.


INDEX.md format
=================

Top-level `insights/INDEX.md` (auto-rebuilt by any layer skill on write):

```markdown
# Insight Base — <project>

Last rebuild: <ISO>

## By topic

### <topic-1>
- K03 — "<claim>"                     ← K layer prominent at top
- W01 — "<rec>"                        ← W layer prominent
- I02, I05 — patterns                  ← I layer summarized
- D01-D07 — observations (7)           ← D layer just counted (or batched)

### <topic-2>
...

## By layer

| Layer | Count | Active | Stale | Superseded |
|-------|-------|--------|-------|------------|
| D     | 28    | 28     | 0     | 0          |
| I     | 6     | 6      | 0     | 0          |
| K     | 4     | 3      | 0     | 1          |
| W     | 3     | 3      | 0     | 0          |

## Recently changed (top 10)

| Date       | ID  | Headline / Claim / Rec                          |
|------------|-----|-------------------------------------------------|
| 2026-05-25 | K03 | "FiLM overfits to seen patients..."             |
| 2026-05-23 | W01 | "Run param-matched FiLM re-test..."             |
| ...        | ... | ...                                             |
```

Per Q-a confirmed: each entry line shows **ID + title + 1-line summary**
(the layer's key field: claim/rec/headline).


K_knowledge/INDEX.md format (and W_wisdom/INDEX.md, same shape)
================================================================

```markdown
# K_knowledge Layer Index

Active: 3 | Stale: 0 | Superseded: 1

## Active

| ID  | Claim                                                     | Confidence | Tags                |
|-----|-----------------------------------------------------------|-----------|----------------------|
| K01 | "<one-line claim>"                                        | high      | [lhm, val]           |
| K03 | "FiLM overfits to seen patients..."                       | high      | [film, conditioning] |
| K05 | "<one-line claim>"                                        | medium    | [scaling, train]     |

## Superseded (kept for history)

| ID  | Claim                  | Superseded by | Tags     |
|-----|------------------------|---------------|----------|
| K02 | "<old claim>"          | K05           | [scale]  |
```

W_wisdom/INDEX.md uses `Rec` / `Type` / `Cost` columns instead.


Loading patterns (5 common cases)
==================================

Case 1 — "Does FiLM help on test-od?"  (single-question lookup)
---------------------------------------------------------------

```
Step 1: Read insights/INDEX.md                           (~200 lines)
        Scan By-topic / FiLM section. See K03 listed.
        
Step 2: Read insights/K_knowledge/K03_*.md               (~50 lines)
        frontmatter.claim answers directly.

TOTAL: ~250 lines loaded. Question answered.
```

Case 2 — "What should we do next about FiLM?"  (W-layer lookup)
----------------------------------------------------------------

```
Step 1: Read insights/W_wisdom/INDEX.md                  (~30 lines)
        Filter for tags:[film]. See W01.
        
Step 2: Read insights/W_wisdom/W01_*.md                  (~50 lines)
        frontmatter.rec answers directly.

TOTAL: ~80 lines.
```

Case 3 — "Show me the evidence behind K03"  (deep dive)
--------------------------------------------------------

```
Step 1: Read K03 (already loaded in case 1)
Step 2: Read K03.sources → I02
        Read insights/I_information/I02_*.md                (~60 lines)
Step 3: Read I02.sources → D01, D02, D03
        Read insights/D_data/{D01,D02,D03}_*.md   (~150 lines)

TOTAL: ~250 additional lines on top of case 1.
```

Case 4 — "What FiLM-tagged entries are stale?"  (filter query)
---------------------------------------------------------------

```
Step 1: Read insights/INDEX.md → By status section
        Note no FiLM entries in stale bucket

OR (if INDEX is stale):

Step 1: grep -l "tags:.*film" insights/**/*.md            (filenames)
Step 2: For each, grep frontmatter "status:" field        (status check)

TOTAL: bash 2 ops.
```

Case 5 — Big project, "summarize all knowledge so far"  (full sweep)
---------------------------------------------------------------------

```
Step 1: Read insights/INDEX.md                           (~300 lines)
Step 2: Read insights/K_knowledge/INDEX.md               (~50 lines)
Step 3: Read all active K entries' bodies                (~200 lines × N)

For ~10 K entries: ~2300 lines. Still fast.
```


Maintenance — when to rebuild INDEX
====================================

INDEX files (top + K/W sub) are auto-rebuilt:

  1. After any layer skill writes/updates an entry — same skill rebuilds
     the index(es) affected:
       - data / information writes  → rebuild top INDEX only
       - knowledge writes/updates   → rebuild top + K_knowledge/INDEX
       - wisdom writes/updates      → rebuild top + W_wisdom/INDEX
  2. After explore skill scans (it rebuilds top INDEX as a side effect)
  3. Manual rebuild: `/haipipe-insight rebuild-index` (from umbrella)

INDEX is derived state; the entries themselves are source of truth. If
INDEX disagrees with entries, the rebuild command trusts entries.


Don't do
==========

  - Don't read body before frontmatter
  - Don't full-text grep across body (slow, noisy); use frontmatter tags
  - Don't try to load all entries' bodies at once (>= 50 entries)
  - Don't hand-edit INDEX — it's derived
  - Don't store insights smaller than one paragraph (collapse into
    sibling entry's Notes section instead)


When to scale up (future, not now)
====================================

If insight count climbs > 100 active entries:
  - Introduce `insights/tags/<tag>.md` auto-generated tag sub-indices
  - Consider embedding cache `insights/.embed_cache/<id>.json` for
    semantic retrieval
  - Introduce a dedicated `/haipipe-insight-load <query>` skill that
    wraps the strategy described here

For our typical project scale (30-100 entries), the strategy above is
sufficient.
