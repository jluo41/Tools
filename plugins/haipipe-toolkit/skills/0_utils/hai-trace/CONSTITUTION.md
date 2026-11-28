# hai-trace · constitution

Each article is a rule the person gave, kept with their words. It wins over SKILL.md. How the Files pane draws a
trace stays in hai-ui's constitution (its trace-plan-and-states article); this file owns the trace file and the loop.

## A01 · Plan first: the files to change are listed and seen before any change

> "for a trace, to be recorded, what is the requirements, like we might have the plan, be clear about what to change, right? and think about what files to changed, what aims to achived, right?" (JL 261125, chat)
> "before my confirm, do not change files, I need to check what files you will change." (JL 261125, chat)
> "I hope next time, the things to change will be shown in [the Files pane]" (JL 261125, Files pane)

**Rule:** Before any file changes, the trace is written with its aim and plan (do, path, what for each file), the plan shows in the Files pane, and the person confirms; only then are the files changed.
**Why:** Files were changed before the person had seen which ones.
**Class:** a change made with no plan written, or a plan the person could not see before it ran.
**Cases:** ✅ every trace made by `trace.py new` · ✅ the Files pane marks planned files (◌, +) · ⬜ traces written by hand in other sessions
**Check:** every trace has an aim and a plan whose lines carry do, path and what.
**Run:** `python3 plugins/haipipe-toolkit/skills/0_utils/hai-trace/scripts/trace.py check`
**Status:** open (other sessions still write traces by hand)

## A02 · Every prompt toward the aim is listed, in the person's words

> "the prompt is limited, I think this prompt should be many, right? I asked many things." (JL 261125, Files pane)

**Rule:** A trace lists every prompt that worked toward its aim, with its time, as typed; it is named for the time of its first prompt.
**Why:** A trace kept only the first prompt, so what was asked along the way was lost.
**Class:** a trace whose Prompts part leaves out a prompt that shaped the work.
**Cases:** ✅ `trace.py prompt` adds one · ⬜ the chat hook writing prompts by itself
**Check:** a reviewer reads the Prompts part against the session.
**Status:** open

## A03 · A closed trace has its Check and Summary

> "is this like the plan or what?" (JL 261125, chat)

**Rule:** A trace is closed only with a Check (what was run or looked at, with its numbers) and a Summary (one paragraph), and its `changed:` list holds the files that changed.
**Why:** Work ended with nothing saying what was checked or what it came to.
**Class:** a closed trace with an empty Check or Summary.
**Cases:** ✅ `trace.py close` refuses an empty one · ✅ `trace.py changed` fills `changed:` from git
**Check:** every closed trace has a non-empty Check and Summary.
**Run:** `python3 plugins/haipipe-toolkit/skills/0_utils/hai-trace/scripts/trace.py check`
**Status:** solved 261125

## A04 · Every plan reply lists its files and waits for the go

> "have you update the skill of /hai-trace? which will tell you the AI will response and tel wich fiell which change" (JL 261125, chat)
> "before my confirm, do not change files, I need to check what files you will change." (JL 261125, chat)

**Rule:** The reply that proposes a change ends with every planned file, one line each (path and change), and the trace's path, then waits for the person's go; the reply after the change lists the files that changed and the checks run, with their numbers.
**Why:** The plan sat in a trace file while the reply did not say which files would change, so the person had to ask.
**Class:** a plan reply with no file list, or a change made before the go.
**Cases:** ✅ SKILL.md § The reply · ⬜ a hook that checks a reply before a change
**Check:** a reviewer reads each plan reply for the file list and the go before the first edit.
**Status:** open (no machine check of a reply)

