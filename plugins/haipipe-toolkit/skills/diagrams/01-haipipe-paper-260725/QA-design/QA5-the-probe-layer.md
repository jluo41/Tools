# QA5 · Q-consumers, Q-executors, and the Evidence Channel

state: 🟡 OPEN · S03/S04 placement is implemented; generic Q-consumer ownership is deferred to QB9@boardform
owner: JL
method: one file per question inside the paper, bound BY PATH to an answer the paper may not produce
session: 822af3ea-7685-49dd-9ee0-7d0ee2eea8ec

## Opening

A paper may not run code and may not read the literature, so where does a question live between being raised and being answered?
It lives in a topic-keyed entry inside the paper: `S04-value/probes/V01-headline-lbp/S-Value-6-opioid-cohort-regression-estimates.md` holds one q-executor and points by path at the answer.
The answer is written by an executor that never learns which claim it settles, because a clean context IS the wall.
The paper's half of that crossing is ruled here; the model itself stays the layer's.

**Where this page sits**: `QA1` names `⑤ /haipipe-probe` as one of the shared families the paper calls and owns none of.
This page is the near side of one of them: the file that holds the question, the words it is written in, and the wall it is asked across.
What the LAYER guarantees is stated in `⑤`'s own `SKILL.md`; its board `01-probe-qa-260726` was retired on 260804 with its rulings graduated.
What the STAGE declares and consumes is `QC4b`; how a landed value renders on a sentence is `QBe1 §5`.

**Why it matters that the stake never crosses**: the bank must not know which answer would be convenient.
Strip the stake and what comes back is evidence; leave it in and what comes back is a request wearing evidence's clothes.
Every number and every citation in the manuscript arrives through this one door, so a claim resting on something nobody can trace back starts here.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Keep the ownership split explicit**: the shared Probe layer owns the execution model. This board owns the Paper overlay that locates a topic and requires the four entry sections. The executable version is `haipipe-board/ref/topic-entry-contract.md`; this page explains why it exists.

**Name the four vocabulary words exactly**: Q-consumer, q-executor, a-executor, a-consumer.
They differ by one letter and one hyphen, and a page that blurs them makes the wall unreadable, which is the only thing this page is for.

**Never give an ordinal to a shared family**: this page called `⑤` "the third reusable skill" until `⑨` and `⑪` joined the map and the ordinal became wrong.
Name what it owns instead of where it sits in a list.

## Diagram

**The crossing**: what leaves the paper, what comes back, and what stays behind.

```text
 📄 ⑦ THE PAPER                              🏦 THE BANK, across the wall
 ┌──────────────────────────────┐            ┌────────────────────────┐
 │ 0-lifecycle/S03-literature/  │            │ examples/Project-*/    │
 │  S-Literature-<n>-<topic>.md │            │   tasks/  discoveries/ │
 │   a sentence owes a number   │            │   tasks/  discoveries/ │
 │   {VAL:? …} [Q-Sec6Results-4]│            │                        │
│   ### Q-consumer register    │            │ owned by /haipipe-task │
 │     🔒 the STAKE lives here  │            │ and /haipipe-discovery │
 │        and never crosses     │            │ neither knows a paper  │
 └────────────┬─────────────────┘            │ exists                 │
              ▼                              │                        │
 ┌──────────────────────────────┐            │ <task-folder>/QA/      │
 │ S03-literature/probes/       │            │   <n>-<slug>.md        │
 │   L01-<topic>/<entry>.md     │            │   state: working |     │
│   #### q-executor  ━━ STRING ━━━━━━━━━━━▶ │   answered | superseded│
│   #### consumer trace        │            │                        │
│   #### bank binding · target: ━━ BY PATH ▶│   points at that file  │
│   #### a-executor ◀━━━━━━━━━━━ the answer │                        │
 └──────────────────────────────┘  as a FILE └────────────────────────┘
```

**The four names**: why one question needs four words.

