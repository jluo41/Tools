<!-- TEMPLATE · ONE OUTWARD TOPIC = ONE LITERATURE EVIDENCE PAGE.
     Copy this file to the topic's page path and fill it. On a paper board that path is
     `0-lifecycle/S03-literature/S-Literature-<n>-<topic>.md`; on any other board it is
     wherever that board's group keeps its evidence pages.
     Replace every `<angle-bracket>` slot. DELETE every `<!-- RULE: ... -->` comment as you
     satisfy it: a RULE comment never ships in a filled page. Delete this block too.

     THIS FILE COVERS TWO FILES, NOT ONE.
       PART A  the evidence PAGE, below, in the order the base frame fixes.
       PART B  the QA-probe RECORD, at the very bottom, inside a fenced block. It is a
               SEPARATE file at `QA-probe/<page name>/<n>-<slug>.md`. Cut it out of the
               page. A record left inside the page is the exact defect the split prevents.

     WHAT THIS TYPE ADDS. Only these four things are this page type's own:
       · the head `route: outward` line, which is the page's machine-readable type key
       · NO `provides:` line, because the page is a VIEW over N records, not an atom
       · Content organized BY EXECUTOR: `### E0 · incoming`, then one `### E<m>` division
         per Q-executor conversation, each owning exactly one QA-probe record
       · the CITATION BINDING a SUPPORTED consumer row must carry
     Everything else is the base frame and is NOT restated here. Read it there:
       `../../haipipe-board/ref/page-template.md`          the authored page shape
       `../../haipipe-page/SKILL.md`                 the section contract
       `../../haipipe-board/ref/topic-entry-contract.md`   E-division and record anatomy
       `./SKILL.md`                                        this route's own dictionary
     The paper family keeps its own wording of the same page at
     `../../../paper/S03-literature/template.md`. Where the two disagree, this file states
     the type-level rule and that one states the paper family's local habits.

     English only. No em-dashes. One sentence per source line. -->

<!-- RULE: THE MECHANICAL GATE, so you know which rules police themselves and which do not.
     Run `python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder>` and read
     the rows for this page and for `QA-probe/<page name>/`. `src/topic_entry_contract.py`
     wakes up ONLY when a page carries the head `route:` line, so a missing `route:` line
     does not fail loudly: it fails by making every rule below invisible.

       ERRORS it raises
       topic-entry-requires-topic  a record answers to no page carrying a route: head key
       topic-probe-division        0 or 2+ E<m> divisions point at one record; must be 1
       topic-record-section        a lean record is missing `## Question` or `## Answer`
       topic-record-state          state: absent, or not one of the five values
       topic-record-route          route: not task|discovery|local, or `local` WITH a
                                   bank:, or non-local WITHOUT a bank:

       WHAT IT NEVER SEES, so you are the only checker for these
       the `#### consumers` and `#### answer digest` blocks, and every row in them
       the three-part citation binding on a SUPPORTED row
       `## Caveats` in a record
       a caption or figure on an `### E<m>` division: `check_division_figures` splits on
         `### <digits>`, and `E1` is not digits, so E divisions are invisible to it
       an Aims or States group named for an E division: `check_group_names` reads the same
         digits, so `group-name-drift` can never fire on this page type
       a `provides:` line that should not be there
     Delete this comment once you have run the checker and read its rows. -->

# S Literature <n> · <Topic title in sentence case>
state: 🔴 OPEN · evidence page opened, no consumer row terminal yet
owner: <who gates this topic, usually JL>
method: <one line: how this topic turns positioning stakes into citation bindings>
route: outward
display: companion
requires: <the hub page this topic hangs off, e.g. S-Literature-Dash; delete the line if none>

<!-- RULE: `route: outward` is REQUIRED, sits right after `owner:`/`method:`, and must be a
     BARE line. The checker matches `^route:\s*outward\s*$`, so a leading `- `, a trailing
     comment, or any other value leaves the page's type unresolvable and the page defective.
     An evidence page wears a stage-shaped filename, so this line is the ONLY thing that
     separates it from a plain stage page (base resolution step ②). -->

<!-- RULE: NEVER write a `provides:` line on this page. An evidence page is a VIEW over N
     records, not an atom: it produces no artifact a downstream page can inherit by id, and
     on the outward route the product of each record is PROSE, which is not a file. A
     `provides:` line here promises a handoff that does not exist. Nothing reports it, which
     is why the rule is written and not checked. -->

<!-- RULE: `state:` takes the page-level four, 🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD,
     with a short readable suffix allowed after the emoji. On THIS type the suffix is worth
     using to say the rung: how many consumer rows are terminal, and what the open ones wait
     on. The page may reach ✅ only when every `### E<m>` division's consumers are SUPPORTED,
     DEFERRED, or WITHDRAWN, AND `### E0 · incoming` is empty. -->

