# b33 · Evidence

board-kind: task-block
package: plugins/haipipe-toolkit
shared-blueprint: b01_haipipe-toolkit
spine: What backs each sentence in any draft, report or slide, and how it is found: CITE cards from discovery Runs (external) and WORK cards from work Runs (internal), each a topic holding items tied to their sentences and anchor words, read from the Runs on every build, and missing evidence turned into flagged proposals a person ticks.
close: haipipe-evidence reads, checks and proposes for one real Section (b21 C2) and one other kind of page; haipipe-draft-evidence is retired in steps; every recorded question has a report Page with an answer status.

## Topic

JL 261016: "I think we need to put them out, like we also have the haipipe-draft and haipipe-display, so it will be
natural to have the haipipe-evidence, like we can find the evidence we need, in many other scenarios"; then "I think you
should create the b33_evidence in Tools/blueprints for this purpose". The skill was born inside b32_draft (s41, s21) and
on b21's C2 Section canvas (WellDoc-SPACE, Project-SHIFT-Study, b21 s05); this Block is its own home.

What is settled so far (261016): two kinds of card by where the evidence comes from, CITE (a discovery Task or Job:
papers, and any value or figure a paper reports; blue, external) and WORK (a work Task or Job: our own Runs; violet,
internal); one card is one topic holding many items; each item names its sentences (`for`) and the exact words it
backs (`anchor`, boxed in the text); cards run in narrative order; a missing item is red and carries `propose`, which
`cards.py propose` turns into a flagged proposal (a new Run, Task, Job or Studio topic, "proposed by evidence", for a
stated purpose) that a person ticks; a draft Task keeps `draft/`, `evidence/` (`cards.yaml`, `proposals.md`) and
`display/` side by side, one writer each. The skills (split 261016, JL: "I think we might want to separate them now"): the door
`skills/1_base/evidence/haipipe-evidence/` (card format, order, proposals, `scripts/cards.py`, a Page's evidence Runs),
with `haipipe-evidence-cite` (CITE: discovery Runs) and `haipipe-evidence-work` (WORK: work Runs) beside it, as
display has its renderers.

Open: retiring haipipe-draft-evidence in steps (new pages first, EMBED into the draft, Proj21's four Page evidence Runs
become cards, then the skill goes); WORK cards on a real Section; the Page workbench's Evidence Space reading
`evidence/`; `page.py` making `evidence/` and `display/` for a new Task; evidence for a report and for slides.

Excluded: how a sentence is written (b32_draft, haipipe-draft-writing) and judged (haipipe-draft-review); how a figure
is drawn (haipipe-display); running a discovery or work Task itself (haipipe-discovery, haipipe-task).

## Questions

```yaml
questions: []
```
