---
name: haipipe-page
description: >-
  The PAGE contract and router of a Board: one persistent Page combines a stable Page Type with a current Page Phase. It owns the shared frame, fixed section order, section obligations, machine write boundaries, evaluation contract, and the lifecycle vocabulary OUTLINE, DRAFT, PROBE, EVIDENCE, REVISE, COMPILE, CHECK. Page Type variants live under page-types/; the workflow lives under page-workflows/, whose head skill haipipe-page-workflow owns RUN. THREE VERBS form the callable door: CREATE scaffolds one Page, WORK ON repairs one Page, and RUN hands off to haipipe-page-workflow, which drives one Page through a bounded non-linear producer/build/judge loop with auditable receipts. RUN is deliberately not ADVANCE. Trigger: create a page, new page, working on a page, update a page, run page lifecycle, page contract, Page Type, Page Phase, outline draft probe evidence revise compile check, seven phases, which phase, rewrite Opening, section evaluation, which section, base page, /haipipe-page.
metadata:
  version: "0.33.0"
  last_updated: "2026-08-17"
  summary: "Sixteen globally unique Page Type variants now ship across six skill sets, including Task Insight and Application Brief, Intervention, and Artifact."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page · the page, as a contract you can load

`haipipe-board` is the door you walk through to RUN a board.
This skill is the door for ONE PAGE, and the spec that page is measured against. Say `create a new page on <topic>`, `working on <page>`, or `run <page>`; load it with no board open and it is a pure contract.
QC1b §1 on the design board states the test it passes: a consumer needs these rules with no board open.
Those consumers exist today: the routing verb deciding "which page, which section", the chat drawer priming a per-page session, and the variant authors in other families.

**The boundary, and it is a hard one:**

**Who owns what**: this skill holds the spec, `haipipe-board` holds the machinery.

```
haipipe-page               haipipe-board
─────────────────────            ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (cli/serve.py)
where a write may land           the checker (cli/check.py)
the base/variant model           the template file itself (ref/page-template.md)
```

This skill never CONTAINS the renderer, the server or the checker. It calls them, because a reader asking for one page should not have to know which script does what, and owning one page end to end is not the same as owning the machinery.
The authoritative template stays `haipipe-board/ref/page-template.md`; this contract cites it and must never fork it.

## 🧬 Page Types, one base

