# haipipe-evidence · Changelog

## [0.8.1] — 2026-10-26

Shorter description (1075 -> 541 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026b.yaml). (describe 261026b)

## [0.8.0] — 2026-10-26

Merged 2 helper skill(s) into `_parts/`: `haipipe-evidence-cite` -> `_parts/cite`, `haipipe-evidence-work` -> `_parts/work`. /haipipe-evidence reads `_parts/<name>/PART.md` instead of calling a separate skill; allowed-tools gained the parts' tools. Old commands map as `/haipipe-evidence-cite` -> `/haipipe-evidence cite`. (merge-parts 261026)

## 0.7.0 · 2026-10-21 · `cards.py bib`: the page's .bib from its cited Runs

- t01_introduction v0.5's LaTeX printed 8 of 10 citations as "?": its `draft/evidence/bibex/` held 2 entries kept by
  hand. `cards.py bib <cards.yaml> --draft <draft.md> --write` writes it from the draft's `\citep` keys in order, each
  entry copied from the one-entry .bib of the Run its CITE item names, a comment saying which Run and whether the entry
  is the Run's export or composed and waiting for a person; a key no CITE item names is reported, exit 1.

## 0.6.1 · 2026-10-21 · a fact may be a table's rows

- `facts()` read only a quoted sentence directly followed by ` Locator`, so Oca 2023's counts (b01.j01.t01.r20: T05 Table 1
  rows, T08 Table 3 rows) and a quote closed by a stop (T04 `". Locator`) were "no fact", and a card could not cite
  "84 of 240 not ophthalmologists". It now reads a quote with or without a stop after it, and a table's rows as written
  (no quotes). Every fact id named in Physician-SPACE's 18 cards.yaml files still reads.
- `work_value()` takes `len(<key>)`: it counts the entries there, so t01 S17's "6 AI agents from 3 companies" is read from
  b03.j03.t01.r04's `metrics.b_by_model` (6 keys), not typed (raised by t01's blind review, 261021).
- `by_topic()` merges two cards of the same Task into one, so a need written in its own block joins the Task's card
  (t01: Hanauer and the new survey need are one CITE card, b01.j02.t02).

## 0.6.0 · 2026-10-20 · VALUE, not WORK; a card is a topic

- JL 261020: "the work 1's name is not good ... I think the work here is more like something else?". The kind `work` is
  `value`, labelled VALUE (what the item is, a number our Run wrote); `kind: work` in an older file still reads as
  `value` (`cards.OLD_KIND`). Every Physician-SPACE cards.yaml (5 LLMRec, 13 MISQ) now says `kind: value`, and each
  proposals.md was rewritten by `cards.py propose --write` (no tick lost).
- JL 261020: "cite 1's name is very weird ... we might want to make it into different cite with the topic". `by_topic`:
  a needed item sits in the card of the Task its proposal would be made in (a Run in a Task: that Task's card; a new
  Task, Job or topic: a card named by it), so no card is a bag of "Sources still needed"; items in reading order, so an
  item's id (CITE 1.2) follows the text. LLMRec t01 is now CITE 1 · Medical hallucination and guardrail, CITE 2 · Patient
  choice and consultation demand, CITE 3 · Audits of LLMs naming real physicians, VALUE 1.
- A figure or table is a Display, shown in a draft Task's own step, 4 · Display.

## 0.5.0 · 2026-10-20 · `scripts/from_items.py`: an older Page's Evidence Items become cards

- JL 261020: "the workbench is not the latest", on Paper-AgreeablePrescriptionDiscretion, whose 14 Sections kept
  their evidence as `draft/<stem>-evidence-items.md`, so the draft Task's 3 · Evidence step showed nothing.
- `from_items.py <task>… [--write]` writes `evidence/cards.yaml` and `proposals.md` from the items: a Discovery
  Supporting Run gives a CITE item, an Execution one a WORK item, each keeping its `item:` id and label; `for` comes
  from §1's `- B<k> · S<n>` Bullets. A Run still to make, an address that no longer resolves (a Block that moved),
  or no Supporting Run gives one `need` per item; DISPLAY, deferred, dropped and retired items get no card.
- The Evidence Items file stays: the Page export reads it for its gates until haipipe-draft's exporter reads cards.
- First use: 13 Sections, 264 items, `cards.py check` clean on all 13 (t07 has no evidence to card).

## 0.4.0 · 2026-10-16 · CITE and WORK become their own skills (JL 261016)

- `ref/cite.md` and `ref/work.md` move out as the sibling skills `haipipe-evidence cite` and `haipipe-evidence work`
  (JL: "could we have the haipipe-evidence work and haipipe-evidence cite ... separate them now"). This skill stays
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
