## 0.1.0 · 2026-10-16 · the judge, split out of haipipe-writing and haipipe-draft-check (JL 261016)

- New skill. It takes everything that EVALUATES prose from `haipipe-writing` (0.22.4): `ref/plain-rules.md`,
  `ref/ai-tells.md`, the anti-slop adapter, rules and attribution, `cli/anti_slop.py`, `cli/score.py`, `cli/agree.py`,
  `cli/holes.py`, the rubric, the evaluation cycle, the method contract and catalog, `ref/methods/`, `ref/external/`,
  `tests/test_anti_slop.py`, and the vendored `1_style/writing-dna-skill`, `2_evaluate/academic-humanizer`,
  `2_evaluate/humanizer`.
- Mode 2 is the Page check gate, moved whole from `haipipe-draft-check` (0.13.1) to `ref/page-check.md`.
- It never edits text, and whoever wrote a text never reviews it (stated in SKILL.md).
- It also reviews text that is not a Page (an email, one paragraph).
- Rubric id is now `haipipe-draft-review/base-v1` (was `haipipe-writing/base-v1`); `cli/anti_slop.py` reports
  `tool: haipipe-draft-review/anti_slop.py`; catalog paths to the vendored skills are `../1_style`, `../2_evaluate`.
- Drafting moved to `haipipe-draft/ref/writing/` (and `haipipe-draft/cli/wdiff.py`).
- Older history: `ref/history/haipipe-writing-CHANGELOG.md`, `ref/history/haipipe-draft-check-CHANGELOG.md`.
