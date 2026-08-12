# The intervention board: 0-lifecycle becomes a control plane
state: 🔴 OPEN
owner: JL
method: read the precedent off QA7@paper, map every stored row to one home, and put the three rulings in front of JL as Decision Now rows

## Opening
Should an intervention's `0-lifecycle/` become a live board, replacing the dashboard and the STATUS.md Gate Ledger as its entry face?
A live board is one rendered S page per gated lifecycle stage, the face a paper already enters through.
Today `enter` prints a dashboard that dies with the session, and STATUS.md stores the frontier, the defect the paper board retired.
This page maps what migrates where and puts three rulings in front of JL.

**What a live board is**: one rendered page per lifecycle stage, of the S kind that closes when a human passes its gate; the paper family's `0-lifecycle/` already renders this way, and its URL is what `/haipipe-paper enter` hands the human.

**What the entry face is**: the first surface a person sees when they start work on an intervention; today that is the terminal dashboard `/haipipe-application enter` prints, plus the STATUS.md state file it scaffolds.

**What the Gate Ledger is**: the table in STATUS.md recording who confirmed each stage done, one `| <stage> | yes | <who> | <date> |` row per passed gate.

**Covered elsewhere**: QA7@paper ruled this same question for papers and is cited here as precedent, not re-argued; this page owns only the intervention case and its migration map.

**Why now**: round 3 opened to settle the entry face, and every session the two consoles run apart is drift between skills built as mirrors of each other.

**What this page does not do**: it decides nothing; the three rulings sit as Decision Now rows in `## States`, and JL answers them.

## Writing Style
How this page must be written, so the next editor edits to the same rules.

**Name the surface, every time**: the dashboard (the terminal render), STATUS.md (the state file), and the board (the proposed face) are three different things, and an unqualified "the status" is exactly the confusion this page exists to remove.

**A migration row has one destination**: a source row that lands in two places recreates the stored-pointer defect in prose, so every row in division 3 names exactly one home or an explicit retirement.

**Proposals are not rulings**: this page recommends; until a Decision Now row carries JL's answer, write "proposed" and never "ruled".

**Language and sentences**: English only, one sentence per source line, no em-dashes.

## Diagram
**The entry face, today and proposed**: what `enter` hands the human, and where state lives.

```text
 🖥 TODAY
    🚪 entry    /haipipe-application enter ─▶ terminal dashboard
    📍 state    STATUS.md · current_layer · maturity · Gate Ledger
    📚 stages   0-lifecycle/<stage>/<stage>.md

 🌐 PROPOSED
    🚪 entry    /haipipe-application enter ─▶ the board's URL
    📍 state    S page state: lines · frontier derived
    📚 stages   one S page per gated stage + Stage Contract
```

## Content

### 1 · The entry face today: two keepers of one fact
**Two keepers of one fact**: where the frontier lives right now.

```text
 🖥 dashboard        derives the frontier from disk · gone when the session ends
 📄 STATUS.md        stores current_layer · maturity · venue rows · Gate Ledger
 📁 1-rounds/        stores latest.md · a pointer to the current round
 ⚖️ the drift rule   disk wins · STATUS.md drift is flagged
```
🖥 Establishes what the current face is made of, and which of its parts stores what disk can derive.

#### 1.1 · The dashboard is right, then it is gone
(the console derives everything per session and keeps none of it)
`/haipipe-application enter` reads the folder, derives the frontier, the maturity and the open needs from disk, and renders the dashboard in the terminal.
Its only persistent trace is `.intervention-console.yaml`, which the contract itself calls session state that a fresh session re-derives.
A colleague who did not run the command sees nothing, and the render cannot go stale only because it does not survive long enough to.

#### 1.2 · STATUS.md stores what the console just derived
(the contract guards against the file it scaffolds)
STATUS.md carries `current_layer` and `maturity` as stored rows, and the same contract that scaffolds them rules that the console never trusts the file alone: disk wins, and drift is flagged.
A file whose own reader must be armed against it is the shape QA7@paper names: a stored derivation agrees for a while, then reports a stage the gates no longer support, and nothing announces the moment.
The paper family stored its frontier in a `current_layer` too, and retired it.
`1-rounds/latest.md` is the same defect one folder over: a stored pointer to the current round, which the paper board replaced with one S-Round page per round.

#### 1.3 · The one fact disk cannot re-derive
(a human approval is real content, not a cached derivation)
The Gate Ledger records who confirmed each stage and when, and a stage counts as passed only when its doc has real content on disk AND its ledger row says yes.
That approval is not derivable from the stage docs, so any migration must move it rather than drop it; division 3 gives it its home.

### 2 · The precedent: what a lifecycle board is
**One glyph, two board kinds**: what ✅ commits a reader to on each.

```text
 🏷 page kind    📋 design: Q, a decision   ·   📄 lifecycle: S, a gated stage
 ✅ means        📋 a ruling was made       ·   📄 a human passed the gate
 ♻️ after ✅     📋 the Law leaves          ·   📄 the Content stays
 🧲 over time    📋 the board empties       ·   📄 the board accumulates
```
📄 Establishes the four properties QA7@paper proved for papers, and how far each carries to an intervention.

