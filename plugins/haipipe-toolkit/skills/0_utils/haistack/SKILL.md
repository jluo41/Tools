---
name: haistack
description: "/haistack: turns JL's feedback into a constitution article that stays solved: his words kept verbatim in the owning skill's CONSTITUTION.md, the rule, a check, the instance fixed and verified on the real thing. Use when JL gives feedback or a correction on any skill, Studio topic, page or drawing. Trigger: feedback, this is wrong, not valid, make it a rule, constitution, sweep, never again, /haistack."
---

# /haistack · feedback that stays solved, in every case

Read [CONSTITUTION.md](CONSTITUTION.md) first; it wins over this file.

A piece of JL's feedback is solved only when these exist (JL 261118: "when I say /haistack the
feedback will be setup so that it will be solided solved"; "markdown my comments and feedback as the
constitutions"):

1. **His words**: kept verbatim, dated, in the owning skill's `CONSTITUTION.md`
2. **The rule**: one sentence an agent can follow, under his words
3. **The cases**: every place the same kind of problem can happen, each fixed or marked open
4. **The check**: a command anyone reruns over all the cases (`**Run:**`), or a named screen to look at
5. **The proof**: every case fixed, and the check run on the real thing
6. **The report**: need, what exists now, the gap, the methods, the update, why never again

```text
JL's words ─▶ owner ─▶ name the class ─▶ list all cases ─▶ fix all ─▶ Run: over all ─▶ solved
                                                                      ▲ rerun by --check forever
```

The instance JL saw is one case. Fixing only it is how the same problem comes back next week on another
theme, level or SPACE.

## The constitution

Each skill that has received feedback keeps `CONSTITUTION.md` beside its `SKILL.md`. It **wins over the
SKILL.md body**: where they disagree, follow the constitution, then bring the body in line. The SKILL.md
carries one line near its top: `Read CONSTITUTION.md first; it wins over this file.`

```markdown
## A03 · <the rule, a few words>

> "<JL's words, verbatim, typos kept>" (JL <YYMMDD>, <where he said it>)

**Rule:** <one sentence>
**Why:** <what went wrong, the real case>
**Class:** <the one thing behind the message, not the single case it showed up in>
**Cases:** ✅ <case> · ✅ <case> · ⬜ <case not yet fixed>
**Check:** <what must hold, in words>
**Run:** `<command run from the Tools-SPACE root; exit 0 means it holds>` (omit only when no machine can see it)
**Status:** solved <YYMMDD> | open
**Solved by:** `<file>`: <change, 8 words or fewer>
**Report:** constitution/A03-<slug>.md
```

1. **Numbered for good**: A01, A02, ... never reused; a replaced article stays, marked `Replaced by A07`.
2. **Verbatim**: his words exactly, Chinese or English, typos kept; the rule is where we paraphrase.
3. **One article, one rule**: two rules in one message are two articles.

## Steps when /haistack runs

1. **Capture**: his words from this message (or the last messages he points at), the date, the screen.
2. **Owner**: the skill whose SKILL.md governs the thing (a Studio drawing: `haipipe-studio`; a page:
   its workbench skill). No owner skill: the Project's own `CONSTITUTION.md` at its root.
3. **Read** the owner's `CONSTITUTION.md` first: an article that already says it means the old one was
   never really solved; reopen it (`Status: open`) instead of writing a duplicate.
4. **Name the class**: what kind of mistake this is, in one line, so it covers more than this instance.
5. **List every case**: walk each axis and write down every place the class can occur; search, never
   recall (`grep`, `find`, `constitution.py`, the served pages):
   - themes: Insight, Labeling, Design, Work, Paper, Cowork, Project
   - levels: SPACE, Project, Block, Job, Task, Run
   - surfaces: page, Studio drawing, skill doc, script, builder, test, generated output
   - SPACEs: every live SPACE that holds one (each SPACE beside Tools, and Tools)
   - writers: every code path or agent that can produce the thing again
6. **Write** the article(s) with Class and Cases; add the SKILL.md line if it is missing.
7. **Fix every case**, not only the one JL saw; the writers too, so a rebuild cannot bring it back.
8. **Make it hold**: a mechanical rule gets a `**Run:**` command that checks ALL cases (a glob, not one
   path): the owner's `check.py`, a test, or a builder assert. Otherwise the check is a question the
   reviewer agent must answer, written in the owner's reviewer ref.
9. **Verify on the real thing**: run the Run line, render, open it with `/wb`, look at the screenshot.
   Wire green is not UI green.
10. **Report**: write `constitution/A<NN>-<slug>.md` beside the constitution: Need, Now, Gap, Methods,
    Update, Never again ([ref/report.md](ref/report.md)), and link it from the article.
11. **Status**: `solved <date>` only after every case passed step 9 and the report exists; else `open`.
12. **Remember**: one feedback memory pointing at the article (`[[<skill>-constitution]]`).

A problem that comes back after `solved` means the Cases list or the Run line was too narrow: reopen the
article, add the missed case to both, never write a second article for it.

## List every article

```bash
python <this skill>/scripts/constitution.py            # every CONSTITUTION.md under Tools-SPACE: id, status, rule
python <this skill>/scripts/constitution.py --open     # only the open ones
python <this skill>/scripts/constitution.py --check    # rerun every Run: line; ❗ a broken rule or a missing report
```

`/haistack sweep` runs `--check` over the whole repo: every ❗ is reopened and worked as above. Run it
after a large change to a shared skill, page or builder.

## Report back

Answer on line 1: solved or open. Then the report's six parts in short (Need, Now, Gap, Methods, Update,
Never again), the cases (✅ ⬜), the Run line's real output, and the link to the report file.
