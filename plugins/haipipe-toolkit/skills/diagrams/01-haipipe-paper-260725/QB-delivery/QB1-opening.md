# Delivery Opening: why the paper exists, where it goes, and what it promises

state: 🟡 PARTIAL · the three-part contract is ruled; one retargeting fork is open in Decision Now
owner: JL
method: bind premise, seed, venue choice, and pitch into one reader-facing Delivery concern without inferring stage dependencies from Board order
session: 8239b12e-122f-405a-ba61-352049912a1a

## Opening

What belongs together when a reader asks how this paper opens?
Three things that usually get filed apart.
The seed is why the paper exists, such as opioid prescribing varying with physician personality.
The venue is the journal it is written for, such as MISQ, and the pitch is what it promises that journal's reader.
Each is settled at a different moment, so they drift into three folders, and this page rules them one concern.

**Where this page sits**: it is the first of the ten Delivery concerns, and QB2 Work is the next.
Work grows the evidence this opening reveals is needed, and it owns the narrative, because an arc is built from the claim ledger rather than from the promise.
QB6 Main owns the manuscript Introduction; this page is lifecycle control, never §1 prose.

**Why Venue lives inside Opening**: a venue is not a later administrative step, it is one of the three answers a reader wants immediately.
Filing it as its own Delivery group made the paper look as though it chose a journal after deciding what it argued, which is backwards.

**What the 260802 `QBv` group did NOT take from this page**: the decision.
`QBv` holds what each venue KNOWS, one page per venue TARGET, because a venue's rewards reach QB4, QB5, QB6, and QB11a at once and can be filed under none of them.
This page still owns which venue this paper picked and where that pin lives; the QBv group intro states the split and cites this ruling rather than reopening it.

**What this grouping does not do**: it does not renumber stages and it does not replace the explicit dependency graph.
Delivery order is reading order; execution order is declared by each stage contract.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never let this page drift into Introduction advice**: the boundary against QB6 is the one this page loses most often.
A sentence about how to phrase the paper's first paragraph belongs on Main. A sentence about whether the paper has decided its promise belongs here.

**Say the three in reader order**: the order carries the argument for the grouping.

✅ `seed, venue, pitch`  ❌ `seed, pitch, and also the venue`

Any other order makes Venue look appended again, which is the reading the 260729 ruling overturned.

**A Decision Now row is read once, by a person in a hurry**: short sentences, plain words, real numbers.
Any option a reader has to re-read has already failed, whatever it says.

**The arc is not this page's**: narrative moved to QB2 Work on 260802.
A sentence here about how the argument is ordered has crossed into Work, whatever it is about.

## Diagram

**The Opening contract**: three answers, the three pages that hold them, and one shape they share.

```text
   🌱 SEED             🎯 VENUE            📣 PITCH
   why it              where it            what it
   exists              goes                promises
      └──────────────────┴───────────────────┘
                📜 one Opening contract
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
  📄 S-Seed-0        📄 S-Venue-0      📄 S-Venue-1
  ───────────        ───────────       ───────────
  ### 1 ━▶ A1        ### 1 ━▶ A1       ### 1 ━▶ A1
  ### 2 ━▶ A2        ### 2 ━▶ (none)   ### 2 ━▶ A2
  ### 3 ━▶ A3        ### 3 ━▶ A3       ### 3 ━▶ A3
  ### 4 ━▶ A4        ### 4 ━▶ A4       ### 4 ━▶ A4

  🔑 ONE shape on every page: the stage's sections ARE its numbered
     Content divisions, the Aims groups mirror them by number, and ANY
     division may raise a Q-<Stage>-<n> · one that raises none has no group
                         │
                         ▼  a Work answer may reopen the pitch
                  🔁 QB2 · Work
                     resource · claims · 🧵 narrative

  🚫 not an execution graph · Delivery order is READING order
  🚫 not the manuscript Introduction, which is QB6 Main
  🚫 not the arc ── that is Work's, since 260802
```

## Content

### 1 · The delivery contract

**What Opening owes**: what it takes in, what it hands on, and the gate that closes it.

```text
  📥 CONSUMES              📤 PROJECTS TO           🚪 GATE
  the paper premise   ━━▶  venue pin          ━━▶  a human accepts the
  known project            paper promise           why / where / promise
  context                  downstream stage        snapshot
                           requirements
  🚫 no ad-hoc                                 🔁 later Work evidence
     literature                                   may reopen it
  🚫 no computation
```

📜 Establishes the contract this concern owes the reader, and the one gate that closes it.

