# Nature portfolio: five journals that reject the same paper for five different reasons

state: 🟡 PARTIAL · the reference shape at 5 outlets and 100 exemplars; the routing table is read by hand and recorded nowhere
owner: JL
method: state what each of the five Nature desks calls a contribution, and record the two structural features this pack has that no other pack in the tree does

## Opening

All five Nature journals would plausibly publish something adjacent to a digital-health paper. So which one is it actually for?

NMI rejects it for being an incremental architecture tweak. Nature Communications rejects it for being too narrow. Nature Medicine rejects it for having no prospective validation. npj Digital Medicine rejects it for being a benchmark with no clinical question. Nature Human Behaviour rejects it for a WEIRD-only sample sold as universal.

**Where this page sits**: it is one pack under `QBv0`, which owns what any pack owes.
This page owns only what is true of `playbook-nature-portfolio` and its five outlets.

**Why this pack routes rather than ranks**: its README is the only one in the tree with a dedicated `## Routing: which journal for which paper` section and a fit-versus-desk-reject table read row by row.
The five desk-reject signals are more discriminating than the five fit signals, because a paper usually fits several and is rejected by exactly one.

**What this repo already published here**: `Paper-MapPhyTrait-npjDM2025` went to npj Digital Medicine, so this pack holds the only outlet in the tree with a shipped paper behind it.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the fit table**: it lives in `playbook-nature-portfolio/README.md` and is cited, never copied.

**Route on the desk-reject column, not the fit column**: fit is where a paper looks plausible everywhere; rejection is where it is decided.

✅ `Nature Medicine desk-rejects retrospective single-center AI`  ❌ `Nature Medicine likes translational work`

**Say npj Digital Medicine in full on first use**: `npj-digital-medicine` is the folder, `npjdm-` is the section prefix, and neither is the journal's name.

## Diagram

**Five desks, one paper**: and five different reasons to reject it.

```text
                📄 one digital-health paper
                          │
   ┌──────────┬───────────┼───────────┬────────────┐
   ▼          ▼           ▼           ▼            ▼
 🤖 NMI    🌍 Nat Comms 🏥 Nat Med  💻 npj DM   🧠 NHB
 novel     cross-       translat-   tool        large-N
 method +  disciplinary ional +     validated   behavioral +
 impact    reach        prospective on clinical mechanism
                        validation  outcomes

 ❌ rejects ❌ rejects   ❌ rejects  ❌ rejects   ❌ rejects
 incremental too narrow  retrospec- benchmark   WEIRD-only
 tweak                   tive       with no     sold as
                         single-    clinical    universal
                         center AI  question

 📊 21        16          25         21          17  exemplars

 🧩 all five own a  <abbr>-related-work/  section
    ── unique to this pack: no JAMA, UTD-IS, PNAS, or
       Diabetes Care outlet has one
 🔧 npj DM alone owns  tech-check.md
    ── the only technical gate in the whole venue tree
 🏆 and the only outlet with a SHIPPED paper behind it:
    Paper-MapPhyTrait-npjDM2025
```

## Content

### 1 · Routing on the rejection, not the fit

**Five fit signals overlap; five desk-reject signals do not**: the discriminating column is the second one.

```text
  🤖 NMI       ❌ incremental architecture tweak · off-the-shelf
                  ML where only the dataset is new · unvalidated
                  "human-level" claims
  🌍 Nat Comms ❌ single-subfield incremental advance · method
                  with no scientific finding · scope too narrow
  🏥 Nat Med   ❌ retrospective single-center AI with no external
                  validation · computation with no clinical
                  grounding
  💻 npj DM    ❌ pure ML benchmark with no clinical question ·
                  N<100 pilot with no validation path ·
                  accuracy tables with no clinical utility
  🧠 NHB       ❌ WEIRD-only sample sold as universal · N<200 lab
                  study with no pre-registration · descriptive
                  social-media analysis with no mechanism
```

🎯 Establishes the routing instrument as the rejection column, which is the one a candidate paper usually matches exactly once.

#### 1.1 · Two of the five rejections are about validation design, not topic
(so they are decided at the task layer, long before venue is picked)
Nature Medicine's and npj Digital Medicine's desk-rejects both turn on whether validation exists and against what.
A paper cannot acquire prospective validation during a retarget, which puts these two outlets upstream of the venue stage rather than downstream of it.

### 2 · The two structural features this pack does not share

