# Medical specialty journals: a pack defined by what it does NOT share with JAMA

state: 🟡 PARTIAL · 1 outlet built · 29 exemplars · a plural pack name with a single journal in it
owner: JL
method: state what Diabetes Care requires that the JAMA house style does not, and keep the pack's extension point visible so the plural name stays honest

## Opening

Diabetes Care runs ADA conventions end to end, and almost every one of them contradicts the JAMA portfolio's. So is a society journal just a general-medicine journal with narrower topics?

The abstract headings differ. The highlights box differs. The reference style differs. Even the figure caption separator differs. A paper moved from JAMA Internal Medicine to Diabetes Care changes its entire apparatus while its argument stays put.

**Where this page sits**: it is one pack under `QBv0`, which owns what any pack owes.
This page owns only what is true of `playbook-medical-journals` and its one built outlet.

**Why the pack is named in the plural with one journal in it**: the pack README says so outright, and calls itself the extension point for future specialty clinical journals.
That is the honest reading and it is also a standing risk: a one-outlet pack quietly becomes a one-journal pack when nobody records what the second one would need.

**What this pack is really for**: it is the tree's only worked example of an apparatus delta, which is a different kind of venue knowledge from taste or from section arcs.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the delta list**: it lives in `playbook-medical-journals/README.md` and is cited, never copied.

**Name the pack and the outlet separately every time**: the pack is `playbook-medical-journals`, the outlet is `diabetes-care`, and collapsing them is how the plural name stops meaning anything.

✅ `the pack's one built outlet is Diabetes Care`  ❌ `the Diabetes Care pack`

**Call the difference an apparatus delta, not a style difference**: headings, boxes, and reference formats are checkable; style is not.

## Diagram

**Same argument, different apparatus**: the delta runs top to bottom.

```text
  🏥 JAMA PORTFOLIO              💉 DIABETES CARE (ADA)
  ─────────────────              ──────────────────────
  IMPORTANCE / OBJECTIVE /   ▶   OBJECTIVE / RESEARCH DESIGN
  DESIGN, SETTING, AND           AND METHODS / RESULTS /
  PARTICIPANTS / EXPOSURES /     CONCLUSIONS
  MAIN OUTCOMES / RESULTS /
  CONCLUSIONS AND RELEVANCE

  Key Points box             ▶   Article Highlights
  3 labeled one-liners           4 narrative bullets

  "Methods"                  ▶   "RESEARCH DESIGN AND METHODS"
  numbered Supplements       ▶   "Supplementary Material"
  superscript refs           ▶   Vancouver numbered
  "Figure 1. Caption"        ▶   "Figure 1--Caption"

  📚 near-mandatory citation: ADA Standards of Care
  🔤 domain vocabulary: TIR · TBR · TAR · GMI · MARD · AGP

  📊 29 exemplars · 6 sections · taste ✓ at outlet level
  🧩 the pack is PLURAL and holds ONE journal, on purpose
```

## Content

### 1 · The apparatus delta is the pack's actual content

**Eight differences, each mechanically checkable**: this is the one venue knowledge a conform pass could enforce today.

```text
  ✅ checkable without judgement
     ① abstract headings are ADA, not JAMA
     ② Article Highlights, 4 narrative bullets
     ③ "RESEARCH DESIGN AND METHODS", not "Methods"
     ④ "Supplementary Material", not numbered Supplements
     ⑤ Vancouver numbered references
     ⑥ figure captions use the em-dash separator
     ⑦ ADA Standards of Care cited
     ⑧ CGM vocabulary used as domain terms, not defined

  💥 every one of these fails silently on a retarget from
     the JAMA portfolio, because the argument still reads fine
```

📐 Establishes the delta as a checkable list, which is why this pack is the natural first consumer of a venue-conform pass.

#### 1.1 · An apparatus delta is a third kind of venue knowledge
(distinct from taste, which routes, and from section style, which shapes prose)
Taste says whether to submit. Section style says how long the Introduction runs.
The delta says what the manuscript must physically look like, and it is the only one of the three a machine can verify.