| Field | Contract |
|---|---|
| Lifecycle | Groups `0-seed/` with `2-venue/`; Venue is inside Opening in the Delivery reading order, not a later peer group. |
| Authority | `S-Seed-*` and `S-Venue-*` pages, excluding the narrative page, which Work owns. |
| Projects to | Venue pin, paper promise, and downstream stage requirements. |
| Skills | `haipipe-paper-stage` for seed, venue, and pitch. |
| Consumes | The paper premise and known project context; no ad-hoc literature or computation. |
| Gate | A human accepts the current why/where/promise snapshot; later Work evidence may reopen the affected pages. |
| Open gaps | Retargeting semantics remain a QA6 decision. |

#### 1.1 · The gate is a snapshot, not a freeze
(a reopened pitch is a normal transition, and the contract has to survive it)
Accepting the three answers does not close them for the life of the paper.
Work runs next and its answers can contradict the promise, so the gate records what was accepted and when.
Reopening is then a transition with a date rather than a failure of the gate.

#### 1.2 · Work sits in the middle of this group, on purpose
(the stages run 0, then 1a and 1b, then 2a and 2b, so this concern has a hole in it)
`stages/index.yml` runs seed 0, resource 1a, claims 1b, venue 2a, pitch 2b, narrative 3.
This concern holds 0, 2a, and 2b, so Work's two stages sit inside its span.
That is the price of grouping by what a reader asks rather than by when the machine runs, and the Law below is what keeps the two apart.

#### 1.3 · Three stages, three pages, and none of them may spend
(the mechanical facts the three share, so each division below can talk about expectations instead)
Seed writes into family Seed at unit 0; venue and pitch both write into family Venue, at units 0 and 1.
Unit 2 of that family is NOT this concern's: `S-Venue-2-narrative.md` belongs to QB2 Work, because narrative was ruled the third half of the venue contract on 260725 and moved to Work on 260802, keeping its family.
No contract spells a filename: each declares `board_family`, `board_unit`, and `board_slug`, and `stage.py resolve` composes `S-<Family>-<unit>-<slug>.md`.
All three declare `gates: [check]`, `probe_depth: 0`, and `runs: once`, so DRAFT, PROBE and REVISE run unattended, and that is safe only because at depth 0 a stage may reuse an answer that already exists and may never commission one that costs.
Each also declares an `artifact_fallback:` for papers that predate the S layout, and a run says which of the two it used.

### 2 · Stage Seed

**What a seed owes**: one venue-free question, and the hedged claim shape it implies.

```text
  🌱 STAGE SEED · order 0 · "Why might this paper exist?"
  📄 S-Seed-0-seed.md          🔨 draft · probe · revise · check

  📚 ## Content · four divisions        🎯 ## Aims · mirrored groups
  ─────────────────────────────         ──────────────────────────────
  ### 1 · Seed Question          ━━▶    ### A1 · ❓ Seed Question
        ONE · 🚫 VENUE-FREE                     - A1.1 · Q-Seed-1 · …
  ### 2 · Motivations            ━━▶    ### A2 · 💡 Motivations
        puzzle ▸ why now ▸ audience             - A2.1 · Q-Seed-2 · …
                                                - A2.2 · Q-Seed-5 · …
  ### 3 · Landscape              ━━▶    ### A3 · 🗺 Landscape
        🚫 not a related-work                   - A3.1 · Q-Seed-3 · …
  ### 4 · Tentative Claim Shape  ━━▶    ### A4 · 🎯 Tentative Claim Shape
        H1 + H2/H3 · ⚠️ HEDGED                  - A4.1 · Q-Seed-4 · …

  🔑 ANY division may raise a question · a division that raises none
     simply has no group
  🔢 TWO independent numbers: the GROUP follows the division it came
     from, the Q-Seed-<n> index runs across the whole page
  🚫 no flat Q-consumer list · 🚫 no P<n> unless it spans the whole page
```

🌱 Establishes what the seed page must contain, and the one property that separates it from everything after it.

#### 2.1 · The seed question is venue-free, and it is the only one of the three that is
(so a retarget can change the venue and the pitch without touching why the paper exists)
It is ONE paper-shaped question, and a run-on is split into a primary sentence plus a secondary boundary-condition sentence.
Venue-free is what makes it survivable: the seed is the answer a retarget must not disturb, which is exactly the fork Decision Now puts in front of you.

#### 2.2 · Motivations answers three things in order, and names its audiences
(puzzle or gap or surprise, then why now, then who cares and why)
One sentence per line, and a sentence that rests on an open question carries the join bracket plus a typed lane beneath it, which together render as the sentence's evidence card.
QB12 owns that grammar and this page does not restate it: the bracket is the join key and never fuses into a marker, the lane names what it attaches, and the chip shows the state of both.
Naming the audience is the part most often skipped, and it is what a later pitch reuses.

