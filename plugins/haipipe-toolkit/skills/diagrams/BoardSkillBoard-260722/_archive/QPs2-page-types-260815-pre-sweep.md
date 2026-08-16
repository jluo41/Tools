# Page · the types: Q · for-stage · for-section · for-venue · for-skill mirror · for-meeting · for-literature · for-value · for-display · for-design · for-slide, and what admits a new one
state: 🟡 IN PROGRESS · seven types admitted and built 260805, base at 0.21.0; the open work is the nesting row, the checker debt (`§5`), and the on-disk shapes (`§7`) that no contract states yet
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

**Where the worked examples live**: this page LISTS the types; the `QBt` group SHOWS each one written out, one page per type, stating only what that type adds over `QB4`. `QBt3-for-display` was the first, written 260806, and eight of the ten now exist: `QBt1` stage, `QBt2` venue, `QBt3` display, `QBt4` literature, `QBt5` value, `QBt6` section, `QBt9` slide, `QBt10` design. `QBt7` and `QBt8` are RESERVED for `for-skill` and `for-meeting` (ruled B, 260807), so the lane keeps 1 to 10 rather than renumbering.

The group is also more than illustration, and `§7` says why: a page type owns FOLDERS AND FILES, the ten contracts between them name six artifact paths, and a specimen is the only form of this page that can be missing a file. `QPs-page-structure/` is therefore a stage folder carrying its own `_fixture/` paper root, and the real scripts run against it.

**What this page does not own**: the phase contracts under `page-phases/` are `QB5`'s.
The entry anatomy itself stays in `haipipe-board/ref/topic-entry-contract.md`, and each family's bank vocabulary stays in that family's projection.

## Diagram

**The two shelves and the list**: types are the stable axis; this page owns the left shelf's list.

