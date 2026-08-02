# Grant: a venue with no journal, where the reviewer buys a plan rather than a finding

state: 🟡 PARTIAL · 8 agencies as README delta tables · no outlet tree · no exemplars
owner: JL
method: state what makes a grant a venue at all, record the agency deltas as the pack's actual unit, and name the two shape rules this pack breaks on purpose

## Opening

This system calls a venue whatever fixes the structure and states the acceptance test. An agency does both harder than any journal: page limits are enforced, section names are prescribed, and the review criteria are published in advance. So why would a funding agency not be in a tree of journals?

What changes is the tense. A journal desk asks what you found. A review panel asks what you will do, why you are the one to do it, and whether the plan is feasible. Everything the paper system knows how to argue from evidence has to be re-aimed at a plan.

**Where this page sits**: it is one pack under `QBv0`, which owns what any pack owes.
This page owns only what is true of `playbook-grant`.

**Why this pack has no outlet tree**: agencies do not have sections in the way journals do; they have prescribed backbones that differ per agency.
The pack encodes them as delta tables inside `README.md`, and `stages/section-kinds.yml` declares this pack blueprint-only by design, which is where a stage reader meets the exception.

**What the pack is missing that every journal pack has**: exemplars.
Eight agencies, no funded proposals on disk, and no `style.md` extracted from anything.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the agency tables**: they live in `playbook-grant/README.md` and are cited, never copied.

**Keep the tense difference in front**: it is the whole reason a paper cannot be reformatted into a proposal.

✅ `the panel buys a plan`  ❌ `the panel reviews the work`

**Name the agency programme, not just the agency**: NSFC General Program and NSFC Young Scientists are two different backbones and the pack lists them separately.

## Diagram

**Eight agencies, one shared tense**: and a backbone that differs for every one of them.

```text
  🗣 THE TENSE ── a panel buys a PLAN, not a finding
     feasibility · track record · fit to the call
                       │
  📐 THE BACKBONE ── prescribed, and different per agency
  ┌────────────────────────────────────────────────────────┐
  │ NSF     Project Summary (1p: Overview / Intellectual   │
  │         Merit / Broader Impacts) + Project Description │
  │         (15p, Aim-based) + Results from Prior Support  │
  │ NSFC    Rationale / Research Content / Objectives /    │
  │         Plan / Feasibility / Novelty / Expected         │
  │         Outcomes / Prior Accumulation                   │
  │         General Program and Young Scientists differ     │
  │         in weighting                                    │
  │ ERC     Extended Synopsis (5p) + Part B2 (14p) with a  │
  │         WP / deliverables / milestones table           │
  │ KAKENHI Summary / Objective / Plan and Methods /       │
  │         Preparation + an explicit year-by-year plan    │
  │ DFG · SNSF · ARC · NWO · GENERIC                       │
  └────────────────────────────────────────────────────────┘

  🔍 THE LENS ── published in advance, per agency
     NSF: Intellectual Merit · Broader Impacts
     NSFC: scientific significance · novelty · feasibility
           · team
     ERC: Ground-breaking nature · Methodology · PI track record

  🚫 no outlet tree · 🚫 no exemplars · taste.md at FAMILY level
```

## Content

### 1 · Why a grant is a venue

**It fixes structure and publishes its acceptance test**: that is the whole definition this tree uses.

```text
  a VENUE, in this system, is whatever
     ① prescribes the structure           ── agencies do, harder
     ② states what will be accepted        ── published criteria
     ③ has a desk that says no first       ── eligibility + fit

  💡 an agency is a STRICTER venue than a journal on ① and ②
     and the pack's stage maps are the same four:
     ->Claims  ->Display  ->Minimap  ->Write/Edit
```

🎯 Establishes the grant as a first-class venue rather than a courtesy inclusion, on the tree's own definition.

#### 1.1 · The four stage maps survive the change of tense
(which is why this pack can sit in the same tree without a second grammar)
Claims become aims, displays become the figures a panel skims, the minimap becomes the work plan.
The lifecycle stages do not change; what they produce is aimed at a plan instead of a result.

### 2 · The agency delta is the pack's unit

**No outlet folder, so the table IS the outlet**: eight backbones and eight review lenses, in one README.

```text
  📄 README.md carries what a journal pack splits into folders
     ── the backbone table  ≈ the section tree
     ── the review-lens table ≈ taste.md

  ⚠️ so a reader who knows the journal pack shape looks for
     playbook-grant/<agency>/ and finds nothing

  ⚠️ and GENERIC is a real row: user-supplied sections, page
     limits, and criteria ── the pack's escape hatch for an
     agency it does not encode
```

