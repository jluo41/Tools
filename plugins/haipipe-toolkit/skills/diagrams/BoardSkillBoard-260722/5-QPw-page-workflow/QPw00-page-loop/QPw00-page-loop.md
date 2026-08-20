# Page · the loop: outline, draft, probe, evidence, revise, compile, check
state: 🟡 IN PROGRESS · Content runs in the loop's own order · open Aims: 23 of 31
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

**One Page across repeated rounds**: the PREPARE loop, its one gate, the unattended middle, and the explicit restart.

```text
                         📄 ONE PERSISTENT PAGE
                                  │
                                  ▼
   ┌─ 🧭 ① OUTLINE ⇄ 📮 ② PROBE ⇄ 🔎 ③ EVIDENCE ─┐   PREPARE · repeats until
   └──────────────────────┬───────────────────────┘   plan and evidence agree
                 🚧 gate   │   a PERSON ticks `approved:`; no machine may
                           ▼
   ✍️ ④ DRAFT ──▶ 🧵 ⑤ REVISE (⑥ COMPILE folded in) ──▶ 🧑 ⑦ CHECK
        ▲                                                    ├──▶ ✅ close
        │             CHECK routes back to any earlier phase ┘
        └────────── 🔁 new round · purpose or Aims reopened

  🔒 one round   purpose + Aims fixed
  🛠 operation   add · delete · move · rewrite
```

**Where an evidence card is born**, stated once so no two phase contracts can answer it differently:

```text
  🧭 OUTLINE   the MARK + the AIM   `- B4 · the four coordinates   📮 · 🎯 A4.1`
  📮 PROBE     the CARD     probe/PP<NN>-<slug>/ · serves: C4.P1.B4 · dispatched
  🔎 EVIDENCE  the ANSWER   binding: <QA path> · proof/ pulled · ids in ## Values
  ✍️ DRAFT     the SENTENCE that writes the landed number, citing the id
  🧵 REVISE    the polish, and it never changes a landed number
```

A plan is rejectable in ten seconds and must leave nothing behind, so OUTLINE may not open the file; the mark IS the proposal, so a card at DRAFT would be a second copy of it.
The Aims live in the plan file too, and that placement is what lets PROBE run ahead of DRAFT: a card's `consumer/` side carries what the page loses, that stake is an Aim, and the Aim exists the moment the plan does.

## Content

### 1 · Overview: what the loop is, and how to read the rest
**The claim this page makes**: a phase is defined by the ONE question it answers, not by the edit it performs, and a Page moves forward by satisfying a phase's exit rather than by being worked on.

#### 1.1 · The loop stated once, before any single phase
**The problem**: one Page is worked by many hands over many days, and the same visible edit can be two different acts.
Adding a paragraph under an existing Aim and adding a paragraph that creates one look identical in a diff.
So the loop names acts by their REASON, never by their diff.
Each phase is the question it answers: OUTLINE asks what shape, PROBE asks what is unknown, EVIDENCE asks what backs it, DRAFT asks how it is said, REVISE asks how it gets better, and CHECK asks where it goes next.
Progress is satisfying a phase's exit, a tick, a landed card, a verdict; hours of editing move nothing without the exit.
The Opening says where this page sits among its siblings.
This division says what the LOOP is.
Neither repeats the other.

#### 1.2 · How to read the rest of it
**The loop is not a line**: QPw00-Display4 draws it: phases ①, ② and ③ repeat as one converging PREPARE loop, and only a person's `approved:` tick on the plan releases the page into ④, ⑤ and ⑦.
Its intake is frozen out of the seven phase contracts and both legal-route tables; nobody has accepted it yet, so `accepted:` still reads ⬜.

```text
  §1        what the loop is, and the four words it spends
  §2-§7     the six phase divisions, in the LOOP's order: OUTLINE ① · PROBE ② ·
            EVIDENCE ③ · DRAFT ④ · REVISE ⑤ (⑥ folded in) · CHECK ⑦
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
```

How much of it has ever EXECUTED is a different card's question: `PP02` owns the run counts, and `§12.2` quotes them.

**Who executes each phase**: QPw00-Display6 names them.
Six agent files sit under `page-workflows/agents/`, five write-scoped producers plus ⑦'s read-only judge, and each walks one fixed skill stack whose shared law lives once in `ref/producer-contract.md`.

#### 1.3 · Workflow, phase, step and round are four different words
**The vocabulary rule**: the loop needs all four and none of them substitutes for another, which is why the word stays "phase" rather than "step".

```text
word         answers                      count in the ONE live run    repeats?
──────────────────────────────────────────────────────────────────────────────────
🌀 WORKFLOW  which LOOP is this?          1  · the run itself          no
⏱️ PHASE     which AUTHORITY acts?        7 defined · 2 used           YES
🔢 STEP      WHERE in this run?           5 · monotonic 1..5           never
🔁 ROUND     which PROMISE era?           1 · bumps only on a reopen   on reopen
```
📌 A phase is a TYPE and a step is an INSTANCE of one: in the one live run the single CHECK phase occupies steps 1, 3 and 5.

**All four in one receipt**: none may be renamed onto another.
(`step: 4 · round: 1 · phase: CHECK · route: REVISE`, four fields in one object)
Renaming phase to step would put two different meanings on one key inside a single receipt, and the auditor reads both.
`step` is the monotonic position that never recurs; `phase` is the kind of work that must be free to recur, which is the property the whole loop is built on.

**Why not "step"**: it would contradict the router's own name.
(RUN is deliberately not ADVANCE, `§12.1`)
The word must permit repetition, because CHECK may route back to any earlier phase, PROBE may be skipped entirely, and a page may re-enter DRAFT in a new round.
The one live run proves it rather than asserting it: CHECK ran three times and REVISE twice inside a single round, so a vocabulary that numbered them 1..7 could not describe what happened.

**The folder settles one of them**: it already carries the workflow word.
(`board/page-workflows/`, one skill per phase plus the head router)
The directory says which of the four words scopes the family, and the contracts inside it say which authority each phase holds.
So the full term is "workflow phase" where disambiguation is needed and "phase" everywhere else, and the 927 occurrences of the word across this board and the skill tree stay as they are.

**Two more words ride along, defined here and spent everywhere below**: a PAGE persists through all of it, and an OPERATION is one edit act upon it: phases are named by reason, operations by shape.
The four words are defined at the top, before any division spends them.
What keeps the siblings honest is a sweep of the family's contracts for a phase called a step or a step called a phase, and A1.2 tracks it.

### 2 · OUTLINE ①: the head of a loop that converges
**The OUTLINE contract**: what it decides, what it leaves alone, and what ends it.

```text
🧭 OUTLINE
   asks     what will this page say, division by division, and what does each
            bullet still owe?
   writes   <page>/outline/<stem>-outline-v<N>.md, and nothing in the page
   marks    a hole, and then STOPS. It raises no card and asks nothing.
   loops    with ② PROBE and ③ EVIDENCE until the plan and its evidence agree
   exits    a person ticks `approved:`. Nothing else ends it.
```

#### 2.1 · What OUTLINE decides, and what it leaves alone
The deliverable is the section list, the paragraph under each section, the bullets under each paragraph, and what each bullet still owes.
It all lives in ONE file, `outline/<stem>-outline-v<N>.md`, and the page's own prose stays untouched until DRAFT.
OUTLINE marks a hole and stops there: raising cards and dispatching questions is PROBE's job.

#### 2.2 · The Aims are agreed here, not later
The Aims are settled in the plan file itself, and not at DRAFT.
Shape and target are read once and approved by one tick.
Every bullet that owes something names its Aim by id, so no id can dangle, and DRAFT transcribes those Aims onto the page rather than inventing them.