A Page's TYPE comes from one machine-readable key on the page: a filename prefix, a head `route:` line, or a frontmatter `page-type:` line.
The type decides how the Page closes, what its Content holds, and which typed records it fills through the base frame's declared extension points.
Everything else is the shared base (the model on the design board's QB4, JL 260729).
The implementation may still call this field `kind`; the contract term is Page Type.

**Type resolution**: one table for ALL types. Resolve ① to ⑤ in order and stop at the first key that matches.

```
step  machine-readable key                            Page Type             contract
─────────────────────────────────────────────────────────────────────────────────────
①     filename Skill-<n>- or Agent-<n>-               Skill / Agent mirror  for-skill
      filename Meeting-<n>-                           Meeting               for-meeting
      filename QBv<n>-                                QBv venue             for-venue
②     ─ retired 260816 · `route:` is a PLUGIN key now, not a type key ─
③     frontmatter `page-type: design`                 Design brief          for-design
      frontmatter `page-type: opening`                Paper opening         for-opening
      frontmatter `page-type: section`                Section unit          for-section
      frontmatter `page-type: narrative`              Narrative             for-narrative
      frontmatter `page-type: insight`                DIKW insight          for-insight
      frontmatter `page-type: brief`                  Application brief     for-brief
      frontmatter `page-type: intervention`           Intervention design   for-intervention
      frontmatter `page-type: artifact`               Application artifact for-artifact
      frontmatter `page-type: dash`                   Family dash           for-dash
                                                      ↳ `dash_family:` says WHICH
                                                        family · it is a field now
      frontmatter `page-type: view`                   View hub              for-view
④     filename S-<Family>-<unit>-<slug>               Stage                 for-stage
⑤     filename Q<group><n>[<face>]-<slug>             Q decision            base only
```

**Every step-③ key now resolves to exactly ONE contract (JL 260816).** `page-type: dash` used to resolve to a family of four, with the `S-<Family>-Dash` filename picking between them. Those four contracts stated one closing rule between them, character for character, so they were merged into `haipipe-page-for-dash` and the family became a FIELD:

```
page-type: dash
dash_family: section | value | display | literature      ← REQUIRED on every dash
```

`dash_family:` was a specimen-only fallback while four contracts existed and a filename could pick between them. With one contract the filename picks nothing, so the field is now required on every dash, including one wearing a `S-<Family>-Dash` filename, where the two must agree. This is the shape `QBt6-for-section` already uses with `section_kind: results`: a type key says which contract, and a field says which instance of it.

EXACTLY ONE step may claim a page, or the page is defective: a page no key matches, or one carrying two keys that disagree, is fixed on the page, never in the resolver.
**Step ② is retired (JL 260816).** `route: outward` / `route: inward` no longer resolve a Page Type, because literature and value are PLUGINS now, not types. The head line SURVIVES unchanged: `src/topic_entry_contract.py` still trusts it, and it still says which evidence lane a page's cards belong to. What it no longer does is pick a contract, so a page carrying `route:` falls through to ④ or ⑤ and is resolved by its filename like any other page.
Step ③'s `page-type:` line is REQUIRED on every type listed at that step, and it BEATS the filename.
That order settles the real collision: `QBt10-for-design` wears a Q filename and is a design brief, so `page-type: design` resolves it at ③ before ⑤ can claim it.
Each type's contract states how it closes; the base's own type, the Q decision page, closes when every Aim is met or explicitly held, and mirror and Meeting pages are NEVER counted in a board's settled totals.

`src/common.py` globs four filename prefixes, `Q`, `S`, `Agent` and `Meeting`, and that glob decides only what counts as a page at all; a `Skill-` page starts with the letter S, so it rides the `S` glob.
Membership is the glob's whole job. The table above, not the glob, decides which type a page is.
`Meeting-<n>` is generated by `cli/meetingpage.py`, and its contract is `haipipe-page-for-meeting`: talk is recorded there, ruled elsewhere.

A Page Type used by one consumer family is a VARIANT of the base: it defines Content and may populate fixed extension points in Aims, States, and Stage Contract, but it never redefines, adds, removes, or reorders those frame sections.

**A variant ships under the `page-types/` folder of the SKILL SET THAT OWNS IT (JL 260809).**
Every skill set carries its own `page-types/`, holding the page versions that skill set maintains, so the folder a variant sits in names its owner and nothing else has to.
This skill owns the BASE those variants extend, and it owns only the variants that are not about any one artifact.
The rule replaced "ships WHERE THE BOARD FAMILY MAINTAINS IT" (JL 260803), which was true only while one family held every variant; the moment the paper family took the five that describe its own artifacts, a single home stopped being able to say who maintains what.

SIXTEEN Page Type variants ship across six skill sets, and one of them must be loaded before you write the Page it governs:

```
owner            variant                        governs
──────────────────────────────────────────────────────────────────────────────
board/           haipipe-page-for-stage         S-<Family>-<unit> · one lifecycle
page-types/                                     stage of a paper or application
  the kinds      haipipe-page-for-skill         Skill-<n> · Agent-<n> · mirrors a
  any board                                     shipped unit and decides nothing
  needs          haipipe-page-for-meeting       Meeting-<n> · talk recorded here,
                                                ruled elsewhere · NEVER counted
                 haipipe-page-for-design        one division per candidate, closes
                                                on a SELECTION record

paper/           haipipe-page-for-opening       one per paper · identity, venue
page-types/                                     position, promise, Narrative handoff
  the kinds      haipipe-page-for-venue         QBv<n> · one place a paper goes
  only a paper   haipipe-page-for-narrative     claim roles, reader order, source
  has                                           allocation, and the Section map
                 haipipe-page-for-section       one reader-ordered unit, bound to
  has                                           its venue allocation · INCLUDES
                                                appendix units, lettered
                 ─ display · literature · value RETIRED 260816: every page
                   has them, so they are PLUGINS, not types (see below) ─
                 haipipe-page-for-dash          EVERY unit of one family at once,
                                                measured against the venue · never
                                                closes · `dash_family:` says which
                                                (four per-family dashes merged 260816)

subjective-      haipipe-page-for-labeling      one corpus × one label target,
label/                                          run by a human authority
page-types/

task/            haipipe-page-for-task          one task-folder · closes when a
page-types/                                     person reads a run-bound result
                 haipipe-page-for-insight       one consumer-neutral DIKW chain;
                                                Probe reaches Task/Discovery here

application/     haipipe-page-for-brief         one application identity, audience,
page-types/                                     venue, promise, and source selection
                 haipipe-page-for-intervention  settled Insights → mechanisms,
                                                components, variants, Artifact map
                 haipipe-page-for-artifact      one independently approvable delivery
                                                unit, bound to handoff + render version

view/            haipipe-page-for-view          QA inputs → readable View body →
page-types/                                     Displays → downstream consumers
```

`for-stage` stays on the board side even though only paper and application have lifecycles, because a stage page is a BOARD mechanism (chain, managed contract span, human gate) that both families instantiate; `for-section` and the rest describe a paper's own artifacts, so they left with the paper.
When a variant moves, its installed symlink still points at the old folder, so re-run `install.sh --global` (repo root) or the skill silently stops resolving.

Opening was admitted 260817 as the paper's identity-and-position page upstream of Narrative. On the same date Task admitted Insight and Application admitted Brief, Intervention, and Artifact. Their keys are globally unique: Application uses Brief rather than Opening and Intervention rather than generic Design, so step ③ never needs family context to resolve a contract.
A slide deck is NOT a Page Type: a page's talk is plugin material at `<page>/slide/<page>-deck.html`, authored by an agent and regenerated on demand (JL 260815, ruled on QPf3; the retired variant's specimen is archived on that board).
`-for-section` loads `-for-stage` the way the topic types load the topic core.
It adds the section kind, the venue contract block, and the landing surface where citation, value, and display bindings reach prose.
A section reads the venue BLUEPRINT, never the QBv catalog.
`-for-meeting` closed a gap this section itself used to record: `Meeting-<n>` pages had a generator and no contract.
Its one owned rule is that a spoken decision is not ruled until routed to the owning page.
**Display, literature and value are NOT Page Types (JL 260816).** They failed the admission law the same way the slide deck did, and for the plainest possible reason: EVERY page has them. A page shows something, a page cites something, a page states a number. A property every page carries cannot tell one kind of page from another, so it decides nothing about how a page closes, and a kind that changes no closing rule is plugin material.
Each already had a plugin lane shipping beside its type, which is what made the duplication visible: `<page>/display/` (QPf5), `<page>/bibex/` (QPf8), and `<page>/probe/` (QPf9) on the design board.
The three retired contracts are archived whole at `paper/page-types/_archive/`. The DASH over each family survives, because a dash rolls up what pages CARRY and never what type they wear.
**The four per-family dashes merged into one on the same day** (JL 260816, "maybe just one thing for all"). Their `closes when` cells were identical, character for character, all four reading `never · a dash has no gate and is regenerated each run`, and so were their type key, their venue rule, their generated-versus-authored split, and their empty-cell rule. Four contracts stating one closing rule is one type whose family is a field.
A slide page shares the deck grain the same way: one division per slide.
Each division embeds the ONE deck file live, via html-ppt's `?preview=N` single-slide mode.
The same file opened bare is the presentation.
JL ruled the embed must be the html itself, and the boardform board's QA4 is the proving page (260805).
A design page is the brief itself: its Opening states audience, goal, and constraints, and each Content division carries one CANDIDATE artifact.
It closes on a SELECTION record naming the winner and each loser's disposition.
It sits UPSTREAM of the display PLUGIN: design selects the candidate, and `<page>/display/` renders the winner.