```text
 🎯 Q-consumer   the question WITH its stake: which claim it settles, which
                 sentence owes it. Stays in the stage doc
 ✂️ q-executor   the same question, stake STRIPPED. The only thing that
                 crosses. General language, no claim ids
 📦 a-executor   the answer, copied back into the probe file verbatim
 🧠 a-consumer   the consumer's INTERPRETATION, back in the stage doc.
                 Whether it settles a claim is the paper's business
 🔖 Q-<Stage>-<n>  the citation in the prose that names the question
```

## Content

### 1 · What the layer owns, and what this board owns

**One seam**: the model belongs elsewhere, the deltas belong here.

```text
 🔎 ⑤ /haipipe-probe          📄 ① the paper side
 0.11.3 · 393 lines           the door's probe/ + fn/probes.md
 ─────────────────────────    ──────────────────────────────────
 the probe-file anatomy       which questions THIS paper raises
 the five-step loop           what stake each one carries
 the cost ladder              how a landed answer is interpreted
 the QA state-line contract
 the two LAWS
 the checker's FAIL codes     💬 it says so itself: "only the
 shared by paper AND             paper-side deltas"
 application
```

🔎 Establishes that the paper depends on a contract it does not own, and rules only its own half of it.

#### 1.1 · Every paper-side tool is an adapter onto a model owned elsewhere
(the same relationship the board tool has, stated by the file in its own words)
`haipipe-paper/fn/probes.md` says of itself that the shared crossing model is `probe/haipipe-probe/SKILL.md`'s, and that the file holds only how a paper runs the loop plus the paper-side deltas.
`create-page.py` is the same thing onto the board tool's `stage.py`.
The pattern is the shared-family pattern `QA1` rules, and this page is one instance of it.

#### 1.2 · The Paper overlay is checked without claiming ownership of the shared execution model
(the Board checks location, dependency, headings, state vocabulary, and trace symmetry)
`haipipe-board/cli/check.py` detects a direct `### Q-consumer register`, then checks nested entries against the generic topic-entry contract. It does not judge the executor's evidence or invent a second Probe model.

#### 1.3 · Nobody has ruled what happens when the layer's contract changes
(two consumer families bind the same folder, and neither owns the migration)
`probes/<topic>/` is bound by the paper family and by `/haipipe-application`.
Nothing says who migrates a paper when the anatomy moves, and `QA8`'s equivalent question for the board grammar is open for the same reason.

### 2 · The vocabulary, and the id that must not collide

**One question, four words, one prose token**: what each name carries.

```text
 stage doc   ── Q-consumer ──✂️── q-executor ──▶ 🧱 ──▶ the bank
     ▲                                                     │
     └── a-consumer ◀── interpretation ── a-executor ◀─────┘

 🔖 in the prose: Q-<Stage>-<n>, and for a per-unit stage
    Q-Sec<unit><Slug>-<n>, both halves read off the S page filename
 🚫 an id shared across consumers manufactures FALSE GREENS
```

🗣 Establishes the four names, the prose token, and why a colliding id is a correctness defect rather than a readability one.

#### 2.1 · A consumer id is consumer-local, and section-edit was breaking that
(the layer already stated the invariant; this was the repair of a rule already written down)
`/haipipe-probe` states that a Q-consumer id must not collide across consumers.
Section-edit `runs: per-unit` while spelling one shared `Q-Section-<n>` for all nine units, so the token was doing two jobs.
The fix reads both halves off the S page filename `S-<Family>-<unit>-<slug>.md`, so an id cannot drift from the page that owns it, and `/haipipe-probe` needed no change at all.

#### 2.2 · A shared id does not confuse a reader, it manufactures a green
(the resolver takes the FURTHEST-ALONG match among entries claiming an id)
Measured on the MISQ paper: `Q-Section-1` named three different questions on three pages, so a DEFERRED §7 citation question inherited the state of an ANSWERED §6 results entry.
Six chips on `S-Main-7` read `ok` or `ready` while the page's own records read DEFERRED, and three on `S-Main-4` read `ready` while its records said no live probe owned them.
Renaming both sides moved all nine to `parked` or `unowned` with zero evidence changed.

