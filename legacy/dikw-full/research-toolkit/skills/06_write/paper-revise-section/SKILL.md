---
name: paper-revise-section
description: "Audit one .tex paper section that carries inline %% Comments: {INITIALS} ... author annotations, then propose a paragraph-level revision plan. Workflow: format-check the file → read author comments → severity-ranked diagnosis (🔴/🟡/🟢) in chat → single integrated ASCII flow diagram (.txt) where each paragraph box carries 📌 NOW + 🔧 PROPOSE inline with verb icons (✅ keep / ✏ edit / ✂ drop / ➕ add) and a bottom length-budget + edits-summary panel → STOP and wait for author approval. Use when the user wants to revise a single section, mentions /paper-revise-section, or hands a .tex file with %% Comments: lines and asks how to fix the logic. Companion to /paper-revise (broader interactive revision workflow); this skill is the lightweight diagnose-only entry."
---

Skill: paper-revise-section
===========================

One-shot **diagnose + plan** pass on a single LaTeX section file that carries
inline author comments. Produces a severity-ranked diagnosis and an ASCII
logic diagram as the deliverable. Does NOT edit the .tex. Editing is a
follow-up step the author triggers explicitly (typically via `/paper-revise`).

The point of this skill is to make the **revision plan** visible and
reviewable BEFORE any prose changes. The diagram IS the deliverable.

Usage
=====

```
/paper-revise-section <path-to-section.tex>
```

That is the only invocation. No subcommands, no flags.

Example:
```
/paper-revise-section examples/.../0-sections/01_introduction.tex
```

---

Required input format
=====================

The target `.tex` file MUST use the two-marker convention:

1. **Paragraph / sentence index headers**, one per logical unit:
   ```
   %% ---- PN.SN ----
   ```
   - `PN` = paragraph number, `SN` = sentence number
   - Numbering is **file-local**: P1 restarts at the top of every section file
   - Optional bracket note allowed: `%% ---- P2.S7 [NEW per v0517] ----`

2. **Author comments**, attached to a specific sentence:
   ```
   %% Comments: {INITIALS} v<tag>: <free-form thoughts>
   ```
   - These are the *thinking* the skill operates on
   - **Never rewrite, translate, summarize, or compress these lines**
   - They stay verbatim in the file across every pass

If the file does not satisfy this format, the skill stops and reports
which paragraphs are missing markers. It does not silently auto-insert.

---

What the skill does (in order)
==============================

### Step 1. Format check

Read the file. Verify:
- every paragraph has a `%% ---- PN.SN ----` header
- `PN` numbering starts at 1 and is monotone within the file
- at least one `%% Comments: {…}` line exists (otherwise there is nothing
  to react to, bail out and tell the author)

If anything fails: print a short table of what's missing and stop. Do not
proceed to diagnosis on a malformed file.

### Step 2. Read the comments

For each `%% Comments: {…}` line, extract:
- which `PN.SN` it is attached to
- the verbatim text of the author's note

Do not paraphrase them in your response. Refer to them by `PN.SN` and quote
the relevant phrase only when needed.

### Step 3. Diagnosis with severity ranking

Print a compact table:

```
| Severity | Location | Problem | Fix sketch |
| 🔴 | P3 → P4 | ... | ... |
| 🟡 | P2 | ... | ... |
| 🟡 | P1.S3 → P2.S1 | ... | ... |
| 🟢 | P5 / P6 | OK | keep |
```

Rules:
- 🔴 = hard blocker (broken logic, redundancy across paragraphs, wrong order)
- 🟡 = compression / re-anchoring needed but the paragraph still has a role
- 🟢 = leave alone
- Always include at least one row per author-commented paragraph
- Rank by severity, not by file order

Do this BEFORE drawing anything. The author should be able to read just
this table and know whether to proceed.

### Step 4. ASCII diagram: the deliverable

Produce **one** `.txt` file that is a single integrated NOW + PROPOSE
flow. Everything decision-relevant lives inside the paragraph boxes;
do **not** open a separate "Decision points" or "Proposed actions"
section at the bottom of the file.

**Header**:

```
📜 <Section name> v<tag> : Logic Flow + Proposed Edits
═══════════════════════════════════════════════════════════

  Each block shows:
    📌 NOW       what v<old> currently says (S<range>, ~Nw)
    🔧 PROPOSE   what v<new> changes
                 ✅ keep   ✏ edit   ✂ drop   ➕ add

  Comments read at : P<i>.S<j> (<one-line summary>)
                     ...
```

**Each paragraph box has two regions, in this fixed order**:

