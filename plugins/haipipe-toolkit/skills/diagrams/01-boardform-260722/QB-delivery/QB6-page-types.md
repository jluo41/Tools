# Page · the types: Q · for-stage · for-section · for-venue · for-skill mirror · for-meeting · for-literature · for-value · for-display · for-design · for-slide, and what admits a new one
state: 🟡 IN PROGRESS · seven types admitted and built 260805, base at 0.21.0; the nesting row and the checker debt (`§5`) are the open work
owner: JL
method: keep one shared structural core per shape, admit a type only on a structural or typed-record delta, and rule the list here rather than on the lifecycle page

## Opening
How many Page Types exist, what admits a new one, and what does each admitted type own?
A Page Type is the stable half of a Page: resolved from the filename or a declared marker, it decides how the Page closes and which typed records it fills.
The list is growing: JL proposed three new types on 260805, and the admission question outgrew the lifecycle page it was parked on.
This page owns the list of types, the admission test, and the layering rule that keeps two types from restating one structure.

**Where this page sits**: `QB4` owns the Page's SPACE, the seven sections.
`QB5` owns the Page's TIME, the four phases and RUN.
This page owns the third list the base keeps: WHICH stable Page shapes exist at all.

**The terms**: a TYPED RECORD is a record only one type fills, such as a citation binding on a Literature topic or a value-with-provenance binding on a Value topic.
The STRUCTURAL CORE is anatomy shared by several types and stated once, such as the topic register with nested entries.
The TRANSLATION LAYER is what one route adds over a shared core: the language its questions go out in and the typed records its answers come back as.

**Where the worked examples live**: this page LISTS the types; the `QBt` group SHOWS each one written out, one page per type, stating only what that type adds over `QB4`. `QBt3-for-display` was the first, written 260806, and eight of the ten now exist: `QBt1` stage, `QBt2` venue, `QBt3` display, `QBt4` literature, `QBt5` value, `QBt6` section, `QBt9` slide, `QBt10` design. Only `for-skill` and `for-meeting` have no specimen; QBt7 and QBt8 are unused numbers rather than missing files, and Decision Now asks whether that gap stays.

**What this page does not own**: the phase contracts under `page-phases/` are `QB5`'s.
The entry anatomy itself stays in `haipipe-board/ref/topic-entry-contract.md`, and each family's bank vocabulary stays in that family's projection.

## Diagram

**The two shelves and the list**: types are the stable axis; this page owns the left shelf's list.

```text
  📄 haipipe-board-page                  the base and router
  ├── 📁 page-types/    ◀ THIS PAGE      📁 page-phases/     ◀ QB5
  │                                        draft · probe · revise · check
  │   SHIPPED                 CONTRACT
  │   Q  decision             base only
  │   S  stage                for-stage
  │   QBv venue               for-venue
  │   Skill · Agent mirror    for-skill
  │   Literature topic        for-literature ┐ ADMITTED 260805 · two types
  │   Value topic             for-value      ┘ over ONE loaded topic core
  │   Display unit            for-display      closes on human ACCEPTANCE
  │   Section unit            for-section      loads for-stage · the venue join
  │   Meeting                 for-meeting      talk recorded, ruled elsewhere
  │   Slide deck              for-slide        live ?preview=N embed per division
  │   Design brief            for-design       division = candidate · closes on SELECTION
  │
  │   REJECTED   for-main: one family's region
  │   OPEN       the nesting row: do the two shelves move INSIDE the base?
```

## Content

### 1 · The list today: twelve types, ten contracts

**What ships now**: the filename or a declared marker decides the type, and ten loadable contracts ship under `page-types/`.

```text
  type            resolved by            closes when                contract
  ─────────────────────────────────────────────────────────────────────────────
  Q  decision     Q<group><n>-<slug>     every Aim met or held      base only
  S  stage        S-<Family>-<unit>      its human gate passes      for-stage
  QBv venue       QBv<n>-<slug>          desk rules recorded        for-venue
  Skill mirror    Skill-<n>-<slug>       the unit ships             for-skill
  Agent mirror    Agent-<n>-<slug>       the unit ships             for-skill
  Literature      head route: outward    every row supported,       for-literature
  topic                                  deferred, or withdrawn
  Value topic     head route: inward     every claim bound to a     for-value
                                         run, deferred, withdrawn
  Display unit    one unit's folder      a person accepts the       for-display
                                         render
  Section unit    per-unit stage +       its own gate, judged       for-section
                  section_kind           against the venue floor
  Meeting         Meeting-<n>-<slug>     faithful + decisions       for-meeting
                                         routed · NEVER counted
  Slide deck      one page per deck,     a person accepts the       for-slide
                  division per slide     deck for the talk
  Design brief    the page states a      a SELECTION record names   for-design
                  brief; one division    the winner and each
                  per candidate          loser's disposition
```

⚙️ Establishes the baseline this page grows from, and the two gaps it already shows.

