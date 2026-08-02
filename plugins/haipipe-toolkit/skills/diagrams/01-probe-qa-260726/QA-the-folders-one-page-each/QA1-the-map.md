# Six folders ship it, three shapes hold it

state: 🟡 PARTIAL
owner: JL
method: count every folder that holds probe material, say which of them this board rules, and name what deliberately gets no page

## Opening
Where does a probe rule, file, or page belong, and how many folders is this layer actually spread across?
Six, plus three file shapes that live inside every project, and this board rules the wall between them and nothing else.
Counting them is the point: the layer reads as one shared skill, and it is not one folder.

The parts that ship and the part that enforces are in different places, which is what makes the count worth stating.
A shared model in `probe/` defines the vocabulary and holds a test fixture, while the only machine that enforces any of it sits forked in two consumer families, 1096 lines against 679.
A reader who assumes the shared folder is the layer will look for the checker there and not find it, and a reader who patches one fork has changed the rule for one consumer.

**Covered elsewhere**: Each folder itself: `QA2` through `QA8` take one each, in the order numbered here. The loop's steps are `QB1` through `QB7`, one page each; the contract is the `QC` group. What a consumer may ask and spend is `QB9@paper`; how a landed answer becomes prose is `QC1@paper`.

## Diagram
```
   ── the flow, once ────────────────────────────────────────────────
   ⑦ THE CONSUMER            ⑧ THE WALL              ⑨ THE BANK
     stage doc                 1-probes/PPnn_<topic>/  tasks/… discoveries/…
     Q-consumer (STAKE)          QXn_<slug>.md           QA/<n>-<slug>.md
     A-consumer                    q-executor ────────▶  written for its
                                   bank binding          OWN reasons
                                   a-executor ◀────────  bound BY PATH

   THIS BOARD rules ⑧ and both of its edges. The stake stops at ⑦.

   ── the six folders that ship it ──────────────────────────────────
   ┌────────────┬───────────────────────────┬────────────────────────┐
   │ THE SHARED │ ① probe/haipipe-probe/    │ ⑤ diagrams/01-probe-   │
   │   MODEL    │    v0.9.9                 │    qa-260726/          │
   │            │    SKILL.md      353      │    13 faces            │
   │  defines   │    ref/template  143      │    WHAT IS ARGUED      │
   │  the words │    test/ ─ a fixture for  │    ← you are here      │
   │            │      a checker it does    │                        │
   │            │      NOT contain          │ ⑥ diagram/260714-      │
   │            │ ② probe/agents/   v1.1.0  │    probe-qa/           │
   │            │    one q-executor agent   │    5 .txt · R1-R18     │
   │            │    93 lines               │    STILL the cited     │
   │            │                           │    SPEC OF RECORD      │
   ├────────────┼───────────────────────────┴────────────────────────┤
   │  THE TWO   │ ③ paper/2-phase/1-probe/haipipe-paper-probe/       │
   │  ADAPTERS  │    v0.6.1 · SKILL 219 · check-probe-cards.sh 1096  │
   │            │ ④ application/2-phase/1-probe/haipipe-application- │
   │  where the │    probe/                                          │
   │  ENFORCING │    v0.3.2 · SKILL 174 · check-probe-cards.sh  679  │
   │  code IS   │                                                    │
   │            │    ③ and ④ diverge by 600 diff lines and are kept  │
   │            │    in step BY HAND. ③ declares itself the source.  │
   └────────────┴────────────────────────────────────────────────────┘

   ── the three shapes, inside every project ────────────────────────
   ⑦ <consumer>/0-lifecycle/<stage>/<stage>.md   the stake lives here
   ⑧ <consumer>/1-probes/PPnn_<topic>/QXn_*.md   MISQ: 5 topics · 17
   ⑨ tasks/<T>/QA/ · discoveries/<G>/<F>/QA/     MISQ: 7 + 3 = 10

   ── the crossings ─────────────────────────────────────────────────
   ⒜ ① ──constitutes──▶ ③ AND ④
        both adapters name ① their constitution. A rule landed on one
        adapter and not the other is a defect, and nothing detects it.

   ⒝ ⑤ ──graduates──▶ ① ③ ④
        a ✅ ruling's Law is COPIED into the owning skill. Zero of the
        thirteen faces here have graduated yet.

   ⒞ ⑦ ──strips the stake──▶ ⑧ ──▶ ② ──▶ the bank orchestrators ──▶ ⑨
        a STRING crosses out, a FILE PATH comes back.

   ⒟ ✗ FORBIDDEN
        ⑨ ──▶ ⑦    a QA file naming a claim, a paper, a consumer id
        ⑦ ──▶ ⑨    a consumer writing into the bank
        ② ──▶ stake the agent's clean context IS the wall

   ── what gets NO page here, and why ───────────────────────────────
   the qa verb that WRITES a QA file      → /haipipe-task, fn/qa.md + twin
   what a consumer may ASK and SPEND      → QB9@paper
   how a landed answer becomes prose      → QC1@paper
   using the channel from the paper side  → QA5@paper
```

## Content
### 1 · Six folders, and the count is the finding
#### The layer is not one folder, and reading it as one sends you to the wrong place
(six that ship, three shapes that hold, counted 260726)
`①` and `②` are the shared half: the model, the vocabulary, the one agent that carries a question across, 589 lines together.
`③` and `④` are the consumer halves, one per family, and they hold every line of enforcing code the layer has.
`⑤` is this board and `⑥` is the design record that preceded it.
Everything else is data: `⑦` where the stake lives, `⑧` the wall itself, `⑨` the bank.