```text
  📄 haipipe-page                  the base and router
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
  haipipe-page                       the base frame
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
1. ✅ SHIPPED 260806 · Type resolution first: exactly one key claims each page, in the base's ①-⑤ order, before any per-type rule runs. `cli/check.py check_page_type`, three findings: `page-type-unknown` a value step ③ does not define, `page-type-twice` two claims on one page, `page-type-conflict` a `route:` and a `page-type:` on the same page where ② resolves first and the ③ key is dead text. Blast radius measured before shipping: 2 findings board-wide, both the QBt1/QBt2 keys already sitting in Decision Now, and 0 on the other three boards including the live MISQ lifecycle.
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

### 7 · Every page has an INPUT folder and an OUTPUT: one rule, ten types

**The list says what each type IS and never said what each type READS and WRITES**: read off the live MISQ paper rather than off the contracts, because the contracts do not say. A grep for `float.tex`, `preview.`, `assets/`, `candidates/`, `QA-probe/`, `sections/`, `.bib`, `.cls` and `.bst` across all ten `page-types/*/SKILL.md` returns six mentions in total, and seven of the ten return zero, `for-display` among them.

A page is a unit of work, so it takes something in and hands something out. That is the same IPO shape the task family already runs on, which is why this is one rule rather than ten:

```text
  📥 INPUT    what this page READS to do its job. Raw material a person
              collected, or the product of a run. Either a folder beside the
              page, or a RECORD pointing at a bank that lives elsewhere.
  📤 OUTPUT   what this page HANDS to someone else. Generated, and never
              hand-edited: fix the input or fix the generator.
```

```text
  type         📥 INPUT                             📤 OUTPUT
  ───────────────────────────────────────────────────────────────────────────────
  display      display/<page>/                      displays/<page>/
                 source · candidates · assets ·       float.tex + assets/,
                 float · preview · README             and nothing else
  slide        slide/<page>/                        slides/<page>/deck.html
  literature   QA-probe/<page>/                     <paper>.bib      GENERATED
                 + the keys it claims from a bank      from claims + \cite
  value        QA-probe/<page>/                     <record>.data/*.csv
                 + <record>.data/source/              parsed from the record's
                 the producing run                    own fence, never retyped
  venue        venue/<page>/                        the blueprint every section
                 the desk's own rules, recorded       binds to · .cls + .bst
                 from a shared playbook               copied to the paper root
  meeting      meeting/<page>/                      decisions ROUTED onto the
                 recording · transcript · what        page that owns each subject
                 was shown
  section      ✗ no folder: the material IS this    sections/<nn>_<slug>.tex
                 page's own Content prose             FLAT, reader-ordered name
  design       ↗ the downstream unit's own          a SELECTION record, and the
                 candidates/                          winner promoted into assets/
  skill        ↗ the skill folder it mirrors        ✗ the unit ships itself
  stage        ↗ its upstream pages' provides       its own provides
```

**Every page has an input. The only question is whether the folder is local.** Six types keep it beside the page; three read a folder someone else owns and keep a RECORD pointing at it; one, section, has no folder because its raw material is the prose on the page itself.

That split is not new and does not need its own vocabulary: it is QA-bank against QA-probe, already ruled for literature, now stated for all ten. The bank lives outside and is shared; the page keeps only what it claims, and never a copy. The word MIRROR, ruled on `§3.2` for `for-skill`, names exactly the three types whose input folder is elsewhere.

📦 Establishes what a page of each type reads and writes, which no contract states today and which the `QBt` group has to build before it can claim to show a type.

#### 7.1 · The specimen group is a stage folder that carries its own paper root
(so the ten specimens run the real scripts rather than a copy of them)
`QPs-page-structure/` plays S03, S04, S05, S06 and S08 at once: it holds the ten pages and their authoring companions, `display/`, `slide/` and `QA-probe/`, and no scripts.
What a stage folder cannot hold is the paper root it ships TO, which on a real paper is `../..`, so the group carries `_fixture/` for it: `sections/`, `displays/`, `slides/`, the generated `.bib`, the venue `.cls` and `.bst`, and a small `.tex` that compiles.
The name and the wiring are the sibling board's, `../PaperSkillBoard-260725/board.md:5` declaring `paper-root: _fixture` under the discipline its README states, the same code path and the same failure modes. One rule differs and is stated in ours: prose lives in this fixture, because here the shipped `.tex` IS the specimen, where there the fixture holds only what a marker resolves against.

#### 7.2 · Two facts about the SECTION shape that a natural guess gets wrong
(both measured on the live paper, and the first was guessed wrong in this pass before it was checked)
`find sections appendices -type d` returns only the two roots, so a section file never gets a subfolder and the paper's hierarchy is not carried by the filesystem.
The mapping is not one to one and the shipped filename never carries the board page id: eight `S-Main-*` pages against fourteen files in `sections/`, with `S-Main-4-measurement.md` shipping `04_personality_extraction.tex`.
The only `\input` inside a section file reaches a DISPLAY float, `sections/05_data_variables.tex:166` naming `displays/S-Display-3c-variable-operationalization/float.tex`, and that one line is the only place the A2 and A1 shapes touch.

#### 7.3 · The display stage tools belong to the BOARD engine, not to one paper and not to one family
(found while deciding whether the specimen group keeps its own copy)
`build-displays.py`, `display-report.py` and `asset-manifest.py` existed exactly once each in the whole repo, inside the MISQ paper's `0-lifecycle/S05-display/`, so a second paper wanting displays had to hand-copy them or reinvent them.
All three anchored on `Path(__file__)`, which is exactly WHY they had to sit inside the stage; the anchor is now a positional stage directory defaulting to the working directory, and the rules live once in `src/display_unit.py`.
The home is `board/haipipe-board/cli/`, not the paper family (JL 260807, on the ground that display is not paper-only and the application family has a display stage of its own). Three things on the board side already agreed before the question was asked: `src/dialect_paper.py` is a board module that already resolves `displays/` and `float.tex`; `cli/refs.py` is already a board command that WRITES and already takes a `<paper-root>` argument; and `page-type: display` is a board key, so the type that owns these artifacts was never paper-scoped either.
A copy in the specimen group would be copy number two and would drift, and a fixture that runs a different file from the paper proves nothing about the paper.

## Aims

- [x] 🗣 Is `for-slide` admitted: one page per deck, one Content DIVISION per slide, each embedding its rendered slide?
      📍 JL proposed it 260805: the page calls `display/skills/html-ppt`, each slide is built from its slide section, and the render is embedded in the division.
      🔔 `Why now` it passes the five-part test on paper (structural delta: division = render unit, which no type has; host-agnostic; closes on acceptance like display), and one mechanical fact must be settled first: `build.py` STRIPS JS from every rendered page, so an embedded slide must be static HTML/CSS, an `<img>`/`<object>` by path, or an iframe to an asset file, never a live JS deck.
      ⭐ `A ·` admit as a sibling of `for-display` sharing its acceptance ladder: division-per-slide, embed-by-path into the division, per-slide render binding (division ↔ rendered file ↔ source recipe), deck order = reader order; the outline chain from `for-section` pages stays the family's (paper-slides → html-ppt).
      `B ·` no new type: a deck is ONE display unit under `for-display`, and slides stay inside its folder.
      🛑 `Blocks` writing the contract; the JS-stripping constraint must be stated in it either way.
      🤖 `If nobody answers` decks stay family convention, embedded nowhere.
      ✅ `Ruled A` JL 260805, by branching the session to Page-for-Slide and saying "go ahead and focusing on the slide." Built the same day at `page-types/haipipe-page-for-slide` 0.1.0, base at 0.18.0 with nine variants. The contract's first stated rule was the JS constraint: the division embeds the PNG export, the live html-ppt deck stays a linked artifact with its runtime intact.
      ✅ `Corrected same day` by JL's follow-up ruling ("what I am thinking is that you will embed the html in the content division") and its proof `QA4`: the division embeds the deck LIVE via html-ppt's `?preview=N` single-slide mode, one file for both surfaces. The strips-JS premise was FALSE: `build.py` only asserts pages stay readable with scripts off, and never rewrites an iframe's file. Contract corrected at 0.2.0 with the wrong premise recorded in place.

- [x] 🗣 Is `for-design` admitted: one page per design BRIEF, one division per CANDIDATE?
      📍 JL defined it 260805 (his words, translated: "we want to design some messages, say message A, B, C for one group of people; the Content divisions ARE the different messages"): the page is the brief, who it is for and what it must do, and each Content division IS one candidate artifact, side by side.
      🔔 `Why now` the shape already exists unruled in two places: the application family designs channel messages per cohort, and the paper family's display units keep `candidates/` folders (display01b has one on disk). Nothing rules how candidates sit on a page or how one is chosen.
      ⭐ `A ·` admit: page = brief · division = candidate (the artifact itself + its rationale + fit to the brief's criteria) · Aims = the brief's criteria · closes on a SELECTION record naming which candidate won, why, and each loser's disposition (dropped · kept for A/B test · merged). Sits UPSTREAM of for-display: design selects the candidate, display accepts its render. An earlier reading of for-design (the Decision Now row grammar) was CC's misreading; that gap is real but belongs to the base, not to this type.
      `B ·` no type: candidates stay a folder convention inside display units and application artifacts.
      🛑 `Blocks` writing the contract.
      🤖 `If nobody answers` candidates stay folder convention, selection stays undocumented.
      ✅ `Ruled A` JL 260805, his definition on this board deciding it: page = brief, division = candidate. The contract shipped the same day at `page-types/haipipe-page-for-design` 0.1.0, base at 0.19.0 with a ten-variant table; its one hard rule is that a losing candidate keeps its division with its disposition, because the rationale for NOT choosing is part of the design record.

- [ ] 🗣 Do `page-types/` and `page-phases/` move INSIDE `haipipe-page/`, with the variant mirrors folding under Skill-3 on QCskill?
      📍 JL proposed it 260805 ("could we just put the skill of page-for-xxxx under haipipe-page?"); it would revise `QB5 A8.1`'s ruling that the two shelves sit BESIDE the base.
      ⭐ `A ·` nest both folders inside `haipipe-page/`. The base becomes a folder that is a skill AND a container, Skill-3's mirror tree then shows every variant and phase, and the redundant Skill-6/Skill-8 mirrors retire to `_archive/`. Costs one path migration (20+ references) and an `install.sh` recursion check.
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
  **Done when:** `page-types/haipipe-page-for-literature/` and `-for-value/` exist, each loads `ref/topic-entry-contract.md` rather than restating it, and the checker still reports the same topic findings on the MISQ board.
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

### A7 · 📦 Every page has an INPUT folder and an OUTPUT: one rule, ten types
- A7.1 · Every type contract states its page's INPUT and its OUTPUT by path.
  **Done when:** each of the ten `page-types/*/SKILL.md` carries its own row from `§7`'s table, so the artifact-path grep returns more than the six mentions counted 260807.
- A7.4 · Every specimen page SHOWS its own input and output, rather than leaving a reader to find them.
  **Done when:** each `QBt` page's `## Diagram` draws its 📥 INPUT and 📤 OUTPUT, and its `## Files` opens with the same two paths plus a checklist for verifying each is alive.