Load the matching one before writing or fixing any Page of those types.
`haipipe-page-for-stage` names the ONE stage that reads a `QBv` Page and the four tiers deciding what crosses from that catalog into a draft.
The first two listed types also do NOT take the `create a new page` steps below: they are GENERATED by `haipipe-board/cli/skillpage.py new`, which writes the Page from its own stub and registers it in `board.md` itself, so copying `ref/page-template.md` and registering by hand produces a Page with no managed spans that the checker then reports as broken forever.
`haipipe-page-for-skill` exists because a mirror page DECIDES NOTHING, so this skill's Opening shape, which ends in `what this page decides`, leaves it with no question to ask; five skill and agent pages filled that empty slot with the same rhetorical question on 260802.

## 🎭 Seven Page Phases, independent of Page Type

A Page persists while the authority acting on it changes.
The current phase is not another Page Type and is not inferred from the edit operation.
There were four until 260817; the three splits and the failure each one allowed are in `page-workflows/haipipe-page-workflow`.

```text
phase       authority                                     load
─────────────────────────────────────────────────────────────────────────────
OUTLINE 🚧  agree the SHAPE, exit only on a person's tick page-workflows/haipipe-page-outline
DRAFT       define or reopen purpose, Aims, promised shape page-workflows/haipipe-page-draft
PROBE       turn each outline mark into a card and ask     page-workflows/haipipe-page-probe
EVIDENCE    land every promised claim's card across the evidence wall
                                                         page-workflows/haipipe-page-evidence
REVISE      improve the current promise while purpose and Aims stay fixed
                                                         page-workflows/haipipe-page-revise
COMPILE     rebuild latex · pdf · word from that prose    page-workflows/haipipe-page-revise
CHECK       judge one version and route its next authority page-workflows/haipipe-page-check
```

Resolve one invocation in this order:

```text
base Page contract
  → matching Page Type, when one exists
  → current Page Phase
  → family craft: the stage's declared craft files (and for probe, the family door's probe tooling), when paper or application adds artifact knowledge
```

The seven phases form a routing grammar, not a conveyor belt.
Each may repeat, PROBE and EVIDENCE may be skipped when the Page promises no claim it cannot support, and CHECK may route to any earlier phase.
Returning to DRAFT because purpose or Aims changed starts a new round on the same Page.

Use the authority test when the visible operation is ambiguous:

```text
the section list itself is being agreed  → OUTLINE
purpose or Aims change                   → DRAFT
a marked hole has no card open for it    → PROBE
a card is open and its answer must land  → EVIDENCE
the same purpose and Aims are improved   → REVISE
a concrete version is judged             → CHECK
```

