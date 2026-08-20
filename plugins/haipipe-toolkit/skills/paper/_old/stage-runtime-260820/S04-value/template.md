<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S04-value/S-Value-<n>-<topic>.md: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished page. Delete this top line too. -->
# S Value <n> · <Topic Title>
state: 🔴 OPEN · evidence page opened, no consumer row terminal yet
owner: <who gates this topic; usually JL>
method: <one line: how this topic binds every number it owns to the run that produced it>
route: inward
requires: <the S04 hub page this topic hangs off, e.g. S-Value-Dash; drop the line if there is none>
<!-- RULE: the route: line is REQUIRED and lives HERE, in the metadata head right after owner:/method:. It is the machine-readable type key that resolves this page to page-types/haipipe-page-for-value (board/haipipe-board/ref/topic-entry-contract.md, "The head route line"). Without it the page's type is unresolvable and the page is defective. -->

## Opening
<!-- RULE: the lead is ONE question and it carries the topic's CLAIM DEPENDENCY: which claim rests on the numbers this topic owns, and what specification would count as producing them. "Get the regression results" is a chore, not a stake, and "produce an estimate near <x>" orders the answer in advance. After the lead, a blank line, then two or three More sentences, one sentence per line. -->
<The stake question, e.g. "What is the paper's <headline number> for <cohort>, and does every place that states it agree with the run?">

<Which claim rests on these numbers, by id.>
<What BOUND takes on this route: a run you can walk to, its specification, and its QA file, each named by path.>

## Stage Contract

<!-- RULE: machine-managed span. Leave this section heading in place and run stage.py sync to fill it from the requires: metadata above; never hand-edit between the haipipe:contract markers once they appear. -->

## Content

<!-- RULE: the numbers this topic owns, each beside the run that produced it. A number appears here only with its provenance; where a sentence states a value and no run is recorded, say so on the spot instead of smoothing it over. -->

### <The numbers this topic owns>
<What the accepted run states, one sentence per line, uncertainty included.>
<Where the manuscript prints each figure, and whether the printed copy agrees with the run.>

### E0 · incoming
<!-- RULE: the standing collect queue, always present. A Q-consumer born on ANY page is COLLECTED here first: one row per waiting question, source page id + the stake in one line. EVIDENCE promotes each row into a new E<m> division and opens its QA-probe; a promoted row leaves this queue. The page cannot close while a row waits here. Write <empty> when nothing waits. -->
- ⬜ `Q-<Stage>-<n>` · from `<source-page-id>` · <the claim dependency, one line, waiting for EVIDENCE to translate it>

### E<m> · <the executor question, in a few words>
<!-- RULE: ONE division per Q-executor conversation, id grammar `### E<m> · <question>`; one division owns exactly one QA-probe (1:1). The pointer line comes first and carries the record's bank-binding state. -->
🔗 QA-probe: `probes/V<nn>-<topic>/<m>-<slug>.md` · state: <planned | commissioned | deferred | read | answered-local>

#### consumers
<!-- RULE: one row per Q-consumer this conversation serves, collected from other pages. Each row: state token, the consumer id, the source page id, the stake in one line; the A-consumer interpretation goes on the indented lines once the answer lands. Row states: ⬜ open · BOUND (the value binding is on the row) · DEFERRED (reason on the row) · WITHDRAWN (the claim the row served changed). The human gate reads these rows, never the QA-probe: an answer sitting in the record's #### A-executor closes nothing until its A-consumer is written here. -->
- ⬜ `Q-<Stage>-<n>` · from `<source-page-id>` · <the claim dependency: which claim rests on the number, and what specification counts as producing it>
- BOUND `Q-<Stage>-<k>` · from `<source-page-id>` · <the claim dependency this row carried>
  <the value with its uncertainty, exactly as the run reported it, e.g. coef <b> (SE <se>), N <n>>
  run `tasks/<task-folder>/` · spec `tasks/<task-folder>/<spec file>` · qa `tasks/<task-folder>/QA/<n>-<slug>.md`
  claim `<claim id>` → <supported | weakened | unresolved>
  <!-- RULE: a BOUND row IS the value binding, three parts on the row: (1) the value with its uncertainty exactly as the run reported it, (2) the run provenance: which run, which specification, which QA file, each BY PATH from the project root, resolving on disk, (3) the claim update: which claim consumed it and what its status became. A number whose provenance line is missing is a HOLE, not a result; the row stays ⬜ however right the number looks. A number typed from memory binds nothing. -->

#### answer digest
<!-- RULE: 2-3 lines from the QA-probe's #### A-executor, no more; the record one click away carries the full text. Empty until the answer lands. -->
<2-3 lines from the A-executor, e.g. "coef <b> (SE <se>) on the accepted spec; N <n>; CI excludes zero.">

## Aims

### A1 · 🚪 The evidence page closes
- A1.1 · Every E division's consumers end BOUND, DEFERRED, or WITHDRAWN, and E0 is empty.
  **Done when:** no consumer row is ⬜, no row waits in E0, every BOUND row carries its three-part value binding, and each provenance path resolves on disk.

## States

### A1 · 🚪 The evidence page closes
- ⬜ A1.1 · <the honest present: how many consumer rows are open, which numbers still lack a run behind them, and whether E0 holds untranslated questions>

## Log

- <date> · [DRAFT-CC] evidence page opened: <n> Q-consumers collected into E0 from <where the claim dependencies came from, e.g. the claim ledger>
<!-- RULE: Log lines wear the ruled grammar `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`, PHASE one of DRAFT EVIDENCE REVISE CHECK. Typical lines on this route, in order: [EVIDENCE-CC] E0 row promoted → E<m> + probes/V<nn>-<topic>/<m>-<slug>.md, then [EVIDENCE-CC] value binding written, consumer row → BOUND, then [CHECK-CC] all rows terminal + E0 empty → CLOSE. The Log narrates and never carries evidence: bindings live on the consumer rows above, and the Log renders chip-free. -->