#### 2.3 · Landscape frames the questions and is not a related-work section
(a few lines that say where the gap is, not a survey)
It is oriented intuition at DRAFT and confirmed and woven at REVISE, sourced from the seed's own novelty and landscape probe.
Where it stakes a novelty claim, it cites the question that tests it.

#### 2.4 · Every hypothesis is hedged, because a seed states shape and not findings
(H1 carries the core, H2 and H3 carry secondary shapes, all in associational language)
A hypothesis written as a finding is the defect this rule exists to stop, since the evidence that would justify it has not been commissioned yet.
That is also why the language stays associational and names its cited enabler.

#### 2.5 · The four sections ARE the Content divisions, and any of them may raise a question
(the template anchors a question to a Seed Question, Motivations, Landscape, or H-line assertion, which is all four)
Seed Question, Motivations, Landscape, and Tentative Claim Shape are `### 1` through `### 4` of the seed page's `## Content`.
A sentence that rests on something unproven carries a `> Q-consumer:` lane and the `[Q-Seed-3]` join bracket, and that question is recorded under the Aims group carrying the number of the division the sentence sits in.
No division is privileged: a hedged H-line and a landscape gap claim raise questions the same way, and a division that raises none simply has no group, which is what QB4 §4.2.1 already allows.
So `Q-consumer` names no section at all: it is the behaviour of raising a question, and the record lives under the division that raised it.

#### 2.6 · Three parts carry a question, not one, and QB12 owns all three
(the bracket alone is bookkeeping; the lane is where the provenance actually lives)
In the sentence sits the marker and, beside it and never fused to it, the `[Q-Seed-<n>]` join bracket.
Under the sentence sits a typed lane, `> Q-consumer:` for a question and `> Citation:` or `> Value:` once an answer lands, and the pair renders as the evidence card with its state chip.
A placeholder with no bracket is a hole no question will ever fill, which is why the bracket is required rather than decorative.
This page names the parts so a stage page is not written bracket-only; the grammar itself is QB12's, and QB12a is where it is specified.

#### 2.7 · The group number and the question number are two different counters
(one says where the question came from, the other says which question it is on this page)
The group is `A<n>` where `n` is the Content division, so a question raised in Landscape is an `A3` record whatever its own index.
The `Q-Seed-<n>` index runs across the whole page and is stage-prefixed, so a cited id is never ambiguous against `Q-Claim-<n>` or `Q-Pitch-<n>`.
Reading `A3.1 · Q-Seed-7` therefore tells you both things at once: it is the first question Landscape raised, and it is the seventh raised on this page.

#### 2.8 · Questions are raised freely and dispatched narrowly
(asking is cheap; spending is not, and `probe_depth: 0` is what enforces the difference)
PROBE handles only feasibility-shaped questions; anything else stays with `Answer: deferred -> RESOURCE` and a forward pointer in the page's Log.
The loop closes at REVISE and not at PROBE: the answer is woven back into every sentence citing the bracket, and the bracket is discharged.
Born from content when DRAFT drops the bracket in, and dead into content when REVISE discharges it.

### 3 · Stage Venue

**What a venue decision owes**: a ranked pick with its rejects, and a measured blueprint.

```text
  🎯 STAGE VENUE · order 2a
  "Which venue does this paper target, and what does it REQUIRE of it?"
  📄 S-Venue-0-venue.md        🔨 draft · probe · check   ⚠️ NO revise

  📚 ## Content · four divisions        🎯 ## Aims · mirrored groups
  ─────────────────────────────         ──────────────────────────────
  ### 1 · Venue Decision         ━━▶    ### A1 · 🏛 Venue Decision
        pick + backups + the NEAREST            - A1.1 · Q-Venue-1 · …
        REJECTED + its hard disqualifier
  ### 2 · Relevant Files         ━━▶    (no group: raises nothing)
        what the decision was read from
  ### 3 · Structural Blueprint   ━━▶    ### A3 · 📐 Structural Blueprint
        per section, MEASURED, each row         - A3.1 · Q-Venue-2 · …
        carrying [source: …/style.md]
  ### 4 · Writing Principles     ━━▶    ### A4 · ✍️ Writing Principles
        the prose rules the venue imposes       - A4.1 · Q-Venue-3 · …

  🔑 ANY division may raise a question · ### 2 raises none, so it simply
     has no group
  🔢 the GROUP follows the division; the Q-Venue-<n> index runs across
     the page, stage-prefixed so a cited id is never ambiguous
  📋 record lines, 🚫 never a pipe table
```

🎯 Establishes what a venue page must decide, and why it produces a contract rather than prose.

