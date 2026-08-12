<!-- TEMPLATE · ONE VALUE EVIDENCE PAGE, AND THE RECORDS IT POINTS AT.
     Copy this file to the evidence page's own path and fill it. The paper family files it as
     `0-lifecycle/S04-value/S-Value-<n>-<topic>.md`; another family uses its own id, and the
     filename is NOT what makes this a value page (see the first RULE below).
     DELETE every RULE comment as you satisfy it. A RULE comment never ships in the filled page.
     PART 2, at the bottom, is the QA-probe record. It is a DIFFERENT FILE, and that whole block
     is deleted from the page once the records exist.

     LOAD THREE THINGS BEFORE WRITING. This template states only what the INWARD ROUTE adds.
       the page frame     board/haipipe-page/SKILL.md
       the E anatomy      board/haipipe-board/ref/topic-entry-contract.md
       this route         board/page-types/haipipe-page-for-value/SKILL.md
     Section order, the Opening blank-line split, the 520-character ceiling, figure captions,
     Aim ids and `Done when`, Decision Now, and the folds all belong to the BASE. They bind this
     page and are not repeated here. Read the base; do not infer it from this file.

     WHAT THIS PAGE IS. A VIEW over N atoms, never an atom itself. Each `### E<n>` division points
     at one QA-probe record, and the RECORD is the thing that has a product. That is why this page
     declares no `provides:` line. A display page is the opposite shape: it IS its atom and does
     declare one.

     WHAT THIS PAGE IS NOT. It does not hold anything that is not one executor conversation:
       the claim ledger the numbers serve       -> the claims stage page (S-Work-C on a paper)
       the rule every value topic obeys         -> the topic's control page (S-Value-Dash)
       the answer's full text                   -> the QA-probe record, then the QA-bank
       the run that produced the number         -> the executor tree, never copied in
       a question about published knowledge     -> an outward page (`route: outward`)
       the render that draws the number         -> the display page that binds the product
     There is no second register. Which consumer waits on which number is READ off the
     `#### consumers` blocks, never maintained as a separate map.

     THE MECHANICAL GATE, and it is real code, not a review habit:
       python3 <board>/cli/check.py <board-folder> | grep '^<PAGE>'
     `src/topic_entry_contract.py` switches on only when the head carries `route: inward` or
     `route: outward`. It then globs `QA-probe/*/*.md` and `probes/*/*.md` from the board root and
     reports, per record:
       topic-entry-requires-topic  the record answers to no page carrying a route: head key
       topic-probe-division        the record's path is not in exactly ONE `### E<n>` body, n > 0
       topic-record-section        a lean record without `## Question` or without `## Answer`
       topic-record-state          `state:` missing, or not one of the five
       topic-record-route          `route:` missing or not task|discovery|local, or the bank
                                   rule broken (local must NOT name a bank; the other two must)
     A record that still carries any `#### Q-executor`-style slot is judged as the OLD four-slot
     shape instead (topic-entry-heading, topic-entry-bank-state, topic-entry-unregistered).
     The checker does NOT see: `## Caveats`, the value binding, the face figures on E divisions
     (its division sweep matches digit-numbered headings only, so `### E1` is invisible to it), or
     whether a consumer row is honest. Those are yours.

     NO markdown pipe tables anywhere (JL 260710): every would-be table is record lines.
     English only. No em-dashes. One sentence per source line. -->

# <Page id> · <the topic, in the project's own words>
state: 🔴 OPEN
route: inward
display: companion
owner: JL
method: collect each consumer's question, send it once with the stake stripped, and write the answer back where the asking page can read it

<!-- RULE: `route: inward` IS THE TYPE KEY and it is REQUIRED. It must sit in the metadata head,
     above the first `## ` heading, on its own line, spelled exactly, with nothing after it and no
     leading `- `. The head regex is `^route:\s*(outward|inward)\s*$`. An evidence page wears a
     stage-shaped filename, so this line is the ONLY thing that separates it from a plain stage
     page: without it the page's type is unresolvable and the page is defective (base resolution
     step ②). `inward` means the answers do not exist yet and this project must RUN something to
     make them; `outward` is the literature sibling and is a different contract. -->

