# Page · the loop: outline, draft, probe, evidence, revise, compile, check
state: 🟡 IN PROGRESS · Content restructured 260819 to the loop's own order, 12 divisions to 15 · open: 14
owner: JL
method: define each phase by its authority over one persistent Page, execute the routes with versioned receipts, and test both legal branches and injected failures
session: 2e9b9226-9933-4bac-af13-7b22cc6e9cb6

## Opening
How does one Page move through its phases without turning them into that many kinds of edits?
The Page persists while each phase changes the authority of the work.
Adding, deleting, moving, or rewriting does not identify the phase, and the loop may restart after revision.
This page defines what each phase owns, how a round moves, when returning to DRAFT begins a new round, and how an automatic RUN is audited.

⚠️ **Content follows the LOOP's order since 260819, and every phase has a division.** It did not until then: Content was written 260804 for a four-phase loop, OUTLINE and EVIDENCE were split out on 260817, and the body kept opening on phase ② with three of the seven phases missing. `§3` to `§7` hand off to QPw2-draft, QPw3-probe, QPw4-evidence, QPw5-revise and QPw6-check, each carrying the fuller argument. `PROBE` also changed MEANING twice: it was the whole evidence phase until 260816, then EVIDENCE's old name, and since 260817 it is the phase that raises the card and asks.

**Where this page sits**: `QB4` owns the Page's fixed reading structure.
This page owns the Page's lifecycle, from choosing what it promises through deciding whether its current version can close.

**The terms**: a Page is the persistent source and rendered surface being worked on.
A phase is a mode of work defined by its authority, while an operation is a local action such as adding or deleting a paragraph.
A round is the period during which the Page's purpose and Aims stay fixed.

**Why it matters**: the same operation can belong to DRAFT or REVISE for different reasons.
Without an authority boundary, a worker cannot tell whether it is improving the current promise or silently replacing it.

**What this page does not own**: it does not decide the content of a paper, application, Q page, S page, or Skill mirror.
Those Page kinds supply their own constraints and closing gates.

### Writing Style

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
  🧭 OUTLINE ─▶ ✍️ DRAFT ─▶ 📮 PROBE ─▶ 🔎 EVIDENCE ─▶ 🧵 REVISE ─▶ 📄 COMPILE ─▶ 🧑 CHECK
     🚧 gate       │          (skippable)                 │            │           │
     ▲            │                                       │            │           ├──▶ ✅ close
     │            └───── CHECK routes back to any of them ┴────────────┴───────────┤
     └────────────────────────── 🔁 new round ◀───────────────────────────────────┘

  🔒 one round   purpose + Aims fixed
  🔁 new round   purpose or Aims reopened
  🛠 operation   add · delete · move · rewrite
  🚧 gate        a PERSON ticks `approved:` on the outline; no machine may
```

**Where an evidence card is born**, because that was the question three contracts answered three ways until 260817:

```text
  🧭 OUTLINE   the MARK   `- B4 · the four coordinates   🔢`   nothing on disk
  ✍️ DRAFT     the AIM    what the page loses if it stays a hole
  📮 PROBE     the CARD   probe/PP<NN>-<slug>/ · serves: C4.P1.B4 · dispatched
  🔎 EVIDENCE  the ANSWER binding: <QA path> · proof/ pulled · state: bound
  🧵 REVISE    the SENTENCE cites the card by id, never restates it
```

A plan is rejectable in ten seconds and must leave nothing behind, so OUTLINE may not open the file; the mark IS the proposal, so a card at DRAFT would be a second copy of it. The deciding reason is the STAKE: a card's `consumer/` side carries what the page loses, that is an Aim, and Aims are written at DRAFT.


## Content

### 1 · Overview: what the loop is, and how to read the rest
**The problem**: one Page is worked by many hands over many days, and the same visible edit can be two different acts.
Adding a paragraph under an existing Aim and adding a paragraph that creates one look identical in a diff.

**The claim this page makes**: a phase is defined by the ONE question it answers, not by the edit it performs, and a Page moves forward by satisfying a phase's exit rather than by being worked on.

The Opening says where this page sits among its siblings. This division says what the LOOP is. Neither repeats the other.

#### 1.1 · The whole loop on one picture
**The loop at a glance**: the seven phases, who acts at each, the five stops that need a person, and where a round restarts.

QPw00-Display4 draws it, rendered 260819 from an intake frozen out of the seven phase contracts and `ref/phase-cards.md`. Nobody has accepted it yet, so `accepted:` still reads ⬜.

#### 1.2 · The roadmap, and two ways to read it
```text
  §1        what the loop is, and the four words it spends
  §2-§7     the seven phases, in the order they run
  §8-§11    the laws that hold them together
  §12-§14   the machine that runs it, the audit that proves it, its price
```

**Two reading paths.** A person who only RUNS the loop reads §1, §8 and §14.
A person implementing one phase reads that phase's division, then its contract file.

**The loop today**: counted rather than described.

```text
  7  phases declared             PP01.v1   COMPILE is one of them
  6  ship a contract file        PP01.v2   COMPILE has none
  5  stops a person owns         PP01.v3   two of the five revert
  3  runs stored, 9 receipts     PP02.v1 · PP02.v2
  4  of 7 phases ever executed   PP02.v3   PROBE, EVIDENCE and COMPILE have
                                           never run              PP02.v4
```

So the loop is fully specified and two thirds exercised. The three phases with no receipt anywhere are the three that put evidence on disk, which is the honest reading of a design that has been argued more than it has been driven.

#### 1.3 · Workflow, phase, step and round are four different words
**The vocabulary rule**: the loop needs all four and none of them substitutes for another, which is why "phase" was kept when JL weighed replacing it with "step" on 260818.

```text
word         answers                      count in the ONE live run    repeats?
──────────────────────────────────────────────────────────────────────────────────
🌀 WORKFLOW  which LOOP is this?          1  · the run itself          no
⏱️ PHASE     which AUTHORITY acts?        7 defined · 2 used           YES
🔢 STEP      WHERE in this run?           5 · monotonic 1..5           never
🔁 ROUND     which PROMISE era?           1 · bumps only on a reopen   on reopen
```
📌 A phase is a TYPE and a step is an INSTANCE of one: in `260805-0216-QB8e` the single CHECK phase occupies steps 1, 3 and 5.

**All four in one receipt**: none may be renamed onto another.
(`step: 4 · round: 1 · phase: CHECK · route: REVISE`, four fields in one object)
Renaming phase to step would put two different meanings on one key inside a single receipt, and the auditor reads both.
`step` is the monotonic position that never recurs; `phase` is the kind of work that must be free to recur, which is the property the whole loop is built on.

**Why not "step"**: it would contradict the router's own name.
(RUN is deliberately not ADVANCE, `§12.1`)
The word must permit repetition, because CHECK may route back to any earlier phase, PROBE may be skipped entirely, and a page may re-enter DRAFT in a new round.
The one live run proves it rather than asserting it: CHECK ran three times and REVISE twice inside a single round, so a vocabulary that numbered them 1..7 could not describe what happened.
JL raised the replacement and answered it himself on 260818: "for phase, we can do it again and again, right?"

**The folder settles one of them**: it already carries the workflow word.
(`board/page-phases/` became `board/page-workflows/` on 260817)
The directory says which of the four words scopes the family, and the contracts inside it say which authority each phase holds.
So the full term is "workflow phase" where disambiguation is needed and "phase" everywhere else, and the 927 occurrences of the word across this board and the skill tree stay as they are.

### 2 · OUTLINE ①: what the page will say, before it says it
**The OUTLINE contract**: what it decides, what it leaves alone, and what ends it.

```text
🧭 OUTLINE
   asks     what will this page say, division by division, and what does each
            bullet still owe?
   writes   <page>/outline/<stem>-outline-v<N>.md, and nothing in the page
   marks    a hole, and then STOPS. It raises no card and asks nothing.
   exits    a person ticks `approved:`. Nothing else ends it.
```

#### 2.1 · The Aims are agreed here, not later
The Aims are settled in the plan file itself, and not at DRAFT.
Shape and target are read once and approved by one tick.
Every bullet that owes something names its Aim by id, so no id can dangle, and DRAFT transcribes those Aims onto the page rather than inventing them.

Before 260819 the plan wrote an id and this page held the target, so a plan that renumbered its divisions pointed `A5.1` at the OLD A5.1.
Nine of sixteen ids on this page's own plan did exactly that, and the 🧭 tab showed a confidently wrong aim.

#### 2.2 · The gate is the cheapest on the board
```text
  change a section list   BEFORE the prose   one line
  change a section list   AFTER  the prose   the prose
```

A phase whose entire output fits on one screen, and which a person can reject in ten seconds, belongs in front of every expensive phase rather than folded into one.
The file's shape, its five marks and its version rules live at `QPw1-outline` and `haipipe-plugin-outline`.

### 3 · DRAFT ②: turning each point into sentences
**The DRAFT contract**: what enters, the one conversion it performs, and what it hands forward.

```text
✏️ DRAFT
   enters   an approved plan, and the Aims already settled inside it
   does     one approved POINT ──▶ one or more SENTENCES on the page
   keeps    every unresolved dependency VISIBLE, at the place it will be used
   never    invents a value, a citation, a reading, or a rendered figure
   exits    every point in the plan has become prose with its holes showing