#### 1.1 · One type ships without a contract
(the Q page leans on the base alone; Meeting's gap closed 260805)
A Q page is the base's home case, so the base doubling as its contract is a choice rather than an accident.
`Meeting-<n>` is generated by `cli/meetingpage.py` and shipped unruled until `for-meeting` closed that gap (`§3.4`).
The one remaining gap does not block the list question, and it is recorded here so it stops being invisible.

#### 1.2 · One structure was enforced before any contract taught it
(the checker held the shape first; the admission closed the gap)
`src/topic_entry_contract.py` enforces the evidence-page shape today: a `route: outward|inward` key in a direct page's head, one `### E<n>` division per QA-probe below `probes/` (four fixed slot headings on each QA-probe), and the standing `E0` queue.
Until the topic types shipped, no loadable contract taught a writer that same shape.
The machine holding a rule the skill list did not state was the strongest standing argument for admitting the topic types, and the two route contracts now load the core that states it.

### 2 · The admission test: five questions, all must pass

**When a candidate earns a folder**: the counterpart to `QB5 §7.2`'s split test, for the Type axis.

```text
  ① STRUCTURAL DELTA     the base does not already provide it        (QB5 §8.1, Law)
  ② SELF-RESOLVING       filename or a declared marker on the page
                         identifies the type with no session memory
  ③ HOST-AGNOSTIC NAME   names a shape or a direction, never one
                         family's section
  ④ OWN CLOSING RULE     or its own typed records; either suffices
  ⑤ CHECKER-ENFORCEABLE  a machine can catch a page breaking it
```

🧪 Establishes the gate every candidate below was measured against.

#### 2.1 · The name test is about direction, not vocabulary policing
(Literature and Value pass it; Main does not)
"Literature" and "Value" read as paper words, but both families probe both banks, so the two names mark evidence DIRECTIONS: outward toward published knowledge, inward toward produced results.
A direction is host-agnostic.
"Main" names one family's manuscript region, which no other family has, and that is why it fails ③ while the other two pass.

#### 2.2 · Self-resolution may use a marker, not only a filename
(the checker already trusts one)
`S-Literature-1` and `S-Value-6` share the `S-<Family>-<unit>` filename shape, so the filename alone cannot separate them from a plain stage page.
The head `route:` line can, and `src/topic_entry_contract.py` keys on exactly that signal (the retired register marker played this role until 260806).
Admitting a type on a declared head key follows the machine's own precedent rather than inventing a second resolution rule.

### 3 · The queue: six admitted and built, one rejected

**Where each candidate stands**: measured against `§2`, with the ruling collected in Decision Now.

```text
  candidate         ①    ②    ③    ④    ⑤     standing
  ──────────────────────────────────────────────────────────────
  for-literature    ✅   ✅   ✅   ✅   ✅    ✅ ADMITTED + built 260805
  for-value         ✅   ✅   ✅   ✅   ✅    ✅ ADMITTED + built 260805
  for-display       ✅   ✅   ✅   ✅   ✅    ✅ ADMITTED + built 260805
  for-section       ✅   ✅   ✅   ✅   ✅    ✅ ADMITTED + built 260805, loads for-stage
  for-meeting       ✅   ✅   ✅   ✅   ✅    ✅ ADMITTED + built 260805
  for-design        ✅   ✅   ✅   ✅   ✅    ✅ ADMITTED + built 260805
  for-main          ❌   ✅   ❌   ❌   —     ❌ rejected: one family's region
```

🧭 Establishes the per-candidate verdicts and the one open dependency.

#### 3.1 · Literature and Value are separate types by their typed records
(JL 260805: "I still want to separate for-literature and for-value")
The two routes share one anatomy and differ in everything the anatomy carries.
A Literature register row carries a positioning stake and its answer becomes a citation binding: a real key, a positioning sentence, a novelty verdict.
A Value register row carries a claim's numeric dependency and its answer becomes a value binding: the number, its run provenance, a claim-ledger row.
The base says a type decides "which typed records it fills," so different records make different types, and the earlier one-type reading under-weighted this half.

#### 3.2 · Display waited on one prior question
(is it the mirror shape generalized, or its own structure?)
A display page mirrors a shipped unit, its float, assets and acceptance state, which is structurally what `-for-skill` already is with a different unit kind.
Ruling `-for-display` before ruling whether "mirror of a shipped unit" is ONE generalized type would risk admitting the same shape twice, the exact failure `§4` exists to prevent.
The mirror question was small and was ruled first: B, in the same breath as the admission, so `-for-display` stands alone.

#### 3.3 · Section was rejected with Main, and only Main deserved it
(the reversal, 260805, measured on the real boards)
The earlier rejection conflated two candidates: Main names one family's manuscript region, and no other family has one, so it fails the name test and stays rejected.
Section is a cross-family shape, because both the paper and application families run section-edit, and the real `S-Main-3-theory` carries a `### Venue contract` block that no plain stage page has: blueprint BINDING, style reference, override stated.
So `for-section` was admitted as a second-level variant: it loads `for-stage` for the chain and gate and adds the section kind, the venue block, and the landing surface where the three record types reach prose.
A section reads the venue BLUEPRINT and never the QBv catalog; the catalog is read once, by the venue stage (JL 260805: "for one section, we will go to check the venue-page? is that so?" ruled exactly this way).

#### 3.4 · Meeting had a generator and no contract
(the gap §1.1 recorded, closed)
`for-meeting` owns one rule: the record is faithful, in the speakers' own words, and a decision spoken in a meeting is not RULED until it lands on the page that owns the subject.
A meeting page is never counted in the settled total, exactly like a mirror.

### 4 · The layering rule: a type LOADS the core, never restates it

**How two types share one anatomy without copying it**: the same inheritance the phase contracts use.

```text
  haipipe-board-page                       the base frame
    └── ref/topic-entry-contract.md        the STRUCTURAL CORE, stated once
          ├── for-literature               + translation layer only:
          │                                  outward stake · citation records ·
          │                                  closes when positioning holds
          └── for-value                    + translation layer only:
                                             inward stake · value records ·
                                             closes when claims bind to runs
```

🔒 Establishes the guard that makes separation safe: anatomy is stated once or the types drift.

#### 4.1 · What a route contract may and may not contain
(the entry's inside is off limits to both)
Each type contract owes its reader four things: what a legal register row carries here, where its entries live, what the returned answer must become, and when the topic closes.
Neither may restate the register or entry anatomy, because a copied rule goes a night out of date while the core moves.
Neither may touch the entry's inside, the Q-executor and A-executor, which stay language-free because that wall is what keeps the bank from learning which answer would be convenient.

### 5 · The checker debt: ⑤ was claimed ten times and implemented three

**What the admission test promised against what the checker holds**: every admitted candidate got a ✅ on ⑤ CHECKER-ENFORCEABLE, and most of those checks do not exist.

```text
  contract            checker coverage today
  ─────────────────────────────────────────────────────────────
  for-skill           REAL            managed spans, checked
  for-stage           PARTIAL         contract span + hash; not the venue block
  for-literature ┐    ANATOMY ONLY    topic_entry_contract.py checks the shape,
  for-value      ┘                    never the routes or the typed records
  for-slide           PARTIAL         embed counts as figure; bindings unchecked
  for-meeting         EXEMPTIONS ONLY never-counted; fidelity, routing unchecked
  for-venue           NOTHING
  for-display         NOTHING
  for-design          NOTHING
  for-section         NOTHING
```

🧾 Establishes the gap between the admission test's ⑤ answers and the checker that exists, and specs the ten rules that would close it.

#### 5.1 · The ten missing rules, one line each
(the spec the next checker pass implements; owned here until each ships)
1. Type resolution first: exactly one key claims each page, in the base's ①-⑤ order, before any per-type rule runs.
2. Design: a page past its gate carries a SELECTION record, and every non-winning division carries a disposition line.
3. Display: an ACCEPTED row is dated, and every shown number names a value binding or a producing run by path.
4. Slide: every division's embed targets the one deck file with `?preview=N#sN` and carries an acceptance row.
5. Literature: every register row sits in a terminal state, and every citation binding's key resolves in the bibliography.
6. Value: every value binding's run, specification, and QA paths exist on disk.
7. Section: the `### Venue contract` block is present with blueprint, style, and override lines, and the blueprint path resolves.
8. Venue: the three figures appear in their fixed order, and every desk fact carries a provenance stamp.
9. Meeting: every decision-shaped line points at where it landed or is marked not-yet-routed.
10. Stage: the page declares venue-free or venue-aligned, and a venue-aligned page's `style-from:` resolves to a venue-pinned upstream page.

#### 5.2 · Why the debt is recorded rather than repaid here
(⑤ was answered about what a machine COULD catch, not what one catches)
The queue in `§3` answered ⑤ as a possibility question, and every candidate passes that reading.
The cost of the shortcut is that a page can violate its type contract today and no build reports it.
Recording the ten specs here means the next ✅ on ⑤ must name the rule it ships with, and A5 below holds the page open until then.

### 6 · The Log pattern per type: same four authorities, different events

**The grammar is QB4's and appears exactly once**: `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`, PHASE from DRAFT · PROBE · REVISE · CHECK, actor from the comment-protocol id table, bare `[<actor>]` legal only for meaning-preserving housekeeping, and doubt resolves to a phase tag (JL 260805, the "every change is one of D P R C" ruling).
What a TYPE owns is none of that; a type owns which EVENTS its typed record makes worth a line.
The rung, the binding, the selection are line TEXT; the authority stays one of four.

#### 6.1 · for-stage, the full trace a stage page walks

```text
birth      [CC]        page created by create-page.py; shell only, and the Log
                       section itself does not exist until this first line
round 1    [DRAFT-CC]  round 1: promise set · Content scaffold authored · P-holes raised
           [PROBE-CC]  P1 ⏳ → probes/L1-<topic>/<n>-<slug>.md   Q-executor out, stake stays here
           [PROBE-CC]  P1 answer landed: A-consumer written HERE, A-executor stays on the QA-probe
           [REVISE-CC] answer woven into Content; its [Q-<Stage>-1] bracket discharged
           [CHECK-CC]  declared checker green + cold read → routes CLOSE
           [CHECK-JL]  gate: state ✅ GATED
maintain   [CC]        stage.py sync regenerated the managed span (meaning-preserving)
reopen     [DRAFT-CC]  `requires:` changed, or a venue retarget: the promise moved, round 2 opens
```

PROBE is the one authority that legally writes two pages in one act, so its lines land on both: the focal page's line above, and the evidence page's own `[PROBE-CC] dispatched, working since <date>` / `answered → <QA path>` pair (a QA-probe is a record, not a page, and carries no Log of its own; its owning E division's page logs on its behalf).

#### 6.2 · The other nine, one pattern line each

```text
for-venue      [REVISE-CC] desk fact updated, provenance stamped · [CHECK-JL] venue PINNED
for-skill      [REVISE-CC] mirror synced to <skill> vX.Y.Z · [CHECK-JL] accepted at ship
for-literature [DRAFT-CC] Q-consumer collected into E0 (the stake) · [PROBE-CC] promoted to
               E<n>, QA-probe ⏳ · [PROBE-CC] citation binding written, consumer row →
               SUPPORTED · [CHECK-CC] every E<n> terminal, E0 empty → CLOSE
for-value      the same voice with the value binding: row → BOUND only when run, spec,
               and QA paths resolve on disk
for-display    the acceptance ladder IS the pattern: [DRAFT-CC] ① requested · [PROBE-CC]
               ② sourced, producing run named · [REVISE-CC] ③ rendered · [CHECK-JL]
               ④ accepted THIS render · [REVISE-CC] ⑤ placed · a re-render after ④ logs
               [REVISE-CC] back to ③, because acceptance was of a render, not a name
for-slide      for-display's ladder at beat grain: accept rows per beat, deck-wide gate last
for-section    for-stage's trace PLUS the venue events: [DRAFT-CC] retarget rewrote the
               venue contract block · [REVISE-CC] a landed binding reached its owing sentence
for-meeting    [CC] spoken decision captured, not yet ruled · [REVISE-CC] routed → owning
               page · [CHECK-CC] every decision line routed → CLOSE
for-design     [DRAFT-CC] brief: audience + candidates A/B/C · [REVISE-CC] candidate B
               rewritten · [CHECK-JL] SELECTION: B; A archived, C parked, dispositions on
               the same line, and a losing division is never silently deleted
```

#### 6.3 · Where the patterns live
Each `page-types/*/SKILL.md` gets a three-to-five line "Log pattern" block, EXAMPLES in that type's own vocabulary, never a restatement of the grammar; the grammar ships once, in the base's Log obligation.
Execution rides the paused Log pass (grammar paragraph + renderer + the QB4 P-row trim), so A6 below holds this page open until the blocks exist.

## Aims

- [x] 🗣 Is `for-slide` admitted: one page per deck, one Content DIVISION per slide, each embedding its rendered slide?
      📍 JL proposed it 260805: the page calls `display/skills/html-ppt`, each slide is built from its slide section, and the render is embedded in the division.
      🔔 `Why now` it passes the five-part test on paper (structural delta: division = render unit, which no type has; host-agnostic; closes on acceptance like display), and one mechanical fact must be settled first: `build.py` STRIPS JS from every rendered page, so an embedded slide must be static HTML/CSS, an `<img>`/`<object>` by path, or an iframe to an asset file, never a live JS deck.
      ⭐ `A ·` admit as a sibling of `for-display` sharing its acceptance ladder: division-per-slide, embed-by-path into the division, per-slide render binding (division ↔ rendered file ↔ source recipe), deck order = reader order; the outline chain from `for-section` pages stays the family's (paper-slides → html-ppt).
      `B ·` no new type: a deck is ONE display unit under `for-display`, and slides stay inside its folder.
      🛑 `Blocks` writing the contract; the JS-stripping constraint must be stated in it either way.
      🤖 `If nobody answers` decks stay family convention, embedded nowhere.
      ✅ `Ruled A` JL 260805, by branching the session to Page-for-Slide and saying "go ahead and focusing on the slide." Built the same day at `page-types/haipipe-board-page-for-slide` 0.1.0, base at 0.18.0 with nine variants. The contract's first stated rule was the JS constraint: the division embeds the PNG export, the live html-ppt deck stays a linked artifact with its runtime intact.
      ✅ `Corrected same day` by JL's follow-up ruling ("what I am thinking is that you will embed the html in the content division") and its proof `QA4`: the division embeds the deck LIVE via html-ppt's `?preview=N` single-slide mode, one file for both surfaces. The strips-JS premise was FALSE: `build.py` only asserts pages stay readable with scripts off, and never rewrites an iframe's file. Contract corrected at 0.2.0 with the wrong premise recorded in place.

- [x] 🗣 Is `for-design` admitted: one page per design BRIEF, one division per CANDIDATE?
      📍 JL defined it 260805 (his words, translated: "we want to design some messages, say message A, B, C for one group of people; the Content divisions ARE the different messages"): the page is the brief, who it is for and what it must do, and each Content division IS one candidate artifact, side by side.
      🔔 `Why now` the shape already exists unruled in two places: the application family designs channel messages per cohort, and the paper family's display units keep `candidates/` folders (display01b has one on disk). Nothing rules how candidates sit on a page or how one is chosen.
      ⭐ `A ·` admit: page = brief · division = candidate (the artifact itself + its rationale + fit to the brief's criteria) · Aims = the brief's criteria · closes on a SELECTION record naming which candidate won, why, and each loser's disposition (dropped · kept for A/B test · merged). Sits UPSTREAM of for-display: design selects the candidate, display accepts its render. An earlier reading of for-design (the Decision Now row grammar) was CC's misreading; that gap is real but belongs to the base, not to this type.
      `B ·` no type: candidates stay a folder convention inside display units and application artifacts.
      🛑 `Blocks` writing the contract.
      🤖 `If nobody answers` candidates stay folder convention, selection stays undocumented.
      ✅ `Ruled A` JL 260805, his definition on this board deciding it: page = brief, division = candidate. The contract shipped the same day at `page-types/haipipe-board-page-for-design` 0.1.0, base at 0.19.0 with a ten-variant table; its one hard rule is that a losing candidate keeps its division with its disposition, because the rationale for NOT choosing is part of the design record.

- [ ] 🗣 Do `page-types/` and `page-phases/` move INSIDE `haipipe-board-page/`, with the variant mirrors folding under Skill-3 on QCskill?
      📍 JL proposed it 260805 ("could we just put the skill of page-for-xxxx under haipipe-board-page?"); it would revise `QB5 A8.1`'s ruling that the two shelves sit BESIDE the base.
      ⭐ `A ·` nest both folders inside `haipipe-board-page/`. The base becomes a folder that is a skill AND a container, Skill-3's mirror tree then shows every variant and phase, and the redundant Skill-6/Skill-8 mirrors retire to `_archive/`. Costs one path migration (20+ references) and an `install.sh` recursion check.
      `B ·` keep the shelves beside the base and only STOP minting new mirrors per variant, so QCskill stays flat but small.
      🛑 `Blocks` moving any folder, retiring any mirror.
      🤖 `If nobody answers` the shelves stay where QB5 A8.1 put them.

### A1 · ⚙️ The list today: twelve types, ten contracts
- A1.1 · The list is recorded here with its two contract gaps named.
  **Done when:** the base's Page Types section and this page agree, and a change to either is a diff on both.

### A2 · 🧪 The admission test: five questions, all must pass
- A2.1 · The five-part test is the ruled gate for every future candidate.
  **Done when:** the next candidate is measured against ①-⑤ on this page before any folder is created.

### A3 · 🧭 The queue: six admitted and built, one rejected
- A3.1 · The Literature and Value types ship as separate contracts over one loaded core.
  **Done when:** `page-types/haipipe-board-page-for-literature/` and `-for-value/` exist, each loads `ref/topic-entry-contract.md` rather than restating it, and the checker still reports the same topic findings on the MISQ board.
- A3.2 · The mirror question is ruled before any display contract is written.
  **Done when:** a ruling records whether "mirrors a shipped unit" is one generalized type or `-for-display` stands alone.

### A4 · 🔒 The layering rule: a type LOADS the core, never restates it
- A4.1 · No admitted type contract duplicates the shared anatomy.
  **Done when:** grep finds the register and entry heading rules stated in exactly one file under `board/`.

### A5 · 🧾 The checker debt: ⑤ was claimed ten times and implemented three
- A5.1 · Every ⑤ claim in the queue is backed by a shipped checker rule, or the coverage table in `§5` stays the admitted truth.
  **Done when:** `cli/check.py` implements the ten rules specced in `§5.1`, or each still-missing rule is re-marked in `§5` with the reason it waits.

### A6 · 📜 The Log pattern per type: same four authorities, different events
- A6.1 · Every type contract carries its own "Log pattern" block, examples in its vocabulary, with the grammar stated once in the base.
  **Done when:** the base's Log obligation carries the `[PHASE-actor]` grammar and all ten `page-types/*/SKILL.md` carry a pattern block matching `§6`.

## States

### Decision Now

- [ ] 🗣 Does the `QBt` lane renumber to close its gaps, or keep them and say what they are for?
      📍 QBt7 and QBt8 were never used: no file, no `_archive/` entry and no `## Links` row anywhere under `skills/` carries either id, so the lane runs 1 to 6 and then 9 to 10 with nothing recording what the two numbers were held for.
      🔔 `Why now` `board.md`'s `QD` block rules the opposite for its own lane, that a lane is renumbered to close its gaps, on the stated reason that a reader cannot tell a gap from a missing page (JL 260801). Two lanes on one board answer the same question two ways, and the `for-skill` and `for-meeting` specimens are the next two pages to be numbered.
      `A ·` renumber `QBt9` and `QBt10` down to QBt7 and QBt8, which obeys the `QD` ruling board-wide and costs every citation of those two ids plus one `## Links` row each.
      ⭐ `B ·` keep the numbers and RESERVE QBt7 and QBt8 for `for-skill` and `for-meeting`, stated on the roster, which costs no rename and answers the `QD` ruling's actual worry by naming what each gap holds.
      `C ·` keep the gaps and say nothing, which is the state this pass found and the one a reader cannot read.
      🛑 `Blocks` numbering the two unwritten specimens.
      🤖 `If nobody answers` the roster line added on 260806 stands, the gap is visible, and the two numbers stay unclaimed.

- [x] 🗣 Which new Page Types are admitted to `page-types/`?
      📍 `A3` owns the queue; the row moved here from `QB5` on 260805 because the list outgrew the lifecycle page.
      🔔 `Why now` the topic shape already ships in the checker (`src/topic_entry_contract.py`) with no loadable writer contract, and the engine's own docstring states the boundary: "The Board engine never names a consumer family such as Paper, Literature, or Value."
      `A ·` admit ONE structural type, `-for-topic`; Literature and Value stay its two paper instances and the translation layers live family-side.
      `B ·` admit the family-named four (`-for-literature`, `-for-value`, `-for-display`, `-for-main`): one contract per family name, at the cost of two byte-similar topic contracts and a section-named type.
      `C ·` admit none: overlays stay family-side and the checker remains the only authority on the topic shape.
      ⭐ `D ·` admit `-for-literature` and `-for-value` as SEPARATE types that both LOAD one shared topic core, each adding only its translation layer (JL 260805: "I still want to separate for-literature and for-value"). `-for-display` queues behind the mirror question; `-for-main` and `-for-section` are rejected.
      🛑 `Blocks` writing any new `page-types/` contract.
      🤖 `If nobody answers` nothing is written, and the topic shape stays checker-only.
      ✅ `Ruled D, plus display` JL 260805: "how about the -for-literature, and -for-values, and -for-display, I want to include them as well." Built the same day: three contracts under `page-types/`, the base at 0.16.0 lists six variants, and the two topic types load `ref/topic-entry-contract.md` rather than restating it.

- [x] 🗣 Is "mirrors a shipped unit" one generalized type, or does `-for-display` stand alone?
      📍 `A3.2` owns this; it gates the display admission only.
      `A ·` generalize: one mirror type whose unit kind varies (skill folder, agent file, display unit), with `-for-skill` becoming its first projection.
      `B ·` keep `-for-skill` as is and admit `-for-display` as its own type, accepting two mirror-shaped contracts.
      🤖 `If nobody answers` neither changes and display pages stay governed by `-for-stage` plus family convention.
      ✅ `Ruled B` JL 260805, by admitting display in the same breath as the topic types. The contract records the difference that keeps them apart: a Skill mirror closes when its unit SHIPS, a display page closes when a person ACCEPTS a specific render.

- [x] 🗣 Is `for-slide` admitted: one page per deck, one Content DIVISION per slide, each embedding its rendered slide?
      📍 JL proposed it 260805: the page calls `display/skills/html-ppt`, each slide is built from its slide section, and the render is embedded in the division.
      🔔 `Why now` it passes the five-part test on paper (structural delta: division = render unit, which no type has; host-agnostic; closes on acceptance like display), and one mechanical fact must be settled first: `build.py` STRIPS JS from every rendered page, so an embedded slide must be static HTML/CSS, an `<img>`/`<object>` by path, or an iframe to an asset file, never a live JS deck.
      ⭐ `A ·` admit as a sibling of `for-display` sharing its acceptance ladder: division-per-slide, embed-by-path into the division, per-slide render binding (division ↔ rendered file ↔ source recipe), deck order = reader order; the outline chain from `for-section` pages stays the family's (paper-slides → html-ppt).
      `B ·` no new type: a deck is ONE display unit under `for-display`, and slides stay inside its folder.
      🛑 `Blocks` writing the contract; the JS-stripping constraint must be stated in it either way.
      🤖 `If nobody answers` decks stay family convention, embedded nowhere.
      ✅ `Ruled A` JL 260805, by branching the session to Page-for-Slide and saying "go ahead and focusing on the slide." Built the same day at `page-types/haipipe-board-page-for-slide` 0.1.0, base at 0.18.0 with nine variants. The contract's first stated rule was the JS constraint: the division embeds the PNG export, the live html-ppt deck stays a linked artifact with its runtime intact.
      ✅ `Corrected same day` by JL's follow-up ruling ("what I am thinking is that you will embed the html in the content division") and its proof `QA4`: the division embeds the deck LIVE via html-ppt's `?preview=N` single-slide mode, one file for both surfaces. The strips-JS premise was FALSE: `build.py` only asserts pages stay readable with scripts off, and never rewrites an iframe's file. Contract corrected at 0.2.0 with the wrong premise recorded in place.

- [ ] 🗣 Do `page-types/` and `page-phases/` move INSIDE `haipipe-board-page/`, with the variant mirrors folding under Skill-3 on QCskill?
      📍 JL proposed it 260805 ("could we just put the skill of page-for-xxxx under haipipe-board-page?"); it would revise `QB5 A8.1`'s ruling that the two shelves sit BESIDE the base.
      ⭐ `A ·` nest both folders inside `haipipe-board-page/`. The base becomes a folder that is a skill AND a container, Skill-3's mirror tree then shows every variant and phase, and the redundant Skill-6/Skill-8 mirrors retire to `_archive/`. Costs one path migration (20+ references) and an `install.sh` recursion check.
      `B ·` keep the shelves beside the base and only STOP minting new mirrors per variant, so QCskill stays flat but small.
      🛑 `Blocks` moving any folder, retiring any mirror.
      🤖 `If nobody answers` the shelves stay where QB5 A8.1 put them.

### A1 · ⚙️ The list today: twelve types, ten contracts
- ⬜ A1.1 · Not started as a synced pair; this page's table was copied from the base at 0.15.0 on 260805.

### A2 · 🧪 The admission test: five questions, all must pass
- ⬜ A2.1 · The test is drafted here and not yet cited by the base.

### A3 · 🧭 The queue: six admitted and built, one rejected
- ✅ A3.1 · Ruled D and built 260805: both contracts exist under `page-types/`, each loads the core by path and states only its route's dictionary; no checker code changed.
- ✅ A3.2 · Ruled B 260805: `-for-display` stands alone, and its contract names the shipping-against-acceptance difference that keeps it off `-for-skill`.

### A4 · 🔒 The layering rule: a type LOADS the core, never restates it
- ⬜ A4.1 · Holds today by accident rather than by rule: the anatomy lives once in `ref/topic-entry-contract.md` and once in the paper projection, which names paths rather than restating headings.

### A5 · 🧾 The checker debt: ⑤ was claimed ten times and implemented three
- ⬜ A5.1 · Recorded 260805; the ten rules are specs only, and the coverage table in `§5` states what the checker holds today: one real coverage, two partials, the topic anatomy, and meeting's counting exemption.

### A6 · 📜 The Log pattern per type: same four authorities, different events
- ⬜ A6.1 · Specced 260805 in `§6` on JL's ask ("could we have each page type and how the logging patterns will change along the way"); no contract carries a pattern block yet, and execution rides the paused Log pass.

## Files

### Contracts

- `../../../board/haipipe-board-page/SKILL.md` · the base whose Page Types section this page grows
- `../../../board/page-types/haipipe-board-page-for-stage/SKILL.md` · the stage type the topic types sit beside
- `../../../board/page-types/haipipe-board-page-for-skill/SKILL.md` · the mirror shape the display question measures against
- `../../../board/haipipe-board/ref/topic-entry-contract.md` · the structural core both topic types would load

### Input files

- `QB-delivery/QB5-page-loop.md` · the Type-against-Phase axis split and the admission law this page extends
- `../../../paper/haipipe-paper/probe/topic-entry-contract.md` · the paper projection showing what a family layer adds (moved 260805, thin-paper phase 2)

### Checks

- `../../../board/haipipe-board/src/topic_entry_contract.py` · enforces the topic shape the admitted types would teach
- `../../../board/haipipe-board/cli/check.py` · catches source and rendering violations on this Page

## Law

- 260806 · JL · Evidence pages organize BY EXECUTOR: one Content division per Q-executor conversation (E<n>), consumers collected under it, E0 incoming queue; one division ↔ one QA-probe; many QA-probes ↔ one QA-bank. Files are QA-bank and QA-probe; slot words are the four capitals Q-consumer/A-consumer/Q-executor/A-executor; the type key is the head route: line.

## Log

- 260806 · [REVISE-CC] the Opening's worked-example line was frozen at "`QBt3-for-display` is the first", written when one specimen existed. `ls QBt-page-types/` returns eight pages, so the line now names all eight and leaves only `for-skill` and `for-meeting` unbuilt. A grep for QBt7 and QBt8 across `skills/` returns nothing, so those two numbers were never used; the gap contradicts the renumbering rule `board.md`'s `QD` block states for its own lane, and the new first Decision Now row asks JL which rule `QBt` follows.
- 260806 2109 · [REVISE-CC] swept to the 260806 architecture; base 0.21.0 in the state line, §1's Literature/Value rows re-keyed to the head `route:` line with the duplicate Meeting row dropped, §1.1/§1.2/§3.2 closed gaps moved to past tense, §6 traces moved to QA-probe and E-division vocabulary with capital slot words
- 260806 1000 · [REVISE-CC] JL's evidence-page ruling executed end to end: the type key moved to the head `route:` line (base 0.21.0, resolution step ②), for-literature/for-value 0.4.0 rewrote the flat `### Q-consumer register` into E<n> divisions with `#### consumers` + `#### answer digest` and the E0 queue, the core contract + checker re-keyed (head route, capital slot headings canonical, 1:1 division↔QA-probe link), templates reshaped (entry-template.md renamed qa-probe-template.md), chips re-anchored to E divisions, and the MISQ S03/S04 eight pages migrated with 28 QA-probes intact; checker baseline held at 11 ERRORs.
- 260806 0100 · [DRAFT-CC] §6 opened with A6: the per-type Log patterns, on JL's ask; for-stage's full trace in §6.1, the nine others in §6.2, the placement rule (examples in each type contract, grammar once in the base) in §6.3. The QB4-owned grammar and the paused Log pass are cited, not restated; the dead workers/ path in Input files repointed to paper/haipipe-paper/probe/ (phase 2 move).
260805 · The checker debt recorded as `§5` with its own Aim (A5.1, ⬜). The admission test's ⑤ was answered ✅ for every candidate, while the checker actually ships one real coverage (for-skill's managed spans), two partials (the stage contract span + hash, the slide embed-as-figure rule), the topic anatomy only, and meeting's counting exemption; venue, display, design, and section have nothing. The ten missing rules are specced one line each in `§5.1`, type resolution first. The same review pass landed across the contracts: the base's one resolution table for all types (0.20.0) with the REQUIRED `route:` register line and `page-type:` frontmatter keys, the core's new Register route line and Register-row states sections, the topic pair de-parallelized into their own voices (0.2.0 each), and patch fixes on section, display, design, slide, and stage.
260805 · `for-design` RULED A and built the same day. JL's definition decided it: the page is the brief, and the Content divisions ARE the different messages, one per candidate carrying the artifact, its rationale, and its fit to the brief's criteria. The contract ships at `page-types/haipipe-board-page-for-design` 0.1.0 and the base at 0.19.0 with a ten-variant table. It sits UPSTREAM of `for-display`, design selecting the candidate and display accepting its render; the page closes on a SELECTION record naming the winner, why, and each loser's disposition (dropped · kept for A/B test · merged), and a losing division is never silently deleted.
260805 · `for-slide`'s embed rule CORRECTED by its first real page. JL rejected the PNG design ("plase try it yourself... you will embed the html in the content division") and demanded proof over discussion. Built `QA4` on this board: seven divisions, each embedding the ONE deck file live via html-ppt's `?preview=N` single-slide mode, verified by driving a real Chrome (slides render live in the divisions; a click plus ArrowRight flips the bare deck). The 0.1.0 premise "`build.py` strips JS" was FALSE: the build only asserts pages read with scripts off, and never touches an iframe's file. Contract at 0.2.0 with the wrong premise recorded in place; the engine gained `![alt](x.html)` live-iframe embeds (`src/body.py`), an existence-based reroot for authored html (`src/page_board.py`), and media-embed-counts-as-figure in `cli/check.py`.
260805 · `for-slide` RULED A and built, on the Page-for-Slide branch. One page per deck, division = slide, and the slide binding (division · source · render · acceptance) as its typed record. The design's one load-bearing constraint came from reading the builder and the renderer together: html-ppt ships a live JS runtime and a headless PNG export, and `build.py` strips JS, so the board embeds the PNG and the browser gets the deck. Two surfaces, one source.
260805 · Second admission the same day (JL: "what I want is also for-venue, for-meeting, for-stage... and also for-section (connecting with for-venue)", thought against the paper skill board and the MISQ paper board): `for-section` and `for-meeting` built, the base at 0.17.0 with an eight-variant table. The section admission reverses `§3.3`'s earlier verdict with the measurement that decides it, and `for-stage`'s "different formats" question resolved without new types: the three shapes (stage page, unit page, dash page) are already `for-stage`'s own section, and per-stage variation lives in `stage.md` plus `template.md`, which is the stage-contract mechanism's whole job.
260805 · Both rows RULED and executed in one message (JL: "I want to include them as well"): D for the topic pair, B for display. Three contracts built under `page-types/`, the base bumped to 0.16.0 with a six-variant table, and the title now carries the full list. The same message raised the next structural question, recorded above as the nesting row: whether the two shelves move inside `haipipe-board-page/` itself.
260805 · Created after JL asked whether Page Types deserve their own Q. Measured against `QB5 §7.2`'s split test: the list question is independent of the lifecycle question, it needs its own Aims and States, it closes on a list ruling rather than a gate or a loop, and its continuation files are the `page-types/` contracts themselves. The admission Decision Now row moved here from `QB5` with option D starred, and the mirror question was split out as its own row because it gates only the display admission. The five-part admission test in `§2` extends `QB5 §8.1`'s one-line law with the self-resolution, naming, closing-rule and enforceability questions the candidates were actually measured against.
