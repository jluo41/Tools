# The evidence channel: how a question crosses the wall

state: 🟡 PARTIAL · the crossing and the vocabulary are ruled; which half of the contract this board may rule is not yet checkable
owner: JL
method: one file per question inside the paper, bound BY PATH to an answer the paper may not produce

## Opening

A paper may not run code and may not read the literature, so where does a question live between being raised and being answered?
It lives in a file inside the paper: `1-probes/PP03_results-values/QX1_slug.md` holds it and points by path at the answer.
The answer is written by an executor that never learns which claim it settles, because a clean context IS the wall.
This page rules the paper's half of that crossing, never the model.

**Where this page sits**: `QA1` names `⑤ /haipipe-probe` as one of the shared families the paper calls and owns none of.
This page is the near side of one of them: the file that holds the question, the words it is written in, and the wall it is asked across.
What the LAYER guarantees is the probe board's, at `QB1@probe`, `QB3@probe` and `QB6@probe`.
What the STAGE declares and consumes is `QC4b`; how a landed value renders on a sentence is `QB12b`.

**Why it matters that the stake never crosses**: the bank must not know which answer would be convenient.
Strip the stake and what comes back is evidence; leave it in and what comes back is a request wearing evidence's clothes.
Every number and every citation in the manuscript arrives through this one door, so a claim resting on something nobody can trace back starts here.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never restate the probe-file anatomy**: the four sections, the QA state line and the two LAWS belong to `⑤` and are not this board's to change.
Cite them; a copy here becomes a second authority the day the layer moves.

**Name the four vocabulary words exactly**: Q-consumer, q-executor, a-executor, a-consumer.
They differ by one letter and one hyphen, and a page that blurs them makes the wall unreadable, which is the only thing this page is for.

**Never give an ordinal to a shared family**: this page called `⑤` "the third reusable skill" until `⑨` and `⑪` joined the map and the ordinal became wrong.
Name what it owns instead of where it sits in a list.

## Diagram

**The crossing**: what leaves the paper, what comes back, and what stays behind.

```text
 📄 ⑦ THE PAPER                              🏦 THE BANK, across the wall
 ┌──────────────────────────────┐            ┌────────────────────────┐
 │ 0-lifecycle/…/S-Main-7.md    │            │ examples/Project-*/    │
 │   a sentence owes a number   │            │   tasks/  discoveries/ │
 │   {VAL:? …} [Q-Sec6Results-4]│            │                        │
 │   ## Q-consumer              │            │ owned by /haipipe-task │
 │     🔒 the STAKE lives here  │            │ and /haipipe-discovery │
 │        and never crosses     │            │ neither knows a paper  │
 └────────────┬─────────────────┘            │ exists                 │
              ▼                              │                        │
 ┌──────────────────────────────┐            │ <task-folder>/QA/      │
 │ 1-probes/PP03_results-values/│            │   <n>-<slug>.md        │
 │   QX1_<slug>.md              │            │   state: working |     │
 │   ### q-executor   ━━ STRING ━━━━━━━━━━━▶ │   answered | superseded│
 │   ### q-consumer             │            │                        │
 │   ### bank binding · target: ━━ BY PATH ━▶│   points at that file  │
 │   ### a-executor  ◀━━━━━━━━━━━ the answer │                        │
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
 v0.9.9 · 353 lines           haipipe-paper-probe
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

#### 1.1 · Every phase worker is an adapter onto a model owned elsewhere
(the same relationship the board tool has, stated by the skill in its own words)
`haipipe-paper-probe/SKILL.md` says of itself that the model is not that file's, and that the file is only the paper-side deltas.
`create-page.py` is the same thing onto the board tool's `stage.py`.
The pattern is the shared-family pattern `QA1` rules, and this page is one instance of it.

#### 1.2 · Which half this board may rule is prose, and not yet checkable
(the paper-side deltas, yes; the anatomy and the QA state line, no)
The line is stated above and nothing enforces it, so a page here could specify the anatomy tomorrow and nothing would report the overreach.

#### 1.3 · Nobody has ruled what happens when the layer's contract changes
(two consumer families bind the same folder, and neither owns the migration)
`1-probes/` is bound by the paper family and by `/haipipe-application`.
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

### 3 · Why the probe folder stays outside the paper board

**Page versus file**: the line, and the case it is measured against.

```text
                      🔁 rounds            🔎 probes
 gated by a human?    yes, a round closes  no, the bank answers
 shape                one unit, one page   one TOPIC, many stages
 owned by             this family alone    shared with application
 duplicated ⑧?        queue · register ·   nothing. the lane and the
                      discussion           chip already surface it

 ✅ rounds MOVED onto the board, because a round CAN be a page
 🚫 a probe file cannot: topic-scoped across stages, and its shape is ⑤'s
 ⏳ EXPIRY: if application stops binding 1-probes/, re-open this ruling
