# Paper build

How hai-paper-assemble prints a paper for its venue: the LaTeX PDF and the Word file.

## 🗂 Topic: Paper build ▸ one folder per venue

How to PRINT for one venue lives in one folder, `hai-paper-assemble/venues/<venue>/`, and the shared scripts
never name a venue. How to WRITE for a venue stays in `skills/3_theme/paper/venue/` (playbooks). Rule and contract:
`hai-paper-assemble/venues/README.md`.

```text
BEFORE                                   AFTER
profiles/<venue>.toml                    venues/<venue>/profile.toml
scripts/venue_jama.py                    venues/jama-internal-medicine/venue.py  (build_word)
styles/jama-ama.bst                      venues/jama-internal-medicine/jama-ama.bst
(none)                                   venues/<venue>/test_<venue>.py
if layout == "jama-internal-medicine"    if "build_word" in globals()
JAMA = ... (build_delivery.py)           [latex] title_block, section_headings, abstract_as_written,
                                         supplement_float_names (in the JAMA and Lancet profiles)
```

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | "for each venue, you can make a module folder"; after the proposal, "yes, please go ahead" (a venue's pieces sat in 3 places; `latex_room_to_docx.py:1667` and `build_delivery.py:280, :331` named JAMA; no venue had a test) | JL via AgreeableJama-Board Report (topic 1) | the move above; JAMA first, then MISQ and the Lancet, a move with no rewrite; `tests/test_venues.py` fails if a shared script names a venue |

Check: old engine against new on scratch copies of Paper-AgreeableOpioid-Jama (JAMA), Paper-PersonalityPDMPMandate
(Lancet) and Paper-LLMRecPhy-Misq (MISQ). Every Word file's text identical; every `master.tex` identical but the
one new line of the next topic; every PDF the same characters. State: fixed.

## 🔣 Topic: Paper build ▸ a copied semicolon is a semicolon

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | in `delivery/j11_writing_v1130_jama-im/latex/Paper-AgreeableOpioid-Jama.pdf` every semicolon copies as U+037E (Greek question mark), so a search for ";" fails (Report topic 3) | AgreeableJama-Board Report | cause: Times New Roman maps ";" and U+037E to one glyph and XeTeX's reverse map picked U+037E; every master, paper-owned head and cover letter now starts with `\XeTeXgenerateactualtext=1`; on the JAMA paper 150 U+037E became 0 and 180 copy as ";" |

State: fixed. Guard: the line is in the engine's generated head (`build_delivery.py` `ACTUALTEXT`), written in
`ref/venue-format.md`; `word_compare.py` also folds U+037E, so an older PDF still compares.

## 🔖 Topic: Paper build ▸ the Word copy cites as the PDF

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | the Word export prints "Lu and Rui" where the PDF has "Lu & Rui", and "(Centers for Medicare & Medicaid Services, 2026; Centers for Medicare & Medicaid Services, 2026)" where the PDF has "2026a, 2026b" (Report topic 3a) | Pp-AgreeableRx-Discrention Report | `scripts/bbl_labels.py`: Word reads each label from `master.bbl`; one author's works share one name; `tests/test_bbl_labels.py`; on a scratch copy the Word file now matches the PDF |
| 11-22 | "Appendix D heading lands before Tables C2-C5" (later withdrawn by the peer: Word's own view showed the right order) | Pp-AgreeableRx-Discrention Report | on the scratch copy the body did hold C2 to C5 under Appendix D; `place_held` now stops at the next Heading 1; the held-display code moved to `scripts/docx_held.py` |
| 11-22 | "Manuscript (Word)" slot beside the PDF; JL: one manuscript only (topic 3c) | Pp-AgreeableRx-Discrention Report | `ref/portal-packet.md`: one manuscript slot only |

State: fixed. Open: no unit test drives `place_held` (it needs Word); the guard rests on the scratch run.

## 🖥 Topic: Paper build ▸ a build never uses the person's open Word

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | "the word app keeps jumping ... opened, and then closed": every build printed through JL's Word, open 36 hours with shared OneDrive files | Pp-AgreeableRx-Discrention bug report | the 19:54 to 20:48 builds were this session's acceptance builds on scratch copies; `word_lock.word_in_use()` now keeps every build out of a Word holding the person's documents (`HAIPIPE_WORD_PREVIEW=word` forces it); checked on this Mac with Word open |

State: fixed. Guard: `tests/test_bbl_labels.py::test_a_build_leaves_a_word_in_use_alone`.

## ✉️ Topic: Paper build ▸ the cover letter: one page, each sentence once

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | JL folded "I submit this manuscript on behalf of my co-authors ..." into his closing paragraph in Word; the build printed it twice (blocking "settle 2") | Pp-AgreeableRx-Discrention | `cover_letter.py` adds its own sentence only when no paragraph says "on behalf of"; `tests/test_cover_letter_on_behalf.py` |
| 11-22 | "why the cover letter is ... not one page in the submission" (page 2 held only "Sincerely," and the signature) | JL via Pp-AgreeableRx-Discrention | the closing is one block; a spill shrinks space, then the type to 11 pt; the Word copy follows; check "letter fits one page"; `tests/test_cover_letter_fit.py`; the real letter went from 2 pages to 1 |

State: fixed.

## 📮 Topic: Portal ▸ a repository URL is not a MISQ submit blocker

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | the plan said "aggregated output at [repository URL]" and the portal ask "add the repository URL", read as a Submit blocker; on MISQ's form (Updated September 6, 2023) the URL star is under Choice 2 only; call § 4.6: deposit at acceptance (Report topic 3) | Pp-AgreeableRx-Discrention Report | desk rule `venue/bank/1-QBv-desks/QBv1-misq/transparency.md` (Choice 4: "deposited in a public repository when the paper is accepted"); `hai-paper/ref/submission-readiness.md` § 5 check; the paper's portal-values.yaml fixed by the peer |
| 11-22 | the form text from the paper's local copy (Updated: September 6, 2023) and `venues/MISQ/call.md` line 62; "A check that flags a portal ask asking for a URL while choice 3 or 4 is picked is still yours" | Pp-AgreeableRx-Discrention | reread the PDF with pdftotext: URL only under Choice 2; desk rule closed; `portal_fill.py` `url_unasked` marks such an answer "disagree"; `tests/test_portal_fill.py` (18); the current values pass, the old "[repository URL]" wording is flagged |

State: fixed. Guard: `tests/test_portal_fill.py::test_an_alternative_plan_that_asks_for_a_url_disagrees`.

## 🧱 Topic: Paper build ▸ a new version prints every Section's words

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-22 | j13 face's compile-order block was a numbered list, "invalid compile-order entry" (topic 1) | LLMRecJamaAI-Board Report | `paper_ladder.py task` writes each Section into the block (`version_face.py order_add`); the error shows the form |
| 11-22 | j13 copied drafts but not t02, t04, t21's `draft/evidence/bibex/*.bib` (topic 2) | LLMRecJamaAI-Board Report | cause: j13 was made with `version` and hand copies; `next --from` carries draft/ whole (all four .bib on a scratch Board copy); `version` now says so |
| 11-22 | three Sections printed 28 words from placeholder Content, the build said DRAFT with no warning; a 1,397-word paper nearly went to co-authors (topic 3) | LLMRecJamaAI-Board Report | `delivery_words.py unadopted`: `build.py check` ❗ and build ⚠ name the Section and "page.py adopt"; a G4 blocker |
| 11-22 | `\section{Discussion}` then `\subsection{Discussion}` (topic 4) | LLMRecJamaAI-Board Report | fixed by the peer: `md2docx_page.py chapter_titles` drops a part named like its Section; `test_md2tex.py` |

State: fixed. Guards: `tests/test_delivery_words.py`, `tests/test_paper_ladder.py::test_version_task_and_run`, `exporters/test_md2tex.py::test_a_chapter_named_like_its_section_is_no_subsection`.

## 🔗 Topic: Paper build ▸ a JAMA reference prints its DOI

| Date | Words | From | What changed |
| --- | --- | --- | --- |
| 11-23 | "Web references print without their URL" (`NYSDOH2026NDCMME`, `ccw_chronic_conditions`; `jama-ama.bst` suspected) (topic 2) | AgreeableJama-Board Report | master.bbl, PDF and Word all print both URLs; the real gap: the venue named no `bibstyle`, the paper set `vancouver`, which prints no DOI (34 references); `venues/jama-internal-medicine/profile.toml` `bibstyle = "jama-ama"`; the paper drops its own `bibstyle` line |

State: fixed in the venue; the paper's own `bibstyle = "vancouver"` and its two "Accessed: 2026-08-21" notes are the
peer's. Guards: `venues/jama-internal-medicine/test_jama_internal_medicine.py::test_references_print_their_doi`;
`send_check.py` ❗ "the bib holds doi …, the reference prints none".
