# JAMA portfolio: one house style, three acceptance bars, and a ladder you can fall down on purpose

state: 🟡 PARTIAL · 3 outlets · 39 exemplars · jama-netopen has section norms and zero exemplars
owner: JL
method: state what the three JAMA desks share, what separates them, and why this is the one pack a paper can descend without a rewrite

## Opening

Three JAMA outlets share one manuscript format: same structured abstract, same Key Points box, same reporting expectations. So what is left for them to differ on?

That makes it the one venue family where a rejection has a planned next move. A paper written for JAMA Internal Medicine is already written for JAMA Network Open.

**Where this page sits**: it is one pack under `QBv0`, which owns what any pack owes.
This page owns only what is true of `playbook-jama-portfolio` and its three outlets.

**Why the shared format is the pack's real asset**: elsewhere in this tree a retarget rewrites sections. Here it rewrites the framing sentence and the cover letter.
`QBv1` shows the opposite case, where a retarget adds a section that did not exist.

**What is actually broken here**: `jama-netopen` has no `examples/` folder, and its three exemplars are filed under `jama-flagship/examples/`.
Its own `taste.md` names them and points across, so the knowledge is correct and the shape is wrong: a reader listing the outlet folder concludes it has none.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the outlet delta table**: it lives in `playbook-jama-portfolio/README.md` and is cited, never copied.

**Never call the ladder a fallback**: descending is a planned route, and naming it a fallback hides that the paper was written for both.

✅ `written for JAMA IM, submittable to Network Open unchanged`  ❌ `Network Open as a backup`

**Say JAMA Network Open in full on first use**: `jama-netopen` is the folder name, not the journal's name.

## Diagram

**One format, three bars**: and the descent the shared format pays for.

```text
  📐 SHARED ── structured abstract · Key Points box · JAMA
                superscript refs · numbered Supplements
                       │
     ┌─────────────────┼──────────────────┐
     ▼                 ▼                  ▼
  🏥 JAMA          💊 JAMA IM        🌐 JAMA Netw Open
  practice-        prescribing ·     sound + broad ·
  changing ·       overuse ·         soundness over
  all physicians   health services   novelty · open access

  bar: highest     bar: high         bar: moderate · APC
  23 exemplars     16 exemplars      3 exemplars, filed
                                     under flagship ⚠️

           ━━━━━━━━━━▶ descend ━━━━━━━━━━▶
        the SAME manuscript · reframe, do not rewrite

  🎯 the ProjB lane sits on JAMA IM:
     prescribing variation is exactly its stated middle
```

## Content

### 1 · What the three desks share

**Format, not judgement**: the shared machinery is what makes the descent cheap.

```text
  ✅ structured abstract
     IMPORTANCE / OBJECTIVE / DESIGN, SETTING, AND PARTICIPANTS
     / EXPOSURES / MAIN OUTCOMES / RESULTS
     / CONCLUSIONS AND RELEVANCE
  ✅ Key Points box ── Question / Findings / Meaning
  ✅ JAMA superscript references
  ✅ numbered Supplements

  ── this is the house style, and the pack's
     style-profile.md is written once for all three
```

📐 Establishes the shared format as a pack-level asset, which is why the outlet pages carry only a delta.

#### 1.1 · The shared format is what the medical-journals pack is defined against
(`QBv5` exists because Diabetes Care breaks every line of it)
ADA headings replace the JAMA ones, Article Highlights replace Key Points, Vancouver numbering replaces superscripts.
A paper moving between the two packs changes its apparatus, not its argument.

### 2 · What separates them, and where this repo's work lands

**Three bars on one axis**: how far beyond the finding's own field it has to travel.

```text
  🏥 JAMA          the finding changes GENERAL practice
                   major trials · landmark cohorts

  💊 JAMA IM       internal-medicine practice and policy
                   prescribing variation · overuse ·
                   de-implementation · safety
                   ◀━━ the ProjB lane, named in the README

  🌐 Netw Open     methodologically sound work of broad scope
                   soundness over novelty · open access ·
                   large volume · faster
```

🎯 Establishes JAMA IM as this repo's target outlet, on the pack's own words rather than on preference.

