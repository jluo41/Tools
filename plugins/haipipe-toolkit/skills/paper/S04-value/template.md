<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S04-value/S-Value-<n>-<topic>.md: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished page. Delete this top line too. -->
# S Value <n> · <Topic Title>
state: 🔴 OPEN · register opened, no row terminal yet
owner: <who gates this topic; usually JL>
method: <one line: how this topic binds every number it owns to the run that produced it>
requires: <the S04 hub page this topic hangs off, e.g. S-Value-Dash; drop the line if there is none>

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

## Aims

### Q-consumer register
route: inward
<!-- RULE: the route line is REQUIRED and is the register's FIRST line: it is the machine-readable key that resolves this page to page-types/haipipe-board-page-for-value (board/haipipe-board/ref/topic-entry-contract.md, "Register route line"). Without it the page's type is unresolvable and the page is defective. -->
<!-- RULE: one row per Q-consumer, and the row is the CANONICAL record: the human gate reads this register, never the entries. An answer sitting in an entry's #### a-executor closes nothing until it becomes a record on its row here. Row states, written on the row itself: ⬜ open · BOUND (the value binding is on the row) · DEFERRED (reason on the row) · WITHDRAWN (the claim the row served changed). An open row points at its entry with the ⏳ pointer. -->
- ⬜ `Q-<Stage>-<n>` · <the claim dependency this row carries: which claim rests on the number, and what specification counts as producing it>
  ⏳ → `probes/V<nn>-<topic>/S-Value-<n>-<slug>.md`
- BOUND `Q-<Stage>-<m>` · <the claim dependency this row carried>
  <the value with its uncertainty, exactly as the run reported it, e.g. coef <b> (SE <se>), N <n>>
  run `tasks/<task-folder>/` · spec `tasks/<task-folder>/<spec file>` · qa `tasks/<task-folder>/QA/<n>-<slug>.md`
  claim `<claim id>` → <supported | weakened | unresolved>
  <!-- RULE: a BOUND row IS the value binding, three parts on the row: (1) the value with its uncertainty exactly as the run reported it, (2) the run provenance: which run, which specification, which QA file, each BY PATH from the project root, resolving on disk, (3) the claim update: which claim consumed it and what its status became. A number whose provenance line is missing is a HOLE, not a result; the row stays ⬜ however right the number looks. A number typed from memory binds nothing. -->

### A1 · 🚪 The register closes
- A1.1 · Every register row ends BOUND, DEFERRED, or WITHDRAWN.
  **Done when:** no row is ⬜, every BOUND row carries its three-part value binding, and each provenance path resolves on disk.

## States

### A1 · 🚪 The register closes
- ⬜ A1.1 · <the honest present: how many rows are open, and which numbers still lack a run behind them>

## Log

- <date> · [DRAFT-CC] register opened: <n> rows raised from <where the claim dependencies came from, e.g. the claim ledger>
<!-- RULE: Log lines wear the ruled grammar `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`, PHASE one of DRAFT PROBE REVISE CHECK. Typical lines on this route, in order: [PROBE-CC] entry ⏳ → probes/V<nn>-<topic>/<entry>.md, then [PROBE-CC] value binding written, row → BOUND, then [CHECK-CC] all rows terminal → CLOSE. The Log narrates and never carries evidence: bindings live on the register rows above, and the Log renders chip-free. -->