<!-- RULE: NO `provides:` LINE. This page is a view over N records, and the record is what ships a
     product. Writing `provides:` here claims an output this page does not own and points every
     downstream binding at the wrong file. `requires:` is allowed when a real upstream stage gates
     this topic; `style-from:` is normally absent. -->

<!-- RULE: `state:` takes the PAGE's four values, 🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD,
     and a short readable detail may follow the emoji (`🟡 PARTIAL · 2 of 5 answered, 1 consumer
     unbound`). These are NOT the record's five states. A record wears planned | commissioned |
     deferred | read | answered-local, and the two vocabularies never mix. -->

## Opening
What numbers must this project produce about <the topic>, who is waiting for each one, and have they come back?

<one paragraph, 4 to 5 sentences, under the base's 520-character ceiling: what the topic covers, which claim rests on it, and what is still missing. Plain English.>

**Where this page sits**: <the page that raised most of these questions, and the page that consumes the answers>.

**Why this page provides nothing**: it is a VIEW over N records, not an atom. Each `### E<n>` division points at one QA-probe record, and that record is the thing with a product. A display page is the opposite shape: it IS its atom and does declare a `provides:`.

**Covered elsewhere**: <the claims page that owns the claim ledger> · <the control page that owns the binding rule> · the record anatomy is `haipipe-board/ref/topic-entry-contract.md`.

<!-- RULE: the Opening must say WHY THIS PAGE PROVIDES NOTHING, in the drawer, in its own words.
     Every reader who has seen a display page arrives expecting a `provides:` line, and the
     absence of one reads as an omission until the page names it as the design. -->

## Diagram
**One page, N records**: where the answer lives, where the binding lives, and where the waiting lives.

```text
  🏦 the executor's own tree            tasks/… · discoveries/…
     the QA-bank is the ORIGINAL and it stays there. This page links
     to it and extracts from it. It is never copied in.
              │
              │  the record's `route:` + `bank:` keys
              ▼
  📋 QA-probe/<page name>/            one record per executor question
  │    1-<slug>.md                    the binding, a digest, the limits
  │    1-<slug>.data/                 optional · the ONE machine-readable product
  │      └── <product>.csv          🎯 what a display actually reads
  │         │
  │         ▼
  📄 <this page>.md                   ← a VIEW. No provides:.
       ### E0 · incoming              the queue, before translation
       ### E1 · <the executor question>   🔗 1-<slug>
  ────────────────────────────────────────────────────────────────
  the BANK holds the answer · the RECORD holds the binding
  the PAGE holds who is waiting · none of the three holds another's half
```

## Content

<!-- RULE: CONTENT IS E DIVISIONS AND NOTHING ELSE (JL 260806). One `### E<n> · <the executor
     question>` per Q-executor conversation, plus the standing `### E0 · incoming`. A prose
     division auditing where a number is stated, a table of every value, or a narrative of what
     went wrong is substance with a home: the value goes on its consumer row, the disagreement
     goes in `## Aims` as the work it is, and history goes in `## Log`. A page that keeps such a
     division is halfway through the 260806 restructure, not finished with it. -->

<!-- RULE: E0 COMES FIRST, matching its number and the core contract's own listing. It is the
     standing collect queue: a Q-consumer born on ANY page lands here first and waits until PROBE
     strips its stake, promotes it into a new `### E<n>`, and opens its QA-probe. E0 is never
     deleted, and an EMPTY E0 is written as empty rather than removed, because "nothing is
     waiting" is one of the two conditions this page closes on. -->

### E0 · incoming
**The standing queue**: what has been collected from a consumer page and not yet sent.

```text
  (empty)
```

📥 Establishes that nothing is waiting. A Q-consumer arriving from any page lands here, gets its stake stripped, and becomes an `### E<n>` division with its own record when it goes out.

- <arrival date> · `<Q-consumer id>` · from `<source page id>` · <the stake, one line>

<!-- RULE: ONE E<n> DIVISION BINDS TO EXACTLY ONE QA-PROBE, and one QA-probe is pointed at by
     exactly one E division. Many records across many papers may point at the SAME QA-bank; that
     sharing lives at the bank and is never mirrored here. Number E divisions from 1 and never
     reuse a number after a division is retired. Keep `E<n>` and the record's leading `<n>` the
     same digit: nothing enforces it, and a mismatch costs every reader one lookup. -->

