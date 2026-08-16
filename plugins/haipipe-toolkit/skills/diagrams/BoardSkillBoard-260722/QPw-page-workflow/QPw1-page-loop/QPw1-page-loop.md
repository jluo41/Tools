# Page · the loop: draft, probe, revise, and check
state: 🟡 IN PROGRESS · contracts and audit pass, first live RUN closed 260805 · open: 12 gaps, the harness
owner: JL
method: define each phase by its authority over one persistent Page, execute the routes with versioned receipts, and test both legal branches and injected failures

## Opening
How does one Page move through DRAFT, PROBE, REVISE, and CHECK without turning the phases into four kinds of edits?
The Page persists while each phase changes the authority of the work.
Adding, deleting, moving, or rewriting does not identify the phase, and the loop may restart after revision.
This page defines what each phase owns, how a round moves, when returning to DRAFT begins a new round, and how an automatic RUN is audited.

**Where this page sits**: `QB4` owns the Page's fixed reading structure.
This page owns the Page's lifecycle, from choosing what it promises through deciding whether its current version can close.

**The terms**: a Page is the persistent source and rendered surface being worked on.
A phase is a mode of work defined by its authority, while an operation is a local action such as adding or deleting a paragraph.
A round is the period during which the Page's purpose and Aims stay fixed.

**Why it matters**: the same operation can belong to DRAFT or REVISE for different reasons.
Without an authority boundary, a worker cannot tell whether it is improving the current promise or silently replacing it.

**What this page does not own**: it does not decide the content of a paper, application, Q page, S page, or Skill mirror.
Those Page kinds supply their own constraints and closing gates.

## Writing Style

**Language and sentences**: Use plain English, one sentence per source line, and no em dash.
Define Page, phase, round, and operation before relying on them.

**Phase descriptions**: Give every phase its trigger, authority, write surface, exit, and forbidden move.
Describe what the phase does to one persistent Page rather than presenting four different Page kinds.

**Boundary examples**: Test DRAFT against REVISE with the same visible operation under two different reasons.
The reason and the promise being held fixed must decide the phase.

**Voice**: State the working model directly.
Keep implementation choices in States until JL rules them, then close the row and carry the ruling into Law and the owning contracts.

## Diagram

**One Page across repeated rounds**: the common route, the shorter routes, and the explicit restart.

```text
                         📄 ONE PERSISTENT PAGE
                                  │
                                  ▼
  ✍️ DRAFT ─────▶ 🔎 PROBE ─────▶ 🧵 REVISE ─────▶ 🧑 CHECK
      ↺ repeat       ↺ branch         ↺ repeat          ├──▶ ✅ close round
      │              │                ▲                 ├──▶ 🧵 revise
      │              └────────────────┘                 ├──▶ 🔎 probe
      └────────────── 🔁 new round ◀────────────────────┘

  🔒 one round   purpose + Aims fixed
  🔁 new round   purpose or Aims reopened
  🛠 operation   add · delete · move · rewrite
```

## Content

### 1 · DRAFT gives the Page a promise
**The DRAFT contract**: what enters, what DRAFT may decide, and what it hands forward.

```text
✍️ DRAFT
├── 📥 enters    page need · constraints · prior round
├── 🎯 owns      purpose · Aims · promised shape
├── 📝 writes    any Page part needed to expose the design
├── 🚩 names     unknowns · dependencies · assumptions
└── 📤 exits     one stable round contract
```
📌 DRAFT decides what this round of the Page is trying to become.

#### 1.1 · DRAFT is design authority, not first typing
(the phase is defined by what may be decided, not by whether the file was empty)
DRAFT may create the first Page, but it may also reopen a Page that already has polished prose.
It owns the Page's purpose, Aims, and promised shape for the round.
A purpose says why the Page exists, and the Aims say which durable results it promises.
The promised shape is the content structure needed to make those results visible.

#### 1.2 · DRAFT may use every editing operation
(new text is not automatically DRAFT, and old text is not automatically REVISE)
DRAFT may add, delete, move, or rewrite material while it is deciding the promise.
It may also repeat without leaving the phase while alternatives are still being tried.
Its exit is not polished prose.
Its exit is a stable purpose and set of Aims, plus explicit unknowns that later work can resolve.

#### 1.3 · DRAFT must expose uncertainty
(a provisional Page names what it does not yet know instead of hiding the gap)
DRAFT can place a provisional statement when its status is visible and its unknown has an owner.
It cannot present unavailable evidence as settled fact.
An unresolved question that matters to the promise becomes an input to PROBE.

### 2 · PROBE resolves what the Page cannot know
**The PROBE contract**: a named unknown leaves the Page, meets a real source, and returns as a result.

```text
🔎 PROBE
├── 📥 enters    question id · stake · source route
├── 🧭 owns      inquiry · retrieval · analysis
├── 🗂 writes    QA-probe · evidence record · answer
├── 📤 returns   result · source · limits · status
└── 🚫 avoids    target Page prose
```
📌 PROBE changes the Page's knowledge boundary without authoring the Page's argument.

#### 2.1 · PROBE begins with a consequential unknown
(curiosity alone does not open a probe; some Page decision must depend on the answer)
PROBE starts when DRAFT, REVISE, or CHECK finds a question whose answer changes what can be supported.
The question carries an id, the reason it matters, and a real route to evidence or a person.
The phase ends when the answer is resolved, explicitly deferred, or reported unreachable.

#### 2.2 · PROBE writes beside the target Page
(the evidence surface and the prose surface keep different jobs)
PROBE records the question, source, method, result, and limits on a probe surface.
It returns those records to the target Page by an explicit pointer.
It does not decide how the result should be narrated or silently insert finished prose into the target Page.
That landing decision belongs to REVISE.

