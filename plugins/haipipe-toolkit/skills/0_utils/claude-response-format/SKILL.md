---
name: claude-response-format
description: "Canonical spec for the assistant's chat reply format in this workspace: every substantive reply is organized into `## [emoji] Short Headline` sections (one emoji + a short readable headline, content beneath); turns that change files end with a git-derived file-change report and a CONDITIONAL 'which files to review' list. The repo CLAUDE.md points here to make it always-on. Trigger: response format, reply format, section headers, emoji headers, file-change report, 回复格式."
argument-hint: "(reference spec — usually not invoked directly)"
allowed-tools: Bash, Read
metadata:
  version: "1.2.0"
  last_updated: "2026-06-26"
  summary: "Emoji headline format for chat replies + end-of-run file-change & conditional review report."
  changelog:
    - "1.0.0 (2026-06-02): initial spec; referenced by repo CLAUDE.md Rule 5."
    - "1.0.1 (2026-06-02): renamed skill dir response-format -> claude-response-format."
    - "1.1.0 (2026-06-09): merged claude-chat-format; added end-of-run file-change report (📁) and conditional review-list (👀) sections; enabled Bash for git status."
    - "1.2.0 (2026-06-26): changed section headers from kebab-case slugs to natural readable headlines in title case."
---

Skill: claude-response-format (0_utils)
=======================================

Canonical format for conversational replies in this workspace. CLAUDE.md Rule 5
points here; this file is the detailed spec + examples. The CLAUDE.md line is
what makes it always-on — this skill is the reference it cites.

Scope
-----

- Applies to CHAT replies — what the assistant writes back to the user.
- Does NOT apply to file / doc contents. Those keep CLAUDE.md Rule 4 (ASCII
  headers `===` / `---`, no `##`). Never let this format leak into `.md`/`.tex`
  files the assistant authors.

The format
----------

Every substantive reply is split into one or more sections. Each section is:

```
## [emoji] Short Headline
<content for that section>
```

- `[emoji]` — ONE emoji that fits the section's role. Suggestive palette (not
  fixed): 🧩 short answer · 🎯 recommendation · ⚠️ caveat/risk · 🛠️ how-to ·
  📋 summary/list · 🔍 findings · ✅ done · 🙋 question for you · 📁 file changes ·
  👀 files to review · 🧪 experiment · 💡 idea · 📊 results · 🚧 in progress.
  Pick what fits.
- `Short Headline` — a short, readable, natural-language headline, ~2-5 words,
  title case (e.g. `My Recommendation`, `What Actually Works`, `Next Step`).
  NOT kebab-case — write it like a headline a human would scan.
- Content sits beneath the header: prose, bullets, tables, code — all fine.

Guidance
--------

- Structure any non-trivial reply into sections; order them most-important-first.
- A trivial one-line reply can be a single section, or skip the header entirely
  if it would only add noise — judgment call, don't be robotic about it.
- Don't over-fragment: ~2-5 sections for a typical reply; each earns its header.
- Keep headlines honest to the content; don't pad to hit a count.
- One emoji per header, at the start, right after `## `.

End-of-run file report (📁)
---------------------------

End ANY turn that changed files with a `## 📁 file-changes` section. Derive the
list from git — never from memory:

    git status --short
    git -C <submodule> status --short      # if a submodule (e.g. Tools/) was touched

Group the entries: code / scripts; generated artifacts (`.ipynb`, results, build
outputs); data side-effects (`_WorkSpace/…`, `local/…`). Flag anything NOT
git-ignored that must not be committed (e.g. data stores).

Which files to review (👀) — conditional
-----------------------------------------

Add a `## 👀 which-files-to-review` section ONLY when files were really changed
AND some warrant a human read. Skip it entirely for trivial / mechanical / no-op
turns — it is not mandatory.

When shown, name the human-judgment files (hand-written logic, prose / docs, the
largest diff, the highest transcription risk), ranked by what most needs a human
eye. Mark derived / generated / copied files "derived — skip" so the user knows
not to bother (e.g. an `.ipynb` converted from a `.py`).

Examples
--------

```
## 🧩 Short Answer
Yes — and one cheap test settles it.

## ⚠️ The Catch
A skill alone can't make a behavior always-on; it only runs when invoked.

## 🎯 My Recommendation
Run the back-test first, because it resolves the direction before any build.

## 📁 File Changes
code:    code-dev/1-PIPELINE/3-Case-WorkSpace/builder_x.py
derived: code/haifn/fn_case/x.py  (rebuilt from builder — skip)

## 👀 Files to Review
builder_x.py — the hand-written CaseFn logic; the generated x.py is derived — skip.

## 🙋 What I Need From You
Pick the model: Bedrock (BAA-covered) vs a local in-VPC model.
```
