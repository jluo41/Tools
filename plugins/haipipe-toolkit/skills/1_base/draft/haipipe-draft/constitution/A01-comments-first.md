# A01 · The person's comments come first, every turn

> "reply my comments. /haistack every time pay attention to the comments I ahve and then update it my comments quickly." (JL 261118, chat, ScalingGlucose t02_results)

## 1. Need
JL writes comments on a draft page in Draft Lab and wants each one answered quickly: the sentence fixed and a reply under the comment, without having to ask in chat.

## 2. Now
Comments are kept in `draft/records/<stem>-comments.md` (`### Comment N · <address>`, `State:`, `- Note · <time>: …`, `- Reply · <time>: …`). Before this change no script read that file for unanswered person notes: `page.py health` (`src/folder_health.py` `folder_health`) checked only `-discussion.md` threads (`check_threads`), and `cli/section_workflow.py` counted only open **AI** comments (`open_ai_comments`). On 261118 Comment 27 on t02 s15 waited about 30 minutes through a W4 round until JL asked.

## 3. Gap
Replying was a memory (`reply-comments-every-round`), not a step any tool showed. A session busy with a loop never reread the file, and nothing failed when a person note had no reply.

## 4. Methods
1. A memory or a SKILL.md sentence only: rejected, it already existed and was missed.
2. A `page.py health` row plus the Section workflow's `next:` line: chosen. Every round already ends in `health`, and the workflow script is read before each step, so the comment shows where the session looks.
3. A per-prompt hook that prints unanswered comments: would reach every turn, but it is harness config per SPACE and session; left as a later step if (2) is not enough.

## 5. Update
- `src/comment_health.py`: `unanswered()` and the health row `comments`.
- `src/folder_health.py`: calls `check_comments` after `check_threads`.
- `tests/test_comment_health.py`: person note, AI note, reply, a note after a reply, closed.
- haipipe-paper-draft `cli/section_workflow.py`: prints `next: 🙋 reply first, then fix: …` when a person comment waits.
- Cases: ✅ health row · ✅ workflow line · ✅ t02 Comment 27 replied · ✅ REACH-SPACE Grant-AITC-Dementia is a frozen snapshot from 2026-11-13, answered in the live WellDoc copy, left out · ✅ Physician AgreeableRx t03 Comment 2 replied by its session · ✅ a State of done or closed is skipped.
- Run: `python3 -m pytest -q tests/test_comment_health.py` → 2 passed.

## 6. Never again
A person comment without a reply is now a WARN in every `health` run and a FAIL at `--final`, so no draft Task can be called finished with one waiting, and the Section workflow names it as the next step before any rewrite round. `/haistack sweep` reruns the test.
