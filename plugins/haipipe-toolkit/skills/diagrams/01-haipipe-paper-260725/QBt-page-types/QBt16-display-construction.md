# QBt16 · Display construction: one bank output, three candidate views

state: 🟡 PARTIAL · three candidates rendered; selection waits on JL
page-type: design
owner: JL
method: hold one proof packet fixed, render three visual forms, compare them against the same criteria, and keep every losing candidate with its reason

## Opening
Which candidate turns one measured bank output into a display that can be checked in five seconds without implying more than the measurement supports?
A display construction is the choice of visual form, such as a table or bar chart, for one fixed proof packet.
The choice is hard because exactness, comparison speed, and scope honesty pull in different directions.
This page decides which of three views should become the worked specimen.

**Who it is for**: A paper worker who has a completed bank result and must decide how to make its useful relation visible before writing narrative or prose.

**What it must do**: Preserve the measured counts, expose the main comparison quickly, and keep the claim at “contract mentions” rather than “contract correctness.”

**What bounds it**: Every candidate reads the same bank file, adds no observations, and carries no paper caption, narrative role, or placement decision.

**Where the candidates live**: `QBt-page-types/display/QBt16-display-construction/candidates/`, generated together by one script from one bank output.

**Covered elsewhere**: `QBt3-for-display.md` owns acceptance of a selected render; `QBt5-for-value.md` owns the Value binding and bank provenance.

## Diagram

**The construction fork**: One proof packet becomes three candidate views before a person selects one.

```text
  🏦 proof packet   QBt5 E1 · counts.csv
          │
          ├──▶ 🅰 ranked bars       comparison first
          ├──▶ 🅱 paths vs lines    relation first
          └──▶ 🅲 audit table       exact lookup first
                          │
                          ▼
                    🧠 JL selection
```

## Content

### 1 · Candidate A · ranked path counts · ⬜ UNDECIDED

**Candidate A**: Contracts are ranked by the number of artifact paths they name.

![](QBt-page-types/display/QBt16-display-construction/candidates/A-ranked-bars.png)

📊 Candidate A makes the distribution and the zero-path contracts visible with the least decoding.

artifact: `QBt-page-types/display/QBt16-display-construction/candidates/A-ranked-bars.png`

**Why it was drafted this way**: The proof question asks how many paths each contract names, so position and bar length encode the measured value directly.

**Fit to the brief**:
P1 fidelity ✅ every bar is one `paths` value from the bank file.
P2 comparison speed ✅ the largest and zero values are visible without reading every label.
P3 scope honesty ✅ the axis says “artifact-path mentions” and makes no correctness claim.
P4 exact lookup 🟡 integer labels are present, but contract line counts are omitted.

**What it bought**: It gives the clearest five-second comparison and keeps exact counts on the bars.

**What it still owes**: JL must decide whether omitting contract length is a useful focus or a lost qualification.

### 2 · Candidate B · paths against contract length · ⬜ UNDECIDED

**Candidate B**: Each contract is positioned by its line count and its number of named artifact paths.

![](QBt-page-types/display/QBt16-display-construction/candidates/B-paths-vs-lines.png)

🔬 Candidate B tests whether path naming merely follows contract length while preserving each contract as a labelled point.

artifact: `QBt-page-types/display/QBt16-display-construction/candidates/B-paths-vs-lines.png`

**Why it was drafted this way**: A long contract has more opportunities to name files, so the second measured column may explain part of the path count.

**Fit to the brief**:
P1 fidelity ✅ both axes come directly from the same bank row.
P2 comparison speed 🟡 the outlier is clear, but ranking the middle contracts takes longer.
P3 scope honesty ✅ the display shows association between two measured counts and claims no cause.
P4 exact lookup ❌ point positions are approximate and several labels compete for attention.

**What it fails**: It answers a new diagnostic question about contract length instead of giving the fastest answer to the original count question.

**Where it might go**: Keep it as a diagnostic candidate if contract-length normalization later matters.

### 3 · Candidate C · exact audit table · ⬜ UNDECIDED

**Candidate C**: Every contract, path count, and line count appears in one lookup table.

![](QBt-page-types/display/QBt16-display-construction/candidates/C-audit-table.png)

