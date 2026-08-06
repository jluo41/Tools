<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S04-value/probes/V<nn>-<topic>/<n>-<slug>.md, where <n> restarts at 1 inside each V<nn>-<topic> folder: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished record. Delete this top line too. -->
# <the neutral question, in a few words>
requires: <evidence-page-id, e.g. S-Value-1>

<!-- RULE: this file is a QA-probe, a RECORD and not a board page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry." One conversation, two QAs: the QA-bank is the original, the QA-probe is the paper's stub that points at it through **target**:. The digit-first filename is the hiding mechanism: the board's page sweep discovers only Q/S/Agent/Meeting prefixes, so <n>-<slug>.md never lands on the board. A QA-probe carries no page frame: no state: header, no Opening, no Stage Contract, no Aims, no States, no Log; the evidence page owns the E<n> division that points here, the consumer rows, the human gate, and the Log lines about this record. -->
<!-- RULE: requires: names the ONE direct evidence page whose E<n> division owns this QA-probe; exactly one division points here (1:1). The checker fails any record beneath probes/ whose requires: is not an evidence page carrying the head route: line. -->

#### Q-executor
<!-- RULE: the computation request with the stake STRIPPED: no claim ids, no "our paper", no hoped-for direction. The stake stays on the evidence page's consumer rows; this is the neutral request another system can run. State the deliverable and what counts as an accepted answer. The four slot words are capitals: Q-executor; consumer trace and bank binding are not among them and stay lowercase. -->
<The neutral computation request a task bank can run without knowing which claim it rescues.>
Deliverable: <what must come back, e.g. the estimate, its SE and CI, N, and the spec that produced them>.
Accepted: <the answer shapes that count, e.g. an answered QA file whose numbers grep in the run's own results files>.

#### consumer trace
<!-- RULE: audit copy only, never a second consumer surface. One line per consumer question id, with the stake as the evidence page states it; every id written here must appear on the parent evidence page, and the checker verifies that. -->
* **Q-<Stage>-<n>**: <the stake this id carries, copied from the evidence page for audit>

#### bank binding
<!-- RULE: route and bank say where the question went; target is the QA-bank, the original file the bank answers at, written as a path from the project root. The **state**: line is the queue, one lowercase value on its own line: planned | commissioned | deferred are queued; read | answered-local are resolved. -->
**route**: task
**bank**: <run | reuse | code | new> · tasks/<task-group>/<task-folder>/
**target**: tasks/<task-group>/<task-folder>/QA/<n>-<slug>.md
**state**: planned

#### A-executor
<!-- RULE: what came back, harvested from the QA-bank at target, still in neutral language: the numbers, their uncertainty, run pointers, caveats, scope. Empty until the bank answers. This QA-probe IS the evidence store; the evidence page's consumer rows interpret it, never replace it, and its answer digest quotes 2-3 lines at most. -->
<empty until the answer lands>
