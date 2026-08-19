# Revise: replace the holes, cite the units, and rebuild until the deliverable matches the source
state: 🟡 IN PROGRESS · the phase ships; COMPILE is folded in and owes its own split test · open: 6
owner: CC
method: fix the promise, then order the work so facts land before voice and both projections are rebuilt last; every rule names the artifact a reader opens
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
The promise is fixed, the answers have landed, so does the file a reader actually opens say the same thing as the source?

REVISE is phase ⑤ and it is where a page BECOMES its artifacts: it replaces the holes DRAFT left, cites each display unit by id in the sentence that makes the claim, renders and picks and builds every unit whose intake EVIDENCE froze, and rebuilds `latex/` and `word/`.
It may add, delete, move, and rewrite as freely as DRAFT can, so the edit shape never identifies it; the one test is whether the page's purpose and Aims still describe the result afterwards.
Its risk is the quiet swap: a revision that redefines what the page is for while calling itself an improvement, which is why a fixed promise is the phase's only boundary.
It also carries COMPILE, folded in since 260817, because "the prose is right" was reported as done while the PDF still carried raw comment markers and literal asterisks.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every rule names the artifact a reader opens**: this phase's failures are all invisible in the markdown and visible in the PDF or the docx.
A rule that stops at the source has not reached this phase's subject.

**Order is a rule here, not a preference**: facts land before argument and argument before voice, because polishing prose around a hole is work that gets thrown away.
State the step numbers when describing the order, so a reader can tell which step was skipped.

**The renderer owns `recipe/` end to end**: this page may say which renderer is called and must never describe what it writes.
When this page and `QPf5` disagree about a unit's folder, the plugin wins.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
The five-step order, the three display steps this phase owns, and the two projections it must rebuild.

```text
🖊 REVISE · phase ⑤ of 7 · the promise is FIXED
┌──────────────────────────────────────────────────────────────────────┐
│ same promise after the change          ──▶ REVISE                     │
│ purpose or an Aim must change          ──▶ DRAFT, new round           │
│ an unsupported claim blocks the edit   ──▶ EVIDENCE, then route again  │
└──────────────────────────────────────────────────────────────────────┘

the pass, in order, and the order is conditional not decorative:
① LAND    read the A-consumer and its A-executor source, discharge the hole
② ARGUE   test accuracy, warrant, sequence, claim strength
③ SOUND   voice and readability, AFTER the final facts are present
④ RENDER  draw every unit whose intake EVIDENCE froze, cite it BY ID
⑤ BUILD   rebuild latex/ and word/ so the deliverable matches the source

the display walk, and REVISE owns the middle three:
① INTAKE  🧑 freeze the answer            EVIDENCE
② RENDER  ⚙️ the renderer writes recipe/  REVISE   ← the caption and which
③ PICK    🧑 choose among candidates/     REVISE     rows ARE the argument
④ BUILD   ⚙️ assets/ float.tex preview    REVISE
⑤ ACCEPT  🧑 README `accepted: ✅`        CHECK

both projections, rebuilt at the END of the pass:
latex/  POST /_board/latex  ─▶ <page>/latex/<stem>.tex + .pdf
word/   the word plugin     ─▶ <page>/word/<stem>.docx + its PDF twin
```
📌 A unit nobody cites is a unit neither projection places, because the projections inherit the citation from the prose.

## Content

### 1 · The promise is fixed, and that is the phase's only test
**The authority test**: everything about the page may change here except what it is for.

```text
the edit                                              phase
────────────────────────────────────────────────────────────────
delete a whole section under the same promise           REVISE
move an argument between divisions                      REVISE
rewrite the Opening for clarity, same purpose           REVISE
add a paragraph serving an existing Aim                 REVISE
change what an Aim PROMISES                             DRAFT
change what the page is FOR                             DRAFT
```
📌 The size, age, and operation of an edit decide nothing; only whether the current promise still describes the result afterwards.