- A7.2 · The `QBt` group is a RUNNABLE specimen: ten pages, their companions, and one `_fixture/` paper root.
  **Done when:** `build-displays.py`, `display-report.py` and `bib-from-bank.py` each run against `QPs-page-structure/` from their skill home, and `pdflatex _fixture/QBt-page-types.tex` produces a PDF carrying the `QBt3` figure through the section file that `\input`s its float.
- A7.5 · The skill is proved by APPLYING it to a real paper, not by reading it.
  **Done when:** the display layer of the live MISQ paper has been audited against `for-display`'s stated shape, every defect the audit found has been fixed in the SKILL rather than worked around in the paper, and the remaining findings are all real states a person must judge.
- A7.3 · The display stage tools have one home in the board engine and take the stage as an argument.
  **Done when:** they sit in `board/haipipe-board/cli/` over `src/display_unit.py`, the MISQ paper holds no copy, `build-displays.py --check` and `display-report.py --check` exit 0 against the MISQ stage, and every live command line in that stage's `display/README.md` and in `paper/S05-display/display/stage.md` names the new path.

## States

### Decision Now

- [ ] 🗣 Do the five paper-owned specimens move off this board, given that the `QBt` set is one interlocked build?
      📍 JL ruled on 260809 that a Page Type variant ships under the `page-types/` folder of the skill set that owns it, and created an empty `QPs-page-structure/` group on `01-haipipe-paper-260725` to hold the paper's specimens. Five of this group's eight pages now describe paper-owned types: `QBt2` venue, `QBt3` display, `QBt4` literature, `QBt5` value, `QBt6` section.
      🔔 `Why now` The five NEW paper types (four dashes plus narrative) already have specimens on the paper board as of 260809, so this group and that one now both hold paper-type specimens. Leaving it is the only state where the rule is half applied.
      ⚠️ What blocks the obvious answer: the eight pages are not independent. `_fixture/` is cited by seven of the eight and is a shared LaTeX build target; `QBt3` builds INTO `_fixture/displays/QBt3-for-display/` and cites sibling `QBt` ids 29 times; `QBt3`'s own figure prints `source: QA-probe/QBt5-for-value/1-artifact-paths`. Moving five of eight cuts a working build in half.
      `A ·` move the five pages with their named artifact folders (`venue/QBt2-*`, `display/QBt3-*`, `QA-probe/QBt4-*`, `QA-probe/QBt5-*`, `_bank/`) and give the paper board its own `_fixture`, which obeys the rule fully and costs a duplicated fixture that will drift.
      ⭐ `B ·` leave all eight here and record on both boards that this group is the INTERLOCKED SPECIMEN SET, exempt from the ownership rule because its pages share one build; the paper board's `QBt` then holds only specimens for types with no fixture coupling, which is what it holds today.
      `C ·` move the five and rewrite them to stop sharing `_fixture`, which obeys the rule and is the only option that leaves no duplication, at the cost of rebuilding five working specimens.
      🛑 `Blocks` nothing today: both groups render and check. It blocks only the claim that the 260809 ownership rule is fully applied.
      🤖 `If nobody answers` B, in 14 days, because it is the state on disk and the only one that is not half-migrated.