### E1 · <the executor question, as the bank was asked it>
**The binding**: what was asked, which record holds the answer, and what state it is in.

```text
  🏦 bank       <path in the executor tree, or "none · route: local">
  🎯 product    1-<slug>.data/<file>                        · <n> rows
  🧾 evidence   1-<slug>.data/extracted-from.md             · when the product is a copy
  📐 shape      <one row per what, carrying which columns>
```

<emoji> Establishes <what this conversation settles for the paper, one line>.

🔗 QA-probe: `QA-probe/<page name>/1-<slug>.md` · state: <planned | commissioned | deferred | read | answered-local>
🖼 Display: `display/<page name>/1-<slug>.md` · state: <candidate | selected | paper-bound | parked | not-displayable>

<!-- RULE: THE POINTER PATH IS RELATIVE TO THIS PAGE'S OWN FOLDER, and the checker reads it
     literally: it takes each record's path relative to the page's directory and requires that
     exact string to appear in the body of exactly ONE `### E<n>` division with n > 0. Write the
     path, never "the record below". The face figure above is the BASE's per-division requirement
     and the pointer line is the CORE contract's; both are kept, figure first, because the
     checker's division sweep cannot see an `E`-numbered heading and will not catch a missing
     figure here. The record's path is written ONCE, on the pointer line, never also inside the
     figure: two copies of a path is one rename away from disagreeing. -->

#### consumers

- ⬜ `<Q-consumer id>` · from `<source page id>` · <the stake, one line: which claim rests on this number and what would count as producing it>
  A-consumer: <what THIS page reads the answer to mean for that consumer, in the consumer's terms>
  value: <the number with its uncertainty, exactly as the run reported it>
  run: `<run or task folder>` · spec `<the specification>` · qa `<path to the answering QA file>`
  claim: `<claim id>` · <supported | weakened | unresolved>

<!-- RULE: A CONSUMER ROW CARRIES A CLAIM DEPENDENCY, never a chore and never an ordered answer.
       ✅  "H2 states high-dose prescribing rises with the trait score. It needs the LBP-cohort
            estimate, its CI, and the spec that made it."
       🚫  "Get the regression results."          no claim named, so nothing can judge the answer
       🚫  "Produce an estimate near 0.3."        the answer ordered in advance
     The stake stays HERE. The record's question is neutral, and the bank that runs it never
     learns which claim would be rescued; `page-phases/haipipe-page-probe` owns that wall. -->

<!-- RULE: EVERY ROW WEARS EXACTLY ONE STATE, as the first token after the dash:
       ⬜         open, the answer has not been read back into this consumer's terms
       BOUND      the value, its provenance, and the claim update are all on the row
       DEFERRED   with the reason written on the row itself
       WITHDRAWN  because the claim the row served changed
     `⬜` is the only one that is an emoji; the other three are written as capitals. SUPPORTED is
     the outward route's word and is wrong here. -->

<!-- RULE: BOUND NEEDS THREE PARTS AND ALL THREE ARE PATHS OR NUMBERS, never a memory:
       1  the value           with its uncertainty, exactly as the run reported it
       2  the run provenance  which run, which specification, which QA file, EACH BY PATH
       3  the claim update    which claim consumed it, and whether it is now supported,
                              weakened, or unresolved
     A number whose provenance line is missing is a HOLE, not a result: it reads exactly like a
     real one, which is why the row, not the prose, is what CHECK audits. Until the paths exist
     and resolve, the row stays ⬜, however right the number looks in the manuscript. -->

<!-- RULE: AN ANSWERED QUESTION WITH NO CONSUMER IS A VISIBLE OPEN ROW, not a quiet success.
     Write it as `- ⬜ nobody yet` with one line saying what that costs, and resolve it by binding
     a consumer or retiring the division with a dated line. -->

#### answer digest

<2 to 3 lines from the record's Answer: the finding, and the one limit that caps every claim built on it. The full text stays in the record, one click away.>

<!-- RULE: THE DISPLAY CARD IS A SIBLING, not evidence copied here. It gives this answer a
     candidate value table or figure, its takeaway, its claim role, and its disposition. A
     `not-displayable` card is a valid outcome and says why. Narrative may select a card; only
     a selected card may request a formal Paper Display unit. -->