## Opening
<!-- RULE: the lead is ONE question carrying this topic's POSITIONING STAKE: what the work
     claims to add here, and what published result would strengthen or break that claim.
     `Find papers about <area>` is a reading list, not a stake, and `Confirm nobody has done
     this` is a verdict ordered in advance. Everything before the FIRST BLANK LINE is the
     only prose a reader sees; keep it under 520 characters, target ~450. -->
<The stake question, e.g. "Is <our measure or angle> novel, or did <field> already do it, and has any answer become a citation the manuscript can use?">
<One or two more sentences: what the topic's own words mean, and what this page owns.>

<!-- RULE: below the blank line, write labelled parts, never one block of prose. Two parts
     are this type's own and belong here; the rest is the base's. -->
**Why a returned answer is not yet evidence**: <a digest is a convenience; what a manuscript may lean on is the citation binding written on the asking row.>

**Why this page provides nothing**: <it is a view over N records, and a literature answer's product is prose rather than a file.>

**Covered elsewhere**: <the inward twin, the hub, and `haipipe-board/ref/topic-entry-contract.md` for the record anatomy.>

## Stage Contract
<!-- RULE: REQUIRED whenever the page's filename starts with `S`, because `check.py` raises
     `missing-stage-section` on any S page without it. Leave the heading in place and let
     `stage.py sync` fill the managed block from `requires:`. Never hand-edit between the
     `haipipe:contract` markers. Delete the whole section on a board whose evidence pages do
     not wear S filenames. There is no `### Provides` subsection on this type. -->

## Writing Style
<!-- Base only. Nothing this type adds. See `../../haipipe-board/ref/page-template.md`.
     Delete the section if the page inherits no rules and owns none. -->

## Diagram
<!-- Base only, and optional. If you draw one, the figure worth drawing on this type is the
     path an outward answer travels: the published record, the QA-bank that searched it, the
     QA-probe record, the E division, and the consumer row that must turn it into a citation.
     Delete the whole section if no figure helps. -->

## Content

<!-- RULE: Content on this type is organized BY EXECUTOR and by nothing else. One
     `### E<m> · <the executor question>` division per Q-executor conversation, and one
     division owns exactly ONE QA-probe record (1:1). A flat register of consumers is
     retired (JL 260806). Ordinary prose divisions may sit ABOVE E0 when this topic also
     carries a lineage or a source list; every E division comes after them, E0 first. -->

### E0 · incoming
<!-- RULE: the one STANDING division. It is always present, even when empty, because its
     emptiness is a fact the close rule reads. A Q-consumer born on ANY page is COLLECTED
     here first: one row per waiting question, carrying the source page id and the stake in
     one line. PROBE promotes a row into a new `### E<m>` division and opens its QA-probe;
     a promoted row LEAVES this queue. E0 never points at a record. The page cannot close
     while a row waits here. Write `<empty>` when nothing waits. -->
- ⬜ `Q-<Stage>-<n>` · from `<source-page-id>` · <the stake, one line, waiting for PROBE to translate it> · arrived <YYMMDD>

### E<m> · <the executor question, in a few words>
<!-- RULE: the POINTER LINE comes first in the division, before the consumers block, and it
     carries the record's own bank-binding state. The path is written RELATIVE TO THIS
     PAGE'S OWN FOLDER, because that is the string the checker looks for inside this
     division's body. A variant is legal and one specimen uses it: carry the pointer as the
     first ROW INSIDE the division's face figure, keeping this exact wording, which avoids
     printing the pointer twice when the division also wants a caption and a figure. -->
🔗 QA-probe: `QA-probe/<page name>/<m>-<slug>.md` · state: <planned | commissioned | deferred | read | answered-local>
🖼 Display: `display/<page name>/<m>-<slug>.md` · state: <candidate | selected | paper-bound | parked | not-displayable>

<!-- RULE: the drawer is named after the PAGE, exactly: `QA-probe/<page file stem>/`, one
     file per question, digit first, `<m>` restarting at 1 per drawer. `probes/<topic>/` is
     the pre-rename name; it still parses, and new work does not write it.
     THE TRAP, and it is a real ERROR rather than a style note: when the drawer name is not
     also the page's resolved id, the record must say which page owns it. A page called
     `S-Literature-2-reviews-reputation.md` resolves to the id `S-Literature-2`, so a drawer
     named `QA-probe/S-Literature-2-reviews-reputation/` raises
     `topic-entry-requires-topic` on every record inside it unless each record carries a
     `requires: S-Literature-2` head key. A page with no `S-<Family>-<n>` prefix resolves to
     its own stem, so its drawer name matches and no `requires:` line is needed. -->