```

🚫 Establishes why working state that looks like it belongs on the board does not, and records the condition that would reopen the question.

#### 3.1 · The boundary is page-versus-file, not working-state-versus-output
(probes are working state, and so were rounds, so that axis decides nothing)
Rounds moved into `⑧` because a round can become a page: one round, one gate, one unit.
A probe file cannot, because it is topic-scoped across stages and its four-section shape belongs to `⑤` and is shared.

#### 3.2 · The layer is visible from the board without living in it
(which is the outcome moving it would have been trying to buy)
An S page's Q-consumer names its questions, and the sentence chips on `QB12a` and `QB12b` resolve their states onto the sentences that owe them.
On the MISQ board that is 215 chips over eighteen probe files.

## Aims

### A1 · 🔎 What the layer owns, and what this board owns
- A1.1 · The probe layer is named as a shared family this paper depends on and does not own.
  **Done when:** every page citing the crossing names `⑤` as the owner of the model and the paper side as a delta.
- A1.2 · Which half of the probe contract this board may rule is checkable, not just stated.
  **Done when:** something reports a page here that specifies the probe-file anatomy or the QA state line.
- A1.3 · The migration path is ruled for when the layer's contract changes.
  **Done when:** a named owner exists for migrating a paper when the anatomy moves, and `QA8` records the same answer for the board grammar.

### A2 · 🗣 The vocabulary, and the id that must not collide
- A2.1 · The four names and the prose token are on the board in the layer's own words.
  **Done when:** a reader can follow one question from Q-consumer to a-consumer without opening `⑤`.
- A2.2 · A per-unit stage names its unit in its own consumer id.
  **Done when:** no two consumers share a `Q-<Stage>-<n>` token, and the gate that checks it asserts a non-zero count.

### A3 · 🚫 Why the probe folder stays outside the paper board
- A3.1 · `1-probes/` stays where it is, on the page-versus-file line, with a recorded expiry test.
  **Done when:** the ruling names its expiry condition and something reopens it if `/haipipe-application` stops binding the folder.

### P · 🏁 Page-level
- P1 · No claim on this page about a folder it does not own is left without a check.
  **Done when:** every sentence asserting the state of `⑥` or of `/haipipe-application` names how a reader verifies it.

## States

### A1 · 🔎 What the layer owns, and what this board owns
- ✅ A1.1 · Ruled 260726. It was called "the third reusable skill" until 260802, when `⑨` and `⑪` joined `QA1`'s map and made the ordinal wrong.
- 🔨 A1.2 · Written above as prose. Nothing enforces it, so an overreach would go unreported.
- 🧠 A1.3 · Waiting on a ruling, not on work. Two consumer families bind `1-probes/` and neither owns the migration.

### A2 · 🗣 The vocabulary, and the id that must not collide
- ✅ A2.1 · The four names, the bank binding and the stripped stake are all on the page. They had been live for months and appeared nowhere on this board.
- ✅ A2.2 · Ruled and shipped 260727. Three letters-only id regexes had to move with it, in `dialect_paper.py`, `body.py` and `check-probe-cards.sh`, and none of them failed loudly.

### A3 · 🚫 Why the probe folder stays outside the paper board
- ✅ A3.1 · Ruled 260726 with the expiry test recorded. Eighteen probe files on the MISQ paper bind to ten QA answers across nineteen task groups.

### P · 🏁 Page-level
- 🔨 P1 · One such claim was repaired on 260802: `⑥` had been recorded as a design folder rather than a board since before that board existed, here and on `QA1`. The rule is now in `## Writing Style`; the remaining claims have not been re-read against it.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `../../probe/haipipe-probe/`
  `⑤` itself: the anatomy, the loop, the cost ladder, the QA state-line contract, and the two LAWS. Consulted, never written from here.