📐 Establishes the delta table as the pack's real unit, and the missing outlet folder as a shape the reader has to be told about.

#### 2.1 · The exception is declared inside the thing it excepts
(so only a reader already in the pack ever learns the pack is shaped differently)
`venue/README.md` says grant and patent are not journals and encode deltas in `README.md` instead of `<journal>/` trees.
A stage resolving `packs:` never opens that file, which is what `QBv0` A3.3 has to fix.

### 3 · No exemplars, anywhere

**Eight agencies and nothing funded on disk**: the pack has rewards and no evidence.

```text
  📚 every journal pack   exemplar PDFs + INDEX.md per outlet
     ── the source every style.md number is extracted from

  📭 playbook-grant       0 exemplars
     ── the backbones are correct and the LANGUAGE has no
        source: no funded NSF Project Description, no NSFC
        Rationale section, nothing to imitate

  💥 and the README calls Write/Edit "the main purpose"
     ── the pack's stated main purpose is the one it cannot
        currently serve
```

⚠️ Establishes the gap between the pack's stated purpose and what is on disk to serve it.

## Aims

### A1 · 🎯 Why a grant is a venue
- A1.1 · The tense change is stated where a paper is converted into a proposal.
  **Done when:** converting a claim ledger into aims names what each claim becomes, rather than reusing it.

### A2 · 📐 The agency delta is the pack's unit
- A2.1 · The blueprint-only declaration and this pack's own contents cannot disagree.
  **Done when:** adding a per-section pack here fails until `section-kinds.yml` stops calling it blueprint-only.

### A3 · ⚠️ No exemplars, anywhere
- A3.1 · At least one funded proposal per agency this repo actually targets lands in the pack.
  **Done when:** the language guidance the README calls its main purpose has a source on disk.

## States

### A1 · 🎯 Why a grant is a venue
- ⬜ A1.1 · Not started. The stage maps exist; the claim-to-aim conversion is unwritten.

### A2 · 📐 The agency delta is the pack's unit
- ✅ A2.1 · Resolved on inspection, and replaced. `stages/section-kinds.yml` names grant and patent blueprint-only by design, in a file both venue and section-edit read.

### A3 · ⚠️ No exemplars, anywhere
- ⬜ A3.1 · Not started. Zero exemplars against 21 to 29 for each populated journal outlet.

## Files

- `../../paper/venue/playbook-grant/README.md` · the agency backbone and review-lens tables, plus the four stage maps
- `../../paper/venue/playbook-grant/taste.md` · the panel's test, at family level
- `QBv7-patent.md` · the other non-journal pack, same shape exception
- `QBv0-venue-pack-contract.md` · what any pack owes, and the exception this pack instantiates

<!-- exemplars:begin -->

📚 **Exemplars** · 0 papers on disk, regenerated by `_tools/sync-exemplars.py`

Filed at FAMILY level under `../../paper/venue/playbook-grant/examples/`, not under the outlet (QBv0 A3.1).

- none. No `examples/` folder under `../../paper/venue/playbook-grant/`, so this outlet states section norms with no exemplar behind them.

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · none declared in `stages/section-kinds.yml`, so this venue is blueprint-only: the S-Venue-0 blueprint is binding and no per-section pack is resolved.

<!-- kinds:end -->

## Law

A grant is a venue because it prescribes structure and publishes its acceptance test, and it is a stricter one than any journal on both counts.
A panel buys a plan, so every lifecycle artifact is re-aimed from what was found to what will be done, and a claim converted into an aim without changing tense has not been converted.

## Glossary

- **Backbone**: an agency's prescribed section sequence, which plays the role a journal's section tree plays in the other packs.
- **Review lens**: the published criteria a panel scores against, which plays the role `taste.md` plays for a journal.
- **GENERIC**: the pack's escape-hatch row, for an agency whose sections, page limits, and criteria the user supplies.

## Log

260802 · Corrected against `stages/section-kinds.yml`, found while answering how a Content division becomes an S-Main page. That file already carries the glob rule for the section abbreviation, an outlet-to-kinds map measured on disk, the `theory-model` alias, and the blueprint-only declaration for grant and patent. Four claims on this group that something was undeclared were wrong, and the Aims they carried are replaced by drift guards.
260802 · Opened with the QBv group, from `playbook-grant` at `Venue-Paper@fe25a88`.
