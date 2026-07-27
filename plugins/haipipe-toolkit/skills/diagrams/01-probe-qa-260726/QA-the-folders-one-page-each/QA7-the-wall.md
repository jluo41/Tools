# ⑧ The wall: one q-executor, one file, one path

state: 🟡 PARTIAL
owner: JL
method: one q-executor, one file, one path, four named subsections, and the original kept beside the strip so it can be audited

## Question
What is one probe, and what is it on disk?
One question a consumer cannot answer, bound BY PATH to one bank file that answers it, living as one `QXn_<slug>.md` of its own.
Those are one ruling seen twice: nothing binds by id across the wall, so the unit has to be reachable by path, and a path needs a file.

This folder is the wall itself, which makes it the place scope creeps.
It sees the question and it sees the answer, and it is tempting to let it judge the fit.
It must not, because whether an answer settles a claim depends on the claim, and the claim lives in the consumer's own files where a human can still argue with it.
The disk shape follows from the same wall: an entry named "the third heading in that file" is not a pointer anyone can hand to an agent.

## Boundary
- ✅ Covered here
  What one probe is, the folder and file layout, the four subsections, the frozen strip and how it is audited, and the pre-gate review that reads what a checker cannot.
- ↪ Covered elsewhere
  The stake this folder must not contain, and the law about it, is `QA6`; the bank on the other side is `QA8`.
  Where the answer comes to rest after it lands here is `QB6`; the act that writes into this folder is `QB2`, and the loop's order is `QB1`.
  What a consumer needs in order to USE the channel, rather than what the layer guarantees, is `QA5@paper`.

## Diagram
```
   CONSUMER ⑦ (holds the stake)            THE BANK ⑨ (probe-unaware)
   ──────────────────────────              ────────────────────────
   stage doc                               tasks/A03_welldoc_cycle/
     ## Q-Claim-6  "…my claim dies if…"      └── QA/1-cycle-indicator.md
          │                                        ▲
          │ ① ORGANIZE · strip the stake            │ written for the
          ▼                                        │ executor's OWN reasons
   1-probes/PP03_welldoc/QX1_cycle.md              │
     ### q-executor  ────── the ONLY thing ────────┘
         FROZEN once written; the dispatch payload
     ### q-consumer         the originals, kept so the strip
                            can be AUDITED rather than trusted
     ### bank binding       route · bank · target · state
     ### a-executor  ◀───── a copy of the answer

   one folder per topic · one file per q-executor · one entry per file
   no markdown tables anywhere: a table hides which field is missing
```

## Content
### 1 · Why the unit is the q-executor
A consumer question and an executor question are not the same question, so one of them has to be the unit.
The q-executor is chosen because it is the reusable one: several consumer questions routinely reduce to a single executor question, and when they do the entry lists them and copies each in.
Numbering by consumer question would produce one bank task per asker for the same fact.

### 2 · Carrying is not judging
The probe copies the answer back as `### a-executor` and stops.
The consumer then writes its own interpretation next to its own question, in its own stage doc, where the stake it carries is legitimate.
Whether a claim survives is decided in `1b-claims.md` and never in `1-probes/`.

### 3 · The file holds both halves of the strip, which is what makes it auditable
The stripped question and the original sit in the same file, in adjacent subsections, so the comparison needs no second document and no memory of how the entry was written.
That is a property of the FILE, and it is why the entry has four subsections rather than two: the act that produces them is `QB2`, and this shape is what the act writes into.
Measured 260726 on the MISQ paper: 17 files hold 27 `### q-consumer` bullets, so six of them carry the evidence that one executor question served several askers.

### 4 · The layout, and why the flat form is retired
`1-probes/PPNN_<topic>/` is a folder per topic holding one `QXn_<slug>.md` per q-executor, each with a single `## QX<n>` entry.
The flat `PPNN_<topic>.md` came first and is retired: it made an entry unaddressable and made two people editing two questions edit one file.
Splitting cost almost nothing, because `check-probe-cards.sh` globs `PP*/*.md` and each file keeps its heading, so the section parser never changed.
PP numbers are consumer-local footnote numbers, and two consumers may both carry a PP04 because no PP id ever crosses to the bank.

### 5 · Four named subsections, and no tables
Each part exists because something must be auditable: `q-executor` is the frozen dispatch payload, `q-consumer` keeps the originals so the strip can be audited, `bank binding` records route, verdict and target so a reader can see WHY the entry points where it does, and `a-executor` is the copy that makes the consumer side self-contained.
All but the last are authored at PROBE.
No markdown tables anywhere, because a table hides which field is missing.

#### Deferred is declared, never inferred
(the two ways of not answering a question must not look the same on disk)
An entry whose bank verdict sits above the run's `probe_depth` lands in `deferred`, which is a correct outcome rather than a failure.
It must carry `**deferred**: depth-<n> · <what it would take>`; without that line it is a bare `planned` and fails as `deferred-undeclared`.
`SKILL.md` line 173 names `probe-not-run` for this, which is the wrong code and is `QC2`'s open correction; this page repeated the same error until 260726.

#### Build-lane fields
(an answer that legitimately takes weeks still has to be accountable)
An entry whose answer takes days to weeks carries owner, eta, blocks and cross-project fields, and only at `state: commissioned`.
An entry still commissioned when a gate runs is build-lane by definition, so those fields are unconditional there.

## Items to Finish
- [x] 📐 The unit is the q-executor, and it is one file with one path
      `QXn_<slug>.md` per q-executor, one `## QX<n>` each; the flat form is retired and the checker glob still covers it.
- [x] 🧱 Carrying and judging are separated in the contract
- [x] 🧩 Four named subsections, no tables
- [x] ✂️ The file holds the frozen strip and the original side by side
      Which is what makes the strip auditable from the file alone; the act itself is `QB2`.
- [x] 🏷 `deferred` must be declared with a depth and a cost line
- [x] 🧰 Build-lane fields are required at `commissioned`
- [ ] 🧪 The separation is checked, not just stated
      Nothing detects a probe file that has started interpreting, which is the failure this page exists to prevent.
- [ ] 🧹 The retired shape is gone from real projects
      Scanned 260726: two projects still carry a `1-probe-plans/` folder, `Project-Subjective-Label` and `Project-PhyPat-Simulation`, and each holds nothing but a `README.md`.
      The MISQ paper, the only consumer with a live probe layer, is clean and uses `1-probes/` throughout, so this is two stub folders rather than live data in the retired shape.
- [ ] 📖 A worked example of every entry state ships with the skill
      The fixtures cover five states as test inputs; the prose shows one filled entry.

## Where we are
Ruled and in use. The unit is the q-executor, the layer is communication only, the strip is auditable because both halves are kept, and the disk shape makes every question path-addressable.

Three gaps remain and none is about the design: judging is unchecked, two projects still hold an empty folder in the retired shape, and the states are shown as rules rather than as examples.

## Files
- `SKILL.md`
  The operational contract and the vocabulary source. Where another skill disagrees, this file wins.
- `ref/probe-template.md`
  The fillable form and the per-field rules.
- `test/`
  Fixtures carrying five QX states, used by `run-checker-tests.sh`.