### 3 · Why live probe entries belong inside their evidence topic

**Topic first, entry second**: the durable paper object and the evidence work it owns.

```text
  S03 Literature                         S04 Value
  ├── S-Literature-<n>-<topic>.md        ├── S-Value-<n>-<topic>.md
  │   └── Aim: Q-consumer + stake         │   └── Aim: Q-consumer + stake
  └── probes/                             └── probes/
      └── L01-<topic>/                        └── V01-<topic>/
          └── one entry per q-executor            └── one entry per q-executor
              discovery binding                     task binding
              a-executor                            a-executor

  queue = entries whose bank-binding state is planned | commissioned | deferred
  _archive/1-probes/ = historical provenance, never a live work queue
```

✅ Establishes that a topic owns the paper-facing reason for an answer and its active evidence entries, while the shared Probe layer still owns the loop and entry anatomy.

#### 3.1 · The topic owns the paper stake; the entry owns the execution payload
(the Q-consumer must stay with the paper, while the q-executor must stay clean)
The topic page sits directly in S03 or S04 and is the canonical home for the Aim and Q-consumer because it explains why the paper needs an answer.
Its keyed entry under `probes/<topic>/` holds one q-executor, its bank binding, and its a-executor because those are the neutral exchange with Discovery or Task; it retains the original Q-consumer text only as a review trace during the page-level normalization.
The generic Probe layer remains the owner of the loop and entry anatomy, so nesting changes the live location without forking the contract.

#### 3.2 · The queue is a view, not another folder
(the bank-binding state is the only live source of backlog)
An entry is queued exactly when its `#### bank binding` names `state: planned`, `commissioned`, or `deferred`; `read` and `answered-local` are resolved states and leave the queue. The topic page's own `state:` records delivery readiness, not queue membership.
No queue file is written by hand, so moving or resolving an entry cannot leave an out-of-date duplicate behind.

## Aims

### A1 · 🔎 What the layer owns, and what this board owns
- A1.1 · The probe layer is named as a shared family this paper depends on and does not own.
  **Done when:** every page citing the crossing names `⑤` as the owner of the model and the paper side as a delta.
- A1.2 · The Paper overlay is checkable without replacing the shared Probe model.
  **Done when:** Board check reports an entry whose topic dependency, anatomy, state, or consumer trace is invalid.
- A1.3 · The migration path is ruled for when the layer's contract changes.
  **Done when:** a named owner exists for migrating a paper when the anatomy moves, and `QA8` records the same answer for the board grammar.

### A2 · 🗣 The vocabulary, and the id that must not collide
- A2.1 · The four names and the prose token are on the board in the layer's own words.
  **Done when:** a reader can follow one question from Q-consumer to a-consumer without opening `⑤`.
- A2.2 · A per-unit stage names its unit in its own consumer id.
  **Done when:** no two consumers share a `Q-<Stage>-<n>` token, and the gate that checks it asserts a non-zero count.

### A3 · 🧭 Why live probe entries belong inside their evidence topic
- A3.1 · Each live Literature or Value entry lives in the `probes/` folder of the topic it serves.
  **Done when:** S03 and S04 contain every live entry beneath its assigned topic, no S11 Probe group remains, and `_archive/1-probes/` is historical provenance only.

### P · 🏁 Page-level
- P1 · No claim on this page about a folder it does not own is left without a check.
  **Done when:** every sentence asserting the state of `⑥` or of `/haipipe-application` names how a reader verifies it.

## States

