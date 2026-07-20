# Section `.md` Format Spec — the working document

This file is the **rulebook** for the section working document. `ref/section-template.md` is the fill-in skeleton you copy; **this file explains what a finished, filled-in `.md` looks like and the rules it must obey.** Read it once per session.

The section `.md` lives at `0-lifecycle/5-section-edit/{section}/{section}.md`. It is the single working document for the whole section-edit stage — one file, four phases:

```
DRAFT   writes the REAL prose + the "Questions Raised" block
PROBE   fills the placeholders' sources (citations, values, displays)
REVISE  polishes the sentences, then syncs .md -> tex
CHECK   verifies everything matches
```

## The one rule that governs everything

- **The `.md` holds REAL paper prose** — complete academic sentences the user can read as a paper, not telegraphic notes and not a skeleton. (JL ruling 2026-07-09, supersedes the old "lean plan" model.)
- **The `.tex` is GENERATED from the `.md` by sync.** Never hand-edit tex prose.
- **Scaffold by copying `ref/section-template.md`:** fill every `<slot>`, delete every `<tpl:` guidance line. Done when `grep -c '<tpl' {section}.md` prints `0`.

## About the examples below

> **Every example in this file is illustrative.** The venue (`MISQ 2026`), the topic, the sentences, and the numbers are placeholders — the format applies to **any venue and any topic**. When you see concrete prose, read it as "a sentence shaped like this," not "use this sentence."

> JL: How do you get rid of the one paper specfic trace!! remember this is to the genearl topics.
> CC: The paper-specific running example (agreeableness / LLM scoring) is gone — the examples now use a generic construct / instrument / coders topic, and this banner states the format generalizes. OK to retire this note?

## Shape of the file

A finished section `.md` has four parts, top to bottom:

```
1. Title + venue header      what section, which venue, what's binding
2. Structure overview        the paragraph map + word/sentence budget
3. Paragraph blocks          the REAL prose, one ### per paragraph
4. Questions Raised block     the mandatory last block PROBE will drain
```

The next four sections specify each part.

---

## Part 1 · Title + venue header

The first lines name the section and pin its venue contract. DRAFT writes this **once, at scaffold**.

```markdown
# Section N: Title -- Structure

venue: MISQ 2026 · section-type: methods (+results flavor)
blueprint: 0-lifecycle/2a-venue/2a-venue.md (methods block)   <- BINDING: budget, structure, density
style: venue/playbook-utd-is/MISQ/MISQ-methods/style.md · MISQ-results/style.md   (reference only)
```

The four header fields:

```
venue         the pin from STATUS.md (illustrative here — any venue)
section-type  this section's mapping (e.g. 4-llmtrait -> methods)
blueprint     the paper's 2a-venue.md block — the authoritative digest
style         the deep-dive style pack, resolved from the blueprint's [source:] tag
```

- **Blueprint is BINDING** — word budget, paragraphs-per-subsection, citation density, display limits. Deviating fails CHECK.
- **Style pack is REFERENCE ONLY** — mine it for arc, signature moves, and exemplar sentences; deviation is fine and never a CHECK failure.
- A **hybrid section** (e.g. a methods section that also reports validation results) lists more than one style file, `·`-separated.

> JL: This should be chagned into different venue as wel.
> JL: maybe we can write the rules and styles here for the references, instead just list the file, because we might won't read it, how do you think about it?
> CC (venue): agreed — this header value is only an EXAMPLE; DRAFT reads the real venue from STATUS.md at scaffold, so the field is already venue-agnostic (ISR, Nature, JAMA, a grant, a patent all work). Marked it as an example.
> CC (inline vs path): agreed for the BINDING rules. That is exactly what `2a-venue.md`'s blueprint block is meant to be — the pack COMPILED into a readable digest you do NOT have to open the pack for. Recommended middle ground: the section header carries a one-line summary of THIS section's binding numbers (budget · ¶ · density) + the 2-3 key style moves inline, and keeps the full style pack as a deep-dive LINK (packs are long and reference-only, so pasting them whole would bury the header). Thread left OPEN for your call.

### Resolving the style pack path

Resolve the pack path **layout-agnostically** — installed skills flatten the tree:

```bash
VEN=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -type d -path '*skills/paper/venue' 2>/dev/null | head -1)
```

Record the RESOLVED path so later phases (and the user) follow the link instead of re-deriving it. If the pack file is absent, write `style: (pack missing — blueprint only)` and flag for CHECK.