📋 Candidate C preserves exact values and source order but asks the reader to perform the comparison.

artifact: `QBt-page-types/display/QBt16-display-construction/candidates/C-audit-table.png`

**Why it was drafted this way**: A table is the safest form when the job is audit and exact retrieval rather than pattern recognition.

**Fit to the brief**:
P1 fidelity ✅ every cell is copied by the generator from the bank row.
P2 comparison speed ❌ the reader must scan and rank ten rows.
P3 scope honesty ✅ the column names preserve the measured units.
P4 exact lookup ✅ both measured values are printed for every contract.

**What it fails**: It is an excellent evidence surface and a weak five-second display because it externalizes no comparison.

**Where it might go**: Keep it as the audit companion to whichever visual candidate wins.

### 4 · SELECTION · pending JL

**The open selection record**: The winner and every loser’s disposition wait on one human ruling.

```text
  🏁 SELECTION · pending · JL
  ─────────────────────────────────────────────────────────
  winner      ⬜ pending
  loser A     ⬜ pending
  loser B     ⬜ pending
  loser C     ⬜ pending
  downstream  ⬜ pending
```

🏁 The candidates are complete enough to choose; no candidate is selected by the builder that drew them.

## Aims

### P · 🎯 The brief’s criteria and selection
- P1 · 🔗 Every visible value comes from the one declared bank output.
  **Done when:** one build reads the bank file directly and every candidate can be regenerated from it.
- P2 · 👁 The main comparison can be read within five seconds.
  **Done when:** a cold reader can identify the largest, smallest, and zero-path contracts without reconstructing the data.
- P3 · 🧱 The display does not outrun the measurement.
  **Done when:** labels and rationale say path mentions, never contract correctness or quality.
- P4 · 🔢 The form preserves enough exactness for its intended job.
  **Done when:** the winner either prints exact values or names the audit companion that does.
- P5 · 🏁 The selection record names the winner, why it won, every loser’s disposition, and a real downstream path.
  **Done when:** JL rules and all five lines in Content 4 are filled.

## States

### Decision Now
- [ ] 🗣 Which candidate should become the Display construction specimen?
      All three use the same bank output; the choice is which reading job the specimen should teach first.
      A · Choose ranked bars, committing the specimen to five-second comparison with exact labels and a separate audit companion.
      B · Choose paths versus lines, committing the specimen to diagnosing whether contract length explains the count.
      C · Choose the audit table, committing the specimen to exact retrieval while leaving pattern recognition to the reader.
      → CC recommends A, because it answers the proof question directly while C can remain its audit companion and B can remain a diagnostic alternative.

### P · 🎯 The brief’s criteria and selection
- ✅ P1 · `source/build.py` reads the QBt5 E1 bank CSV directly and generated all six candidate artifacts in one run.
- 🧠 P2 · The candidates are visible; the five-second reading still needs a cold human comparison.
- ✅ P3 · Every axis, column, and rationale says paths, mentions, contracts, or lines; none claims correctness.
- ✅ P4 · A prints each count, B preserves both measured axes, and C prints every exact bank value.
- 🧠 P5 · The selection record waits on JL; no downstream page has been named.

## Files

- `QBt-page-types/display/QBt16-display-construction/input/proof-packet.md`
  Read the fixed proof question, bank path, scope, and claim ceiling before judging a candidate.
- `QBt-page-types/display/QBt16-display-construction/source/build.py`
  Regenerate A, B, and C together from the same bank output.
- `QBt-page-types/display/QBt16-display-construction/candidates/A-ranked-bars.png`
  Candidate A, optimized for five-second comparison.
- `QBt-page-types/display/QBt16-display-construction/candidates/B-paths-vs-lines.png`
  Candidate B, optimized for diagnosing the relation between paths and contract length.
- `QBt-page-types/display/QBt16-display-construction/candidates/C-audit-table.png`
  Candidate C, optimized for exact lookup and audit.
- `../../board/page-types/haipipe-page-for-design/SKILL.md`
  The contract this page instantiates; the selection and loser-retention rules come from it.

## Log

- 260810 · [DRAFT-CC] Opened one specimen brief against the existing QBt5 E1 bank output, generated three candidate forms from one script, and left selection to JL.
