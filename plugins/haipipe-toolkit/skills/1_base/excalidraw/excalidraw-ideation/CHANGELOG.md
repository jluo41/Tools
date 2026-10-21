## 0.1.0 · 2026-10-14 · An ideation as one drawing, its ideas as steps

- New skill (JL 261014: "How do you think we can add it to the themes/paper skills set"; "Or we should have one named
  excalidraw-ideation?"; "haipipe-paper-ideation will call it to draw when it is available").
- `scripts/ideation_drawing.py`, lifted from Physician-SPACE Paper-LLMRecPhy-Quick's `build_s01_ideation.py` (JL 261013:
  "主次分明 … 阶梯状的结构 … 你不能每一个都是朝左对齐"): ① every idea as steps, ② the setting, one card per lead
  idea, the path to G0. `draw <topic>` and `make <topic>`; the words in `<topic>-drawing.yaml`.
- Generalized: the question, heading and frame name come from `index`; the setting takes a `flow` list (the older
  `roster` keys still read); a card's state comes from the idea's `state`, or from the face's Ideas table by
  `state: columns`. Redrawing Paper-LLMRecPhy-Quick's yaml through it gives the same 164 elements, frames and words.
- A card may carry `does:`, the design in one line under Why it matters (Paper-LoopExpLearning's loop: 12 loops,
  7 new treatments each, 98 a send); absent, the card is as before.
- A card may carry `closest:` and `new:`, its novelty check in two lines (JL 261014: "you also have the
  /novelty-check things for the evaluation … did you add them to the s01 as well?"); absent, as before.
- An optional ⑧ `evaluation` frame below the path, what G0 reads: each test's verdict and who ran it (two a row;
  a test not run is red and dashed), then the venues from ambitious to fallback as stairs (JL 261014: "we should add
  the frame about the evaluation and the targeted journal or venue"). Absent, the drawing is as before.
- First users: Paper-LLMRecPhy-Quick (origin) and Paper-LoopExpLearning's s01 (261014).
