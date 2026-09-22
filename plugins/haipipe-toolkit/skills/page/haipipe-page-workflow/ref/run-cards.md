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
```

Scratch does not edit the Outline's `Draft:` prose. The registry is a live
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
```

## `Page.delivery` · `rdNN_<target>`

```text
🎯 TARGET   one web, LaTeX, Word, PDF, or render output
👤 ACTOR    agent/system
⚙ ACTION   adopt exact accepted inputs, build, check, snapshot
🚪 GATE     artifact is current and build receipt passes
🔀 ROUTE    SELF · Page.check · NEW_RUN · HOLD
🧾 RECEIPT  delivery artifact fingerprint + runtime/build receipt
🖥 SPACE    Delivery · Runtime
```

## `Page.check`

```text
🎯 TARGET   one immutable built Page version
👤 ACTOR    fresh agent/hybrid, separate from producer/builder
⚙ ACTION   read-only mechanical + semantic judgment
🚪 GATE     pass or one named finding route
🔀 ROUTE    CLOSE · owning Run Spec · HOLD
🧾 RECEIPT  check Result and Workflow Runtime route record
🖥 SPACE    read-only Draft · Evidence · Runtime · Delivery
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