- [x] 🗣 Does the `QBt` lane renumber to close its gaps, or keep them and say what they are for?
      📍 QBt7 and QBt8 were never used: no file, no `_archive/` entry and no `## Links` row anywhere under `skills/` carries either id, so the lane runs 1 to 6 and then 9 to 10 with nothing recording what the two numbers were held for.
      🔔 `Why now` `board.md`'s `QD` block rules the opposite for its own lane, that a lane is renumbered to close its gaps, on the stated reason that a reader cannot tell a gap from a missing page (JL 260801). Two lanes on one board answer the same question two ways, and the `for-skill` and `for-meeting` specimens are the next two pages to be numbered.
      `A ·` renumber `QBt9` and `QBt10` down to QBt7 and QBt8, which obeys the `QD` ruling board-wide and costs every citation of those two ids plus one `## Links` row each.
      ⭐ `B ·` keep the numbers and RESERVE QBt7 and QBt8 for `for-skill` and `for-meeting`, stated on the roster, which costs no rename and answers the `QD` ruling's actual worry by naming what each gap holds.
      `C ·` keep the gaps and say nothing, which is the state this pass found and the one a reader cannot read.
      🛑 `Blocks` numbering the two unwritten specimens.
      🤖 `If nobody answers` the roster line added on 260806 stands, the gap is visible, and the two numbers stay unclaimed.
      ✅ `Ruled B` JL 260807, by approving the whole `QBt` structure with the two names already in it, saying it was the structure he wanted. The tree he approved listed `QBt7-for-skill.md` and `QBt8-for-meeting.md` with the option-B citation on the same line, so the numbers are claimed rather than renumbered and the lane keeps 1 to 10. Recorded from that approval rather than from a separate ask; the reading is stated here so the row reopens on one line if it is wrong.

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
      ✅ `Ruled A` JL 260805, by branching the session to Page-for-Slide and saying "go ahead and focusing on the slide." Built the same day at `page-types/haipipe-page-for-slide` 0.1.0, base at 0.18.0 with nine variants. The contract's first stated rule was the JS constraint: the division embeds the PNG export, the live html-ppt deck stays a linked artifact with its runtime intact.
      ✅ `Corrected same day` by JL's follow-up ruling ("what I am thinking is that you will embed the html in the content division") and its proof `QA4`: the division embeds the deck LIVE via html-ppt's `?preview=N` single-slide mode, one file for both surfaces. The strips-JS premise was FALSE: `build.py` only asserts pages stay readable with scripts off, and never rewrites an iframe's file. Contract corrected at 0.2.0 with the wrong premise recorded in place.

