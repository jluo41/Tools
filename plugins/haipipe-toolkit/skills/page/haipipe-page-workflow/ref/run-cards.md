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
🔘 BUTTON   Context · Page · ^rp-context-
💬 PROMPT   /haipipe-page run {page} from CONTEXT: refresh the Context record of {page}.
```

## `Page.interactive-writing.structure` · `rp-struct-01`

```text
🎯 TARGET   whole-Page map, ordered Bullets, paragraph jobs, evidence decisions
👤 ACTOR    hybrid; one shared Run may have many participants/contributors
⚙ ACTION   SHAPE and SURVEY as internal Steps
🚪 GATE     Shape and Survey contract explicitly accepted
🔀 ROUTE    SELF/next Step · NEW_VERSION · writing/evidence Run · NEW_RUN · HOLD
🧾 RECEIPT  runs/rp-struct-01.md + results/rp-struct-01/runtime.yaml + Version journal
🖥 SPACE    Draft · Evidence · Runtime
🔘 BUTTON   Structure revise · Draft · ^rp-struct- · views table
💬 PROMPT   /haipipe-page run {page} rp-struct: revise ## 1 Structure of {plan} (headings, paragraph jobs, Bullet Points); no sentence changes.
```

## `Page.interactive-writing.scratch` · `rp-scratch-NN_<target>`

```text
🎯 TARGET   one Section (C1) or whole paragraph group (C1.P1); no B/symbol target
👤 ACTOR    human
⚙ ACTION   capture rough thinking; Save or Finish Scratch
🚪 GATE     Person clicks Finish; AI returns a non-empty Summary
🔀 ROUTE    SELF · CLOSE / owning Run Spec · NEW_RUN
🧾 RECEIPT  selected Outline `## Scratch` registry + paired ticket/result/runtime.yaml
🖥 SPACE    Draft · Scratch view; Run Space
🔘 BUTTON   Scratch · Draft · ^rp-scratch- · views scratch
💬 PROMPT   /haipipe-page scratch {page} {target}: read my notes under {target} in ## 2 Scratch of {plan} and summarize what to write there.
```

Scratch does not edit the Outline's Draft prose. The registry is a live
index beside the plan, while the paired Result is the durable interaction
receipt. A closed Scratch Run is immutable.

## `Page.interactive-writing.section` · `rp-sec-NN`

```text
🎯 TARGET   one named Section drafting/revision goal
👤 ACTOR    hybrid
⚙ ACTION   draft → review/rate → diagnose → revise as one Step cycle
🚪 GATE     scoped human acceptance; Bullets settled; evidence obligations ready
🔀 ROUTE    SELF · NEW_VERSION · evidence/delivery Run · NEW_RUN · HOLD
🧾 RECEIPT  paired Version/Step journal + runtime receipt
🖥 SPACE    Draft · Runtime
🔘 BUTTON   Section revise · Draft · ^rp-sec-.*\.md$ · views revise
💬 PROMPT   /haipipe-page revise {page} {target}: review the whole section in ## 3 Draft of {plan}; keep every Point; show Before / After per paragraph.
```

## `Page.interactive-writing.paragraph` · `rp-para-NN_Pxx[-Pyy]`

```text
🎯 TARGET   one fixed paragraph or contiguous paragraph group
👤 ACTOR    hybrid
⚙ ACTION   capture feedback, revise, validate, save one Step
🚪 GATE     exact scoped text accepted; dependent Bullets/evidence settled
🔀 ROUTE    SELF · NEW_VERSION · evidence/delivery Run · NEW_RUN · HOLD
🧾 RECEIPT  paired Version/Step journal + runtime receipt
🖥 SPACE    Draft · Evidence · Runtime
🔘 BUTTON   Paragraph revise · Draft · ^rp-para- · views revise
💬 PROMPT   /haipipe-page revise {page} {target}: revise the sentences of {target} in ## 3 Draft of {plan}; keep each Point; show Before / After per sentence.
```

Ordinary feedback is a Step. Same-target reopening is a Version. Changed goal
or target is a new Run.

## `Page.evidence-item` · `re-value|cite|display-*`

```text
🎯 TARGET   one focal VALUE, CITE, or DISPLAY Result for one make-item
👤 ACTOR    agent/system/hybrid; declared human verification when needed
⚙ ACTION   LAND Supporting Results/input, execute local work, EMBED ready meaning
🚪 GATE     typed Acceptance passes; CITE/worker verification recorded when required
🔀 ROUTE    SELF · writing/delivery Run · NEW_RUN · HOLD
🧾 RECEIPT  owner-native Ticket/Result + Page RE runtime receipt
🖥 SPACE    Evidence · Runtime
🔘 BUTTON   Bind / update citation · Evidence · ^re-cite- · views citations
🔘 BUTTON   Build figure / table · Evidence · ^re-display- · views displays
🔘 BUTTON   Bind / update value · Evidence · ^re-value- · views values
💬 PROMPT   /haipipe-page evidence {page} {target}: land and verify this evidence item against its Acceptance line in the Evidence Markdown, then bind its Result.
```

## `Page.delivery` · `rdNN_<target>`

```text
🎯 TARGET   one web, LaTeX, Word, PDF, or render output
👤 ACTOR    agent/system
⚙ ACTION   adopt exact accepted inputs, build, check, snapshot
🚪 GATE     artifact is current and build receipt passes
🔀 ROUTE    SELF · Page.check · NEW_RUN · HOLD
🧾 RECEIPT  delivery artifact path and build time + runtime/build receipt
🖥 SPACE    Delivery · Runtime
🔘 BUTTON   Build · Delivery · ^rd\d+_ · views preview artifacts
💬 PROMPT   /haipipe-page build {page} {target}: build the {target} output from the accepted Page, then run the consistency checks.
```

## `Page.auto-writing` · `rp-auto-NN_<target>`

```text
🎯 TARGET   one paragraph or Section whose Points are settled
👤 ACTOR    agent, then the person
⚙ ACTION   write → review against the rubric → rewrite, then hand Before / After back
🚪 GATE     the person accepts or sends it to a manual revise
🔀 ROUTE    SELF · Page.interactive-writing.paragraph · NEW_VERSION · HOLD
🧾 RECEIPT  runs/draft-auto-run/<run>.md + results/<run>/ (versions, rubric, runtime)
🖥 SPACE    Draft · Runtime
🔘 BUTTON   Auto write · Draft · ^rp-auto-|^rp-sec-.*\.sh$ · views reading
💬 PROMPT   /haipipe-page auto-write {page} {target}: write the sentences of {target} from its Points, review them against the rubric, rewrite, then show me Before / After.
```

## `Page.evidence-embed` · `rp-embed-NN_<target>`

```text
🎯 TARGET   one paragraph or the whole Page whose evidence is accepted
👤 ACTOR    agent, then the person
⚙ ACTION   take accepted Evidence Results; write Answered lines into ## 1 Structure
           and citation keys or values into ## 3 Draft; show Before / After
