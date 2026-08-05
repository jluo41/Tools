<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S04-value/probes/V<nn>-<topic>/<n>-<slug>.md, where <n> restarts at 1 inside each V<nn>-<topic> folder: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished record. Delete this top line too. -->
# <the neutral computation, in a few words>
requires: <topic-page-id, e.g. S-Value-1>

<!-- RULE: this file is a probe QA (the entry record), a RECORD and not a board page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry." One conversation, two QAs: the bank QA is the original, the probe QA is the paper's copy that points at it through **target**:. The digit-first filename is the hiding mechanism: the board's page sweep discovers only Q/S/Agent/Meeting prefixes, so <n>-<slug>.md never lands on the board. A probe QA carries no page frame: no state: header, no Opening, no Stage Contract, no Aims, no States, no Log; the topic page owns the register row, the human gate, and the Log lines about this record. -->
<!-- RULE: requires: names the ONE direct topic page whose register raised this probe QA. The checker fails any record beneath probes/ whose requires: is not a topic page owning a ### Q-consumer register. -->

#### q-executor
<!-- RULE: the computation with the stake STRIPPED: no claim ids, no "our paper", no target value, no hint of which result would rescue what. The stake stays on the topic page's register; this asks for the computation in neutral terms. State the deliverable and what counts as an accepted answer, including the honest refusal shape. -->
<From <the existing task's outputs or the data it may touch>, emit <the exact statistics or estimates wanted>.>
Deliverable: <the numbers with their source paths, in a QA digest>.
Accepted: <all emitted with provenance | not producible from this source; name which and why>.

#### consumer trace
<!-- RULE: audit copy only, never a second register. One line per consumer question id, with the stake as the register states it; every id written here must appear in the parent topic page's register, and the checker verifies that. -->
* **Q-<Stage>-<n>**: <the stake this id carries, copied from the register for audit>

#### bank binding
<!-- RULE: route and bank say where the computation went; target is the bank QA, the original file the bank answers at, written as a path from the project root. The **state**: line is the queue, one lowercase value on its own line: planned | commissioned | deferred are queued; read | answered-local are resolved. If the wanted aggregate cannot come from the bound export, say so here and DEFER rather than fabricating. -->
**route**: task
**bank**: <run | code | reuse | new> · tasks/<task-group-or-folder>/
**target**: tasks/<task-folder>/QA/<n>-<slug>.md
**state**: planned

#### a-executor
<!-- RULE: what came back, harvested from the bank QA at target, still in neutral language: each figure with its uncertainty and its source path, plus every caveat the run recorded. Empty until the bank answers. This probe QA IS the evidence store. A figure the export cannot produce is written NOT ANSWERABLE with the reason, never estimated. -->
<empty until the answer lands>
