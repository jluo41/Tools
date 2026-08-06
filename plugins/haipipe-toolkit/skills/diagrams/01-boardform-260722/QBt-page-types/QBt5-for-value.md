# QBt5 · V01 Drift evidence: what this project must PRODUCE, and who is waiting

state: 🟡 PARTIAL · rung: 2 of 2 questions answered, 1 consumer still unbound
route: inward
owner: JL
method: collect each consumer's question, send it once with the stake stripped, and write the answer back where the asking page can read it

## Opening

What numbers must this project produce about contract drift, who is waiting for each one, and have they come back?

🚫 **Everything under `QA-probe/` is fabricated.** No corpus was counted. This page is a real `for-value` evidence page and its FORMAT is what it teaches; its content is invented.

An evidence page on the inward route asks what this project must PRODUCE, as against the outward route's question of what is already KNOWN. It owns no answer itself: each answer is written once by whoever produced it, the paper keeps one bound record under `QA-probe/`, and this page is the register saying which question went out, who asked, and what came back.

**Why this page provides nothing**: it is a VIEW over N atoms, not an atom. Each `### E<n>` division points at one QA record, and that record is the thing with a product. A display page is the opposite shape: it IS its atom and does declare a `provides:`. Both are pages; only one produces.

**Covered elsewhere**: `QBt3` is the display specimen that consumes E1's answer. `QB6` owns which types exist. The QA record anatomy is `haipipe-board/ref/topic-entry-contract.md`.

## Diagram

**One page, N atoms**: the shape that makes an evidence page different from every other typed page.

```text
  🏦 the executor's own tree          tasks/… · discoveries/…
     the bank lives HERE and stays here. The paper links to it and
     extracts from it. It is never copied in. This group holds none.
              │
              │  `- route: task` + `- bank: <path>`
              ▼
  📋 QA-probe/QBt5-for-value/       one record per question. Same three H2s.
  │    1-drift-counts.md            route: local · no bank, this IS the original
  │    1-drift-counts.data/
  │      └── counts.csv           🎯 the one product downstream may read
  │    2-corpus-size.md             route: task · bank not cloned here
  │    2-corpus-size.data/
  │      ├── size.csv             🎯 product, an extract from that bank's run
  │      └── extracted-from.md    🧾 evidence: where the copy came from
  │         │
  │         │  resolved by ID from the consumer's `needs:` line
  │         ▼
  📄 QBt5-for-value.md            ← this page. A VIEW. No provides:.
       ### E1 · how much drift, by key tenure?   🔗 1-drift-counts
       ### E2 · how large is the corpus?         🔗 2-corpus-size
       ### E0 · incoming
  ─────────────────────────────────────────────────────────────────────
  the BANK holds the answer, wherever it was produced
  the RECORD holds the binding, a digest, and the one extract
  the PAGE holds who asked · none of the three can hold another's half
```

## Content

### E1 · How much does a page drift from its contract, by how long it has declared a type key?

**The binding**: what was asked, which record holds the answer, and what state it is in.

```text
  🏦 bank       banks/QBt5-for-value/1-drift-counts.md    · route: task
  📋 QA-probe   QA-probe/QBt5-for-value/1-drift-counts.md   · state: read
  🎯 product    1-drift-counts.data/counts.csv            · 5 rows
  📐 shape      one row per tenure band: pages · drift_events · CI bounds
```

🔢 Establishes the drift measurement the display unit is built on.

#### consumers

- `QBt3-for-display` · needs it for the render's five bars.
  A-consumer: the bands go on the y axis in tenure order, and the CI columns are carried but not drawn.
  bound ✅ by id, `needs: QA-probe/QBt5-for-value/1-drift-counts` in that page's head.

#### answer digest

Drift falls from 17.3 percent for pages whose type is inferred from a filename to 3.0 percent for pages that have declared a key for thirteen months or more. Two limits travel with it and cap every downstream claim: tenure is not assigned, and page size is not controlled. Anything built on this says association, never reduces.

### E2 · How large is the Fabricated Corpus, and how was the count arrived at?

**The binding**: the same three facts, for an answer whose extract is too large to type.

```text
  🏦 bank       banks/QBt5-for-value/2-corpus-size.md     · route: task
  📋 QA-probe   QA-probe/QBt5-for-value/2-corpus-size.md    · state: read
  🎯 product    2-corpus-size.data/size.csv               · 9 rows, an extract
  🧾 evidence   2-corpus-size.data/extracted-from.md      · where the copy came from
```