Adding, deleting, moving, and rewriting may be DRAFT or REVISE.
The reason for the change decides.
`RUN` is the router verb now that the automatic loop has a concrete contract.
It is deliberately not called `ADVANCE`: a Page can repeat a phase, branch, HOLD, or return to DRAFT in a new round.
RUN is OWNED by the workflow's head skill, `page-workflows/haipipe-page-workflow`, and the shared packet, receipt, version, role-separation, and stop rules live in its `ref/page-run-contract.md`.

## 📑 The sections, in their fixed on-stage order

**The sections in order**: what each owes a reader, and how much a machine may write into it.

The AUTHORITY is `haipipe-board/ref/board-form.md` §4, which fixes the ON-STAGE order as five, `Opening → Diagram → Content → Aims → States`, with Files after them and the folds last. This skill adds no section to that list; the table below names the same run plus what a machine may write into each. `ref/page-template.md` carries more `##` headings than this because it also seeds the optional and folded ones.

```
#   section            owes the reader                      phase authority
──────────────────────────────────────────────────────────────────────────────────
1   Opening            the lead question + why it matters   DRAFT defines · REVISE clarifies
2   Diagram            the figure; ids in it are links      DRAFT/REVISE, within Page Type rules
3   Content            the substance, ### divisions         DRAFT defines · REVISE realizes
4   Aims               durable Content-linked targets       DRAFT; changing intent starts a round
5   States             one factual current State per Aim    any phase, from inspectable evidence
6   Files              action map + scoped Page context      DRAFT/REVISE maintain
7   folds              Discussion · Law · Lesson · Glossary · Log  the phase owning the record
```

Each section answers ONE reader question, and the same five rows define every section's contract (JL 260801, ruled on the design board's QB4 §0): **conveys**, the reader question it answers · **holds**, the elements it must contain · **source**, how the author writes it · **rules**, what binds a write · **omit**, when it may be absent.

**One reader question per section**: the question it answers, and when it may be left out.

```
section            conveys · the reader question                omit
──────────────────────────────────────────────────────────────────────
🧭 Opening          what is this page, why should I care?        never
🖼 Diagram          can I see the whole subject at once?         when no figure helps: delete
📚 Content          what does this page actually establish?      Q may · S never
🎯 Aims             what should become true, and for which Content division? never
📍 States           what is true now for each Aim, what waits?   never
📎 Files            which few files or Page fragments continue this work? allowed, advised against
🗃 folds            what was ruled, learned, changed, if needed  each optional
```

A sentence answering another section's question is MISPLACED, and the protocol names its home: substance found in Opening moves to Content, Required Inputs and Venue move to Stage Contract, prose rules move to Writing Style, intended outcomes move to Aims, current facts move to States, and temporary next steps become an Aim's optional Plan.
The full five rows per section live in the design board's `QB4` Content divisions; the authoritative source form stays `haipipe-board/ref/page-template.md`.

An Aims or States group is `### A<n> · <emoji> <name>`, taking the NUMBER, NAME and EMOJI of the Content part it answers, so the three sections line up by eye as well as by id (JL 260802; it was `C<n>` until then, which made a reader translate one letter to see that `A3.1` belonged under it, and `C<n>` still resolves). `P` is for a target belonging to no single part. Ordinary Files groups are a MENU of actions, taken as they apply: ⚙️ Engines what RUNS the subject · 📋 Contracts what CARRIES a rule to other pages · 🧪 Checks what CATCHES a page breaking one · 📥 Input files what the work READS · 📤 Output files what a BUILD writes. Their names state an ACTION, never a subject, because a subject-named group rots the moment its subject leaves the page.

`### 🔗 Related Board Pages` is the one fixed Files group. It is a selective context map between Pages, not a file dependency graph and not configuration inheritance. The fixed group name gives the checker a parser boundary; each row begins with the action-like relation that ordinary Files groups put in their heading:

```markdown
### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · EVIDENCE` · [QB7 §3](QB-research/QB7-literature.md)
  Read the evidence boundary before resolving this Page's consequential unknown.
```

The four relations are `reads`, `constrained by`, `continues`, and `contrasts`. The phase is `DRAFT`, `EVIDENCE`, `REVISE`, `CHECK`, or `ALL` (`EVIDENCE` still parses as EVIDENCE). The target is a Board-root-relative Page source. Its visible id must match that Page. Scope is `page` or one direct Content division such as `§3` or `§3.2`; a division read automatically carries the target Page's identity, Opening, and matching Aims/States group so the fragment does not arrive without its promise and current state. When one packet selects several divisions from the same target Page, identity and Opening are emitted once rather than repeated per row.

Read the current Page whole first. Then run `python3 <board-skill>/cli/pagecontext.py <current-page.md> --phase <PHASE>` and load only the returned packet. The reader follows one hop: it never traverses Related Board Pages declared by a target Page. Cycles are therefore harmless, context stays bounded, and a phase sees only rows written for it or for `ALL`. `check.py` rejects a malformed row, a path outside the Board, a dead Page, a mismatched Page id, or a missing scope before an agent can silently work without that context.

An Aim is not a task. Write `- A3.1 · target` for a result owned by Content part 3, under the group `### A3`, and `P1` only for a target that genuinely crosses parts. One division may have zero, one, or many Aims. Each Aim has a testable `Done when` and may carry a temporary `Plan`; changing Plan does not change the Aim.

