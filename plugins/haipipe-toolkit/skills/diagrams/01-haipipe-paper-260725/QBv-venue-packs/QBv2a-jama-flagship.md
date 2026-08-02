# JAMA: the desk whose test is what a clinician does on Monday

state: 🟡 PARTIAL · 20 exemplars · 7 sections · taste ✓ · its exemplar count is inflated by 3 misfiled JNO papers
owner: JL
method: state JAMA's own desk signals and one-sentence test, and record that this outlet's examples folder is also holding its sibling's

## Opening

JAMA's test is the shortest in the tree and the hardest to fake: will a practising clinician change what they do Monday morning because of this result? Everything else the desk asks for is downstream of that. So which papers actually clear it?

**Where this page sits**: it is one outlet under `QBv2`, which owns the JAMA house format the three outlets share.
This page owns only what is true of `playbook-jama-portfolio/jama-flagship/`.

**Why this outlet is the ceiling and rarely the target**: the bar is practice change at national scale, and the portfolio's own delta table says so.
For this repo's prescribing work, `QBv2b` records the outlet the pack actually names.

**What is wrong with its folder**: `examples/` holds 23 files, three of which are JAMA Network Open papers filed here rather than under `jama-netopen/`.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the section norms**: word budgets live in `jama-flagship/jama-<section>/style.md` and are cited, never copied.

**State the bar as an action, not as a quality**: this desk's own test is behavioural and paraphrasing it as importance loses the test.

✅ `will a clinician change what they do Monday`  ❌ `is the finding important`

## Diagram

**One question, asked of the reader's next week**: and five ways to fail it.

```text
  🎯 THE TEST
     "Will a practicing clinician change what they do Monday
      morning because of this result?"

  ✅ WHAT CLEARS IT
     a question affecting millions, answered definitively
       ── RCT · large cohort · meta-analysis
     patient-centered outcomes ── mortality · morbidity ·
       quality of life · functional status
     public-health significance in the FIRST paragraph
     STROBE / CONSORT / PRISMA compliance, pre-registered
       where possible
     policy relevance ── guidelines · CMS decisions
     a clean Key Points box: Question / Findings / Meaning,
       one sentence each

  ❌ DESK-REJECT
     surrogate endpoints with no clinical outcome
     single-center with small N where large registries exist
     an incremental drug trial with no practice implication
     an AI/ML method paper with no patient-outcome impact
     overclaimed generalizability from a convenience sample

  📊 23 files in examples/ ── 3 of them are JNO papers ⚠️
```

## Content

### 1 · What the Monday test actually excludes

**Two of the five rejections are about endpoints, not scale**: a large study can fail this desk on what it measured.

```text
  🚫 surrogate endpoints alone
     ── the study can be enormous and still not answer the
        question the test asks

  🚫 an AI/ML method paper with no demonstrated impact on
     patient outcomes
     ── the nearest failure mode to this repo's work, and the
        same one npj Digital Medicine names at QBv3a

  💡 so the binding constraint is the OUTCOME VARIABLE, which
     is fixed at the task layer and not at venue
```

🎯 Establishes the outcome variable as the gate, which places this outlet upstream of the venue stage like ISR and Nature Medicine.

#### 1.1 · The first paragraph carries a stated requirement
(which makes it one of the few section-level rules a desk names in its taste file)
The signals ask for public-health significance in the first paragraph, not somewhere in the Introduction.
That is a placement rule from the desk itself, and `jama-introduction/style.md` is where it has to be honoured.

### 2 · The three misfiled JNO papers

**A count that is wrong in two directions at once**: this folder is over by three and its sibling is empty.

```text
  📂 jama-flagship/examples/
     burns-2024-jamanetworkopen-opioid-variation
     jamanetworkopen-2026-antipsychotic-by-clinician-type
     jamanetworkopen-2026-peer-feedback-hospitalist-antibiotic

  ✅ jno-taste.md names all three and points here on purpose
  💥 but this outlet's style.md numbers were extracted from a
     folder containing another outlet's papers

  ⚠️ so the defect is not only filing: a JAMA word budget may
     rest partly on JNO prose
```

⚠️ Establishes the misfiling as a possible contamination of this outlet's own norms, not only a navigation problem.

## Aims

### A1 · 🎯 What the Monday test actually excludes
- A1.1 · The outcome-variable gate is scored before venue rather than at submission.
  **Done when:** a paper with only surrogate endpoints is not shortlisted for this outlet.

### A2 · ⚠️ The three misfiled JNO papers
- A2.1 · The three JNO papers move to `jama-netopen/examples/`.
  **Done when:** this folder holds only JAMA flagship papers and both counts are true.