### 2 · What the desk actually wants

**Diabetes technology with clinical outcomes, not device accuracy**: the fit signals are narrower than the pack's general-medicine sibling.

```text
  ✅ CGM / digital diabetes technology validated on clinical
     outcomes ── HbA1c · TIR · hypoglycemia events
  ✅ large registry or claims evidence on management,
     prescribing, or complications
  ✅ ADA Standards of Care alignment ── informs or challenges
  ✅ health equity in diabetes ── access disparities
  ✅ AI/ML for diabetes care with PROSPECTIVE validation in a
     clinical workflow
  ✅ real-world CGM / pump / closed-loop evidence at scale

  🎯 the recurring word is OUTCOMES ── device accuracy alone
     does not clear this desk
```

🎯 Establishes the outlet's demand as outcome-anchored, which is what separates it from a device or ML venue.

#### 2.1 · This is the specialty analogue of npj Digital Medicine's rejection
(the same test, scoped to one disease and one society's guidelines)
npj Digital Medicine rejects accuracy tables with no clinical utility; Diabetes Care rejects device accuracy with no clinical outcome.
A paper failing one usually fails the other, which makes them a routing pair rather than alternatives.

### 3 · The plural name is a promise nobody has to keep

**One outlet, and no record of what a second would need**: the extension point is stated and unspecified.

```text
  📦 playbook-medical-journals/
     └── diabetes-care/     ← the only built outlet

  ⚠️ the README calls the pack "the extension point for future
     specialty clinical journals" and stops there

  💥 nothing records what building the next one requires:
     which files, which conventions to diff against, or how
     an outlet decides its section abbreviation
     ── `diabcare-` was chosen and written down nowhere
```

⚠️ Establishes the gap between a named extension point and a usable one.

## Aims

### A1 · 📐 The apparatus delta is the pack's actual content
- A1.1 · The eight-item delta becomes a checkable list a conform pass can run.
  **Done when:** a Diabetes Care manuscript can be failed on apparatus without a human reading it.

### A2 · 🎯 What the desk actually wants
- A2.1 · The outcome-anchored test is paired with npj Digital Medicine's, so a candidate is routed against both.
  **Done when:** a digital-diabetes paper is scored on the pair rather than on one pack at a time.

### A3 · ⚠️ The plural name is a promise nobody has to keep
- A3.1 · Adding the second specialty outlet has a written recipe.
  **Done when:** the pack states which files a new outlet owes and how its section abbreviation is chosen, which `QBv0` A1.1 also needs.

## States

### A1 · 📐 The apparatus delta is the pack's actual content
- ⬜ A1.1 · Not started. The eight differences are prose bullets in the pack README.

### A2 · 🎯 What the desk actually wants
- ⬜ A2.1 · Not started. The two outlets are scored independently and their overlap is unrecorded.

### A3 · ⚠️ The plural name is a promise nobody has to keep
- ⬜ A3.1 · Not started. One outlet built, no recipe for the next, and `diabcare-` chosen with no rule behind it.

## Files

- `../../paper/venue/playbook-medical-journals/README.md` · the delta list and the extension-point sentence
- `../../paper/venue/playbook-medical-journals/diabetes-care/taste.md` · the outcome-anchored desk test
- `QBv2-jama-portfolio.md` · the house style this pack is defined against
- `QBv0-venue-pack-contract.md` · what any pack owes, and the abbreviation problem this pack instantiates

## Law

A specialty journal's apparatus is part of its venue knowledge, and unlike taste or section style it is mechanically checkable, so a retarget that leaves the apparatus alone has failed even when the prose reads well.
A pack named in the plural owes a written recipe for its next outlet, or the plural is decoration.

## Glossary

- **Apparatus delta**: the checkable differences in headings, boxes, reference format, and caption punctuation between two venue families, distinct from taste and from section style.
- **Article Highlights**: the ADA's four-narrative-bullet box, which replaces the JAMA portfolio's three-labeled-one-liner Key Points.

## Log

260802 · Opened with the QBv group, from `playbook-medical-journals` at `Venue-Paper@fe25a88`.
