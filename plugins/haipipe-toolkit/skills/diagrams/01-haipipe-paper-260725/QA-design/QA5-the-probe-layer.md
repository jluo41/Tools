# ⑤ The EVIDENCE channel: /haipipe-probe
state: 🟡 PARTIAL
owner: JL
method: one file per question inside the paper, bound BY PATH to an answer the paper may not produce

## Opening
A paper may not run code and may not read the literature, so where does a question live between being raised and being answered?
Every number and every citation in the manuscript arrives through one door, and this face is the door's near side: the file that holds the question, the words that describe it, and the wall it is asked across. Get it wrong and a claim ends up resting on something nobody can trace back.

The map has five reusable skills, not two. `①` writes the paper, `③` renders and runs its boards, `⑤ /haipipe-probe` owns the crossing where evidence enters, `⑨` makes the floats, and `⑪` rewrites prose that already exists. It is the same relationship in all five cases: this family depends on a contract it does not own, and rules only its own half. `⑤` and `③` are the two that are CHANNELS, which is a narrower claim than being shared (`QA1`).

That is not a design analogy, it is written in the skill. `haipipe-paper-probe/SKILL.md` says of itself: "THE MODEL IS NOT THIS FILE'S, it is owned by `probe/haipipe-probe/SKILL.md`. This file is only the paper-side deltas." Exactly as `create-page.py` is the paper-side delta on the Board's `stage.py`. Every phase worker in `①` is an adapter onto a shared model, and until now only one of those models was on the map.

Scope: This page covers Where `1-probes/` sits, what one probe file contains, the vocabulary the whole loop is written in, what is on the far side of the wall and who owns it, and why the answer is pointed at rather than copied. Neighbouring pages cover What the LAYER guarantees rather than what a consumer needs from it, its wall, its contract and what a machine enforces, is the probe board, `probe-board/`: the step order is `QB1@probe`, what a MATCH may spend is `QB3@probe`, and where an answer comes to rest is `QB6@probe`. That board restructured twice on 260726, so face-level links here are the ones that resolved at build time and not a stable contract. What the STAGE declares and consumes, its route, its ceiling and when an answer counts as landed, is `QC4b`; what the prose says meanwhile is `QC4a`; how a landed value renders on a sentence is `QB12b`. The probe-file anatomy, the QA state-line contract and the two LAWS belong to `⑤` itself and are not ours to change.

## Diagram
```
   ⑦ THE PAPER                                     THE BANK, across the wall
   ┌──────────────────────────────┐                ┌────────────────────────┐
   │ 0-lifecycle/…/S-Main-7.md    │                │ examples/Project-*/    │
   │   a sentence owes a number   │                │   tasks/       19 grps │
   │   {VAL:? …} [Q-Sec6Results-4]    │                │   discoveries/         │
   │            │                 │                │                        │
   │   ## Q-consumer              │                │  owned by /haipipe-task│
   │     the STAKE lives here     │                │  and /haipipe-discovery│
   │     and never crosses        │                │  neither knows a paper │
   └────────────┼─────────────────┘                │  exists                │
                ▼                                  │                        │
   ┌──────────────────────────────┐                │  <task-folder>/QA/     │
   │ 1-probes/PP03_results-values/│                │    <n>-<slug>.md       │
   │   QX1_<slug>.md              │                │    state: working |    │
   │   ### q-executor  ───────────┼── as a STRING ─┼──▶ answered | superseded│
   │   ### q-consumer             │   in a prompt, │                        │
   │   ### bank binding · target: ─┼── BY PATH ────┼──▶ points at that file │
   │   ### a-executor  ◀──────────┼── the answer   │                        │
   └──────────────────────────────┘   comes back   └────────────────────────┘
                                       as a file
                                       the executor wrote

   ── the four names, and why there are four ─────────────────────────
      Q-consumer   the question WITH its stake: which claim it settles,
                   which sentence owes it. Stays in the stage doc.
      q-executor   the same question with the stake STRIPPED. The only
                   thing that crosses. General language, no claim ids.
      a-executor   the answer, copied back into the probe file verbatim
      a-consumer   the consumer's INTERPRETATION of it, back in the stage
                   doc. Whether it settles a claim is the paper's business
                   and never the probe's.
      Q-<Stage>-<n>  the citation in the prose that names the question

   ── why the stake is stripped ──────────────────────────────────────
      the bank must not know what answer would be convenient. A clean
      context IS the wall. Strip the stake and the answer is evidence;
      leave it in and it is a request.
```

## Content
### `1-probes/` is ours, and its shape is not
The folder lives inside the paper, we write every file in it, and eighteen of them exist on the MISQ paper. But the SHAPE is `⑤`'s: `PPNN_<topic>/QXn_<slug>.md`, with four sections, `### q-executor`, `### q-consumer`, `### bank binding`, `### a-executor`.