#### 3.1 · The decision names what it rejected, not only what it picked
(a pick with no rejects cannot be reviewed, because nothing says what it was weighed against)
It gives a ranked suggestion: the pick, one or two backups with a one-line why each, and the nearest rejected outlet with its hard disqualifier.
Then it says which claim hits which of that outlet's rewards, and it carries the outlet's one-sentence desk test.

#### 3.2 · The blueprint is measured, not described
(numbers per section, each carrying the source it was measured from)
Per section it records subsections, paragraphs per subsection, sentences per paragraph, average sentence length, citation density, results detail, and which display units belong there.
Each row carries a `[source: <journal>-<section>/style.md]` anchor, so a later reader can check the measurement rather than trust it.
It also records the adaptation: how this paper's own claims map onto that section.

#### 3.3 · The blueprint is where a paper's section list comes from
(one folder per section in the playbook, transcribed here, then adapted by narrative)
A venue playbook holds one folder per section with its own measured `style.md`, and MISQ has seven: abstract, introduction, theory, methods, results, discussion, appendix.
The blueprint transcribes those, and QB2's narrative page then cuts them into the sections THIS paper writes, recording which venue section each one obeys.
That is why the blueprint carries an `Adaptation:` row: the venue says how a paper of this journal reads, and the paper says how it is cut (JL 260802).

#### 3.4 · Venue has no REVISE, and that follows from what it produces
(the one place these three stages differ in shape, and it is not an oversight)
Seed and pitch run draft, probe, revise, check; venue runs draft, probe, check.
What venue produces is a scored decision plus a transcribed blueprint, so there is no prose for REVISE to polish.
The only invariant the three share is that `phases` ends with `check`.

#### 3.5 · Relevant Files is the division that shows what an empty group looks like
(it records what the decision was read from, and reading a file raises nothing)
The other three can each raise a `Q-Venue-<n>`: the decision runs recent-publications, editor, and competing-paper checks, the blueprint can owe a measurement, and a writing principle can owe a confirmation.
`### 2` states where the evidence was read from, which is a fact about this page rather than a claim about the world, so it has no Aims group at all.
That is the shape QB4 §4.2.1 describes when it says a part with nothing left to establish simply has no group.