- [ ] 🗣 Do `page-types/` and `page-phases/` move INSIDE `haipipe-page/`, with the variant mirrors folding under Skill-3 on QCskill?
      📍 JL proposed it 260805 ("could we just put the skill of page-for-xxxx under haipipe-page?"); it would revise `QB5 A8.1`'s ruling that the two shelves sit BESIDE the base.
      ⭐ `A ·` nest both folders inside `haipipe-page/`. The base becomes a folder that is a skill AND a container, Skill-3's mirror tree then shows every variant and phase, and the redundant Skill-6/Skill-8 mirrors retire to `_archive/`. Costs one path migration (20+ references) and an `install.sh` recursion check.
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

### A7 · 📦 Every page has an INPUT folder and an OUTPUT: one rule, ten types
- ✅ A7.1 · Met 260807. All ten `page-types/*/SKILL.md` carry a `## 📥📤 What this page reads, and what it hands on` block with their own row from `§7`, real paths, and for the five that a paper actually runs, the commands. Measured with the same instrument that opened `§7`, `QA-probe/QBt5-for-value/1-artifact-paths.data/source/measure.py`: artifact-path mentions went 6 → 30 and contracts naming none went 7 → 2. The two still at zero are `meeting` and `skill`, correctly rather than owed, since neither produces a paper artifact. The aim behind it is JL's: someone updating the MISQ paper's display layer should be able to load `for-display` alone and finish, which is why that contract now carries the four commands and the rule that `displays/` is a build target.
- ✅ A7.4 · Met 260807 on JL's ask that a page and its Diagram must both state their own input folder and output folder. All eight pages state 📥 INPUT and 📤 OUTPUT in their `## Diagram`, and `QBt3`, `QBt4` and `QBt5` additionally open `## Files` with the same two paths plus a checklist for verifying each is alive.
- ⬜ A7.2 · Structure ruled by JL 260807, approving the proposed structure as the one he wanted; the group on disk still carries the shape built from contract prose (`unit.py`, an invented `out/` layer, `source/` sitting inside `displays/`, a `sections/source/`, a local copy of the shared venue folder) and `_fixture/` does not exist yet. The nested path is not a risk: `src/dialect_paper.py:1089` joins `paper-root` straight onto the board dir, so `QPs-page-structure/_fixture` resolves like any other, and this board's own build already asks for the key, reporting 7 markers rendering as plain text with no `dialect:` declared.
- ✅ A7.3 · Ruled by JL 260807 in two steps, "should it go to skills?" then "why not the board, we may use display in other applications too", and shipped the same day. The three tools sit in `board/haipipe-board/cli/` over `src/display_unit.py`, take the stage as a positional argument, and the MISQ paper holds no copy. Verified against the live paper before the copies were removed, by byte-diffing each tool's output rather than reading its own summary: `build-displays.py` left 14 of 25 shipped files identical and changed exactly two distinct lines across the other 11, both halves of the banner swap; `display-report.py` changed exactly one line; `asset-manifest.py` changed one line across 11 manifests. Uncommitted, and it lands in two repos: `Tools`, and the paper, which is its own nested submodule rather than part of `Project-Personality-OpioidRx`.
- 📍 A7.3 raised something that is NOT this board's to fix, recorded so it is not lost: `asset-manifest.py --check` reports 21 problems across the live MISQ paper, ten table bodies and figures stale against their own `source/`, and six untraceable or unreferenced files on `S-Display-2c` and `S-Display-4c`. All 21 predate the move and the retired tool reports the same list. It belongs to the paper's own display stage.

## Files

### Contracts

- `../../../../board/haipipe-page/SKILL.md` · the base whose Page Types section this page grows
- `../../../../board/page-types/haipipe-page-for-stage/SKILL.md` · the stage type the topic types sit beside
- `../../../../board/page-types/haipipe-page-for-skill/SKILL.md` · the mirror shape the display question measures against
- `../../../../board/haipipe-board/ref/topic-entry-contract.md` · the structural core both topic types would load

### Input files

