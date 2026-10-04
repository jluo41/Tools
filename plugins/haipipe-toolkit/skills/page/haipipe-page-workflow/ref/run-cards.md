# Page Run Spec cards

The compact Run Spec view, one card per Run of the Page workflow; it does not
define Run authority, the owning skill under `skills/page/workflow-runs/` does.

Route is the recorded legal transition or control outcome; it is not a second
Run identity.

```text
🎯 TARGET   bounded goal
👤 ACTOR    human | automatic | agent | hybrid
⚙ ACTION   action or interaction
🚪 GATE     testable entry/exit condition
🔀 ROUTE    legal next Run Spec/control outcome
🧾 RECEIPT  durable terminal record
🖥 SPACE    Workspace bindings
🧩 SKILL    the one skill the button's run uses; the Runs panel shows it on each run
🤖 AGENT    who does the run
✍️ SIGNS    what the person signs on it, or none
```

## `Page.context`

```text
🎯 TARGET   one Page/Folder context snapshot
👤 ACTOR    agent or hybrid
⚙ ACTION   collect, resolve, freeze
🚪 GATE     identity/authorities resolved; required sources fresh; conflicts explicit
🔀 ROUTE    SELF · Page.structure · HOLD
🧾 RECEIPT  Context record and controller/Run receipt
🖥 SPACE    Folder inspection; Runtime only when independently commissioned
🔘 BUTTON   Context · Draft · ^(?:rp-context-|run-context-) · views table
🧩 SKILL    haipipe-page-context
🤖 AGENT    haipipe-page-context-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page run {page} from CONTEXT: refresh the Context record of {page}.
```

## `Page.interactive-writing.structure` · `run-structure-<MMDD>-<slug>`

```text
🎯 TARGET   whole-Page map, ordered Bullets, paragraph jobs, evidence decisions
👤 ACTOR    hybrid; one shared Run may have many participants/contributors
⚙ ACTION   SHAPE and SURVEY as internal Steps
🚪 GATE     Shape and Survey contract explicitly accepted
🔀 ROUTE    SELF/next Step · NEW_VERSION · writing/evidence Run · NEW_RUN · HOLD
🧾 RECEIPT  runs/`run-structure-<MMDD>-<slug>`.md + results/`run-structure-<MMDD>-<slug>`/runtime.yaml + Version journal
🖥 SPACE    Draft · Evidence · Runtime
🔘 BUTTON   Structure revise · Draft · ^(?:rp-struct-|run-structure-) · views table
🧩 SKILL    haipipe-page-structure
🤖 AGENT    haipipe-page-structure-agent
✍️ SIGNS    the plan
💬 PROMPT   /haipipe-page run {page} run-structure: revise ## 1 Structure of {plan} (headings, paragraph jobs, Bullet Points); no sentence changes.
```

## `Page.interactive-writing.scratch` · `run-scratch-<MMDD>-<slug>`

