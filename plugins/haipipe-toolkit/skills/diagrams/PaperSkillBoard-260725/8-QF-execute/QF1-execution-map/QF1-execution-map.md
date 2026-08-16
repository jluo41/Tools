# Execute: what actually ran, as distinct from what was designed

state: 🟡 PARTIAL
owner: JL
method: record bounded runs from a named Delivery target through a named Engine route, with an artifact, evidence, and an owning reopen path

## Opening

How does the Board tell a delivery design apart from a run that actually produced something?

An execution is a bounded run of one named route on one named fixture, under explicit limits on what it may write. A receipt is what it leaves behind. The distinction matters because a design can be internally perfect and still have never been run, and from inside the board those two look identical.

**Where this page sits**: QB1 through QB10 own the desired delivery and its human gate, and QC1 owns the reusable route an execution invokes.
This group records what happened when the two were put together, and it is the third layer rather than a second authoring tree.

**Why a receipt is not permission**: the dangerous reading of a passing run is that it authorizes the next step.
It does not. A passing execution permits only its own declared next handoff, and QB9's promotion law still requires a person.
Every record here therefore names its non-write boundary explicitly, so what the run was forbidden to touch is as visible as what it produced.

**What a failure owes**: a page to reopen.
A blocked run that does not name the Delivery or Engine page responsible for the repair is a dead end, and the block will simply be rediscovered later by someone with less context.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md` and are not restated here.

**A record names all six fields or it is not a record**: Delivery target, Engine route, fixture, evidence, non-write boundary, reopen path.
A run written up without its non-write boundary reads as though nothing was at risk, which is the one thing a reader most needs to know.

**Never let a receipt sound like an approval**: write what a run permits, not what it proves.
"G0 to G3 passed" is a fact; "the candidate is ready" is a promotion decision this layer may not make.

**Report a block with its owner in the same sentence**: a blocker with no named page is an orphan, and orphans are how the same defect gets found twice.

## Diagram

**One bounded execution**: what goes in, what comes out, and where a failure goes.

```text
   🎯 Delivery target  +  ⚙️ Engine route  +  📁 named fixture
                            │
                            ▼
                  🧪 BOUNDED EXECUTION
                            │
              📦 artifact / candidate / observation
                            │
              🚪 gate  +  🧾 receipt  +  🔒 non-write check
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ✅ pass                      🛑 fail
       the declared NEXT            reopen the owning
       handoff, and nothing         Delivery or Engine
       further                      page
```

## Content

### 1 · Execute is not a second authoring layer

**Three layers, one authority each**: what each may say, and what it may not.

```text
   📄 DELIVERY        ⚙️ ENGINE           🧪 EXECUTE
   the only content   reusable route      what OCCURRED when
   authority          definitions         a route was run
        │                  │                    │
        └──────────────────┴────────────────────┘
   🚫 Execute never becomes a place to author content
   ✅ Execute may record a BLOCK that stops the next handoff
```

🧭 Establishes Execute's standing beside the other two groups, so a record is never mistaken for a decision.

#### 1.1 · A block is a first-class result
(a run that stopped is evidence, and it is often the more useful kind)
Recording a block prevents the run from reaching the next handoff, which is the mechanism working rather than a gap in the record.
A board that only writes down successes cannot tell an untried route from a refused one.

### 2 · Three kinds of execution evidence

**What each mode can prove**: and the one the author is not allowed to run.

```text
  ⚙️ MECHANICAL     declared paths, contracts, static closure obey the route
                    e.g. manifest validation, a contract checker
                    👤 the author MAY run it

  📦 CANDIDATE      a bounded route makes an ISOLATED artifact without
                    touching submission authority
                    e.g. Main-1 ━━▶ 3-dist/tex/<run-id>/
                    👤 the author MAY run it

  🧪 FRESH AGENT    a clean-context agent finds the entry, follows the
                    route, and stops at the right boundary
                    🚫 the author may NOT run it ── see QF3
```

🔬 Establishes the three evidence modes, and which of them the author's own context disqualifies them from producing.

| Mode | What it proves | Example |
|---|---|---|
| Mechanical | Declared paths, contracts, and static closure obey the route | manifest validation or a contract checker |
| Candidate | A bounded route makes an isolated artifact without touching submission authority | Main-1 → `3-dist/tex/<run-id>/` |
| Fresh agent | A clean-context agent finds the entry, follows the route, and stops at the right boundary | `QF3` stage acceptance run |

#### 2.1 · Only the third mode can fail invisibly
(the first two produce facts; the third produces a judgment the author cannot make about themselves)
Mechanical and candidate runs yield artifacts anyone can inspect afterwards.
A behavioural run is about what an agent DID, and the author reads every contract with the context already in their head, which is why QF3 owns that mode separately.

### 3 · The first recorded execution

**MISQ Main-1, candidate-only**: the six fields, filled in for real.

```text
  🎯 target    Main ━▶ Build · main-1 introduction projection
  ⚙️ route     stage authority ━▶ haipipe-paper-project generate/check/compile
  📁 fixture   Paper-Personality2Opioid-MISQ2026 · candidate-only
  📦 artifact  3-dist/tex/f53ccf5c…/
  🧾 evidence  G0 coverage ✅ · G1 gate ✅ · G2 isolation ✅ · G3 markers ✅
  🛑 block     G4 refuses a BASELINE missing displays/S-Display-4a-…/float.tex
  🔒 non-write no submission file changed · G5 not run
  🔁 reopen    repair the owning Display projection, rerun isolated G4 from QB9