```

DRAFT no longer owns the Aims. They are settled at OUTLINE since 260819, and this phase transcribes them.
What stayed is the conversion, and the conversion is the whole phase: the plan says what a part must establish, and DRAFT writes the sentences that will establish it.

#### 3.1 · One point becomes several sentences, and the address carries across
```text
  🧭 plan     C3.P1.B4 · Establish robustness across specifications
                 │
                 ▼  DRAFT
  📄 page     C3.P1.S1 · The primary estimate is <VALUE HOLE>.        [PP01]
              C3.P1.S2 · It remains <ROBUSTNESS HOLE> across specifications.
              C3.P1.S3 · <DISPLAY HOLE> compares the estimates.       [Display2]
```

One bullet is a POINT, not a sentence, so the two sides count different units and say so.
`C3.P1` is shared by both, which is what keeps the join alive; only the last token differs.
The backlink rides in a comment on the scaffold line, `<!-- realizes: C3.P1.B4 -->`, so REVISE may split or merge the sentence later without losing it.

#### 3.2 · A mark in the plan becomes a hole in the sentence
```text
  🧭 the plan's mark           📄 the sentence's hole
  ──────────────────────────────────────────────────────────────────
  🔢 value                     <VALUE HOLE> [PP<NN>]   at the exact spot
  📚 citation                  <CITE HOLE>  [key]       the number will sit
  🖼 display                   <DISPLAY HOLE> [DisplayN]
```

The hole sits where the answer will sit, and it carries the id of the card that will fill it.
That is what makes the two failure modes visible instead of silent: a hole no card serves, and a card no hole uses.
DRAFT may never write the answer itself, and never a hedge in place of a hole.
A sentence that already knows its answer was written after the fact.

#### 3.3 · A scaffold is still prose, so it is written like prose
One idea per sentence, and a sentence past about thirty words is usually two.
The AI-tell catalogue at `haipipe-writing/ref/ai-tells.md` applies HERE and not only at REVISE, because a scaffold written in machine cadence gets rewritten twice instead of once.

**What a scaffold may not contain**, as a list a writer can check against:
an invented number; a hedge standing in for a hole; a summary of what a card says, which the 🧭 tab already reads live; or a division the plan did not name.

The full contract, its worked Point-to-scaffold example and the rule that an owned hole names the Aim it costs live at `QPw2-draft`.

### 4 · PROBE ③: turning a mark into a card, and asking
**The PROBE contract**: an approved mark leaves the plan, becomes a card, and is asked.

```text
🔎 PROBE
├── 📥 enters    the approved mark, still bare, from the plan
├── 🧭 owns      the MATCH lookup, the card, and the dispatch
├── 🗂 writes    probe/PP<NN>-<slug>/ · consumer/ · executor/
├── 📤 exits     the moment the stripped question leaves
└── 🚫 avoids    target Page prose · landing the answer
```
📌 PROBE turns an approved mark into a card and asks; landing what comes back is EVIDENCE's job.

#### 4.1 · The trigger, the MATCH lookup, and the optional rule now live at QPw3-probe and QPw4-evidence
(this page's own §3-§7 predate the 260817 split; the Opening banner above already names it once)
PROBE's trigger, its four-step MATCH lookup that runs before any dispatch, and its optional-when-no-unknown-is-hidden rule now live at QPw3-probe.
The write surface it hands off to, binding the returned answer and landing it in a card, now lives at QPw4-evidence.
PROBE's meaning changed on 260817, exactly as this page's own Opening states it: it now only raises the card and asks.

#### 4.4 · Filing a QA-probe does not identify the target Page
(physical evidence routing and ownership of the Page-facing question are separate decisions)
The target Page is the Page whose lifecycle raised the stake-bearing Q-consumer.
A family may file the QA-probe under an evidence route such as Literature or Value without transferring the Q-consumer, A-consumer, or State to that route's topic Page.
The Paper family's S03 and S04 layout exposes the distinction: a Results Page can raise the question, a QA-probe can live beneath a Value topic, and a QA-bank file can answer it.
Treating physical placement as an ownership transfer gives one exchange two Page-facing consumer surfaces before the answer reaches prose.

#### 4.5 · One active Page bounds the consumer write
(a shared answer creates handoffs to sibling Pages rather than inline rewrites of their Content)
One PROBE run may write its declared Probe surface and the active target Page's Probe reference, A-consumer, and State.
When the same Q-executor serves other Q-consumers, the Probe surface records their references and makes the answer available without authoring those sibling Pages in the current run.
Each sibling interprets the answer and changes its own Content through its own PROBE or REVISE route, with its own version and CHECK.
This preserves one Q-executor for reuse without turning one answer into an unbounded cross-Page edit.

#### 4.6 · A projection can show the full chain without another authored copy
(one canonical reference should drive human display, agent context, and stale-source checks)
The active Page may need to show the Q-executor, bank target, state, returned answer, and limits while keeping its source concise.
A read-only projection can render that chain from the QA-probe and bank answer, while the Page source keeps the Probe reference and its own A-consumer interpretation.
The same reference should drive phase-scoped context loading and CHECK, so an author does not maintain a Probe pointer, an embed, and a Related Board Pages row for one relationship.
Missing targets, superseded answers, or changed source hashes must fail visibly rather than leave an old projection looking current.

### 5 · EVIDENCE ④: landing what came back
**The EVIDENCE contract**: what enters, the lanes it runs, and what ends it.

```text
🃏 EVIDENCE
   enters   a dispatched question that has returned, a known bib key, or a
            unit whose material exists
   lanes    📚 citation · 🔢 value · 🖼 display      IN PARALLEL
   stages   ① MAKE the thing · ② BIND it so a sentence can name it
   exits    every marked bullet has its thing on disk, or a named HOLD
```

QPw00-Display5 draws the whole of this division at once: the two stages, which tick belongs to which lane, which two ticks revert, and the line the phase stops at. Rendered 260819 from an intake frozen out of six contracts; nobody has accepted it yet.

#### 5.1 · Two stages, MAKE then BIND, and the prose is in neither
```text
  ① MAKE   build the thing in the folder that owns it
           📚 the bibex entry
           🔢 the card's answer, pulled into proof/
           🖼 the unit DRAWN: intake · recipe · assets · preview.pdf

  ② BIND   make it pointable, so a sentence can name it and be checked
           📚 the key resolves in bibex/                  `verified` ✋
           🔢 target: names the answering QA file by PATH  `read:` ✋
           🖼 the unit is previewable, its intake frozen

  ─────────── the page's prose starts HERE, and this phase stops ──────────
  ⑤ REVISE the sentence that uses it, its caption, the projections
```

Neither stage touches this page's `## Content`.
That is the whole boundary: EVIDENCE changes what the page KNOWS and REVISE changes what it SAYS.
A phase that both landed the answer and wrote the sentence could not be audited, because the only evidence that the answer came first would be its own report.

#### 5.2 · 📚 The citation lane
**What it lands**: one entry in `bibex/<stem>.bib`, and a key a sentence can cite.

```text
  made by   a PERSON, verbatim. A machine may SUBSET or TRANSCRIBE bibtex
            and may never COMPOSE it.
  tick      `verified`, on the entry itself. It does not revert.
  failure   a 📚 mark naming a sibling board page. That is a cross-reference,
            written in the bullet's own words; only a bib key wears 📚.
```

#### 5.3 · 🔢 The value lane
**What it lands**: a number bound BY PATH to the QA file that answered it, with the pulled file sitting in the card's own `proof/`.

```text
  made by   the bank, task or discovery, answering into its own QA file.
            PROBE already raised the card and asked.
  tick      `read:`, and it REVERTS when `target:` changes or proof/ is re-pulled
  id        PP<NN>.v<n> — one card holds several numbers
```

**One card, many values.** A card is ONE question and its answer usually holds several numbers, so the id goes one level deeper. `PP01` answers four things; `§1` uses `PP01.v1` and `§12` uses `PP02.v4`. The ids are allocated here, in `card.md`'s `## Values` block, when the answer lands and never before.

That is what makes two failures visible instead of silent: a number in the prose citing no `PP<NN>.v<n>`, and a value in a card that no sentence uses. The 🔢 tab reports both, and `haipipe-plugin-value` owns it: a surface, with no storage, because the number already lives in `proof/` with its source, run and sha256.

#### 5.4 · 🖼 The display lane
**What it lands**: a DRAWN, previewable unit, not a folder of material.

```text
  ① INTAKE  🧑 freeze the material           EVIDENCE
  ② RENDER  ⚙️ the renderer writes recipe/   EVIDENCE
  ③ PICK    🧑 choose among candidates/      EVIDENCE
  ④ BUILD   ⚙️ assets/ · float.tex · preview EVIDENCE
  ⑤ ACCEPT  🧑 README `accepted: ✅`         CHECK      the human tick
```

