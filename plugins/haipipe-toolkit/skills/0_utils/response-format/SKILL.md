---
name: response-format
description: >-
  Canonical spec for the assistant's chat reply format in this workspace: the
  answer on line 1, then sections whose numbered one-line scan points state the
  takeaways, with plain prose paragraphs underneath carrying the detail. Turns that change
  files end with a git-derived file-change section, as a flat dash list. The repo
  CLAUDE.md points here to make it always-on. Trigger: response format, reply
  format, outline format, bullet points, section headers, emoji headers, 回复格式.
argument-hint: "(reference spec — usually not invoked directly)"
allowed-tools: Bash, Read
metadata:
  version: "0.4.0"
  last_updated: "2026-09-09"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: response-format (0_utils)
================================

Canonical format for conversational replies in this workspace. The repo `CLAUDE.md`
points here; this file is the detailed spec. The CLAUDE.md line is what makes it
always-on, this skill is the reference it cites.

Scope
-----

- Applies to CHAT replies, meaning what the assistant writes back to the user.
- Does NOT apply to file or document contents. Those keep the repo's own rules
  (ASCII headers `===` / `---`, no `##`). Never let this format leak into a
  `.md` or `.tex` file the assistant authors.


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
stops after the numbers already has the point.

```
scan point   N. **Short title**: one takeaway. ONE line, <= 14 words
prose        plain paragraphs after the whole list. no keys, no titles.
             as detailed as the point deserves. skip it when it adds nothing
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

Dashes now mean something: a dash list is an inventory of paths or names, a
numbered list is an argument. That is why 📁 File Changes and 👀 Files To Review
keep their dashes and take no prose. Never nest anything under a point, either.
Multiple takeaways are multiple numbers.

Rules, all countable
--------------------

```
scan -> explain                  that ORDER, in every section
1. 2. 3. not -                   numbered scan layer; dashes mean inventory
1 line per scan point            it wraps, it is too long. cut it
<= 14 words per scan point       title included. count them
1 to 5 scan points               a 6th means the section is really two
title = 1 to 3 words             it NAMES the point, it does not state it
plain prose after the list       no keys, no titles repeated from above
prose runs as long as it needs   this layer is where detail belongs
0 nested children                multiple takeaways are multiple numbers
prose is allowed HERE ONLY       under a scan list. never as the whole reply
inventory lists keep dashes      File Changes and Files To Review are exempt
```

One count does the work: 14 words caps the scan point. The prose below it has no
cap, because the cap is what forces detail out of the list and into the prose,
which is the only place it reads well.

Sections
--------

- **Header shape** — `## [emoji] Short Headline`, one emoji, then a 2 to 5 word
  headline in title case. Not kebab-case; write it like a headline a human scans.
- **Emoji palette**, suggestive and not fixed — 🧩 short answer · 🎯 recommendation ·
  ⚠️ caveat or risk · 🛠️ how-to · 📋 summary · 🔍 findings · ✅ done ·
  🙋 question for you · 📁 file changes · 👀 files to review · 🧪 experiment ·
  💡 idea · 📊 results · 🚧 in progress.
- **How many** — 2 to 5 for a typical reply, ordered most important first. One
  section is fine for a small reply. A trivial reply can be the answer line alone.
- **Honest headlines** — the headline names what is under it. Never pad to hit a count.

When a code block is still allowed
----------------------------------

Flat bullets are the default scan layer and prose paragraphs are the default
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

File changes (📁)
-----------------

End ANY turn that changed files with a `## 📁 File Changes` section, as a flat
DASH list, derived from git and never from memory:

```
git status --short
git -C <submodule> status --short      # if a submodule such as Tools/ was touched
```

- **Group them** — code and scripts · generated artifacts (`.ipynb`, results,
  build output) · data side effects (`_WorkSpace/…`, `local/…`).
- **Flag the dangerous** — anything NOT git-ignored that must not be committed,
  such as a data store.
- **Keep it dashed and flat**: an inventory is not an argument, so it takes no
  numbers and no explanation paragraphs. The paths and statuses are the content.

Files to review (👀), conditional
---------------------------------

- **Only when** files really changed AND some warrant a human read. Skip it for
  trivial, mechanical or no-op turns. It is not mandatory.
- **Rank by** what most needs a human eye: hand-written logic, prose and docs,
  the largest diff, the highest transcription risk.
- **Mark the rest** `derived — skip`, so the user knows not to bother.

Example
-------

```
Yes, and one cheap test settles it.

## 🧩 Short Answer
1. **Claim holds**: the back-test resolves direction before any build
2. **The catch**: a skill alone cannot make a behavior always-on

A skill runs only when it is invoked, so an always-on rule has to live in
`CLAUDE.md` as well. That is a mechanism limit, not a judgement call.

## 🎯 My Recommendation
1. **Back-test first**: 20 minutes decides the next week
2. **Both outcomes act**: no wasted branch either way

Flat kills the build before anything is spent, and positive hands it a target it
already chose. Nothing here is exploratory.

## 📁 File Changes
- **code**: `code-dev/1-PIPELINE/3-Case-WorkSpace/builder_x.py`
- **derived**: `code/haifn/fn_case/x.py`, rebuilt from the builder, skip

## 🙋 What I Need From You
1. **Pick the model**: Bedrock (BAA-covered), or a local in-VPC model
```

## 📎 "Show me" means in the reply (JL 260904)

"Show me", "preview", "so we can understand it": paste the content INTO the
reply, as bullets or a real table. Never answer with an Artifact link, an HTML
page, a viewer, or a file to open. JL reads the chat; a link is a detour and
the build is his tokens. An Artifact only when JL says "artifact" or "page".