Two consequences follow, and both bind.

It is TOPIC-scoped and cross-stage. The folder skill states it: "one cross-stage pool, one file per TOPIC". A probe topic is not owned by one S page, which is exactly why it cannot become one.

It is SHARED with `/haipipe-application`, which uses the identical `1-probes/PPNN_<topic>/` path for interventions. The location is part of a contract two consumer families depend on, so this board may rule what a paper puts in a probe file and may not rule where the folder is.

### The answer is pointed at, never copied
The `bank binding` section names a `target:` path. The manuscript never contains the bank's file, and the bank never contains the paper's claim. That is what makes a number auditable a year later: the sentence names a question, the question names a QA file, and the QA file names the run.

### Why it does not move into `⑧`
Rounds moved onto the board and probes should not, and the three reasons are the exact inverse of that case.

```
                        rounds                     probes
 gated by a human?      yes, a round closes        no, the bank answers
 shape                  one unit, one page         one TOPIC, many stages
 owned by               this family alone          shared with application
 duplicated the board?  queue, register,           nothing. The lane and
                        discussion, a stored       the chip already surface
                        latest.md pointer          it on the sentence
```
Moving it would break a path two families bind to, force a cross-stage topic into a single-unit page, and gain nothing, because `QB12a` and `QB12b`'s chips already resolve a probe's state onto the sentence that owes it: 215 of them on the MISQ board.

### What `⑤` owns, and what we own
```
 ⑤ /haipipe-probe    the probe-file anatomy · the five-step loop ·
   v0.9.9 · 353 ln   the cost ladder · the QA state-line contract ·
                     the two LAWS · the checker's FAIL codes
                     shared by paper AND application

 ① the paper side    haipipe-paper-probe, which says of itself that it
                     is "only the paper-side deltas"
                     which questions this paper raises, what stake they
                     carry, and how a landed answer is interpreted
```

## Aims
- [x] 🧭 Name the probe layer as a reusable skill in its own right
      `①` writes, `③` renders and runs, `⑤` owns the crossing. Each phase worker is a paper-side delta on a model owned elsewhere (JL 260726). It was called the THIRD until 260802, when `⑨` and `⑪` joined the map and made the ordinal meaningless.
- [x] 🗣 Put the vocabulary on the board
      Q-consumer, q-executor, a-executor, a-consumer, bank binding, `Q-<Stage>-<n>`, and why the stake is stripped.
- [x] 🚫 Rule that `1-probes/` does not move into `⑧`, WITH an expiry test
      The boundary is page-versus-file, not working-state-versus-output: probes ARE working state, and they stay outside because a probe file cannot BECOME a page. Its four-section shape is `⑤`'s and is shared with `/haipipe-application`.
      EXPIRY: if `/haipipe-application` ever stops binding `1-probes/`, the shared-contract half of this ruling dies and only the weaker page-versus-file argument remains. Re-open it then rather than treating this as permanent (JL 260726).
      Topic-scoped, ungated, and shared with `/haipipe-application`; the inverse of the round case on all three counts.
- [x] 🔑 A per-unit stage's consumer id carries the unit (JL 260727)
      `/haipipe-probe` already states the invariant: a Q-consumer id is CONSUMER-LOCAL and
      "the ids never collide across consumers"; section-edit was breaking it, because it
      `runs: per-unit` while spelling one shared `Q-Section-<n>` for all nine units. So this is
      not a new rule; it is the repair of one already written down. The token is
      `Q-Sec<unit><Slug>-<n>`, both halves read off the S page filename
      `S-<Family>-<unit>-<slug>.md`, so an id cannot drift from the page that owns it.
      No change to `/haipipe-probe`: `Q-<Stage>-<n>` was always right, and the per-unit stage
      is what the `<Stage>` resolves to.
      MEASURED on the MISQ paper, and this is why it mattered: `Q-Section-1` named three
      different questions on three pages, and the resolver takes the FURTHEST-ALONG match, so
      a DEFERRED §7 citation question inherited the state of an ANSWERED §6 results entry.
      Six chips on `S-Main-7` read `ok`/`ready` while the page's own records read DEFERRED, and
      three on `S-Main-4` read `ready` while its records said no live probe owns them. Renaming
      both sides moved all nine to `parked`/`unowned`, with zero evidence changed. A shared
      consumer id does not merely confuse a reader; it manufactures false greens.
- [ ] 📐 State which half of the probe contract this board may rule
      The paper-side deltas, yes; the anatomy and the QA state line, no. Written above as prose and not yet checkable.
