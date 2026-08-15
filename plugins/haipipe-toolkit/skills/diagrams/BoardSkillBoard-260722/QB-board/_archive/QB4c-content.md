# Page Content: divisions, paragraphs, markers
state: 🟡 PARTIAL · grammar settled, composition and icon items open
owner: CC
method: two heading levels, depth carried by numbering; the group-title marker and its icons live with the grammar they depend on
session: 55a58f3b-66e1-4e55-951b-1e515691e52b
## Question
How is a page's `## Content` written and rendered: which heading levels exist, what a paragraph heading is, where an S page's blueprint comes from, and what a whole-line bold means?
The grammar was settled on `QB4` (the former QA4) and moved here verbatim.
The open work moved with it: creation-time blueprint composition, the 20 mislabelled bold lines, and the four icon forks absorbed from the retired icon-automation page.


## Boundary
- ✅ Covered here
  The two-level `###`/`####` grammar, the job line, the S blueprint sources (stage → venue → previous contracts), the group-title marker, and the sentence-apparatus demo.
- ↪ Covered elsewhere
  The fixed on-stage order: `QB4`. What a sentence's apparatus IS: the `QAb` group.
  The source side is §4 below. How a topic becomes pages and groups in the first place: `QA2`.

## Diagram

```
 HOW A PAGE'S  ## Content  IS WRITTEN  ·  two levels, one marker, one source
 ═══════════════════════════════════════════════════════════════════════

 §1 THE GRAMMAR · two heading levels, depth carried by the numbering
 ───────────────────────────────────────────────────────────────────────
   📚 ## Content              required on S · optional on Q
   └── 🗂 ### division         folds on its own · one part of the argument
        │   ▧ face diagram    first fenced block under the heading (RULE 260731)
        ├── 📄 #### P1 …       ALWAYS one paragraph, never bold
        │    └─ (job line)     grey-italic scan hook, ≤120 chars, right below
        └── ✏️ sentence        one per source line · may carry ⚑ apparatus
                                > Citation: / Value: / Display: / Q-consumer:
                                > Link: / Note: / JL: / CC:  fold under it

 §2 THE MARKER · a whole-line **bold** is a GROUP TITLE, not a paragraph
 ───────────────────────────────────────────────────────────────────────
   **bold line**  ──▶  🔹 GROUP TITLE   (div.gt > span.gi, emoji at its head)
        head has an emoji ─▶ used  ·  none ─▶ default 🔹  ·  build.py never guesses
   ⚠️  20 of 36 bold lines lead PROSE, not items ─▶ WARN bold-not-a-group-title

 §3/§4 THE SOURCE · composed ONCE at  stage.py new , the page then owns it
 ───────────────────────────────────────────────────────────────────────
   🧩 stage tmpl  ──▶  🏛 venue tmpl  ──▶  📎 prev contracts  ──▶  🗂 ### headings
     base jobs         reader rules       accepted inputs        written once,
     artifacts+gate    can refine,        linked+summarized      author-owned;
                       cannot delete      never copied whole     build.py renders
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/board.excalidraw&frame=QAa3

## Content
### 1 · What Content conveys
```
📚 Content · answers: what does this page actually establish?
──────────────────────────────────────────────────────────────
conveys   the page's own product: the argument, the design, the section
holds     🗂 ### divisions that fold on their own, each opening with its
          face diagram (this very block) · 📄 #### paragraph headings
          with a (job line) · ✏️ one sentence per source line, each able
          to carry ⚑ apparatus
source    author-owned ### headings · S: composed once at stage.py new,
          stage template ▸ venue overlay ▸ previous contracts
rules     only the real product, nothing that lives elsewhere: contracts
          to Stage Contract, settled flags to Where we are, open work to
          Items to Finish · a whole-line **bold** is a group title, never
          a paragraph
omit      Q may omit it · S never: the stage's product lives here
```
Content carries the material the page exists to establish after orientation.
It is required on S and optional on Q.
Each direct `###` heading becomes one named, collapsible subsection so readers can see the argument's parts before choosing which details to open.
On Q, Why this matters appears first; on S, an optional Stage Record moves to Opening when supplied and the remaining stage substance stays here.
Since 260731 the figure above is the RULE, not a flourish: each division opens with its FACE DIAGRAM, the first fenced ascii figure directly after the `###` heading, stating the division's concept at high level (JL: "after the subsection name, add the diagram-ascii to explain in high level about this section's concept or content"); this page's four divisions are the worked example.