> JL: In think we should just get from the venue.md? How do you think?
> CC: For anything BINDING we already do — 2a-venue.md's blueprint block is self-sufficient for drafting, and the style pack is REFERENCE ONLY. If you'd rather drop the `style:` link from the header entirely and mention packs only here in the resolution step, that's a clean simplification. Your call. (Open design question.)

---

## Part 2 · Structure overview

A fenced block near the top maps the paragraphs and their budget. Update it whenever the structure changes.

```
§N.1 Subsection Title (K paragraphs)
  P1. Short paragraph job description                        5 sentences · ~110 words
  P2. Short paragraph job description                        5 sentences · ~120 words
  P3. Short paragraph job description                        4 sentences · ~95 words

§N.2 Subsection Title (K paragraphs)
  P4. Short paragraph job description                        5 sentences · ~105 words

total: 4 ¶ · 19 sentences · ~430 words   (venue budget for this section: ~500)
```

- Each `Pn` line carries `N sentences · ~M words` — approximate, note the `~`.
- The `total:` line closes the block with ¶ / sentence / word totals against the **venue budget from 2a-venue.md**.
- Recount whenever the block changes (at draft, and after REVISE). Over budget -> **flag it, don't silently trim.**
- Headings: `##` for subsections, `###` for paragraphs.

---

## Part 3 · Paragraph blocks

Each paragraph is one `###` block with **three elements**:

```
1. Heading + preview   the paragraph's job + one scan-hook line (~80–120 chars)
2. Prose sentences     REAL draft prose, one sentence per line, blank line between
3. Comment threads     > USER: / > CC: notes under the sentence they discuss
```

Illustrative example (generic topic — read for shape, not content):

```markdown
## §N.1 Subsection Title

### P1. Why the measure is credible here
(enabler framing; anchors the construct to a validated instrument)

We operationalize the focal construct with the measurement pipeline validated in \citep{smith2024}.

The pipeline recovers expert judgments at a mean absolute error of {VAL:? measurement MAE}.

Its agreement with human coders falls within the range reported for human–human agreement.

> USER: this claim feels strong, soften?
> CC: softened to "closely tracks" — will land in REVISE.

### P2. What this paragraph does
(one-line preview of the key points)

First real sentence of the paragraph.

Second sentence, citing prior work as \citep{wang2022} when the key is already in the .bib, or \cite{TOADD} when it is not.
```

> JL: You need to mention here they are just the examples, keep in mind that we want this to be generalized to other topics as well.
> CC: Done — the "About the examples" banner up top says exactly this, and the example above now uses a generic construct / instrument / coders topic instead of a paper-specific one. OK to retire this note?

Rules for paragraph blocks:

- **Preview = ONE short line** (~80–120 chars): a scan hook (concept name + one distinguishing phrase), not a mini-abstract.
- **Sentences are REAL prose:** complete academic sentences close to submission register, content-complete. If a fact is missing, **write the sentence anyway with a placeholder** — verification comes in PROBE.
- **One sentence per line, blank line between** (each becomes a `Pn.Sn` marker when synced to tex). Never prefix a sentence with its number (`S1.` etc.) — `Pn.Sn` indexing lives only in tex.
- **Target 5–6 sentences per paragraph** (MISQ/ISR norm; consult the section-type for venue-specific).
- **Comments** go directly under the sentence discussed: `> USER:` for the user, `> CC:` for your reply. (Full lifecycle: Cross-cutting conventions below.)

### Citations & numbers — real or greppable, never invented

(JL ruling 2026-07-10, supersedes the old `[CITE: <topic>]` markers and parenthetical "(Author Year)". A legacy `[CITE:]` in an old draft is treated as `\cite{TOADD}`.)

Three placeholder forms, and nothing guessed:

```
{VAL:? <what>} [Q-<Stage>-<n>]  a number PROBE must trace to a source, + the question that will produce it
\citep{key} / \citet{key}       a REAL citation — the key must already EXIST in the .bib
\cite{TOADD} [Q-<Stage>-<n>]    a citation slot with no suitable .bib key yet, + the question that will produce it
```

The placeholder and its anchor bracket are **two markers side by side, never fused**. The bracket names the `1-probes/` question that owes the answer; without it the placeholder is a defect.