### A1 · 🔎 What the layer owns, and what this board owns
- ✅ A1.1 · Ruled 260726. It was called "the third reusable skill" until 260802, when `⑨` and `⑪` joined `QA1`'s map and made the ordinal wrong.
- ✅ A1.2 · Shipped 260804. `haipipe-board/cli/check.py` validates the generic topic-entry overlay; the door's `probe/check-probe-cards.sh` validates the Paper runtime form.
- ✅ A1.3 · Ruled and carried out 260803. The Paper board moves live entries beneath S03 and S04 topics; `_archive/1-probes/` keeps the old source paths as provenance.

### A2 · 🗣 The vocabulary, and the id that must not collide
- ✅ A2.1 · The four names, the bank binding and the stripped stake are all on the page. They had been live for months and appeared nowhere on this board.
- ✅ A2.2 · Ruled and shipped 260727. Three letters-only id regexes had to move with it, in `dialect_paper.py`, `body.py` and `check-probe-cards.sh`, and none of them failed loudly.

### A3 · 🧭 Why live probe entries belong inside their evidence topic
- ✅ A3.1 · JL refined and CC applied 260804. S03 and S04 topic pages sit directly in their stage folders; ten discovery entries live in `S03-literature/probes/L01-<topic>/` and eighteen task entries in `S04-value/probes/V01-<topic>/`. Each entry is one q-executor; S11 no longer exists as a live group.

### P · 🏁 Page-level
- 🔨 P1 · One such claim was repaired on 260802: `⑥` had been recorded as a design folder rather than a board since before that board existed, here and on `QA1`. The rule is now in `## Writing Style`; the remaining claims have not been re-read against it.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `../../probe/haipipe-probe/`
  `⑤` itself: the anatomy, the loop, the cost ladder, the QA state-line contract, and the two LAWS. Consulted, never written from here.
- `../../paper/haipipe-paper/probe/`
  The paper-side probe tooling of the one door; `../../paper/haipipe-paper/fn/probes.md` states the deltas-only split in its own words.
- `../../probe/haipipe-probe/SKILL.md`
  Where the layer's guarantees live. Its own board `01-probe-qa-260726` was retired on 260804 with its rulings graduated.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Detects `### Q-consumer register` and validates the generic topic-entry seam: direct topic dependency, headings, state, and trace symmetry.

### 📤 Output files · what a BUILD writes
- `../board/QA/QA5-the-probe-layer.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Law

- The probe layer is a reusable family this paper depends on and does not own. The paper side is a delta on a shared model, and this board rules the delta and never the model.
- A question crosses the wall as a STRING with its stake stripped, and the answer comes back as a FILE the executor wrote, bound BY PATH. The manuscript never contains the bank's file and the bank never learns the claim, because a clean context IS the wall: strip the stake and the answer is evidence, leave it in and it is a request.
- An S03 Literature or S04 Value topic page lives directly in its stage folder. Its `### Q-consumer register` is the canonical paper-facing mapping from Q-consumer to entry. Live entries belong in that stage's `probes/<topic>/` folder. Each entry is one q-executor and holds its bank binding and a-executor; its consumer trace is audit history only.
- `_archive/1-probes/` preserves historical provenance only. It is not a live queue or a location for new probe entries.
- Queue is derived from the `state:` inside each nested entry's bank binding. It is never maintained as a separate file or a third register.
- A Q-consumer id is CONSUMER-LOCAL and must not collide across consumers, so a stage that `runs: per-unit` names its unit in its own token, both halves read off the S page filename. The resolver takes the FURTHEST-ALONG match among entries claiming an id, so a shared id lets a DEFERRED question inherit an ANSWERED one's state. That is a manufactured green on the exact chip a reader trusts.

## Lesson

- A scheme change is never only a rename. The per-unit consumer id needed three letters-only regexes to move with it, in `dialect_paper.py`, `body.py` and `check-probe-cards.sh`, and every one of them silently dropped the new token instead of erroring. Fixing the last also exposed a permanent vacuous green: the gate derived `section-edit` and grepped `q-section-edit`, which matched nothing, so the stage had been passing on an empty set.
- An ordinal given to a member of an open set goes wrong when the set grows. This page called the probe layer "the third reusable skill" until two more families joined the map.