#### 2.1 · Descending is a decision made before writing, not after rejection
(it matters because the reframe is cheap only if the paper never claimed general practice change)
A manuscript that overclaims for JAMA reads as overclaiming at Network Open too.
Writing for the middle bar keeps both doors open; writing for the top bar closes the bottom one.

### 3 · The misfiled exemplars

**Three JNO papers living in the flagship's folder**: the knowledge is right and the shape is wrong.

```text
  🏥 jama-flagship  23 exemplars · 7 sections · taste ✓
  💊 jama-im        16 exemplars · 7 sections · taste ✓
  🌐 jama-netopen    0 in its own folder · 6 sections · taste ✓

  📂 the three JNO exemplars actually on disk, all under
     jama-flagship/examples/ :
       burns-2024-jamanetworkopen-opioid-variation
       jamanetworkopen-2026-antipsychotic-by-clinician-type
       jamanetworkopen-2026-peer-feedback-hospitalist-antibiotic

  ✅ jno-taste.md names all three and points across
  💥 but a reader who lists jama-netopen/ concludes it has
     none, and the flagship's count of 23 is inflated by 3

  ⚠️ and it has 6 sections where its siblings have 7
     ── no jno-letter/, undeclared
```

⚠️ Establishes a filing defect rather than a knowledge gap, which is a cheaper fix and a different one.

## Aims

### A1 · 📐 What the three desks share
- A1.1 · The shared-format claim is checkable rather than asserted.
  **Done when:** a conform pass can verify a JAMA-portfolio manuscript carries all four shared elements.

### A2 · 🎯 What separates them, and where this repo's work lands
- A2.1 · The descent is recorded as a route on the paper that plans it.
  **Done when:** a paper written for JAMA IM records Network Open as a declared next outlet rather than as a conversation.

### A3 · ⚠️ The misfiled exemplars
- A3.1 · The three JNO exemplars move into `jama-netopen/examples/`, or the cross-pointing is declared as the pack's convention.
  **Done when:** listing an outlet folder gives that outlet's true exemplar count.
- A3.2 · The missing `jno-letter/` is either added or declared absent on purpose.
  **Done when:** the six-versus-seven difference is written down rather than discovered by listing.

## States

### A1 · 📐 What the three desks share
- ⬜ A1.1 · Not started. The four shared elements are prose in the pack README.

### A2 · 🎯 What separates them, and where this repo's work lands
- ⬜ A2.1 · Not started. The ProjB lane is named in the pack README and nowhere on a paper page.

### A3 · ⚠️ The misfiled exemplars
- ⬜ A3.1 · Not started. Three JNO papers sit under `jama-flagship/examples/`; `jno-taste.md` names them and points across.
- ⬜ A3.2 · Not started. `jama-flagship` and `jama-im` both carry a letter section; `jama-netopen` does not.

## Files

- `../../paper/venue/playbook-jama-portfolio/README.md` · rewards, outlet delta table, stage maps
- `../../paper/venue/playbook-jama-portfolio/jama-im/taste.md` · the desk this repo's prescribing work is scored on
- `QBv5-medical-journals.md` · the pack defined against this house style
- `QBv0-venue-pack-contract.md` · what any pack owes

## Law

The three JAMA outlets share one manuscript format and differ in bar, so a descent reframes and never rewrites; a paper that overclaims for the top bar has closed the bottom one.
An exemplar is filed under the outlet it exemplifies, because a reader counts an outlet's evidence by listing its folder and not by reading a pointer inside its taste file.

## Glossary

- **Descent**: submitting the same manuscript to a lower-bar outlet in the same portfolio, planned before writing rather than after rejection.
- **Key Points box**: the JAMA-specific Question / Findings / Meaning block, which the medical-specialty pack replaces with Article Highlights.

## Log

260802 · Corrected on the same day it was opened: `jama-netopen` has three exemplars, filed under `jama-flagship/examples/` and named in its own `taste.md`. The defect is filing, not absence.
260802 · Opened with the QBv group, from `playbook-jama-portfolio` at `Venue-Paper@fe25a88`.