The plan carries both the Aim's id and its target, so a renumber moves them together and no id can point at a target the plan does not hold.

The same placement is what lets PROBE run ahead of DRAFT.
A probe card's stake is an Aim, so PROBE can start no earlier than the phase that settles the Aims.
The Aims exist the moment the plan does, so the card carries its stake from the plan and waits for nothing.

#### 2.3 · The loop, and what makes it stop
**Evidence changes the plan, and never just confirms it**: this page's own PREPARE loop shows both directions: a planned division scored 0 of 4 on `§10`'s split tests and was folded away, and a planned count of 17 was recomputed as 13 before the tick (both recorded in outline v3).

Four machine checks run on every version of the plan.
Coverage: every mark is served both ways.
Address: every `serves:` resolves.
Value: every quoted number recomputes.
Shape: the divisions match the page type.
The person is asked LAST, and for DIRECTION rather than arithmetic: the machine already proved the numbers, so the tick's question is whether the plan aims at the right thing.
A tick belongs to the version it ticked.
Quietly editing an approved plan is how `serves:` addresses go stale; a changed plan gets a new version and a new tick.

**What the gate sees on this board today**: `PP06.v1` counts 17 plans, and `PP06.v2` finds 6 that pass all four checks.
Coverage is the common failure (`PP06.v3`, 10 plans); address and shape fail none (`PP06.v4` and `PP06.v5`, both 0); value fails one (`PP06.v6`).

The plan is ONE file, so its folds serialize: PROBE and EVIDENCE fan out safely across separate folders, and one OUTLINE pass per round is the merge point.
The FIRST check is the human's own look, ruled after this page's own live round: the look is cheap and early, and it catches structure and style before any card is raised or run is spent.
The look is not the gate.
`approved:` ends the loop, and it is taken only after the four checks pass.

#### 2.4 · The gate that ends the loop
```text
  change a section list   BEFORE the prose   one line
  change a section list   AFTER  the prose   the prose
```

No machine may write the tick: it is the loop's one hard human gate.
A phase whose entire output fits on one screen, and which a person can reject in ten seconds, belongs in front of every expensive phase rather than folded into one.
The file's shape, its marks and its version rules live at `QPw1-outline` and `haipipe-plugin-outline`.

### 3 · PROBE ②: turning a mark into a card, and asking
**The PROBE contract**: an approved mark leaves the plan, becomes a card, and is asked.

```text
📮 PROBE
├── 📥 enters    the approved mark, still bare, from the plan
├── 🧭 owns      the MATCH lookup, the card, and the dispatch
├── 🗂 writes    probe/PP<NN>-<slug>/ · consumer/ · executor/
├── 📤 exits     the moment the stripped question leaves
└── 🚫 avoids    target Page prose · landing the answer
```
📌 PROBE turns an approved mark into a card and asks; landing what comes back is ③ EVIDENCE's job.

#### 3.1 · The phase in one paragraph, pointing at QPw3-probe
The card holds the question, its `serves:` backlink into the plan, and later its `## Values`; the question goes out stripped of stake.
PROBE is the only phase that may create `probe/PP<NN>-<slug>/`: OUTLINE marks, and EVIDENCE fills.
It looks before asking, MATCH before RAISE: an existing card on this page, a PageX match, or a QA-bank answer to the same question is reused, never duplicated.
The trigger, the four-step MATCH lookup, and the optional-when-no-unknown-is-hidden rule live at `QPw3-probe`.

#### 3.2 · The three rules argued nowhere else
**Filing a QA-probe does not name the target Page**: the probe layer never learns which page consumes the answer, and that wall is what keeps executors stake-blind.
A family may file the QA-probe under an evidence route such as Literature or Value without transferring the Q-consumer, the A-consumer, or the State to that route's topic Page.
Treating physical placement as an ownership transfer gives one exchange two Page-facing consumer surfaces before the answer reaches prose.

**One active Page bounds the consumer write**: a PROBE run writes consumer rows only into the one page it was opened for.
When the same Q-executor serves other Q-consumers, the Probe surface records their references and makes the answer available, and each sibling page interprets it through its own PROBE or REVISE route, with its own version and CHECK.
This preserves one Q-executor for reuse without turning one answer into an unbounded cross-Page edit.

**One reference shows the whole chain**: from the bullet's mark to the card, to the QA file, to the pulled proof, every hop is a recorded pointer, so a read-only projection can render the chain without a second authored copy.
Missing targets, superseded answers, or changed source hashes must fail visibly rather than leave an old projection looking current.

**One edge stays open, and it is recorded rather than hidden**: whether a family adapter may transfer Q-consumer ownership after handoff is the open Decision Now row below, and `A3.2` waits on it.

### 4 · EVIDENCE ③: landing what came back
**The EVIDENCE contract**: what enters, the lanes it runs, and what ends it.

```text
🔎 EVIDENCE
   enters   a dispatched question that has returned, a known bib key, or a
            unit whose material exists
   lanes    📚 citation · 🧮 value · 🖼 display      IN PARALLEL
   stages   ① MAKE the thing · ② BIND it so a sentence can name it
   exits    every marked bullet has its thing on disk, or a named HOLD
```

#### 4.1 · The whole phase on one picture
QPw00-Display5 draws the division at once, and its head is the probe card: the plan ASKS, the card answers, the value lane fills the card itself, a data display freezes FROM the card's `proof/`, and the citation lane is a person's and does not pass through the card.

```text
  ① MAKE   build the thing in the folder that owns it
           📚 the bibex entry
           🧮 the card's answer, pulled into proof/
           🖼 the unit DRAWN: intake · recipe · assets · preview.pdf

  ② BIND   make it pointable, so a sentence can name it and be checked
           📚 the key resolves in bibex/                   `verified` ✋
           🧮 target: names the answering QA file by PATH  `read:` ✋
           🖼 the unit is previewable, its intake frozen

  ─────────── the page's prose starts HERE, and this phase stops ──────────
  ⑤ REVISE the sentence that uses it, its caption, the projections
```

Neither stage touches this page's `## Content`.
That is the whole boundary: EVIDENCE changes what the page KNOWS and REVISE changes what it SAYS.
A phase that both landed the answer and wrote the sentence could not be audited, because the only evidence that the answer came first would be its own report.

#### 4.2 · 📮 The probe mark, the ask the lanes answer
A 📮 mark sits on a bullet that ASKS.
The bullet keeps only the question; the answer arrives later as an append plus the card's values.
One card may serve many bullets, and its `serves:` line lists every address it answers.
The ask and the quote share one `probe/` folder: 📮 marks the ask, 🧮 marks a quote of one landed number, and both point into the same card.
The live example is one division up: `§1.2`'s counts stand on `PP01`, whose card carries the question, its state, and the three landed values.

#### 4.3 · 🧮 The value lane
**What it lands**: a number bound BY PATH to the QA file that answered it, with the pulled file sitting in the card's own `proof/`.

```text
  made by   the bank, task or discovery, answering into its own QA file.
            PROBE already raised the card and asked.
  tick      `read:`, and it REVERTS when `target:` changes or proof/ is re-pulled
  id        PP<NN>.v<n> · one card holds several numbers
```

**One card, many values.** A card is ONE question, and its answer usually holds several numbers, so the id goes one level deeper: allocated in `card.md`'s `## Values` block when the answer lands, and never before.
That is what makes two failures visible instead of silent: a number in the prose citing no `PP<NN>.v<n>`, and a value in a card that no sentence uses.
Both directions are checked, and the 🔢 tab reports them: a surface with no storage, because the number already lives in `proof/` with its source, run and sha256.
The live example: this page states 7 declared phases from `PP01.v1`, 6 contracts from `PP01.v2`, and 5 person-reserved ticks from `PP01.v3`.
The card's v4 row reads `NOT HERE` and points at `PP02`, because run counts are that card's question, and its `read:` still reads ⬜, so every one of these quotes still waits on a person.

