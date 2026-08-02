# Diabetes Care: the outlet whose requirements a machine could actually check

state: 🟡 PARTIAL · 29 exemplars · 6 sections · taste ✓ · the eight-item apparatus delta is enforced by nothing
owner: JL
method: state what the Diabetes Care desk wants, and record that its apparatus requirements are the one venue knowledge in this tree that is mechanically checkable

## Opening

Every other outlet page in this group ends with a judgement a human has to make. This one does not: eight of this desk's requirements are string-level facts about the manuscript. So why is none of them checked?

**Where this page sits**: it is the only built outlet under `QBv5`, and `QBv5` owns the pack-level facts about `playbook-medical-journals`.
This page owns only what is true of `playbook-medical-journals/diabetes-care/`.

**Why this outlet is the natural first consumer of a conform pass**: `QBv5` records the apparatus delta as a third kind of venue knowledge, distinct from taste and from section style, and the only one a machine can verify.
This is the outlet that instantiates it.

**What the desk itself wants**: outcomes. The recurring word across its six fit signals is a clinical outcome, and device accuracy alone does not clear it.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the section norms**: word budgets live in `diabetes-care/diabcare-<section>/style.md` and are cited, never copied.

**Split the checkable from the judged**: this page's value is the boundary between them, and mixing the two loses it.

✅ `the abstract headings are ADA, not JAMA`  ❌ `the paper should follow ADA conventions`

## Diagram

**Eight string-level requirements, and one judgement**: the rare desk where most of the bar is mechanical.

```text
  🤖 CHECKABLE WITHOUT JUDGEMENT
     ① ADA abstract headings ── OBJECTIVE / RESEARCH DESIGN
        AND METHODS / RESULTS / CONCLUSIONS
     ② Article Highlights, 4 narrative bullets
     ③ "RESEARCH DESIGN AND METHODS", not "Methods"
     ④ "Supplementary Material", not numbered Supplements
     ⑤ Vancouver numbered references
     ⑥ figure captions use the em-dash separator
     ⑦ ADA Standards of Care cited
     ⑧ CGM vocabulary used, not defined
        TIR · TBR · TAR · GMI · MARD · AGP

  🧠 JUDGED
     🎯 "Does this change how we monitor, treat, or think
         about diabetes care for the patient in front of us?"

  ✅ FIT ── the recurring word is OUTCOMES
     CGM / digital diabetes tech validated on HbA1c, TIR,
       hypoglycemia events
     large registry or claims evidence
     ADA Standards of Care alignment
     health equity in diabetes
     AI/ML with PROSPECTIVE clinical-workflow validation
     real-world CGM / pump / closed-loop at scale

  📊 29 exemplars · 6 sections
```

## Content

### 1 · Eight requirements a conform pass could enforce today

**Nothing in the lifecycle looks at any of them**: and all eight fail silently on a retarget from JAMA.

```text
  💥 the silent-failure property
     a paper retargeted from JAMA Internal Medicine keeps its
     argument intact and its apparatus wrong, and it READS
     fine at every stage that checks prose

  🤖 what a check would need
     ── the pinned outlet (already on S-Venue-0)
     ── the eight strings (already in the pack README)
     ── nothing else

  ⚠️ so the gap is not knowledge and not design, it is that
     no one has written the pass
```

🤖 Establishes the check as buildable from artifacts that already exist, which is what makes this outlet the right first consumer.

#### 1.1 · The em-dash separator is the one item worth naming twice
(because this repo's own writing rule forbids em-dashes and this venue requires one)
Diabetes Care figure captions take the form `Figure 1--Caption text.` with an em-dash separator.
A blanket em-dash removal applied to a manuscript pinned here would break a venue requirement, which is exactly why the delta belongs in a check and not in a habit.

### 2 · The desk wants an outcome, and pairs with npj Digital Medicine

**Device accuracy does not clear it**: the same rejection npj Digital Medicine makes, scoped to one disease.

```text
  💻 npj DM        rejects accuracy tables with no clinical
                   utility
  💉 Diabetes Care rejects device accuracy with no clinical
                   outcome

  🔗 so the two are a ROUTING PAIR, not alternatives
     a paper failing one usually fails the other
     ── and a paper clearing one is a live candidate at both

  🔀 what separates them
     💻 npj DM        ── any disease, digital tool angle
     💉 Diabetes Care ── diabetes only, ADA guideline angle
```

🔗 Establishes the pair, and the disease-versus-tool axis that separates them, which is the routing question a digital-diabetes paper actually faces.

## Aims

### A1 · 🤖 Eight requirements a conform pass could enforce today
- A1.1 · The eight-item delta is implemented as a check on a manuscript pinned to this outlet.
  **Done when:** a Diabetes Care manuscript can be failed on apparatus with no human reading it.
- A1.2 · The em-dash caption requirement is exempted from any blanket em-dash rule.
  **Done when:** a repo-wide em-dash pass cannot break a caption in a paper pinned here.

### A2 · 🔗 The desk wants an outcome, and pairs with npj Digital Medicine
- A2.1 · A digital-diabetes candidate is routed on the disease-versus-tool axis.
  **Done when:** the choice between the two outlets is made on a stated question rather than by preference.

## States

### A1 · 🤖 Eight requirements a conform pass could enforce today
- ⬜ A1.1 · Not started. All eight are prose bullets in the pack README.
- ⬜ A1.2 · Not started. No exemption exists, and the conflict is recorded here for the first time.

### A2 · 🔗 The desk wants an outcome, and pairs with npj Digital Medicine
- ⬜ A2.1 · Not started. Both taste files exist and nothing compares them.

## Files

- `../../paper/venue/playbook-medical-journals/diabetes-care/taste.md` · the desk signals and the one-sentence test
- `../../paper/venue/playbook-medical-journals/README.md` · the eight-item apparatus delta against the JAMA house style
- `QBv3a-npj-digital-medicine.md` · the outlet this one pairs with
- `QBv5-medical-journals.md` · the pack this outlet is the whole of

## Law

Eight of this desk's requirements are string-level facts about the manuscript, so this is the one outlet in the tree that can be failed by a machine, and every one of them fails silently on a retarget from the JAMA portfolio.
This venue requires an em-dash caption separator, so a blanket em-dash rule must exempt a manuscript pinned here.

## Glossary

- **Apparatus delta**: the checkable differences in headings, boxes, reference format, and caption punctuation between two venue families.
- **Routing pair**: two outlets whose rejections overlap so closely that a candidate clearing one is live at both, here Diabetes Care and npj Digital Medicine.

## Log

260802 · Opened with the QBv outlet pages, from `playbook-medical-journals/diabetes-care` at `Venue-Paper@fe25a88`.