#### consumers
<!-- RULE: one row per Q-consumer this conversation serves, collected from other pages. A
     row carries, in order: the row state, the consumer id, the source page id, and the
     stake in one line. The A-consumer interpretation goes on an indented line once the
     answer lands. Row states are `⬜` open · SUPPORTED · DEFERRED with the reason on the
     row · WITHDRAWN because the claim the row served changed. The human gate reads THESE
     ROWS, never the record: an answer sitting in a record's `## Answer` closes nothing
     until its A-consumer is written here. -->
- ⬜ `Q-<Stage>-<n>` · from `<source-page-id>` · <the stake: what the work claims to add, and what published result would break it>
- SUPPORTED `Q-<Stage>-<k>` · from `<source-page-id>` · <the stake this row carried>
  A-consumer: <what the answer means for the sentence or claim that asked, in this page's own words>
  citation binding · key `<realkey>` · positioning: <this work EXTENDS | CONTRADICTS | is FIRST-IN-SETTING against the found result, one sentence> · verdict: novelty <supported | threatened | broken>, <the source named, and the search scope when the verdict rests on an absence>
<!-- RULE: a SUPPORTED row IS the citation binding, and it has three parts, all on the row:
       1  a real key      resolvable in the bibliography. Grep the `.bib` BEFORE writing it.
                          A key from memory is a fabricated citation. When no key exists
                          yet, write `\cite{TOADD}` and keep the row open.
       2  a positioning   one sentence saying how this work stands NEXT TO the found result.
          sentence
       3  a novelty       supported · threatened · broken, with the source named.
          verdict
     🚫 NEVER write "novelty confirmed" from an ABSENCE of findings alone. An absence after
     a bounded search is written as "no precedent found within <the search's own scope>",
     because the search's limits are part of the fact. A search that came back empty
     supports nothing by itself: the row either carries the bounded no-precedent finding,
     scope and all, or it stays `⬜`. -->

#### answer digest
<!-- RULE: 2-3 lines lifted from the record's `## Answer`, and no more. The record is one
     click away and carries the full text. Leave it empty until the answer lands. A digest
     is NOT a citation: a division with a digest and no binding on its rows is an answered
     question the manuscript cannot use, and the page stays 🟡 until the binding is written
     or the row is WITHDRAWN. -->
<2-3 lines, e.g. "UNOCCUPIED within the scope of a two-pass sweep; nearest neighbour `<realkey>` shares the text-derived half and stops before the outcome.">

<!-- RULE: THE DISPLAY CARD IS A SIBLING, not a second citation digest. It proposes a literature
     matrix or map, its takeaway and claim role, or records `not-displayable` with the reason.
     Narrative may select it; only then may it request a formal Paper Display unit. -->

## Aims
<!-- RULE: one group per Content division, taking that division's NUMBER and NAME plus an
     emoji on the group: `### A0 · 📥 E0 · incoming`, `### A1 · <emoji> E1 · <short name>`.
     The numbers line up by eye, which is the base's whole reason for the rule, and nothing
     reports it when they do not because the group checker cannot see an `E` heading.
     A target that crosses divisions goes under `### P · Page-level`.
     ONE COLLISION TO KNOW ABOUT. `check_group_names` compares groups against Content
     divisions matching `### <digits> · <name>`. When this page carries no digit-numbered
     division, that list is empty and the check returns without looking, which is why an
     `A<m>` group naming an `E<m>` division passes. Add ONE digit-numbered prose division
     above E0, such as `### 1 · Lineage`, and the list stops being empty: every `A<m>` group
     then reports `group-no-division` or `group-name-drift` against it. Either leave the
     prose divisions unnumbered, as both live pages do, or expect those two warnings and say
     on the page why they are accepted. -->

### A0 · 📥 E0 · incoming
- A0.1 · <no positioning question sits in E0 longer than one working round>
  **Done when:** <E0 is empty, or every row in it carries the date it arrived>

### A<m> · <emoji> E<m> · <short name of the conversation>
- A<m>.1 · <the outcome this conversation owes, e.g. the answer becomes a citation binding or the row is withdrawn>
  **Done when:** <the testable condition, naming the page and section where the binding lands>

### P · Page-level
- P1 · The evidence page closes.
  **Done when:** no consumer row is `⬜`, every SUPPORTED row carries its three-part citation binding, no row waits in `E0`, and the owner has read the divisions.

## States
<!-- RULE: mirror every Aim id exactly once with ⬜ 🔨 🧠 ✅ ❄️, in the same groups. States
     is a snapshot: why a row changed belongs in `## Log`. `### Decision Now` is the base's,
     goes FIRST when present, and on this type the row that earns it is usually a division
     holding an answer that never became a citation binding. -->

### A0 · 📥 E0 · incoming
- ⬜ A0.1 · <how many rows wait in E0, and since when>

### A<m> · <emoji> E<m> · <short name of the conversation>
- ⬜ A<m>.1 · <the honest present for this conversation>