- `QPw-page-workflow/QPw1-page-loop/QPw1-page-loop.md` · the Type-against-Phase axis split and the admission law this page extends
- `../../../../paper/haipipe-paper/probe/topic-entry-contract.md` · the paper projection showing what a family layer adds (moved 260805, thin-paper phase 2)
- `../PaperSkillBoard-260725/_fixture/README.md` · the `paper-root:` precedent `§7.1` follows, and the one rule it states that ours breaks
- `../../../../paper/S05-display/display/stage.md` · names the stage tool it does not hold, and the argument shape `§7.3` implements

### Checks

- `../../../../board/haipipe-board/src/topic_entry_contract.py` · enforces the topic shape the admitted types would teach
- `../../../../board/haipipe-board/cli/check.py` · catches source and rendering violations on this Page

## Law

- 260806 · JL · Evidence pages organize BY EXECUTOR: one Content division per Q-executor conversation (E<n>), consumers collected under it, E0 incoming queue; one division ↔ one QA-probe; many QA-probes ↔ one QA-bank. Files are QA-bank and QA-probe; slot words are the four capitals Q-consumer/A-consumer/Q-executor/A-executor; the type key is the head route: line.

## Log

- 260815 1730 · [REVISE-CC, JL ruled] for-slide leaves the type roster: "We will not have a page-type of slide, the slide will just be the plugin version" — every page may have one optional deck in its `slide/` plugin, ruled on `QPf3`, which is now the plugin's page. The QBt9 specimen is archived whole at `_archive/QBt9-for-slide.md`. This is the third kind reduced to material (for-skill → the `skill/` plugin, for-meeting → `meeting/`, for-slide → `slide/`), and this page's roster, figures, and admission rows still describe the pre-reduction world; the sweep is owed and named on QPf3's Aims.
- 260807 1520 · [REVISE-CC] APPLICATION step run, closing the specimen → skill → application flow JL named. The point of the step is not that the paper got fixed; it is that the real paper found four defects in the skill that the specimen could not, because the specimen has one unit and the paper has eleven with eight years of history between them. All four were the same shape: a check that was RIGHT about its rule and WRONG about its inputs. Documentation in `source/` is not an input, `.gitkeep` is not an asset, a `.png` twin of a used `.pdf` is not unused, and a generator's output is not untraceable for failing to equal its own input. One correction landed on my own first fix: excluding `REBUILD.md` left the tool reporting `source/ is empty` about folders that are not empty, so the message now says PROSE ONLY and names the note. The paper's content was not touched at all. What remains is eight real findings, three of which would change a printed figure and are therefore JL's call rather than mine, and the sharpest is that `S-Display-4c` compiles a figure older than its own `source_data.csv`.

- 260807 1420 · [REVISE-CC] A7.1 shipped, and the loop it exercises closed on itself. All ten type contracts gained an INPUT/OUTPUT block, on JL's aim that a person updating the MISQ paper should be able to load `for-display` alone and finish rather than come back to this board. The change was then MEASURED by the instrument that found the hole: 6 artifact-path mentions became 30, and 7 contracts naming none became 2. That re-measurement made `QBt5`'s own value record stale, which is the discipline the specimen exists to teach, so the record was re-measured, its CSV re-parsed and the slide deck rebuilt, and the deck's headline moved from `7 of 10` to `2 of 10` with no digit typed by hand anywhere in the chain. One correction landed in the same pass: `QBt2`'s venue was made real earlier in the day and REVERTED, because that page's own Opening gives the reason and it holds. A venue page states what a desk refuses, and a word cap or reference style that reads as real can be followed by mistake and cost a live submission; a wrong figure wastes an afternoon, a wrong desk rule loses a paper. Its journal stays invented under an RFC 2606 reserved host, and its input record now says that is a safety ruling rather than unfinished work.

- 260807 1330 · [REVISE-CC] §7 REFRAMED from "five on-disk shapes" to one rule, INPUT and OUTPUT, on JL's ask that the concept be written where it belongs and the earlier concepts folded into it. The shapes were a classification a reader had to memorise; a page is a unit of work, so it reads something and hands something out, which is the IPO shape the task family already runs on and needs no second vocabulary. Two things changed substantively rather than in wording. MEETING gains an input folder on JL's correction: a meeting reads a recording, a transcript and whatever was shown, which is collected raw material like any other, and calling it typeless was wrong. And the earlier "five types own nothing" collapsed once the question became WHERE the input folder is rather than WHETHER there is one: six types keep it beside the page, three read a folder someone else owns and keep a record pointing at it, and only `for-section` has none because its raw material is the prose on the page itself. That three-way split needs no new word: it is QA-bank against QA-probe, ruled for literature on 260806 and now stated for all ten, and MIRROR (`§3.2`) names exactly the three.

