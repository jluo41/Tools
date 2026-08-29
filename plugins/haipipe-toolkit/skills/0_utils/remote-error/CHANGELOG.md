remote-error — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.6.0] - 2026-08-29

The trailing return block is GONE. JL pasted it back and said "I dont want this."

0.5.0 had made it the reply's signature: eleven `key: value` lines, no heading,
always last. Every one of those lines was already stated, in readable form, in
the five sections above it. The gate verdict was the GATE bullet, the issue id
and every landed path were 📄 The Report I Wrote, the canonical paths were WHERE,
the session name was in the issue file's own header. So the block was a second
copy of the whole reply written in a shape a person cannot read, and the last
thing their eye lands on.

It also broke the reply's own ending. 🙋 Your Call asks the person two questions;
burying them above a wall of machine text tells them the questions are not the
point. The reply now ends ON the question.

Nothing consumed the block. No agent calls this skill, and the "so a caller can
read the outcome without prose" justification named a caller that does not exist.

Deleted: the `Return block` section, its line in the shape diagram, the
"SIGNATURE" paragraph, and the trailing `· block` in the need-more-log shape.

**One thing the deletion broke, repaired in the same version.** The four
`status` values were DEFINED only inside the deleted block, while two other
places still cited them by name, so `status` was referenced and never defined
and a fresh reader could not learn that `fixed` and `environment-limit` were the
other two. JL: "fold the four values into your call." They now open
🙋 Your Call as an OUTCOME sentence, not a field: the run says which of the four
it reached and why, in words, using the same four words the register uses. The
dangling citation in 🛠️ was rewritten to point at that sentence.

**COMMIT AND PUSH stops printing the commands.** JL, handed the two git lines:
"don't need to show it as well, because we are more like what to do, and then
you will do it for me, I don't need to see the code here." He is deciding, not
typing. The question is now one plain sentence naming WHAT is committed and
WHICH repo or submodule it lands in, and on a yes this session runs the commands
and reports the commit line. Printing them was the assistant's work showing, and
it put a wall of git text under the one question the reply exists to ask.

**🛠️ reorders to WHERE, BEFORE, AFTER, WHY.** 0.5.0 had it as WHAT then WHERE,
so the reply opened with a fenced `// was` / `// now` pair and named the file
underneath it. JL: "for things here, it is not correct. How to make it starting
with the place, like xxxx file, line xx, before, xx, then after, xx." He is
right: a change is unreadable until you know where it is, and with two files
changed a reader cannot tell which block belonged to which. The section is now
one GROUP per file, each opening with the path and the line range on their own
line, then a `before` block, then an `after` block, then the rule. `WHAT` as a
label is gone; `before` and `after` say it without a word. A worked example of
the group was added so the shape is copyable rather than described.


## [0.5.0] - 2026-08-29

THE REPLY SHAPE is now part of the contract. Until now the skill said what the
five phases DO and left how they come back in chat to whoever ran it, so the
same run could return a wall of prose or a table, and neither was wrong.

JL settled three things about it:

1. **`🛠️ What I Changed, Where, And Why`, past tense.** JL first asked "you mean
   what you changes, and how could I change it? like which file which lines to be
   changed, right?", and the section was written as the person's to-do list. He
   corrected it: "So the skill should really change the code, do you got what I
   mean?" He is right, and phase 3 already said so: the skill EDITS the canonical
   file. A reply that hands the person a to-do list is describing work it was
   supposed to have done. The section is now three ordered parts, WHAT (old ->
   new, the smallest quotable unit), WHERE (full path, canonical or copy,
   file:line, copies synced), WHY (the rule, and where the rule does NOT apply),
   then exactly two bullets: CARRY, the one thing still left to the person, with
   a grep string proving the fix travelled to their machine; and GATE, last.
   If no fix could be made from here the section does not exist at all: a section
   titled "what I changed" that changed nothing is the [LIES] kind, committed by us.

2. **Ask about commit and push, every time.** "you should also ask whether I need
   to commit it and push it or not." New `## 🙋 Your Call`, required and never
   optional: print the exact commands, never run them. A lesson file is worth
   nothing uncommitted, and the person owns this repo's history.

3. **Show the report, not only its path.** "I think you should add one block what
   what report you generared for this for the Issue-from-Server." New
   `## 📄 The Report I Wrote`: the issue file's id, slug, path and one line per
   heading it filled, then the other landing places, then the gate row.