#### 3.6 · Records are written as lines, never as a pipe table
(the template says so twice, and it is the shape this stage's output is checked in)
Both the reward mapping and the claim-to-RQ mapping are record lines.
A table invites one-word cells, and what makes these reviewable is the reason attached to each row.

### 4 · Stage Pitch

**What a pitch owes**: the editor's-chair answer, and candidate openings that are never thrown away.

```text
  📣 STAGE PITCH · order 2b
  "Why would THIS venue's editor send this paper out for review?"
  📄 S-Venue-1-pitch.md        🔨 draft · probe · revise · check

  📚 ## Content · four divisions        🎯 ## Aims · mirrored groups
  ─────────────────────────────         ──────────────────────────────
  ### 1 · Title                  ━━▶    ### A1 · 🏷 Title
        short · specific · ≤ 15 words
  ### 2 · Hook                   ━━▶    ### A2 · 🪝 Hook
        ≥ 2 candidates, ONE move each           - A2.1 · Q-Pitch-1 · …
        Paradox · Vivid Scene · Surprising
        Fact · Stakes · Gap
        ⚠️ keep ALL, mark one as the lead
  ### 3 · Audience and Venue Fit ━━▶    ### A3 · 👥 Audience and Venue Fit
        the reader BEFORE the format            - A3.1 · Q-Pitch-2 · …
        ONE [primary] claim for THIS venue
  ### 4 · Next Evidence Move     ━━▶    ### A4 · ⏭ Next Evidence Move
        starts with a VERB, names the           - A4.1 · Q-Pitch-3 · …
        artifact it updates

  🔑 ANY division may raise a question · a division that raises none
     simply has no group
  🔢 the GROUP follows the division; the Q-Pitch-<n> index runs across
     the page, stage-prefixed so a cited id is never ambiguous
  ⚠️ a venue change re-runs ### 3, and its Aims group with it
```

📣 Establishes what the pitch page must answer, and why a venue change re-runs part of it.

#### 4.1 · The pitch is the cover letter, so it names the reader before the format
(the editor is a person with a need, and the format is what that need is expressed in)
It reads `S-Venue-0-venue.md` for the editor's-chair question and gives every primary claim a one-sentence answer to it.
That answer is a VENUE question and never an evidence question, which is the boundary this stage loses most easily.

#### 4.2 · Candidate openings are kept, never pruned
(at least two, each committing to one narrative move, with one marked as the recommended lead)
The moves are Paradox, Vivid Scene, Surprising Fact, Stakes, and Gap, and a candidate commits to exactly one.
Nothing is hidden and nothing is deleted: the author picks the lead at write time, and a rejected opening is often the right one for the next venue.

#### 4.3 · One claim is designated primary FOR THIS VENUE
(the claims themselves stay venue-neutral; only the designation is venue-shaped)
It reads the venue-neutral H1, H2, and H3, designates one as primary for this outlet, and reframes the hypotheses as venue-specific research questions, as record lines.
A venue change re-runs this section, which is the concrete half of the retargeting question this page has open.

#### 4.4 · A venue change reopens division 3, and only division 3
(the retarget question this page has open is concrete here: it is one division, not the page)
`### 3` is where the venue-neutral claims are reframed as venue-specific research questions and one is designated `[primary]`, so a change of outlet re-runs it and reopens whatever `A3` holds.
`### 1`, `### 2`, and `### 4` survive a retarget: a title, a set of candidate openings, and the next evidence move are not venue-shaped.
That is the pitch half of the fork sitting in Decision Now, stated at the division that actually moves.

#### 4.5 · The hook must land for a newcomer, and the risks are capped at three
(a plain paragraph for someone with no background, and only the highest-risk weaknesses)
The plain-language paragraph runs four to six short sentences: a framing sentence, the puzzle, the method in plain words, the surprising finding, and why it matters plus who could use it.
Weaknesses are limited to the top three highest-risk, because a longer list reads as thoroughness and buries the ones that would actually stop a desk decision.
Every point ties to a table, display, model, check, or source, and a planned one is marked planned.

### 5 · What the paper board shows

**The group a reader opens**: what this concern looks like on a real paper, and what is in it that no stage made.

```text
  📋 0-lifecycle/board.md  ── the PAPER's own board, grouped by concern
  ### Delivery · Opening (includes Venue)
        "Fix why the paper exists, who it is for, and which venue
         contract governs every downstream unit."
        📄 S-Seed-0-seed.md        ← stage seed  0     ✅ expected
        📄 S-Venue-0-venue.md      ← stage venue 2a    ✅ expected
        📄 S-Venue-1-pitch.md      ← stage pitch 2b    ✅ expected
        📄 S-Venue-2-narrative.md  ← stage narrative 3 ⚠️ Work's since 260802
        🗑 S-Venue-3-decisions.md  ← RETIRED 260802, not replaced

  🔑 THREE kinds of page can sit in a concern group
     📄 one per runs:once stage      seed · venue · pitch
     📑 N when a stage is per-unit   section-edit ━▶ S-Main-0 … S-Main-8
     🗂 a family control page        S-Main-Dash · S-Appendix-0-control
  🚫 "one stage, one page" holds one way only: every stage makes a page,
     not every page comes from a stage
  🚫 no central decision register ── a decision sits on the page that owns it
```

📋 Establishes what this concern is expected to look like on a paper's own board, measured against the MISQ paper.

#### 5.1 · The concern is the group, and the family is not
(a page's `S-<Family>` prefix says which family wrote it, never which group it appears under)
`0-lifecycle/board.md` groups by Delivery concern, so `### Delivery · Opening (includes Venue)` is this page's counterpart on a real paper.
The families cut across it: `S-Seed-1-literature.md` is family Seed and appears under `Delivery · Literature`, and `S-Venue-2-narrative.md` is family Venue and belongs to Work.
Reading a filename tells you the family and tells you nothing about the group.

#### 5.2 · A decision sits on the page that owns it, and nowhere else
(JL retired the central register on 260802, so the group has no page outside the three kinds)
The MISQ paper kept `S-Venue-3-decisions.md`, a register of rulings more than one page had to follow.
It is retired and not replaced: a decision is a `Decision Now` row in the States of the stage page it belongs to, and a ruling that binds several pages takes the Law of one of them while the others cite it.
That leaves one live gap in the Opening group, `S-Venue-2-narrative.md`, which moved to Work on 260802 and which the paper board has not caught up with.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · Venue is read as part of Opening rather than as a later peer group.
  **Done when:** no page on this board files Venue as its own Delivery concern, and `## Pages` shows Opening followed directly by Work.
- A1.2 · Opening stays separable from the manuscript Introduction.
  **Done when:** this page carries no guidance on writing §1 prose, and QB6 owns every such sentence.
- A1.3 · The arc is owned by Work rather than by Opening.
  **Done when:** no page on this board lists narrative under Opening, and QB2 names it in its own contract.

### A2 · 🌱 Stage Seed
- A2.1 · The seed question stays venue-free, so a retarget never has to touch it.
  **Done when:** no seed page on any paper names an outlet, and a venue change leaves `S-Seed-0` unedited.
- A2.2 · Every hypothesis on a seed page is hedged.
  **Done when:** no H-line on a seed page is phrased as a finding, and CHECK can say so without judgement.
- A2.3 · Each stage template numbers its sections as Content divisions, and records a raised question under the matching Aims group.
- A2.4 · A sentence resting on an open question carries the lane and the card, not the bracket alone.
  **Done when:** the three templates ask for a typed lane beneath the sentence as well as the join bracket, and QB12a stays the only page specifying that grammar.
  **Done when:** the three templates write `### 1` to `### 4` for their sections and `A<n>.<m>` for a question raised in division `n`, retiring the flat `Q-consumer` list and reserving `P` for a target that spans the page.

### A3 · 🎯 Stage Venue
- A3.1 · A venue decision records what it rejected, not only what it picked.
  **Done when:** every venue page carries the pick, its backups, and the nearest rejected outlet with the hard disqualifier that ruled it out.
- A3.2 · The structural blueprint is measured rather than described.
  **Done when:** every blueprint row carries a `[source: …/style.md]` anchor a reader can check.

### A4 · 📣 Stage Pitch
- A4.1 · Candidate openings are kept rather than pruned.
  **Done when:** a pitch page shows at least two candidates, one marked as the recommended lead, and no earlier candidate has been deleted.
- A4.2 · Exactly one claim is designated primary for the target venue.
  **Done when:** a pitch page names one `[primary]` claim, and a venue change re-runs that designation rather than inheriting it.

### A5 · 📋 What the paper board shows
- A5.1 · The live Opening group holds only pages this concern owns.
  **Done when:** `S-Venue-2-narrative.md` sits under `Delivery · Work` on the MISQ paper, matching the 260802 ruling.
- A5.2 · Every page in the group has a declared owner, whether or not a stage made it.
  **Done when:** the group holds only the three kinds in `§5`, and no page sits outside them.
- A5.3 · The five rulings the retired register held are re-homed before it is deleted.
  **Done when:** each of D01, D05, D11, D15 and D16 sits in the Law of one page it binds, or in a `Decision Now` row if it is still open, and only then does the file go.

### P · 🏁 Page-level
- P1 · Retargeting a paper to a different venue has defined consequences for the answers it does not change.
  **Done when:** a ruling says which of the three a venue change reopens, and this page carries it in `## Law` with the options it rejected.
- P2 · These three divisions cannot silently disagree with the templates they restate.
  **Done when:** a mechanical check compares each division against its `template.md` and reports a rule this page missed.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · JL ruled the sequence on 260729: Opening includes Venue. `## Pages` lists QB1 Opening then QB2 Work, and no Venue group exists on the board.
- ✅ A1.2 · The Scope paragraph names QB6 Main as the owner of the Introduction, and no §1 prose guidance appears on this page.
- ✅ A1.3 · Done 260802 on JL's ruling. Narrative left for QB2, and `board.md`'s Board Map row now reads Seed, Venue, and Pitch.

### A2 · 🌱 Stage Seed
- 🔨 A2.1 · Written into `§2.1` from `0-seed/template.md`'s own rule. Whether any live seed page obeys it has not been checked.
- 🔨 A2.2 · Written into `§2.4`. The template states it as a RULE comment that the author deletes, so nothing verifies it after the page is filled.
- ⬜ A2.4 · Not started, and this page had the same gap until 260802: `0-seed/template.md` asks only for the trailing bracket, so a seed page written to it carries a join key with no lane and no card.
- 🧠 A2.3 · Waiting on the paper family, and it is a real conflict rather than a gap. All three templates write a raised question as `- P<n> · Q-<Stage>-<n>` in one flat block, while their own rule says each question is anchored to a specific assertion. Once those assertions are numbered divisions, the anchor already names the group, so the record is `A<n>.<m>` and `P` goes back to meaning page-level. The templates predate the 260802 `A<n>` ruling, when the prefix was still `C<n>`.

### A3 · 🎯 Stage Venue
- 🔨 A3.1 · Written into `§3.1` from the Venue Decision rule. The MISQ venue page has not been read against it.
- 🔨 A3.2 · Written into `§3.2`. The blueprint's `[source:]` anchor is in the template; no check resolves it.

### A4 · 📣 Stage Pitch
- 🔨 A4.1 · Written into `§4.2` from the Hook rule, which says keep all candidates and hide none.
- 🔨 A4.2 · Written into `§4.3`. That a venue change re-runs the designation is the concrete half of the fork in Decision Now above.

### A5 · 📋 What the paper board shows
- 🧠 A5.1 · Waiting on JL. The MISQ `Delivery · Opening` group still lists the narrative page, and the choice is one row, on QB2's Decision Now, because Work is the group that gains it.
- ✅ A5.2 · Ruled by JL on 260802 with option B: the register is retired and not replaced. `§5` now lists three kinds, and the Law carries the ruling with the option it rejected.
- ❄️ A5.3 · Held while we work the design board. The register still holds five rulings and two of them are open, so deleting the file before they are re-homed would lose them. This thaws when we turn to the MISQ paper.

### P · 🏁 Page-level
- ✅ P1 · Ruled by JL on 260802, directly rather than through QA6: a retarget reopens the pitch and leaves the seed. The ruling with its rejected options is in `## Law`, and QB1 `§4.3` already carries the pitch half, since a venue change re-runs the primary-claim designation.
- ⬜ P2 · Not started, and it is this page's weak point. Three divisions restate three `template.md` files, so a rule added to any of them leaves this page quietly wrong and nothing reports it.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order and the Board Map row naming Seed, Venue, and Pitch; changing what this concern holds means editing it
- `QB2-work.md` · the concern that took the arc, and the only other page that has to agree with this one
- `../QBv-venue-packs/QBv1-misq.md` · the venue KNOWLEDGE group opened 260802, one page per venue target; it cites this page's ruling and owns no part of the decision

📥 **Input files** · what the work reads

- `../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml` · declares seed, venue, and pitch as separate stages, which is exactly what this concern groups
- `../../paper/1-lifecycle/haipipe-paper-stage/stages/0-seed/stage.md` · the seed contract, and `0-seed/template.md` beside it, which fixes that page's sections
- `../../paper/1-lifecycle/haipipe-paper-stage/stages/2a-venue/stage.md` · the venue contract, and `2a-venue/template.md` beside it
- `../../paper/1-lifecycle/haipipe-paper-stage/stages/2b-pitch/stage.md` · the pitch contract, and `2b-pitch/template.md` beside it
- `../QC-engine/QC2-stage-contract.md` · owns what a stage IS; `### 2` here only records what these three declare

## Law

- **Opening is Seed plus Venue plus Pitch** (JL 260729).
  Venue is not a separate Delivery group.
  Rejected: keeping Venue as its own concern, because that made the paper read as though it chose a journal after deciding what it argued.
- **Narrative belongs to Work, not to Opening** (JL 260802: "I think the narrative should go to the Work as well").
  An arc is built from the claim ledger, so it cannot be honest before the ledger is.
  Rejected: leaving narrative here, and cutting the concern at Work so that venue, pitch, and narrative became a fourth group; JL chose the move instead.
- **A venue change reopens the pitch and leaves the seed** (JL 260802, answering Decision Now with "A").
  Why a paper exists does not change with the journal; what it promises is shaped by one.
  Rejected: re-gating the whole concern on every retarget, because that reopens a seed nobody intended to change; and reopening nothing automatically, because two papers retargeted the same way would then end in different states.
- **There is no central decision register; a decision lives on the stage page that owns it** (JL 260802: "we will delete it, and will not use it anymore. The decision will be in each stages' Decision").
  `S-Venue-3-decisions.md` is retired and not replaced.
  Rejected: keeping it for the rulings that bind several pages at once, which was CC's recommendation on the ground that a cross-page rule has no single owner; JL ruled that one queue beats two, and that a shared rule takes the Law of a page it binds.
- **Reading order, never an execution graph**: this grouping does not renumber stages and it does not replace their explicit dependency graph.

## Lesson

- 🔧 **A replacement without an assert is a silent no-op that reports success** (260802).
  Two rulings were announced as written into `## Law` and neither had landed: both anchors had been reworded by an earlier repair in the same session, so the replace matched nothing and returned the text unchanged.
  Every other edit that day carried `assert t.count(old) == 1`, and every one of those landed.
  A write with no assertion is not a write, and a page that CLAIMS a record exists must be read back before the claim is made.

- 🗣 **A Decision Now row must be readable in ONE pass by a weak English reader** (JL 260802: "I didn't get your question after one read").
  The first version of the row below stacked three abstract nouns into its question and hung four clauses off one `Why now`.
  The rule QB4 states for the Opening paragraph applies here with more force, because this is the one section that ASKS the reader to act.
  Write short sentences. Use numbers. Name the real file. Say what each option costs in one line.

## Glossary

- **Opening**: the lifecycle contract that decides why the paper exists and where it goes, and states what it promises.
- **Pitch**: what the paper promises a reader of this venue, which is a different thing from the seed, which is why it exists at all.

## Log

260802 · The `QBv · Venue Packs` group opened, and this page kept the decision. The split is knowledge against decision: a pack's `-> Claims`, `-> Display`, `-> Minimap`, and `-> Write/Edit` maps reach four other Delivery concerns, so the knowledge sits outside all of them, while the pin stays on `S-Venue-0` and stays this page's. The 260729 ruling is cited by the QBv group intro, not reopened.
260802 · JL: say what the paper board is expected to show. `### 5` added, measured against the MISQ paper's `0-lifecycle/board.md`: the concern is the GROUP there, three stage pages are expected in it, and two more are present that this concern does not own. It also records the four kinds of page a group can hold, since "one stage, one page" holds only in the stage-to-page direction. A5.1 and A5.2 carry the two live gaps.
260802 · JL: the bracket is not the whole story, check the QB12 series. `§2.2` said a sentence carries its question id in a trailing bracket and stopped there, which is half the grammar: QB12a specifies marker plus join bracket IN the sentence and a typed lane UNDER it, rendering together as the evidence card. New `§2.6` names the three parts and points at QB12 rather than restating it, and A2.4 opens on the templates, which ask for the bracket alone.
260802 · Corrected a claim this page made and QB2 disproved: `§1.3` said there was no `S-Venue-2`, but narrative declares `board_family: Venue` and `board_unit: 2`, so unit 2 exists and belongs to Work.
260802 · QB1's own `## Diagram` brought onto the same logic. It still showed the pre-restructure three-box view and said nothing about the structure `§2` to `§4` now establish, so it draws the three pages side by side with their divisions mirrored into Aims groups. The shape is stated ONCE at the top, which is what lets each stage division below talk about what is true only of it.
260802 · Venue and Pitch brought onto the same logic as Seed: each figure now maps its four sections to `### 1`-`### 4` of that page's Content and to the mirrored `A<n>` groups, with `Q-Venue-<n>` and `Q-Pitch-<n>` able to come from any of them. Two division-specific facts came out of drawing them: venue's `### 2 · Relevant Files` raises nothing and is the concrete case of a part with no group, and a venue change reopens pitch's `### 3` alone rather than the whole page.
260802 · JL: in theory a `Q-Seed-<n>` can come from ANY division, not only the claim shape. The figure showed a record under one group alone, which read as a restriction; it now shows one under each, says a division raising none simply has no group, and `§2.6` separates the two counters, since the group number follows the division while the `Q-Seed-<n>` index runs across the page.
260802 · JL sharpened it again: the four template sections ARE the Content divisions, so a `Q-Seed-<n>` raised in `### 2` is recorded as `A2.<m>`, and the number is the join. That dissolves `Q-consumer` entirely: it names a behaviour, not a section and not a flat list. The same model is stated for venue and pitch, and A2.3 now asks all three templates for it rather than only the seed.
260802 · JL: Q-consumer belongs in Aims. `§2`'s figure listed it as a fifth Content section of the seed page, which is exactly what `0-seed/template.md` forbids and what QB4's Log records moving out of Content on 260725. The figure now shows the four Content parts feeding `## Aims`, `§2.5` states the rule, and `§2.6` keeps the raise-and-dispatch behaviour. A2.3 opened for a conflict the alignment exposed: the template's `P<n>` id form contradicts QB4 §4.2.1.
260802 · Content restructured on JL's correction: one division PER STAGE, not one division holding all three. `### 2 · Stage Seed`, `### 3 · Stage Venue`, and `### 4 · Stage Pitch` each say what that stage's page is expected to contain, written from its own `template.md` rules; the mechanical facts the three share collapsed into `#### 1.3`. Aims and States gained mirrored A2, A3, and A4 groups, and the drift risk moved to P2.
260802 · Added a per-stage division on JL's ask: per stage, the one question it asks, the S page it resolves to, its phases, and the sections its template requires. Three facts came out of writing it, none of which was stated anywhere on the board: the three stages land in TWO families, venue alone has no REVISE because it produces a contract rather than prose, and all three run at `probe_depth: 0`, which is why one gate at CHECK is enough. A2.3 records the drift risk, since the table restates four template files and nothing compares them.
260802 · Rewritten against `QB4-overall.md` as of 02:28. Law now carries each ruling with its person, date, JL's own words, and the option rejected (§5.2.6, §7.1.2); Files regrouped by action into Contracts and Input files and repointed at what an editor would actually touch (§6.1.1, §6.2.2); `#### 1.2`'s heading rewritten for the weak-English test; a good/bad pair given its own line in Writing Style; the on-stage paragraph rewritten to the question-terms-difficulty-decision shape.
260802 · JL ruled narrative into Work. This concern is now Seed plus Venue plus Pitch, and the Law, the Diagram, the contract table, and A1.3 record the move.
260802 · Brought onto `QB4-overall.md`'s current requirements: `### Decision Now` moved to the top of States in the six-field shape, and P1 changed from ❄️ to 🧠, because waiting on QA6 is waiting on something outside this page.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260729 · JL placed Venue inside Opening.