#### The shared folder holds a test for a checker that is not in it
(`probe/haipipe-probe/test/` against `check-probe-cards.sh`, which lives in `③` and `④`)
The fixture under `test/fixture/proj/` builds a whole synthetic project, papers and tasks and discoveries, and `run-checker-tests.sh` drives a checker from a different skill folder.
That is the clearest single sign that the shared half and the enforcing half were meant to be one thing and are not.
It also means the test can pass against one fork while the other has drifted, since nothing names which fork it ran.

### 2 · The enforcement is forked, and the fork is declared rather than solved
#### Two checkers, 1096 and 679 lines, kept in step by a comment
(`③` declares itself the source and asks the other to follow)
The paper copy's own header says the application family "carries the same file, same rules, same shared LEAK_AWK pattern set", then lists the differences.
The paper fork has passes the application fork does not: the sidecar ledger pass, the manuscript placeholder-ownership pass, a resource-stage pass, and a twelfth terminal condition for a concern the bank cannot close.
Those are genuine consumer differences, so a single file would need flags rather than a merge, and that is a design decision nobody has made.
What is not defensible is the current state, where the divergence is 600 diff lines and the mechanism holding them together is the sentence "keep the two in step".

### 3 · The record that still outranks this board
#### Eight places cite `⑥` as the spec of record, and none cites `⑤`
(`skills/STRUCTURE.md` twice, plus seven skill families' changelogs)
`diagram/260714-probe-qa/` is five `.txt` files from 2026-07-14 carrying rulings R1 to R18, and it is named the layer's contract in `STRUCTURE.md` line 8 and again at line 181.
The paper board's `QA1@paper` calls it "a design FOLDER, not a board. The one gap", which was true on 260725 and is now stale, because `⑤` exists.
Until the citations move, this board is a second record rather than the record, and a fresh agent following `STRUCTURE.md` reaches the `.txt` files.

### 4 · Three skills, one wall, and why the seams are declared
`/haipipe-probe` is the only skill that touches both sides, so it is the one that has to state the seams rather than assume them.
The paper board and this board were linked in both directions on the day this board was created, because a cross-board reference written as prose does not survive a rename: three broke on 260726 alone, and the only one caught quickly was caught because the link had been declared.

### 5 · The cut with the paper board
The paper board's `QA5@paper` describes the channel as a consumer needs it: where `1-probes/` sits, what a file looks like from outside, who is across the wall.
This board describes what the layer guarantees: why the stake may not cross, what one entry must contain, what the checker fails on, and what nothing holds at all.
Same folder, two readers, and the two descriptions must not drift into disagreeing about the same fact.

### 6 · Placing something new
```
 a probe rule still argued            →  a Q face on ⑤
 a probe rule decided                 →  ⑤ as a ## Law, then graduate into ①
 a word both families must share      →  ① SKILL.md, then propagate  (QD1)
 a check one family needs             →  that family's fork, ③ or ④
 a check BOTH families need           →  ③ first, then copy to ④, by hand
 one consumer's question and stake    →  ⑦
 one q-executor and its binding       →  ⑧
 an answer                            →  ⑨, written by the bank, never by us
```

## Aims
- [x] 🗺 The layer is drawn once, with the out-of-scope list beside it
- [x] 🔗 The seam with the paper board is declared in both directions
- [x] 🗂 Every folder that holds probe material is counted
      Six that ship and three shapes that hold, with line counts and versions, measured 260726.
      The count is what surfaced the forked checker and the stale spec pointer, neither of which was visible while the layer was described as "one skill".
- [ ] 🧠 JL confirms this board's scope is ⑧ and its edges
      The alternative is that the probe board also rules the executor-side `qa` verb, which today belongs to `/haipipe-task`.
      This closes when the split is agreed rather than inherited from where the code happens to live.
- [ ] 🍴 The forked checker gets one owner or one file
      1096 lines against 679, kept in step by a comment, with real consumer differences inside the divergence.
      This closes when JL rules either one file with family flags, or two files with a named owner and a diff check that runs.
- [ ] 📌 The spec of record moves from `⑥` to `⑤`
      `STRUCTURE.md` and seven changelogs point a fresh agent at five `.txt` files from 260714.
      This closes when the citations name this board, or a ruling says the `.txt` folder stays the contract and this board is only its argument.
- [ ] 🔍 The two descriptions of the same folder are compared once
      `QA5@paper` and `QA7` describe one thing from two sides; nobody has read them together to check they still agree.
      `QA1@paper` also still calls this board's folder "the one gap", which the existence of this board makes wrong.

## States
The map is drawn, the seams are declared, and as of 260726 the folders are counted rather than gestured at.

Counting them found two things that the phrase "the probe layer" had been hiding.
The enforcement is forked into two files that differ by 600 diff lines and are reconciled by hand.
And the layer's cited contract is still the `.txt` folder from 260714, in eight places, none of which knows this board exists.

What is not settled is the scope line itself: this board rules the wall because that is where the code sits, not because anyone decided it should.

## Files
- `SKILL.md`
  The shared model, `①`. Defines the vocabulary every other folder copies.
- `haipipe-probe/`
  The shared folder, including the `test/` fixture that drives a checker living elsewhere.
- `agents/`
  `②`, the one agent that carries a q-executor across the wall.
- `haipipe-task/`
  Owns the executor side: the `qa` verb that writes the answers this layer reads.
- `haipipe-discovery/`
  The other bank, same door, same file shape.

## Glossary
adapter: a consumer family's own probe skill, `③` or `④`, which restates the shared model for one kind of consumer and holds that family's checker.
spec of record: the file a skill's changelog names as the authority its rulings came from. Today that is `⑥`, not this board.