#### 2.3 · PROBE is optional and repeatable
(the presence of an unresolved consequential question, not a fixed sequence, triggers it)
A Page with no consequential unknown can move from DRAFT directly to CHECK.
Several probes may branch from one round, and a later phase may open another probe.
Skipping PROBE is valid only when no unresolved question is being hidden.

#### 2.4 · Filing a QA-probe does not identify the target Page
(physical evidence routing and ownership of the Page-facing question are separate decisions)
The target Page is the Page whose lifecycle raised the stake-bearing Q-consumer.
A family may file the QA-probe under an evidence route such as Literature or Value without transferring the Q-consumer, A-consumer, or State to that route's topic Page.
The Paper family's S03 and S04 layout exposes the distinction: a Results Page can raise the question, a QA-probe can live beneath a Value topic, and a QA-bank file can answer it.
Treating physical placement as an ownership transfer gives one exchange two Page-facing consumer surfaces before the answer reaches prose.

#### 2.5 · One active Page bounds the consumer write
(a shared answer creates handoffs to sibling Pages rather than inline rewrites of their Content)
One PROBE run may write its declared Probe surface and the active target Page's Probe reference, A-consumer, and State.
When the same Q-executor serves other Q-consumers, the Probe surface records their references and makes the answer available without authoring those sibling Pages in the current run.
Each sibling interprets the answer and changes its own Content through its own PROBE or REVISE route, with its own version and CHECK.
This preserves one Q-executor for reuse without turning one answer into an unbounded cross-Page edit.

#### 2.6 · A projection can show the full chain without another authored copy
(one canonical reference should drive human display, agent context, and stale-source checks)
The active Page may need to show the Q-executor, bank target, state, returned answer, and limits while keeping its source concise.
A read-only projection can render that chain from the QA-probe and bank answer, while the Page source keeps the Probe reference and its own A-consumer interpretation.
The same reference should drive phase-scoped context loading and CHECK, so an author does not maintain a Probe pointer, an embed, and a Related Board Pages row for one relationship.
Missing targets, superseded answers, or changed source hashes must fail visibly rather than leave an old projection looking current.

### 3 · REVISE makes the current promise work
**The REVISE contract**: the Page changes while its purpose and Aims remain fixed.

```text
🧵 REVISE
├── 📥 enters    current Page · evidence · feedback
├── 🔒 holds     purpose · Aims
├── 🛠 owns      add · delete · move · rewrite
├── 🧾 updates   Content · Opening · States · records
└── 📤 exits     stronger version · visible remaining gaps
```
📌 REVISE improves the realization of the current round rather than redefining its promise.

#### 3.1 · REVISE is execution under a fixed promise
(the Page may change substantially while the reason it exists stays the same)
REVISE uses landed evidence, feedback, and close reading to make the current Aims true.
It may add a paragraph, delete a section, move an argument, or rewrite the Opening.
Large edits are still REVISE when the same purpose and Aims continue to describe the result.

#### 3.2 · DRAFT and REVISE are separated by one test
(ask whether the current promise still describes the Page after the proposed change)
If the purpose and Aims remain accurate without amendment, the work is REVISE.
If the work changes what the Page is for or what it promises to establish, the work returns to DRAFT.
The amount of changed text and the age of the Page do not decide the phase.

#### 3.3 · REVISE may discover a gap but may not invent its answer
(new uncertainty routes outward before it is written inward as fact)
When revision exposes a consequential unknown, REVISE names it and routes it to PROBE.
Evidence that landed is interpreted and woven into the Page.
Evidence that did not land remains a visible limit, a deferred pointer, or a reason the round cannot close.

### 4 · CHECK decides where the current version goes next
**The CHECK contract**: one concrete version is judged against its promise and routed.

```text
🧑 CHECK
├── 📥 enters    rendered version · Aims · evidence · constraints
├── 👁 owns      judgment · findings · closing decision
├── 📝 writes    comments · findings · gate record
├── 🔀 routes    close · REVISE · PROBE · new DRAFT · HOLD
└── 🚫 avoids    curing its own substantive finding
```
📌 CHECK observes and decides; another phase performs the content change it requests.

#### 4.1 · CHECK tests a version, not an abstract Page
(the checker needs a visible object and a stable promise to compare it with)
CHECK reads the rendered Page against its Aims, evidence, inherited constraints, and closing rule.
Mechanical checks may run throughout the work, but the CHECK phase is the gate that decides the version's fate.
The kind of Page supplies the gate, such as a self-audit, human approval, or an external shipping event.

#### 4.2 · CHECK has five meaningful outcomes
(a finding names the next authority instead of becoming a vague failure)
A passing version closes the round.
A content or clarity problem routes to REVISE.
A missing answer routes to PROBE and then normally to REVISE.
A broken purpose or Aim routes to a new DRAFT round.
Missing authority, evidence, tools, or a pending human ruling routes to HOLD, the honest stop that `§9` gives the automatic loop.

#### 4.3 · CHECK does not become a hidden revision phase
(judgment and execution remain separable even when one person performs both)
CHECK may add comments, findings, and a gate record.
It does not quietly rewrite the content and call the same version checked.
If the checker also performs the fix, the work changes phase explicitly and the resulting version is checked again.

### 5 · Transitions form rounds, not a rigid conveyor belt
**The transition grammar**: repetition is legal, and returning to DRAFT changes the round.

