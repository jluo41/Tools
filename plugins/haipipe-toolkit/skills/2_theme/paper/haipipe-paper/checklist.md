# Paper checklist · where a paper stands, from its question to the send

JL 261031: "here we should also try to add the checklist.md, so everytime, the haipipe-paper we can have the things
like check the progress"; JL 261101: "what is the final checklist we should have? what is the delivery, and what is
the delivery requirements"; "make the checklist to be a sNN as well". One line per thing a paper needs, in the four
layers' order (SKILL.md § Four layers), with ⓪ Layout before them and ⑤ Delivery after. Every line a file can prove
is ticked by `scripts/paper_check.py <Paper-Board>`; the rest are the person's call (🙋).

Each paper Board keeps it as a topic, `sNN-paper-checklist/` (s05 when free): `paper_check.py <Board> --write` ticks
it into that face below its GENERATED line, so the Studio and the workbench show where the paper stands. What is
above the line (Decided, Open) stays the person's. `paper_ladder.py update` makes the topic when it is missing.

```text
✅ done     ⏳ under way     ⬜ not yet     🙋 waits on a person
```

## ⓪ Layout · is the folder on the latest layout?

`paper_ladder.py audit <Board>` prints these; `paper_ladder.py update <Board> [--date MMDD] [--apply]` fixes them in
order (a dry run without `--apply`), each step a script with its own rollback.