- 260807 1150 · [REVISE-CC] A7.3 shipped: the three display stage tools moved into `board/haipipe-board/cli/` over a new `src/display_unit.py`, which holds the anchor rules the three used to each derive from `__file__`. They went to `paper/S05-display/` first and JL moved them one layer out the same hour, on the ground that display is not paper-only. He is right and the board side already said so three times: `src/dialect_paper.py` is a board module that resolves `displays/` and `float.tex`, `cli/refs.py` is a board command that WRITES and takes a `<paper-root>`, and `page-type: display` is a board key. Two defects were caught during verification and both are worth recording, because both are the session's dominant failure shape, a check that shares a defective premise with the thing it checks. Dropping `import glob` while `describe()` still used it killed the relocated `asset-manifest.py`; it wrote nothing, so the A/B harness compared the ORIGINAL's output against itself and reported IDENTICAL. It was caught only because a line had been changed on purpose and the diff should not have been empty, so the harness now asserts both exit codes. The second was real behaviour: `float_targets()` stripped the unit prefix using a path that was correct only while the tool was required to run from the paper root, so once it moved, all 11 units reported `float.tex DOES NOT POINT AT assets/`. The prefix is now passed in the paper's own frame. The same class of misreading nearly landed a false alarm earlier in the pass, when a `git diff` against HEAD on `S-Display-Dash.md` looked like the table had changed and was in fact showing an earlier session's uncommitted work; an A/B between the two tools showed exactly one differing line.

- 260807 1105 · [DRAFT-CC] §7 opened with A7: what each type OWNS ON DISK, after the `QBt` specimens were found to have been written from contract PROSE rather than copied from a real instance. The five shapes (A1 UNIT · A2 SECTION · B QA-PROBE · C NONE · D MIRROR) were measured against the live MISQ paper rather than read off the contracts, because the contracts do not say: a grep for real artifact paths across all ten `page-types/*/SKILL.md` returns six mentions in total and seven contracts return zero, `for-display` among them, which is the hole a specimen finds and a prose review cannot. Two shapes moved during the pass. `for-section` separated from the unit shape when `find sections appendices -type d` returned only the two roots, and one guess was wrong on the way: the flat directory does NOT carry a tree through section-to-section `\input`, and the orphan `05-1_*.tex` splits are referenced by nothing. `for-venue` and `for-design` moved from NONE to MIRROR on JL's correction that design also delivers, which `for-design/SKILL.md:17` already supports by ruling the display unit's `candidates/` folder as its artifact home. §7.3 records a find that belongs to the paper family rather than to this board: the three display stage tools exist exactly once each in the repo, inside one paper, while `paper/S05-display/display/stage.md:11` already names one of them and already specifies the stage-directory argument none of them take.

- 260806 · [REVISE-CC] Rule 1 of §5.1 shipped, so the checker debt is 9 rather than 10. Worth recording what the measurement caught before it became a rule: a first version of the step ④ pattern demanded a digit unit and reported 25 of the live MISQ paper's 59 pages as claimed by no key. The board was fine; the pattern was wrong. Real units there are `Pitch`, `Seed`, `C`, `C0`, `R1`, `1a` and `Dash`, so the unit segment is alphanumeric and the slug is optional. Shipping the first version would have put 25 false findings on JL's paper, which is how a checker stops being read.