- **`\citep{key}`** — grep the `.bib` **first**. Writing a key that does not grep in the `.bib` is **inventing a citation**.
- **`\cite{TOADD} [Q-<Stage>-<n>]`** — every `TOADD` carries the bracket of the question that will produce the key, side by side, **never fused into one marker**. A bare `\cite{TOADD}` with no bracket is a defect: a hole no question will ever fill. `grep -c TOADD` counts open slots; a `TOADD` that survives into compiled tex **fails CHECK**.
- **`{VAL:?}`** — the `<what the number is>` text is what PROBE traces.

Citation commands (`\citep` / `\citet` / `\cite{TOADD}`) are the **only** LaTeX allowed in the `.md` — they sync to tex verbatim. No other markup.

---

## Part 4 · Questions Raised by This Draft (mandatory last block)

**BINDING (JL 2026-07-18): every DRAFT MUST end with this block, in this exact structure.** A DRAFT that omits it, or writes it as freeform prose, is INCOMPLETE and FAILS the gate — no exceptions.

The draft **proposes** the questions (the Q_consume list); PROBE, after the gate, **fills** each Answer. This is the human-readable list the user reviews at the DRAFT gate and the list the PROBE run drains.

It is the **last content** of the `.md`, and has three parts in order: **(1) the questions, (2) settled flags, (3) the user's own notes.**

```markdown
---

## Questions Raised by This Draft

Each question is a Q_consume: it links back to the sentence that raised it, and its Answer is filled later by the probe group (the bank).

### <TAG>-Q1 · <short title>
- **Question.** <one clear line — the consumer question>
- **Links to.** §<N> P<x>.S<y>  ·  serves: <claim id / stage>  ·  track: <citation | values | display | discovery | decision | wording>
- **Description.** <2–4 short sentences: what is uncertain, why it matters, what a good answer looks like>
- **Answer (from the group).** _pending — filled by PROBE_

### <TAG>-Q2 · <short title>
- **Question.** ...
- **Links to.** ...
- **Description.** ...
- **Answer (from the group).** _pending — filled by PROBE_

---

## Settled Flags (not open questions — logged, no action)

- <accepted deviations, already-ruled items, and placeholder rollups that resolve paper-local — bullet lines, never a table>

---

## My Notes & Feedback — JL
<!-- Yours. Agents never overwrite below this line. Add rulings, priorities, extra questions, corrections. -->

_(empty — add your notes here)_
```

Rules for this block:

- **The index carries a TAG** so every question is globally unique and traceable to its origin: `§<N>-Q<n>` for a manuscript section (`§1-Q1`, `§6-Q2`; `§0` = abstract), `<stage>-Q<n>` for a lifecycle stage (`seed-Q1`, `claims-Q1`, `pitch-Q1`).
- **One `###` subsection per question** — never collapse questions into a shared bullet list or a table. Each carries all four labelled fields: **Question · Links to · Description · Answer (from the group)**.
- **`Links to` is MANDATORY** — it is how the reader jumps from the question back to the exact `Pn.Sn` sentence that raised it. It also carries `serves:` (claim/stage) and `track:`.
- **`Answer (from the group)`** starts as `_pending — filled by PROBE_`. PROBE writes the harvested answer here (plus the `target:` QA-file path). A question that is a pure human decision reads `JL decision`.
- **Everything heavier than pointer-following becomes a numbered question** — every `{VAL:?}`, every `\cite{TOADD}`, every display need. Only items that resolve paper-local (a pointer the draft already sees) go under **Settled Flags** instead.
- **A missing DISPLAY UNIT is never a question** — it becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (section-edit never creates displays).
- **`My Notes & Feedback — JL`** is a mandatory, user-owned section, always present (even when empty). Agents NEVER rewrite or delete anything below its marker (JL comment-lifecycle rule).
- **Bullet lines, never markdown tables**, anywhere in this block (JL standing rule — no tables in probe documents).
- This block is the **consumer-facing view.** At PROBE-run time the heavier bank questions are DISPATCHED via `1-probes/PP<NN>_<topic>.md` (executor-facing `q-executor:`, no stake) + a `1-probes/README.md` bullet row (`- PP<NN> · <stage/section> · <state> · <one-line need> · file: <path>`); the harvested answer flows back into the matching question's Answer field here.
- The **⛔ STOP presentation shows this block**, so the user reviews the STRUCTURE and the QUESTIONS at the same gate.

---

## Cross-cutting conventions

These apply everywhere in the `.md`:

