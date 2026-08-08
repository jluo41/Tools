# QBt11 · page-type LABELING · one corpus and one target, walked from step 1 to step 5 on one page

state: 🟡 PARTIAL · step ① has run and step ② is now the live one; the embedding unit inside ① is still on HOLD, and every label on this page is still a proposal
page-type: labeling
owner: JL
method: make the five doors of the labeling lifecycle the page's own divisions, so a person can see which step is live and which are locked
session: 4087376d-7520-493a-a30f-c0a660c2e3bd

## Opening

How does one person take one corpus and one label target from nothing to a finished set, on a single page?
A label target is the one thing being judged, and no corpus arrives carrying it.
The method is settled, so that is not the difficulty.
The difficulty is that a person opening the page cannot see where to start.
So this specimen makes the lifecycle's five doors its own Content divisions.

**What is refused, and why**: each division states its own precondition, so a step that cannot run says what is missing instead of simply failing.

✅ **Unlike its sibling specimens, this page fabricates nothing.** The corpus is real and measured, the seal is a real split, and the quoted turns are verbatim. What is honestly absent is any result, because step ② has not run and nobody has given a label.

**What this page teaches**: that a typed page can be a STEPPER. Every other specimen here organizes Content by subject; this one organizes it by the order a person does things, and each division reports whether it is locked, ready, resumable, waiting on a person, done, or held.

**Where the steps come from**: the `subjective-label` plugin's board, `../../../../subjective-label/diagram/02-subjective-label-260722`. Its `QF1` names five doors and fixes the dispatch as state read, precondition check, one phase, authorized write, next state. This page invents no step and reorders none.