### P · Page-level
- ⬜ P1 · <how many consumer rows are terminal out of how many, what each open row waits on, and whether E0 is empty>

## Files
<!-- RULE: base groups and base rules. Three rows are this type's own and belong on every
     page of it. -->
- `QA-probe/<page name>/`
  The records, one per E division. Open one to read the full answer the digest summarizes.
- `display/<page name>/`
  One candidate Literature Display card per E division. It makes positioning evidence inspectable
  as a matrix or map without claiming it is a final paper float.
- `<the bibliography this page's keys must resolve in>`
  Every key written into a citation binding resolves here, or the binding is not written.
- `<../page-types/haipipe-page-for-literature/SKILL.md>`
  The contract this page is an instance of. If the two disagree, the contract wins.

## Log
<!-- RULE: `- <YYMMDD> [HHMM] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`, PHASE one of
     DRAFT PROBE REVISE CHECK. The Log narrates and never carries evidence: bindings live on
     the consumer rows. Read the clock or a git commit for the time, or omit it. Never
     delete a `> USER:` line: resolve it and move it here verbatim. -->
- <YYMMDD> · [DRAFT-CC] evidence page opened: <n> Q-consumers collected into E0 from <where the stakes came from>

<!-- ══════════════════════════════════════════════════════════════════════════════════════
     PART B · THE QA-PROBE RECORD. A SEPARATE FILE. Cut everything below out of the page.

     One record per `### E<m>` division, at `QA-probe/<page name>/<m>-<slug>.md`, digit
     first, `<m>` restarting at 1 per drawer. The digit-first name IS the hiding mechanism:
     the Board's page sweep discovers pages by the prefixes `Q`, `S`, `Agent`, `Meeting`, so
     a digit-first file is never swept onto the board, never listed in `## Pages`, and never
     rendered. Do not "fix" a missing record by giving it a page-shaped name.

     A record carries NO page frame: no `## Opening`, no `## Aims`, no `## States`, no
     `## Files`, no `## Log`, and no gate. The evidence page carries all of those for it.

     TWO RECORD SHAPES ARE LIVE, and the file itself says which it is. The template below
     teaches the LEAN form, ruled 260806. You will still meet the pre-260806 FOUR-SLOT form
     in older drawers: `#### Q-executor`, `#### consumer trace`, `#### bank binding` holding
     a `**state**:` line, `#### A-executor`, often wrapped in a full page frame left over
     from when records were board pages. The checker detects a four-slot record by those
     headings and applies the old rules to it, so an old record is not broken and does not
     need migrating on sight. Write LEAN for anything new. Three of the four old slots were
     copies of something that already existed elsewhere: the bank's question, the evidence
     page's consumers, and the bank's answer.
     ══════════════════════════════════════════════════════════════════════════════════════ -->

````markdown
# <the conversation, as a short title>

state: <planned | commissioned | deferred | read | answered-local>
route: <task | discovery | local>
bank: <path to the answering QA-bank file; DELETE this key entirely when route is local>
requires: <the owning evidence page's id; needed only when the drawer name is not that id>

<!-- RULE: the head keys are read in either style, `route: discovery` or `- route: discovery`.
     `state:` must be one of the five: planned, commissioned, and deferred are QUEUED; read
     and answered-local are RESOLVED. Queue membership is derived from this line and is
     never maintained in a second file.
     `route:` must be one of the three. `task` and `discovery` mean the answer lives in an
     executor tree, so `bank:` is REQUIRED and names the QA-bank file, the original. `local`
     means the answer was produced here, so this file IS the original and a `bank:` key is an
     ERROR. A local answer on the outward route is legitimate and cheap; its cost goes in
     Caveats, because an absence read off two sources on the shelf is bounded by those two
     sources.
     NEVER write a `provides:` line on an outward record. The product is prose, not a file.
     The inward twin's records may carry one; this route's never do. -->

## Question

<the Q-executor: the neutral question, with the stake STRIPPED. No claim id, no hypothesis, no page id, no hint of which answer would be convenient. The stake stays on the evidence page's consumer row, and the wall between them belongs to PROBE.>

## Answer

<the A-executor, digested from the bank. State the verdict first, then the sources that carry it, then the scope the verdict rests on. A small fenced table of key, what it does, and the leg it misses reads faster than prose.>

## Caveats

<!-- RULE: Caveats are COPIED WHOLE from the bank, never digested. Nothing checks that this
     section exists, and it is the one a reader most needs: a digest of a LIMIT is how a
     paper ends up claiming more than its evidence supports. On the outward route the first
     caveat is almost always the search's own scope, because absence within a scope is not
     absence. -->
- <the search's scope, stated so the verdict cannot be quoted without it>
- <what the nearest neighbour does NOT make comparable>
- <anything unverified: an identifier checked but the bibtex not, a preprint, a rate-limited channel>
````