The section labels are deliberately both plural: `Aims` contains Aim records and `States` contains their State records. States mirrors every Aim id exactly once: `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person or something outside this page, `✅` met with the evidence named, or `❄️` on ice, held on purpose. Each says its meaning by SHAPE (JL 260802); the old `🟡` `🟠` `⏸️` still parse. This is the AIM vocabulary and NOT the page `state:` line, which keeps its own ✅ 🟡 🔴 ⏸️ set and is checked apart. The section is a snapshot, so the reason for a transition belongs in Log. The strict one-to-one relationship is Aim to current State row, never Content division to Aim.

## 🚪 Three verbs, and this skill is the door for all three

Say any of these and this skill runs it. You never call the engine yourself.

```
📄 CREATE     /haipipe-page create a new page on <topic>   [on <board>]
🔧 WORK ON    /haipipe-page working on <page>              or just the path
🔁 RUN        /haipipe-page run <page> [from <phase>]
```

`haipipe-board` owns the machinery and this skill owns the contract, which is why the boundary above says this skill never renders, serves or checks: it does not CONTAIN that code. It does CALL it. A page is one unit of work, and a reader asking for one page should not have to know which script does what.

### 📄 create a new page on a topic

1. Resolve the board folder, and the group the page belongs to. Ask ONLY if the group is genuinely ambiguous.
2. Pick the id (`Q<group><n>-<slug>`, or `S-<Family>-<unit>-<slug>` for a lifecycle stage) and copy `haipipe-board/ref/page-template.md` to it. Never retype the shape from memory: the template's guide sentences ARE the contract.
3. Write the title so it states the page's PURPOSE, in sentence case.
4. Write the Opening: the visible paragraph above the first blank line, everything else below it.
5. Write Content as numbered parts, each opening with a caption, a `/diagram-ascii` figure and a short intro.
6. Write Aims, their States, and Files. When another Page supplies necessary context, add only the exact Related Board Pages row and scope the current phase needs.
7. Register the page in the board's `board.md` roster.
8. Build, check, and read the RENDER. Report the page's finding count, not the fact that you finished.

### 🔧 working on an existing page

Scope is the one thing this verb got wrong when it was measured. On 260802 three fresh agents were each given one sentence and nothing else, and all three found this skill unaided and drove their page to zero findings. They then disagreed completely about how far to reach: one wrote to a single file, its own page; another wrote to fifteen, including four shipped `SKILL.md` files, four `CHANGELOG.md` files, six sibling pages and the shared `board.md`. Neither was wrong on the merits, and the wide one was fixing citations a renumbering really had broken. The skill simply never said where to stop, so steps 7 and 8 below now do.

1. Read the whole target file first, including Content, Aims, States, Files and the settled folds. If Files declares Related Board Pages, resolve the current phase with `cli/pagecontext.py` and read that one-hop packet before changing prose.
2. Run the checker on it and work its list. Every finding names the rule it breaks and the part it is in, so nothing has to be read to know what to do.
3. Fix the MECHANICAL findings first, in bulk: dead `## Files` paths, a part with no figure, a figure with no caption, a group name that drifted. None needs judgment.
4. Then read for what no checker reaches: the weak-English axis, whether each part still answers one question, whether the Opening's visible paragraph says anything the title did not.
5. If a fix reveals a rule nobody wrote down, write it in three places: the owning page, `haipipe-board/ref/page-template.md`, and this file. A repair that stops at one page will be needed again next week.
6. Build, check, read the render, and report the before and after counts.
7. ONE page is the deliverable. Step 5 sends you to other files on purpose, and this step bounds it: a write outside the target page is allowed only when the page CANNOT be made correct without it, and every such write is named in the report, with the reason, file by file.
8. Never rewrite a sibling page's content. Repointing a citation your own renumbering broke is repair; rewriting the page that citation lands in is a second job, and it belongs to that page's own turn.

### 🔁 run one Page lifecycle

RUN is the automatic, bounded loop, and it lives with the workflow it drives:
saying `run <page>` here loads `page-workflows/haipipe-page-workflow`, the head
skill that combines the phase contracts, and follows its procedure.

