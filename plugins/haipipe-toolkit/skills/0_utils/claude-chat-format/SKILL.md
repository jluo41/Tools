---
name: claude-chat-format
description: "Uniform reply format for Claude Code chat in this project: '#### <emoji>: <heading>' sections, terse result-first prose, an end-of-run file-change report (derived from git status), and a CONDITIONAL 'which files to review' list. Apply on every substantive reply; invoke /claude-chat-format to (re)load the convention. Trigger: chat format, reply format, response format, uniform format, claude-chat-format."
allowed-tools: Bash, Read
metadata:
  version: "1.0.0"
  last_updated: "2026-06-02"
  summary: "Uniform '#### emoji: heading' reply format + end-of-run file-change & conditional review report."
  changelog:
    - "1.0.0 (2026-06-02): initial format skill (emoji headings, file-change report, conditional review list)."
---

Skill: claude-chat-format
=========================

The standing reply format for this project. Apply it to every substantive
reply (not to one-line acknowledgements). Invoke `/claude-chat-format` to
reload the convention. Apply it silently — do NOT announce "using
claude-chat-format"; just produce the format.

---

§ ① Section headers
-------------------

Structure a reply as `#### <emoji>: <heading>` sections, with content beneath
each.

```
#### ✅: Result
<content>

#### 📁: File changes
<content>
```

  - One emoji + a short heading (≤ ~6 words).
  - A reply is a handful of such sections, ordered MOST-IMPORTANT-FIRST.
  - Emoji signals the section's role (suggested vocabulary):
    ```
    ✅ done / result        ⚠️  caveat / risk        ❌ failure
    🔎 investigation         🔧 fix                   📝 note
    📁 file changes          👀 which files to review  🧠 memory / learning
    ⏳ in progress           ⏭️  next steps            ❓ question / decision
    ```

§ ② Prose style
---------------

  - Lead with the result / answer. Bare numbers, no preamble.
  - Terse — no paragraphs of analysis unless asked.
  - Results reports: the FIRST line is a one-line dataset descriptor
    (aidata, version, splits, subset, horizon) BEFORE any metric table.
  - Report outcomes faithfully: failures with their output, skipped steps
    stated plainly, "done" only when verified.

§ ③ End-of-run file-change report  (#### 📁)
--------------------------------------------

At the end of ANY turn that changed files, include a `📁` section. Derive the
list from git — never from memory:

```
git status --short
git -C <submodule> status --short      # if a submodule (e.g. Tools/) was touched
```

  Group the entries:
    - code / scripts
    - generated artifacts (`.ipynb`, results, build outputs)
    - data side-effects (`_WorkSpace/…`, `local/…`)
  Flag anything NOT git-ignored that must NOT be committed (data stores).

§ ④ Which files to review  (#### 👀) — CONDITIONAL
--------------------------------------------------

Include this section ONLY when files were really changed AND some are important
enough to warrant a human read. It is NOT strict — skip it entirely for
trivial / mechanical / no-op turns.

When shown:
  - Name the human-judgment files (hand-written logic, prose / docs, the
    largest diff, the highest transcription risk), ranked by what most needs
    a human eye.
  - Mark derived / generated / copied files "derived — skip" so the user
    knows not to bother (e.g. `.ipynb` converted from a `.py`).

---

See also: project `CLAUDE.md` → "Reply Format"; memories
`feedback_reply_emoji_headings`, `feedback_end_of_run_file_report`.