- `../../paper/2-phase/1-probe/haipipe-paper-probe/`
  The paper-side deltas, which say so in their own summary.
- `../01-probe-qa-260726/`
  `⑥`, the layer's own board. Read-only from here.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Reports page structure. Nothing checks the seam this page rules, which is why `A1.2` is 🔨.

### 📤 Output files · what a BUILD writes
- `../board/QA/QA5-the-probe-layer.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Law

The probe layer is a reusable family this paper depends on and does not own. The paper side is a delta on a shared model, and this board rules the delta and never the model.

A question crosses the wall as a STRING with its stake stripped, and the answer comes back as a FILE the executor wrote, bound BY PATH. The manuscript never contains the bank's file and the bank never learns the claim, because a clean context IS the wall: strip the stake and the answer is evidence, leave it in and it is a request.

`1-probes/` stays where it is, and the line is PAGE versus FILE rather than working-state versus output. Rounds moved into `⑧` because a round can be a page: one round, one gate, one unit. A probe file cannot, because it is topic-scoped across stages and its four-section shape belongs to `⑤` and is shared with `/haipipe-application`.

The layer is therefore VISIBLE from the board without living in it: an S page's Q-consumer names its questions, and the sentence chips resolve their states.

A Q-consumer id is CONSUMER-LOCAL and must not collide across consumers, so a stage that `runs: per-unit` names its unit in its own token, both halves read off the S page filename. The resolver takes the FURTHEST-ALONG match among entries claiming an id, so a shared id lets a DEFERRED question inherit an ANSWERED one's state. That is a manufactured green on the exact chip a reader trusts.

This ruling carries an expiry test. If `/haipipe-application` stops binding `1-probes/`, re-open it.

## Lesson

A scheme change is never only a rename. The per-unit consumer id needed three letters-only regexes to move with it, in `dialect_paper.py`, `body.py` and `check-probe-cards.sh`, and every one of them silently dropped the new token instead of erroring. Fixing the last also exposed a permanent vacuous green: the gate derived `section-edit` and grepped `q-section-edit`, which matched nothing, so the stage had been passing on an empty set.

An ordinal given to a member of an open set goes wrong when the set grows. This page called the probe layer "the third reusable skill" until two more families joined the map.

## Glossary

- **q-executor**: the question with its stake stripped, which is the only part that crosses the wall.
- **a-consumer**: the paper's interpretation of a landed answer, which is the paper's business and never the bank's.
- **The wall**: the clean context between a paper's claim and the executor's evidence.

## Log

260802 · Migrated to the `QB4` page contract: Writing Style added, Content numbered into three divisions each with a face figure and caption, Aims regrouped as A1-A3 plus P with `Done when`, States mirrored one row per Aim, Files grouped by action.

260802 · Two stale claims cleared: `⑤` was described as the one reusable skill without a board, and as the third of three. Its board `01-probe-qa-260726` has existed since 260726, and `QA1`'s map now carries five shared families.

260727 · JL ruled the per-unit consumer id and it went in the same day. Three id regexes had to move with it and none failed loudly; fixing the last closed a permanent vacuous green on section-edit, which surfaced five PP03 entries whose QA files existed but were never harvested, and two PP05 answers that landed in the bank and were never read back.

260726 · Created on JL's observation that `1-probes/`, the q-executor vocabulary and the bank were nowhere on the board. Ruled that probes do NOT move into `⑧`, with the reason sharpened from purity to page-versus-file, and an expiry test recorded against `/haipipe-application`.