- [ ] 🧠 Rule what happens when `⑤`'s contract changes
      Two consumer families depend on `1-probes/`. Nothing says who migrates a paper when the anatomy moves, and `QA8`'s equivalent question for the Board grammar is open for the same reason.
- [x] 📚 `⑤` has a board, and this item was stale
      It said `⑤`'s rationale lived at `diagram/260714-probe-qa/`, a design folder rather than a board. `diagrams/01-probe-qa-260726/` has been a real board since 260726 and this page went on recording the gap as open (cleared 260802, with the same claim on `QA1`).

## States
The layer is implemented, in daily use, and now on the map. Eighteen probe files on the MISQ paper bind to ten QA answers across nineteen task groups, and the chips on `QB12a` and `QB12b` resolve their states onto the sentences that owe them.

What is new here is placement, not mechanism: the vocabulary and the wall were live for months and appeared nowhere on this board, so a reader could see `QC4b`'s five steps without ever learning what a q-executor is or why the stake is stripped.

## Files
- `probe/haipipe-probe/`
  `⑤` itself: the anatomy, the loop, the ladder, the QA contract, the two LAWS.
- `2-phase/1-probe/haipipe-paper-probe/`
  The paper-side deltas, which say so in their own summary.
- `1-probes/`
  Eighteen live probe files on the MISQ paper.
- `diagrams/01-probe-qa-260726/`
  `⑥`, `⑤`'s own board. Read-only from here.

## Law
The probe layer is the third reusable skill this family depends on and does not own. `①` writes the paper, `③` renders and runs its boards, `⑤` owns the crossing where evidence enters. In every case the paper side is a delta on a shared model, and this board rules the delta and never the model.

A question crosses the wall as a STRING with its stake stripped, and the answer comes back as a FILE the executor wrote, bound BY PATH. The manuscript never contains the bank's file and the bank never learns the claim, because a clean context IS the wall: strip the stake and the answer is evidence, leave it in and it is a request.

`1-probes/` stays where it is, and the line is PAGE versus FILE, not working-state versus output. Probes are working state; so were rounds. Rounds moved into `⑧` because a round can be a page: one round, one gate, one unit. A probe file cannot, because it is topic-scoped across stages and its four-section shape belongs to `⑤` and is shared with `/haipipe-application`.

The probe layer is therefore VISIBLE from the board without living in it: an S page's Q-consumer names its questions, and the sentence chips resolve their states. That is the outcome moving it would have been trying to buy.

A Q-consumer id is CONSUMER-LOCAL and MUST NOT collide across consumers, so a stage that `runs: per-unit` names its unit in its own token: `Q-Sec<unit><Slug>-<n>`, both halves read off the S page filename.
`/haipipe-probe`'s `Q-<Stage>-<n>` is unchanged; the per-unit stage is what `<Stage>` resolves to.
This is not a cosmetic id rule, because the resolver takes the FURTHEST-ALONG match among the entries claiming an id: a shared id lets a DEFERRED question inherit an ANSWERED one's state, which is a manufactured green on the exact chip a reader trusts.

This ruling carries an expiry test. If `/haipipe-application` stops binding `1-probes/`, re-open it.

## Log
260726 · Created on JL's observation that `1-probes/`, the q-executor vocabulary and the bank were nowhere on the board. Ruled that probes do NOT move into `⑧`, with the reason sharpened from purity to page-versus-file, and an expiry test recorded against `/haipipe-application`.
260727 · JL ruled the per-unit consumer id (`Q-Sec0Abstract-<n>`, `Q-Sec6Results-<n>`) and it
  went in the same day. Three things had to move that the ruling itself does not mention, and
  each was a letters-only id regex that silently dropped the new token rather than erroring:
  `dialect_paper.py` (2 sites), `body.py` (4 sites) and `check-probe-cards.sh` (8 sites). The
  last one bit during the work: after the rename the shell gate reported ten `cite-unowned` /
  `value-unowned` defects on pages whose brackets were sitting right there in the prose. A
  scheme change is therefore never only a rename; it is a rename plus every regex that ever
  hard-coded the old shape, and none of them fail loudly.
  Fixing that gate also closed `_TODO` E2: `stage_stem()` derived `section-edit` and grepped
  `q-section-edit`, which matched nothing, so section-edit had a permanent vacuous green. It
  now maps to `Sec` and the gate asserts 12 probe entries and 16 stage pages, surfacing five
  PP03 entries whose QA files exist but were never harvested into `### a-executor`, and two
  PP05 answers that landed in the bank and were never read back. That work was always owed and
  nothing could see it.
260802 · Two stale claims cleared: `⑤` was described as the one reusable skill without a board, and as the third of three. Its board `01-probe-qa-260726` has existed since 260726, and the map now carries five shared families.