#### Content holds the real thing only (S)
An S page's Content is the stage's own product and nothing else (JL 260725).
For a manuscript section page that means the section itself: its parts, its paragraphs, its prose, so a reader who opens Content reads the Results section rather than a folder of working material about it.
Three kinds of material that accumulate around a stage belong outside Content: the inherited venue or writing contract goes to Stage Contract inside Opening, settled flags and corrections go to Where we are because they report what is now true, and anything still owed goes to Items to Finish.
The heading names the stage for exactly this reason, reading `📚 Content · Main 7 §6 Results` rather than a subsection count: a count invites the page to accumulate boxes, while a name asks whether what follows really is the Results section.
That label is derived from the page title, so a page whose artifact carries its own number states both: the board index number and the artifact number are usually offset, and a title like `S Main 7 · §6 Results` stops them competing on the same screen instead of leaving the reader to work out which `7` is meant.

#### Heading levels inside Content
Two levels, and the depth is carried by the numbering rather than by the heading level (JL 260725).
Every division that holds content of its own is a direct `###`, so it folds independently; everything one step inside it is `####`, always.
On a manuscript section page that reads: each subsection is `### §6.1 Main Results` and each paragraph is `#### P1. …`, while a section with no subsections carries one division for itself, `### §1 Introduction`, with its paragraphs directly under it as `#### P1. …`.
The board folds exactly one level, so a page that nested subsections under a section-level `###` would collapse a whole ten-paragraph section into a single box and lose per-subsection folding; numbering the headings keeps the hierarchy legible without asking the renderer for a second fold level.
A section-level heading appears only when it holds prose of its own, which for a flat section is its paragraphs: a page never emits a division that would open onto nothing.
The rule is checkable, which is its point: the subsection count is the number of `###` headings whose number contains a dot, so a page can be compared against the venue blueprint's declared subsection count without reading a word of the prose.

#### A paragraph heading is not a group title
`####` renders as its own level: no icon, one size below a group title, its own spacing (JL 260725).
Before that it was flattened to `**bold**` on the way in, and a full-line bold is the group-title construct, so every paragraph arrived on the page wearing 🔹 and claiming to lead a run of items.
Deleting the icon would have hidden the mistake rather than fixed it, because the page was not over-decorating a paragraph: it was calling the paragraph something it is not.
The two levels now say different things and 🔹 means only what it always meant, a sentence that leads the items beneath it, which is why a real group title such as `🔹Settled Flags` still carries it.
A full-line `(…)` written directly under a paragraph heading is that paragraph's job, and it stays on stage in grey italic: it is the scan hook that lets a reader see what each paragraph does without reading the prose, so hiding it behind a click would cost a click per paragraph to recover the thing it exists for.
Only the line immediately after the heading is read that way, and the venue template caps it at roughly 80 to 120 characters, because a job line long enough to be mistaken for prose has stopped being a scan hook.

#### Content blueprint sources
An S page's Content is composed once, when `stage.py new` creates the page, from four layers:

1. The shared board shell fixes the visible page order but does not invent disciplinary content.
2. The stage template supplies the base subsection jobs, required artifacts, and gate conditions.
3. The venue template overlays reader expectations, section conventions, length, terminology, claim boundaries, and writing style.
   It may refine the stage blueprint but cannot erase a stage-required artifact or gate.
4. Previous Stage Contracts supply accepted inputs and visibly unresolved requirements.
   They are linked and summarized, never copied whole into the new page.

Resolution order is fixed: stage first, venue second, previous contracts third; the shell fixes layout only and never competes on content.
The creator materializes the result as explicit direct `###` headings with guide text in the new Markdown, and from then on the page owns those headings.
No later pass takes them back: `build.py` is render-only and never regenerates the blueprint, and `stage.py sync` refreshes only the managed Stage Contract block, never authored Content.
A stage or venue template edit after creation surfaces as an explicit staleness warning (the stored `contract-source-hash` no longer matches); a human decides what to adopt, and nothing rewrites silently.
Stage Contract remains a separate provenance and dependency layer, not a second copy of Content.

#### Sentence apparatus
A sentence can carry hidden apparatus: `>` lines written directly beneath it fold under the sentence, which shows a ⚑ badge until clicked.
> Note: this row is the demonstration; it was hidden until you clicked the sentence above.
> Link: `QB5a-evidence-card.md` holds the decision; inline-marker chips are its open item.

Typed lanes name what each attachment is, and review threads join the same drawer.
> Citation: a `\cite{TOADD}` placeholder resolves here once its key lands in the paper's .bib.
> Value: a `{VAL:? …}` placeholder surfaces here with the number it owes.
> Display: a DR id points at the `0-displays/` asset the sentence relies on.
> Q-consumer: a `[Q-Section-n]` bracket binds the sentence to its probe record.
> CC: threads like this one hide with the evidence they discuss.
> Note: this line was added FROM THE PAGE via the new POST /_board/sentence endpoint (smoke test, 260725).