- **Comment lifecycle (binding).** The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies underneath with `> CC:`. Only the **user** declares a thread resolved; a resolved thread MOVES to `_LOG` verbatim. Each phase starts with a clean file.
- **Surgical edits only.** Change the specific lines under discussion. A full-file rewrite of a `.md` that carries `> USER:` comments is forbidden.
- **Never a tex mirror.** No LaTeX markup except citation commands, no `%%` markers, no agent monologue in the `.md`.

---

## What DRAFT prose IS — and is NOT

DRAFT settles **WHAT** each sentence says, in real sentences. REVISE settles **HOW** it sounds.

DRAFT prose is:

- **NOT verified** — that's PROBE (`{VAL:?}` and `\cite{TOADD}` stay until traced).
- **NOT venue-polished** — that's REVISE (humanizer, sentence economy, weave).
- **NOT LaTeX** — that's sync-to-tex after REVISE.
- **NOT the agent's scratchpad** — analysis and options belong in the session, not the file.

If a sentence says the **wrong thing**, fix it in the `.md` during DRAFT (or restart DRAFT). If it says the right thing but **sounds bad**, REVISE fixes it — in the `.md` first, then sync to tex.

---

## Backward-fill: populating from existing tex

When the section already has prose in `0-sections/*.tex`, fill the `.md` from it once:

1. Read the tex file.
2. Extract paragraph structure (from `% Para [id]` banners or `%% ---- Pn.Sn ----` markers).
3. For each paragraph: create the heading + preview, then copy the sentences as prose lines (one per line, blank-line separated, markers stripped).
4. Preserve any existing `> USER:` comments from prior rounds exactly where they were.
5. Present the populated `.md` to the user for review.

This is a **backward fill** (tex -> `.md`), done ONCE at scaffold. From then on the `.md` is the source and tex is sync output.

---

## Reference

### Inputs for section drafting

```
z-structure     0-lifecycle/5-section-edit/z-structure/z-structure.md   paper-level architecture
narrative       0-lifecycle/3-narrative/3-narrative.md                  the story beats
existing tex    0-sections/NN_section.tex                               if the section already has prose
section-type    section-type/section-{type}/SKILL.md                    structure norms for this section type
venue contract  0-lifecycle/2a-venue/2a-venue.md                          blueprint + writing principles (venue/ packs = fallback)
claims          0-lifecycle/1b-claims/1b-claims.md                        what claims this section must support
```

### Done-criteria for section DRAFT

- [ ] `grep -c '<tpl' {section}.md` = 0 (template fully instantiated, no guidance residue)
- [ ] Every paragraph has a heading, preview, and real prose sentences
- [ ] Structure overview matches the paragraph blocks
- [ ] Every unverified number is a `{VAL:? <what>} [Q-<Stage>-<n>]`; every citation gap a `\cite{TOADD} [Q-<Stage>-<n>]`; every `\citep{key}` greps to a real .bib entry (nothing invented); no placeholder is left without its bracket
- [ ] **MANDATORY** "Questions Raised by This Draft" block is the `.md`'s LAST content, in the fixed structure: one `###` Q-subsection per question (Question · Links to · Description · Answer from the group), then a Settled Flags section, then a user-owned "My Notes & Feedback — JL" section. A DRAFT missing this block, or writing it as freeform prose, FAILS the gate.
- [ ] Every placeholder + display need + heavier question appears as a numbered Q with a `Links to` back-reference and a `_pending_` Answer slot
- [ ] ⛔ The user has reviewed the STRUCTURE + the QUESTIONS and approved (no open structural `> USER:` questions)
- [ ] `_LOG` has a `[GATE] draft-review: approved` entry quoting the user

### _LOG entry format for DRAFT

```markdown
## YYYY-MM-DD #N ~HH:MM [GATE] draft-review: approved
> USER: "looks good, go"

## YYYY-MM-DD #N ~HH:MM [DRAFT]
> USER: original comment
> CC: response
-> applied / rejected / deferred
- Created section .md with N paragraphs, M sentences, K {VAL:?} + J \cite{TOADD} slots, L \citep{} keys from .bib
- Key decisions: [structural choices from resolved comments]
```

### DRAFT vs REVISE

```
DRAFT                                  REVISE
-----                                  ------
settle WHAT to say                     settle HOW to say it
real prose, one sentence per line      venue-quality prose, humanized
\citep{key} from .bib + \cite{TOADD}   verified values; TOADD resolved to real keys
content decisions                      sentence economy, voice, flow
writes the .md                         revises the .md, THEN syncs to tex
```

The draft prose is the INPUT to REVISE. Both phases work the `.md`; only sync touches tex.
