# QBt17 · Display boundary: one topic, how many Displays?

state: 🟡 PARTIAL · three architectures instantiated; boundary ruling waits on JL
page-type: design
owner: JL
method: hold the L2 and L5 evidence fixed, vary only the semantic boundary, then select the smallest independently acceptable reader message

## Opening
When one regression topic has binary and continuous exposure results, should it become one multi-panel Display or two related Displays?
A Display is not defined by one image file, one table body, or one analysis topic.
Its boundary must follow the message a reader can understand and a person can accept independently.
This page tests that boundary on the live L2 and L5 main-regression case before any skill is changed.

**Who it is for**: A display worker deciding whether related evidence belongs in panels of one composition or in sibling Displays.

**What it must do**: Separate topic, message, panel, render, and placement so file count never decides the argument's unit.

**What bounds it**: The existing L2 and L5 values, takeaways, and placements stay fixed; this page changes only how they are grouped.

**Covered elsewhere**: `QBt16-display-construction.md` compares visual forms for one fixed message; this page decides how many messages and acceptance units exist before a form is selected.

## Diagram

**The five levels**: Topic groups the work, while Display is the smallest independently acceptable reader message.

```text
  TOPIC                    main regression
    │
    ├── DISPLAY            one Reader Takeaway + claim job + placement
    │     ├── PANEL        one complementary view or sub-proof
    │     └── PANEL        another view needed for the same takeaway
    │
    ├── CANDIDATES         mutually exclusive compositions of that Display
    │
    └── ARTIFACTS          PDF · PNG · TEX are formats, not new Displays
```

## Content

### 1 · Fixed proof inventory

**The evidence held constant**: L2 and L5 share a regression topic but currently perform different reader jobs.

```text
  E1 · trait_l2 · binary threshold exposure
       takeaway   crossing 0.75 is associated with more MME and
                  higher probabilities of high-dose flags
       claim job  C1 headline + C2 consequence
       placement  Results §6, main text

  E2 · trait_l5 · continuous exposure
       takeaway   the beyond-rating association survives a continuous form
       claim job  C1 functional-form robustness
       placement  Appendix E

  naming note     trait_l5 is continuous; trait_l5_buc is the five-bucket form
```

📦 The shared topic does not erase the different takeaways, claim roles, or placements.

### 2 · Candidate A · one composite Display

**Architecture A**: L2 and L5 become two panels under one comparative Reader Takeaway.

```text
  D1 · robustness across exposure operationalizations
  RT · The association appears under both threshold and continuous coding.

       ┌───────────────────── one float ─────────────────────┐
       │ Panel A · L2 primary threshold result              │
       │ Panel B · L5 continuous-form result                │
       └─────────────────────────────────────────────────────┘
       one caption · one placement · one acceptance decision
```

🧩 This is valid only if the paper wants the comparison itself to be the message and both panels must be read together.

**What it buys**: The functional-form comparison becomes visible in one place.

**What it costs here**: The current L2 panel carries headline outcomes while L5 carries only a specification ladder, so the comparison is asymmetric; it also pulls appendix evidence into the main-text placement or pushes headline evidence out.

### 3 · Candidate B · one family, two Displays

**Architecture B**: One topic owns two sibling Displays, each with its own takeaway, composition, placement, and acceptance.

```text
  T-main-regression
       │
       ├── D1 · L2 primary result
       │      RT         threshold exposure predicts MME + high-dose flags
       │      panels     MME · flags · logit translation
       │      placement  Results §6
       │      gate       accepted independently
       │
       └── D2 · L5 functional-form robustness
              RT         beyond-rating result survives continuous coding
              panels     SPEC1-SPEC5 ladder
              placement  Appendix E
              gate       accepted independently
```

🌳 Candidate B keeps topical kinship without pretending the two units perform one reader job.

**What it buys**: Narrative may select, place, revise, or reject either message without silently changing the other.

**What it costs**: The topic needs a family record so D1 and D2 do not look unrelated or get regenerated inconsistently.

### 4 · Candidate C · two unrelated Displays

**Architecture C**: L2 and L5 are treated as independent units with no shared topic record.

```text
  D1 · L2 main result              D2 · L5 robustness
  RT · primary association        RT · continuous-form check
  placement · Results §6          placement · Appendix E

                  no family link
                  no shared proof inventory
                  no coordinated fragility rule
```