#### 4.4 · 📚 The citation lane
**What it lands**: one entry in `bibex/<stem>.bib`, and a key a sentence can cite.

```text
  made by   a PERSON, verbatim. A machine may SUBSET or TRANSCRIBE bibtex
            and may never COMPOSE it.
  tick      `verified`, on the entry itself. It does not revert.
  failure   a 📚 mark naming a sibling board page. That is a cross-reference,
            written in the bullet's own words; only a bib key wears 📚.
```

`verified` never reverts because provenance does not decay: it records that a person read the entry against its source.
The live example is this page's own store: `luo2026eventglucose` was transcribed verbatim from QPf4-chat's bibex and carries its `verified = {<who> <date>}` signature, so a sentence here may cite the key and its chip resolves green.

#### 4.5 · 🖼 The display lane
**What it lands**: a DRAWN, previewable unit, not a folder of material.

```text
  ① INTAKE  🧑 freeze the material           EVIDENCE
  ② RENDER  ⚙️ the renderer writes recipe/   EVIDENCE
  ③ PICK    🧑 choose among candidates/      EVIDENCE
  ④ BUILD   ⚙️ assets/ · float.tex · preview EVIDENCE
  ⑤ ACCEPT  🧑 README `accepted: ✅`         CHECK      the human tick
```

Steps ② to ④ live in this lane because a display's return must be as directly usable as the other lanes': a citation lands a key, a value lands a bound number, so a display lands a drawn unit rather than an unrendered folder.
Which units wait depends on their kind: a DATA unit (table, figure) freezes its intake FROM a probe card's `proof/` and waits for an answer, while a CONCEPT unit (diagram, tex, illustration) freezes a listing of source files and waits for nothing.
The intake manifest pins every source with a sha256, so a moved or edited input is computable staleness, and `accepted: ✅` reverts with it: acceptance binds to the frozen inputs it was accepted with.
The live example is QPw00-Display3, one glance down at `§14`: a concept unit with 15 frozen inputs in its `intake/manifest.yaml`, `accepted:` still ⬜, and cited both here and by `§14`'s table, which is legal because a unit owes AT LEAST one citing sentence, not exactly one.

#### 4.6 · What the three lanes have in common
```text
  📚 citation   ─▶  bibex/<stem>.bib entry   returns a bib key
  🧮 value      ─▶  probe/PP<NN>-<slug>/     returns a number bound to its run
  🖼 display    ─▶  display/<unit>/          returns a drawn, previewable figure
```

They run at the same time, and none waits for another: the fold at ① OUTLINE is the only merge point.
Each return is directly usable by a sentence: a citable key, a quotable id, a previewable figure.
Three ticks live here and two of them revert: `verified` never, `read:` when `target:` changes or `proof/` is re-pulled, `accepted:` when the frozen intake changes.
The ticks belong to stage ② BIND, because a tick is what turns a made thing into one a sentence may quote; `accepted: ✅` is the exception and stays at CHECK, since what it judges is the drawn artifact as a reader meets it.

**EVIDENCE on this board, counted**: `PP03.v1` finds 23 probe cards, `PP03.v2` 13 still at `planned`, `PP03.v3` 0 read by a person, `PP03.v4` 10 of 10 display units rendered, and `PP03.v5` 0 accepted.
Every person-reserved tick in this phase is open across the whole board.
The lanes are real folders under real contracts with almost no traffic, and saying so is the difference between a contract and a description.

The lane contracts are `QPw4c-citation`, `QPw4v-value` and `QPw4d-display`, under the phase contract `QPw4-evidence`.

### 5 · DRAFT ④: turning each point into sentences
**The DRAFT contract**: what enters, the one conversion it performs, and what it hands forward.

```text
✍️ DRAFT
   enters   an approved plan whose evidence has ALREADY landed
   does     one approved POINT ──▶ one or more SENTENCES that write the number
   cites    every value, key and figure BY ID, at the place it is used
   never    invents a value, a citation, a reading, or a rendered figure
   exits    every point in the plan has become prose; a hole is the EXCEPTION
```

#### 5.1 · What DRAFT actually does, now that the Aims have left
DRAFT enters on landed evidence, so it writes the NUMBER itself rather than a placeholder: the PREPARE loop already landed everything a sentence needs.
A hole is the exception, not the normal case, and it names the input it is missing rather than just marking a gap.
The Aims are settled at OUTLINE, and this phase transcribes them onto the page rather than inventing them.
It executes the approved plan and names nothing new: a shape found wrong during DRAFT goes back to OUTLINE as a new version, never a quiet local fix.
And it is named by reason, never by diff: the same edit shape can be DRAFT or REVISE, and only the reason distinguishes them.

#### 5.2 · One point becomes several sentences, and the join survives both ways
QPw00-Display7 draws the conversion in both directions: one approved POINT becomes one or more sentence scaffolds, and the join survives later edits because it is carried twice.

```text
  🧭 plan     C3.P1.B4 · Robustness across specifications   🧮 PP01.v1 · 🖼 Display4
                 │
                 ▼  DRAFT
  📄 page     C3.P1.S1 · The primary estimate is 0.42 (PP01.v1).
              C3.P1.S2 · It moves by less than 0.03 across specifications (PP01.v2).
              C3.P1.S3 · Display4 compares the estimates.
```

One bullet is a POINT, not a sentence, so the two sides count different units and say so.
`C3.P1` is shared, and only the last token differs: B for a point in the plan, S for a sentence on the page.
The backlink also rides in a comment on the scaffold line, `<!-- realizes: C3.P1.B4 -->`, so REVISE may split or merge the sentence later without losing it.
When a question stayed genuinely BLOCKED, the sentence keeps a visible hole carrying the card that owes it, so a reader sees what is missing and who owes it; `§14.1`'s PP05 hole is this page's one worked example.
A sentence may never invent a value, a citation, a reading, or a rendered figure: a sentence that already knows its answer was written after the fact, and holes keep the order honest.

#### 5.3 · How it is written, because a scaffold is still prose
One idea per sentence, and a sentence past about thirty words is usually two.
The haipipe-writing plain rules apply to scaffolds, not only to finished prose.
The AI-tell catalogue at `haipipe-writing/ref/ai-tells.md` applies HERE and not only at REVISE, because machine cadence written at DRAFT gets rewritten twice instead of once.
**What a scaffold may not contain**, as a list a writer can check against: an invented number; a hedge standing in for a hole; a summary of what a card says, which the 🧭 tab already reads live; or a division the plan did not name.
Each forbidden thing is a way of smuggling unlanded evidence into prose.
The full contract and its worked example live at `QPw2-draft`.

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

#### 6.1 · The phase in one paragraph, pointing at QPw5-revise
REVISE improves the realization while purpose and Aims stay fixed; if either moves, it is not REVISE, and the work reopens OUTLINE in a new version or DRAFT in a new round.
It is the phase that fills a landed hole: the hole is replaced by the number plus its id, never by a restatement of the card.
Its fixed-promise test, its five-step LAND, ARGUE, SOUND, CITE, BUILD order, and the `latex/` and `word/` rebuilds live at `QPw5-revise`, which also carries COMPILE.
This page's own `§9` still carries the shared DRAFT-versus-REVISE test table that separates the two phases on the same edit, so a reader is pointed sideways as well as forward.