#### 1.1 · An administrative correction to an Aim is not a DRAFT
(preserving an Aim's meaning is REVISE, changing what it promises is DRAFT even when the diff is one word)
The test reads the Aim's intent rather than its characters, which is why a small diff can be DRAFT and a large one can be REVISE.
`QPw00 §6.2` carries the same test for moving and rewriting across the whole loop.

#### 1.2 · REVISE has no fixed position in the loop
(it may run straight after DRAFT, after EVIDENCE, after CHECK feedback, or repeatedly)
It is not the third step of a rigid sequence, and a page that reaches it twice in one round has not regressed.
The moment the promise stops fitting, the work becomes a new DRAFT round and must say so rather than continuing quietly.

### 2 · Land the facts before polishing the prose around them
**The order rule**: five steps, and each one exists because doing it later wastes the one before it.

```text
① LAND    discharge the owned hole from the landed answer
② ARGUE   accuracy · warrant · sequence · claim strength
③ SOUND   voice and readability, only once the facts are final
④ RENDER  every frozen intake becomes a drawn, cited unit
⑤ BUILD   both projections rebuilt from that prose

why the order: polishing a sentence around a hole is work thrown away when
the number arrives, and building before ④ ships a PDF missing its figures
```
📌 The order is conditional rather than a claim that every REVISE follows EVIDENCE: with no answer landed, begin at the first applicable step.

#### 2.1 · An unanswered hole stays visible and keeps its id
(never estimate, never infer from nearby prose, never quietly drop the sentence)
Removing a marker to make the page look finished is the one failure this phase can cause that no later phase can detect.
The hole and its id survive the pass so CHECK can see what is still owed, which is the whole reason the marker was made visible at DRAFT.

### 3 · The page becomes its artifacts here, or it never does
**The realization rule**: nothing downstream builds the projections, so a pass that changed a claim and did not rebuild leaves the source and the deliverable disagreeing.

```text
what a rebuild-less pass ships
  the markdown says 0.42 and the PDF says <VALUE HOLE>
  the markdown cites Display3 and the .tex inputs nothing
  the docx carries raw <!-- --> comments and literal ** asterisks

and the person who finds it is the READER
```
📌 This is why COMPILE was split off REVISE and then folded back into it: the two were one phase reporting one done, and "the prose is right" covered a broken PDF.

#### 3.1 · Cite each unit by its short id in the sentence that makes the claim
(`Display3`, `Display5`, in the prose and never in a list at the bottom)
LaTeX embeds the unit's float after the citing paragraph, and Word embeds the rasterized figure with its `(Figure n)` and a 🖼 comment, so both projections inherit their placement from the citation.
A unit nobody cites is a unit neither projection places, which is how five declared display units reached LaTeX as two.

#### 3.2 · Rendering is not release
(a labelled candidate may be rendered and cited while a method or provenance question stays open)
A PHI-safe aggregate intake may go through steps ② to ④ before anything is approved, because review needs something to look at.
Only step ⑤'s human tick releases it, and that tick belongs to CHECK.

#### 3.3 · The renderer owns `recipe/` and REVISE never hand-writes into it
(call the renderer the unit's `kind:` row names, or `haipipe-display` as the door when the kind is unclear)
`table`, `figure`, `diagram`, `tex`, and `illustration` each name their own skill, and a hand-edited recipe is a render nobody can reproduce.
Choosing among `candidates/` is step ③ and is a person's judgment, not the renderer's.

### 4 · Direct and candidate modes
**The mode rule**: direct is the default and candidate exists only on an explicit author request.

```text
DIRECT      change the page, and record why a non-trivial change was made
CANDIDATE   leave the page UNCHANGED and place a reviewable proposal in the
            Page Type's sentence or comment surface
```
📌 Candidate mode is review material rather than a completed revision, and the page returns to direct REVISE once the author chooses.

### 5 · Exit and routing, and the one thing REVISE may never do
**The routing rule**: it may propose judgment and may never pass it.

```text
the fixed promise now works and is ready to judge  ─▶ ⑦ CHECK
another claim turns out to have no support         ─▶ ④ EVIDENCE
purpose or Aims must change                        ─▶ ② DRAFT, new round
more work under the same promise                   ─▶ ⑤ REVISE again

🚫 REVISE never closes a human gate, never labels its own version
   approved, and never routes to CLOSE
```
📌 `reopens_promise: true` appears in the receipt only when the revision DISCOVERED that purpose or Aims changed, and then the controller increments the round exactly once.

## Aims

### A1 · 🔒 The promise is fixed, and that is the phase's only test
- A1.1 · The test is stated on a concrete edit list rather than as a principle.
  Done when six edits are classified and each names its phase.

### A2 · 🧵 Land the facts before polishing the prose around them
- A2.1 · No page on this board carries a hole that was removed rather than filled.
  Done when every claim that had a marker either shows a landed value or still shows its marker with its id.

### A3 · 🏗 The page becomes its artifacts here, or it never does
- A3.1 · No page on this board has a projection older than the source it projects.
  Done when `cli/check.py` reports zero `projection-stale` findings.
- A3.2 · Every rendered unit on this board is cited by id in the prose that claims it.
  Done when `cli/check.py` reports zero `display-rendered-not-cited` findings.
- A3.3 · COMPILE either earns its own phase page or is recorded as permanently folded.
  Done when the split test in `QPw00 §7.2` has been applied to COMPILE and its result written here.

### A4 · 🪞 Direct and candidate modes
- A4.1 · No candidate-mode pass has changed a page.
  Done when every candidate-mode receipt shows an unchanged source hash.

### A5 · 🔀 Exit and routing, and the one thing REVISE may never do
- A5.1 · No REVISE receipt on this board routes to CLOSE or claims approval.
  Done when a receipt audit finds no REVISE row with `route: CLOSE`.

## States
### Decision Now
- [ ] 🗣 Rule whether COMPILE stays folded into REVISE or takes its own phase page
      📍 `Part` §3, the page becomes its artifacts
      🔔 `Why now` the loop's own vocabulary names seven phases including COMPILE, and COMPILE has zero lines of contract: `haipipe-page-revise` carries it, so the board says seven and ships six
      ⭐ `A ·` stay folded, and drop COMPILE from the loop's seven-phase vocabulary so the count matches the contracts: the build is the last step of the same pass, and splitting it recreates the exact 260817 failure where one phase reported the prose right and the PDF wrong
      `B ·` split it out with its own contract and page, which makes the build independently reportable at the cost of a handoff between "the prose is final" and "the file is built", which is the handoff that broke
      🛑 `Blocks` A3.3, and the loop's phase count on QPw00
      🤖 `If nobody answers` A takes effect, because the failure that folded it is documented and the split has no incident behind it

### A1 · 🔒 The promise is fixed, and that is the phase's only test
- ✅ A1.1 · Met. Six edits are classified in `§1`.

### A2 · 🧵 Land the facts before polishing the prose around them
- ⬜ A2.1 · Not measured. No sweep for removed markers has been run, and a removed marker leaves no trace to sweep for, which is itself the finding.

### A3 · 🏗 The page becomes its artifacts here, or it never does
- ⬜ A3.1 · Not met. `cli/check.py` reports `projection-stale` on `QPf5-display` for both its `.tex` and its `.docx`, and on `QPw00-page-loop` for its `.tex`.
- ✅ A3.2 · Met today. `cli/check.py` reports zero `display-rendered-not-cited` findings on this board.
- 🧠 A3.3 · Waiting on the Decision Now row above.

### A4 · 🪞 Direct and candidate modes
- ⬜ A4.1 · Not measurable yet, because no candidate-mode pass has been recorded on this board.

### A5 · 🔀 Exit and routing, and the one thing REVISE may never do
- ⬜ A5.1 · Not measurable until `QPw00r` gives the receipts a page and an audit surface.

## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-revise/SKILL.md`
  The phase contract itself, and the authority on its procedure. It also carries COMPILE.
- `page-plugins/haipipe-plugin-display/SKILL.md`
  The unit contract and the five-step walk, of which this phase owns steps ② ③ ④.
### 📤 Output files · what a BUILD writes
- `<page>/latex/<stem>.tex` and `<page>/word/<stem>.docx`
  The two projections this phase must rebuild at the end of every pass.
- `board/QPw/QPw5-revise.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw4 §4](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The frozen intake and named renderer this phase draws from, and the lane split that produced them.
- `contrasts · DRAFT` · [QPw2 §4](5-QPw-page-workflow/QPw2-draft/QPw2-draft.md)
  The phase on the other side of the fixed-promise test, which owns purpose and Aims.
- `reads · ALL` · [QPf5 §1](4-QPf-page-folder/QPf5-display/QPf5-display.md)
  The display plugin's unit contract, which wins over this page on the folder's shape.
- `reads · ALL` · [QPf6 §1](4-QPf-page-folder/QPf6-latex/QPf6-latex.md)
  The latex projection this phase rebuilds, and the reason a stale `.tex` is a finding.

## Law
- 260817 JL · 🏗 **The page becomes its artifacts in REVISE, or it never does**: nothing downstream rebuilds them
  REVISE and COMPILE were split and folded back the same day, because "the prose is right" was reported as done while the PDF carried raw comment markers and literal asterisks.
  The option rejected was leaving the build to a later phase, which loses because the reader is then the one who discovers the disagreement.
- 260816 JL · 🖼 **Cite each unit by id in the sentence that claims it**: the projections inherit placement from the prose
  A unit nobody cites is a unit neither projection places, which is how five declared display units reached LaTeX as two.
- 🔒 **The promise may not move**: the edit shape decides nothing and the fixed purpose and Aims are the phase's one test
  A revision that redefines what the page is for while calling itself an improvement is the quiet swap this rule exists to catch.
- 🧵 **An unanswered hole stays visible and keeps its id**: never estimate, infer, or quietly drop the sentence
  Removing a marker to make the page look finished is the one failure here that no later phase can detect.
- 🚫 **Rendering is not release**: a labelled candidate may be rendered and cited while its provenance question stays open
  Only step ⑤'s human tick releases it, and that tick belongs to CHECK.

## Glossary
- 🖊 **the pass**: one REVISE run, ordered LAND, ARGUE, SOUND, RENDER, BUILD.
- 🏗 **projection**: a built deliverable generated from the page source, either `latex/<stem>.pdf` or `word/<stem>.docx`.
- 🖼 **display unit**: the folder at `<page>/display/<stem>-Display<N>-<slug>/`, cited in prose by its short id.
- 🪞 **candidate mode**: an explicitly requested pass that leaves the page unchanged and files a reviewable proposal instead.

## Log
- 260818 · [DRAFT-CC] page created to complete the loop after `QPw1`, `QPw2`, `QPw3` and `QPw4`. Written from `haipipe-page-revise`, which also carries COMPILE. Five divisions: the fixed-promise test on a concrete edit list, the five-step order and why each step precedes the next, the realization of both projections with the citation rule, the direct-versus-candidate modes, and routing. Two live checker findings were written into States rather than described as risks: `projection-stale` on `QPf5-display` twice and on `QPw00-page-loop` once. COMPILE's status turned out to be genuinely unsettled, so it is the Decision Now row: the loop's vocabulary names seven phases and only six have contracts, since COMPILE has zero lines of its own.