📦 Establishes the denominator, and demonstrates the second data shape: a digest in the prose, the rows in an extract stored beside it.

#### consumers

- nobody yet ⬜. The denominator is not drawn on any figure and no sentence cites it.
  An answered question with no consumer is a visible open row, not a silent success: either a consumer appears or E2 is retired.

#### answer digest

400 pages across 9 boards after 62 exclusions, which are policy rather than error. The per-board rows are an extract copied once from the census run; `extracted-from.md` names that run and says what was dropped.

### E0 · incoming

**The standing queue**: questions collected from consumer pages, not yet sent.

```text
  (empty)
```

📥 Establishes that nothing is waiting. A Q-consumer arriving from any page lands here first, gets its stake stripped, and becomes an `### E<n>` division with its own QA record when it goes out.

## Aims

### A1 · 🔢 E1 · drift by key tenure
- A1.1 · The answer is bound to every consumer that needs it.
  **Done when:** each consumer under E1 names the id it binds by, and `unit.py check` resolves it.

### A2 · 📦 E2 · corpus size
- A2.1 · Either a consumer binds E2 or the division is retired.
  **Done when:** the `⬜` under E2's consumers is replaced by a bound consumer or a dated retirement line.
- A2.2 · The extract's origin stays checkable.
  **Done when:** `extracted-from.md` names a run, what it read, and what the extraction dropped.

### A3 · 📥 E0 · the incoming queue
- A3.1 · No Q-consumer sits in E0 longer than one working round.
  **Done when:** E0 is empty or every row in it carries the date it arrived.

## States

- 260806 CC · Page written as the `for-value` specimen, and as the demonstration that an evidence page is a VIEW rather than an atom. It declares no `provides:` on purpose, and `unit.py check` reports it as a view page rather than a missing product.
- 260806 CC · A `banks/` folder was built here and then deleted, on JL's ruling: the bank lives in the executor's own tree and the paper links to it, so copying one into the group repeated the very duplication the design removes. What stays is one record per question, wearing `## Question`, `## Answer`, `## Caveats`, plus `- route:` and, on a non-local route, `- bank:`.
- 260806 CC · The two records carry different routes on purpose. E1 is `route: local`, the answer was produced here and this file is the original. E2 is `route: task` and names a bank that is NOT reachable from this checkout, which is the ordinary state of a paper whose executor tree is not cloned; `check` reports it as `⚠️ not cloned here` rather than as a failure, because an unreachable bank is a fact about the checkout, not a defect in the paper.
- 260806 CC · Two QA records of deliberately different shapes: E1 types its table into the bank's Answer and the probe parses the CSV out of it, E2 leaves its rows with the run and the probe holds an extract with `extracted-from.md` beside it. Those are the two answer shapes, and a specimen showing only the first would teach half the pattern.
- 260806 CC · The strict parse was tested, not assumed, and failed the first test. Changing `48` to `4B` in the bank's table made the extract ship four rows instead of five with exit code 0, which is exactly the silent disagreement the parse claims to prevent. Fixed by locating the fence first and requiring every line inside it to parse or fail; re-tested, the same typo now exits 1 and names the line.
- 260806 CC · E2 is left with no consumer on purpose. An evidence page whose every row is bound teaches nothing about the row that is not, and an unbound answered question is the most common quiet failure on a real evidence page.

### Decision Now
- 📍 E2 has an answer and no consumer. Bind it to something, or retire the division. The page stays 🟡 until one of those happens, which is the behaviour being demonstrated.

## Files

- `QA-probe/QBt5-for-value/`
  The two records, one per question, each with a `.data/` folder holding its one product and any evidence. Open both to see the two routes side by side: E1 is `local` and holds its own answer, E2 is `task` and links to a bank it does not copy.
- `unit.py`
  The resolver. `check` reports which pages are atoms and which are views, and verifies every declared need.
- `QBt3-for-display.md`
  The consumer bound to E1, and the display specimen.
- `../../board/page-types/haipipe-board-page-for-value/SKILL.md`
  The contract this page is an instance of.

## Log

- 260806 · [DRAFT-CC] written as the `for-value` specimen on JL's ruling that the QBt group folder IS the scenario: this page is the evidence page itself rather than a model of one, and its probes sit under the group rather than in a separate sandbox.
