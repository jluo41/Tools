# excalidraw-story · changelog

## 0.2.0 · 2026-10-19 · Room for long research questions

- The main frame keeps the long, plain research questions (JL 261019: "你不能太简短，你要说得像人话 ... 比较长"): when the
  face has a narrative, the paper's question is the frame's key point and the answer so far heads the narrative
  frame instead, so four long questions still fit the 200-word map.
- The paper's question may wrap onto several lines in the face (`joined`); it was cut at its first line.
- The title wraps short of the size badge; the count line under it reads "N answered · N partly · N not yet, in red".
- The narrative and the question cards stand beside the main frame as a Job's results do (excalidraw-job's
  `results_layout` and `results_lanes`, imported): top to bottom in reading order, each as near its step as it can
  inside the main frame's top and bottom, or one run centred on it that rises above it exactly as far as it hangs
  below; every other one a step right (错位); a step's line runs straight to its card when level, else along its own
  lane (JL 261019: "make the RQ to be places like this, and it can be as wide as possible"; "最上面的元素，不要超过最上面
  和最下面的边界"; "也是上下排，但是你可以宽一些 … 就跟我们那 job"). The cards are as wide as it takes for the run to stand about
  as tall as the main frame (2,800 to 6,000 px, `CARD_WIDTHS`; wider than a screen is `canvas.large`), their words, and
  the narrative's, scaled to a 2,800 px card; past the frames below the main one when the run hangs that low.
- Every story draws (JL 261019: "yes, please update all the stories"): a face with no question blocks is read from
  its Board's Questions' reports (as excalidraw-workflow does), else from an older §3 table (`| RQ | question | why
  the paper needs it | … | answer state |`); "Why the paper needs it" is its why, 🔨 reads as partly, a §7 table with
  no `state` gets no marks and no path frame. A generic title ("The Story: one prospective paper") gives way to the
  Board's name; with no `**The paper's question**:` the spine's question, the first question, or the one-sentence
  identity stands in. Many long questions share the main frame's 200 words, each keeping its first words. Drawn
  this way: OpioidRx's MISQ, RoboticSurgery, TestToLearn and ScalingGlucose (its own builder kept in `history/`).
- The target venue's details (JL 261019, in the Pp-LLMRecPhy-Policy session): an optional `#### V1 · <title>` bullet
  block under §9 is read into `vdetail` and drawn as one card under the venue list; a face without it draws as before.
- From a fresh-agent test: the path frame no longer names one person ("waits for a person to start it"; G0 is "a
  person's mark"); "1 Run", not "1 Runs"; G0's mark is ⬜, which the renderer can show (🙋 could not); a Run is red
  when its `starts` cell says "<person> starts"; a §7 table with `name` and `feeds` instead of `work` and `where` is
  read too. The frame numbers left the "What it reads" table, where they disagreed with the drawing.
- Once the paper has a plan, the plan owns what is missing (JL 261020, of the "From here to the send" frame: "is
  this more like the plan? right? Maybe we can drop it"): when the Board's studio holds `s03-paper-dataflow` or
  `s04-paper-workflow` (haipipe-paper-plan), the path frame is not drawn; one line under the main frame names the plan
  topics and G0's mark, and the acts are numbered without a gap. A story with no plan topic still draws its path.
- Each question is a row of three frames, read left to right (JL 261020, of the 6,000 px cards: "these are too words,
  you can add the new frames to the rigth of them as well, try to explain them well"): its card (why it matters, now,
  its theories, its Runs), what we expect and why (each hypothesis with the theory in its closing bracket and its
  evidence rows), and what the paper can say (if answered, each claim with now and if it fails). Each frame is 2,800
  px with its words scaled up; the width search up to 6,000 px (`CARD_WIDTHS`) is gone.
- The theory is drawn (JL 261020: "for the s02, of the MISQ, where is the theory? ????"): §4's theory table as one
  frame of stairs by role, each theory with the questions it serves and the hypotheses §3's development table gives
  it, keyed by the Theory bullet's one-line claim; each card names its theories. Frame numbers run past ⑩.
- Left of the theory frame, "How it fits together": a grid with one row per question, read across its theories, its
  hypotheses and its claims (JL 261020: "你可以在它左边再去做一个 ... 做个 table 之类的").
- §9's further `#### V1 · <title>` blocks each draw as a frame to the right of the venue list (JL 261020: "再多加一些
  evidence ... 为什么这是一个 plausible work"). The question rows clear only the frames below the main one that they
  actually reach, so frames far below do not push them right. Frame numbers past ⑳ read (21).
- The main frame is the signboard, drawn three times the size of every other frame (`MAIN_K`): its margins, steps,
  boxes and words all scale, so it reads first and the rest explain it (JL 261020: "你可以把它变得很大 ... 就跟我们招牌
  一样 ... 它是主，其他都是次，我们要做到主次分明").
- The fit table moved into the main frame (JL 261020: "每个 C 内部的东西，比如像这个 … how it fits together，其实可以
  放到这个大里面去 ... 让它变得越大越好"): with §4's theories, each step reads on to its right as one table, its
  theories, hypotheses and claims, and its line to its card leaves from the row's end; the separate "How it fits
  together" frame is gone. The main frame is a signboard (`canvas.signboard`, k = 3), so ⑦ allows it 600 words, and
  the long research questions are no longer cut to share 200.
- Each question is one wide frame, its card, hypotheses and claims as three panels side by side (JL 261020: "for each
  RQ here, could we just have one frame, one very wide frame for each RQ?"): one title a row instead of three, an
  arrow between panels; marked `canvas.columns` so ⑨ judges a wall of text per panel. The MISQ story drops from 22
  frames to 12.
- A pass for the look, checked in Excalidraw itself (headless Chrome over the Studio's own viewer), not only in the
  preview PNG, which draws no frame names (JL 261020: "这里都糊成一团了 ... 为啥这里就没有 style 了 ... 是不是主次分明，
  是不是让人有 zoom in 去读的欲望"): the frames on the right stand ROW_VGAP (420) apart, so each frame's name has room
  above it; the Act 2 label sits well above the column. The hypotheses panel opens on a scoreboard ("10 hypotheses from 6
  theories: 6 with evidence in hand, 4 waiting for a Run"), marks each hypothesis by its evidence (`held()`: ✅ 🔶 ⬜),
  draws an untested one dashed, and sets its name larger than its sentence; claims the same. The card's answer now
  reads a line a finding. The main frame's table is larger and marks each hypothesis and claim.

## 0.1.0 · 2026-10-19 · The story as its questions

- New skill (JL 261019: "In the story studio s02-story, I think we might need to list the research questions, and
  how could we support them"; "should we have a things named /excalidraw-story?"; "This is more like the story, do
  you get it."; "please make the story, I think it should be composed a list of the questions to answer, and the
  quesiton can be the narrative as well").
- `scripts/story_drawing.py draw | make <topic>`: ① the paper's question, the chain of question names, and each
  research question as a step titled by its narrative question, its card the answer so far, its claim, its E rows
  and T rows with their marks (⬜ red and dashed); ② the pitch; ③ what we will not claim; ④ the Runs still to make,
  who starts each, then G0. Read from the telling's face on every build; excalidraw-ideation's boxes and frames, so
  s01 and s02 look alike.
- Each question is a professional research question with why it matters and what the paper can say once it is
  answered (JL 261019: "could you make the questions to be more like the research questions? The professional
  research questions."; "if these questions or hypothese be answered, wht is the narrative behind we can have? Why
  these questions are important"). The main frame holds only the questions as steps; each has its own small card
  (why it matters, now, if answered, E and T rows), and ② is the narrative, if the questions are answered.
- Tested by a fresh agent on a scratch copy: it loaded this skill with haipipe-paper-story, updated the face and
  redrew. Its review made the main frame pass excalidraw-studio's check (words, size, three acts named), made a work
  row's mark read its state's first word ("not done" is ⬜, not ✅), and kept a wrapped heading from ending a list.
- Act 4 · Where the story could go: §9's venues as stairs, from the target to the fallbacks; a venue with no
  desk record is red and dashed (JL 261019: "我们要不要把这个 venue 直接塞到这个 story 里面去？ ... 也要想想它适合什么样的 journal，然后搞出来一个 journal list or conference list").
- First user: Project-LLMRec-Physician's `studio/s02-story-misq-agent-physician-visibility/` (now on its MIS Quarterly Board), four questions, 2 partly answered.