<!-- RULE: THE DIGEST IS A DIGEST. It is what a reader scans, so it never grows into a copy of the
     answer, and it never states a number the consumer rows above do not carry with provenance. -->

## Aims

<!-- RULE: mirror the E divisions, INCLUDING E0. A group is `### A<n> · <emoji> E<n> · <short name>`,
     taking the division's own number and an emoji, so Content, Aims, and States line up by eye:
     E0's group is `### A0`, E3's is `### A3`. `P` is for a target that belongs to no single
     division, which on this page is normally only the human gate. Every Aim needs a testable
     `Done when`, and an Aim never carries a checkbox. -->

### A0 · 📥 E0 · incoming
- A0.1 · No Q-consumer sits in `E0 · incoming` longer than one working round.
  **Done when:** E0 is empty, or every row in it carries the date it arrived.

### A1 · <emoji> E1 · <short name>
- A1.1 · Every consumer under E1 is bound to the answer, or terminal with its reason.
  **Done when:** each row carries the value, its run, its specification, and its QA path, and every path resolves.

### P · Page-level
- P1 · <the human gate: the person named in `owner:` accepts this topic's value set>.
  **Done when:** every E division's consumers are BOUND, DEFERRED, or WITHDRAWN, AND E0 is empty, AND <owner> has said so.

<!-- RULE: THE CLOSE RULE, and it has two halves that are both required. Every E<n> division's
     consumers are terminal, AND E0 is empty. The human gate reads the E DIVISIONS, not the
     records: an answer sitting in a record that never became a consumer row closes nothing. -->

## States

### Decision Now
- [ ] 🗣 <the one choice that stops this page, stated as a question>
      📍 `Part` <the E division it belongs to>
      🔔 `Why now` <what raised it>
      ⭐ `A ·` <the first option, named by its consequence>
      `B ·` <the second option, and what it commits you to>
      🛑 `Blocks` <what stops until it is answered, or `nothing`>
      🤖 `If nobody answers` <the option that takes effect>

### A0 · 📥 E0 · incoming
- ⬜ A0.1 · Not started; E0 has not been swept.

### A1 · <emoji> E1 · <short name>
- ⬜ A1.1 · Not started; no consumer row under E1 carries a resolving provenance path yet.

### P · Page-level
- ⬜ P1 · Not started; no gate ruling has been recorded.

## Files

📥 **Input files** · what this page reads

- `QA-probe/<page name>/`
  The drawer. One record per executor question, each optionally with its `.data/` product beside it.
- `display/<page name>/`
  One candidate Value Display card per executor question. It is the bridge from a probe answer
  to a possible figure or table, not the final float.
- `QA-probe/<page name>/1-<slug>.md`
  <what this record answers, one line. Name the records, not only the folder: "the drawer" is not a way to reach anything.>

📋 **Contracts** · what carries a rule here

- `board/page-types/haipipe-page-for-value/SKILL.md`
  The route contract this page is an instance of.
