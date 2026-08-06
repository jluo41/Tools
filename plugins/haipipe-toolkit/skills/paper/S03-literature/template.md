<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S03-literature/S-Literature-<n>-<topic>.md: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished page. Delete this top line too. -->
# S Literature <n> · <Topic Title>
state: 🔴 OPEN · evidence page opened, no consumer row terminal yet
owner: <who gates this topic; usually JL>
method: <one line: how this topic turns its stake questions into citation bindings>
route: outward
requires: <the S03 hub page this topic hangs off, e.g. S-Literature-Dash; drop the line if there is none>
<!-- RULE: the route: line is REQUIRED and lives HERE, in the metadata head right after owner:/method:. It is the machine-readable type key that resolves this page to page-types/haipipe-board-page-for-literature (board/haipipe-board/ref/topic-entry-contract.md, "The head route line"). Without it the page's type is unresolvable and the page is defective. -->

## Opening
<!-- RULE: the lead is ONE question and it carries the topic's POSITIONING STAKE: what the work claims to add here, and what published result would strengthen or break that claim. "Find papers about <area>" is a reading list, not a stake. After the lead, a blank line, then two or three More sentences, one sentence per line. -->
<The stake question, e.g. "Is <our measure or angle> novel, or did <field> already do it? <Claim id>'s contribution claim dies if a published precedent exists.">

<Which claim or section of the paper leans on this topic.>
<What SUPPORTED takes on this route: named, real sources standing behind the positioning, never an empty search.>

## Stage Contract

<!-- RULE: machine-managed span. Leave this section heading in place and run stage.py sync to fill it from the requires: metadata above; never hand-edit between the haipipe:contract markers once they appear. -->

## Content

<!-- RULE: what the topic has earned so far: the lineage this strand establishes and the source record behind each step. Real keys only: grep the paper's .bib BEFORE writing a key; a citation that does not exist yet is written \cite{TOADD} beside its consumer row, never a key from memory. -->

### <Lineage>
<What this strand establishes, one sentence per line.>
- \citep{<realkey>} · <the one job this source does for the strand>

### E0 · incoming
<!-- RULE: the standing collect queue, always present. A Q-consumer born on ANY page is COLLECTED here first: one row per waiting question, source page id + the stake in one line. PROBE promotes each row into a new E<m> division and opens its QA-probe; a promoted row leaves this queue. The page cannot close while a row waits here. Write <empty> when nothing waits. -->
- ⬜ `Q-<Stage>-<n>` · from `<source-page-id>` · <the stake, one line, waiting for PROBE to translate it>

### E<m> · <the executor question, in a few words>
<!-- RULE: ONE division per Q-executor conversation, id grammar `### E<m> · <question>`; one division owns exactly one QA-probe (1:1). The pointer line comes first and carries the record's bank-binding state. -->
🔗 QA-probe: `probes/L<nn>-<topic>/<m>-<slug>.md` · state: <planned | commissioned | deferred | read | answered-local>

#### consumers
<!-- RULE: one row per Q-consumer this conversation serves, collected from other pages. Each row: state token, the consumer id, the source page id, the stake in one line; the A-consumer interpretation goes on the indented line once the answer lands. Row states: ⬜ open · SUPPORTED (the citation binding is on the row) · DEFERRED (reason on the row) · WITHDRAWN (the claim the row served changed). The human gate reads these rows, never the QA-probe: an answer sitting in the record's #### A-executor closes nothing until its A-consumer is written here. -->
- ⬜ `Q-<Stage>-<n>` · from `<source-page-id>` · <the stake: what the work claims to add, and what published result would break it>
- SUPPORTED `Q-<Stage>-<k>` · from `<source-page-id>` · <the stake this row carried>
  `<realkey>` · <one positioning sentence: how this work stands next to the found result: extends | contradicts | first-in-setting> · novelty <supported | threatened | broken>, with the source named
  <!-- RULE: a SUPPORTED row IS the citation binding, three parts on the row: (1) a real key that resolves in the .bib, (2) one positioning sentence, (3) a novelty verdict with the source named. Never write "novelty confirmed" from an absence of findings alone: absence after a bounded search is written "no precedent found within <the search's own scope>". -->

#### answer digest
<!-- RULE: 2-3 lines from the QA-probe's #### A-executor, no more; the record one click away carries the full text. Empty until the answer lands. -->
<2-3 lines from the A-executor, e.g. "UNOCCUPIED at medium-high confidence within the two-pass search's scope; nearest neighbour <realkey>.">

## Aims

### A1 · 🚪 The evidence page closes
- A1.1 · Every E division's consumers end SUPPORTED, DEFERRED, or WITHDRAWN, and E0 is empty.
  **Done when:** no consumer row is ⬜, no row waits in E0, every SUPPORTED row carries its three-part citation binding, and the owner has read the divisions.

## States

### A1 · 🚪 The evidence page closes
- ⬜ A1.1 · <the honest present: how many consumer rows are open, what each open row is waiting on, and whether E0 holds untranslated questions>

## Log

- <date> · [DRAFT-CC] evidence page opened: <n> Q-consumers collected into E0 from <where the stakes came from, e.g. the delivery pages>
<!-- RULE: Log lines wear the ruled grammar `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`, PHASE one of DRAFT PROBE REVISE CHECK. Typical lines on this route, in order: [PROBE-CC] E0 row promoted → E<m> + probes/L<nn>-<topic>/<m>-<slug>.md, then [PROBE-CC] citation binding written, consumer row → SUPPORTED, then [CHECK-CC] all rows terminal + E0 empty → CLOSE. The Log narrates and never carries evidence: bindings live on the consumer rows above, and the Log renders chip-free. -->