```
  ┌───────────────────────────────────────────────────────┐
  │ <emoji> P<N>  ·  <ROLE LABEL>       [MAIN EDIT]?      │
  │                                                       │
  │ 📌 NOW (S1-S<k>, ~Nw)                                 │
  │    S1: <compact paraphrase of current sentence>       │
  │    S2: ...                                            │
  │                                                       │
  │ 🔧 PROPOSE (<delta>w)                                 │
  │    ✅ keep S<i>, S<j>                                 │
  │    ✏ edit S<k>: "<draft text the author can paste>"   │
  │      reason: <one-line justification>                 │
  │    ✂ drop S<m> (<one-line reason inline>)             │
  │    ➕ add S<n> (<role>): "<draft text>"               │
  │      reason: ...                                      │
  └───────────────────────────────────────────────────────┘
                            │
                            ▼
```

Rules for the two regions:

- **📌 NOW**: sentence-by-sentence compact paraphrase, NOT a copy of
  the original prose. Show the sentence range and approximate word
  count in the header line, e.g. `(S1-S5 + S7-S9, ~137w)`.
- **🔧 PROPOSE**: concrete deltas, one per affected sentence, prefixed
  with the verb icon:
  - `✅ keep`: sentence stays as-is
  - `✏ edit`: sentence is rewritten; **include the draft text in
    quotes** so the author can paste directly
  - `✂ drop`: sentence is removed; include the one-line reason
  - `➕ add`: new sentence; include the draft text and the role
    (hinge / pivot / closer / etc.)
- **`reason:` line**: for any non-`keep` action, give one short reason
  inline (no separate "rationale" section).
- **`[MAIN EDIT]`** tag on the box header: flag the 1 to 2 paragraphs
  that carry the bulk of the change. Helps the author know where to
  focus the review.

**Connectors** between paragraph boxes are minimal: just `│` then `▼`.
Do **not** insert pivot boxes, transition cards, or 笔锋 callouts as
separate nodes. If a transition is the point of the edit, encode it
inside the affected paragraph's PROPOSE block as a `✏ edit S1 opener:`
or `➕ add S<k> (hinge):` action with the draft text.

**Bottom panels** (two, in this order):

```
  ─────────────────────────────────────────────────────────
  📐  Length budget
      v<old> current  : ~Nw / M sentences
      v<new> proposed : ~Nw / M sentences (-Δw, -Δ sents)
      <venue limit, if relevant>
  ─────────────────────────────────────────────────────────

  🗂️  Edits summary
      ➕ P<i>.S<j>      <one-line label>           +Nw
      ✂  P<i>.S<j>      <one-line label>           -Nw
      ✏  P<i>.S<j>      <one-line label>            0w
      ...
  ─────────────────────────────────────────────────────────
```

The Length budget panel is **required** for abstract sections (because
the venue word limit binds) and **encouraged** for any section where
compression is the point. The Edits summary panel is **always required**
and must list every non-`keep` action from every paragraph.

**Style**:

- Use Unicode box drawing (`┌─┐ │ └─┘`), not ASCII (`+--+ |`).
- Use plain ASCII arrows (`->`, `<->`, `=>`) inside boxes; reserve
  the Unicode arrow `▼` for the connectors between boxes.
- Keep lines under ~58 chars wide so boxes fit in a typical editor.
- No em-dashes (rule below); use `·` as the role separator on the
  box header (`P1  ·  SETUP + SIGNAL`).

### Output rules for the diagram

- **Format = `.txt` ONLY.** Not `.tex`, not `.md`, not TikZ. Even if the
  request literally says "TikZ", save a `.txt`. (This rule overrides
  natural-language hints.)
- **Save path** and **naming**:
  - Convention: `<section-stem>_logic.txt` (NOT `-logic-flow`,
    NOT `-flow`). Matches the existing `00_abstract_logic.txt` style.
  - Default location: sibling `1-feedback/v<tag>/` directory next to
    the paper's `0-sections/`. Example: the diagram for
    `0-sections/01_introduction.tex` saves to
    `1-feedback/v0516/01_introduction_logic.txt`.
  - If `1-feedback/v<tag>/` doesn't exist or the author specified a
    different folder, save where the author said and skip the convention.
- Follow the integrated NOW + PROPOSE template described above. See
  `ref/example-intro-logic-flow.txt` for a worked example (npjDM2025
  introduction, 6 paragraphs, three author comments).
- For a shorter section (abstract, ~6 sentences) the same template
  collapses naturally: one box per logical block (WHY, WHAT,
  VALIDATION, FINDINGS, IMPLICATION) instead of one per paragraph.

### Step 4b. Insert the logic-pointer stub into the .tex

After the `.txt` is saved, add (or update) a stub at the top of the
section `.tex` file so the author can jump straight to the logic
diagram via the "Open file under cursor" extension by seito.

**Fixed stub format** (6 lines, wrapped by a `%` line on each side):