#### 6.2 · ⑥ COMPILE is a step of this phase, not a division of its own
**Scored against `§10`'s four split tests**, rather than asserted:

```text
  ① an unresolved question that is not just asking for its definition
     ❌ its only open question is whether the fold is permanent
  ② needs its own Aims and States rather than borrowing
     ❌ its one Aim was the fold itself; nothing else was ever tracked
  ③ an independent closing gate
     ❌ no tick, no receipt, no gate anywhere
  ④ its own continuation map in Files
     ❌ shares REVISE's
                                                        0 of 4 → it stays here
```

COMPILE rebuilds `latex/` and `word/` from the source as it now stands. That is real work with a real audit code, `projection-stale`, and it is the only member of the loop with no contract file, no receipt in any stored run, and no tick.

The loop declares seven phases and the Diagram draws ⑥, because that count is cited across the contracts.
COMPILE gets no division at the same level as the six phases that have one, because a heading of its own would assert a symmetry the four tests refuse.
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

#### 7.1 · The phase in one paragraph, pointing at QPw6-check
CHECK judges one exact version and routes it: CLOSE, or back to the phase that owns the fix.
Only CHECK closes; producers may HOLD or hand forward, and the judge alone ends a page's run.
It judges and never repairs, because a fix by the finder would erase the independent finding; repair returns to a producer.
The judge-may-not-repair separation, the three independent built-artifact counts it reads, and the accept-biased human gate live at `QPw6-check`: unclear findings route forward for repair rather than blocking the page.
This page's own `§13` still carries the receipt fields and invariants CHECK's routed findings are measured against, so nothing here is left an orphaned reference.

### 8 · Transitions form rounds, not a rigid conveyor belt
**The transition grammar**: repetition is legal, and returning to DRAFT changes the round.

```text
📄 ROUND n · purpose + Aims fixed

┌ 🧭 OUTLINE ⇄ 📮 PROBE ⇄ 🔎 EVIDENCE ┐ ↺ PREPARE · until plan and evidence agree
└───────────────┬─────────────────────┘
   🚧 `approved:`│
                 ▼
   ✍️ DRAFT ──▶ 🧵 REVISE ↺ ──▶ 🧑 CHECK ──▶ ✅ close
                     ▲               │
                     └── sent back ──┤  CHECK may return to any earlier phase
                                     ▼
📄 ROUND n+1 ◀── ✍️ DRAFT ◀── purpose or Aims reopened
```
📌 The arrows express dependencies and routing choices, not a rule that every phase runs once.

#### 8.1 · The three rules, and the split they made safe
The common order is not the only legal order: rounds may repeat phases or skip them, and the route table defines legality, not habit.
`DRAFT, DRAFT, PROBE, REVISE, DRAFT` is a legal history: two repeated design passes in one round, an optional question, a repair, and a final DRAFT that means revision reopened the promise and began a new round.
REVISE to DRAFT is that restart, not a forbidden edge: the Page persists, earlier evidence remains available, and its relevance is re-checked against the new promise, while any earlier closing decision stops applying.
A phase label requires a reason: "we edited prose" names no phase, "the aim moved" does, and without the reason two identical diffs can be mislabeled as different phases.
These rules are what made the six-page split safe: six phase pages split out of this one, and the comparison and transition grammar they must agree on stays here, in `§8` and `§9`, where one home keeps them auditable.
The shape to take away is three bands, not eleven steps: OPEN happens once, the PREPARE and writing phases repeat, and the CLOSE acts happen when CHECK stops the loop; `§14` prices the same shape as work.

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

#### 9.1 · The table the sibling pages cite
Adding and deleting name no phase: adding a paragraph to explain evidence for an existing Aim is REVISE, and adding one because the Page now answers a new question is DRAFT.
Deleting unsupported or duplicate prose while keeping the Aim is REVISE; deleting the promised result itself, or its Aim, is DRAFT.
Moving and rewriting use the same test: improving flow under the same argument is REVISE, and changing the argument the Page promises is DRAFT even when the diff is one moved heading.
PROBE and CHECK produce records on different write surfaces, cards and verdicts, and neither touches page prose; when either causes target prose to change, the edit runs under REVISE or a restarted DRAFT.
Sibling pages cite this page by `§` address rather than copying it (`QPw1-outline` pins `QPw00 §6` and `QPw6-check` pins `QPw00 §10` in their Files today), so a silent move of any division here, this table included, breaks their pins.

### 10 · One lifecycle Page holds the phases together
**The Page split rule**: each phase begins as a Content division and earns a Page only by becoming an independent question.

```text
✂️ a phase earns its own Page · ALL four required
├── ❓ an independent question, not just its definition
├── 🎯 its own Aims and 📍 States
├── 🚪 an independent closing gate
└── 📁 its own continuation files

⚙️ phase skill   executable law, loaded one contract at a time
📄 design Page   an independently closable question
🚫 mapping       neither implies the other
```
📌 Shared boundaries stay together; a phase moves out only when it can carry and close a question of its own.

#### 10.1 · The division its own ruling overturned
A phase begins as a Content division here and earns a Page of its own only by becoming an independently closable question: one it can close with its own evidence, its own gate, and its own continuation files.
The four tests above decide it, and they are not left abstract: the re-cut that made this board's phase pages scored the phases against them, overturned this division's stay-together default, and split six pages out, `QPw1-outline` through `QPw6-check`, while COMPILE scored 0 of 4 and stays a step of `§6`; the Log keeps that ruling.
Separate skills still do not require separate design pages: a phase skill is executable law a worker loads one contract at a time, a design page is an argument, and one phase may have both or either.

### 11 · Page Type and Page Phase are separate skill axes
**The skill composition**: the base resolves what the Page is and how the current work is acting on it.

```text
📄 haipipe-page                the shared Page contract and router
├── 📁 page-types/             what kind of Page PERSISTS · QB6 owns the roster
│   ├── for-stage · for-task · for-venue · for-section · …
│   └── sixteen variants across six skill sets (haipipe-page 0.36.0)
└── 📁 page-workflows/         what AUTHORITY acts now · page-phases/ is its retired name
    ├── haipipe-page-outline ① · haipipe-page-probe ② · haipipe-page-evidence ③
    ├── haipipe-page-draft ④ · haipipe-page-revise ⑤ · haipipe-page-check ⑦
    └── haipipe-page-workflow · the RUN router that composes them

one invocation = base + matching Page Type + current Page Phase + family worker
```
📌 Page Type and Page Phase are orthogonal, so their folder names and skill names must not collapse them into one label.

#### 11.1 · The axis split
`for-*` names only Page Types: the preposition says which persistent Page shape varies from the base, and the roster has grown to sixteen variants across six skill sets, with `QB6` owning the admission test and the list.
Phase skills use direct names, `haipipe-page-<phase>`, because a phase is an active authority and not a Page variant, and it applies across Page Types.
PROBE keeps one vocabulary across the boundary: the target Page owns the stake-bearing Q-consumer, the phase strips it into a neutral Q-executor, binds the returned A-executor, and writes an A-consumer interpretation for each consumer; one Q-executor may serve several Q-consumers, and `haipipe-probe` remains the shared crossing protocol.
The paths are one rename behind in places: contracts still name `page-phases/`, the retired folder name, and each is one mechanical sweep away from correct.
The base-adoption question itself is closed as `P1`: option B won, the smallest reversible adoption, and the concrete router later earned the verb RUN rather than ADVANCE.

### 12 · RUN turns the phase grammar into a bounded loop
**The executable flow**: one controller composes separate producer, builder, and judge roles without prescribing one phase sequence.