Steps ② to ④ were REVISE's until 260819. They moved because this lane was the only one of the three that returned nothing a page could use: a citation lands a key, a value lands a bound number, and a display landed an unrendered folder.

**Whether a unit waits depends on its kind**, which no phase contract said before that day:

```text
  data kind     table · figure                freezes FROM a probe card's proof/
                                              ── it WAITS for an answer
  concept kind  diagram · tex · illustration  freezes a listing of source files
                                              ── nothing to wait for
```

QPw00-Display4 is a concept unit: its nine inputs are contract files and the route table's code that already existed, so no probe had to answer first.

#### 5.5 · What the three lanes have in common
```text
  📚 citation   ─▶  bibex/<stem>.bib entry   returns a bib key
  🔢 value      ─▶  probe/PP<NN>-<slug>/     returns a number bound to its run
  🖼 display    ─▶  display/<unit>/          returns a drawn, previewable figure
```

They run at the same time, and none waits for another to finish.
Three ticks live here, more than in any other phase, and two of them revert when their inputs change, because acceptance binds to the inputs it was accepted with.
A tick belongs to stage ② BIND, because a tick is what turns a made thing into one a sentence may quote; `accepted: ✅` is the exception and stays at CHECK, since what it judges is the drawn artifact as a reader meets it.

A fourth mark, `🧮 proof`, existed from 260817 to 260819 and is RETIRED. It came from one transcribed quote and no ruling; going to a task folder or a discovery folder for the evidence behind a claim IS a probe, which is 🔢 (JL 260819).

**EVIDENCE on this board**: how much of it has ever executed.

```text
  22  probe cards exist            PP03.v1
  14  still at `planned`           PP03.v2   never dispatched
   0  a person has read            PP03.v3   so no number may be quoted yet
   8  display units, 8 rendered    PP03.v4
   0  display units accepted       PP03.v5
```

Every person-reserved tick in this phase is open across the whole board.
The lanes are real folders under real contracts with almost no traffic, and saying so is the difference between a contract and a description.

The lane contracts are `QPw4c-citation`, `QPw4v-value` and `QPw4d-display`, under the phase contract `QPw4-evidence`.

### 6 · REVISE ⑤: turning landed evidence into sentences
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

#### 6.1 · The fixed-promise test, the five-step order, and the display-walk split now live at QPw5-revise
(which also carries COMPILE, folded in since 260817)
REVISE's fixed-promise test, its five-step LAND, ARGUE, SOUND, RENDER, BUILD order, and the three display-walk steps it owns now live at QPw5-revise, which also carries COMPILE.
This page's own §9, Operations route by reason, still carries the shared DRAFT-versus-REVISE test table that separates the two phases on the same edit, so a reader is pointed sideways as well as forward.

#### 6.4 · ⑥ COMPILE is a step of this phase, not a division of its own
**Scored against §9.2's four split tests**, rather than asserted:

```text
  ① an unresolved question that is not just asking for its definition
     ❌ its only open question is whether the fold is permanent
  ② needs its own Aims and States rather than borrowing
     ❌ A7.1 was the fold itself; nothing else was ever tracked
  ③ an independent closing gate
     ❌ no tick, no receipt, no gate anywhere
  ④ its own continuation map in Files
     ❌ shares REVISE's
                                                        0 of 4 → it stays here
```

COMPILE rebuilds `latex/` and `word/` from the source as it now stands. That is real work with a real audit code, `projection-stale`, and it is the only member of the loop with no contract file, no receipt in any stored run, and no tick.

So the loop still DECLARES seven phases and the Diagram still draws ⑥, because that count is cited across the contracts. What this page no longer does is give it a division at the same level as the six phases that have one, since a heading of its own asserted a symmetry the four tests refuse.
Whether the fold is permanent is `QPw5-revise`'s open ruling.

### 7 · CHECK ⑦: where the current version goes next
**The CHECK contract**: one concrete version is judged against its promise and routed.

```text
🧑 CHECK
├── 📥 enters    rendered version · Aims · evidence · constraints
├── 👁 owns      judgment · findings · closing decision
├── 📝 writes    comments · findings · gate record
├── 🔀 routes    close · REVISE · EVIDENCE · new DRAFT · HOLD
└── 🚫 avoids    curing its own substantive finding
```
📌 CHECK observes and decides; another phase performs the content change it requests.

