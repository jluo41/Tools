# A06 · A Job is a fixed workflow a command can close; a Studio topic is free design a person closes

**Need.** JL could not tell a Job from a Studio topic in b17. JL's own line: a Job is coding-heavy, a fixed workflow an
agent runs; a Studio topic is free-style thinking and design that JL drives.

**Now.** The split is drawn by who judges the end. A Job's `close:` is answered by a command or a test (tests pass, the
part shows on the page). A Studio topic ends when the person picks. Overlap is expected, because one piece of work moves
back and forth: a preview (Studio) is followed by "yes, do it" (Job), and so on.

**Gap.** 8 of 30 Job faces closed on a person's agreement ("all nine sNN are agreed", "b17-s01 is agreed"), so those
Jobs did the Studio's work.

**Methods.** `scripts/job_close_check.py` reads every `examples/*/work/*/jNN_*/jNN_*.md` close line and flags the words
that wait on a person (agreed, signed, approved, picked, JL says).

**Update.** b17 j01's close is now a fresh agent building the demo Block from the SKILL.md. b17 j03's close is the code
changes made, the tests passing, and each part showing on 5623. The check now reports 6 Jobs, all in other theme Blocks
(b11, b12, b15, b16, b35), left to their sessions.

**Never again.** The Run line fails while any Job's close waits on a person. new_job.py's prompt for `close:` should ask
for a check (still ⬜).
