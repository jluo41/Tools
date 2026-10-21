## 0.2.0 · 2026-10-21 · scores out of 10; the Revise review overlay (Coherence, Anti-AI writing)

- JL 261021: "你这个 rubric 怎么没有分数？而且里面没有提到句子连贯性、反 AI 写法之类的吗？... 你有没有拿那个来测试"; then
  "我觉得还是用十分制吧". `ref/evaluation-rubric.md`: each row may carry a score out of 10 beside its verdict, with five
  bands; the verdict still decides, NOT VERIFIABLE scores at most 4, and the mean is a reading aid, never a pass mark.
  A Revise review adds two rows: Coherence (each sentence-to-sentence join) and Anti-AI writing (`cli/anti_slop.py
  audit` plus `ref/ai-tells.md`, the proposed text audited too).

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