A `>` run that opens a section with no sentence above it renders exactly as before, and the supporting folds never fold apparatus.



### 2 · The group-title marker, and who fills it
```
✏️ a whole-line **bold** renders as a 🔹 GROUP TITLE (a sentence leading a run of items)
──────────────────────────────────────────────────────────────────────────────────────────
  🔸 emoji at its head → used  ·  none → default 🔹  ·  build.py never guesses
  ⚠️ 20 of 36 bold lines lead PROSE, not items  →  WARN bold-not-a-group-title
  🖐 who fills the 11 real blanks?  build.py can't (static); serve.py can (OAuth + SDK)
```
A whole-line `**bold**` is a GROUP TITLE: it renders as `div.gt > span.gi`, and the span carries an emoji.
Write one at the head of the bold text and it is used; write none and the renderer supplies the default 🔹, because `build.py` has no brain and must never guess (`GT_ICON` in `src/body.py`).
That is the whole hand-written mechanism and it has worked since 260723.

#### P1. A group title has to actually lead a group
(the rule that was ruled and never enforced, and the number that shows it)
A group title is a line that leads a run of items. A paragraph is never written in bold, which is §1's rule, and a `####` heading is what a paragraph gets instead.
Counted 260726: this board carries 36 whole-line `**bold**` lines, and 20 of them are followed by prose rather than by a run of items.
Each of those 20 renders as a decorated 🔹 sitting in front of a paragraph, which is the exact confusion §1 was written to remove, one level up.
`check.py` now reports them as `bold-not-a-group-title`; the paper board, written after the ruling, scores zero.

#### P2. Automatic assignment is a live-layer job, and it is blocked on P1
(absorbed from the retired icon-automation page on 260726)
`build.py` is a static generator with no network and no model, so automating the choice there would mean keyword guessing against free-form sentences.
`serve.py` already holds an OAuth login and the SDK, so an endpoint there could read a page, find the group titles with no emoji, and fill them, exactly as the ➕ affordances already write single lines into the markdown.
It is blocked on `P1` rather than on effort: assigning icons to a set that is 55% mislabelled would decorate the mistakes instead of revealing them.
Of the 36 lines today, 5 carry a hand-written icon and 11 are genuine group titles still on the default, so the population that actually wants filling is 11, not 36.



### 3 · Each page shapes its own Content
```
one grammar, two axes : the base fixes the frame, the page KIND fills it
──────────────────────────────────────────────────────────────────────────────────────────
  🔒 BASE, every page kind : ### folds on its own · #### is always a paragraph
     └ these two are the only constraints that are mandatory
  🎛 VARIANT, per page KIND : division names, numbering, count, the §-shape default
     └ set by the owning skill (e.g. haipipe-paper-stage)
```
Division names, numbering, and count are the page's own call (JL 260729): the `§`-numbered manuscript shape is the default for manuscript-like pages, never a mandate.
Two mechanical constraints are all that remain fixed, because the renderer folds exactly one level: a direct `###` is a division that folds on its own, and `####` is always a paragraph heading inside one.
A page may also source Content from files beside it, with `![[path]]` / `![[path#Section]]` embeds (`ref/board-form.md` §5), so a subject folder can carry the material and the face stays the argument.
And since 260729 Content holds ONLY what the author wrote: the Question rationale no longer auto-joins as a first subsection, because it moved to Opening's drawer (`QB4a`).
This flexibility is the variant axis of the base/variant model on `QB4`: a page KIND fixes Content's default blueprint through its owning skill, so the manuscript shape is the Stage kind's default supplied by `haipipe-paper-stage`, and the base mandates only the two fold-level constraints above.

### 4 · The source: Q optional, S required
```
composed ONCE at `stage.py new`; the order is fixed, then the page OWNS the result
──────────────────────────────────────────────────────────────────────────────────────────
  1. 🧩 stage tmpl → base jobs, required artifacts, gate
  2. 🏛 venue tmpl → refines reader rules; cannot delete a required artifact or gate
  3. 📎 prev contracts → accepted inputs; linked and summarized, never copied whole
  4. 🗂 ### headings → written once, then author-owned; build.py only renders
```
Use direct `###` headings for coherent substantive parts; each becomes one collapsible Content subsection.
On S, an optional exact direct `### Stage Record` is orientation metadata and moves into Opening collapsed when supplied, while every other subsection remains under Content.
Do not maintain a second live copy of stage substance.
Content holds the stage's real product and nothing else: the inherited contract goes to `## Stage Contract`, settled flags and corrections to `## Where we are`, and anything still owed to `## Items to Finish`.
The rendered heading names the stage rather than counting subsections, so a name that does not describe what a reader finds there is the signal that something has crept in.