✂️ Candidate C preserves independent acceptance but loses the fact that both are alternate operationalizations of the same construct.

**What it buys**: The simplest formal unit folders.

**What it fails**: A change to the exposure definition can update one Display while leaving its sibling stale because nothing declares the shared topic dependency.

### 5 · Proposed boundary contract

**The rule the specimen is testing**: Cardinality follows semantic and acceptance boundaries, not the number of plots or files.

```text
  ONE TOPIC       may own 1..n Displays
  ONE DISPLAY     owns exactly 1 primary Reader Takeaway
                  and 1 independently accepted placement job
                  and may contain 1..n complementary Panels
  ONE PANEL       gives one view or sub-proof inside that takeaway
  CANDIDATES      are mutually exclusive compositions of one Display
  ARTIFACTS       are render formats of the selected composition

  same takeaway + same placement + joint acceptance     → panels of ONE Display
  different takeaway OR placement OR independent gate   → sibling Displays
  same topic but sibling Displays                        → ONE Display family
```

📐 The formal page should therefore mirror one Reader Takeaway and its selected composition, not one image file.

### 6 · SELECTION · pending JL

**The open architecture record**: Selection decides the unit boundary that the later skill must enforce.

```text
  🏁 SELECTION · pending · JL
  ──────────────────────────────────────────────────────
  winner       ⬜ A composite · B family · C unrelated
  Display      ⬜ semantic unit definition
  Panel        ⬜ cardinality rule
  family       ⬜ whether topic kinship is formal
  skill work   ⬜ blocked until this ruling closes
```

🏁 CC recommends B for the live L2/L5 case and the boundary contract in Content 5 for the general skill.

## Aims

### P · 🎯 The Display boundary
- P1 · 🧠 Define Display without referring to one figure, table, or file.
  **Done when:** the definition names one Reader Takeaway, one claim job, and one independent acceptance boundary.
- P2 · 🧩 Allow a Display to contain more than one Panel.
  **Done when:** panels coexist only when they are complementary parts of the same takeaway and placement.
- P3 · 🌳 Preserve related Displays without merging their messages.
  **Done when:** one Topic or family can own sibling Displays with separate takeaways and gates.
- P4 · 🏁 Test the rule on L2 and L5.
  **Done when:** the chosen architecture explains both why they are related and why they do or do not merge.
- P5 · 🔒 Keep formal contracts unchanged until the specimen is ruled.
  **Done when:** no page-type, lifecycle skill, or application file changes before JL selects A, B, or C.

## States

### Decision Now
- [ ] 🗣 Which architecture should define the L2/L5 specimen?
      A makes robustness across operationalizations the one message and requires one joint placement.
      B keeps two messages and two placements inside one declared main-regression family.
      C keeps two messages but declares no family relation.
      → CC recommends B because the live units have different Reader Takeaways, claim jobs, placements, and independent acceptance gates.

### P · 🎯 The Display boundary
- ✅ P1 · Content 5 defines Display as a semantic and acceptance unit rather than a visual file.
- ✅ P2 · Candidate A and Content 5 show how one Display may contain multiple complementary Panels.
- ✅ P3 · Candidate B instantiates one Topic with two sibling Displays and separate gates.
- 🧠 P4 · The three architectures are explicit; JL's selection is still open.
- ✅ P5 · This page changes no formal skill or application contract.

## Files

- `QBt16-display-construction.md`
  The companion specimen for choosing among visual forms after the Display boundary is known.
- `../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/S05-display/S-Display-4al2-main-regression.md`
  The live binary-exposure Display page used as E1.
- `../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/S05-display/S-Display-4al5-main-regression.md`
  The live continuous-exposure robustness Display page used as E2.
- `../../../../../../examples/Project-Personality-OpioidRx/diagram/02-cmsreg-260725/QB-regression/QB2-trait-variable.md`
  The source that defines trait_l2, trait_l5, and trait_l5_buc and warns that their names are misleading.
- `../../paper/page-types/haipipe-page-for-display/SKILL.md`
  The current formal Display page contract that this specimen may later revise.

## Log

- 260810 · [DRAFT-CC] Added after the first construction specimen exposed a missing question: before choosing a visual form, the system must decide whether related evidence forms panels of one Display or sibling Displays in one topic family.