Shape: five sections plus a trailing fenced block.

```
line 1                             the verdict: KIND, step, whose fault
## 🔍 What Failed                   phase 1
## 🧠 Why                           phase 2
## 🛠️ What I Changed, Where, And Why phase 3 + 4 merged, past tense
## 📄 The Report I Wrote             phase 5
## 🙋 Your Call                      commit/push · anything still blocked
<trailing fenced block>             the return block, no heading
```

- Phases 3 and 4 merged into one section. A fix and its line report are one
  thought: "I changed this" is unreadable without "at these lines", and `4 LINES`
  alone is a table with no subject. It also keeps the reply inside the five-section
  budget `/claude-response-format` 0.2.0 sets.
- The return block became the reply's SIGNATURE rather than a section: no
  heading, always last.
- A skipped phase leaves NO section. On `need-more-log` there is no 🛠️ and no 📄.
  An empty heading reads as work that happened.


## [0.4.0] - 2026-08-29

RENAMED `haipipe-server-error` -> `remote-error`, and the session itself
became part of the contract. JL: "I want to rename the skill to be the
remote-error ... for a remote-error debugging, we should also have a session name
for it, one session is over, and then we move to the next step." Then: "no
haipipe."

**The rename, two halves.**

`server` -> `remote`. 0.3.0 already made the body engine-neutral and pushed every
CMS-and-Stata command into `ref/profile-cms-stata.md`, but the NAME still said
`server`. A server is a place; half the failures this skill handles do not come
from one. The JHU VDI, the Mac Studio over SSH, a CI runner, and RateMDs
returning 403 are all the same shape: the run happened where this session cannot
reach, and only pasted TEXT came back. `remote` names that boundary, which is the
actual spine, and it matches the wall diagram at `SKILL.md:26-31` that was
already written in those words.

`haipipe-` dropped. The prefix marks a skill that operates the HAI-Pipe
lifecycle and speaks its vocabulary: stage letters, task-folders, Pages, units.
This one does none of that. It takes pasted text and a repo and returns a rule,
which is why it reads a PROFILE instead of a pipeline. The three neighbours in
`0_utils` that are also method-only carry no prefix either:

```
0_utils/
  claude-response-format     no prefix   method
  diagram-ascii              no prefix   method
  notebook-cell-python       no prefix   method
  remote-error               no prefix   method       <- joins them
  field-test          prefix      operates a HAI-Pipe planned run
  haipipe-skillset-status    prefix      reports on the HAI-Pipe skillset
```

**The session.** New `Session` section between Inputs and Profiles. One session
= one remote step: `C-LBP` while the LBP data pipeline is under debug, a new one
when the step or the topic changes, and the same one for a second error at the
same step. Three name shapes, `<STAGE>-<COHORT>` first.

- New optional `--session` input. Read from the transcript when the session is
  already named; otherwise PROPOSE a name and let the person type `/rename`.
  The skill never renames a session itself: a rename mid-round breaks the tie to
  the files already written under the old name.
- `ref/issue-file-template.md` gains a `**Session:**` metadata line, and rule 0:
  the files say WHAT changed, the chat says why the other candidates were
  rejected, and the session name is the only trace between them.
- The return block gains `session:` and `next_session:`. Phase 5 ends by
  printing the name the NEXT step should carry.

Prompted by the real trail: session `C-LBP` (id `d56ecbdb`, 2026-08-29) ran the
LBP launch prep and then drifted into building this skill, so it had to be
renamed `SKILL-REMOTE-ERROR` mid-flight. Two topics, one session, one name; the
convention above is what stops that.


## [0.3.0] - 2026-08-29

MOVED from `skills/task/8_stata/` to `skills/0_utils/`, and the engine-specific
half split out into a profile. JL: "I think this should not be in the task, it
should be in 0_utils."

He is right, and there is a stronger reason than placement. The spine of this
skill is not Stata: a run failed on a machine this session cannot reach, and the
failure has to become a rule. That loop already covers the JHU VDI, the Mac
Studio over SSH, a CI runner, and a live site returning 403. The repo's own
RateMDs lesson is exactly this shape and has no Stata in it. Only the commands
are engine-bound.

