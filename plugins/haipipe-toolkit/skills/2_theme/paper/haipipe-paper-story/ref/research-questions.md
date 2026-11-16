How §3 Research Questions is written: the story question by question, the why-we-ask table, one block per question (haipipe-paper-story).

Open §3 with **the story, question by question**: `**The paper's question**: …`, then a numbered list of the
research questions in reading order, each a plain question with its answer so far and its mark. Read top to bottom
the list is the paper's narrative, and each question's Section is where the paper answers it (JL 261019: "the
quesiton can be the narrative as well"). excalidraw-story titles its steps from this list. Then
`**The narrative, if the questions are answered**`: a numbered list of what the paper can say, step by step, once each
question is answered as expected, item n saying what question n lets the paper say (the Story view pairs them by
number). The face also keeps a `**G0:**` line (JL's mark, ✅ or ⬜) and a `**Desk:**` line
under its studio marks, and §5 ends with a `**We will not claim**:` list; excalidraw-story reads all of these labels
as written.

§3 may then carry **why each question is asked, and how others asked it** (0.30.0, Paper-CMS-AI-Usage 261111): a
table whose header names `why we ask it`, `how others asked it` and `what is new here`, one row per question, its
first cell starting with the question's number (`1 · how many physicians`). The workbench shows the questions as one
table, these three columns between the question and what it lets the paper say (no State column); keep each cell to a few words
and name the prior work (Wu et al., NEJM AI 2024).

```markdown
| RQ | why we ask it | how others asked it | what is new here |
|---|---|---|---|
| 1 · <short name> | <who needs the answer, and why> | <prior work: how it asked it> | <what this paper adds> |
```

Write each research question as one long, plain sentence a patient or a reader could ask out loud, not a short
label (JL 261019: "你不能太简短，你要说得像人话 ... 一个 research question，肯定是相对比较长，然后比较 straightforward、比较易懂的"):
say who asks, what, and against what; follow a factor question with its plain consequence ("What factors influence
whether an AI agent recommends a doctor ..., and is the result fair to doctors?"); keep the sub-questions in
parentheses after it. The `Name` stays the short label.

**Two papers from one study are two Boards** (JL 261019: "我觉得你可以说我们有两篇文章嘛 ... MISQ version"; "for this
one, we want to make it quick and most short"; "we don't need to list all of them"). The ladder keeps one paper per
Board, so a quick, short paper gets its own `paper/Paper-<Slug>/` with its own telling. It lists only the few
questions already answered on disk, and it never takes the long paper's headline; each face names the other as its
companion. First: Project-Example-B's `Paper-Example-B` (a JAMA Network Open Original Investigation, three
questions, the project's original research; first planned as a letter) and its MIS Quarterly companion (four
questions) on a Board of its own.

Write one block per question (JL 260929: "the question is the main block"): a
`#### 3.N · Question N · RQn` heading, the question's own fields, then four
groups, each a bold label and one line per item. Every link is written once,
pointing up the chain, so the block reads as a narrative: the question, the
guesses at its answer, what the paper would claim, why a reader would care,
and the work that tests each guess.

```markdown
#### 3.1 · Question 1 · RQ1
- **Name**: <a short phrase, five words or fewer>
- **Research question**: <one long, plain sentence a reader could ask out loud> (RQ1a: <a smaller question>? RQ1b: <…>?)
- **Question**: <one plain sentence: what we do to answer it>
- **Why it matters**: <its job in the paper, and why a reader cares>
- **Answer form**: <what evidence would answer it>
- **Answer state**: <its mark ✅ 🔶 ⬜, then where the answer stands>
- **If answered**: <what the paper can say if the answer comes out as expected, and what it says if not>
- **Section**: Results, Discussion

**Hypotheses**
- **1a** · <Short name>: <one plain sentence> · tested by Ework01
- **1b** · <Short name>: <one plain sentence> · tested by Ework02

**Potential claims**
- **1a** · C1 · from 1a · <Short name>: <the statement the paper would make>
  - **Role**: <primary · mechanism · scope …>
  - **Now**: <where it stands and what gates it>
  - **If it fails**: <what the paper becomes>

**Potential contributions**
- rests on 1a, 1b · <Short name>: <what the reader gains>

**Potential work**
- **T1** · for 1a, 1b
- **T9** · for 1a · b04.j03.t01, b04.j03.t02
- **D1** · for 1a, 1b
```

The **Research question** is the long, plain sentence (JL 261019, above); its smaller questions follow it in
parentheses, each opening `RQ1a:`, `RQ1b:`, so excalidraw-story can move them to the card. A face written before
261019 may lack it; the Name and the Question then stand in. A question's **Name** is a short phrase of five words or fewer, often itself a question ("Model or data?", "Different Prediction Horizon"), the words the Paper Workbench prints beside "Question N"; the **Question** below it is one plain sentence saying what the paper does to answer it, with no field terms ("We make the model bigger, or give it more training data, and see which one lowers the forecast error."). The precise, technical wording belongs in the hypotheses and claims, not here (JL 260930: "the question here we have are just too long"). Items are coded by question: 1a, 1b under Question 1, 2a under Question 2 (JL 260929).

A question that sets the study's tasks instead of testing a guess (the pretraining task and
the downstream tasks every other question is scored on) comes first, as `#### 3.0 · Question 0
· RQ0`, and opens with a **Tasks** group, one line per task: `- Pretraining · Next reading:
<what the model reads, what it predicts, how it learns>` and `- Downstream · <Short name>:
<what it predicts and how it is scored>`. Its other groups say `- none: <why>` (JL 260930:
"we missed one important question about what is the task we used here … what is the
pretraining task, and also the downstream task"). The Paper Workbench draws the Tasks
first and leaves out the groups that are empty.
A hypothesis and the claim it yields share a code; a claim keeps its paper-wide id
(C1, C2, …, used by the Pitch, §8 and the Section Pages) right after its code. Every
item is a short name, a colon, and one plain sentence (JL 260929: "short-phrase-name:
explanation"), so the bold names alone read as the argument. A hypothesis guesses an
answer and names the §5 evidence rows (Ework01, Ecite01, …) that test it. A claim says which
hypothesis it comes from; a hypothesis may yield no claim (a corollary the paper will
never claim says so as `- none: <why>`). A contribution names the claims it rests on.
A work item names a §7 Task or §6 Discovery row and the hypotheses it tests;
addresses after it narrow a row several questions use to the folders this question
needs. The foundation every question stands on (the training set, the model runs,
their scores) is not listed: its §7 row says `every question`, and it belongs to
every block. The Paper Workbench reads these blocks for its High-level logic +
Low-level work tab; the older one-row-per-RQ table is still read (`RQ | question |
why the paper needs it | answer form | Discovery | Task | intended claim/Section |
answer state`), with one hypothesis per §5 evidence row.

The RQ text describes the paper's inquiry. State and cross-references keep the
inquiry traceable, but they are secondary to the question and answer logic.
An RQ asks; a hypothesis anticipates an answer; an evidence proposition states
what is or could be supported. Operational checks need not become separate
RQs. One RQ can need several propositions and several inquiries or analyses.
“Answered” describes a supported answer, including a null or adverse answer;
it does not mean the hoped-for proposition was confirmed.