#### 2.1 · Four properties, and none of them is a guess
(the precedent is measured, not argued)
QA7@paper runs one S page per independently gated unit, derives the frontier as the earliest page whose gate has not passed, lets nothing graduate because a gated page's Content is the artifact, and treats a stale render as a defect because the board is the face the human enters through.
The frontier derivation was run against a real paper's 40 S pages on 260726, and every stage predicate resolved.
On that board ✅ means a human passed the gate, and only a human writes it.

#### 2.2 · The intervention spine is already a list of gated units
(every Gate Ledger row is the gate of exactly one stage)
Seed, the 1a-1d ladder rungs, venue, pitch, narrative, display and section-edit each pass one confirm gate today, which is exactly what earns a page.
A venue-skipped stage is passed over rather than counted as a gap in the current contract, and the skip travels with the venue rows to the venue S page, so the frontier derivation reads it there.

#### 2.3 · Where interventions differ, and where they only look different
(the artifact edge matches; the maturity ladder has no paper analogue)
The deployable artifact in `0-artifacts/` looks like a divergence but is the same OUT edge the paper board has: `sections/*.tex` is generated from S page Content there, and an SMS draft is generated from the ladder and venue stages the same way.
Two real differences remain: an intervention is a plain folder with no repo backing, and the maturity ladder (prospect through retired) has no paper analogue, so division 3 must either derive it from the S pages or retire it.

**2.4 · The four calls, named**
- One S page per gated unit: adopt; the spine already provides the units (2.2).
- Frontier derived, never stored: adopt; it is the console's own derivation, relocated (3.2).
- Nothing graduates: adopt; the stage docs are the Content, and artifacts leave by generation only (2.3).
- Stale render is a defect: adopt; `enter` builds the board before the human sees anything, so the face cannot be optional.

### 3 · The migration map: every stored row gets one home
**Every row's one home**: the proposed map from stored to derived or moved.

```text
 🧾 Gate Ledger row            ━▶ the stage's S page · ✅ state + dated Log line
 📍 current_layer              ━▶ derived · earliest S page with an unpassed gate
 🌡 maturity                   ━▶ derived from the S pages, or retired
 📮 venue · stages_skipped ·
    claims_settlement          ━▶ the venue S page
 🔁 1-rounds/latest.md         ━▶ one S-Round page per round · no pointer file
 🪪 identity rows              ━▶ D2's ruling · machine header or the board
 🧰 open needs · focus strip   ━▶ each S page's Aims · the board Index
```
🗺 Establishes the proposed destination of every row STATUS.md and the dashboard hold today, so the ruling is made against a complete map rather than a slogan.

