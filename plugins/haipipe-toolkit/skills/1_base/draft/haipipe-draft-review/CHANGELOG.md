## 0.3.1 · 2026-10-21 · a text under headings

- A blind reviewer of a structured abstract (JAMA IM Key Points and 7 headings) named four gaps in
  `ref/sentence-logic.md`, now closed: each heading stands alone (its first sentence an opening, joins counted inside
  a heading, Key Points one Flow line, hand-off "none needed" unless the next heading leans on it); a pointer may cross
  a heading when the heading before holds what it names; under a binding word cap a Fix names what it cuts, or the
  Venue row sums what the Fixes add; a sentence too long for one pass is shortened, never split (one sentence per S).

## 0.3.0 · 2026-10-21 · sentence by sentence logic review

- JL 261021: "当你去 review 整个 paragraph 的时候，能不能针对每句话提出来它有什么具体问题（比如逻辑怎样等等）？ 主要是 review
  逻辑关系：每句话都要看一下上下文 ... 给每句话打分或评估 ... 我觉得这个是 draft review 的一个很重要的 skill"; "我觉得这个
  东西一定要读起来顺才行，而且要有逻辑". New `ref/sentence-logic.md`, Mode 1's step 0: every sentence read with the one
  before and after, five checks (link and its relation, pointers, setup and payoff, claim fit, job), a logic and a read
  score out of 10 (passes at 8 on both, no broken link), the specific problem and the rewrite, one line each, then a
  flow line per paragraph. The rubric's Coherence row sums these lines up.
- Tried on a real Introduction by a fresh reviewer (Skill tool, Mode 1, step 0), which named three gaps, now closed:
  a paragraph's first sentence joins the last of the paragraph before (n - 1 joins, seams included); a repeated noun
  may link across a sentence, only pointer words must land in the one before; a sentence in the wrong place gets
  `Fix: move after S<n>`.
- A second trial closed two more: the first sentence's link is `opening`; a word an author's ruling fixes is noted,
  not scored down.
- JL 261021: "当我们说 logic 的时候 ... transition、逻辑衔接，或者是不是达到了总分总这种结构？ ... 如果这个逻辑没问题，
  或者如果有问题，你该怎么去表述呢？". Logic is read at three levels: the sentence (the five checks), the paragraph's
  shape (topic, support, hand-off: 总分接, a closing summary only at a Section's end) and the Section's arc. The Flow
  line names each paragraph's shape; a problem names the words, what they promised and what the reader got, and a
  sound link says what holds it.

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