```text
📦 raw-material packet
│  Page · Type · start Phase · intent · sources · constraints · gate · limits
▼
🧭 controller
├── every phase except CHECK          ─▶ producer
├── 🏗 build + version snapshot       ─▶ mechanical builder
└── 🧑 CHECK exact version            ─▶ fresh read-only judge
                  │
                  ├── ✅ CLOSE
                  ├── 🧵 REVISE ──────┐
                  ├── 🔎 EVIDENCE ────┤
                  ├── ✍️ DRAFT round+1│
                  └── ⏸ HOLD          │
                                      └──▶ controller ↺
```
📌 RUN follows returned authority routes and stops at explicit terminals or limits.

#### 12.1 · A router, not a conveyor belt
RUN means execute the current Page lifecycle from a named starting authority until CLOSE or HOLD; it is not ADVANCE, which would promise forward-only steps.
The controller reads each phase's requested route and follows the legal-route table, which is dynamic: producers may repeat or hand off, and only CHECK may CLOSE.
The packet bounds what agents may know: it names the Page, its Type, the starting Phase, the run intent, source paths, settled constraints, the closing gate, and step and round limits; context beyond it is contamination.
A missing source, unknown gate, or ambiguous authority becomes HOLD rather than an invented input.
The controller itself only routes, because writing or judging from the controller would collapse the producer, builder and judge separation it exists to keep: the producer performs exactly one phase, the mechanical builder rebuilds and snapshots the version, and the fresh judge returns the verdict, testing for CHECK rather than listing producer phases.
Every stop is honest: CLOSE, explicit HOLD, missing input, failed build, version mismatch, required human ruling, maximum steps, or maximum rounds; reaching a limit says the process did not converge within its budget, and it never says the Page passed.

#### 12.2 · The loop drawn, and what it has actually done
QPw00-Display1 states the controller as an algorithm, so a reader can see the three actors alternate and read the stop conditions in the order the loop tests them.
QPw00-Display2 writes the legal-route table as six explicit row-sets and derives the laws this prose would otherwise assert: PROBE and EVIDENCE route only sideways or BACK to OUTLINE, so OUTLINE's gate is the one door into DRAFT; and CHECK cannot route to CHECK, so a judged version reaches a second judgment only through a producer.

**The runs so far, counted**: `PP02.v1` finds 4 runs stored under `_runs/page/`, `PP02.v2` 24 receipts across them, `PP02.v3` 6 of 7 phases covered, and `PP02.v4` exactly one phase never executed, COMPILE.
So the loop is fully specified and all but one phase exercised, and the one phase with no receipt anywhere is also the one with no contract of its own.

#### 12.3 · The producer role is filled per phase
Each phase is executed by its own producer: the controller's `PRODUCER_AGENTS` table maps a phase to `haipipe-page-<phase>-agent`, with the creator agent as the fallback.
The agent files stay thin wrappers: each carries identity, skill chain, walls and receipt duty, and the shared law lives ONCE in `ref/producer-contract.md`, because an agent file that restates a contract is a mirror, and mirrors drift.
**Counted on disk**: `PP07.v1` finds 6 agent files under `page-workflows/agents/`, `PP07.v2` 5 phases owning a producer of their own, `PP07.v3` 2 sharing or borrowing one (COMPILE and CHECK), and `PP07.v4` 4 support agents beside them.
The roster itself, with each unit's daily debts, lives on `QPw00a`: this page owns the RULE, because a mirror of the roster here would drift within a day.

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

#### 13.1 · What a receipt binds, and what a pass does not cover
Each receipt binds one attempted phase to its actor, its builder, its status, the source and render SHA-256 identities before and after, the route it requests, and its reason, artifacts, evidence, findings and human-gate state; CHECK additionally binds `checked_version` and a verdict.
Receipts are ordered and stored outside Page discovery under `_runs/page/<page-id>/<run-id>.json`, and the deterministic auditor independently rehashes the artifacts on disk, so a claim repeated inside a receipt is never accepted as its own proof.
Seven invariants make the loop auditable, among them version continuity from receipt to receipt, one writer per pen with distinct actor identities per role, legal routes only with CLOSE reserved to CHECK, packet and limit matching, and a human gate that closes only on durable evidence.
Testing covers both directions: the happy paths and branch routes must pass, and injected faults, self-approval, mutation after CHECK, illegal routes, broken continuity, symbolic hashes, missing human evidence, must each be rejected for the specific invariant they violate.
Quality is evidenced, never declared: a green audit proves the declared process ran, not that every substantive claim is true, and silence is never a pass.

**The auditor, run on this board's own receipts rather than described**: `PP04.v1` audits 4 stored runs, `PP04.v2` finds 0 that PASS, `PP04.v3` 8 findings, `PP04.v4` 5 distinct fault codes, and `PP04.v5` exactly 1 real contract violation.
The real one is `checked-version-mismatch`, on a stored CHECK receipt: CHECK must leave `version_before`, `version_after` and `checked_version` identical, because a judge reporting on a version it did not read is the one failure the receipt exists to catch.
No reasoning predicted it; running the auditor found it.
Most of the rest is expected noise, `artifact-version-mismatch` on pages edited after their runs closed, which is the recorded cost of auditing live pages rather than frozen ones.

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
QPw00-Display3 renders this table for print, with the fifteen files it is transcribed from frozen beside it.

#### 14.1 · TIME is the only estimated column, and it is estimated because nothing has been timed
**The one measured number is zero**: `PP05.v1` reports 0 phases with a measured duration, and `PP05.v2` names the 2 inputs that block it.

Every phase's real duration is <HOLE: PP05 blocked, no stored receipt carries a start/end pair, and COMPILE has no receipt at all (PP02.v4)>, so the TIME column stays an estimate on its own face.

```text
  ① every stored receipt carries ONE timestamp,   a completion time, not a
     the newest PROBE receipt included             start/end pair     PP05.v2
  ② one phase has never run at all                COMPILE            PP02.v4
```

Block ① is the one to fix first, because it is a contract change rather than work: the receipt shape in `ref/page-run-contract.md` needs a per-phase start and end stamp.
Block ② then clears by running the loop once end to end.
An estimate was not substituted, because substituting one is how this column got its current values.
Every other cell is transcribed from a file frozen in `display/QPw00-Display3-who-does-what/intake/inputs/`: the manifest names all fifteen with the sha256 of the copy AND of the live source, so `checks/intake.py` can recompute staleness on demand.
Row 3d carries no estimate at all, because nobody has priced the lane's render, pick and build steps.
A number nobody has measured is marked as an estimate on the table's own face rather than left to look like the others.
Once receipts carry start and end pairs, the column is rebuilt from `_runs/page/` timestamps instead of estimated, which is `A14.2`'s whole test.

## Aims

Every Aim is one row: the tick says where it stands, `Done when:` is the test a reader can apply without asking anyone, and `Now:` is what is true today.

🔒 Target and test are transcribed from the approved plan `outline/QPw00-page-loop-outline-v3.md`, which is where Aims are settled (JL 260819). `Now:` is the page's own, and `## States` merged into this section the same day (`haipipe-page` 0.34.0).

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
      📍 `A3.2` owns the boundary between the active target Page and an evidence route supplied by a family.
      🔔 `Why now` the Paper adapter currently makes the Literature or Value topic Page canonical after another Page raises the Aim, while this page's `§11.1` (QB5 §8.3 before the renumber) says the target Page owns the Q-consumer.
      `A ·` Allow the transfer. The evidence topic Page owns the stake, A-consumer, State, and Probe path; this keeps a self-contained topic register but makes one PROBE a multi-Page consumer write.
      ⭐ `B ·` Keep ownership on the Page that raised the Q-consumer. The QA-probe may be filed under any family route, while topic Pages show a derived rollup and receive their own lifecycle only when their synthesis changes.
      🛑 `Blocks` changing the Paper topic-entry contract and implementing the zero-copy topic projection.
      🤖 `If nobody answers` the implemented Paper topic-owned rule remains unchanged, and `§3.2` stays the recommended shared boundary rather than shipped family behavior.