The decisive precedent is the neighbour: `0_utils/field-test` runs the
SAME failure-to-rule loop against a PLANNED run (expectation ledger, friction
log, gaps become law patches and checker teeth). This skill runs it against a
REAL failure. They belong side by side, and `0_utils` is where a method skill
that crosses every stage and every engine lives.

- `SKILL.md` is now engine-neutral: the four failure KINDS, the honesty rules,
  the generated-file law, the ID grammar, the status emoji, the return block.
- `ref/profile-cms-stata.md` is NEW and carries everything that was CMS-only:
  the r-code table, the three log artifacts, the PowerShell 5.1 limits,
  `sync_shared.py`, `check_server_ready.py` and its 19 rules, the ENV/ALL/unit
  prefixes, the register's four files, and the PHI rule that overrides all of it.
- New `--profile` input, inferred from the error's own shape.
- A profile that does not exist is not a refusal: run the generic laws, say no
  profile covered it, and offer to write one. A SECOND failure from the same
  machine justifies a profile; the first does not.

`haipipe-task-for-stata` 0.2.9 already points here by NAME, which survives the
move; its wording changed from "sibling skill" to name the new home.


## [0.2.0] - 2026-08-29

The report destination is now the PERSON's, not the skill's. JL: "the place to
save the report should [be] provided by the user."

New `Inputs` section, and `${REGISTER}` replaces the hardcoded
`_WorkSpace/0-CMS-Store/Issue-From-CMS-Server/` everywhere in phase 5. Resolution
order: `--register <dir>` on the call, then `$HAIPIPE_ISSUE_REGISTER`, then the
repo default. The resolved path is echoed before the first write, and a register
with no `SERVER-READY-CHECK.md` is created rather than refused, so the skill
carries to a project that is not this study.

Two files deliberately stay OUTSIDE the register, because they belong to the code
and not to the report: `<task-folder>/ISSUES.md`, which a reader of the folder
must see next to the code, and `tasks/_tools/check_server_ready.py` with its
`tasks/LESSON.MD` entry, which is the gate itself.

The return block gained a `register:` line naming the resolved path AND how it
was resolved, so a silent fallback to the default is visible.


## [0.1.0] - 2026-08-29

New skill. It owns the RETURN leg of CMS secure-server work: a person pastes an
error a run produced on a machine this session cannot reach, and the skill gives
the reason, edits the canonical file, names every line it touched, and lands the
lesson in the issue register.

JL asked for a skill called "work with server". That name was not taken, because
it names a PLACE and half that place already has a skill: `haipipe-task-for-stata`
runs the OUTBOUND leg (scaffold the folder, Gate 1, write `SERVER_CHECK.md`,
SKILL.md:211-248). The missing half is the return leg, and it is a different job
with a different trigger, so it became its own skill named for its input.

Home is `skills/task/8_stata/`, beside `haipipe-task-for-stata`, because the two
share `ref/cms-server-checklist.md` and `ref/stata-dialect.md`. Not
`haipipe-utils`, whose family is clinical-text normalization (describe-food,
describe-medication, haipipe-norm). Not `0_utils`, whose skills are engine-neutral
helpers.

The five phases are JL's own words from the 260829 session, in his order:
READ, REASON, FIX, LINES, LESSON. Phase ④ exists because he asked for it by
name: "let me know which lines you changed."

Three rules were written in because they had already been paid for elsewhere in
the repo:

- **Never edit a GENERATED FILE copy.** Edit the canonical under
  `tasks/00_cms-stata-template/`, then `sync_shared.py`. The copy's own head says
  so, and checker rule R19 fails until it is done.
- **A laptop fix is 🟠 FIXED, never ✅ CLOSED.** There is no Stata and no CMS data
  here, so nothing written from this machine has been verified. Writing ✅ from
  the laptop is exactly the `[LIES]` failure kind, committed by us.
- **Gate 1 green is necessary, not sufficient.** Register entry ALL-09 records a
  synthetic unit with eleven real violations passing 17 of 19 rules.

`ref/issue-file-template.md` freezes the six-heading shape that
`260828/issue-001-forvalues-brace-r198.md` already used, including its two
unenforceable rules: the Symptom block is verbatim, and Status stays 🟠 until a
server run moves it.

Not yet validated through a fresh subagent on a real error. Owed.
