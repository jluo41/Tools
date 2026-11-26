# workbench-paper · Constitution

JL's feedback on the paper workbench, kept verbatim. It wins over SKILL.md; where they disagree, follow this file.


## A01 · Every Delivery item names its artifact

> "could you udpaet the name? … call it Paper-Latex, and Paper-Latex-Diff, you need to udpate it to the skills, using /haistack for it." (JL 261121, chat, with screenshots of the Paper Board's Delivery › LaTeX list showing "The paper" and "Changes since the last round")

**Rule:** Every item in the paper panel's Delivery lists is named by its artifact, as a hyphenated Kind-Lane[-Variant] name (Paper-Latex, Paper-Latex-Diff, Paper-Word), and the name shown in the list is the item's full name.
**Why:** The list showed "The paper" under both LaTeX and Word and "Changes since the last round" for the diff, so a reader could not tell the LaTeX PDF from the Word file, nor name the diff to a co-author.
**Class:** a delivered artifact shown under a generic description instead of its own name.
**Cases:** ✅ Paper-Latex · ✅ Paper-Latex-Diff · ✅ Paper-Word · ✅ Paper-Word-Tracked · ✅ Supplement-Latex · ✅ Supplement-Word · ✅ Combined-Latex · ✅ Cover-Letter · ✅ Portal · ✅ haipipe-paper-assemble `ref/latex-diff.md` (names the diff item)
**Check:** `TAB_GROUPS` in `servers/workbench-paper/board_writing.py` holds only artifact names whose shown name equals the full name, includes Paper-Latex and Paper-Latex-Diff, and no old generic name is written.
**Run:** `python3 -m pytest -q plugins/haipipe-toolkit/servers/workbench-paper/tests/test_delivery_item_names.py`
**Status:** solved 261121
**Solved by:** `servers/workbench-paper/board_writing.py`: TAB_GROUPS and item names renamed
**Report:** constitution/A01-delivery-item-names.md