### A1 · 🧭 Overview: what the loop is, and how to read the rest
- ⬜ A1.1 · The loop is stated once, whole, before any single phase is argued.
  **Done when:** a reader can stop after §1 and say what the seven phases are, which one they are in, and where to read next.
  **Now:** Not met. §1 states the loop whole this round, PREPARE first, and no reader has been asked whether they can stop there and still say what the seven phases are.
- 🔨 A1.2 · No document in this family uses one of the four words for another's meaning.
  **Done when:** a sweep finds no receipt field, contract sentence, or page division calling a phase a step or a step a phase.
  **Now:** Being worked on now. The four are separated here and in `haipipe-page-workflow`; the sweep across the other 63 pages of this board has not run.
- ✅ A1.3 · The four are readable from one figure without opening the receipt.
  **Done when:** each word carries what it answers, its count in a real run, and whether it repeats.
  **Now:** Met. `§1.3`'s figure carries all four with their live counts from `260805-0216-QB8e`.

### A2 · 🧭 OUTLINE ①: the head of a loop that converges
- 🔨 A2.1 · OUTLINE has a division of its own, stating its authority, its deliverable and the tick that ends it.
  **Done when:** the body opens on phase ① rather than phase ②, and a reader reaches DRAFT already knowing what an approved plan is.
  **Now:** The body opens on phase ① and `§2` states authority, deliverable and tick; whether a reader reaches `§5` already knowing what an approved plan is has not been tested on a reader.
- 🔨 A2.2 · The Aims are settled during OUTLINE, in the plan file, and every owing bullet links to one by id.
  **Done when:** no bullet names an Aim the plan does not declare, and DRAFT transcribes the Aims rather than inventing them.
  **Now:** Exercised again this round: outline v3 declares all 31 Aims and this section is transcribed from it. The rule is still absent from `haipipe-page-outline` itself, whose 0.6.0 text names no Aims at all.
- 🔨 A2.4 · The loop's order is argued from what each phase NEEDS, not from habit.
  **Done when:** a reader can say why PROBE may run before DRAFT now and could not before 260819.
  **Now:** Written this round: `§2.2` states the stake argument that moved PROBE, and `§2.3` records the fold cases and the one merge point.
- 🔨 A2.5 · Self-consistency is four checks a machine runs, and the human tick is scoped to what they cannot reach.
  **Done when:** all four are named with the tool that runs them, and the tick's question is stated as direction rather than correctness.
  **Now:** Written this round in `§2.3` with PP06's counts landed; the four checks are named there and the tick's direction-only scope is stated in `§2.3` and `§2.4`.

### A3 · 📮 PROBE ②: turning a mark into a card, and asking
- ✅ A3.1 · PROBE has an explicit trigger, write surface, return record, and exit.
  **Done when:** a reader can route a consequential unknown without letting PROBE author target prose.
  **Now:** Met 260818, renumbered 260819. `§3`'s face card, pin line, and `§3.1` state PROBE's post-260817 meaning consistently with the Diagram and the Opening, and point at QPw3-probe rather than re-arguing it.
- 🧠 A3.2 · The target Page, Probe surface, sibling handoff, and forbidden cross-Page write are unambiguous.
  **Done when:** a family can file a QA-probe by evidence route without silently transferring Q-consumer ownership or authoring a sibling Page in the same run.
  **Now:** Waiting on the open Decision Now row. `§3.2` states the origin-owned, one-active-Page alternative and the Paper S03/S04 case that exposed the ambiguity.
- 🧠 A3.3 · One Probe reference can show the full evidence chain without becoming a second authored answer.
  **Done when:** the reference drives render projection, bounded phase context, dependency versioning, visible failure, and CHECK.
  **Now:** Waiting on A3.2. The Board already supports live Markdown embeds and scoped Related Board Pages, but no single Probe reference drives display, context, dependency identity, and CHECK.

### A4 · 🔎 EVIDENCE ③: landing what came back
- 🔨 A4.1 · EVIDENCE is readable as parallel lanes, and the marks a plan can carry are named against the three lanes that exist.
  **Done when:** a reader can say why 📮 probe and 🧮 value are two marks over the one probe/ folder, without opening another contract.
  **Now:** Rewritten this round to the plan's own text. `§4.2` and `§4.3` state the two marks over one probe/ folder, and the retired 🧮-proof reading survives only in the Log.
- 🔨 A4.2 · The three ticks EVIDENCE carries are stated with which two revert.
  **Done when:** a reader can name the input whose change reverts `read:` and the one that reverts `accepted:`.
  **Now:** Written in `§4.6`, with the reverting input named for both `read:` and `accepted:`.
- 🔨 A4.3 · What each lane returns is stated side by side.
  **Done when:** the three returns are one block, not three paragraphs in three contracts.
  **Now:** Written in `§4.6` as one block of three returns.
- 🔨 A4.4 · EVIDENCE is readable as two stages, MAKE then BIND, with the boundary to prose visible.
  **Done when:** a reader can say which stage a person's tick belongs to, and why neither stage may write a sentence.
  **Now:** Written in `§4.1` and `§4.6`: the two stages, the ticks living at BIND, and the auditability argument for why neither stage writes a sentence.
- 🔨 A4.5 · A value is addressable on its own, not only through the card that holds it.
  **Done when:** every number in this page's prose carries a `PP<NN>.v<n>`, and no card holds a value no sentence uses.
  **Now:** This round quotes every landed value on the seven cards by id somewhere in Content; the reverse check, a prose number with no id, is the 🔢 tab's to report at CHECK.

### A5 · ✍️ DRAFT ④: turning each point into sentences
- 🔨 A5.1 · DRAFT is defined by the point-to-sentence conversion, not by first creation and not by owning Aims.
  **Done when:** a reader can identify DRAFT in both an empty Page and a mature Page that reopens its promise, and can say what DRAFT kept when the Aims left.
  **Now:** Rewritten 260819. `§5` defines DRAFT by the conversion and by entering on landed evidence; until this round the division sat at `§3` and still drew holes as the normal case.
- 🔨 A5.2 · Every mark in the plan becomes a visible hole in the sentence that will use it, with its card id beside it.
  **Done when:** no landed answer can be written into prose without passing through a hole, and no hole exists that no card serves.
  **Now:** `§5.2` keeps the mark-to-hole rule for the blocked case and names `§14.1` as the page's one worked example; the normal case now writes the landed number directly.
- ⬜ A5.3 · A scaffold reads like a person wrote it, before REVISE touches it.
  **Done when:** `score.py` on a fresh DRAFT output flags no more sentences than it flags on the same page's already-revised prose.
  **Now:** Not measured against revised prose on the same page yet; this round's DRAFT output has not been through the comparison.
- 🔨 A5.4 · A hole in the prose is the EXCEPTION and names the input it is missing.
  **Done when:** no hole on this page lacks a named blocker, and PP05 is the worked example.
  **Now:** The page's one hole sits in `§14.1` and names PP05's two blocking inputs; whether an unnamed hole hides elsewhere is a reader's check at ⑦.