- `board/haipipe-board/ref/topic-entry-contract.md`
  The E-division and record anatomy, shared with the outward route.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · PROBE` · [<consumer page id>](<path/to/consumer-page.md>)
  <why this phase needs that fragment>

## Log
YYMMDD · <what changed>

<!-- ══════════════════════════════════════════════════════════════════════════════════════════
     PART 2 · THE QA-PROBE RECORD. A DIFFERENT FILE. DELETE THIS WHOLE COMMENT FROM THE PAGE.

     WHERE IT GOES:  QA-probe/<page name>/<n>-<slug>.md
     The drawer is named for the PAGE, exactly, and sits beside it. `probes/<topic>/` is the
     pre-rename spelling; both are globbed and both still check, but new work writes `QA-probe/`.
     The paper family's projection files it as `probes/V<nn>-<topic>/` and is migrating.

     RULE: THE NAME IS DIGIT-FIRST, AND THAT IS THE HIDING MECHANISM, not a style choice. The
     Board engine's page sweep discovers pages only by the filename prefixes Q, S, Agent, and
     Meeting, so `1-drift-counts.md` is never swept onto the board, never listed in `## Pages`,
     and never rendered. `<n>` restarts at 1 in every drawer. Never "fix" a record by giving it a
     page-shaped name.

     RULE: A RECORD CARRIES NO PAGE FRAME. No `owner:`, no `## Opening`, no `## Diagram`, no
     `## Aims`, no `## States`, no `## Files`, no `## Log`, and no gate. The evidence page carries
     all of those on its behalf. A record that grew a page frame is usually an old probe entry
     that was once a board page; it renders nowhere and its frame is dead weight.

     RULE: TWO SHAPES ARE LIVE AND THE FILE ITSELF SAYS WHICH IT IS. The LEAN shape below was
     ruled on 260806, after JL observed that three of the old four slots were copies of something
     that already existed: the bank's question, the evidence page's consumers, and the bank's
     answer. The PRE-260806 four-slot shape (`#### Q-executor`, `#### consumer trace`,
     `#### bank binding`, `#### A-executor`, with `**state**:` inside the binding) still parses and
     is still checked, so an old record is not a defect. WRITE THE LEAN SHAPE. Never mix them: the
     presence of any one four-slot heading switches the whole file to the old checker.

     RULE: THE HEAD KEYS, in this order. Either `state:` or `- state:` parses; the list form below
     is what the task banks already use.
       state:     planned | commissioned | deferred | read | answered-local
                  planned, commissioned, and deferred are QUEUED; read and answered-local are
                  RESOLVED. Queue membership is derived from this line, never kept in a second file.
       route:     task | discovery | local
       bank:      the path to the answering QA-bank file. REQUIRED on task and discovery.
                  FORBIDDEN on local, because local means the answer was produced here and this
                  file IS the original. Both halves are checked.
       provides:  OPTIONAL. The one machine-readable product this record ships, relative to this
                  file's folder. Omit it when the answer is prose only.

     RULE: THE ANSWER IS A DIGEST, THE CAVEATS TRAVEL WHOLE. On any route but local the bank is
     the original and is never copied in, so `## Answer` here is a digest of it. `## Caveats` is
     the one part copied verbatim, because a digest of a LIMIT is how a paper ends up claiming
     more than its design supports. `## Question` and `## Answer` are mechanically required;
     `## Caveats` is required by this contract and by nothing in code, which means you are the
     only thing standing between the paper and an overclaim.

     RULE: THE PRODUCT LIVES IN `<n>-<slug>.data/`, beside the record, and holds ONE product.
       <n>-<slug>.data/<product>.csv     what a display binds to
       <n>-<slug>.data/source/build.py   regenerates it, and parses STRICTLY: every line inside
                                         the source fence must parse or the build fails. A parse
                                         that skips the lines it cannot read ships a short table
                                         with exit code 0, which is the silent disagreement the
                                         parse exists to prevent.
       <n>-<slug>.data/extracted-from.md REQUIRED when the product is a COPY of a run's output
                                         rather than parsed from this file. Name the run, what it
                                         read, what the extraction dropped, by whom, and when.
                                         An extract with no recorded origin is a number nobody
                                         can check, and it goes stale silently when the run is
                                         re-executed.
     A downstream page binds to the product BY ID where the group ships a resolver, for example
     `needs: QA-probe/<page name>/<n>-<slug>` read by the specimen group's `unit.py`. Where there
     is no resolver it binds by path, and the path is the thing that dies when a folder moves.

     ─────────────────────────────────────────────────────────────────────────────────────────
     THE FILE, ready to copy from the line below:

# <the executor question, as a title>

- state:    planned
- route:    task
- bank:     <path to the answering QA-bank file, in the executor's own tree>
- provides: <n>-<slug>.data/<product>.csv

## Question

<the neutral computation request: what to compute, over what, at what precision, and what would
count as delivering it. No claim id, no paper stake, no hint of which result is wanted.>

## Answer

<the digest of what the bank returned. On `route: local` this IS the original answer, and any
table typed here is the ONE place those numbers are typed: the product is parsed out of it, never
retyped alongside it.>

## Caveats

- <the design limit, copied whole from the bank>
- <what makes the answer stale, and what has to be done deliberately to refresh it>

<one line naming what anything built on this answer may and may not say>

     END OF PART 2. Delete everything from the PART 2 banner down.
     ══════════════════════════════════════════════════════════════════════════════════════════ -->