#### 3.1 · Gate rows become the gate itself
(the approval survives as the S page's own state)
A ledger row of the shape `| 1c-claims | yes | JL | 260721 |` becomes the 1c-claims S page's ✅ `state:` line plus one dated Log line naming who passed it.
That is the paper rule adopted unchanged: only a human writes the ✅, and an unattended worker may prepare a gate but never pass it.

#### 3.2 · The derived values stop being stored
(current_layer and maturity become one pass over the pages)
`current_layer` becomes the frontier the console already computes: the earliest non-skipped S page in spine order whose gate has not passed.
`maturity` either derives from the same pages, since each rung is implied by which gates have passed and what `0-artifacts/` holds, or it retires; storing it would recreate the defect the migration removes.
The venue rows (`venue`, `stages_skipped`, `claims_settlement`) are written once at pin time and belong on the venue S page, which is where the pin is made.
Open needs stay derived, but they land as each S page's Aims instead of a table that evaporates with the terminal, and the focus strip becomes the board's Index.

#### 3.3 · What STATUS.md still holds afterwards
(the leftover file is D2, not an accident)
After the map runs, STATUS.md holds only identity: intervention, audience, created.
Whether that header stays as a machine-read anchor or retires entirely is JL's second ruling, and the map works under either answer.
What it may not keep under any answer is state: a leftover `current_layer` beside a board is two frontiers, and the enter contract's drift rule already tells us how that ends.

## Aims

### A2 · 📄 The precedent: what a lifecycle board is
- A2.1 · Each of the precedent's four properties carries an explicit adopt-or-diverge call for interventions.
  **Done when:** one page per gated unit, the derived frontier, nothing graduates, and stale-render-as-defect each have a call on this page, with any divergence reasoned.

### A3 · 🗺 The migration map: every stored row gets one home
- A3.1 · Every stored row and derived value has exactly one destination or an explicit retirement.
  **Done when:** the map covers every STATUS.md row and every dashboard value, and no destination stores a second copy of a derivable fact.
- A3.2 · No shipped skill still scaffolds what the ruling would remove.
  **Done when:** `haipipe-application-enter` scaffolds no stored `current_layer` or Gate Ledger, and its console builds the board instead of a terminal-only dashboard.
  **Plan:** blocked until D1 is answered; the rewrite lands in the enter skill's Dashboard Contract section first.

### P · 🏁 Page-level
- P1 · The round-3 ruling is answered and recorded.
  **Done when:** all three Decision Now rows carry JL's answer, the rulings stand in `## Law` with the rejected options named, and the matching States rows update in the same edit.

## States

### Decision Now
- [ ] 🗣 Does an intervention's `0-lifecycle/` become a live board, its entry face?
      📍 `Part` 2 · the precedent and the semantics
      🔔 `Why now` round 3 opened to settle the entry face, and the paper family has run this way since 260726, so every session widens the gap between two consoles built as mirrors
      ⭐ `A ·` adopt: one S page per gated stage under `0-lifecycle/`, rendered by haipipe-board; `enter` builds the board and hands over its URL, and the terminal keeps only the URL, one frontier line and the next command. CC recommends A: the precedent is measured (QA7@paper, 40 S pages, every predicate resolves), and the enter contract already distrusts the file this replaces.
      `B ·` decline: keep the terminal dashboard and the Gate Ledger; the paper precedent stays paper-only, and the drift rule remains the guard.
      🛑 `Blocks` D2, D3, and A3.2's enter rewrite
      🤖 `If nobody answers` B holds by inertia: the dashboard keeps rendering and nothing migrates
- [ ] 🗣 What does STATUS.md hold after migration?
      📍 `Part` 3 · the migration map
      🔔 `Why now` the map gives every state row a board home, and an unruled leftover file becomes a second pointer, the defect the migration exists to remove
      ⭐ `A ·` keep it as a machine-read header: identity only (intervention, audience, created), with no `current_layer`, no `maturity`, and no Gate Ledger. CC recommends A: scripts that key on the file keep a stable anchor, and a header with no state cannot drift.
      `B ·` retire it: identity moves onto the board and the root loses the file; every reader of STATUS.md must be found and repointed first.
      🛑 `Blocks` the migration step and what a new intervention's scaffold writes on day 0
      🤖 `If nobody answers` A: keeping a stateless header is the reversible choice
- [ ] 🗣 When does an existing intervention migrate?
      📍 `Part` 3 · the migration map
      🔔 `Why now` the enter skill already runs one confirm-gated migration for the pre-ladder layout, and a second, differently triggered path would double the shapes a session can meet
      ⭐ `A ·` on next enter, confirm-gated: the console detects the old face, offers the move, and migrates only on the user's yes, the same pattern as the ladder migration. CC recommends A: it reuses a proven gate and touches no intervention nobody is working on.
      `B ·` one batch sweep now: every intervention migrates in one pass before any session touches it; faster to done, but it rewrites folders nobody has opened and any defect lands everywhere at once.
      🛑 `Blocks` nothing while D1 is open; after a yes on D1 it blocks the first enter into any existing intervention
      🤖 `If nobody answers` A: the confirm gate means an unanswered row migrates nothing

### A2 · 📄 The precedent: what a lifecycle board is
- ✅ A2.1 · Met on this page: 2.4 names an adopt call for each of the four properties, with the artifact edge shown in 2.3 as generation-out rather than a divergence.

### A3 · 🗺 The migration map: every stored row gets one home
- 🧠 A3.1 · The map is drafted in division 3 and waits on D1 and D2, which decide whether it runs and what the header keeps.
- ⬜ A3.2 · Not started; the enter skill still scaffolds STATUS.md with a stored `current_layer` today, and rewriting it before D1 is answered would decide the ruling by side effect.

### P · 🏁 Page-level
- 🧠 P1 · Waiting on JL: the three Decision Now rows above are unanswered.

## Files

### 📥 Input files · what this ruling reads
- `../../01-haipipe-paper-260725/QA-design/QA7-the-paper-board.md`
  The precedent (QA7@paper): the four properties division 2 carries over, measured against a real paper on 260726.
- `../../../application/0-enter/haipipe-application-enter/SKILL.md`
  The dashboard contract this ruling would replace; division 1 states its drift rule and division 3 relocates its derivations.
- `../_fixture/STATUS.md`
  The Gate Ledger and state rows as they exist today, the source column of division 3's map.

## Glossary

- 🚪 **Entry face**: the first surface a person sees when they start work on an intervention; today the terminal dashboard plus STATUS.md, and under this proposal the rendered board.
- 🧾 **Gate Ledger**: the STATUS.md table recording who confirmed each stage done and when, one `| <stage> | yes | <who> | <date> |` row per passed gate.
- 📌 **Stored pointer**: a derivable fact written into a file, such as `current_layer`; it agrees with the pages for a while and then lies without announcing it.
- 🌐 **Lifecycle board**: a board whose pages are gated S stages rather than Q decisions; its Content accumulates and never empties.
- 🕹 **Control plane**: a surface you operate the work from, where state is read off the pages themselves rather than reported beside them.
- 📄 **QA7@paper**: the paper design board's page that ruled this same question for papers, at `../../01-haipipe-paper-260725/QA-design/QA7-the-paper-board.md`.

## Log

260802 · Page created for the round-3 ruling: the precedent read from QA7@paper, the current face read from the enter contract and the STATUS.md fixture, the migration map drafted, and three Decision Now rows put in front of JL.