### A6 · 🧵 REVISE ⑤: turning landed evidence into sentences
- 🔨 A6.1 · REVISE is separated from DRAFT by whether purpose and Aims remain fixed.
  **Done when:** the same add, delete, move, or rewrite operation can be classified from its reason.
  **Now:** The fixed-purpose-and-Aims test now lives at QPw5-revise §1, and the shared operation table stays on this page's own `§9`; awaiting human check.
- ✅ A6.2 · COMPILE's fold into REVISE is stated as a measured decision with its open ruling named, not as an inherited silence.
  **Done when:** the division scores COMPILE against §10's four split tests and points at QPw5-revise for the ruling.
  **Now:** Met 260819. `§6.2` scores COMPILE against `§10`'s four split tests, 0 of 4, and names QPw5-revise as the owner of whether the fold is permanent.

### A7 · 🧑 CHECK ⑦: where the current version goes next
- 🔨 A7.1 · CHECK judges one version and routes it to close, REVISE, PROBE, or a new DRAFT.
  **Done when:** every finding names the authority that owns the next change.
  **Now:** The judged outcomes and the no-hidden-revision rule now live at QPw6-check §1-§4, cited from this page's own `§7.1`; awaiting human check.

### A8 · 🔁 Transitions form rounds, not a rigid conveyor belt
- 🔨 A8.1 · Repetition, optional phases, and REVISE to DRAFT are represented without contradiction.
  **Done when:** `DRAFT, DRAFT, PROBE, REVISE, DRAFT` has an unambiguous round interpretation.
  **Now:** Written in `§8.1` with repeated phases, optional PROBE, REVISE to DRAFT as a new round, and the PREPARE loop drawn in the division figure; awaiting human check.

### A9 · 🛠 Operations route by reason, not by edit shape
- 🔨 A9.1 · Common Page edits are examples rather than phase definitions.
  **Done when:** adding, deleting, moving, and rewriting each have both a DRAFT case and a REVISE case.
  **Now:** Written in `§9.1` with paired add, delete, move, and rewrite cases; awaiting human check.

### A10 · 📄 One lifecycle Page holds the phases together
- ✅ A10.1 · Each phase remains a Content division until it becomes an independently closable question.
  **Done when:** the Page names the four split tests and distinguishes phase skills from design Pages.
  **Now:** The four tests stay named in `§10`, now with the record that the 260818 split applied them and overturned this division's original stay-together default; the skill-versus-page distinction stands beside them.

### A11 · 🗂 Page Type and Page Phase are separate skill axes
- ✅ A11.1 · The skill tree keeps persistent Page variation separate from current phase authority.
  **Done when:** Page Types live under `page-types/`, Page Phases live under `page-workflows/`, and the base routes both without introducing an Entry phase or treating RUN as linear ADVANCE.
  **Now:** JL ruled 260804 that `for-*` skills belong under `page-types/` and phase skills use direct names; the folder is `page-workflows/` since 260817 and `§11`'s tree now draws it.

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
  **Now:** Met 260818, and then extended the same day. `QPw00-Display3` was the FIRST unit on this board with a frozen intake, eight inputs with sha256; `QPw00-Display1` (4 inputs) and `QPw00-Display2` (2 inputs) were frozen hours later, and `haipipe-board-approver-agent` recomputed all fourteen digests against disk. `QPf5-Display1` and `QPf5-Display2` remain the only unfrozen units on the board. Extended again 260819: all five `QPw00` units re-froze in the `file:` + `source:` + sha256 shape, `checks/intake.py` recomputes every source hash on demand, and Display3's manifest grew to fifteen inputs when the fourth stored run landed; `QPf5-Display1`, `QPf5-Display2` and `QPf6-Display1` are what remain on the old copy-only shape, five inputs unresolvable.
- ⬜ A14.2 · The TIME column stops being an estimate.
  **Done when:** `_runs/page/` holds at least one receipt for each of OUTLINE, DRAFT, PROBE and EVIDENCE, and the column is rebuilt from their timestamps.
  **Now:** Not met. `_runs/page/` holds 4 runs and 24 receipts (`PP02.v1`, `PP02.v2`), but no receipt carries a start and end pair, so no duration is computable (`PP05.v1` reports 0 phases measured).

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

- `../../../../paper/haipipe-paper/SKILL.md` · the current thin Paper door; it selects typed Pages and delegates their loop to `page-workflows/`
- `../../../../application/2-phase/` · the application family's existing lifecycle model
- `3-QPs-page-structure/QPs1-overall/QPs1-overall.md` · the fixed Page structure paired with this lifecycle
- `../PaperSkillBoard-260725/1-QA-architecture/QA2-ownership-boundary/QA2-ownership-boundary.md` · the current Paper ownership boundary, including parallel PageX and Probe lanes

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
- 🔒 **Round contract**: the purpose, Aims, and promised shape, settled in the approved plan at OUTLINE since 260819, that the rest of one round holds fixed.
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

