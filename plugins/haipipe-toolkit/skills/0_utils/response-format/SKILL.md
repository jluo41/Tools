---
name: response-format
description: >-
  Canonical spec for the assistant's chat reply format in this workspace: the
  answer on line 1, then sections whose numbered one-line scan points state the
  takeaways, with plain prose paragraphs underneath carrying the detail. A section
  whose work changed files ends with those files, one short line each saying what
  changed. The last section is always the summary and next steps; there is no
  file section. This is a reference spec and does not self-activate. Trigger: response format, reply
  format, outline format, bullet points, section headers, emoji headers, 回复格式.
argument-hint: "(reference spec — usually not invoked directly)"
allowed-tools: Bash, Read
metadata:
  version: "0.7.0"
  last_updated: "2026-09-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: response-format (0_utils)
================================

Canonical reference for conversational replies in this workspace. Apply it when
the user invokes this skill or another active instruction loads it. A skill file
does not make itself always-on, and this checkout has no root `CLAUDE.md` that
activates it.

When a loaded skill defines a reply shape for a specific request, that scoped
shape takes precedence for that request. In particular, `/task-table`'s
table-only response and `/remote-error`'s required report sections are explicit
exceptions to the general answer-first scan format below. Do not combine both
shapes in one reply.

Scope
-----

- Applies to CHAT replies, meaning what the assistant writes back to the user.
- Does NOT apply to file or document contents. Follow the actual directory
  guidance and document template, including their heading syntax. This chat
  skill neither forbids Markdown `##` nor requires ASCII underline headings
  in authored files.


The format
----------

**Line 1 is the answer.** A bare answer, before any heading, before any bullet.
A closed question gets its yes, its no, or its one name, and nothing else on
that line. Never build up to it.

**Everything after line 1 is sectioned.** Each section is a NUMBERED list of
one-line points, then plain prose underneath for whatever needs explaining. The
list is what the reader scans. The prose is ordinary paragraphs, with no keys
and no repeated titles. Never interleave the two.

```
<the answer, one line>

## [emoji] Short Headline
1. **Short title**: the takeaway, the so-what
2. **Next title**: another takeaway

The paragraph that explains them, in plain prose, after the whole list. It
covers what the points could not hold, and it is often not needed at all.
```


Inside one section: scan, then explain
--------------------------------------

Every section has two layers in THIS order. First a numbered scan layer of
one-line points. Then plain prose for whatever needs more context. A reader who
stops after the numbers already has the point. A section whose work changed files
adds a third layer last: its file lines (see "Files live in their section").

```
scan point   N. **Short title**: one takeaway. ONE line, <= 14 words
prose        plain paragraphs after the whole list. no keys, no titles.
             as detailed as the point deserves. skip it when it adds nothing
file lines   - `name` (where): change in <= 8 words. only if the section changed files
```

1. **Numbers, not dashes**: the scan layer is `1.` `2.` `3.`, never `-`.
2. **One line, hard**: a point that wraps to a second line is too long.
3. **The title names, it does not tell**: `**Push landed**`, not a sentence.
4. **The takeaway is the consequence**: the verdict, the number, the decision.
5. **The prose carries the detail**: plain paragraphs, as long as they need.

Numbering makes the section countable at a glance. The reader sees three points
rather than an unbounded list, and can say "point 2" out loud without quoting it.

The one-line cap is the readability lever that matters most. Two-line points are
exactly how a scan layer decays back into prose. When a point will not fit, its
detail belongs in the paragraph below, or it was really two points.

Below the list, write normally, and write as much as the material deserves. The
scan layer is deliberately starved: 14 words cannot hold a mechanism, an
argument, or a caveat with its conditions attached. Those go in the prose, at
whatever length they need, because a hard cap here would only push the detail
back into the points and undo the split. The one thing to avoid is padding a
section that had nothing more to say, in which case the list simply ends.

Earlier drafts keyed each paragraph to its number and repeated its bold title,
which put the same words on the page twice and made the section look like a
form. Plain paragraphs read better, and the reader can already see which points
they answer.

Dashes now mean something: a dash list is a list of files or names, a numbered
list is an argument. File lines keep their dashes, but a bare path is not
information: every file line says what changed. Never nest anything under a point,
either. Multiple takeaways are multiple numbers.

Rules, all countable
--------------------

```
scan -> explain -> files         that ORDER; files only if the section changed some
1. 2. 3. not -                   numbered scan layer; dashes mean inventory
1 line per scan point            it wraps, it is too long. cut it
<= 14 words per scan point       title included. count them
1 to 5 scan points               a 6th means the section is really two
title = 1 to 3 words             it NAMES the point, it does not state it
plain prose after the list       no keys, no titles repeated from above
prose runs as long as it needs   this layer is where detail belongs
0 nested children                multiple takeaways are multiple numbers
prose is allowed HERE ONLY       under a scan list. never as the whole reply
a file line says what changed    `name` (where): change, <= 8 words, one line
```

One count does the work: 14 words caps the scan point. The prose below it has no
cap, because the cap is what forces detail out of the list and into the prose,
which is the only place it reads well.

Sections
--------

- **Header shape** — `## [emoji] Short Headline`, one emoji, then a 2 to 5 word
  headline in title case. Not kebab-case; write it like a headline a human scans.
