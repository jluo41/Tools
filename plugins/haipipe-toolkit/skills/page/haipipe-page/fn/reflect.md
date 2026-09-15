---
name: haipipe-page-reflect
description: >-
  Read one complete Page session (a Codex or Claude thread, or a kept Studio
  Chat transcript) and write one reflection record: every input the person
  gave, verbatim and in order; how the assistant understood and acted on each
  one; and the changes the person wants in the Page skill family. Records
  land in skills/page/feedback/. Reflect writes records; it never edits a
  skill, a Page, or a transcript.
argument-hint: "<session-name | codex-thread-id | transcript-path> [--out <dir>]"
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Reflect · read one Page session, write down what the person wanted

Use `/haipipe-page reflect <session>` after a real Page session has run. The
person asked for this on 260914 (Codex thread "Haipipe-Page reflect"):

> 我想做一个 self-evolving 的 function ... 在你的 fn 里面加一个 reflect.md，就是它会读整个
> session，然后认真学习领会我的每一句话，然后还有这个对应的 response ... 学习我的 feedback，
> 然后总结我的 feedback，然后看一看这里面有哪些点可以拿来去提升我们的 skill。
>
> 我们最终的目的是为了写下来，就是读这些 session，然后总结。

So reflect has one product: a written record per session, and one reader:
the person, who decides afterwards what to change in `skills/page`.

```text
one Page session (Codex · Claude · Studio Chat)
        ↓  cli/session_dump.py           read-only intake
every user turn ⟷ the assistant's response ⟷ skills, phases, files it touched
        ↓  this function                 read, classify, write
skills/page/feedback/<YYMMDD>-<session-slug>.md
        ↓  the person reads              (outside this function)
skill revision pass → fresh-subagent field test
```

## What reflect is, next to its neighbours

| Function | Reads | Writes | Judges |
|---|---|---|---|
| **reflect** (this) | one whole Page session, both sides of every turn | one record per session under `skills/page/feedback/` | what the person wanted from the Page machinery |
| `haipipe-application/fn/digest.md` | a session's human turns | routed items in per-skill inboxes, after a confirm gate | tool/skill gripes across the Application family |
| `haipipe-page-workflow/ref/post-run-analysis.md` | one closed Page Run journal | one analysis Task Result | preference signals inside that Run |
| Writing Step (`interactive-writing-run.md`) | one feedback message | the next Step in the open Run | nothing beyond the paragraph |

Reflect differs from digest in one thing the person insisted on: it reads the
assistant's side too. A gripe list says what annoyed; a reflection says what
was asked, what the assistant understood, what it did, and whether the person
had to say it again. Reflect never routes or files into inboxes, never edits a
skill, and never rewrites Page prose.

## 1 · Locate and dump the session

Run from the repository root. The dumper is read-only over the provider store.

```bash
DUMP=Tools/plugins/haipipe-toolkit/skills/page/haipipe-page/cli/session_dump.py
python3 $DUMP --list-codex 'Paper-MISQ%'                       # find thread ids by name
python3 $DUMP --codex <thread-id> --name <session> --out <scratch>/<session>.md
python3 $DUMP --codex <thread-id> --name <session> --out <scratch>/<session>.compact.md --compact 1500
python3 $DUMP --claude ~/.claude/projects/<cwd-slug>/<session-id>.jsonl --out <scratch>/x.md
python3 $DUMP --studio <page>/studio/chat/<YYMMDD-HHMM>/transcript.md --out <scratch>/x.md
```

Rules for the intake:

- A Codex thread may span several rollout files; a fork continues the thread
  in a second file named `rollout-<time>-<thread-id>_<fork-id>.jsonl`. Read all
  of them plus `thread_history_1.sqlite`; the dumper merges and de-duplicates.
- Never resolve a session by display name alone when two threads share it;
  `--list-codex` shows every id, and a forked sub-agent thread is not the
  person's session.
- The dump is scratch material. The record cites the thread id and span so the
  dump can be regenerated; it does not copy the dump into `feedback/`.
- The person's inputs are never trimmed. `--compact` trims only the
  assistant's replies and drops tool lines; when a turn needs the full reply,
  open the full dump.

## 2 · Read every turn on both sides

For each user turn `Uxx` build three columns before writing anything:

