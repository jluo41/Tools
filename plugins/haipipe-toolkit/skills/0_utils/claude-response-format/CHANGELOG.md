claude-response-format — Changelog
==================================


## [0.2.0] - 2026-08-29

OUTLINE REPLACES DIAGRAM. JL: "for this one, I want you to update it so it will
just reply all the things in the bullet point format."

The 0.1.x spec set the SECTION shape (`## [emoji] Short Headline`) and then said
of the content: "prose, bullets, tables, code — all fine." That permission is
what the reply format kept drifting through. `~/.claude/CLAUDE.md` had been
patching around it from the other side with a diagram-first rule and a prose
budget ("a paragraph longer than 2 lines = a diagram you have not drawn yet"),
which produced replies built out of ASCII boxes that were, most of the time,
lists drawn with box-drawing characters.

- Content is now an OUTLINE: nested bullets, and zero prose paragraphs. A
  paragraph is a bullet that has not been split yet.
- Countable rules, so it can be checked rather than felt: one bullet = one fact ·
  <= 2 lines per bullet · <= 3 levels · <= 6 top-level bullets per section ·
  a bold lead-in label on every top-level bullet · numbers live in the bullet.
- "Line 1 is the answer" was promoted from CLAUDE.md into this spec, so the
  answer-first rule and the outline rule live in the same file.
- A fenced block is now EARNED, not default. Four cases keep it: a before/after
  tree, a real compared table, verbatim output (log, error, return block,
  command), and a file:line report. A block that is only a list drawn with box
  characters was never a diagram, and becomes bullets.
- Carried over unchanged from CLAUDE.md so this file is self-sufficient: define
  every term at first use, say the real name, no em-dashes.
- The 📁 file-changes and 👀 files-to-review sections survive, restated as bullets.

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.1.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.2.0; older entries below keep their original numbers).

## [1.2.0] — 2026-06-26

- changed section headers from kebab-case slugs to natural readable headlines in title case.

## [1.1.0] — 2026-06-09

- merged claude-chat-format; added end-of-run file-change report (📁) and conditional review-list (👀) sections; enabled Bash for git status.

## [1.0.1] — 2026-06-02

- renamed skill dir response-format -> claude-response-format.

## [1.0.0] — 2026-06-02

- initial spec; referenced by repo CLAUDE.md Rule 5.