**Covered elsewhere**: `QB4` owns what any page is. The variant contract is `haipipe-board-page-for-labeling`, (now in the `subjective-label` plugin's own `skills/`, because that plugin maintains it) whose `template.md` is the copy-and-fill specimen; this page is the worked one. `QBt3` is the display specimen, which is the opposite shape: it IS its atom, while this page is a process over one.

## Diagram

**Five doors, one live**: the lifecycle from `QF1 §1`, with this run's real position marked.

```text
  ①  init        🟡 PART    corpus ✅ · seal ✅ · B_1 ✅ · embeddings ⛔ HOLD
      │                     ran 260808 · runs/acibench-authority/
      ▼                     the HOLD blocks step ② from round 2, not round 1
  ②  round       🟢 ready   C_t → P_t → B_t → Session → Checkpoint
      │                     round 1 is B_t → Session → Checkpoint only
      ▼                     safe next action: the round-1 Human-AI Session
  ③  gates       🔒 locked  quality · stability · coverage · risk
      │                     a human signoff, never auto-closed (QF1 §3.1)
      ▼
  ④  evaluate    🔒 locked  freeze G* → blind T* gold → executor scorecards
      │                     requires a QD4 stop AND a frozen G*
      ▼
  ⑤  complete    🔒 locked  production → risk queue → final audit

  ─────────────────────────────────────────────────────────────────────
  🗄 the corpus behind it, measured 260807, nothing fabricated
     ACI-Bench · 207 encounters · 5,896 doctor turns · median 17 words
     development pool 4,683        🔒 sealed 1,213, split == test3, unread
     sha256 cb30a6140b95b1fe  ← the corpus checksum QF2 §1 asks for
```

## Content

### 1 · Step ① init

**🟡 PART**: four of the five units ran on 260808; the fifth is a capability that has not shipped, and `QF1 §3.2` says to say so rather than fabricate it.

```text
needs      a corpus that resolves, and a human authority named
produces   project dir · config.yaml · corpus manifest · .state.json
           · the seal reserved BEFORE any embedding
           · the random round 1 batch
state      🟡 PART · runs/acibench-authority/ exists
ran        corpus validated · seal reserved · dev table built · B_1 frozen
missing    embeddings · torch, sentence-transformers, faiss are not installed
next       the round-1 Human-AI Session, which needs no index
```

#### 1.1 · What ran, and what the HOLD does not excuse
(Separates the four units that produced files from the one that produced a refusal.)
The corpus was validated at 5,896 turns with unique ids and no empty text, sha256 `cb30a6140b95b1fe`, and 4,683 of them are eligible.
The seal was reserved first: 1,213 ids written to `test/sealed/manifest.protected.jsonl` at mode `400` inside a `700` directory, with an access log opened, and the development table then built with every sealed row carrying `text: null`.
`B_1` is 60 items drawn by `random.Random(42)` from the eligible pool at inclusion probability `0.012812`, containing no sealed row and none of the five seed cases.
What refused is `--embed bge-m3`: the environment has none of `torch`, `sentence_transformers`, or `faiss`, so `cache/embeddings/` holds a `HOLD.md` and no vector, and the honest consequence is that round 2 cannot start rather than that round 1 cannot.

#### 1.2 · Why the seal is reserved before embedding and not after
(The one ordering inside step ① that cannot be recovered from later.)
`QC1 §3.2` and the embedder's own contract both exclude sealed ids from development embedding, indexing, deduplication and retrieval.
Embedding the whole corpus first and filtering afterwards leaves the sealed items inside the index, where retrieval will surface them into a candidate pool with nothing raising an error.
Because the exclusion is a field test, `split != test3`, a manifest can be checked for leakage after the fact; a promise could not be.

### 2 · Step ② round

**🟢 ready**: this is the only step a person actually works inside, and it is resumable across all four of its phases.

```text
needs      step ① done, and a closed policy for round 2 onward
produces   the policy G_t, the human gold, and one checkpoint
state      🟢 ready for round 1 · 🔒 locked for round 2 by the embedding HOLD
```

```text
  2.1 candidate   C_t   round 1 skips this: QB1 requires a random draw
  2.2 prelabel    P_t   round 1 skips this: there is no policy to pre-label with
  2.3 session     B_t   ← THE ONLY THING THE PERSON DOES · 60 items, frozen, waiting
  2.4 checkpoint        closes G_t and makes it available to the next round
```

#### 2.1 · Round 1 is two phases, not four
(Why the first round is cheaper than every later one, and why it must be.)
`QB1` requires round 1 to be a random draw, so no candidate pool is generated and no embedding is needed to start.
There is also no closed policy, so there is nothing for a weak executor to pre-label and nothing to seal.
Round 1 is therefore a session and a checkpoint, which is the whole reason the embedding HOLD does not block starting work.
Later rounds run all four phases, and only then does step ① need to have produced an index.
This stopped being a hypothetical on 260808: the embedding unit refused, round 1 was frozen anyway, and the claim that the first round is cheap enough to start without an index is now a thing that happened rather than a thing the page asserts.

#### 2.2 · What the person does, and what nothing else may do
(`QF1 §3.1`: semantic acceptance cannot be auto-closed by the router.)
In the session the person is shown items one at a time and gives a class, a region, an uncertainty and a reason.
A machine may show, order, and record; it may not decide, and a proposed class is never gold until the session confirms it.
The reasons are what become boundary rules, so a session that collects classes and discards reasons has produced labels and no policy.

#### 2.3 · The ledger, and why a round is never a division
(The rule the whole page type exists for.)
Rounds are strictly ordered, so round 4 cannot be approved while round 3 is refused, and they fail the per-unit test that decides what earns a page or a heading.
Each closed round therefore adds a four-line record here, newest first, and moves no heading:

```text
📌 0 rounds closed · 0 items in cumulative gold · no policy is open

(this is where the first record lands)
**Round 1** · closed <date> · no prior policy · 60 items
  🎯 challenge  not applicable, there was no policy to challenge
  📊 audit      not applicable, there were no predictions to audit
  📜 diff       first guideline written
  🗺 coverage   which of the seven regions were seen at all
```

#### 2.4 · The policy is this step's real product
(What a reader most wants from the page, and where it lives.)
Once round 1 closes, the classes and boundary rules for the target belong here, in the words the person used.
Until then the honest content is the proposal below, which no round has confirmed.

```text
📜 G_0 · PROPOSED, not closed · target: authority appeal
   🟢 HIGH   the turn offers the speaker's own standing as the reason to accept
   🔵 LOW    adjacent but not it: an instruction, or a reason that is not standing
   ⚪ NONE   the turn does no persuasive work at all
```

Real turns, verbatim, proposed by CC and confirmed by nobody:

```text
H   D2N023  "the biggest issue I'VE SEEN ... your peaks are getting greater than 1,500"
HL  D2N069  "after MY EXAM ... on the x-ray and your exam ... MY RECOMMENDATION would be"
L   D2N006  "i want you to continue on the omeprazole , 40 milligrams , once a day"
N   D2N001  "hi , martha . how are you ?"
```

`D2N069` is the one a person has to rule, and both readings are defensible, which is what makes it an HL item rather than a hard one.

### 3 · Step ③ gates

**🔒 locked by ②**: four conditions, all conjunctive, and the signoff is a person's.

```text
needs      at least two closed checkpoints
produces   a stop-or-continue decision, and the freeze authorization
state      🔒 locked · no round has closed

📊 quality     comparable audit stratum clears its floor        ⬜
📉 stability   two consecutive checkpoints hold that floor      ⬜
🗺 coverage    every thin region carries a disposition          ⬜
🚨 risk        the routed fraction is small enough to work      ⬜
```

#### 3.1 · Why this is a step and not a readout
(A gate that only displays numbers would let the page freeze itself.)
`QD4` makes the four conditions conjunctive and gives the signoff to a person, so the step's product is a decision rather than a measurement.
The stability gate is the one that usually blocks, because a single good round proves nothing and a second is the only thing that can tell a level from a lucky batch.
The coverage gate is the one that waits on a person, because narrowing a target is a semantic act no default may take.

### 4 · Step ④ evaluate

**🔒 locked by ③**: the seal opens here and nowhere earlier.

```text
needs      a QD4 stop AND a frozen G*
produces   late human gold on T*, and one scorecard per candidate executor
state      🔒 locked · nothing is frozen

🔒 G*   not frozen
🧪 T*   split == test3 · 1,213 turns · sealed and unread
📊 S*   no executor scored
```

#### 4.1 · An empty division is a status
(Deleting it would lose the only true thing it has to report.)
Every row above says what has not happened, and a missing heading could not say that.
When the gates pass, these three rows are replaced by the frozen version id, the labeled test, and one row per scored executor.

### 5 · Step ⑤ complete

**🔒 locked by ④**: the last door, and the only one that touches the whole corpus.

```text
needs      an eligible production policy and a selected executor
produces   D* · the risk queue · the final audit
state      🔒 locked · no policy is eligible

📦 D*            ⬜  4,683 development turns wait
🚨 risk queue    ⬜
🎲 final audit   ⬜
```

### 6 · The specimen's own test

**Does the shape work**: the one thing this page cannot answer about itself.

```text
🪜 does a cold reader name the next action unprompted?   🧠 only JL can say
⛔ does any step render as done that has not run?         ✅ no
```

#### 6.1 · Why a specimen must be judged by someone who did not write it
(The author knows the order already, so the author cannot test the order.)
The claim this page makes is that a stepper Content lets a person see where to start.
The author of a stepper always knows where to start, so reading it back proves nothing.
The test is a person new to the project opening the page and naming the next action without being told, which is `A6.1` and is why it waits on JL rather than on work.

## Aims

### A1 · 🧾 Step ① init
- A1.1 · The project exists and the seal is reserved before anything is embedded.
  **Done when:** a project dir resolves, and its manifest shows the sealed ids excluded from every development index.

### A2 · 🔁 Step ② round
- A2.1 · Round 1 runs without an index, as a session and a checkpoint only.
  **Done when:** round 1's checkpoint closes and G_1 exists.
- A2.2 · The policy is executable, and every rule names the round that produced it.
  **Done when:** a weak executor applies G_t to unseen turns with no clarification asked.

### A3 · 🛑 Step ③ gates
- A3.1 · The four gates carry a reading, and the signoff is a person's.
  **Done when:** all four clear their floors and a person authorizes the freeze.

### A4 · 🔒 Step ④ evaluate
- A4.1 · The seal survives to the freeze.
  **Done when:** no manifest in any round contains a `split == test3` row.
- A4.2 · Every candidate executor is scored under one protocol.
  **Done when:** T* carries human gold and each executor has a scorecard.

### A5 · 🏭 Step ⑤ complete
- A5.1 · The corpus is complete with provenance, and the audit says what is reliable.
  **Done when:** one reconciled record per turn, and a final audit written up.

### A6 · 🪞 The specimen's own test
- A6.1 · A reader can tell which step is live without being told.
  **Done when:** a person new to the project opens this page and names the next action unprompted.
- A6.2 · No step renders as done that has not run.
  **Done when:** the HOLD at `§1` stays visible until a project dir exists.

## States

### A1 · 🧾 Step ① init
- 🟡 A1.1 · Half met, 260808. The project dir resolves at `_WorkSpace/InLabStore/runs/acibench-authority/`, and the seal was reserved before the development table was built, which is the ordering the Aim is really about. The other half cannot be met yet: the Aim asks that sealed ids be excluded from every development index, and no index exists, because the embedding unit is on HOLD.

### A2 · 🔁 Step ② round
- ⬜ A2.1 · Not started, but no longer locked. `B_1` is frozen at 60 items and the session is the next action. This is the Aim the embedding HOLD was predicted not to block, and it did not.
- ⬜ A2.2 · Not started, locked by A2.1.

### A3 · 🛑 Step ③ gates
- ⬜ A3.1 · Not started. No round has closed.

### A4 · 🔒 Step ④ evaluate
- ✅ A4.1 · Met and holding. `test3` has never been read. This Aim is met on day one and every later step must keep it met, which is the only Aim here that can be lost rather than gained.
- ⬜ A4.2 · Not started. Nothing is frozen.

### A5 · 🏭 Step ⑤ complete
- ⬜ A5.1 · Not started.

### A6 · 🪞 The specimen's own test
- 🧠 A6.1 · Waiting on JL. The stepper shape is what this page is for, and only a cold reader can say whether it works.
- ✅ A6.2 · Met and tested, 260808. `§1` moved from ⛔ HOLD to 🟡 PART because four of its units genuinely ran, and it kept the embedding HOLD visible rather than rounding the step up to done. `§3` through `§5` still render 🔒 and no gate carries a reading.

### Decision Now

🗣 **Should a labeling page's Content divisions be the five lifecycle STEPS, as this page does, or subjects as `template.md` currently does?**
📍 Part: the whole of `## Content`
🔔 Why now: `template.md` and this page now disagree, and every new run page copies one of them
- ⭐ **Steps.** A person opening the page sees where to start and what is refused. It costs the subject reading, so "what does this target mean" moves inside step ②.
- Subjects. A reader scanning for the current policy finds it at the top, but nobody can tell what to do next, which is the complaint that produced this page.
🛑 Blocks: updating `template.md`, and the two live run pages on the `label-runs` board
🤖 If nobody answers: the two shapes stay in disagreement, which is worse than either

## Files

**This specimen's corpus**, real and measured on 260807:

```text
_WorkSpace/InLabStore/runs/acibench-authority/items.jsonl
  5,896 items · 1.9 MB · sha256 cb30a6140b95b1fe
  fields: item_id · source_id · split · text · context_prev · n_words
```

**The project step ① built around it**, 260808, in the same folder:

```text
config.yaml · .state.json · REPORT.md
corpus/manifest.json · corpus/items.jsonl   sha256 05ce4a7559931362, sealed text withheld
test/sealed/  700       manifest.protected.jsonl 400 · status.json · access_log.jsonl
rounds/round_01/        manifest.yaml · human_batch.jsonl sha256 afac61430b2162da
cache/embeddings/       HOLD.md, and nothing else
policy/ gold/ evaluation/ production/ audit/   empty scaffolds
```

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QB4 page](QB-delivery/QB4-overall.md)
  QB4 owns the section grammar every typed page obeys, including this one.