🚪 GATE     the person accepts; the plan moves one evidence version (v2.5 → v2.5.1)
🔀 ROUTE    SELF · NEW_VERSION · Page.interactive-writing.paragraph · HOLD
🧾 RECEIPT  runs/draft-auto-run/<run>.md + results/<run>/ + the new plan version
🖥 SPACE    Draft · Evidence · Runtime
🔘 BUTTON   Evidence embed · Draft · ^rp-embed- · views table
💬 PROMPT   /haipipe-page embed {page} {target}: take the accepted evidence for {target} from the Evidence Markdown; write its Answered lines into ## 1 Structure and its citation keys into ## 3 Draft of {plan}; show Before / After; save as an evidence version.
```

`🔘 BUTTON` lines are what the workbench shows: `label · Space · ticket
pattern`, and optionally `· views <names>`. The Space is Draft, Evidence,
Delivery or Page (a Page-level run; no Space shows it); the pattern matches a run's ticket file name,
so each Space's Runs panel can count and list the runs behind a button. `views`
names the Draft views (`table reading scratch revise`), the Evidence tabs
(`citations displays values`) or the Delivery views (`preview artifacts
checks`) where the button shows, so each view lists only its own runs (JL
260927). In Delivery the format tab (Web, LaTeX, Word, Slides) picks the builds
of that format and fills `{target}`. `💬 PROMPT` is the text a person copies to
start that run in a Claude or Codex session; the panel fills in `{page}`,
`{plan}`, `{target}`, `{button}` and `{run}`.

## `Page.check`

```text
🎯 TARGET   one immutable built Page version
👤 ACTOR    fresh agent/hybrid, separate from producer/builder
⚙ ACTION   read-only mechanical + semantic judgment
🚪 GATE     pass or one named finding route
🔀 ROUTE    CLOSE · owning Run Spec · HOLD
🧾 RECEIPT  check Result and Workflow Runtime route record
🖥 SPACE    read-only Draft · Evidence · Runtime · Delivery
🔘 BUTTON   Check · Page · ^rp-check-
🔘 BUTTON   Check · Delivery · ^rp-check- · views checks
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