- 260820 0103 · [REVISE-CC, run `260820-0103-QPw00`] The attribution sweep: `## Content` now states every rule without a person's name or a date code as authority, 7 sentences or headings rewritten under fixed Aims (§1.3's 📌 line, §1.3's phase-versus-step paragraph, §4.4's bibex example, §11.1's heading and P1 sentence, §12.3's heading, §13.1's violation sentence). The history the removed attributions carried, held here: §1.3's step counts are the live run `260805-0216-QB8e`'s, where CHECK occupies steps 1, 3 and 5; the phase-versus-step replacement was raised and answered by JL on 260818 ("for phase, we can do it again and again, right?"); §4.4's live example really carries `verified = {JL 260815}` on the bibex entry itself; §11.1's axis split was settled and option B chosen by JL on 260804; §12.3's per-phase producers landed 260819; §13.1's one real violation sits at run `260818-1543` receipt[2]. Kept, listed rather than edited: §14's two frozen Display3 table cells ("since 260819" in rows 3d and 6), because the table is Display3's transcription source and clearing them is a display redraw, EVIDENCE's pen, not this one's; and §14.1's PP05 hole, still blocked and named. `latex/` and `word/` rebuilt this pass, so both projections match the swept source.
- 260820 0041 · [REVISE-CC, run `260820-0022-QPw00`] The date-code sweep reached the keeps DRAFT's 🕰 pass left behind, under fixed Aims: 15 lines rewritten, 12 bare date codes removed, across the state line, both Diagram captions, and Content (§1.2, §1.3, §2.3, §6.2's stale A7.1 reference, §8.1, §10.1, §11's tree and prose, §12.1, §14's Display3 sentence, §14.1's figure). The history those dates carried lives in this row now: the card-birth question had three answers in three contracts until the 260817 split; JL weighed "step" against "phase" on 260818; three `serves:` addresses went stale on 260819 from editing an approved plan; the six-page split and the §10 re-cut are 260818's; `page-phases/` became `page-workflows/` on 260817; JL chose base-adoption option B on 260804. Kept, each for its named exception: the Opening banner (the creator's revise-opening pen), quoted rulings, run ids, `verified = {JL 260815}`, §14's frozen Display3 table cells (`since 260819` twice, a display-walk redraw), the plan-named headings §5.1, §10.1, §11.1 and §12.3, and §14.1's PP05 hole. `latex/` and `word/` rebuilt this pass, so both projections match the swept source.
- 260820 0022 · [DRAFT-CC, run `260820-0022-QPw00`] The 🕰 present-tense sweep (`haipipe-page-draft` §🕰, 260820) re-realized 15 Content sentences that narrated the past into current-rule statements, none moving an Aim or a landed number: §1.3's folder parenthetical and defined-at-top line, §2.2's Aims-placement and PROBE-order paragraphs, §4.5's display-steps sentence, §5.1's Aims-transcription line, §6.2's seven-phase pair, §10.1's overturn record (folded into the 260818 split sentence, two self-narrating sentences removed), and §14.1's row-3d line. Step 19's producer-owed fix landed with it: the state line's dangling `open: 14` now reads `open Aims: 23 of 31`, counted from this page's own Aims rows (8 ✅, 18 🔨, 3 ⬜, 2 🧠). Out of this sweep's pen: the Opening banner (the creator's revise-opening verb), the Diagram's "Since 260819" line, §14's table cells (Display3's frozen transcription), and the plan-named paragraph titles carrying dates. The outline, probe/, display/ and bibex/ untouched; latex/ and word/ go stale with this edit and their rebuild is owed to ⑤ REVISE.
- 260819 2348 · [REVISE-CC, run `260819-1813-QPw00`] The projections rebuilt and three wording slips fixed under fixed Aims. `latex/` and `word/` regenerated from the DRAFT v3 source, so Display6 and Display7, cited since DRAFT, now embed as real floats with their own captions (clearing 2 `display-cited-not-embedded` ERRORs and the `projection-stale` WARN). Three sentences corrected, none moving an Aim: §2.3 said `approved:` "closes the round" where the page's own §1.3 vocabulary requires "ends the loop" (the round runs on through DRAFT, REVISE and CHECK); §6.1's five-step order still read RENDER where QPw5-revise says CITE since the 260819 display-walk move; the Glossary's Round contract row still said DRAFT hands the promise to the round, which stopped being true when the Aims moved to OUTLINE 260819. §14.1's PP05 hole stays, blocked and named. The outline, probe/, display/ recipes and bibex/ untouched.
- 260819 2330 · [DRAFT-CC, run `260819-1813-QPw00`] Executed outline v3, the first plan approved after the loop's own reorder. Content's phase divisions now run in the LOOP's order: §3 PROBE ② (was §4), §4 EVIDENCE ③ (was §5), §5 DRAFT ④ (was §3), with sub-headings, circled numbers and every in-page §-reference repointed; §2 retitled "the head of a loop that converges" and given §2.3, the PREPARE loop with PP06's counts. Every division realizes its v3 bullets with landed values cited by id: PP01 (§1.2 · §4.2 · §4.3), PP06 (§2.3), PP03 (§4.6), PP02 (§12.2 · §14.1), PP07 (§12.3), PP04 (§13.1), PP05 (§14.1), the bib key luo2026eventglucose (§4.4), and Display1-Display7 cited from §12.2, §12.2, §14 plus §4.5, §1.2, §4.1, §1.2 and §5.2. The one hole is §14.1's and names PP05's two blocking inputs. §8-§11 and §13 compressed to one sub-division each per the plan; §6.4 renumbered §6.2; §10's stay-together text rewritten to record its own 260818 overturn; §11's tree now draws page-workflows/ and the sixteen-type roster; the Diagram redrawn to the PREPARE shape. ## Aims retranscribed from v3: A3/A4/A5 rotated to PROBE/EVIDENCE/DRAFT, five new rows (A2.4, A2.5, A4.4, A4.5, A5.4), the open Decision Now row repointed from A4.2 to A3.2. Two garbled Log references ("§4.4-2.6") repaired to name the material's current home, §3.2, without changing those rows' historical claims. The outline, probe/, display/ and bibex/ untouched; latex/ and word/ stay owed to ⑤ REVISE.
- 260819 2227 · [REVISE-CC, run `260819-1813-QPw00`] Executed CHECK step 14's seven findings, nothing else: the five `## Files` Contracts rows now point at `page-workflows/` (the run contract at its 260815 home, the four phase contracts under the 260817 folder name §1.3 already states), the two dead Engines rows now name the shipped agents `haipipe-page-auditor-agent` and `haipipe-page-creator-agent` with descriptions their own headers support, the literal `%s` in the 260819 Log row's time slot is dropped because no receipt names a time for that pass, the fused 260818 1435 and 260818 1041 Log rows are two source lines again, and the open Decision Now row and A4.2's `Now:` cite §4.4-4.6 instead of the pre-renumber 2.4-2.6. Content order, Aims intent, the outline, probe/, display/ and bibex/ untouched; the rebuild of latex/ and word/ is owed to the builder.
- 260819 · [CC shipped] DRAFT executed `outline-v2`. Content is now the LOOP's order: 15 divisions, four of them new (§1 Overview, §2 OUTLINE ①, §5 EVIDENCE ④, §7 COMPILE ⑥), old §10 folded into §1.2, nothing deleted. 48 section anchors and 16 Aim ids remapped in one pass, with four cross-page references left alone. `## Aims` is TRANSCRIBED from the plan, which is where Aims are settled since JL's 260819 ruling; seven new Aims got their States rows. Two holes are visible and owned: `[Q-loopstate]` in §1.1 and `[Q-evidencerun]` in §5.2.
- 260819 · [JL ruled] the 🧮 proof mark is RETIRED ("我从开始到最后都没有说 proof，我一直说 probe"). It came from one transcribed quote, no Log row ever ruled it, and it was the only mark with no plugin, no folder, no lane, no id and no backlink. 48 marks stripped from 14 plan files; `haipipe-plugin-outline` 0.10.0, `haipipe-page-evidence` 0.8.0 (withdrawing 0.7.3), `haipipe-page-probe` 0.4.2.
- 260819 · [JL ruled] the Aims are settled at OUTLINE, in the plan file, and every owing bullet links to one by id. Before this, a plan that renumbered divisions pointed `A5.1` at the OLD A5.1, and nine of sixteen ids on this page's plan did exactly that.

- 260818 1625 · [REVISE-CC] `§14`'s count was WRONG and `haipipe-board-approver-agent` failed the unit on it. The caption, the README claim, this Log and the `📌` line all said "five of the eleven rows need a person, the other six run machine-only". The drawing shows SEVEN rows carrying a job and FOUR reading `nothing`, and rows 0 and 6 are billed 15 minutes each in the table's own TIME column. The claim also placed the five ticks on FOUR rows, which reproduces the exact miscount the unit's own frozen `haipipe-page-check.SKILL.md:153` corrects. Two more rules failed with it: R14, because row 0 OPEN traced to none of the eight frozen inputs (`haipipe-page.SKILL.md` is now the ninth, and row 0 names its CREATE verb); and R8, because the built page embeds the asset at `width=.85\linewidth`, which printed the 176mm original at 0.733x and delivered 8pt body type to the reader at 5.9pt. The natural width is now 124mm and the same embed prints at 0.9x.

- 260818 · [REVISE-CC, run `260818-1543-QPw00`] Executed outline v1's C1.P1 to C4.P1, plus C2.P2's explicit instruction to leave the QA-probe ownership trio untouched (§2.4-2.6 then, §3.2 now).
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
- 260818 1510 · [OUTLINE-CC, run `260818-1510-QPw00`] RUN from OUTLINE wrote `outline/QPw00-page-loop-outline-v1.md`, the plan to turn Content divisions 1-4 into short hand-off pointers to QPw2-QPw6, keeping the QA-probe ownership trio (§2.4-2.6 then, §3.2 now) in place because no QPw2-QPw6 page yet restates that material. Terminal route HOLD, correctly: `approved:` is a person-only tick and no machine may write it. Receipt at `_runs/page/QPw00/260818-1510-QPw00.json`. The audit surfaced a 13th RUN-contract defect: `page-lifecycle.workflow.js` normalizes the top-level `page` field to board-relative (the 260818 fix logged below) but never touched the echoed `packet.page`, so the auditor's own `packet-run-mismatch` invariant could never pass on a fresh run. Fixed with one line, `parsed.page = page`; `pageflow.py audit` now PASSes this receipt.
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