🚫 **The dispatch stays in the session you typed it in.** A subagent is not
handed the `Workflow` tool, so `run <page>` may not be handed off to
`haipipe-page-orchestrator-agent` or any other agent. Proved 260818: that agent
was dispatched as itself for the first time and returned `blocked` with 0 steps. The
packet, receipt, role-separation, and stop rules are that skill's
`ref/page-run-contract.md`; the receipts land under
`<board>/_runs/page/<page-id>/`. This door keeps only the two rules a caller
needs before handing off: a NEW Page is CREATEd and registered here first and
then RUN starts at DRAFT, and an existing Page with no known next authority
starts at CHECK.

The engine the direct verbs call, so nobody has to remember it:

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE>'
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
```

`watch.py` rebuilds on any `.md` save, so step "build" is usually already done; a change to `.py`, `.css` or `.js` is not watched and needs the build run once.

## ✍️ What CREATE and WORK ON write to

Load this skill and `haipipe-board/ref/writing-rules.md` directly before writing.
Do not copy their requirements into an assignment prompt: a copied checklist becomes a second prose authority and drifts.
For an existing page, read the entire target file before changing any section, including Content, Aims, States, Files, and settled folds.

A CHANGE IS FINISHED WHEN IT IS ON THE RENDERED PAGE, and nobody is asked for permission on the way (JL 260801: "don't wait me to say go next time, just go ahead and don't stop until the content is updated in the Page").
The unit of work is a visible page, not an edit.
Carry every change all the way through: write the source, propagate the rule to `haipipe-board/ref/page-template.md` and to this file so a new page inherits it, run `check.py`, then confirm the RENDER rather than the markdown.
Stopping mid-way to ask for a go leaves the change half-applied, which is strictly worse than either finishing or not starting: a renamed label with a dozen sentences still naming the old one, or a rule written on one page and in no template.
Verify on the artifact a reader opens, because source-is-correct is not page-is-correct: a dead watcher and a shut `<details>` each produced a correct file and a wrong page.
The page's own source is what keeps a rewritten Opening from promising something the rest of the page does not establish.

The title is a phrase in SENTENCE CASE that says what the page is FOR (JL 260801, ruled on the design board's QB4 §8). Capitalize the first word and proper nouns and nothing else; a defined term keeps its capitals. A colon may carry a short subtitle, and that is usually where the purpose lands: `The page template: one grammar every page kind obeys` rather than `Page Template design`, which mixes two cases and names only a topic. On the Index the title is the only line a reader gets before choosing, so a title naming its subject alone makes them open the page to learn what the page was for. Sentence case is a string test a checker can own; whether the title states a purpose is a judgment and belongs to the Evaluation contract below.

The `state:` line is a row, not a paragraph (JL 260816, ruled on the design board's QPs1). After the status word come at most two ` · ` parts: what stands, then `open:` with a short list or a count. Keep the whole line under 110 characters; `check.py` warns past that. A part that could end in a period is prose: the facts belong in States and the reason in Log, so the line only points. Good: `🟡 PARTIAL · ruled, card grammar adopted · open: landing address, citation hop, tab`.

An Opening keeps one fixed physical shape: one real question paragraph, then one plain rationale paragraph.

THE FIRST BLANK LINE IN `## Opening` IS THE SPLIT (JL 260801, ruled on QB4 §1). Above it is the ONE paragraph a reader sees without clicking, joined into a single block; below it is the `More details` drawer, behind a click. Nothing reports a blank line in the wrong place, so the failure mode is a page whose Opening renders as one bare question while its explanation sits unread. The visible paragraph is 4-5 sentences, about five lines on screen: target ~450 characters, HARD CEILING 520, measured on the RENDER. 520 is what `check.py` enforces (`OPENING_MAX_STAGE_CHARS`); ~450 is the comfortable length, not the limit. Write it in PLAIN ENGLISH for a reader whose English is weak: a shorter common word always beats a precise rare one. Its shape is the question, what the question's own words mean, why that is hard, what this page decides. NEVER open with a list that will grow: name examples and say the set grows, so a fourth member never forces an edit; the roster lives in the Content division that owns it.

EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT (JL 260801, ruled on QB4 §2). Write `**Name**: what this diagram shows.` directly above the fence, one line only. A section may hold several figures, and an unlabelled one makes the reader decode it before learning what it is; the caption goes ABOVE because an explanation that arrives after the figure arrives too late.

CONTENT IS NUMBERED ALL THE WAY DOWN (JL 260801, ruled on QB4 §1). A division is `### 3 · Content`, a group inside it is `**3.2 · Group title**`, and a paragraph is `#### 3.2.1 · Its heading`; an ungrouped division numbers its paragraphs `#### 3.1 ·` straight through, so the depth of the number says whether a group exists. This is the same rule the board applies one level up with `§6` against `§6.1`. Numbering is also a defect detector: it exposes a group holding exactly one paragraph, which is the floating-group-title defect, and it gives every paragraph a name a person can say in chat.