```text
🎯 TARGET   one Section (C1) or whole paragraph group (C1.P1); no B/symbol target
👤 ACTOR    human
⚙ ACTION   capture rough thinking; Save or Finish Scratch
🚪 GATE     Person clicks Finish; AI returns a non-empty Summary
🔀 ROUTE    SELF · CLOSE / owning Run Spec · NEW_RUN
🧾 RECEIPT  selected Outline `## Scratch` registry + paired ticket/result/runtime.yaml
🖥 SPACE    Draft · Scratch view; Run Space
🔘 BUTTON   Scratch · Draft · ^(?:rp-scratch-|run-scratch-) · views scratch
🧩 SKILL    haipipe-page-scratch
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page scratch {page} {target}: read my notes under {target} in ## 2 Scratch of {plan} and summarize what to write there.
```

Scratch does not edit the Outline's Draft prose. The registry is a live
index beside the plan, while the paired Result is the durable interaction
receipt. A closed Scratch Run is immutable.

## `Page.interactive-writing.section` · `run-section-<MMDD>-<slug>`

```text
🎯 TARGET   one named Section drafting/revision goal
👤 ACTOR    hybrid
⚙ ACTION   draft → review/rate → diagnose → revise as one Step cycle
🚪 GATE     scoped human acceptance; Bullets settled; evidence obligations ready
🔀 ROUTE    SELF · NEW_VERSION · evidence/delivery Run · NEW_RUN · HOLD
🧾 RECEIPT  paired Version/Step journal + runtime receipt
🖥 SPACE    Draft · Runtime
🔘 BUTTON   Section revise · Draft · ^(?:rp-sec-.*\.md$|run-section-) · views revise
🧩 SKILL    haipipe-page-writing
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page revise {page} {target}: review the whole section in ## 3 Draft of {plan}; keep every Point; show Before / After per paragraph.
```

## `Page.interactive-writing.paragraph` · `run-paragraph-<MMDD>-<slug>`

```text
🎯 TARGET   one fixed paragraph or contiguous paragraph group
👤 ACTOR    hybrid
⚙ ACTION   capture feedback, revise, validate, save one Step
🚪 GATE     exact scoped text accepted; dependent Bullets/evidence settled
🔀 ROUTE    SELF · NEW_VERSION · evidence/delivery Run · NEW_RUN · HOLD
🧾 RECEIPT  paired Version/Step journal + runtime receipt
🖥 SPACE    Draft · Evidence · Runtime
🔘 BUTTON   Paragraph revise · Draft · ^(?:rp-para-|run-paragraph-) · views revise
🧩 SKILL    haipipe-page-writing
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page revise {page} {target}: revise the sentences of {target} in ## 3 Draft of {plan}; keep each Point; show Before / After per sentence.
```

Ordinary feedback is a Step. Same-target reopening is a Version. Changed goal
or target is a new Run.

## `Page.revise` · `run-revise-<MMDD>-<slug>`

```text
🎯 TARGET   one target's frozen Before and After texts
👤 ACTOR    human (a Save in Draft Space → Revise) or agent (compares two texts)
⚙ ACTION   record every change as a ledger row: Before, After, kind, Why, decision
🚪 GATE     every difference has a decision
🔀 ROUTE    SELF/next Step · NEW_RUN · HOLD
🧾 RECEIPT  change ledger in results/`run-revise-<MMDD>-<slug>`/
🖥 SPACE    Draft
🔘 BUTTON   Revise edits · Draft · ^(?:rp-revise-|run-revise-) · views revise
🧩 SKILL    haipipe-page-revise
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    the edits kept
💬 PROMPT   /haipipe-page-revise {page} {target}: read the change ledger of {run} against ## 3 Draft of {plan}; settle every Before / After and say which changes to keep.
```

## `Page.roadmap` · `run-roadmap-<MMDD>`

```text
🎯 TARGET   the whole Page: the logic of its argument
👤 ACTOR    agent drafts the logic tree; the person edits it on the canvas
⚙ ACTION   read the plan's Bullets, write the logic as a tree (claim → the reasons it rests on → Bullets), draw it with draw-logic-tree (ref/draw_logic_tree.py --logic); later, revise the drawing where the person asks
🚪 GATE     every Bullet is a leaf; the person accepts the logic
🔀 ROUTE    SELF · CLOSE · Structure revise when the logic exposes a missing or misplaced Bullet
🧾 RECEIPT  studio/<stem>-roadmap.excalidraw (the source of the logic; never replaced without asking)
🖥 SPACE    Draft · RoadMap Draw view
🔘 BUTTON   Draw the logic · Draft · ^run-roadmap- · views roadmap
🧩 SKILL    draw-logic-tree
🤖 AGENT    haipipe-studio-agent (new)
✍️ SIGNS    the logic
💬 PROMPT   /draw-logic-tree draw the logic of {page} in its RoadMap: read {plan}, write the Section's argument as a tree read left to right (its claim at the left, the reasons it rests on beside it, every Bullet a row) and draw it with draw_logic_tree.py --logic; if studio/{page}-roadmap.excalidraw exists, change only what I ask and keep my edits.
```

## `Page.section-map` · `run-sectionmap-<MMDD>`

```text
🎯 TARGET   the Section map: paragraphs, each Bullet a row, a Text column and evidence cards
👤 ACTOR    agent
⚙ ACTION   rerun excalidraw_section.py from the plan and its Evidence Items; never edit the map
🚪 GATE     every plan Bullet and every Evidence Item is drawn
🔀 ROUTE    SELF
🧾 RECEIPT  studio/<stem>-sections.excalidraw (generated; its source names the script)
🖥 SPACE    Draft · RoadMap Draw view
🔘 BUTTON   Redraw the Section map · Draft · ^run-sectionmap- · views roadmap
🧩 SKILL    excalidraw-section
🤖 AGENT    haipipe-studio-agent (new)
✍️ SIGNS    none
💬 PROMPT   /excalidraw-section redraw the Section map of {page}: run excalidraw_section.py on {page} from {plan} and its Evidence Items; never edit the map by hand.
```

## `Page.evidence-item` · `re-value|cite|display-*`

```text
🎯 TARGET   one focal VALUE, CITE, or DISPLAY Result for one make-item
👤 ACTOR    agent/system/hybrid; declared human verification when needed
⚙ ACTION   LAND Supporting Results/input, execute local work, EMBED ready meaning
🚪 GATE     typed Acceptance passes; CITE/worker verification recorded when required
🔀 ROUTE    SELF · writing/delivery Run · NEW_RUN · HOLD
🧾 RECEIPT  owner-native Ticket/Result + Page RE runtime receipt
🖥 SPACE    Evidence · Runtime
🔘 BUTTON   Bind / update citation · Evidence · ^(?:re-cite-|run-citation-) · views citations
🧩 SKILL    haipipe-page-evidence
🤖 AGENT    haipipe-page-evidence-agent
✍️ SIGNS    the source check
🔘 BUTTON   Build figure / table · Evidence · ^(?:re-display-|run-display-) · views displays
🧩 SKILL    Build figure / table: haipipe-display
🤖 AGENT    haipipe-display-unit-agent
✍️ SIGNS    accepting the display
🔘 BUTTON   Bind / update value · Evidence · ^(?:re-value-|run-value-) · views values
🧩 SKILL    Bind / update value: haipipe-page-evidence
🤖 AGENT    haipipe-page-evidence-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page evidence {page} {target}: land and verify this evidence item against its Acceptance line in the Evidence Markdown, then bind its Result.
```

## `Page.delivery` · `run-delivery-<lane>`

```text
🎯 TARGET   one lane: run-delivery-webpage · run-delivery-latex · run-delivery-word
👤 ACTOR    agent/system
⚙ ACTION   rerun the lane's one Run: page.py export <page> --lane <lane>
🚪 GATE     the lane's files are at least as new as the Page
🔀 ROUTE    SELF · Page.check · HOLD
🧾 RECEIPT  none typed: the files in delivery/<lane>/ and their file time
🖥 SPACE    Delivery
🔘 BUTTON   Build · Delivery · ^run-delivery- · views preview artifacts
🧩 SKILL    haipipe-page-delivery
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page export {page} {target}: rerun this lane's one Delivery Run (page.py export --lane), then say which files changed. No new Run id, no receipt, no hash.
```

## `Page.auto-writing` · `run-auto-write-<MMDD>-<slug>`

```text
🎯 TARGET   one paragraph or Section whose Points are settled
👤 ACTOR    agent, then the person
⚙ ACTION   write → review against the rubric → rewrite, then hand Before / After back
🚪 GATE     the person accepts or sends it to a manual revise
🔀 ROUTE    SELF · Page.interactive-writing.paragraph · NEW_VERSION · HOLD
🧾 RECEIPT  runs/draft-auto-run/<run>.md + results/<run>/ (versions, rubric, runtime)
🖥 SPACE    Draft · Runtime
🔘 BUTTON   Auto write · Draft · ^(?:rp-auto-|run-auto-write-)|^rp-sec-.*\.sh$ · views reading
🧩 SKILL    haipipe-page-writing
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    adopting the draft
💬 PROMPT   /haipipe-page auto-write {page} {target}: write the sentences of {target} from its Points, review them against the rubric, rewrite, then show me Before / After.
```

## `Page.evidence-embed` · `run-evidence-embed-<MMDD>-<slug>`

```text
🎯 TARGET   one paragraph or the whole Page whose evidence is accepted
👤 ACTOR    agent, then the person
⚙ ACTION   take accepted Evidence Results; write Answered lines into ## 1 Structure
           and citation keys or values into ## 3 Draft; show Before / After