| id | what | done when | update's step |
|---|---|---|---|
| L1 | Pages are topics and Jobs | no `A1-Story/`, `Ba-`/`Bb-`/`Bc-` page folder or `studio/` left | `carry_over/migrate_paper.py`, `topics_paper.py`, then `sweep_names.py` |
| L2 | Versions dated, Sections tNN | no `jNN_v<N>_` version, no `S-…` Section folder | `carry_over/rename_tasks.py --date MMDD` |
| L3 | Writing Jobs named | no `jNN_v<MMDD>_<desk>/`: it is `jNN_writing_v<MMDD>_<desk>/`, from j11 | rename the Job and its `delivery/` folder, sweep the name |
| L4 | The checklist topic | `sNN-paper-checklist/` exists | make it (haipipe-studio `new_topic.py`), then `paper_check.py --write` |
| L5 | Faces the views read | the Story has its Task Roadmap (T) and Discovery Roadmap (D) tables, §8 Section Narrative opening with `#### Story arc`, and per-Section rows (§8 or a version's `## Narrative`); the data-flow topic its `-drawing.yaml` | 🙋 haipipe-paper-story, haipipe-paper-plan |
| L6 | Pages say their use | `board.md`, every Job face and every Task face has a `use-case:` line (the b16 matrices' word) | update writes it |

Missing evidence Jobs (V1) are made by update too (`paper_ladder.py evidence`).

## ① Plan · the paper Board's own topics

| id | what | done when |
|---|---|---|
| P1 | The question | `board.md` has `spine:` and `close:` filled (no `<…>`) |
| P2 | The idea | the ideation topic (`sNN-ideation/`) exists |
| P3 | The story | `board.md` `story-current:` names a topic that exists |
| P4 | The telling chosen | the story face has no open sign line (`**G0:** ⬜`) |
| P5 | The venue | `venues/<venue>/call.md` exists for `board.md`'s `venue:` |
| P6 | The data flow | the data-flow topic (`sNN-paper-dataflow/`) exists |
| P7 | The paper flow | the paper-flow topic (`sNN-paper-workflow/`) exists |
| P8 | The related work | the related-work topic (`sNN-related-work-…/`) exists |
| P9 | The display plan | `s06-paper-displays/` plans every display, and `display_plan.py check` finds none against the venue's display rules |

## ② Explore · the Blocks that support the paper

| id | what | done when |
|---|---|---|
| E1 | Work Blocks named | the Board's pages name at least one `work/bNN_…` that exists |
| E2 | Discovery Blocks named | the Board's pages name at least one `discovery/bNN_…` that exists |
| E3 | The Runs returned | the Story's Task Roadmap (`| T | work | where | state | …`) has no row still waiting (⏳ or ⬜) |

## ③ Evidence · what the paper quotes

| id | what | done when |
|---|---|---|
| V1 | The evidence Jobs | `j01_evidence_display`, `j02_evidence_value`, `j03_evidence_cite` exist |
| V2 | Displays drawn | every display Task's `status:` says drawn (or accepted) |
| V3 | Values filled | every value Task's newest Run wrote `result/values.yaml` (haipipe-paper-evidence `values_ledger.py`), else its `status:` says filled (or checked); differ, missing and owed counts are noted |
| V4 | Citations checked | every claim Task of `j03_evidence_cite` (t99 aside) finds all its keys verified in its newest Run (haipipe-paper-evidence `cite_tasks.py`), else its `status:` says checked |
| V5 | Numbers agree | haipipe-paper-evidence's `evidence_ledger.py` on the newest writing Job finds nothing to fix (❗), its value checks included (a printed value with no Run, from a screen read, or whose binding differs) |
| V6 | Displays say their message | each printed display (the newest writing Job's `display/Display<n>-*/`) has a `## Message` in its drawing Run's `result/method.md`: what we want to say with it (haipipe-paper-evidence, the display checklist) |
| V7 | Examples compared | the Board has an `sNN-paper-display-examples` drawing of the venue's published displays |
| V8 | Display questions answered | no collection Run (haipipe-interaction) under `j01_evidence_display` is `waiting` |
| V9 | Displays accepted | each printed display's unit README says `accepted: yes`, by a person (a blind review that passes is V5's) |

## ④ Writing · one Job per send

| id | what | done when |
|---|---|---|
| W1 | A writing Job | a `jNN_writing_v<MMDD>_<desk>/` (or an older `jNN_v…`) exists |
| W2 | Plans signed | each Section's newest draft says `approved: ✅` |
| W3 | Text written | each Section's newest draft has no `⟦…⟧` placeholder left |
| W4 | Paper built | `delivery/<writing Job>/build-manifest.json` exists |
| W6 | 📚 Examples read first | each Section of the newest send has 3 to 4 published papers of its article type read, or says `examples: none · <reason>`; made before the words (haipipe-paper-draft § Examples first) |
| W5 | Nothing waits on a person | no waiting question set (`runs/rNN_collect_*`, status waiting) on the Board |

## ⑤ Delivery · the package of the newest send, and its requirements

The delivery is what one send hands over: the manuscript (PDF and Word), the supplement when the venue takes one,
the cover letter, the venue's own files (its author kit: title page, declarations, data sharing, code link), and the
receipt, `delivery/<writing Job>/build-manifest.json`, the one record of what was built and from what. What is
uploaded is the portal packet, `delivery/<writing Job>/portal/` (JL 261102: "the final delivery content that are
ready to submit directly in the portal"): the build copies each file the portal takes there, one row per upload slot
in its `portal.md`, with the slot's state. Each line
names where its rule lives; the checklist never copies a rule.

| id | what | done when | the rule lives in |
|---|---|---|---|
| D1 | The manuscript | the manifest's `pdf` and `docx` outputs exist | haipipe-paper-assemble § Required outputs |
| D2 | The supplement | every supplement output the manifest declares exists (none declared is fine) | haipipe-paper-assemble |
| D3 | The cover letter | a letter Task in the writing Job, built by the paper's build (`[coverletter]` and `[outputs] cover_letter_pdf / _docx` in paper-build.toml), so it shows in the Writing view's assembled paper | haipipe-paper-assemble § The cover letter lane |
| D4 | The venue's desk rules | main-text words within `call.md`'s limit, no desk rule still UNKNOWN, built with the venue's own profile | `venues/<venue>/call.md` (haipipe-paper-venue) |
| D5 | Clean text | no `⟦…⟧` placeholder in the built Sections | AGENTS.md § Papers: deliverables carry no process text |
| D6 | Citations verified | no `\citep{TOADD}`, no draft citation, every key resolves; each Task's `draft-bibliography:` is its own `draft/evidence/bibex/<task>.bib` | haipipe-paper-evidence |
| D7 | The build is ready | the manifest's status is not `DRAFT` (its blockers listed) | `ref/submission-readiness.md` (G4, the 21 SUB-* points) |
| D8 | The portal packet | `delivery/<writing Job>/portal/portal.md` lists every slot the portal asks for, each ✅ ready (none missing, stale or built but not approved) | haipipe-paper-assemble § The portal packet |
| D9 | The portal fill page | a `jNN_submission_…` Job says `for: <writing Job>`, a real walk replaced its starter, `delivery/<that Job>/portal-fill.html` is newer than its fields and values, with no ❗ or ⬜ (🙋 while a person still decides); made by `scripts/portal_fill.py` | haipipe-paper § The submission Job |
| D10 | Read and approved | 🙋 the final read (paper, cover letter, supplement) came back clean, then a person reads the built paper and approves this exact build | haipipe-paper-assemble § The final read; `ref/submission-readiness.md` § Human reading pass |
| D11 | Sent | `delivery/delivery.md` has a `sent` row for the writing Job; only a person writes it | haipipe-delivery |