**A pack-wide related-work section, and one outlet's technical gate**: the first is a retarget cost, the second is a file kind nothing else in the tree has.

```text
  📚 <abbr>-related-work/     ── ALL FIVE outlets
     a manuscript section between Introduction and Methods.
     Every outlet in every OTHER pack folds related work into
     the Introduction.
     💥 into this pack: gain a section
        out of this pack: dissolve one

  🔧 tech-check.md            ── npj DM ONLY
     the only file of its kind in the whole venue tree.
     Not taste, not style: a technical gate.
```

🧩 Establishes the related-work section as a pack-wide retarget cost, the same class `QBv1` records for the UTD-IS theory section, and `tech-check.md` as a one-outlet exception.

#### 2.1 · The one shipped paper in this repo sits on the outlet carrying both
(which is why the shape is worth writing down rather than rediscovering)
`Paper-MapPhyTrait-npjDM2025` was written into this outlet and published.
Its section layout is therefore evidence, and it is the closest thing this repo has to a worked example of a venue pack being satisfied.

### 3 · What is stocked

**A hundred exemplars, evenly spread**: this is the best-populated pack in the tree and the only one with no shape gap.

```text
  🤖 NMI            21 exemplars · 7 sections · taste ✓
  🌍 Nat Comms      16 exemplars · 7 sections · taste ✓
  🏥 Nat Medicine   25 exemplars · 7 sections · taste ✓
  💻 npj DM         21 exemplars · 7 sections · taste ✓ + tech-check
  🧠 NHB            17 exemplars · 7 sections · taste ✓

  ✅ no missing taste · no empty examples/ · no section count
     that disagrees with its siblings
```

📊 Establishes this pack as the reference shape the other six are measured against.

## Aims

### A1 · 🎯 Routing on the rejection, not the fit
- A1.1 · The venue stage scores a Nature-portfolio candidate on the desk-reject column and records which rows it survived.
  **Done when:** a 2a-venue run naming a Nature outlet cites the rejection rows it cleared, not only the fit row it matched.

### A2 · 🧩 The two structural features unique to npj DM
- A2.1 · The related-work section and `tech-check.md` are declared as retarget costs where a retarget is decided.
  **Done when:** moving a paper into or out of npj DM surfaces both before pitch is rewritten.

### A3 · 📊 What is stocked
- A3.1 · This pack is named the reference shape in `QBv0`'s pack contract.
  **Done when:** the pack-shape rule in `QBv0` cites a pack that actually satisfies it.

## States

### A1 · 🎯 Routing on the rejection, not the fit
- ⬜ A1.1 · Not started. The table is read by hand and no run records which rows it cleared.

### A2 · 🧩 The two structural features unique to npj DM
- ⬜ A2.1 · Not started. Both are visible only by listing the outlet folder.

### A3 · 📊 What is stocked
- ⬜ A3.1 · Not started. `QBv0` states the shape abstractly and names no pack that meets it.

## Files

- `../../paper/venue/playbook-nature-portfolio/README.md` · the five journals, the routing section, the fit-versus-reject table
- `../../paper/venue/playbook-nature-portfolio/npj-digital-medicine/tech-check.md` · the only technical gate in the venue tree
- `Paper-MapPhyTrait-npjDM2025` · the shipped paper behind this pack, in the SPACE repo's `examples/ProjA-PhyTraitLandScape/`
- `QBv0-venue-pack-contract.md` · what any pack owes

## Law

A Nature-portfolio candidate is routed by the desk-reject signal it fails, not the fit signal it matches, because a plausible paper matches several fits and fails exactly one desk.
Two of the five rejections turn on validation design, which cannot be acquired during a retarget, so those outlets are decided upstream of the venue stage.

## Glossary

- **Desk-reject signal**: the property that stops a paper before review at one specific outlet, recorded per journal in the pack README.
- **tech-check**: npj Digital Medicine's technical gate file, unique in the venue tree, distinct from taste and from section style.
- **Related-work section**: a standalone manuscript section between Introduction and Methods, carried by all five Nature outlets and by no outlet in any other pack.

## Log

260802 · Corrected on the same day it was opened: `<abbr>-related-work/` is carried by all five outlets, not by npj Digital Medicine alone. Only `tech-check.md` is a one-outlet file.
260802 · Opened with the QBv group, from `playbook-nature-portfolio` at `Venue-Paper@fe25a88`.