```

🧾 Establishes the first complete record, and demonstrates the six-field form on a real run rather than describing it.

| Field | Record |
|---|---|
| Delivery target | Main → Build, `main-1` introduction projection |
| Engine route | stage authority → `haipipe-paper-project` generate/check/compile boundary |
| Fixture | Paper-Personality2Opioid-MISQ2026, candidate-only run |
| Artifact | content-addressed candidate under `3-dist/tex/f53ccf5c5fc965bbc0c74f478e9015ac8ded949e91e7bc35a667c54cc38ffa98/` |
| Evidence | G0 exact coverage, G1 gate, G2 isolation, and G3 pre-render marker checks passed |
| Block | G4 refuses the baseline missing `displays/S-Display-4a-main-regression/float.tex` |
| Non-write boundary | No submission file changed and G5 was not run |
| Reopen path | Repair the owning Display projection, then rerun isolated G4 from QB9 |

#### 3.1 · The block belongs to the baseline, and the record says so
(that one field is what makes the run actionable instead of merely disappointing)
The absent Display input is reached by the baseline master, not introduced by the candidate.
Naming the reopen path in the record is what sends the repair to the owning display work rather than leaving it as a property of the build.

## Aims

### A1 · 🧭 Execute is not a second authoring layer
- A1.1 · Execute is defined as a bounded real or fixture run, and never as content authority.
  **Done when:** every record in this group names its six fields, and no record states a rule that a Delivery or Engine page does not already own.

### A2 · 🔬 Three kinds of execution evidence
- A2.1 · A fresh-agent execution exists for a complete route.
  **Done when:** QF3's behavioural run has been performed on one full stage and its observations are recorded here as a third-mode record.

### A3 · 🧾 The first recorded execution
- A3.1 · The Main-1 candidate-only execution is recorded without promotion.
  **Done when:** the record shows G0 to G3 passing, G4 blocked, G5 unrun, and no submission file changed.
- A3.2 · Round has an execution record once it has a callable route.
  **Done when:** one Round record connects reviewer input, chosen action, diff, compile, and resubmission.

### P · 🏁 Page-level
- P1 · Every Delivery concern points at an execution record or at an explicit absence.
  **Done when:** a reader can tell, for each of QB1 to QB10, whether a route has ever been run, without inferring it from an Engine design.

## States

### A1 · 🧭 Execute is not a second authoring layer
- ✅ A1.1 · Ruled 260730, when JL replaced the proposed Test layer with Execute. The Law names all six fields and the Main-1 record fills every one of them.

### A2 · 🔬 Three kinds of execution evidence
- ⬜ A2.1 · Not started. QF3 is 🔴 OPEN and its behavioural run has never been performed, so the third mode is defined and unexercised.

### A3 · 🧾 The first recorded execution
- ✅ A3.1 · Done. The candidate is content-addressed under `3-dist/tex/f53ccf5c…/`, G4 records the baseline blocker, and G5 remains unrun by design.
- ⬜ A3.2 · Not started. Round has a delivery definition on QB10 but no callable route, so there is nothing to record yet.

### P · 🏁 Page-level
- 🔨 P1 · Active and partial. Build has a record; Present and Round have delivery definitions and no runnable record, and their absence is stated here rather than linked from their own pages.

## Files

- `2-QB-delivery/QB9-build/QB9-build.md` · owns the Build delivery contract and the G5 promotion law
- `6-QC-engine/QC1-delivery-skill-map/QC1-delivery-skill-map.md` · owns the Delivery × Engine route map
- `../QF3-fresh-agent-run/QF3-fresh-agent-run.md` · owns the behavioural mode this page cannot produce
- `2-src/projection-receipts/` · immutable records of the MISQ candidate run
- `3-dist/tex/f53ccf5c5fc965bbc0c74f478e9015ac8ded949e91e7bc35a667c54cc38ffa98/` · the candidate artifact

## Law

- An execution must name its Delivery target, Engine route, fixture, observable evidence, non-write boundary, and failure-to-reopen path.
  Passing an execution permits only its declared next handoff; it never implies promotion.

## Glossary

- **Execute**: a bounded run that records what actually happened when a Delivery route was invoked.
- **Non-write boundary**: files or authorities the run is prohibited from changing.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into three divisions with face figures and captions, Aims regrouped as A1/A2/A3/P with `Done when`, States mirrored per Aim.
260801 · Renamed into QF Execute after the Paper Skill-Board consolidated its groups.
260730 · Created after JL replaced the proposed Test layer with Execute and accepted the Delivery-first, skill-first Engine design.
