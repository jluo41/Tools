# A display with a caption and a label: an argument, and a promise

state: 🔴 OPEN
owner: JL
method: say what the caption must accomplish and what the label promises, and put both where the ruling says they live

## Opening

The picture is finished. What does the paper still have to write on it?

Two things, and neither is the renderer's. A caption is prose in the paper's voice, doing work the picture cannot. A label is the anchor every `\ref{}` depends on. They arrive together and they are not the same kind of thing at all.

**Where this page sits**: `QB5@display` already ruled who owns them and is ✅ SETTLED, so ownership is not re-argued here.
QB11c owns where the float then lands, QB12c and QB12d own what a citing sentence means, and QB11a owns float numbering across the document.

**Why this face is still 🔴 with ownership settled**: the ruling says the fields are consumer-owned and says nothing about what they must contain.
So the ownership is decided and the CONTENT rules are blank, which is exactly how every caption on this paper came to be typed straight into `float.tex` by hand.

**What that costs beyond tidiness**: a caption with no decision record.
Nothing says who approved this wording or what the earlier one was, so a caption cannot be reviewed, only rewritten.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never re-argue ownership**: `QB5@display` settled that the fields are consumer-owned and that a renderer may serialize but not invent or revise them.
This page writes the content rules that ruling left blank.

**Treat the caption and the label as two topics, never one wrapper**: they fail differently, and the page that called them one thing had to be split.
A weak caption costs a reader effort; a changed label breaks every sentence that cited it.

**Write the caption rule so CHECK can apply it**: a test, not a template.
"Says what the reader should take away" can be judged; "is well written" cannot.

## Diagram

**Two fields, two jobs**: and what each one breaks when it is wrong.

```text
  ✍️ THE CAPTION                      🔖 THE LABEL
  ─────────────                       ────────────
  prose, in the paper's voice         a stable promise
  names what the reader should        every \ref{} in every section
  take away                           depends on it
                                      survives a re-render, a promotion,
  🚫 restating the axis labels          a change of renderer, a change
     spends a float and says            of file path
     nothing
  👁 it is the only part of a         🚫 two units may NEVER declare
     display most readers read           the same label

  💥 a weak caption   ━━▶ costs a reader effort
  💥 a changed label  ━━▶ BREAKS every citing sentence, silently
```

## Content

### 1 · Two fields, two different jobs

**What each owes**: the caption argues, the label promises.

```text
   the CAPTION does work the PICTURE CANNOT
        ┌──────────────────────────────────────┐
        │ ✅ what the reader should take away  │
        │ ❌ a description of what is drawn    │
        └──────────────────────────────────────┘

   the LABEL is the ONLY part other files depend on
        ┌──────────────────────────────────────┐
        │ a sentence points at the UNIT,       │
        │ never at a file  ── QB12c's Law      │
        └──────────────────────────────────────┘
```

✍️ Establishes the two fields as separate topics with separate failure modes.

#### 1.1 · The caption is the most-read part of a display
(most readers read it and never study the picture, which sets how much work it has to do)
A caption that restates the axis labels has spent a float and said nothing.
It is the one place the paper gets to say what the picture is FOR, and skipping that wastes the most expensive object on the page.

### 2 · Where they are supposed to be authored

**The ruled home, and the actual one**: twelve pages, zero blocks.

```text
  📜 QB5@display names the home:
     a  ### Wrapper  block on the matching S-Display-N page

  📊 on this paper
     12 display pages carry  ### What it shows  +  Registry id
      0 carry  ### Wrapper                              ⚠️

  ━━▶ every caption and label was authored directly into
      displays/*/float.tex ── the file the ruling says a renderer
      may only SERIALIZE into

  💥 the cost: a caption with NO decision record
     nothing says who approved this wording, or what the earlier one was
```

🏠 Establishes the gap between the ruled home for these fields and where they actually live today.

#### 2.1 · Drift here removes review, not just tidiness
(a field with no decision record cannot be reviewed, only overwritten)
Authoring into `float.tex` puts the caption in a file that a re-render may legitimately rewrite.
There is no history, no approver, and no earlier version, so a disagreement about wording has nothing to point at.

### 3 · What a label promises, stated so it can be broken

**One live violation**: two units, one section, and a reference that resolves to nothing.

```text
  🔒 two consequences of a label being a promise
     ① renaming one is a BREAKING CHANGE across the manuscript
     ② two units may NEVER declare the same label

  ⚠️ this paper breaks ② today
     displays/Table/table1-agreeableness-distribution
        └── \label{tab:distribution}
     display09-agreeableness-distribution
        └── \label{tab:agreeableness-distribution}

     §4 \inputs the FIRST and \cites the SECOND
     ━━▶ the section cites a label that nothing it reaches declares
```

🔒 Establishes the label's promise in a form that can be violated, together with the violation currently in the paper.

#### 3.1 · The legacy folder is the live breach
(it matters because the symptom looks like a display problem and is really a duplicate-label problem)
The older `Table/` folder and `display09` describe the same table under two labels.
A reader chasing the `??` in §4 finds a missing float, when what is actually wrong is that two units claim one name.

## Aims

### A1 · ✍️ Two fields, two different jobs
- A1.1 · What a caption must accomplish for this venue is stated as a test.
  **Done when:** CHECK can pass or fail a caption without judgement, using a written test rather than a template.

### A2 · 🏠 Where they are supposed to be authored
- A2.1 · The `### Wrapper` block the ruling already requires exists.
  **Done when:** every `S-Display-N` page on this paper carries a `### Wrapper` block, and no caption is authored only in `float.tex`.

### A3 · 🔒 What a label promises, stated so it can be broken
- A3.1 · A label is ruled a breaking change, and no two units may share one.
  **Done when:** the rule is written here and the `Table/` against `display09` duplicate is resolved, so §4 cites a label something it reaches declares.

## States

### A1 · ✍️ Two fields, two different jobs
- ⬜ A1.1 · Not started. Ownership is settled upstream at `QB5@display`; the content rules it left blank have never been written, which is why this face is still 🔴.

### A2 · 🏠 Where they are supposed to be authored
- ⬜ A2.1 · Not started. Twelve display pages, zero `### Wrapper` blocks, and every caption lives hand-written in `float.tex`.

### A3 · 🔒 What a label promises, stated so it can be broken
- ⬜ A3.1 · Not started, and violated today. `displays/Table/table1-agreeableness-distribution` and `display09-agreeableness-distribution` declare different labels for the same table, and §4 inputs one while citing the other.

## Files

- `displays/*/float.tex` · where caption and label actually live today, written by hand
- `0-lifecycle/3-display/S-Display-*.md` · the twelve pages that should carry `### Wrapper` and do not
- `QB13-delivery-display.md` · the series head, which owns why the float is its own unit

## Law

A caption is an argument in the author's voice and a label is a promise other files depend on; a renderer may serialize both and may invent or revise neither.
Two units may never declare the same label, and renaming one is a breaking change across the manuscript.

## Glossary

- **Caption**: prose doing the work the picture cannot, namely naming what the reader should take away.
- **Label**: the anchor every citing sentence depends on, which survives a re-render, a promotion, and a change of file path.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into three divisions with face figures and captions, Aims regrouped as A1/A2/A3 with `Done when`, States mirrored per Aim, and Law and Glossary written for the first time.
260802 · Became QB13c under the float series, which is where the paper's own authored text on a display belongs.
260727 · Reframed from "the wrapper: caption, label and placement"; placement left for QB5f because where a float lands is decided by which section cites it first.
