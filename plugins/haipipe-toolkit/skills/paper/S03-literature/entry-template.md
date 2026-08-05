<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S03-literature/probes/L<nn>-<topic>/<n>-<slug>.md, where <n> restarts at 1 inside each L<nn>-<topic> folder: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished record. Delete this top line too. -->
# <the neutral question, in a few words>
requires: <topic-page-id, e.g. S-Literature-2>

<!-- RULE: this file is a probe QA (the entry record), a RECORD and not a board page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry." One conversation, two QAs: the bank QA is the original, the probe QA is the paper's copy that points at it through **target**:. The digit-first filename is the hiding mechanism: the board's page sweep discovers only Q/S/Agent/Meeting prefixes, so <n>-<slug>.md never lands on the board. A probe QA carries no page frame: no state: header, no Opening, no Stage Contract, no Aims, no States, no Log; the topic page owns the register row, the human gate, and the Log lines about this record. -->
<!-- RULE: requires: names the ONE direct topic page whose register raised this probe QA. The checker fails any record beneath probes/ whose requires: is not a topic page owning a ### Q-consumer register. -->

#### q-executor
<!-- RULE: the question with the stake STRIPPED: no claim ids, no "our paper", no hint of which verdict would rescue what. The stake stays on the topic page's register; this is the neutral question another system can answer. State the deliverable and what counts as an accepted answer. -->
<The neutral question a discovery bank can answer without knowing why it matters.>
Deliverable: <what must come back, e.g. a prior-art digest naming the closest study on each half>.
Accepted: <the answer shapes that count, e.g. occupied (name the study) | unoccupied (name the nearest neighbors)>.

#### consumer trace
<!-- RULE: audit copy only, never a second register. One line per consumer question id, with the stake as the register states it; every id written here must appear in the parent topic page's register, and the checker verifies that. -->
* **Q-<Stage>-<n>**: <the stake this id carries, copied from the register for audit>

#### bank binding
<!-- RULE: route and bank say where the question went; target is the bank QA, the original file the bank answers at, written as a path from the project root. The **state**: line is the queue, one lowercase value on its own line: planned | commissioned | deferred are queued; read | answered-local are resolved. -->
**route**: discovery
**bank**: <run | reuse | new> · discoveries/<discovery-group>/<discovery-folder>/
**target**: discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
**state**: planned

#### a-executor
<!-- RULE: what came back, harvested from the bank QA at target, still in neutral language: findings, sources, caveats, scope. Empty until the bank answers. This probe QA IS the evidence store; the topic page's register row interprets it, never replaces it. -->
<empty until the answer lands>