`More details` IS A LIST OF LABELLED PARTS, NEVER ONE BLOCK OF PROSE (JL 260801, ruled on QB4 §1). Each part starts with a bold label saying what it answers, then its sentences, with a blank line between parts. The two halves of an Opening have two different readers: the paragraph on stage is read straight through by someone deciding whether to stay, while `More details` is opened by someone who already decided and is hunting one specific thing, so they scan for a label instead of reading from the top.

A FIGURE ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE (JL 260801, ruled on QB4 §2). If a row could end in a period it is prose, and it belongs in the paragraph under the figure rather than inside the fence. A figure earns its fence by being scannable; a wall of clauses in a box is slower to read than the same clauses outside it.

The rationale's FIRST job is to define the words the question itself uses (JL 260801, ruled on QB4 §1). A sharp lead question is specific, and being specific usually means naming this board's own things, so the sharper the question the more it leans on vocabulary a cold reader does not have. Give each such term one line with a REAL EXAMPLE, never a restatement: `a lifecycle-stage page carries one stage of a paper being written, such as its Results section` lands where `a lifecycle-stage page represents a stage` does not. A restatement passes the author's own eye as an explanation, because the author already knows what the word means. Only then place the page on the board (the bearing rule), and only then argue the stake: a reader who cannot parse the question cannot be told where the page sits or why it matters. Names chosen in the question bind the rest of the page and must be used identically in Content and Law.
The rationale has no required sentence count and no required rhetorical order.
Use as many short sentences as the page needs, then stop when a cold reader can say what the page asks, why that question deserves attention, and what this page owns.
Difficulty, failure, downstream effect, and a success consequence are diagnostic prompts for missing stakes, not four slots to fill and not one sentence each.

Speak about the subject whenever possible.
`This page defines ...`, `The hard part is ...`, and `It succeeds when ...` are not forbidden phrases, but a writer may not use them as a reusable scaffold.
If the paragraph still fits another page after its nouns are replaced, it is generic and must be rewritten.
Move frameworks, implementation history, evidence inventories, current status, and plans to their owning sections instead of using them to pad the Opening.

Before writing back, run a local self-check:

1. Compare the question and rationale with the whole target page; remove any promise the page does not support.
2. Remove any sentence whose only job is filling a category such as difficulty, downstream, or success.
3. Apply the noun-substitution test; wording that could introduce a sibling page is not page-specific enough.
4. Preserve one sentence per source line, English only, and the no-em-dash rule.

This self-check improves the draft but never approves it.
A fresh reviewer judges the page after the writer's context is gone.

## ✅ Evaluation contract

Evaluation asks whether the authored page satisfies its declared requirements; it does not ask whether the reviewer personally likes the format.
The requirements stay here, in the page spec and its cited template, rather than being copied into a second evaluation skill.
The evaluator is a consumer of this contract.

Resolve applicable requirements in this order:

1. The base section contract in this skill and `ref/page-template.md`.
2. The Page Type variant, when one exists.
3. The current Page Phase contract, when the review concerns work performed under DRAFT, EVIDENCE, REVISE, or CHECK.
4. The Page's own `## Writing Style`; on S Pages, also its `## Stage Contract`.
5. The local `###` division purpose and each `####` heading's immediately following `(job line)`, when present.

A more specific source may refine a broader one but may not silently contradict it.
When two sources disagree, report a requirement conflict and stop judging that criterion until the owner resolves it.

Review four distinct axes:

| Axis | Question | Judge |
|---|---|---|
| Mechanics | Is the required structure present, ordered, addressable, and internally consistent? | `check.py` |
| Function | Does this section answer the reader question the contract assigns to it? | semantic reviewer |
| Evidence | Can every factual compliance claim point to visible text, a State row, or a linked artifact? | semantic reviewer |
| Readability | Can a zero-background reader understand the section without supplying a missing premise? | fresh-context reviewer |

The review units are every present `##` section, every direct `###` Content division, and every `####` paragraph whose local job must be tested.
Use exactly four verdicts: `MEETS`, `NEEDS WORK`, `N/A`, and `NOT VERIFIABLE`.
`N/A` means a rule genuinely does not apply; `NOT VERIFIABLE` means the required evidence is unavailable and is never a pass.

When the same section changes on several pages, the batch is an additional readability unit.
Read those sections consecutively in Board order after judging them page by page.
A sentence can be clear alone and still fail in the batch when several pages reuse its opening stem, rhetorical sequence, or generic success ending.
The batch NEEDS WORK when prose is interchangeable after noun substitution or when repeated scaffolds make distinct pages sound like one form letter.
Do not repair this by demanding cosmetic synonym changes; the smallest fix is to restate each page's actual stake in its own natural order.

The report is one row per review unit:

**The evaluation row**: one row per reviewed unit, so a failed criterion points straight at its repair.