```text
📄 ROUND n · purpose + Aims fixed

✍️ DRAFT ↺ ──┬──▶ 🧑 CHECK ──▶ ✅ close
              └──▶ 🔎 PROBE ↺ ──▶ 🧵 REVISE ↺ ──▶ 🧑 CHECK
                        ▲               │                 │
                        └───────────────┘                 │
                                                        ▼
📄 ROUND n+1 ◀────────────── ✍️ DRAFT ◀──── purpose or Aims reopened
```
📌 The arrows express dependencies and routing choices, not a rule that every phase runs once.

#### 5.1 · The common order is not the only legal order
(each phase may repeat, and optional work disappears when its trigger is absent)
`DRAFT, DRAFT, PROBE, REVISE, DRAFT` is a legal history.
The first two DRAFT entries can be repeated design work in one round.
The final DRAFT means that revision reopened the promise and therefore began a new round.
A complete draft with no unknowns and no revision need may go directly to CHECK.

#### 5.2 · REVISE to DRAFT is a restart, not a forbidden edge
(the explicit restart preserves the distinction between improving and redefining)
REVISE may reveal that the current purpose or Aims are wrong.
The Page then returns to DRAFT and receives a new round, while the Page itself persists.
Earlier evidence remains available, but its relevance must be checked against the new promise.
Any earlier closing decision no longer applies to the new round.

#### 5.3 · A phase label requires a reason
(the visible sequence alone cannot classify the work)
The history should say which authority was used: promise reopened, unknown resolved, current promise improved, or version judged.
Without that reason, two identical diffs can be mislabeled as different phases and two different intentions can be mislabeled as the same one.

### 6 · Operations route by reason, not by edit shape
**The same operation under two authorities**: a compact test for ordinary Page changes.

```text
🛠 operation   ✍️ DRAFT when                 🧵 REVISE when
────────────────────────────────────────────────────────────────────
➕ add         new promise or Aim             serves a fixed Aim
➖ delete      removes a promise or Aim        removes weak or extra prose
↕️ move        changes the promised argument  improves flow under the promise
✏️ rewrite     reframes purpose or Aim         improves supported expression
```
📌 The operation says what changed in the file; the authority says which phase performed it.

#### 6.1 · Adding and deleting do not name a phase
(the same paragraph-level change can design the promise or improve its realization)
Adding a paragraph to explain evidence for an existing Aim is REVISE.
Adding a paragraph because the Page now answers a new question is DRAFT.
Deleting unsupported or duplicate prose while keeping the Aim is REVISE.
Deleting the promised result itself, or deleting its Aim, is DRAFT.

#### 6.2 · Moving and rewriting use the same test
(clarity stays inside the round; reframing opens a new one)
Moving paragraphs to improve flow under the same argument is REVISE.
Changing the argument the Page promises to make is DRAFT even if the diff is only one moved heading.
Rewriting the Opening for clarity is REVISE when the purpose stays fixed.
Rewriting it to give the Page a different purpose is DRAFT.

