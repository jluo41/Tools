response-format — Changelog
===========================


## [0.4.0] - 2026-09-09

SCAN -> EXPLAIN inside each section. JL: "No this is too scatter, what I want is
`## 🛡️ Two Escapes I Built In` / `- Compact Form xxxxxxxx` /
`- Inventory Sections Exempt` / `Paragraphs to explain`."

The first draft of this version put the takeaways and the explanation INSIDE
every bullet, as nested children under a bold title. That is what scattered the
reply: one point was broken across three indent levels, and the scan layer was
buried under the detail meant to support it. The revised rule pulls the two
apart into two layers of the SECTION, not of the bullet:

- Each ordinary section begins with 1 to 6 flat `**Title**: takeaway` bullets.
- Optional explanation paragraphs follow the complete bullet list, in the same
  order, and repeat the bold title so each paragraph maps to its bullet.
- A short point with no needed context stays a single bullet and gets no
  paragraph. No nested takeaway bullets are needed.
- 📁 File Changes and 👀 Files To Review remain flat inventory lists, with no
  explanation layer.
- The worked example demonstrates the point-first, paragraph-second shape.
- NUMBERED, not dashed. JL: "mabe change - to be 1. 2. 3? amd make the as short
  and concise and readable as possible." The scan layer is `1.` `2.` `3.`; a
  dash list now means an INVENTORY of paths or names, so the two are visually
  distinct on sight.
- PLAIN PROSE below the list. JL: "a few bullet points of 1, 2, 3, and then we
  just have the paragraphas as before for details." Two intermediate drafts tried
  to key each paragraph to its point, first by repeating the bold title and then
  by opening `**1.**`. Both put the same words on the page twice and made a
  section read like a form. Paragraphs are now ordinary paragraphs: no keys and
  no repeated titles.
- ONE HARD CAP, on the scan point only: <= 14 words including the title, on one
  line. JL: "the paragraphs can be detailed." The prose layer is deliberately
  UNCAPPED, because the point cap is what pushes mechanism, argument and caveat
  out of the list and into the prose, and a second cap there would only push
  them back. Titles drop to 1 to 3 words, since the number now does the pointing.
  The only thing to avoid is padding a section that had nothing more to say.
- REVERSES the `0 prose paragraphs` rule that 0.2.0 set. Prose is legal again,
  but in one position only: under a completed scan list, never as the reply
  itself and never above the bullets. 0.2.0 banned prose because it drifted into
  unstructured replies; the ban then pushed every explanation into nested
  bullets, which is the scatter this version removes. The rules block states the
  new limit as `prose is allowed HERE ONLY`.


## [0.3.0] - 2026-09-09

RENAMED `claude-response-format` -> `response-format`, reversing the 1.0.1 rename
of 2026-06-02. JL: "update this Tools/plugins/haipipe-toolkit/skills/0_utils/
claude-response-format to be response-format." The `claude-` prefix said nothing
the folder did not already say: every skill here is a Claude skill, and the
prefix only made the invocation longer. It now sits with the other unprefixed
methods in `0_utils` (`diagram-ascii`, `field-test`, `notebook-cell-python`,
`remote-error`), which carry no vendor prefix either.

- `name:` in SKILL.md frontmatter and the `Skill:` header line follow the folder.
- Repo `CLAUDE.md` Rule 5 now cites `.../0_utils/response-format/`.
- The live cross-reference in `remote-error/SKILL.md` points at `/response-format`.
- Body text corrected: the pointer lives in the repo `CLAUDE.md`, not
  `~/.claude/CLAUDE.md`. The spec itself is unchanged, this is a rename only.


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