Write one sentence per source line, because the page gives each prose line its own row.
A sentence may carry apparatus: `>` lines written directly beneath it fold under that sentence, with typed lanes naming the attachment (`> Citation:`, `> Value:`, `> Display:`, `> Check:`, `> Q-consumer:`, `> Link:`, `> Source:`, `> Note:`) and `> JL:` / `> CC:` threads joining the same drawer.
Adjacency is the only binding, so a lane placed after a paragraph attaches to whatever line precedes it; the full grammar is `QB5a`.

For S creation, use this precedence:

1. Stage template defines the base jobs, artifacts, and gate.
2. Venue template refines reader expectations, section conventions, length, terminology, claim boundaries, and style without deleting stage-required work.
3. Previous Stage Contracts add accepted inputs and unresolved requirements.
4. The creator writes the resolved structure into this page as explicit direct `###` headings.

These are creation inputs, not three live backing documents.
`build.py` only renders the materialized Markdown.
`requires` and `style-from` continue to expose dependency and writing provenance in Stage Contract, while Content remains author-owned.

## Items to Finish
### Template composition and blueprint
- [ ] 🧬 S Content can be instantiated from stage and venue templates
      The creation path must resolve the stage template as the base blueprint, overlay the venue's section and writing constraints, add previous-stage requirements, and write the resulting direct `###` headings into the new Markdown.
      The composition rule is now specified here and mirrored in the template (`ref/q-template.md`); `stage.py new` still needs the template-resolution input and materializer.

### Group title automation work
- [ ] 🧹 The 20 bold lines that are not group titles are fixed first
      Counted 260726: of 36 whole-line `**bold**` lines, 20 are followed by prose rather than by a run of items, so they render as a 🔹 group title in front of a paragraph.
      §1 already forbids this and nothing enforced it; `check.py` now reports each one as `bold-not-a-group-title`.
      This blocks the icon work below: assigning icons to a set that is 55% mislabelled would decorate the mistakes rather than reveal them.
- [ ] 🔀 How icon assignment triggers   (from the retired icon page)
      A button (one click, cheap, controllable, reversible) against auto-on-save (spends money on every save and edits the markdown while you type).
      Every write affordance built since the icon question opened is button-triggered, so this may close by precedent rather than by argument; see `QB4`'s Discussion (the group-title icons thread).
- [ ] 🤖 Model and overwrite policy   (from the retired icon page)
      Which model picks the emoji, and the rule that only group titles WITHOUT an emoji are filled, never overwriting what an author wrote.
      Picking an emoji is a small job, so a small model should do it.
- [ ] 📄 Scope   (from the retired icon page)
      One page at a time, or the whole board in a pass.
- [ ] 🔨 Built and verified   (from the retired icon page)
      A `serve.py` endpoint plus a page button; assigned emoji are visible in the markdown, editable by hand, and revertible.

### Content flexibility and display
- [x] 📐 Content is flexible per page, and the auto first subsection is gone
      JL 260729: each page shapes its own Content; the two fold-level constraints stay; the Q rationale renders in Opening (`QB4a`), so Content is exactly what the author wrote.
- [ ] 👁 The paragraph job line becomes a hover-reveal at the end of the heading   (JL 260731)
      Today the `(…)` job renders as a grey-italic line ON stage under the `####` heading (`.pj` in `src/body.py`, §1 "A paragraph heading is not a group title"); JL wants it tucked to the END of the heading and shown only on hover, the way a sentence carries its apparatus.
      This REFINES rather than breaks the 260725 on-stage ruling: that ruling rejected hiding the job behind a CLICK because the scan hook would then cost a click per paragraph to recover; HOVER costs no click, so the hook stays free and the grey line leaves the stage.
      Fork to confirm: hover (CSS-only, zero-click, instant) vs the sentence's click-drawer (`⚑` on a `<details>`); recommend hover here precisely because the job is a scan hook, not evidence. Renderer touch is `.ph`/`.pj` in `src/body.py`.
