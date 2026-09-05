---
name: claude-response-format
description: >-
  Canonical spec for the assistant's chat reply format in this workspace: the
  answer on line 1, then everything else as a nested OUTLINE of bullets under
  `## [emoji] Short Headline` sections. Prose paragraphs are not a format here;
  a paragraph is a bullet that has not been split yet. Turns that change files
  end with a git-derived file-change section, also as bullets. The repo
  CLAUDE.md points here to make it always-on. Trigger: response format, reply
  format, outline format, bullet points, section headers, emoji headers, 回复格式.
argument-hint: "(reference spec — usually not invoked directly)"
allowed-tools: Bash, Read
metadata:
  version: "0.2.0"
  last_updated: "2026-08-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: claude-response-format (0_utils)
=======================================

Canonical format for conversational replies in this workspace. `~/.claude/CLAUDE.md`
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

**Everything after line 1 is an OUTLINE.** Sections, then nested bullets. There
are no prose paragraphs in a reply. A paragraph is a bullet that has not been
split yet.

```
<the answer, one line>

## [emoji] Short Headline
- **Lead-in label** — the fact, on one line
  - the detail that qualifies it
  - the second detail
- **Next label** — the next fact
```

Rules, all countable
--------------------

```
one bullet = one fact          if it holds two, it is two bullets
<= 2 lines per bullet          a third line means it needs a child bullet
<= 3 levels of nesting         level 4 means the section is really two sections
<= 6 top-level bullets         per section; more means split the section
bold lead-in label             on every top-level bullet, so the page is scannable
numbers live IN the bullet     never in a sentence after the list
0 prose paragraphs             the whole reply, headings and bullets only
```

The lead-in label is a noun or a short phrase, then an em-dash-free separator
(a colon, or a spaced hyphen), then the fact. It is what makes the reply
readable at a glance without reading any bullet in full.

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

Bullets are the default. A fenced block earns its place only when the content is
genuinely two-dimensional and a list would destroy it:

```
a folder TREE, before and after, side by side
a table whose columns are compared across rows
verbatim output: a log, an error, a return block, a command
a file:line report
```

Everything else that used to be an ASCII diagram becomes nested bullets. If a
block is only a list drawn with box characters, it was never a diagram.

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

End ANY turn that changed files with a `## 📁 File Changes` section, as bullets,
derived from git and never from memory:

```
git status --short
git -C <submodule> status --short      # if a submodule such as Tools/ was touched
```

- **Group them** — code and scripts · generated artifacts (`.ipynb`, results,
  build output) · data side effects (`_WorkSpace/…`, `local/…`).
- **Flag the dangerous** — anything NOT git-ignored that must not be committed,
  such as a data store.

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
- **The claim holds** — the back-test resolves direction before any build
- **The catch** — a skill alone cannot make a behavior always-on; it runs only
  when invoked

## 🎯 My Recommendation
- **Run the back-test first** — it is 20 minutes and it decides the next week
  - if it comes back flat, the build is dead and nothing was spent
  - if it comes back positive, the build has its target already chosen

## 📁 File Changes
- **code** — `code-dev/1-PIPELINE/3-Case-WorkSpace/builder_x.py`
- **derived** — `code/haifn/fn_case/x.py`, rebuilt from the builder, skip

## 🙋 What I Need From You
- **Pick the model** — Bedrock (BAA-covered) or a local in-VPC model
```

## 📎 "Show me" means in the reply (JL 260904)

"Show me", "preview", "so we can understand it": paste the content INTO the
reply, as bullets or a real table. Never answer with an Artifact link, an HTML
page, a viewer, or a file to open. JL reads the chat; a link is a detour and
the build is his tokens. An Artifact only when JL says "artifact" or "page".