🚪 GATE     the person accepts; the plan moves one evidence version (v2.5 → v2.5.1)
🔀 ROUTE    SELF · NEW_VERSION · Page.interactive-writing.paragraph · HOLD
🧾 RECEIPT  runs/draft-auto-run/<run>.md + results/<run>/ + the new plan version
🖥 SPACE    Draft · Evidence · Runtime
🔘 BUTTON   Evidence embed · Draft · ^(?:rp-embed-|run-evidence-embed-) · views table
🧩 SKILL    haipipe-page-evidence
🤖 AGENT    haipipe-page-evidence-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page embed {page} {target}: take the accepted evidence for {target} from the Evidence Markdown; write its Answered lines into ## 1 Structure and its citation keys into ## 3 Draft of {plan}; show Before / After; save as an evidence version.
```

`🔘 BUTTON` lines are what the workbench shows: `label · Space · ticket
pattern`, and optionally `· views <names>`. The Space is Draft, Evidence or
Delivery; the pattern matches a run's ticket file name, so each Space's Runs
panel can count and list the runs behind a button. Patterns accept the readable
names (`run-section-0927-cleanup`, `src/run_names.py`) and the older short ones
(`rp-sec-07`) until every Page has moved (`page.py run-names`). `views` names the
Draft views (`table reading scratch revise`), the Evidence tabs (`citations
displays values`) or the Delivery views (`preview artifacts checks`) where the
button shows, so each view lists only its own runs (JL 260927). In Delivery the
format tab (Web, LaTeX, Word, Slides) picks the builds of that format and fills
`{target}`. Under each button, `🧩 SKILL`, `🤖 AGENT` and `✍️ SIGNS` agree with its row of
`haipipe-workbench-page/ref/workbench-table.md` (`table-workbench --check --cards`); a
card's first `🧩 SKILL` is every button's, and `🧩 SKILL <button label>: a` names one
button's own (2026-10-03: one skill per button; a writing skill a run also needs is
loaded by that skill). `💬 PROMPT` is the text a
person copies to start that run in a Claude or Codex session; the panel fills in
`{page}`, `{plan}`, `{target}`, `{button}` and `{run}`.

The order and the design drawing: `servers/workbench-page/studio/page-workbench-design.excalidraw`
§ "The runs of a Page". A run opens with `page.py open-run` (one ticket,
`runs/<name>.md`), changes only the text while it is open, and closes with
`page.py close-run` when the person says so (`results/<name>/` and one log line).

## `Page.check`

```text
🎯 TARGET   one immutable built Page version
👤 ACTOR    fresh agent/hybrid, separate from producer/builder
⚙ ACTION   read-only mechanical + semantic judgment
🚪 GATE     pass or one named finding route
🔀 ROUTE    CLOSE · owning Run Spec · HOLD
🧾 RECEIPT  check Result and Workflow Runtime route record
🖥 SPACE    read-only Draft · Evidence · Runtime · Delivery
🔘 BUTTON   Check · Delivery · ^(?:rp-check-|run-check-) · views checks
🧩 SKILL    haipipe-page-check
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    release
💬 PROMPT   /haipipe-page check {page}: judge the current built version read-only and route any finding.
```

The current automated controller may keep CHECK as its terminal Gate rather
than an L4 Run. It becomes a Run only when given its own stable id, Ticket,
Result, receipt, and independent close boundary.

## Human work

Human input always points to an owning Run:

| Human act | Placement |
|---|---|
| feedback/comment inside fixed writing goal | Step in current RP Run |
| acceptance of fixed writing goal | exit Gate of current RP Run |
| branching evidence decision | Gate in Structure/Evidence Run |
| independently commissioned bounded decision | human decision Run |

Never mint another Run merely because a Workspace collected a click or note.