```text
unit | applicable requirements + source | verdict | evidence | smallest fix
```

Then report requirement conflicts, mechanical findings, and one page-level verdict.
The review is read-only: it never edits prose, changes an Aim State, ticks Decision Now, or closes a page.

Execution uses existing surfaces rather than a new skill:

- `check.py --strict` supplies the deterministic mechanical findings.
- The page's `✅ Quality Check` runs the complete row-by-row rubric quickly in the current page chat.
- `haipipe-board-reviewer-agent` runs the same contract in a fresh context after revision and adds the batch voice gate when several pages changed.

The quick check helps the author iterate; only the fresh reviewer tests whether the page stands on its own without conversation context.

There is NO `## Boundary` section (JL 260731, said twice). It was added by CC on 260723 and never ruled in. What a page covers is the Opening's job; point at a neighbouring page from the prose that needs it, as a `**Covered elsewhere**:` part in the Opening's drawer.

The same ruling renamed three sections: `## Question` -> `## Opening`, `## Items to Finish` -> `## Aims`, `## Where we are` -> `## States`. `src/common.py` still ALIASES every old name, so a page on the old vocabulary keeps rendering correctly. Do not read that as permission. This skill claimed the removal was finished on 260731; on 260802 the board still had 26 `## Boundary` sections and 45 of 55 pages on the old names, because a forgiving renderer means nobody ever sees the drift. `check.py` now reports every retired name as `retired-section`, which is the only reason this paragraph can be trusted.

One name is RESERVED inside States (JL 260731): `### Decision Now` holds the decisions a machine proposes and the human must make, one `- [ ]` row each carrying the ask, the options, and a recommendation.
One exception is UNSETTLED and admitted: the paper board's S pages use `### Needs JL · tick these`, which JL approved four days before this reservation, and neither ruling supersedes the other in writing; keep each board's local name until JL rules once for both (the conflict is recorded in `page-types/haipipe-page-for-stage`).
A proposal never lives only in chat: it is written there on the owning page, the human answers by ticking, and an answered row moves into the page's dated record.

The options take ONE LINE EACH, and each line says what choosing it commits you to (JL 260731: "I want the decision A, B, C, to be in a new line and explain each options, not all the options in one line").
Three labels crammed onto one line name the options and explain none, so the reader has to reconstruct the consequences before they can choose.
The recommendation is its own line, naming the letter and why it beats the others.

**A Decision Now row**: the shape a page uses to put one choice in front of a human.

```markdown
- [ ] 🗣 The ask, stated as one question
      One or two lines of context: what is true today, and what it costs.
      A · the first option, and what choosing it commits you to.
      B · the second option, and what it commits you to.
      → CC recommends B, because <the reason it beats A>.
```

**The write anchor rule (QC1b §4, from a real casualty).**
A machine write lands at a SECTION BOUNDARY, never at a byte offset: on 260730 a concurrent session spliced a `###` block into the middle of another page's `## Opening` sentence.
Appending under a named `## ` heading is safe; inserting by offset is how that damage reproduces at scale.

**The human-decision rule (QC1b §5).**
A verb reading a transcript can report what the transcript CLAIMS, not verify it.
So a machine may update an Aim's State only from evidence it can inspect, and may propose a human ruling as a `### Decision Now` row.

**Closing a row (JL 260802, amending the never-tick rule).**
A machine CLOSES a `### Decision Now` row once the human has answered it, and records the answer in the same write: which option, who ruled, when, and the words they used.
What it may never do is close a row nobody answered, or flip a page-level human gate.
The old rule left every answered row open, so a page showed decisions as pending that had been made hours earlier and acted on, which is the same drift the board exists to prevent.
Answered means the human said it: in chat, in a comment lane, or by ticking. A machine's own recommendation is not an answer, however confident it is.

## 🏷 Addressing

**How a location is addressed**: what each level of the board is called, and how it is written.

```
page        QB4            #QB4
face        QB4a           a page whose id carries its parent's number
group       #group-QB      scrolls the index, opens nothing
sentence    QB8's grammar  haipipe-sentence owns everything below the section
```

Every id inside a fenced figure renders as a link (haipipe-board 0.53.0), so a contract that names pages is itself a map.

## 📂 Files

**This skill's own files**: what ships in the folder, and what each part is for.

```
haipipe-page/
├── SKILL.md            this contract
└── CHANGELOG.md        version history
```

Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 (the section mapping and requiredness) and §8 (on-stage order) as the authority; owns no scripts.
The lifecycle packet and receipt spec moved with RUN to `page-workflows/haipipe-page-workflow/ref/page-run-contract.md` (260815); executable workflow and audit machinery remain under `haipipe-board`.
The named next step (QC1b §1): `live/chat.py`'s four hand-rolled rule strings (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`) become this contract's consumers instead of restating it, which kills the copies, one of which has already rotted once.