- `reads · ALL` · [QBt3 page](QBt-page-types/QBt3-for-display.md)
  QBt3 is the opposite shape: it IS its atom, while this page is a process over one.

## Law

- 🪜 **A typed page may be a STEPPER.** Where a lifecycle has ordered doors with preconditions, the Content divisions may be those doors instead of subjects, and each division reports its own step state.
- ⛔ **A missing capability renders as HOLD, never as not-started.** HOLD names what is missing and the safe next action. Not-started says a person has not got to it, which is a different and usually false claim.
- 🔓 **One live step.** Exactly one division is actionable; the rest are locked by a stated precondition, so nothing on the page invites work that would be refused.
- 🔒 **An Aim that is met on day one and can only be lost gets said so.** The seal is the only one here, and a page that lists it beside Aims that are gained reads as though it were progress.

## Log

260807 · Written as the labeling page type's worked specimen. Took `QBt11` rather than the free QBt7, because whether the QBt7 and QBt8 gap is filled is an open Decision Now row on `QB6`, and taking a number would settle it silently.
260807 · Corpus measured and flattened before writing, so no count on this page is estimated. Step ① is genuinely on HOLD; nothing here is fabricated to make the shape look finished.
260808 · `/sl-init` ran. Four units of step ① produced files, the fifth refused: `--embed bge-m3` found no `torch`, `sentence_transformers`, or `faiss`, so `cache/embeddings/` holds a HOLD and no vector. The seal was reserved before the development table was built, and `test3` was found not to straddle an encounter, so no development turn shares an encounter with a sealed one. `B_1` is 60 items, `random.Random(42)`, p = 0.012812, no sealed row and no seed case. Step ① moved ⛔ → 🟡 and step ② moved 🔒 → 🟢; no gate, policy, or label moved at all.
260808 · Two facts this page states were checked against the corpus and one neighbouring page was found wrong: the seed case quoted at `§2.4` as `D2N023` is `D2N023#t65`, while `S-Label-1`'s Stage Contract JSON gives its id as `D2N023#t31`, which is a different turn reading only "right .". That page owns the defect; this one records that it was found.