```latex
%
%% Logic + proposed edits diagram:
%%   ../1-feedback/v<tag>/<section-stem>_logic.txt
%% To open side-by-side: right-click the path above ->
%%   Open file -> "Open file under cursor in editor beside active"
%%   (or Alt+P for same-tab open; requires "Open file under cursor" extension by seito)
%

%% ---- P1.S1 ----
<existing first sentence>...
```

For sections wrapped in an environment (e.g. abstract, which uses
`\begin{abstract}...\end{abstract}`), the stub goes immediately INSIDE
the environment, between `\begin{...}` and the first sentence marker.
For plain sections (introduction, methods, etc.), the stub goes at the
very top of the file.

**Rules**:

- The path is **relative from the .tex file's location**. From
  `0-sections/<stem>.tex` that resolves to `../1-feedback/v<tag>/...`.
- Indentation is `%%` followed by 3 spaces then the path. The path is
  on its own line so "Open file under cursor" can detect it cleanly.
- **Idempotent**: if a stub already exists (any line starting with
  `%% Logic + proposed edits diagram:` or containing a `_logic.txt`
  path), update the path in place (e.g. `v0516` → `v0517`). Do not
  stack stubs.
- One blank `%` line above and one below the stub block.
- This is the **only permitted edit** to the `.tex` in this skill.
  No prose changes, no marker renumbering, no `%% Comments:` rewrites.

**Side-by-side opening, no keybinding setup needed**: the seito
extension ships a context-menu command `Open file ▸ Open file under
cursor in editor beside active`. The author right-clicks the path,
picks that submenu item, and the `.txt` opens in the right group.
This is the recommended default. If the author wants a single-key
shortcut, they can bind it in VS Code keybindings:

```json
{
  "key": "alt+shift+p",
  "command": "seito-openfile.openfileBeside",
  "when": "editorTextFocus"
}
```

(Optional, user-level config; not something the skill writes.)

### Step 5. STOP

After saving the `.txt` and inserting/updating the `.tex` stub, end the
turn with a short summary:

- one line on the diagnosis (top 🔴 issue)
- one line on the diagram path
- one line confirming the stub was inserted/updated
- one line offering the next step ("apply via /paper-revise?" or
  "want me to draft the new P4 opener inline?")

Do NOT touch any other part of the `.tex`. Do NOT write per-section
`.md` reports. Do NOT update any `revision-checklist.md`. The diagram,
the diagnosis in chat, and the 2-line stub are the entire deliverable.

---

Hard rules (do not violate)
===========================

1. **Preserve `%% Comments: {…}` lines verbatim** if you ever touch the
   .tex (this skill normally does not). No translation, no compression.

2. **PN.SN markers are file-local.** Never use cross-file continuous
   numbering. P1 restarts at the top of every section file.

3. **No em-dashes anywhere.** In diagnosis prose, in the diagram, in any
   suggested rewrites: use comma, colon, or sentence break instead.

4. **No AI-flavored prose.** No buzzword stacks, no parenthetical
   name-explosions, no italics-on-nouns. Short plain academic sentences.

5. **Compress, don't split.** Long sentences get adjectives /
   parentheticals / hedging removed. Do not chop them into fragments.
   ≤6 sentences per paragraph is the hard ceiling.

6. **ASCII diagram only.** Even if the prompt names TikZ or LaTeX figure,
   save `.txt`. If the author insists on TikZ after seeing the `.txt`,
   they will say so explicitly and override this rule.

7. **No `.md` report files** as a side effect. The diagnosis table lives
   in the chat reply only. The diagram is the only file written.

---

When to invoke this skill vs. neighbours
========================================

| If the author wants ... | Use |
|---|---|
| diagnose one section + plan the revision | **paper-revise-section** (this) |
| interactive multi-pass revision with sentence-level annotations + apply | `/paper-revise` |
| draft a section from an outline | `/paper-write` |
| critique paper-wide structure, not one section | `/paper-structure-planning` |
| build a TikZ figure for the published paper | `/figure-spec` or `/diagram-drawio` |

This skill is the lightweight diagnose-and-plan entry. Once the diagram
is accepted, the author typically continues with `/paper-revise` to apply
sentence-level changes.

---

Worked example
==============

See `ref/example-intro-logic-flow.txt` for the diagram produced from the
npjDM2025 introduction section (6 paragraphs, three author comments at
P1.S3, P2.S9, P3.S3). That file shows the exact box layout, the four
verb icons in use (✅ ✏ ✂ ➕), how `reason:` lines are attached to each
non-keep edit, and how the bottom Length-budget and Edits-summary
panels are populated.

For the matching abstract-style example (one box per logical block
rather than per paragraph), see the v0516 workspace file
`1-feedback/v0516/00_abstract_logic.txt` in the npjDM2025 paper folder.
That file is the source style this skill is based on.
