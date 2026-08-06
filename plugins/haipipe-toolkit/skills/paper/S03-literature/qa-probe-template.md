<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S03-literature/probes/L<nn>-<topic>/<n>-<slug>.md, where <n> restarts at 1 inside each L<nn>-<topic> folder: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished record. Delete this top line too. -->
# <the neutral question, in a few words>
requires: <evidence-page-id, e.g. S-Literature-2>

<!-- RULE: this file is a QA-probe, a RECORD and not a board page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry." One conversation, two QAs: the QA-bank is the original, the QA-probe is the paper's stub that points at it through **target**:. The digit-first filename is the hiding mechanism: the board's page sweep discovers only Q/S/Agent/Meeting prefixes, so <n>-<slug>.md never lands on the board. A QA-probe carries no page frame: no state: header, no Opening, no Stage Contract, no Aims, no States, no Log; the evidence page owns the E<n> division that points here, the consumer rows, the human gate, and the Log lines about this record. -->
<!-- RULE: requires: names the ONE direct evidence page whose E<n> division owns this QA-probe; exactly one division points here (1:1). The checker fails any record beneath probes/ whose requires: is not an evidence page carrying the head route: line. -->

#### Q-executor
<!-- RULE: the question with the stake STRIPPED: no claim ids, no "our paper", no hint of which verdict would rescue what. The stake stays on the evidence page's consumer rows; this is the neutral question another system can answer. State the deliverable and what counts as an accepted answer. The four slot words are capitals: Q-executor, consumer trace and bank binding are not among them and stay lowercase. -->
<The neutral question a discovery bank can answer without knowing why it matters.>
Deliverable: <what must come back, e.g. a prior-art digest naming the closest study on each half>.
Accepted: <the answer shapes that count, e.g. occupied (name the study) | unoccupied (name the nearest neighbors)>.

#### consumer trace
<!-- RULE: audit copy only, never a second consumer surface. One line per consumer question id, with the stake as the evidence page states it; every id written here must appear on the parent evidence page, and the checker verifies that. -->
* **Q-<Stage>-<n>**: <the stake this id carries, copied from the evidence page for audit>

#### bank binding
<!-- RULE: route and bank say where the question went; target is the QA-bank, the original file the bank answers at, written as a path from the project root. The **state**: line is the queue, one lowercase value on its own line: planned | commissioned | deferred are queued; read | answered-local are resolved. -->
**route**: discovery
**bank**: <run | reuse | new> · discoveries/<discovery-group>/<discovery-folder>/
**target**: discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
**state**: planned

#### A-executor
<!-- RULE: what came back, harvested from the QA-bank at target, still in neutral language: findings, sources, caveats, scope. Empty until the bank answers. This QA-probe IS the evidence store; the evidence page's consumer rows interpret it, never replace it, and its answer digest quotes 2-3 lines at most. -->
<empty until the answer lands>
