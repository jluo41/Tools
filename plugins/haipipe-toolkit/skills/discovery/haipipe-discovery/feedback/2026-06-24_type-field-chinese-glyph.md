---
status: fixed
created: 2026-06-24
context: discovery.yaml schema / the type: field (Axis 2)
fixed_in: "2.1.0"
---

RESOLUTION (2026-06-24): JL chose to rename the type axis to English words
**Search / Review / Idea** (搜 -> Search, 析 -> Review, 创 -> Idea). Names mirror the
Execute bucket (Search=1_search+2_read, Review=3_review, Idea=4_idea). The two branch
glosses were also de-CJK'd (判 -> judge, 综 -> synthesize). Migrated SKILL.md +
ref/lifecycle-map.md + ref/discovery-yaml-schema.md and all existing discovery folders;
the "different alphabets" orthogonality rationale was rewritten (both axes English now:
process verbs vs folder kinds, non-overlapping word lists). Chinese TRIGGER phrases
(查新/找idea/全流程/专利) were intentionally kept. Pending: fresh-subagent validation.


Reporter (JL): `type: 搜` <- why is the type here Chinese? please think about
updating this.
(re: discoveries/.../discovery.yaml `type:` field; the value is a CJK glyph 搜/析/创)

## Current design + rationale
`ref/lifecycle-map.md` makes the Chinese deliberate: "The type axis is named in
Chinese single characters and the stage axis in English on purpose: different
alphabets mean the two axes can never be mistaken for each other." So 搜/析/创
(type, Axis 2) vs Plan/Build/Execute/Report (stage, Axis 1) are kept in different
scripts so a reader never confuses the two axes.

## Analysis (asked to think about it)
- KEY FACT: nothing PARSES `type:`. The skill has no .sh/.py — it is all Markdown +
  YAML read by Claude, and Claude handles CJK fine. So the usual "non-ASCII enum
  breaks tooling" argument is weak HERE (no grep/sort/switch in code branches on it).
- Remaining real downsides of a CJK value in a machine-style field:
  - Sits next to all-ASCII siblings `role:` / `status:` -> intra-file script mismatch
    reads as inconsistent.
  - Friction for any non-CJK collaborator / future script / CSV export / IME-less
    grep; risk of mojibake in non-CJK terminals.
  - `role:` already carries the English semantic (source_gather / landscape_review /
    idea_generation), so the type's "name the kind" job is partly redundant.
- The orthogonality benefit the glyph provides is real and worth keeping for HUMANS.

## Fix (decide in a revision pass)
Recommended: SPLIT display from storage.
- Make the stored machine value ASCII: `type: source | analyze | create`
  (orthogonality vs stages preserved: type = source/analyze/create nouns-ish vs
  stage = plan/build/execute/report verbs).
- Keep 搜/析/创 as a HUMAN display glyph in headings, `_index.md` roll-up tables, and
  the dashboard, where it is never parsed. Optionally store both:
  `type: source` + `glyph: 搜`.
- Do NOT use single Latin letters `S/A/C` — they collide with the group-letter hints
  (S = source-base group, C = counterevidence group).
Scope if accepted: edit `ref/lifecycle-map.md` + `ref/discovery-yaml-schema.md` +
`SKILL.md`, migrate the ~10 existing files carrying `type: 搜/析/创` (discovery.yaml +
status.yaml) and their `_index.md` display, then fresh-subagent validate per the
repo CLAUDE.md skill-dev rule.
Alternative if JL prefers minimal change: keep CJK as-is (low technical risk since
nothing parses it) and just document that the glyph is intentional.