- 260806 · [REVISE-CC] the Opening's worked-example line was frozen at "`QBt3-for-display` is the first", written when one specimen existed. `ls QPs-page-structure/` returns eight pages, so the line now names all eight and leaves only `for-skill` and `for-meeting` unbuilt. A grep for QBt7 and QBt8 across `skills/` returns nothing, so those two numbers were never used; the gap contradicts the renumbering rule `board.md`'s `QD` block states for its own lane, and the new first Decision Now row asks JL which rule `QBt` follows.
- 260806 2109 · [REVISE-CC] swept to the 260806 architecture; base 0.21.0 in the state line, §1's Literature/Value rows re-keyed to the head `route:` line with the duplicate Meeting row dropped, §1.1/§1.2/§3.2 closed gaps moved to past tense, §6 traces moved to QA-probe and E-division vocabulary with capital slot words
- 260806 1000 · [REVISE-CC] JL's evidence-page ruling executed end to end: the type key moved to the head `route:` line (base 0.21.0, resolution step ②), for-literature/for-value 0.4.0 rewrote the flat `### Q-consumer register` into E<n> divisions with `#### consumers` + `#### answer digest` and the E0 queue, the core contract + checker re-keyed (head route, capital slot headings canonical, 1:1 division↔QA-probe link), templates reshaped (entry-template.md renamed qa-probe-template.md), chips re-anchored to E divisions, and the MISQ S03/S04 eight pages migrated with 28 QA-probes intact; checker baseline held at 11 ERRORs.
- 260806 0100 · [DRAFT-CC] §6 opened with A6: the per-type Log patterns, on JL's ask; for-stage's full trace in §6.1, the nine others in §6.2, the placement rule (examples in each type contract, grammar once in the base) in §6.3. The QB4-owned grammar and the paused Log pass are cited, not restated; the dead workers/ path in Input files repointed to paper/haipipe-paper/probe/ (phase 2 move).
260805 · The checker debt recorded as `§5` with its own Aim (A5.1, ⬜). The admission test's ⑤ was answered ✅ for every candidate, while the checker actually ships one real coverage (for-skill's managed spans), two partials (the stage contract span + hash, the slide embed-as-figure rule), the topic anatomy only, and meeting's counting exemption; venue, display, design, and section have nothing. The ten missing rules are specced one line each in `§5.1`, type resolution first. The same review pass landed across the contracts: the base's one resolution table for all types (0.20.0) with the REQUIRED `route:` register line and `page-type:` frontmatter keys, the core's new Register route line and Register-row states sections, the topic pair de-parallelized into their own voices (0.2.0 each), and patch fixes on section, display, design, slide, and stage.
260805 · `for-design` RULED A and built the same day. JL's definition decided it: the page is the brief, and the Content divisions ARE the different messages, one per candidate carrying the artifact, its rationale, and its fit to the brief's criteria. The contract ships at `page-types/haipipe-page-for-design` 0.1.0 and the base at 0.19.0 with a ten-variant table. It sits UPSTREAM of `for-display`, design selecting the candidate and display accepting its render; the page closes on a SELECTION record naming the winner, why, and each loser's disposition (dropped · kept for A/B test · merged), and a losing division is never silently deleted.
260805 · `for-slide`'s embed rule CORRECTED by its first real page. JL rejected the PNG design ("plase try it yourself... you will embed the html in the content division") and demanded proof over discussion. Built `QA4` on this board: seven divisions, each embedding the ONE deck file live via html-ppt's `?preview=N` single-slide mode, verified by driving a real Chrome (slides render live in the divisions; a click plus ArrowRight flips the bare deck). The 0.1.0 premise "`build.py` strips JS" was FALSE: the build only asserts pages read with scripts off, and never touches an iframe's file. Contract at 0.2.0 with the wrong premise recorded in place; the engine gained `![alt](x.html)` live-iframe embeds (`src/body.py`), an existence-based reroot for authored html (`src/page_board.py`), and media-embed-counts-as-figure in `cli/check.py`.
260805 · `for-slide` RULED A and built, on the Page-for-Slide branch. One page per deck, division = slide, and the slide binding (division · source · render · acceptance) as its typed record. The design's one load-bearing constraint came from reading the builder and the renderer together: html-ppt ships a live JS runtime and a headless PNG export, and `build.py` strips JS, so the board embeds the PNG and the browser gets the deck. Two surfaces, one source.
260805 · Second admission the same day (JL: "what I want is also for-venue, for-meeting, for-stage... and also for-section (connecting with for-venue)", thought against the paper skill board and the MISQ paper board): `for-section` and `for-meeting` built, the base at 0.17.0 with an eight-variant table. The section admission reverses `§3.3`'s earlier verdict with the measurement that decides it, and `for-stage`'s "different formats" question resolved without new types: the three shapes (stage page, unit page, dash page) are already `for-stage`'s own section, and per-stage variation lives in `stage.md` plus `template.md`, which is the stage-contract mechanism's whole job.
260805 · Both rows RULED and executed in one message (JL: "I want to include them as well"): D for the topic pair, B for display. Three contracts built under `page-types/`, the base bumped to 0.16.0 with a six-variant table, and the title now carries the full list. The same message raised the next structural question, recorded above as the nesting row: whether the two shelves move inside `haipipe-page/` itself.
260805 · Created after JL asked whether Page Types deserve their own Q. Measured against `QB5 §7.2`'s split test: the list question is independent of the lifecycle question, it needs its own Aims and States, it closes on a list ruling rather than a gate or a loop, and its continuation files are the `page-types/` contracts themselves. The admission Decision Now row moved here from `QB5` with option D starred, and the mirror question was split out as its own row because it gates only the display admission. The five-part admission test in `§2` extends `QB5 §8.1`'s one-line law with the self-resolution, naming, closing-rule and enforceability questions the candidates were actually measured against.