```text
the person's words        verbatim, original language, nothing paraphrased
the assistant's response  what it said it understood · which skill or phase it
                          loaded · which files it wrote · which Runs it opened
the outcome               accepted · corrected in the next turn · repeated later
```

Then tag the turn with exactly one primary tag:

| Tag | Meaning | Becomes a wanted change? |
|---|---|---|
| `CONFIG` | how the Page machinery should behave: Draft, Evidence or Run Space, Serve and links, RP/RE/RD Runs, phases, delivery (LaTeX, Word, CoWork copy), plugins, naming, reply shape | yes |
| `CORRECTION` | the person re-explained, pushed back, or said it again | yes, and record the misreading |
| `CONTENT` | the paper's prose, argument, evidence, or citations | no; kept in §5 so it is not mistaken for skill feedback |
| `INSTRUCTION` | a one-off task with no preference in it | no |

A compound turn is the norm: one message often carries a task, a preference,
and a complaint. Split it; a turn may yield two tags or none beyond
`INSTRUCTION`. Tag by the SUBJECT of the sentence, not by the skill it names.

## 3 · Write the record

Path: `Tools/plugins/haipipe-toolkit/skills/page/feedback/<YYMMDD>-<session-slug>.md`,
where `YYMMDD` is the session's last active day and the slug is the session
name lower-cased. One session, one file. Take the clock time from `date`.

```markdown
---
session: Paper-MISQ-Intro-v3
provider: codex
thread: 01a09ae3-a83f-7290-b16b-d0de1c3f8427
span: 2026-09-13 09:10 → 2026-09-14 21:39
page: examples/…/Ba-MISQ-Main/S-MISQ-Main-1-Introduction
turns: 119
written: 260915 0041
status: draft · not yet reviewed by JL
---

# Paper-MISQ-Intro-v3 · reflection

## 1 · The session in one paragraph
## 2 · Your inputs, verbatim, in order
### U01 · 2026-09-13 09:10 · [INSTRUCTION]
> the words, unchanged
⟶ what the assistant did (one or two lines) · outcome
## 3 · What you had to correct
## 4 · Changes you want in skills/page
## 5 · Content decisions (paper-level, not skill feedback)
## 6 · Open questions for JL
```

Section rules:

- **§2 is complete.** Every user turn appears, numbered as in the dump, with
  its time, tag, verbatim text, and the assistant's response in one or two
  lines. Chinese stays Chinese; a translation may follow in parentheses but
  never replaces the quote. Annotation turns (text the person selected in a
  reply and commented on) are inputs too.
- **§3 groups the `CORRECTION` turns**: what the assistant read, what the
  person meant, how many turns it took. This is the highest-value section.
- **§4 is a numbered list of wanted changes.** Each item names the quoted turn
  or turns, the owning file or skill by real path (check it exists with `ls`),
  the change in one sentence, and a repetition count. An item without a
  quoted turn is invented and is deleted.
- **§5 keeps paper-level decisions** so a later reader does not mistake them
  for skill feedback and does not lose them either.
- **§6 lists what the reflector could not decide**: a turn whose intent is
  ambiguous, two turns that conflict, or a change whose owner is unclear.

Writing rules: no em-dashes; short sentences; real paths and real field names;
no coined words. Define a term the first time it appears. The record's status
stays `draft` until the person reviews it; reflect never writes a tick.

## 4 · What reflect must not do

- Edit any file under `skills/` other than creating its own record.
- Edit, rebuild, or re-deliver the Page the session worked on.
- Modify, lock, or resume the provider session; the store is read-only.
- Merge two sessions into one record, or route items into an inbox.
- Translate a quote in place, summarize a turn instead of quoting it, or
  drop a turn because it looks like noise. Injected system blocks are the
  only text the dumper removes.

## 5 · After the records exist

Cross-session synthesis (which changes repeat across sessions, which contradict)
is a separate reading step and lands beside the records as
`feedback/README.md`. The actual skill edits go through the normal skill
revision pass and are validated by a fresh subagent on a realistic task
(`Physician-SPACE/CLAUDE.md`, Gotchas). Neither is part of this function.

## 📂 Files

```text
haipipe-page/
├── fn/reflect.md            this contract
├── cli/session_dump.py      read-only intake: Codex · Claude · Studio Chat → Markdown
└── ../feedback/             one record per session, plus README.md as the index
```
