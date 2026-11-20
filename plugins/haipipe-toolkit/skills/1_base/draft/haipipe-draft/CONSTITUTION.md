# haipipe-draft · Constitution

JL's feedback on draft pages, kept verbatim. It wins over SKILL.md; where they disagree, follow this file.


## A01 · The person's comments come first, every turn

> "reply my comments. /haistack every time pay attention to the comments I ahve and then update it my comments quickly." (JL 261118, chat, ScalingGlucose t02_results)

**Rule:** At the start of every turn on a draft Task, read its `draft/records/<stem>-comments.md`, and reply under each person comment that has no reply (fix the sentence and say what it reads now, or answer the question) before any other work.
**Why:** JL wrote Comment 27 on t02 s15 ("very hard to each? Which block and job you are referring too?") at 16:52 while the session ran a W4 round; nothing showed it, and it waited until JL asked in chat. The memory "reply comments every round" existed but no check enforced it.
**Class:** a person's page comment that sits unseen because no step of the session reads the comments file.
**Cases:** ✅ `page.py health` row `comments` (every draft Task, every theme) · ✅ haipipe-paper-draft `cli/section_workflow.py` prints it as the next step before W1 to W5 · ✅ a Paper's t02 Comment 27 replied and s15 rewritten · ✅ a Grant Page in another SPACE: a frozen snapshot from 2026-11-13, answered in its live copy on 2026-11-15, left out of the sweep · ✅ Physician AgreeableRx t03_theory Comment 2 (replied by its session) · ✅ a comment whose State is done or closed is skipped
**Check:** a person Note with no Reply after it shows as a `comments` WARN in `page.py health` (FAIL with `--final`) and as the first `next:` line of the Section workflow.
**Run:** `cd plugins/haipipe-toolkit/skills/1_base/draft/haipipe-draft && python3 -m pytest -q tests/test_comment_health.py`
**Status:** solved 261118
**Solved by:** `src/comment_health.py`: the health row; `section_workflow.py`: comments first
**Report:** constitution/A01-comments-first.md