#### 7.1 · The judge/repair separation, the three built-artifact counts, and the accept-biased gate now live at QPw6-check
(this page's own §13, Audit proves process claims, still carries the receipt and invariant material CHECK is measured against)
CHECK's judge-may-not-repair separation, the three independent built-artifact counts it reads (declared, rendered, accepted), and its accept-biased human gate now live at QPw6-check.
This page's own §13 still carries the receipt fields and invariants CHECK's routed findings are measured against, so nothing here is left an orphaned reference.

### 8 · Transitions form rounds, not a rigid conveyor belt
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

#### 8.1 · The common order is not the only legal order
(each phase may repeat, and optional work disappears when its trigger is absent)
`DRAFT, DRAFT, PROBE, REVISE, DRAFT` is a legal history.
The first two DRAFT entries can be repeated design work in one round.
The final DRAFT means that revision reopened the promise and therefore began a new round.
A complete draft with no unknowns and no revision need may go directly to CHECK.

#### 8.2 · REVISE to DRAFT is a restart, not a forbidden edge
(the explicit restart preserves the distinction between improving and redefining)
REVISE may reveal that the current purpose or Aims are wrong.
The Page then returns to DRAFT and receives a new round, while the Page itself persists.
Earlier evidence remains available, but its relevance must be checked against the new promise.
Any earlier closing decision no longer applies to the new round.

#### 8.3 · A phase label requires a reason
(the visible sequence alone cannot classify the work)
The history should say which authority was used: promise reopened, unknown resolved, current promise improved, or version judged.
Without that reason, two identical diffs can be mislabeled as different phases and two different intentions can be mislabeled as the same one.

#### 8.4 · The bands are the shape, and a row number is only a reading order
**Three bands, not eleven steps**: once per page · the loop · what ends it.

A reader who takes only the three bands away already has the loop: one thing happens once, six things repeat until CHECK stops sending them back, and two things happen when it does.
The numbers are not a sequence, because the three EVIDENCE lanes run at the same time and CHECK may return to any earlier phase.
That is what this division argues from transitions, and `§14` prices the same shape as work.

### 9 · Operations route by reason, not by edit shape
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

#### 9.1 · Adding and deleting do not name a phase
(the same paragraph-level change can design the promise or improve its realization)
Adding a paragraph to explain evidence for an existing Aim is REVISE.
Adding a paragraph because the Page now answers a new question is DRAFT.
Deleting unsupported or duplicate prose while keeping the Aim is REVISE.
Deleting the promised result itself, or deleting its Aim, is DRAFT.

#### 9.2 · Moving and rewriting use the same test
(clarity stays inside the round; reframing opens a new one)
Moving paragraphs to improve flow under the same argument is REVISE.
Changing the argument the Page promises to make is DRAFT even if the diff is only one moved heading.
Rewriting the Opening for clarity is REVISE when the purpose stays fixed.
Rewriting it to give the Page a different purpose is DRAFT.

#### 9.3 · PROBE and CHECK use different write surfaces
(they can produce records without becoming authors of the target Page's content)
PROBE writes questions, sources, evidence, and answer records.
CHECK writes findings, comments, and gate records.
When either phase causes target prose to change, the actual content edit is performed under REVISE or a restarted DRAFT.

### 10 · One lifecycle Page holds the phases together
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

#### 10.1 · One phase does not automatically mean one Page
(a description is a division; an independently managed question is a Page)
DRAFT, PROBE, REVISE, and CHECK remain divisions of QB5 because their meanings depend on comparison and transition.
The DRAFT and REVISE boundary is easier to judge when both definitions and the operation examples stay on one Page.
The transition rules also need one home that no phase-specific Page can own alone.

#### 10.2 · A phase earns a Page by passing four tests
(the split happens only when the new Page can be worked on and closed independently)
The phase must have an unresolved question that is not merely asking for its definition.
It must need its own Aims and States rather than borrowing QB5's records.
It must have an independent closing gate and its own small continuation map in Files.
If any test fails, the material remains a division or paragraph on QB5.

#### 10.3 · Separate skills do not require separate design Pages
(an executable contract and a design question have different reasons to be separate)
A phase skill may remain separate because a worker needs to load one execution contract at a time.
That file boundary does not force the Board to create a matching design Page.
If a phase later passes the split test, QB5 keeps the shared boundaries and transitions while pointing to the new Page for that phase's independent question.

### 11 · Page Type and Page Phase are separate skill axes
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

#### 11.1 · `for-*` names only Page Types
(the preposition says which persistent Page shape varies from the base)
`haipipe-page-for-stage`, `-for-skill`, and `-for-venue` keep their names and move under `page-types/`.
The roster has since grown to ten Page Types, and `QB6` owns the admission test and the list.
The grouping folder is organizational and carries no `SKILL.md` of its own.
A new Page Type is added only when a persistent Page needs a structural contract that the base does not provide.

#### 11.2 · Phase skills use direct names
(a phase is an active authority, not a Page variant)
The phase contracts are `haipipe-page-draft`, `-probe`, `-revise`, and `-check` under `page-phases/`.
They apply across Page Types and therefore do not use `for-stage` in their names.
The base first adopted the phase vocabulary without adding `ADVANCE`.
The automatic router now earns a verb named `RUN`, because it may repeat, branch, HOLD, or return to DRAFT rather than advance in one direction.

#### 11.3 · PROBE keeps one vocabulary across the boundary
(Q-consumer and Q-executor remain the two question forms; Entry is not a fifth lifecycle concept)
The target Page owns the stake-bearing Q-consumer.
The PROBE phase strips the stake into a neutral Q-executor, binds the returned A-executor, and writes an A-consumer interpretation for each consumer.
One Q-executor may serve several Q-consumers.
`haipipe-probe` remains the shared crossing protocol, while `haipipe-page-probe` applies that protocol to a Board Page.

### 12 · RUN turns the phase grammar into a bounded loop
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
QPw00-Display1 states the same controller as an algorithm, so a reader can see the three actors alternate and read the stop conditions in the order the loop tests them.

#### 12.1 · RUN is not ADVANCE
(the verb must describe what the router can actually do)
ADVANCE suggests that one phase has one next phase and that progress always moves forward.
RUN means execute the current Page lifecycle from a named starting authority until CLOSE or HOLD.
The legal route table is dynamic: DRAFT, PROBE, and REVISE may repeat or hand off, while only CHECK may CLOSE.
QPw00-Display2 writes that table as six explicit row-sets and derives four laws from them, two of which this prose never states: CHECK cannot route to CHECK, so a judged version reaches a second judgment only through a producer; and DRAFT is in neither R(PROBE) nor R(EVIDENCE), so the PREPARE loop's one door out is OUTLINE's own gate.
Returning to DRAFT from another phase increments the round only when purpose or an Aim reopened.

#### 12.2 · The raw-material packet bounds what agents may know
(automation begins with explicit inputs rather than hidden conversational memory)
The packet names the persistent Page, stable Page Type, starting Phase, run intent, source paths, settled constraints, closing gate, and step and round limits.
A new Page is first created and registered, then RUN starts it at DRAFT.
An existing Page with no known next need starts at CHECK, allowing a cold judge to route the visible version.
A missing source, unknown gate, or ambiguous authority becomes HOLD rather than an invented input.

#### 12.3 · The controller routes but does not write or judge
(this page OWNS the role-separation rule; `QPw00a` owns only the roster of units that fill the roles and each unit's debt, ruled 260818 when JL read `QPw00a` and could not tell what it was for)
(coordination is a separate authority from production and approval)
The producer performs exactly one phase and suggests a legal route, and the controller decides which hand takes it by testing for CHECK rather than by listing producer phases: every phase except CHECK goes to the producer. Naming three of them was true of the four-phase loop and became false at the 260817 split, which left OUTLINE, EVIDENCE and COMPILE going to the read-only judge on paper for two days.
The mechanical builder rebuilds, runs deterministic checks, and identifies the source plus render version.
The fresh reviewer performs CHECK against that exact version and returns CLOSE, REVISE, PROBE, DRAFT, or HOLD.
The controller validates and follows the route, but it cannot alter Page prose or convert a pending human gate into CLOSE.

#### 12.4 · Every loop has honest stop conditions
(bounded automation must distinguish non-convergence from quality)
The run stops on CLOSE, explicit HOLD, missing input, failed build, version mismatch, required human ruling, maximum steps, or maximum rounds.
Reaching a limit says the process did not converge within its budget.
It never says the Page passed.
The run's final state and every attempted phase remain inspectable instead of disappearing into an agent transcript.

### 13 · Audit proves process claims with receipts and fault tests
**The assurance model**: deterministic invariants, fresh semantic judgment, and direct or human evidence support different quality claims.

```text
🧾 phase receipts             what happened, by whom, to which version
⚙️ deterministic audit       legal routes · rounds · roles · versions · bounds
🧑 fresh CHECK               function · evidence · readability · local gate
🗣 human evidence            approval only where the Page Type requires it
🧪 branch + fault tests      expected success and expected refusal
```
📌 A passing process audit proves that the declared process ran correctly, not that every possible substantive claim is true.

#### 13.1 · A receipt binds action, actor, version, and route
(a prose summary cannot reveal self-approval or changed-after-check)
Each receipt records step, round, Phase, producer or judge actor, builder actor, status, source and render SHA-256 values, route, reason, artifacts, evidence, findings, and human-gate state.
CHECK additionally binds `checked_version` and a verdict.
The receipts are ordered and stored outside Page discovery under `_runs/page/<page-id>/<run-id>.json`.
The deterministic auditor independently rehashes the source and rendered files on disk; matching claims repeated inside a receipt are not accepted as artifact evidence by themselves.
The terminal CHECK record is not appended to the Page afterward, because that append would change the version it claims to approve.

#### 13.2 · Seven invariants make the loop auditable
(the highest-risk failures become machine-detectable)
The preserved raw-material packet must match the run identity, first Phase, declared gate, and limits.
Only legal phase routes are accepted, and only CHECK may CLOSE.
A non-DRAFT route to DRAFT must name the reopened purpose or Aim and increment the next round exactly once.
The producer, mechanical builder, and judge of one version must have different actor identities.
Every version id must be the two declared lowercase SHA-256 digests joined by `:`, and every receipt must begin from the preceding receipt's ending version.
CHECK must observe identical before, after, and checked ids; the auditor rehashes the current artifacts, and any later change requires a new CHECK.
A required human gate closes only with durable evidence that the person ruled.
Maximum steps and rounds terminate as non-convergence, never as a pass.

#### 13.3 · Testing covers branches and injected failures
(a green common path does not demonstrate a router)
Happy paths include DRAFT directly to CHECK and DRAFT through optional PROBE and REVISE.
Branch tests include CHECK to REVISE and back, CHECK to PROBE, and CHECK to a new DRAFT round.
Fault injection includes self-approval, mutation after CHECK, illegal route, packet mismatch, broken version continuity, symbolic hashes, missing human evidence, failed worker, non-terminal trace, and exhausted limits.
The deterministic harness must reject each injected fault for the specific invariant it violates.

#### 13.4 · Quality is evidenced, not declared absolute
(different checks justify different confidence claims)
The mechanical checker can prove structural facts, and the lifecycle auditor can prove process facts.
A fresh reviewer supplies semantic evidence that the Page performs its declared function and is readable without the drafting conversation.
Direct sources or a human gate supply claims those instruments cannot settle.
The final report therefore names the checked version, traversed branches, evidence inspected, remaining findings, gate state, and residual risk instead of saying only that quality is guaranteed.


#### 13.5 · What the auditor says about this board's own receipts
**The audit, run rather than described**: `src/page_lifecycle.py` over every file under `_runs/`.

```text
  3  runs audited                  PP04.v1
  0  runs that PASS                PP04.v2
  5  findings in total             PP04.v3
  3  distinct fault codes          PP04.v4
  1  REAL contract violation       PP04.v5
```

The three codes are not equally serious.
`artifact-version-mismatch` fires on all three runs and is expected: it compares each page as it stands now against the identity recorded when the run finished, and every one of these pages has been edited since.
`page-path-stale` fires on the oldest run because its page was later renamed, and the auditor degraded to a named finding instead of a false "artifact missing".

`checked-version-mismatch` at run `260818-1543` receipt[2] is the real one.
CHECK must leave `version_before`, `version_after` and `checked_version` identical, because a judge reporting on a version it did not read is the one failure the receipt exists to catch.
No reasoning predicted it; running the auditor found it.

So this division's claim is half-earned. The machinery works and caught a genuine violation in the board's own history, and the passing half of A13.1's "both a passing and a failing test" still has no stored example.

### 14 · The same loop, priced: what a person is actually asked to do
**The cost rule**: a reader deciding whether to run this loop needs the WORK, not the authority, so the loop is stated once more as one row per step, with a person's job and its price in it.

```text
#    PHASE      WHAT HAPPENS                    YOUR JOB              TIME    HOW OFTEN
────────────────────────────────────────────────────────────── once per page ───────────
0    OPEN       CREATE copies the template      ✋ write the title    15 min  once
                and registers the page in          so it states the
                board.md (a VERB, not a phase)     page's PURPOSE
──────────────── the loop · CHECK may send you back to rows 1, 2, 3, 4 or 5 ────────────
1    OUTLINE    a machine writes the SHAPE      ✋ judge DIRECTION,   10 min  ↺ each pass
                only, then FOUR checks run:        never arithmetic,
                coverage · address · value ·       then tick `approved:`
                shape                           ⬅ the four run BEFORE you are asked;
                                                   this is the loop's one gate
2    PROBE      MATCH first (this page, PageX,  nothing               0       ↺ each pass
                the QA bank), only then a card;
                the stripped question is the
                only thing that crosses
3c   CITATION   a machine may SUBSET or         ✋ land the entry     20 min  ↺ per entry
                TRANSCRIBE a real record,          verbatim, so it
                never COMPOSE one                  carries `verified`
3v   VALUE      the bank answers into its own   ✋ tick `read:` =     30 min  ↺ per card
                QA file, `target:` names that      "I agree with the
                file BY PATH, and                  judgment", not "I
                `checks/values.py` re-runs         checked the arithmetic"
                the number                      ⬅ reverts when target or proof moves
3d   DISPLAY    this lane DRAWS since 260819:   ✋ rule `intake/`,     ?      ↺ per unit
                intake, recipe, the pick, then     choose among
                assets/ + preview.pdf              candidates/
                                                ⬅ no tick here: `accepted:` is row 7a's
     ⚡ rows 1, 2 and 3 REPEAT AS ONE UNIT until the plan and its evidence agree,
        and 3c · 3v · 3d run at the SAME TIME
4    DRAFT      enters on evidence that has     nothing               0       per round
                ALREADY landed, so it writes
                the NUMBER; a hole is the
                EXCEPTION and names the input
                it is missing
5    REVISE     the sentence citing each drawn  nothing               0       ↺ each round
                unit by id, the caption, the
                latex/ + word/ rebuild. It no
                longer draws
6    COMPILE    folded into 5 since 260819,     nothing               0       with 5
                holding no contract of its own
     ⚡ 4, 5 and 6 run END TO END and stop for nobody
7    CHECK      a DIFFERENT actor judges the    ✋ take CLOSE, or     15 min  ↺ each round
                RENDERED page and the BUILT        name where to go
                artifact                           back, by phase NAME
────────────────── what ends it · both ticks below are row 7 CHECK's own ───────────────
7a   ACCEPT     shown only once the page's      ✋ tick               10 min  per unit
                mechanical errors are ZERO: a      `accepted: ✅`
                confirmation, not an inspection ⬅ a changed intake/ drops it back to ⬜
7b   CLOSE      CLOSE is a ROUTE and not a      ✋ sign the RULING    5 min   per round
                phase; only `verdict: pass`     ⬅ silence is not consent
                may take it
```
⚠️ **The row numbers here are the WORK's, not the loop's.** Row 0 OPEN is a verb, and rows 7a ACCEPT and 7b CLOSE are ⑦ CHECK's own ticks; rows 3c, 3v and 3d are the three lanes inside phase ③. Rows 1, 2, 4, 5 and 7 are phases ①, ②, ④, ⑤ and ⑦, and phase ⑥ COMPILE holds row 6 only to say out loud that it is folded into row 5.

📌 EIGHT of the twelve rows ask something of a person and four read `nothing` (2, 4, 5, 6); of those eight, five carry a tick a machine may never write (1, 3c, 3v, 7a, 7b), and three (row 0 OPEN, row 3d DISPLAY, row 7 CHECK) ask for a judgment that leaves no tick behind. Every asking row is the OPEN that starts the page, a step of the PREPARE loop, or CHECK: the loop's whole human cost is paid BEFORE DRAFT and AFTER REVISE, and never inside them. That is the same fact `§12` states as authority, priced instead.
QPw00-Display3 renders this table for print, with the fourteen files it was transcribed from frozen beside it.

#### 14.1 · TIME is the only estimated column, and it is estimated because nothing has been timed
**The one measured number is zero**: `PP05.v1` reports 0 phases with a measured duration, and `PP05.v2` names the 2 inputs that block it.

```text
  ① three phases have NO receipt anywhere    PROBE · EVIDENCE · COMPILE   PP02.v4
  ② the receipts that DO exist carry one     a completion time, not a
     timestamp, not two                      start/end pair
```

Block ② is the one to fix first, because it is a contract change rather than work: the receipt shape in `ref/page-run-contract.md` needs a per-phase start and end stamp. Block ① then clears by running the loop once end to end.
An estimate was not substituted, because substituting one is how this column got its current values.
Every other cell is transcribed from a file frozen in `display/QPw00-Display3-who-does-what/intake/inputs/`, and the manifest names all fourteen with the sha256 of the copy AND of the live source, so `checks/intake.py` can recompute staleness on demand. Row 3d carries no estimate at all: the lane took over three of REVISE's steps on 260819 and nobody has priced it since.
A number nobody has measured is marked as an estimate on the table's own face rather than left to look like the others.



## Aims

Every Aim is one row: the tick says where it stands, `Done when:` is the test a reader can apply without asking anyone, and `Now:` is what is true today.

🔒 Target and test are transcribed from the approved plan `outline/QPw00-page-loop-outline-v2.md`, which is where Aims are settled (JL 260819). `Now:` is the page's own, and `## States` merged into this section the same day (`haipipe-page` 0.34.0).

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
      📍 `A4.2` owns the boundary between the active target Page and an evidence route supplied by a family.
      🔔 `Why now` the Paper adapter currently makes the Literature or Value topic Page canonical after another Page raises the Aim, while `QB5 §8.3` says the target Page owns the Q-consumer.
      `A ·` Allow the transfer. The evidence topic Page owns the stake, A-consumer, State, and Probe path; this keeps a self-contained topic register but makes one PROBE a multi-Page consumer write.
      ⭐ `B ·` Keep ownership on the Page that raised the Q-consumer. The QA-probe may be filed under any family route, while topic Pages show a derived rollup and receive their own lifecycle only when their synthesis changes.
      🛑 `Blocks` changing the Paper topic-entry contract and implementing the zero-copy topic projection.
      🤖 `If nobody answers` the implemented Paper topic-owned rule remains unchanged, and sections 4.4 to 4.6 stay the recommended shared boundary rather than shipped family behavior.

### A1 · 🧭 Overview: what the loop is, and how to read the rest
- ⬜ A1.1 · The loop is stated once, whole, before any single phase is argued.
  **Done when:** a reader can stop after §1 and say what the seven phases are, which one they are in, and where to read next.
  **Now:** Not met. §1 is written this round and no reader has been asked whether they can stop there and still say what the seven phases are.
- 🔨 A1.2 · No document in this family uses one of the four words for another's meaning.
  **Done when:** a sweep finds no receipt field, contract sentence, or page division calling a phase a step or a step a phase.
  **Now:** Being worked on now. The four are separated here and in `haipipe-page-workflow`; the sweep across the other 63 pages of this board has not run.
- ✅ A1.3 · The four are readable from one figure without opening the receipt.
  **Done when:** each word carries what it answers, its count in a real run, and whether it repeats.
  **Now:** Met. `§1`'s figure carries all four with their live counts from `260805-0216-QB8e`.

### A2 · 🧭 OUTLINE ①: what the page will say, before it says it
- 🔨 A2.1 · OUTLINE has a division of its own, stating its authority, its deliverable and the tick that ends it.
  **Done when:** the body opens on phase ① rather than phase ②, and a reader reaches DRAFT already knowing what an approved plan is.
  **Now:** Written this round. §2 gives OUTLINE its own division for the first time; the body opened on phase ② from 260804 to 260819.
- 🔨 A2.2 · The Aims are settled during OUTLINE, in the plan file, and every owing bullet links to one by id.
  **Done when:** no bullet names an Aim the plan does not declare, and DRAFT transcribes the Aims rather than inventing them.
  **Now:** Written this round, and already exercised: `outline-v2` declares all 24 Aims and this section is transcribed from it. The rule is not yet in `haipipe-page-outline`, which still reads as if DRAFT owns Aims.

### A3 · ✏️ DRAFT ②: turning each point into sentences
- 🔨 A3.1 · DRAFT is defined by the point-to-sentence conversion, not by first creation and not by owning Aims.
  **Done when:** a reader can identify DRAFT in both an empty Page and a mature Page that reopens its promise, and can say what DRAFT kept when the Aims left.
  **Now:** Rewritten 260819. §3 now defines DRAFT by the point-to-sentence conversion; until this round it read as if DRAFT owned the Aims, which left with them on 260819.
- 🔨 A3.2 · Every mark in the plan becomes a visible hole in the sentence that will use it, with its card id beside it.
  **Done when:** no landed answer can be written into prose without passing through a hole, and no hole exists that no card serves.
  **Now:** Written this round in §3.2, with the mark-to-hole table and the two failure modes named. Not yet exercised: this page has five holes and five cards, and no answer has landed to test the join.
- ⬜ A3.3 · A scaffold reads like a person wrote it, before REVISE touches it.
  **Done when:** `score.py` on a fresh DRAFT output flags no more sentences than it flags on the same page's already-revised prose.
  **Now:** Not met, and not measured. `score.py` has never been run on a fresh DRAFT output and compared against revised prose on the same page.

### A4 · 📮 PROBE ③: turning a mark into a card, and asking
- ✅ A4.1 · PROBE has an explicit trigger, write surface, return record, and exit.
  **Done when:** a reader can route a consequential unknown without letting PROBE author target prose.
  **Now:** Met 260818. §4's face-card, pin line, and §4.1 now state PROBE's post-260817 meaning consistently with the Diagram and the Opening, and point at QPw3-probe and QPw4-evidence rather than re-arguing it.
- 🧠 A4.2 · The target Page, Probe surface, sibling handoff, and forbidden cross-Page write are unambiguous.
  **Done when:** a family can file a QA-probe by evidence route without silently transferring Q-consumer ownership or authoring a sibling Page in the same run.
  **Now:** Waiting on the open Decision Now row. Sections 4.4 and 4.5 state the origin-owned, one-active-Page alternative and the Paper S03/S04 case that exposed the ambiguity.
- 🧠 A4.3 · One Probe reference can show the full evidence chain without becoming a second authored answer.
  **Done when:** the reference drives render projection, bounded phase context, dependency versioning, visible failure, and CHECK.
  **Now:** Waiting on A4.2. The Board already supports live Markdown embeds and scoped Related Board Pages, but no single Probe reference drives display, context, dependency identity, and CHECK.

### A5 · 🃏 EVIDENCE ④: landing what came back
- 🔨 A5.1 · EVIDENCE is readable as parallel lanes, and the four marks a plan can carry are named against the three lanes that exist.
  **Done when:** a reader can say why proof is the fourth kind and has no lane, without opening another contract.
  **Now:** Written this round. §5 gives EVIDENCE its own division and names three marks against three lanes; the retired 🧮 is recorded there rather than left silent.
- 🔨 A5.2 · The three ticks EVIDENCE carries are stated with which two revert.
  **Done when:** a reader can name the input whose change reverts `read:` and the one that reverts `accepted:`.
  **Now:** Written this round in §5.2, with the revert rule stated for both `read:` and `accepted:`.
- 🔨 A5.3 · What each lane returns is stated side by side.
  **Done when:** the three returns are one block, not three paragraphs in three contracts.
  **Now:** Written this round in §5.1 as one block of three returns.

### A6 · 🖊 REVISE ⑤: turning landed evidence into sentences
- 🔨 A6.1 · REVISE is separated from DRAFT by whether purpose and Aims remain fixed.
  **Done when:** the same add, delete, move, or rewrite operation can be classified from its reason.
  **Now:** The fixed-purpose-and-Aims test now lives at QPw5-revise §1, and the shared operation table stays on this page's own §9; awaiting human check.
- ✅ A6.2 · COMPILE's fold into REVISE is a scored decision with its open ruling named, not an inherited silence.
  **Done when:** the fold is scored against §10.2's four split tests on the page, and QPw5-revise is named as the owner of whether it is permanent.
  **Now:** Met 260819. §6.4 scores COMPILE against §10.2's four split tests, 0 of 4, and names QPw5-revise as the owner of whether the fold is permanent.

### A7 · ✅ CHECK ⑦: where the current version goes next
- 🔨 A7.1 · CHECK judges one version and routes it to close, REVISE, PROBE, or a new DRAFT.
  **Done when:** every finding names the authority that owns the next change.
  **Now:** The judged outcomes and the no-hidden-revision rule now live at QPw6-check §1-§4, cited from this page's own §7.1; awaiting human check.

### A8 · 🔁 Transitions form rounds, not a rigid conveyor belt
- 🔨 A8.1 · Repetition, optional phases, and REVISE to DRAFT are represented without contradiction.
  **Done when:** `DRAFT, DRAFT, PROBE, REVISE, DRAFT` has an unambiguous round interpretation.
  **Now:** Written in Content with repeated phases, optional PROBE, and REVISE to DRAFT as a new round; awaiting human check.

### A9 · 🛠 Operations route by reason, not by edit shape
- 🔨 A9.1 · Common Page edits are examples rather than phase definitions.
  **Done when:** adding, deleting, moving, and rewriting each have both a DRAFT case and a REVISE case.
  **Now:** Written in Content with paired add, delete, move, and rewrite cases; awaiting human check.

### A10 · 📄 One lifecycle Page holds the phases together
- ✅ A10.1 · Each phase remains a Content division until it becomes an independently closable question.
  **Done when:** the Page names the four split tests and distinguishes phase skills from design Pages.
  **Now:** JL agreed 260804 that every phase gets a Content division by default, not its own Page; division 7 records the four tests for a later split.

### A11 · 🗂 Page Type and Page Phase are separate skill axes
- ✅ A11.1 · The skill tree keeps persistent Page variation separate from current phase authority.
  **Done when:** Page Types live under `page-types/`, Page Phases live under `page-workflows/`, and the base routes both without introducing an Entry phase or treating RUN as linear ADVANCE.
  **Now:** JL ruled 260804 that `for-*` skills belong under `page-types/`, direct phase skills belong under `page-phases/`, and the remaining layering proposal stands.

### A12 · 🔁 RUN turns the phase grammar into a bounded loop
- 🔨 A12.1 · One automatic router composes phase producers, version snapshots, independent CHECK, legal branches, new rounds, and honest stops.
  **Done when:** a new or existing Page can run from a named Phase to CLOSE or HOLD without assuming DRAFT, PROBE, REVISE, and CHECK each run once in order.
  **Now:** LIVE-PROVEN with one caveat, 260805: run `260805-0216-QB8e` drove a real page CHECK→REVISE→CHECK→REVISE→CHECK→CLOSE in 5 receipts, findings 8→2→0, distinct fresh-context actors per role, audit PASS with hashes recomputed from disk (`_runs/page/QB8e/260805-0216-QB8e.json`). The caveat keeping this 🔨: `page-lifecycle.workflow.js` was NOT invocable as shipped (no Workflow harness in the live environment); the controller logic was executed by hand, and the run surfaced 11 contract ambiguities, logged below.

### A13 · 🧪 Audit proves process claims with receipts and fault tests
- ✅ A13.1 · Every run is reconstructable and every critical invariant has both a passing and failing test.
  **Done when:** the durable receipt passes the deterministic auditor, fresh-context review passes the checked version, and branch plus fault coverage rejects known bad flows.
  **Now:** Met 260805: the live QB8e run supplied the missing semantic CHECK, three fresh judges on three exact versions, converging 8→2→0, terminal verdict pass with zero findings; the deterministic auditor passed the same bundle with artifact hashes recomputed from disk.

### A14 · 💰 The same loop, priced: what a person is actually asked to do
- ✅ A14.1 · Every cell except TIME is transcribed from a frozen file rather than from memory.
  **Done when:** `display/QPw00-Display3-who-does-what/intake/manifest.yaml` lists a sha256 for every source the table quotes, and `cli/check.py` reports no `display-intake-unfrozen` on this unit.
  **Now:** Met 260818, and then extended the same day. `QPw00-Display3` was the FIRST unit on this board with a frozen intake, eight inputs with sha256; `QPw00-Display1` (4 inputs) and `QPw00-Display2` (2 inputs) were frozen hours later, and `haipipe-board-approver-agent` recomputed all fourteen digests against disk. `QPf5-Display1` and `QPf5-Display2` remain the only unfrozen units on the board. Extended again 260819: all five `QPw00` units re-froze in the `file:` + `source:` + sha256 shape (`Display3` alone names fourteen inputs), and `checks/intake.py` recomputes every source hash on demand; `QPf5-Display1`, `QPf5-Display2` and `QPf6-Display1` are what remain on the old copy-only shape, five inputs unresolvable.
- ⬜ A14.2 · The TIME column stops being an estimate.
  **Done when:** `_runs/page/` holds at least one receipt for each of OUTLINE, DRAFT, PROBE and EVIDENCE, and the column is rebuilt from their timestamps.
  **Now:** Not met, and not close. `_runs/page/` holds ONE run with five receipts, all CHECK or REVISE, so four of the table's phases have never been executed under the contract.

### P · Page-level
- ✅ P1 · The base Page contract either adopts this lifecycle vocabulary or explicitly leaves it family-specific.
  **Done when:** JL chooses the base-adoption option and the affected contracts are either wired or retired.
  **Now:** JL chose B on 260804: the base adopted the lifecycle vocabulary first; the later concrete router is now named `RUN`, not linear `ADVANCE`.

## Files

### Contracts

- `../../../../board/haipipe-page/SKILL.md` · the base Page contract that may adopt the lifecycle vocabulary
- `../../../../board/page-workflows/haipipe-page-workflow/ref/page-run-contract.md` · the shared raw-material packet, phase receipt, role, version, and stop contract
- `../../../../board/page-workflows/haipipe-page-draft/SKILL.md` · the DRAFT phase contract
- `../../../../board/page-workflows/haipipe-page-probe/SKILL.md` · the PROBE phase contract
- `../../../../board/page-workflows/haipipe-page-revise/SKILL.md` · the REVISE phase contract
- `../../../../board/page-workflows/haipipe-page-check/SKILL.md` · the CHECK phase contract

### Input files

- `../../../../paper/haipipe-paper/fn/` · the paper family's side: the LaTeX workers became `fn/` verbs in the 260806 one-door merge (the old `paper/workers/` sits in `paper/_old/workers/`); the loop itself lives in `page-phases/`
- `../../../../application/2-phase/` · the application family's existing lifecycle model
- `3-QPs-page-structure/QPs1-overall/QPs1-overall.md` · the fixed Page structure paired with this lifecycle
- `../PaperSkillBoard-260725/1-QA-design/QA5-the-probe-layer/QA5-the-probe-layer.md` · the Paper S03/S04 implementation case that exposed the difference between Probe placement and target Page ownership

### Checks

- `../../../../board/haipipe-board/cli/check.py` · catches source and rendering violations on this Page
- `../../../../board/haipipe-board/src/page_lifecycle.py` · validates routes, rounds, roles, immutable CHECK versions, human gates, and terminal state
- `../../../../board/haipipe-board/cli/pageflow.py` · audits one durable Page RUN receipt
- `../../../../board/haipipe-board/tests/test_page_lifecycle.py` · exercises happy paths, branch routes, and injected failures

### Engines

- `../../../../board/haipipe-board/ref/page-lifecycle.workflow.js` · defines the bounded producer, builder, reviewer, and routing loop; not invocable without a Workflow harness, so the 260805 live RUN drove the controller by hand
- `../../../../board/agents/haipipe-page-auditor-agent.md` · validates the RUN packet, stores the exact receipt under `_runs/page/`, and runs the lifecycle auditor; not the dispatcher since 260818
- `../../../../board/agents/haipipe-page-creator-agent.md` · the producer base the per-phase agents wrap; keeps create-page and revise-opening, and stands in when a phase agent is missing
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
- 🌀 **Workflow**: one bounded RUN over one Page, from a named starting phase until CLOSE or HOLD.
- 🎭 **Phase**: a mode of work defined by the authority it may exercise over the Page. A TYPE, and free to recur.
- 🔢 **Step**: the monotonic position of one attempted phase inside one workflow. An INSTANCE, and never reused.
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

- 260819 2227 · [REVISE-CC, run `260819-1813-QPw00`] Executed CHECK step 14's seven findings, nothing else: the five `## Files` Contracts rows now point at `page-workflows/` (the run contract at its 260815 home, the four phase contracts under the 260817 folder name §1.3 already states), the two dead Engines rows now name the shipped agents `haipipe-page-auditor-agent` and `haipipe-page-creator-agent` with descriptions their own headers support, the literal `%s` in the 260819 Log row's time slot is dropped because no receipt names a time for that pass, the fused 260818 1435 and 260818 1041 Log rows are two source lines again, and the open Decision Now row and A4.2's `Now:` cite §4.4-4.6 instead of the pre-renumber 2.4-2.6. Content order, Aims intent, the outline, probe/, display/ and bibex/ untouched; the rebuild of latex/ and word/ is owed to the builder.
- 260819 · [CC shipped] DRAFT executed `outline-v2`. Content is now the LOOP's order: 15 divisions, four of them new (§1 Overview, §2 OUTLINE ①, §5 EVIDENCE ④, §7 COMPILE ⑥), old §10 folded into §1.2, nothing deleted. 48 section anchors and 16 Aim ids remapped in one pass, with four cross-page references left alone. `## Aims` is TRANSCRIBED from the plan, which is where Aims are settled since JL's 260819 ruling; seven new Aims got their States rows. Two holes are visible and owned: `[Q-loopstate]` in §1.1 and `[Q-evidencerun]` in §5.2.
- 260819 · [JL ruled] the 🧮 proof mark is RETIRED ("我从开始到最后都没有说 proof，我一直说 probe"). It came from one transcribed quote, no Log row ever ruled it, and it was the only mark with no plugin, no folder, no lane, no id and no backlink. 48 marks stripped from 14 plan files; `haipipe-plugin-outline` 0.10.0, `haipipe-page-evidence` 0.8.0 (withdrawing 0.7.3), `haipipe-page-probe` 0.4.2.
- 260819 · [JL ruled] the Aims are settled at OUTLINE, in the plan file, and every owing bullet links to one by id. Before this, a plan that renumbered divisions pointed `A5.1` at the OLD A5.1, and nine of sixteen ids on this page's plan did exactly that.

- 260818 1625 · [REVISE-CC] `§14`'s count was WRONG and `haipipe-board-approver-agent` failed the unit on it. The caption, the README claim, this Log and the `📌` line all said "five of the eleven rows need a person, the other six run machine-only". The drawing shows SEVEN rows carrying a job and FOUR reading `nothing`, and rows 0 and 6 are billed 15 minutes each in the table's own TIME column. The claim also placed the five ticks on FOUR rows, which reproduces the exact miscount the unit's own frozen `haipipe-page-check.SKILL.md:153` corrects. Two more rules failed with it: R14, because row 0 OPEN traced to none of the eight frozen inputs (`haipipe-page.SKILL.md` is now the ninth, and row 0 names its CREATE verb); and R8, because the built page embeds the asset at `width=.85\linewidth`, which printed the 176mm original at 0.733x and delivered 8pt body type to the reader at 5.9pt. The natural width is now 124mm and the same embed prints at 0.9x.

- 260818 · [REVISE-CC, run `260818-1543-QPw00`] Executed outline v1's C1.P1 to C4.P1, plus C2.P2's explicit instruction to leave §4.4-2.6 untouched.
  Replaced #### 1.1-1.3, #### 2.1-2.3, #### 3.1-3.3, and #### 4.1-4.3 with one short pointer paragraph each, naming QPw2-draft, QPw3-probe, QPw4-evidence, QPw5-revise, and QPw6-check by name.
  Corrected §4's face-card and pin line, which mixed PROBE's post-260817 job with EVIDENCE's (outline C2.P1 B1), and corrected one term the outline did not name: §7's face-card still routed CHECK to `PROBE`, the phase's pre-260817 name for the job now called EVIDENCE, so it now reads `EVIDENCE` to match QPw6-check's own routing table.
  Updated the Opening's 260817 banner and the top `state:` line, both of which said Content divisions 1 to 4 still described the four phases from 260804: that claim stopped being true this pass, so both now name the five pages §3-§7 hand off to.
  Updated States rows A3.1, A4.1, A6.1, and A7.1 to point at their new locations; A4.1 moves to ✅, because its own text made the STALE claim conditional on "owed a REVISE round," which this pass supplies, while A3.1, A6.1, and A7.1 stay 🔨 because their qualifier was a pending human check of the model, not missing content, and REVISE does not rule on that.
  A4.2 and A4.3's States rows, the open Decision Now row on A4.2, and every Aim's id and intent are untouched, per the outline's own instruction.
  Route CHECK: the promise is unchanged, §3-§7's realization now matches the current loop, and the next legal authority is a fresh judge of this version.

- 260818 1543 · [DRAFT-CC, run `260818-1543-QPw00`] RUN from DRAFT, entered right after JL approved outline v1 ("ok, approved", 260818 1543).
  Tested outline v1's C1.P1 to C4.P1 bullets against this page's own `§9.1` rule ("adding a paragraph to explain evidence for an existing Aim is REVISE") and against `haipipe-page-draft`'s authority test ("an operation does not identify DRAFT").
  Every bullet replaces an existing paragraph with a short pointer paragraph that serves an already-fixed Aim, tagged 🎯 A3.1, A4.1, A6.1 or A7.1 in the outline itself, and outline v1 already states on its own first page that the plan "only shrinks the REALIZATION of Content divisions 1 to 4" and "is REVISE material, not a reopened round."
  Purpose and every Aim and State id (A1 to A12, P1) stay exactly as written, so DRAFT found nothing to define or reopen and wrote no change to Content, Aims, or States this round, matching the packet's own "may go DRAFT straight to REVISE."
  Receipt at `_runs/page/QPw00/260818-1543-QPw00.json`.
  Route REVISE: the next producer executes outline v1's C1.P1 to C4.P1 verbatim under REVISE authority, the phase this page's own operations table (`§9`) already assigns to the edit.
- 260818 1510 · [OUTLINE-CC, run `260818-1510-QPw00`] RUN from OUTLINE wrote `outline/QPw00-page-loop-outline-v1.md`, the plan to turn Content divisions 1-4 into short hand-off pointers to QPw2-QPw6, keeping §4.4-2.6 in place because no QPw2-QPw6 page yet restates that material. Terminal route HOLD, correctly: `approved:` is a person-only tick and no machine may write it. Receipt at `_runs/page/QPw00/260818-1510-QPw00.json`. The audit surfaced a 13th RUN-contract defect: `page-lifecycle.workflow.js` normalizes the top-level `page` field to board-relative (the 260818 fix logged below) but never touched the echoed `packet.page`, so the auditor's own `packet-run-mismatch` invariant could never pass on a fresh run. Fixed with one line, `parsed.page = page`; `pageflow.py audit` now PASSes this receipt.
- 260818 1435 · [DRAFT-CC] `§14` added, on a shape JL handed over rather than described: a labeling protocol written as `# · PHASE · WHAT HAPPENS · YOUR JOB · TIME · HOW OFTEN`, with the three bands once / the loop / what ends it. The page already stated the loop four times as AUTHORITY, and never once as WORK, so a reader could not find out what it would cost them. The count that falls out is that seven of eleven rows ask something of a person and four read `nothing`, five of the seven carrying a tick. `QPw00-Display3-who-does-what` renders it, and is the FIRST unit on this board with a frozen `intake/inputs/`: eight files with sha256, so every cell except TIME is transcribed rather than remembered. TIME is an estimate and says so on its own face, because `_runs/page/` holds one run whose five receipts are CHECK · REVISE · CHECK · REVISE · CHECK and four of the table's phases have never executed.
- 260818 1041 · [RESTRUCTURE-CC, JL ruled] the group was re-cut and this page became `QPw00`, the holder, on `QA00`'s precedent. Four rulings in one round. ① **The loop is the 00 page**: it keeps only the time axis, the transitions (§8), the operations test (§9), the Type-against-Phase axes (§11), RUN (§12) and the audit (§13). ② **One page per phase**, `QPw1` OUTLINE through `QPw6` CHECK, which SUPERSEDES this page's own `§10.1`: that paragraph kept DRAFT · PROBE · REVISE · CHECK as divisions because "their meanings depend on comparison and transition", and it was written when the loop had four phases and no phase had a contract of its own. Six now ship 111 to 286 lines each, and the comparison it protected stays here in §8 and §9, which is exactly what makes the split safe. COMPILE gets no page: zero lines of its own, folded into `haipipe-page-revise`. ③ **The human gate goes LAST**, `QPw00g`, after `QPw00r` the receipts, because the receipt READS the tick and can never hold it: the controller writes receipts, so a gate inside one is a machine writing its own approval, and a tick is mutable (a changed `intake/` drops `accepted: ✅` back to ⬜) while receipts are an append-only sha256 chain. ④ **The gate is accept-biased** (JL: "human should be more likely to accept it"): a person is asked to sign only after the machine's findings are all zero, so the gate is a confirmation and not an inspection. The bias changes what is PRESENTED, never who writes the tick; silence is still not consent, and a required gate with no durable evidence still routes to HOLD.
  §3-§7 now carry a hand-off line each rather than the phase argument, and the four scattered ticks (`approved:` on the outline, `verified` per bibex entry, `accepted: ✅` per display README, the Page Type ruling) are `QPw00g`'s question because no page holds them today.

- 260817 0738 · [DRAFT-CC] the loop became SEVEN phases and this page's Diagram now draws them; §3 to §7 still describe the four and are owed a REVISE round. The round's real question was JL's: "具体的 proof 应该由谁来做？我还没想好这部分是在 draft 阶段来做，还是在 outline 阶段来做？" Three contracts answered it three ways: `haipipe-page-draft` §🃏 said DRAFT creates the card in OWED state, `haipipe-page-evidence` §🧾 said a card "may arrive already PROPOSED" by DRAFT, and `haipipe-plugin-outline` §📐 said "the card is created at PROBE". **Ruled: PROBE creates it**, on the stake argument, and PROBE finally has its own contract at `page-workflows/haipipe-page-probe` instead of borrowing EVIDENCE's. Also settled without a separate round: one mark is not one card (many bullets may share one, `PP04` on QC1-visitlbp serves three), 🖼 display units are created at EVIDENCE and not earlier because their `intake/` freezes FROM a `proof/` that does not exist until an answer does, and 🧮 proof earns NO folder, closing `haipipe-plugin-outline`'s open ⬜. The 🧭 Page-phases stepper now draws seven, and its `PROBE` token resolves against the RECEIPT'S OWN DATE rather than a global alias, which would have relabelled every future PROBE as EVIDENCE.
- 260806 2107 · [REVISE-CC] swept to the 260806 architecture; state line now records the 260805 QB8e live RUN instead of calling it pending, dead `paper/workers/` path repointed at `paper/haipipe-paper/fn/`, §11 tree shows all ten Page Types with QB6 owning the roster, and live prose now says QA-probe with capitalized Q-executor/A-consumer slot words
- 260806 0210 · [PROBE-CC] a 12th RUN-contract ambiguity, found by re-auditing the QB8e bundle a day later: `pageflow.py audit` now reports `artifact-version-mismatch` on the RENDER hash alone, because later innocent rebuilds changed the html while the source hash still matches `final_version`. The receipt treats source:render as one identity; the contract must say the SOURCE hash is the version's identity and the render hash is advisory (a rebuild is not a mutation), or every rebuild retroactively breaks every closed run. Also: the bundle carries no `audit` key at all, so "audit PASS" survives only in session history, which is item ⑩'s snapshot-has-no-receipt-home problem wearing a second face.
260805 · FIRST LIVE RUN, `260805-0216-QB8e`: CLOSE, audit PASS, and the run's second product is a defect list for this page's own contract, 11 items recorded in the bundle and owed fixes here. The sharpest six: ① the workflow controller is not invocable outside a Workflow harness and the contract never says what a bare caller may do; ② the producer prompt omits the judge's findings, so a strict REVISE guesses (the controller forwarded them as a disclosed deviation); ③ "the local closing rule" is ambiguous for a mid-life Q page whose Decision rows wait on JL by design, so the contract must say run-level CLOSE certifies THE VERSION, not the page's decisions; ④ `mechanical_errors` scope is undefined, and board-scoped counting would let one foreign dead link forbid CLOSE forever; ⑤ warnings do not gate CLOSE, so the semantic judge is the only defense on a WARN-only page; ⑥ fresh judges oscillate (r1s1 waived unnumbered paragraphs, r1s3 raised them), and max_steps is the only brake. Also surfaced: no run_id minting rule, no concurrency rule while a foreign session rebuilds board/, the pre-run snapshot has no receipt home, extra bundle keys pass unaudited, and the Decision Now row shape diverges between the base and page-template.md.

260805 · The Page-Types admission row MOVED to `../QB6-page-types/QPs2-page-types.md`, created after JL asked whether Page Types deserve their own Q. Measured against this page's own `§10.2` split test, the list-of-types question passes all four: independent question, own Aims and States, its own closing rule, and the `page-types/` contracts as its continuation files. This page keeps the axis split (`§11`) and the lifecycle; `QB6` keeps the list, the admission test, and the D-starred separation ruling.
260805 · JL held the separation: "I still want to separate for-literature and for-value," and named the reason that decides it: each uses ITS OWN LANGUAGE to understand the Q and the A crossing the executor wall. That is a typed-records difference, and the base says the type decides "which typed records it fills," so the separation is principled rather than preferential. Option D added and starred: two types over ONE loaded structural core, so the register and entry anatomy is never stated twice. The earlier A recommendation under-weighted the translation layer by reducing the two routes to "which bank answers."
260805 · JL proposed `-for-display`, `-for-value`, `-for-literature` as new Page Types and asked how far the list grows. Added the Decision Now row: the recommended shape admits by STRUCTURE rather than by family name, because the type-resolution rule reads the filename and `S-Literature-1`, `S-Value-6`, `S-Display-2a` and `S-Main-3` all resolve to the stage type today, while the topic shape (register + nested `probes/` entries) is one structure appearing under two family names and is already enforced by `src/topic_entry_contract.py` with no loadable contract teaching a writer the same shape. A `-for-topic` admission would key on the declared `### Q-consumer register` marker, the same signal the checker already trusts.
260804 · Moved the Probe ownership and zero-copy discussion from the Paper board to this Page lifecycle owner. Added sections 2.4 to 2.6, Aims A4.2 and A4.3, the open family-adapter ownership decision, the one-active-Page handoff boundary, and the requirement that one Probe reference drive projection, context, dependency identity, and CHECK. The Paper S03/S04 layout remains an input case rather than the owner of the generic rule.
260804 · Opened a new DRAFT round for the automatic Page flow. Added RUN as a bounded dynamic router, the raw-material packet and phase receipt, producer/build/reviewer separation, version identity, CLOSE/HOLD stops, deterministic lifecycle auditing, branch coverage, and fault injection. Updated Aims A9 and A10, continuation files, Law, Glossary, and Discussion to track implementation and fresh validation separately.
260804 · Added JL's open discussion on an automatic AI-agent quality loop: what evidence proves the Page process works, which failures and branches must be audited, and how builder, checker, fixer, and approver remain separable.
260804 · Fresh-context audits followed the new skill without conversation history, accepted the process fixture, and rejected injected self-approval, symbolic hashes, and builder/judge collapse. Their findings led to strict source/render SHA-256 validation, explicit builder identity, independent artifact rehashing, packet/run matching, and receipt-to-receipt version continuity. They also correctly refused to treat a process fixture as semantic Page quality. Live Claude Workflow execution remains an honest open gate.
260804 · JL chose base-adoption option B and approved the `page-types/` plus `page-phases/` split. Added division 8, closed P1, and recorded that `for-*` belongs only to Page Types, phase skills use direct names, PROBE retains its four Q/A forms without introducing Entry, and `ADVANCE` remains deferred.
260804 · JL agreed that DRAFT, PROBE, REVISE, and CHECK remain Content divisions of QB5 by default. Added division 7, Aim A10.1, its completed State, and the dated Law that requires four tests before a phase becomes its own Page.
260804 · Reframed the page around one persistent Page and gave DRAFT, PROBE, REVISE, and CHECK one Content division each. Added separate divisions for non-linear transitions and operation routing. `REVISE → DRAFT` now means an explicit new round, and add, delete, move, and rewrite no longer determine the phase by themselves. No skill contract changed.
260804 · Created from the paper-board session that proposed one Page moving through DRAFT, PROBE, REVISE, and human CHECK, after fresh-context validation found four board phase contracts with zero inbound references.