#### 6.3 · PROBE and CHECK use different write surfaces
(they can produce records without becoming authors of the target Page's content)
PROBE writes questions, sources, evidence, and answer records.
CHECK writes findings, comments, and gate records.
When either phase causes target prose to change, the actual content edit is performed under REVISE or a restarted DRAFT.

### 7 · One lifecycle Page holds the phases together
**The Page split rule**: each phase begins as a Content division and earns a Page only by becoming an independent question.

```text
📄 QB5 · ONE LIFECYCLE QUESTION
├── 📚 1 · ✍️ DRAFT
├── 📚 2 · 🔎 PROBE
├── 📚 3 · 🧵 REVISE
├── 📚 4 · 🧑 CHECK
├── 📚 5 · 🔁 transitions
└── 📚 6 · 🛠 operations

✂️ split test · ALL required
├── ❓ independent question
├── 🎯 own Aims + 📍 States
├── 🚪 independent closing gate
└── 📁 own continuation files

⚙️ phase skill   executable contract
📄 design Page   independently closable question
🚫 mapping       no automatic 1:1 mirror
```
📌 Shared boundaries stay together until one phase can carry and close a question of its own.

#### 7.1 · One phase does not automatically mean one Page
(a description is a division; an independently managed question is a Page)
DRAFT, PROBE, REVISE, and CHECK remain divisions of QB5 because their meanings depend on comparison and transition.
The DRAFT and REVISE boundary is easier to judge when both definitions and the operation examples stay on one Page.
The transition rules also need one home that no phase-specific Page can own alone.

#### 7.2 · A phase earns a Page by passing four tests
(the split happens only when the new Page can be worked on and closed independently)
The phase must have an unresolved question that is not merely asking for its definition.
It must need its own Aims and States rather than borrowing QB5's records.
It must have an independent closing gate and its own small continuation map in Files.
If any test fails, the material remains a division or paragraph on QB5.

#### 7.3 · Separate skills do not require separate design Pages
(an executable contract and a design question have different reasons to be separate)
A phase skill may remain separate because a worker needs to load one execution contract at a time.
That file boundary does not force the Board to create a matching design Page.
If a phase later passes the split test, QB5 keeps the shared boundaries and transitions while pointing to the new Page for that phase's independent question.

### 8 · Page Type and Page Phase are separate skill axes
**The skill composition**: the base resolves what the Page is and how the current work is acting on it.

```text
📄 haipipe-page                   the shared Page contract and router
├── 📁 page-types/                      what kind of Page persists · ten types · QB6 owns the roster
│   ├── for-stage
│   ├── for-skill
│   ├── for-venue
│   └── … seven more · for-design · for-display · for-literature · for-meeting · for-section · for-slide · for-value
└── 📁 page-phases/                     what authority acts now
    ├── draft
    ├── probe
    ├── revise
    └── check

one invocation = base + matching Page Type + current Page Phase + family worker
```
📌 Page Type and Page Phase are orthogonal, so their folder names and skill names must not collapse them into one label.

#### 8.1 · `for-*` names only Page Types
(the preposition says which persistent Page shape varies from the base)
`haipipe-page-for-stage`, `-for-skill`, and `-for-venue` keep their names and move under `page-types/`.
The roster has since grown to ten Page Types, and `QB6` owns the admission test and the list.
The grouping folder is organizational and carries no `SKILL.md` of its own.
A new Page Type is added only when a persistent Page needs a structural contract that the base does not provide.

#### 8.2 · Phase skills use direct names
(a phase is an active authority, not a Page variant)
The phase contracts are `haipipe-page-draft`, `-probe`, `-revise`, and `-check` under `page-phases/`.
They apply across Page Types and therefore do not use `for-stage` in their names.
The base first adopted the phase vocabulary without adding `ADVANCE`.
The automatic router now earns a verb named `RUN`, because it may repeat, branch, HOLD, or return to DRAFT rather than advance in one direction.

#### 8.3 · PROBE keeps one vocabulary across the boundary
(Q-consumer and Q-executor remain the two question forms; Entry is not a fifth lifecycle concept)
The target Page owns the stake-bearing Q-consumer.
The PROBE phase strips the stake into a neutral Q-executor, binds the returned A-executor, and writes an A-consumer interpretation for each consumer.
One Q-executor may serve several Q-consumers.
`haipipe-probe` remains the shared crossing protocol, while `haipipe-page-probe` applies that protocol to a Board Page.

### 9 · RUN turns the phase grammar into a bounded loop
**The executable flow**: one controller composes separate producer, builder, and judge roles without prescribing one phase sequence.

```text
📦 raw-material packet
│  Page · Type · start Phase · intent · sources · constraints · gate · limits
▼
🧭 controller
├── ✍️ DRAFT / 🔎 PROBE / 🧵 REVISE  ─▶ producer
├── 🏗 build + version snapshot       ─▶ mechanical builder
└── 🧑 CHECK exact version            ─▶ fresh read-only judge
                  │
                  ├── ✅ CLOSE
                  ├── 🧵 REVISE ──────┐
                  ├── 🔎 PROBE ───────┤
                  ├── ✍️ DRAFT round+1│
                  └── ⏸ HOLD          │
                                      └──▶ controller ↺
```
📌 RUN follows returned authority routes and stops at explicit terminals or limits.

#### 9.1 · RUN is not ADVANCE
(the verb must describe what the router can actually do)
ADVANCE suggests that one phase has one next phase and that progress always moves forward.
RUN means execute the current Page lifecycle from a named starting authority until CLOSE or HOLD.
The legal route table is dynamic: DRAFT, PROBE, and REVISE may repeat or hand off, while only CHECK may CLOSE.
Returning to DRAFT from another phase increments the round only when purpose or an Aim reopened.

#### 9.2 · The raw-material packet bounds what agents may know
(automation begins with explicit inputs rather than hidden conversational memory)
The packet names the persistent Page, stable Page Type, starting Phase, run intent, source paths, settled constraints, closing gate, and step and round limits.
A new Page is first created and registered, then RUN starts it at DRAFT.
An existing Page with no known next need starts at CHECK, allowing a cold judge to route the visible version.
A missing source, unknown gate, or ambiguous authority becomes HOLD rather than an invented input.

#### 9.3 · The controller routes but does not write or judge
(coordination is a separate authority from production and approval)
The producer performs exactly one DRAFT, PROBE, or REVISE phase and suggests a legal route.
The mechanical builder rebuilds, runs deterministic checks, and identifies the source plus render version.
The fresh reviewer performs CHECK against that exact version and returns CLOSE, REVISE, PROBE, DRAFT, or HOLD.
The controller validates and follows the route, but it cannot alter Page prose or convert a pending human gate into CLOSE.

#### 9.4 · Every loop has honest stop conditions
(bounded automation must distinguish non-convergence from quality)
The run stops on CLOSE, explicit HOLD, missing input, failed build, version mismatch, required human ruling, maximum steps, or maximum rounds.
Reaching a limit says the process did not converge within its budget.
It never says the Page passed.
The run's final state and every attempted phase remain inspectable instead of disappearing into an agent transcript.

### 10 · Audit proves process claims with receipts and fault tests
**The assurance model**: deterministic invariants, fresh semantic judgment, and direct or human evidence support different quality claims.

```text
🧾 phase receipts             what happened, by whom, to which version
⚙️ deterministic audit       legal routes · rounds · roles · versions · bounds
🧑 fresh CHECK               function · evidence · readability · local gate
🗣 human evidence            approval only where the Page Type requires it
🧪 branch + fault tests      expected success and expected refusal
```
📌 A passing process audit proves that the declared process ran correctly, not that every possible substantive claim is true.

#### 10.1 · A receipt binds action, actor, version, and route
(a prose summary cannot reveal self-approval or changed-after-check)
Each receipt records step, round, Phase, producer or judge actor, builder actor, status, source and render SHA-256 values, route, reason, artifacts, evidence, findings, and human-gate state.
CHECK additionally binds `checked_version` and a verdict.
The receipts are ordered and stored outside Page discovery under `_runs/page/<page-id>/<run-id>.json`.
The deterministic auditor independently rehashes the source and rendered files on disk; matching claims repeated inside a receipt are not accepted as artifact evidence by themselves.
The terminal CHECK record is not appended to the Page afterward, because that append would change the version it claims to approve.

#### 10.2 · Seven invariants make the loop auditable
(the highest-risk failures become machine-detectable)
The preserved raw-material packet must match the run identity, first Phase, declared gate, and limits.
Only legal phase routes are accepted, and only CHECK may CLOSE.
A non-DRAFT route to DRAFT must name the reopened purpose or Aim and increment the next round exactly once.
The producer, mechanical builder, and judge of one version must have different actor identities.
Every version id must be the two declared lowercase SHA-256 digests joined by `:`, and every receipt must begin from the preceding receipt's ending version.
CHECK must observe identical before, after, and checked ids; the auditor rehashes the current artifacts, and any later change requires a new CHECK.
A required human gate closes only with durable evidence that the person ruled.
Maximum steps and rounds terminate as non-convergence, never as a pass.

#### 10.3 · Testing covers branches and injected failures
(a green common path does not demonstrate a router)
Happy paths include DRAFT directly to CHECK and DRAFT through optional PROBE and REVISE.
Branch tests include CHECK to REVISE and back, CHECK to PROBE, and CHECK to a new DRAFT round.
Fault injection includes self-approval, mutation after CHECK, illegal route, packet mismatch, broken version continuity, symbolic hashes, missing human evidence, failed worker, non-terminal trace, and exhausted limits.
The deterministic harness must reject each injected fault for the specific invariant it violates.

#### 10.4 · Quality is evidenced, not declared absolute
(different checks justify different confidence claims)
The mechanical checker can prove structural facts, and the lifecycle auditor can prove process facts.
A fresh reviewer supplies semantic evidence that the Page performs its declared function and is readable without the drafting conversation.
Direct sources or a human gate supply claims those instruments cannot settle.
The final report therefore names the checked version, traversed branches, evidence inspected, remaining findings, gate state, and residual risk instead of saying only that quality is guaranteed.

## Aims

### A1 · ✍️ DRAFT gives the Page a promise
- A1.1 · DRAFT is defined by authority over purpose and Aims rather than by first creation.
  **Done when:** a reader can identify DRAFT in both an empty Page and a mature Page that reopens its promise.

### A2 · 🔎 PROBE resolves what the Page cannot know
- A2.1 · PROBE has an explicit trigger, write surface, return record, and exit.
  **Done when:** a reader can route a consequential unknown without letting PROBE author target prose.
- A2.2 · The target Page, Probe surface, sibling handoff, and forbidden cross-Page write are unambiguous.
  **Done when:** a family can file a QA-probe by evidence route without silently transferring Q-consumer ownership or authoring a sibling Page in the same run.
- A2.3 · One Probe reference can show the full evidence chain without becoming a second authored answer.
  **Done when:** the reference drives render projection, bounded phase context, dependency versioning, visible failure, and CHECK.

### A3 · 🧵 REVISE makes the current promise work
- A3.1 · REVISE is separated from DRAFT by whether purpose and Aims remain fixed.
  **Done when:** the same add, delete, move, or rewrite operation can be classified from its reason.

### A4 · 🧑 CHECK decides where the current version goes next
- A4.1 · CHECK judges one version and routes it to close, REVISE, PROBE, or a new DRAFT.
  **Done when:** every finding names the authority that owns the next change.

### A5 · 🔁 Transitions form rounds, not a rigid conveyor belt
- A5.1 · Repetition, optional phases, and REVISE to DRAFT are represented without contradiction.
  **Done when:** `DRAFT, DRAFT, PROBE, REVISE, DRAFT` has an unambiguous round interpretation.

### A6 · 🛠 Operations route by reason, not by edit shape
- A6.1 · Common Page edits are examples rather than phase definitions.
  **Done when:** adding, deleting, moving, and rewriting each have both a DRAFT case and a REVISE case.

### A7 · 📄 One lifecycle Page holds the phases together
- A7.1 · Each phase remains a Content division until it becomes an independently closable question.
  **Done when:** the Page names the four split tests and distinguishes phase skills from design Pages.

### A8 · 🗂 Page Type and Page Phase are separate skill axes
- A8.1 · The skill tree keeps persistent Page variation separate from current phase authority.
  **Done when:** Page Types live under `page-types/`, Page Phases live under `page-phases/`, and the base routes both without introducing an Entry phase or treating RUN as linear ADVANCE.

### A9 · 🔁 RUN turns the phase grammar into a bounded loop
- A9.1 · One automatic router composes phase producers, version snapshots, independent CHECK, legal branches, new rounds, and honest stops.
  **Done when:** a new or existing Page can run from a named Phase to CLOSE or HOLD without assuming DRAFT, PROBE, REVISE, and CHECK each run once in order.

### A10 · 🧪 Audit proves process claims with receipts and fault tests
- A10.1 · Every run is reconstructable and every critical invariant has both a passing and failing test.
  **Done when:** the durable receipt passes the deterministic auditor, fresh-context review passes the checked version, and branch plus fault coverage rejects known bad flows.

### P · Page-level
- P1 · The base Page contract either adopts this lifecycle vocabulary or explicitly leaves it family-specific.
  **Done when:** JL chooses the base-adoption option and the affected contracts are either wired or retired.

## States

### Decision Now

- [x] 🗣 Does the base Page contract adopt this lifecycle model now?
      📍 `P1` controls whether this page remains a design note or becomes shared Page grammar.
      🔔 `Why now` four phase contracts exist in the board family with no authoritative caller.
      `A ·` Add the vocabulary and an ADVANCE verb now, giving routers one door for running a named phase.
      ⭐ `B ·` Add the vocabulary and boundaries now, but wait to add ADVANCE until a router needs it; this is the smallest reversible adoption.
      `C ·` Keep the lifecycle family-specific and retire or relocate the orphaned board phase contracts.
      🛑 `Blocks` changing the base contract and wiring the four phase contracts.
      🤖 `If nobody answers` B remains the proposal, and no skill contract changes are made.
      ✅ `Ruled B` JL 260804: "Yes, correct. Please go ahead for it."

- [ ] 🗣 Can a family adapter transfer Q-consumer ownership when it files a QA-probe under an evidence topic?
      📍 `A2.2` owns the boundary between the active target Page and an evidence route supplied by a family.
      🔔 `Why now` the Paper adapter currently makes the Literature or Value topic Page canonical after another Page raises the Aim, while `QB5 §8.3` says the target Page owns the Q-consumer.
      `A ·` Allow the transfer. The evidence topic Page owns the stake, A-consumer, State, and Probe path; this keeps a self-contained topic register but makes one PROBE a multi-Page consumer write.
      ⭐ `B ·` Keep ownership on the Page that raised the Q-consumer. The QA-probe may be filed under any family route, while topic Pages show a derived rollup and receive their own lifecycle only when their synthesis changes.
      🛑 `Blocks` changing the Paper topic-entry contract and implementing the zero-copy topic projection.
      🤖 `If nobody answers` the implemented Paper topic-owned rule remains unchanged, and sections 2.4 to 2.6 stay the recommended shared boundary rather than shipped family behavior.

### A1 · ✍️ DRAFT gives the Page a promise
- 🔨 A1.1 · Written in Content with mature-Page and repeated-DRAFT cases; awaiting the human check of the model.

### A2 · 🔎 PROBE resolves what the Page cannot know
- 🔨 A2.1 · Written in Content with a separate evidence surface and explicit return boundary; awaiting human check.
- 🧠 A2.2 · Waiting on the open Decision Now row. Sections 2.4 and 2.5 state the origin-owned, one-active-Page alternative and the Paper S03/S04 case that exposed the ambiguity.
- 🧠 A2.3 · Waiting on A2.2. The Board already supports live Markdown embeds and scoped Related Board Pages, but no single Probe reference drives display, context, dependency identity, and CHECK.

### A3 · 🧵 REVISE makes the current promise work
- 🔨 A3.1 · Written in Content with the fixed-purpose-and-Aims test; awaiting human check.

### A4 · 🧑 CHECK decides where the current version goes next
- 🔨 A4.1 · Written in Content with four outcomes and a no-hidden-revision rule; awaiting human check.

### A5 · 🔁 Transitions form rounds, not a rigid conveyor belt
- 🔨 A5.1 · Written in Content with repeated phases, optional PROBE, and REVISE to DRAFT as a new round; awaiting human check.

### A6 · 🛠 Operations route by reason, not by edit shape
- 🔨 A6.1 · Written in Content with paired add, delete, move, and rewrite cases; awaiting human check.

### A7 · 📄 One lifecycle Page holds the phases together
- ✅ A7.1 · JL agreed 260804 that every phase gets a Content division by default, not its own Page; division 7 records the four tests for a later split.

### A8 · 🗂 Page Type and Page Phase are separate skill axes
- ✅ A8.1 · JL ruled 260804 that `for-*` skills belong under `page-types/`, direct phase skills belong under `page-phases/`, and the remaining layering proposal stands.

### A9 · 🔁 RUN turns the phase grammar into a bounded loop
- 🔨 A9.1 · LIVE-PROVEN with one caveat, 260805: run `260805-0216-QB8e` drove a real page CHECK→REVISE→CHECK→REVISE→CHECK→CLOSE in 5 receipts, findings 8→2→0, distinct fresh-context actors per role, audit PASS with hashes recomputed from disk (`_runs/page/QB8e/260805-0216-QB8e.json`). The caveat keeping this 🔨: `page-lifecycle.workflow.js` was NOT invocable as shipped (no Workflow harness in the live environment); the controller logic was executed by hand, and the run surfaced 11 contract ambiguities, logged below.

### A10 · 🧪 Audit proves process claims with receipts and fault tests
- ✅ A10.1 · Met 260805: the live QB8e run supplied the missing semantic CHECK, three fresh judges on three exact versions, converging 8→2→0, terminal verdict pass with zero findings; the deterministic auditor passed the same bundle with artifact hashes recomputed from disk.

### P · Page-level
- ✅ P1 · JL chose B on 260804: the base adopted the lifecycle vocabulary first; the later concrete router is now named `RUN`, not linear `ADVANCE`.

## Files

### Contracts

- `../../../../board/haipipe-page/SKILL.md` · the base Page contract that may adopt the lifecycle vocabulary
- `../../../../board/haipipe-page/ref/page-run-contract.md` · the shared raw-material packet, phase receipt, role, version, and stop contract
- `../../../../board/page-phases/haipipe-page-draft/SKILL.md` · the DRAFT phase contract
- `../../../../board/page-phases/haipipe-page-probe/SKILL.md` · the PROBE phase contract
- `../../../../board/page-phases/haipipe-page-revise/SKILL.md` · the REVISE phase contract
- `../../../../board/page-phases/haipipe-page-check/SKILL.md` · the CHECK phase contract

### Input files

- `../../../../paper/haipipe-paper/fn/` · the paper family's side: the LaTeX workers became `fn/` verbs in the 260806 one-door merge (the old `paper/workers/` sits in `paper/_old/workers/`); the loop itself lives in `page-phases/`
- `../../../../application/2-phase/` · the application family's existing lifecycle model
- `QPs-page-structure/QPs1-overall/QPs1-overall.md` · the fixed Page structure paired with this lifecycle
- `../../../01-haipipe-paper-260725/QA-design/QA5-the-probe-layer.md` · the Paper S03/S04 implementation case that exposed the difference between Probe placement and target Page ownership

### Checks

- `../../../../board/haipipe-board/cli/check.py` · catches source and rendering violations on this Page
- `../../../../board/haipipe-board/src/page_lifecycle.py` · validates routes, rounds, roles, immutable CHECK versions, human gates, and terminal state
- `../../../../board/haipipe-board/cli/pageflow.py` · audits one durable Page RUN receipt
- `../../../../board/haipipe-board/tests/test_page_lifecycle.py` · exercises happy paths, branch routes, and injected failures

### Engines

- `../../../../board/haipipe-board/ref/page-lifecycle.workflow.js` · defines the bounded producer, builder, reviewer, and routing loop; not invocable without a Workflow harness, so the 260805 live RUN drove the controller by hand
- `../../../../board/agents/haipipe-page-orchestrator-agent.md` · dispatches one non-interactive RUN and stores its exact receipt
- `../../../../board/agents/haipipe-board-creator-agent.md` · performs one DRAFT, PROBE, or REVISE phase without judging it
- `../../../../board/agents/haipipe-board-reviewer-agent.md` · performs fresh read-only CHECK on one exact version

## Law

- 260804 JL · 🗂 Page Type and Page Phase are separate axes
      The base Page contract routes both axes.
      Stable `for-*` variants live under `page-types/`, and active phase contracts use direct names under `page-phases/`.
      The grouping folders are catalogs rather than loadable skills.
      The base adopts the vocabulary and boundaries now but adds no `ADVANCE` verb until a real router requires one.
      The later router need is implemented as `RUN`, because it may repeat, branch, HOLD, or restart a round.
      PROBE retains Q-consumer, Q-executor, A-executor, and A-consumer; Entry is not introduced as another lifecycle concept.

- 260804 JL · 📄 A phase gets a Content division before it gets a Page
      QB5 remains the shared home for the four phase definitions, their boundaries, and their transitions.
      A phase moves to its own Page only when it has an independent question, its own Aims and States, an independent closing gate, and its own continuation files.
      A separate phase skill is an executable contract and does not require a one-to-one design Page.

- 260804 JL · 🔁 Make the Page flow executable and auditable
      The design question, Page skill set, automatic flow, and auditing and testing must be updated together.
      The flow must explain how work moves along the way and how the process demonstrates that it works.
      Automation cannot hide writing, judging, fixing, and approval inside one agent pass.

## Glossary

- 📄 **Page**: the persistent Markdown source and rendered surface that survives every phase and round.
- 🎭 **Phase**: a mode of work defined by the authority it may exercise over the Page.
- 🔁 **Round**: a span of work during which the Page's purpose and Aims stay fixed.
- 🔒 **Round contract**: the purpose, Aims, and promised shape that DRAFT hands to the rest of one round.
- 🛠 **Operation**: a local file change such as adding, deleting, moving, or rewriting text.
- 🔁 **RUN**: the bounded router that executes a Page from one named Phase until CLOSE or HOLD.
- 🧾 **Phase receipt**: one auditable record binding an attempted Phase to its actor, versions, reason, evidence, findings, and route.
- 🔐 **Version identity**: the SHA-256 of the Page source joined to the SHA-256 of its rendered HTML.
- ⏸ **HOLD**: an honest terminal route for missing authority, evidence, tools, human ruling, or remaining loop budget.

## Discussion

> JL: A Probe used while writing one Page may be filed beneath a Literature or Value topic, so does PROBE also have to update that topic Page and every other Page that consumes the same answer?
> CC: Not by default. The active Page owns the Q-consumer, the Probe Page owns the neutral exchange, and the bank owns its answer receipt. Another consumer gets a handoff and interprets the answer in its own lifecycle.
> JL: Can the topic Page still show every Probe and its answer without copying the same Markdown into two places?
> CC: Yes, if one canonical Probe reference drives a read-only projection, bounded agent context, stale dependency detection, and CHECK. Section 2.6 records that requirement without treating the renderer as another source of truth.

> JL: Can CHECK become an automatic AI-agent loop that repeatedly routes a newly created Page through DRAFT, PROBE, REVISE, and CHECK without turning the common route into a mandatory sequence?
> CC: Yes, as RUN rather than ADVANCE. The current authority is an input, each worker returns a route, and only CHECK may CLOSE.
> JL: What raw-material packet, execution receipt, independent reviewer, branch coverage, failure injection, stop condition, and human gate would let that loop demonstrate that the process works and Page quality is high?
> CC: Divisions 9 and 10 now define those surfaces. The process claim is deterministic, semantic quality comes from a fresh reviewer, and claims requiring a person remain at a durable human gate.
> JL: How do we prevent one agent from writing, judging, fixing, and approving its own output inside one hidden pass?
> CC: Producer, builder, reviewer, controller, and human are distinct roles. Actor and version identities make self-approval and mutation after CHECK auditable failures.

## Log

- 260806 2107 · [REVISE-CC] swept to the 260806 architecture; state line now records the 260805 QB8e live RUN instead of calling it pending, dead `paper/workers/` path repointed at `paper/haipipe-paper/fn/`, §8 tree shows all ten Page Types with QB6 owning the roster, and live prose now says QA-probe with capitalized Q-executor/A-consumer slot words
- 260806 0210 · [PROBE-CC] a 12th RUN-contract ambiguity, found by re-auditing the QB8e bundle a day later: `pageflow.py audit` now reports `artifact-version-mismatch` on the RENDER hash alone, because later innocent rebuilds changed the html while the source hash still matches `final_version`. The receipt treats source:render as one identity; the contract must say the SOURCE hash is the version's identity and the render hash is advisory (a rebuild is not a mutation), or every rebuild retroactively breaks every closed run. Also: the bundle carries no `audit` key at all, so "audit PASS" survives only in session history, which is item ⑩'s snapshot-has-no-receipt-home problem wearing a second face.
260805 · FIRST LIVE RUN, `260805-0216-QB8e`: CLOSE, audit PASS, and the run's second product is a defect list for this page's own contract, 11 items recorded in the bundle and owed fixes here. The sharpest six: ① the workflow controller is not invocable outside a Workflow harness and the contract never says what a bare caller may do; ② the producer prompt omits the judge's findings, so a strict REVISE guesses (the controller forwarded them as a disclosed deviation); ③ "the local closing rule" is ambiguous for a mid-life Q page whose Decision rows wait on JL by design, so the contract must say run-level CLOSE certifies THE VERSION, not the page's decisions; ④ `mechanical_errors` scope is undefined, and board-scoped counting would let one foreign dead link forbid CLOSE forever; ⑤ warnings do not gate CLOSE, so the semantic judge is the only defense on a WARN-only page; ⑥ fresh judges oscillate (r1s1 waived unnumbered paragraphs, r1s3 raised them), and max_steps is the only brake. Also surfaced: no run_id minting rule, no concurrency rule while a foreign session rebuilds board/, the pre-run snapshot has no receipt home, extra bundle keys pass unaudited, and the Decision Now row shape diverges between the base and page-template.md.

260805 · The Page-Types admission row MOVED to `../QB6-page-types/QPs2-page-types.md`, created after JL asked whether Page Types deserve their own Q. Measured against this page's own `§7.2` split test, the list-of-types question passes all four: independent question, own Aims and States, its own closing rule, and the `page-types/` contracts as its continuation files. This page keeps the axis split (`§8`) and the lifecycle; `QB6` keeps the list, the admission test, and the D-starred separation ruling.
260805 · JL held the separation: "I still want to separate for-literature and for-value," and named the reason that decides it: each uses ITS OWN LANGUAGE to understand the Q and the A crossing the executor wall. That is a typed-records difference, and the base says the type decides "which typed records it fills," so the separation is principled rather than preferential. Option D added and starred: two types over ONE loaded structural core, so the register and entry anatomy is never stated twice. The earlier A recommendation under-weighted the translation layer by reducing the two routes to "which bank answers."
260805 · JL proposed `-for-display`, `-for-value`, `-for-literature` as new Page Types and asked how far the list grows. Added the Decision Now row: the recommended shape admits by STRUCTURE rather than by family name, because the type-resolution rule reads the filename and `S-Literature-1`, `S-Value-6`, `S-Display-2a` and `S-Main-3` all resolve to the stage type today, while the topic shape (register + nested `probes/` entries) is one structure appearing under two family names and is already enforced by `src/topic_entry_contract.py` with no loadable contract teaching a writer the same shape. A `-for-topic` admission would key on the declared `### Q-consumer register` marker, the same signal the checker already trusts.
260804 · Moved the Probe ownership and zero-copy discussion from the Paper board to this Page lifecycle owner. Added sections 2.4 to 2.6, Aims A2.2 and A2.3, the open family-adapter ownership decision, the one-active-Page handoff boundary, and the requirement that one Probe reference drive projection, context, dependency identity, and CHECK. The Paper S03/S04 layout remains an input case rather than the owner of the generic rule.
260804 · Opened a new DRAFT round for the automatic Page flow. Added RUN as a bounded dynamic router, the raw-material packet and phase receipt, producer/build/reviewer separation, version identity, CLOSE/HOLD stops, deterministic lifecycle auditing, branch coverage, and fault injection. Updated Aims A9 and A10, continuation files, Law, Glossary, and Discussion to track implementation and fresh validation separately.
260804 · Added JL's open discussion on an automatic AI-agent quality loop: what evidence proves the Page process works, which failures and branches must be audited, and how builder, checker, fixer, and approver remain separable.
260804 · Fresh-context audits followed the new skill without conversation history, accepted the process fixture, and rejected injected self-approval, symbolic hashes, and builder/judge collapse. Their findings led to strict source/render SHA-256 validation, explicit builder identity, independent artifact rehashing, packet/run matching, and receipt-to-receipt version continuity. They also correctly refused to treat a process fixture as semantic Page quality. Live Claude Workflow execution remains an honest open gate.
260804 · JL chose base-adoption option B and approved the `page-types/` plus `page-phases/` split. Added division 8, closed P1, and recorded that `for-*` belongs only to Page Types, phase skills use direct names, PROBE retains its four Q/A forms without introducing Entry, and `ADVANCE` remains deferred.
260804 · JL agreed that DRAFT, PROBE, REVISE, and CHECK remain Content divisions of QB5 by default. Added division 7, Aim A7.1, its completed State, and the dated Law that requires four tests before a phase becomes its own Page.
260804 · Reframed the page around one persistent Page and gave DRAFT, PROBE, REVISE, and CHECK one Content division each. Added separate divisions for non-linear transitions and operation routing. `REVISE → DRAFT` now means an explicit new round, and add, delete, move, and rewrite no longer determine the phase by themselves. No skill contract changed.
260804 · Created from the paper-board session that proposed one Page moving through DRAFT, PROBE, REVISE, and human CHECK, after fresh-context validation found four board phase contracts with zero inbound references.