- **Emoji palette**, suggestive and not fixed — 🧩 short answer · 🎯 recommendation ·
  ⚠️ caveat or risk · 🛠️ how-to · 📋 summary and next (the last section) ·
  🔍 findings · ✅ done · 🙋 question for you ·
  👀 (a mark on a file line: read this one) · 🧪 experiment ·
  💡 idea · 📊 results · 🚧 in progress.
- **How many** — 2 to 5 for a typical reply, ordered most important first. One
  section is fine for a small reply. A trivial reply can be the answer line alone.
- **The last section is the summary and next steps** (JL 260927) — every
  substantive reply ends with `## 📋 Summary and Next`: its scan points say where
  things stand now and what comes next, most important first; its prose holds the
  detail. It is the section a reader who skipped everything else reads, so it
  carries the real state and the real next step, never a list of files. A question
  for the user belongs here too, as the next step it blocks.
- **Honest headlines** — the headline names what is under it. Never pad to hit a count.

When a code block is still allowed
----------------------------------

Numbered scan points are the default scan layer and prose paragraphs are the default
explanation layer. A fenced block earns its place only when the content is
genuinely two-dimensional or must be shown verbatim:

```
a folder TREE, before and after, side by side
a table whose columns are compared across rows
verbatim output: a log, an error, a return block, a command
a file:line report
```

Everything else that used to be an ASCII diagram becomes numbered scan points
followed by explanation paragraphs. If a block is only a list drawn with box characters,
it was never a diagram.

Carried over, unchanged
-----------------------

- **Define every term at first use**, inline, even when it looks obvious.
  Write `AAMC = Association of American Medical Colleges`, not `AAMC`.
- **Say the real name** — real file paths, real field names, real function names.
  No nicknames, no invented vocabulary, and never pass a subagent's coined word
  through without translating it first.
- **No em-dashes.** Use a colon, a semicolon, a comma, parentheses, or a new sentence.

Files live in their section (JL 260926)
---------------------------------------

A list of bare paths at the end of a reply answers "which files" and nothing else.
So a changed file is written down next to the work that changed it, as short as it
can be while still saying what changed.

1. **In the section**: a section whose work changed files ends with those files.
2. **Name, where, change**: ``- `name` (where): change``, the change in 8 words or fewer.
3. **👀 means read it**: add `Check:` and what to confirm, 8 words or fewer.
4. **Outputs too**: a notebook or result goes under the section that made it.
5. **No file section**: a leftover is one sentence in the closing section, never a section.

A file line is ONE line; if it wraps, cut it. `name` is the file name, or the
shortest path that is unique in the reply; never an absolute path. When the reader
needs the folder, say it once in the section's prose, not on every line. "Where" is
a line range, a function, or `new`. The change is a verb and an object (`added
hourly reader`), never what the file is for. Files that share one change share one
line.

```
- 👀 `serialize_windows.py` (~141-180): added hourly format and reader. Check: NA rule
- `r05_hourly_start_delta.yaml`, `.sh` (new): b02's fifth Run
- `r09_pt_hourly_start_delta.ipynb` (generated, git-ignored): format on real windows
```

Mark 👀 only on what really deserves a human read: hand-written logic, prose and
docs, the largest diff, the highest transcription risk. Derived and generated files
get no mark.

Before writing the reply, run the git check; it is never written from memory:

```
git status --short
git -C <submodule> status --short      # if a submodule such as Tools/ was touched
```

Every path git shows for this turn must sit in some section's file lines. What no
section claims (a side effect such as `_WorkSpace/...` written or deleted, or
another session's file that could end up in a commit by mistake) is one sentence in
the prose of the closing `## 📋 Summary and Next`. There is no `📁 File Changes`
section (JL 260927): a reply ends on where things stand and what comes next.

Example
-------

```
Yes, and one cheap test settles it.

## 🧩 Short Answer
1. **Claim holds**: the back-test resolves direction before any build
2. **The catch**: a skill alone cannot make a behavior always-on

A skill runs only when it is invoked or explicitly loaded by another active
instruction. To make this format always-on, an active global instruction must
load it; this checkout currently has no root `CLAUDE.md` pointer.

## 🛠️ What I Changed
1. **Builder fixed**: the trigger now skips days with no readings
2. **Rebuilt**: the generated function matches the builder again

The builder counted empty days as windows, so every empty day produced a case with
no readings. It now skips them, and the rebuild picked that up.

- 👀 `builder_x.py` (`build_cases`): skip days with zero readings. Check: skip before window cut
- `fn_case/x.py`: regenerated from the builder

## 📋 Summary and Next
1. **Now**: empty days no longer make cases; the CaseSet is rebuilt
2. **Next**: pick the model, Bedrock (BAA-covered) or a local in-VPC model

The rebuild wrote `_WorkSpace/3-CaseStore/x/@v0002/`, which git ignores. Once the
model is picked, the training Run can start from this CaseSet.
```

## 📎 "Show me" means in the reply (JL 260904)

"Show me", "preview", "so we can understand it": paste the content INTO the
reply, as bullets or a real table. Never answer with an Artifact link, an HTML
page, a viewer, or a file to open. JL reads the chat; a link is a detour and
the build is his tokens. An Artifact only when JL says "artifact" or "page".