- A2.2 · The flagship section norms are re-checked against the corrected folder.
  **Done when:** no `jama-<section>/style.md` number rests on a JNO exemplar.

## States

### A1 · 🎯 What the Monday test actually excludes
- ⬜ A1.1 · Not started. The test is prose in `jama-flagship/taste.md`.

### A2 · ⚠️ The three misfiled JNO papers
- ⬜ A2.1 · Not started. Three files, named in the sibling's taste file, sitting here.
- ⬜ A2.2 · Not started, and dependent on A2.1.

## Files

- `../../paper/venue/playbook-jama-portfolio/jama-flagship/taste.md` · the desk signals and the Monday test
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/jama-introduction/style.md` · where the first-paragraph rule has to land
- `QBv2c-jama-netopen.md` · the outlet whose exemplars are in this folder
- `QBv2-jama-portfolio.md` · the family this outlet belongs to

<!-- exemplars:begin -->

📚 **Exemplars** · 20 papers on disk, regenerated by `_tools/sync-exemplars.py`

- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/article2338266-2015-jama-medical-marijuana-for-treatment-of-chronic-pain-and-other-medical-and-psychiatric.pdf`
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/article2503508-2016-jama-cdc-guideline-for-prescribing-opioids-for-chronic-pain-united-states-2016.pdf`
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/bronfort-2025-jama-spinal-manipulation-and-clinician-supported-biopsychosocial-self-management-for-ac.pdf` · Bronfort 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/burns-2024-jamanetworkopen-opioid-variation.md` · Burns 2024
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/cantor-2025-jama-physician-medicare-participation.pdf` · Cantor 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/cashin-2026-jama-low-back-pain-a-review.pdf` · Cashin 2026
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/cipriani-2026-jama-decision-support-antidepressant.pdf` · Cipriani 2026
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/dijk-2025-jama-clinical-decision-support-imaging.pdf` · Dijk 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/holste-2025-jama-ai-echocardiography-deep-learning.pdf` · Holste 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/jamanetworkopen-2026-antipsychotic-by-clinician-type.md` · Jamanetworkopen 2026 · +xml
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/jamanetworkopen-2026-peer-feedback-hospitalist-antibiotic.md` · Jamanetworkopen 2026 · +xml
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/krebs-2018-jama-effect-of-opioid-vs-nonopioid-medications-on-pain-related-function-in-patients.pdf` · Krebs 2018
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/kroenke-2014-jama-telecare-collaborative-management-chronic-pain-primary-care.pdf` · Kroenke 2014
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/mathioudakis-2025-jama-ai-lifestyle-diabetes-prevention.pdf` · Mathioudakis 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/miller-2025-jama-digital-health-lung-cancer-screening.pdf` · Miller 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/nguyen-2025-jama-payments-physicians-ai-devices.pdf` · Nguyen 2025
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/peachman-2016-jama-opioid-guidelines-mindfulness-pain-relief.pdf` · Peachman 2016
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/peachman-2022-jama-will-the-new-cdc-opioid-prescribing-guidelines-help-correct-the-course-in.pdf` · Peachman 2022
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/rotenstein-2026-jama-ai-scribes-clinician-time.pdf` · Rotenstein 2026
- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/yang-2026-jama-cns-prescribing-older-adults-letter.pdf` · Yang 2026

- `../../paper/venue/playbook-jama-portfolio/jama-flagship/examples/JAMA_EXPANSION_RESULTS.md` · the pack's own manifest, not an exemplar

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · 7 declared in `stages/section-kinds.yml`, regenerated by `_tools/sync-exemplars.py`

Each kind is one unit `section-edit` runs on, and one page it writes: 6 numbered `S-Main-<n>` pages plus `S-Appendix-<letter>`.

- `abstract` · `S-Main-<n>`
- `introduction` · `S-Main-<n>`
- `methods` · `S-Main-<n>`
- `results` · `S-Main-<n>`
- `discussion` · `S-Main-<n>`
- `appendix` · `S-Appendix-<letter>`
- `letter` · `S-Main-<n>`

<!-- kinds:end -->

## Law

This desk's bar is a change in clinical action, so the binding constraint is the outcome variable, which is fixed at the task layer and cannot be acquired during a retarget.
An exemplar is filed under the outlet it exemplifies, because a section norm extracted from a folder inherits whatever is in it.

## Glossary

- **Monday test**: this desk's own one-sentence bar, asking whether a practising clinician changes what they do because of the result.
- **Surrogate endpoint**: a measured proxy standing in for a clinical outcome, sufficient for many venues and named as a desk-reject here.

## Log

260802 · Opened with the QBv outlet pages, from `playbook-jama-portfolio/jama-flagship` at `Venue-Paper@fe25a88`.
