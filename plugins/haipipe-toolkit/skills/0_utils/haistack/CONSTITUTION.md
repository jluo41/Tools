# haistack · Constitution

JL's feedback on /haistack itself, kept verbatim. It wins over SKILL.md; where they disagree, follow this file.


## A01 · Every article has a report, and the report is seen

> "and for each time, we should have a report, to explain what is the need, what current things do, and why current settings doesn't support it. and what is the methods to update, how do we update it, and what this methods can avoid the next time we will not have this problem again, do you get it?" (JL 261118, chat)
> "and for this information, how do we save it in the disk folder, and how to present them in the UI? that is also the questions." (JL 261118, chat)

**Rule:** Every article links a report `constitution/A<NN>-<slug>.md` with six parts (Need, Now, Gap, Methods, Update, Never again), and every SPACE Home lists every article under 📜 Constitution, opening its report.
**Why:** The first articles kept JL's words and the rule, but not why the old setup failed or why the fix will hold, and they could be read only in the repo.
**Class:** a rule whose reasons are not kept, or are kept where JL never looks.
**Cases:** ✅ haistack A01 · ✅ haipipe-studio A01 · ✅ haipipe-studio A02 · ✅ haipipe-studio A03 · ✅ haipipe-studio A04 · ✅ SPACE Home in Tools-SPACE · ✅ SPACE Home in a SPACE with Tools/ inside
**Check:** `--check` marks ❗ an article whose report is missing; the Home lists every article.
**Run:** `python3 plugins/haipipe-toolkit/skills/0_utils/haistack/scripts/constitution.py --reports`
**Status:** solved 261118
**Solved by:** `scripts/constitution.py`: --check requires the report; `servers/workbench/page/space_constitution.py`: Home section
**Report:** constitution/A01-a-report-each-time.md