## Glossary

- **q-executor**: the question with its stake stripped, which is the only part that crosses the wall.
- **a-consumer**: the paper's interpretation of a landed answer, which is the paper's business and never the bank's.
- **The wall**: the clean context between a paper's claim and the executor's evidence.

## Discussion

- 🔗 Generic Probe ownership moved to the Boardform lifecycle Page
  The S03/S04 folder layout remains the implemented Paper case.
  Whether filing a Probe Page may transfer Q-consumer ownership is now owned by `QB9@boardform` §2.4 to §2.6, including the one-active-Page handoff boundary and the zero-copy projection question.

- 🧭 Adopted direct-topic probe structure
  JL ruled on 260804 that S03 and S04 topic pages are direct children of their stage folders, while a shared `probes/` child groups their entries by topic.
  The live shape is `S03-literature/S-Literature-<n>-<topic>.md` plus `S03-literature/probes/L01-<topic>/<entry>.md` for discovery, and the parallel S04 Value shape for task evidence.
  The topic is the canonical home for the Q-consumer and paper stake, while each entry is one neutral q-executor with its bank binding and returned a-executor.
  The queue is derived from planned, commissioned, and deferred bank-binding states, so it is never a second hand-maintained file.
  The former `1-probes/` tree is preserved only at `_archive/1-probes/`, and the separate S11 Probe group is gone.

## Log
- 260806 0900 · [REVISE-CC] TWO RULINGS landed and executed. Ruling B (JL: entry is a hidden source file, like a PDF, never on the board): entries demoted from board pages to records named <n>-<slug>.md (digit-first, invisible to the page glob); 28 MISQ entries renamed with pointers repointed, MISQ board 87 to 59 pages, record shape = title + requires + four slots, no page frame. Naming law (JL: call them both QA): one conversation, two QAs, the BANK QA is the original (# Q = q-executor, ## Answer = a-executor) and the PROBE QA is the paper's copy that points at it; QA-executor/QA-consumer retired as file names, consumer/executor words name slots only. Contracts at topic-entry-contract + for-literature/for-value 0.3.0 + page-probe 0.3.3, haipipe-board 0.123.0; 131 tests green.

- 260806 0720 · [REVISE-CC] swept to the thin architecture (one door + stage data + board rental); the paper-side probe adapter is now the door's `probe/` + `fn/probes.md` (the `workers/haipipe-paper-probe` skill dissolved 260805), and the retired probe board's pages are no longer cited as live.

260804 · Moved the generic Q-consumer ownership, one-active-Page handoff, and zero-copy projection discussion to `QB9@boardform`. This Page now keeps only the implemented Paper S03/S04 case and a pointer to the lifecycle owner.

260804 · JL refined the topic-owned structure: S03 and S04 topic pages are direct stage children, and their evidence entries live in `probes/<topic>/`. CC applied it to the Paper board. One entry equals one q-executor; each topic's Q-consumer register is canonical, and queue is derived from bank-binding state.

260802 · Migrated to the `QB4` page contract: Writing Style added, Content numbered into three divisions each with a face figure and caption, Aims regrouped as A1-A3 plus P with `Done when`, States mirrored one row per Aim, Files grouped by action.

260802 · Two stale claims cleared: `⑤` was described as the one reusable skill without a board, and as the third of three. Its board `01-probe-qa-260726` has existed since 260726, and `QA1`'s map now carries five shared families.

260727 · JL ruled the per-unit consumer id and it went in the same day. Three id regexes had to move with it and none failed loudly; fixing the last closed a permanent vacuous green on section-edit, which surfaced five PP03 entries whose QA files existed but were never harvested, and two PP05 answers that landed in the bank and were never read back.

260726 · Created on JL's observation that `1-probes/`, the q-executor vocabulary and the bank were nowhere on the board. Ruled that probes do NOT move into `⑧`, with the reason sharpened from purity to page-versus-file, and an expiry test recorded against `/haipipe-application`.
