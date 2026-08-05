<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S03-literature/S-Literature-<n>-<topic>.md: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished page. Delete this top line too. -->
# S Literature <n> · <Topic Title>
state: 🔴 OPEN · register opened, no row terminal yet
owner: <who gates this topic; usually JL>
method: <one line: how this topic turns its stake questions into citation bindings>
requires: <the S03 hub page this topic hangs off, e.g. S-Literature-Dash; drop the line if there is none>

## Opening
<!-- RULE: the lead is ONE question and it carries the topic's POSITIONING STAKE: what the work claims to add here, and what published result would strengthen or break that claim. "Find papers about <area>" is a reading list, not a stake. After the lead, a blank line, then two or three More sentences, one sentence per line. -->
<The stake question, e.g. "Is <our measure or angle> novel, or did <field> already do it? <Claim id>'s contribution claim dies if a published precedent exists.">

<Which claim or section of the paper leans on this topic.>
<What SUPPORTED takes on this route: named, real sources standing behind the positioning, never an empty search.>

## Stage Contract

<!-- RULE: machine-managed span. Leave this section heading in place and run stage.py sync to fill it from the requires: metadata above; never hand-edit between the haipipe:contract markers once they appear. -->

## Content

<!-- RULE: what the register has earned so far: the lineage this strand establishes and the source record behind each step. Real keys only: grep the paper's .bib BEFORE writing a key; a citation that does not exist yet is written \cite{TOADD} beside its register row, never a key from memory. -->

### <Lineage>
<What this strand establishes, one sentence per line.>
- \citep{<realkey>} · <the one job this source does for the strand>

## Aims

### Q-consumer register
route: outward
<!-- RULE: the route line is REQUIRED and is the register's FIRST line: it is the machine-readable key that resolves this page to page-types/haipipe-board-page-for-literature (board/haipipe-board/ref/topic-entry-contract.md, "Register route line"). Without it the page's type is unresolvable and the page is defective. -->
<!-- RULE: one row per Q-consumer, and the row is the CANONICAL record: the human gate reads this register, never the entries. An answer sitting in an entry's #### a-executor closes nothing until it becomes a record on its row here. Row states, written on the row itself: ⬜ open · SUPPORTED (the citation binding is on the row) · DEFERRED (reason on the row) · WITHDRAWN (the claim the row served changed). An open row points at its entry with the ⏳ pointer. -->
- ⬜ `Q-<Stage>-<n>` · <the stake question this row carries: what the work claims to add, and what published result would break it>
  ⏳ → `probes/L<nn>-<topic>/<n>-<slug>.md`
- SUPPORTED `Q-<Stage>-<m>` · <the stake question this row carried>
  `<realkey>` · <one positioning sentence: how this work stands next to the found result: extends | contradicts | first-in-setting> · novelty <supported | threatened | broken>, with the source named
  <!-- RULE: a SUPPORTED row IS the citation binding, three parts on the row: (1) a real key that resolves in the .bib, (2) one positioning sentence, (3) a novelty verdict with the source named. Never write "novelty confirmed" from an absence of findings alone: absence after a bounded search is written "no precedent found within <the search's own scope>". -->

### A1 · 🚪 The register closes
- A1.1 · Every register row ends SUPPORTED, DEFERRED, or WITHDRAWN.
  **Done when:** no row is ⬜, every SUPPORTED row carries its three-part citation binding, and the owner has read the register.

## States

### A1 · 🚪 The register closes
- ⬜ A1.1 · <the honest present: how many rows are open, and what each open row is waiting on>

## Log

- <date> · [DRAFT-CC] register opened: <n> rows raised from <where the stakes came from, e.g. the delivery pages' Q-consumers>
<!-- RULE: Log lines wear the ruled grammar `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`, PHASE one of DRAFT PROBE REVISE CHECK. Typical lines on this route, in order: [PROBE-CC] entry ⏳ → probes/L<nn>-<topic>/<entry>.md, then [PROBE-CC] citation binding written, row → SUPPORTED, then [CHECK-CC] all rows terminal → CLOSE. The Log narrates and never carries evidence: bindings live on the register rows above, and the Log renders chip-free. -->