- [ ] 🖼 Each Content division opens with its face diagram
      PROPOSED: ruled by JL 260731 in Discussion ("please add it as a rule that after the subsection name, add the diagram-ascii to explain in high level about this section's concept or content"), closing the fork opened on the canvas 260729.
      The grammar stays positional, no new syntax: the FIRST fenced ascii figure directly after the `###` heading is the division's face diagram.
      Shipped as an authoring rule: §1 states it, `ref/q-template.md`'s Content guide teaches it, and this page's four divisions are the worked example.
      Still open: renderer promotion (pin and rank like the page's headline ▧ ASCII) and the retrofit pass over existing boards' divisions.

### Face ownership
- [ ] 🧠 JL confirms this face owns the Content grammar
      Carved 260729 from QB4 §3 and §8 with the text verbatim; the history stays on `QB4`.

## Where we are
The grammar is settled and live on every board; what is open moved here with its sections: `stage.py new` does not yet materialize template-derived `###` headings, 20 bold lines still render as false group titles, and the icon automation is blocked on that cleanup.
JL ruled the per-division face diagram on 260731 (the Discussion line below); the authoring rule shipped the same round in §1, the template guide, and this page's own four divisions.

### Decision Now
- [ ] 🖼 Tick the shipped face-diagram rule
      PROPOSED: ruled in your Discussion line and shipped 260731 (§1, the template guide, four worked examples on this page); a tick closes the matching Items row.
      Still yours to rule separately: the retrofit, new pages only or a pass over existing divisions, and whether the renderer later pins the face diagram the way the headline ▧ ASCII is pinned.
- [ ] 👁 Pick hover or drawer for the paragraph job line
      Recommended: hover, because the `(…)` job is a scan hook and hover keeps it zero-click (the 260725 ruling only rejected paying a CLICK); the alternative is the sentence-style ⚑ drawer.

## Files
### Engines
- `src/body.py`
  The two heading levels, the job line, and `GT_ICON` (the 🔹 default).
- `src/page_question.py`
  `render_content` and the division folding.
- `check.py`
  `bold-not-a-group-title`, the enforcement half of the marker rule.

### Specification
- `ref/board-form.md`
  The graduated spec of the grammar.

## Discussion
> JL: For each content's subsection, please add it as a rule that after the subsection name, add the diagram-ascii to explain in high level about this section's concept or content.
> CC: Shipped 260731 as the rule: §1 states it, the template guide teaches it, and this page's four divisions each open with their face diagram; the retrofit over existing boards and the renderer's pin-and-rank remain yours to rule on the Decision Now row.

## Log
260801 · §1 renamed "What Content conveys" and its face diagram reshaped to the five-row protocol (conveys · holds · source · rules · omit) on JL's ask; the retired icon page's mentions reworded so the reused QD4 id stops mislinking; master view on QB4 §0
260731 1615 · Fixed the render error: a literal triple-backtick sat INSIDE two fenced diagrams (top ## Diagram + §1), which closed the fence early; reworded to "fenced block". Also dropped em-dashes (JL rule) and made all four face diagrams alignment-robust (emoji at line-starts, inline separators, no fragile columns)
260731 1520 · Redrew all four in-Content face diagrams to one house style (concept title → ─ rule → emoji-anchored rows → ──▶ arrows); replaced the mixed tree/bare-lines/dashed-table/pipeline idioms JL called ugly
260731 1500 · Added the missing ## Diagram ASCII head (grammar / marker / source), matching QB4b and QB4d; the excalidraw frame link kept below it
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · JL ruled the face diagram in Discussion; the rule shipped in §1 and the template guide, and this page's four divisions each gained theirs as the worked example (0.72.0)
260731 · JL reaffirmed the per-division diagram ask; both pending forks (🖼 diagram grammar, 👁 job-line hover) surfaced as Decision Now rows; the related Cn/Hn chip collision shipped on QB5d the same round
260731 1120 · Recorded two JL Content refinements as open items: (1) 👁 the `(…)` paragraph job line moves to a hover-reveal at the end of the heading, framed as a refinement of the 260725 on-stage ruling (hover costs no click); (2) sharpened the 🖼 per-division diagram item with a positional face-diagram grammar
260729 · JL's canvas note on the QA0 frame recorded as an open item here: per-division ascii diagrams, a fork on this grammar
260729 · §3 tied to the base/variant model on QAa0: a page kind fixes Content's default blueprint through its owning skill; headings simplified and the provenance parentheticals dropped on JL's ask
260729 · Flexibility decided (JL: "each page can have its own content structure"): the manuscript shape becomes the default rather than the mandate, embeds can source content from a page's own folder, and the auto Why-this-matters subsection left for Opening
260729 · Opened by carving QA4 §3 (Content) and §8 (group-title marker) out to their own face, text verbatim, together with the six open items that block on this grammar
