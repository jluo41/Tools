# haipipe-evidence · Changelog

## 0.4.0 · 2026-10-16 · CITE and WORK become their own skills (JL 261016)

- `ref/cite.md` and `ref/work.md` move out as the sibling skills `haipipe-evidence-cite` and `haipipe-evidence-work`
  (JL: "could we have the haipipe-evidence-work and haipipe-evidence-cite ... separate them now"). This skill stays
  the door: card format, narrative order, proposals, `scripts/cards.py`, a Page's evidence Runs.

## 0.3.0 · 2026-10-16 · A Page's evidence Runs fold in (s41-D11)

- The skill haipipe-draft-evidence (LAND, EMBED; `run-value|display|citation-<slug>`) is now `ref/page-evidence.md`; its
  changelog is `ref/history/haipipe-draft-evidence-CHANGELOG.md`. Run names and the agent name are unchanged.
- New section A Page's evidence Runs; its triggers join the description (JL 2026-10-16).

## 0.2.0 · 2026-10-16 · evidence/ beside draft/ and display/ (JL 261016)

- Cards live in the Task's `evidence/cards.yaml`, proposals in `evidence/proposals.md`; `cards.py` reads a
  cards.yaml directly (`load()`), and a face with `--key` still works. b21's C2 cards moved there from s05's face.

## 0.1.0 · 2026-10-16 · A skill of its own (JL 261016)

- New skill beside haipipe-draft and haipipe-display (JL 261016: "it will be natural to have the haipipe-evidence ...
  in many other scenarios"; one skill, CITE and WORK as two ref pages).
- `scripts/cards.py`: resolve a CITE (discovery/) or WORK (work/) address to its folder or Run result, both work-Run
  layouts; read a paper's title and citation from its `.bib`, quoted facts from `facts.md`, a work value by
  `file` + `key`; `order()` by narrative; `check()` every address, fact, value and anchor; `propose` writes
  `evidence-proposals.md` with flagged proposals (run, task, job, topic), ticks kept by id.
- Moved here from b21 s05's builder, which now imports it.
