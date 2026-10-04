Method
======

1 · The six steps
-----------------

| step | what happens | methods | where in the workbench | who signs |
|---|---|---|---|---|
| Plan | freeze the brief, then the parts, paragraphs and Bullets, one role each | Draft | Draft › Table · runs Context, Structure revise | the plan |
| Draw the logic | the claim at the left, the reasons beside it, every Bullet a row | Draft | Draft › RoadMap Draw · run Draw the logic | the logic |
| Bind the evidence | every value, citation and display bound to the Result it came from | Evidence | Evidence › Citations · Displays · Values · runs Bind / update, Build figure / table | the source check, each display |
| Write and adopt | one sentence per Bullet, then adopted into the Page | Draft | Draft › Reading · Revise · runs Auto write, Section or Paragraph revise | adopting the draft |
| Check | an agent that did not write the Page runs the six tests | Delivery | Delivery › Checks · run Check | none: the checker routes |
| Build | one source built as a web page, LaTeX and Word | Delivery | Delivery › Preview · Artifacts · run Build | the release |

A failed check goes back to the step that owns the fault: a missing reason to Plan, a
stale number to Bind the evidence, an unclear sentence to Write. Nothing is fixed in the
built files. Every run is in the Runs panel beside its Space, with the prompt to start it.

One example runs through this page, and it is made up: a paper Section that asks whether a
reminder text raises prescription refills.


2 · Steps 1, 2 and 4 in depth: the Draft methods
------------------------------------------------

The plan comes before any prose, and the logic before the sentences, so each sentence has
a reason to be there. In the example, the plan names four Bullets under the claim
"Reminders raised refills", the logic tree hangs them under three reasons, and each
sentence is written from its Bullet.

| family | method | card |
|---|---|---|
| Draft: What will the Page say, and why? | By outline first | methods/draft/01-by-outline-first.md |
| Draft: What will the Page say, and why? | By logic tree | methods/draft/02-by-logic-tree.md |
| Draft: What will the Page say, and why? | By reader expectations | methods/draft/03-by-reader-expectations.md |

| test | asks | when | source |
|---|---|---|---|
| T1 Logic | every Bullet sits under a reason in the logic tree | step 2 | claim, grounds and warrant (Toulmin 2003) |
| T0 Covered | every Bullet of the plan is realized by one Page sentence | step 4 | (ours) |


3 · Step 3 in depth: the Evidence methods
-----------------------------------------

A number on a Page is never computed there and never typed in: it is bound to the Result a
Run wrote, and the Page keeps which one. So any sentence can be followed down to its file.

```
sentence   "Refills rose from 41% to 44%."         (made up)
   ↓ realizes
Bullet     B4 · [Result] refills rose in the reminder arm
   ↓ binds
Result     results/r03_refills/metrics.json, written by its Run
```

| family | method | card |
|---|---|---|
| Evidence: Where does each number come from? | By bound value | methods/evidence/01-by-bound-value.md |
| Evidence: Where does each number come from? | By provenance | methods/evidence/02-by-provenance.md |

| test | asks | when | source |
|---|---|---|---|
| T2 Bound | every value, citation and display names the Result it came from | step 3 | provenance records (Moreau & Missier 2013) |
| T3 Fresh | no bound Result is newer than the Page's reading of it | step 3 · step 5 | dynamic documents (Gentleman & Temple Lang 2007) |

In the example, T2 fails if "44%" names no Result, and T3 fails if `r03_refills` was rerun
after the Page read it.


4 · Steps 5 and 6 in depth: check and build
-------------------------------------------

The Check run judges all six tests, T0 to T5, and is done by an agent that wrote nothing on
the Page; it returns CLOSE or the step to go back to. Then the one source is built in every
format, and a person signs the release.

| family | method | card |
|---|---|---|
| Delivery: How does it reach the reader, checked? | By independent check | methods/delivery/02-by-independent-check.md |
| Delivery: How does it reach the reader, checked? | By single source | methods/delivery/01-by-single-source.md |

| test | asks | when | source |
|---|---|---|---|
| T4 Independent | an agent that did not write the Page checks it | step 5 | self-preference of model evaluators (Panickssery et al. 2024) |
| T5 Builds | the one source builds the web page, LaTeX and Word | step 6 | single-source conversion (MacFarlane n.d.) |


5 · Why it works
----------------

A Page says one thing
~~~~~~~~~~~~~~~~~~~~~

A Page is one readable unit: a Section of a paper, a Task's report, a Discovery or Insight
page. It says one thing, and everything on it serves that thing (一页只说一件事).

```
claim      Reminders raised refills
  ↑
reasons    who got them · what was measured · how much it changed
  ↑
Bullets    B1  B2  B3  B4 …          one point each, each with one role
```

Because the claim, its reasons and its Bullets are written down before the prose, a
reader can see the argument before reading it, and a missing reason shows as a gap in the
tree rather than as a vague paragraph.

What the evidence says
~~~~~~~~~~~~~~~~~~~~~~

- Writing is a set of distinct thinking processes, planning, putting ideas into words and
  reviewing, organized by the writer's own goals (Flower & Hayes 1981); the plan is where
  those goals are written down.
- A model judging text tends to score its own output higher than other text human raters
  judge equal (Panickssery et al. 2024), and without outside feedback models struggle to
  correct their own reasoning (Huang et al. 2023). So the writer of a Page never checks it.
- No study tests this whole loop on agent-written Pages; its order is our own judgment.


Reference
---------

Terms and people
~~~~~~~~~~~~~~~~

| term | 中文 | read more |
|---|---|---|
| Argument map | 论证图 * | [Wikipedia](https://en.wikipedia.org/wiki/Argument_map) |
| Topic and comment (given and new) | 主题与述题 * | [Wikipedia](https://en.wikipedia.org/wiki/Topic_and_comment) |
| Literate programming | 文学编程 | [Wikipedia](https://en.wikipedia.org/wiki/Literate_programming) · [中文维基](https://zh.wikipedia.org/wiki/文学编程) |
| Data provenance (lineage) | 数据溯源 * | [Wikipedia](https://en.wikipedia.org/wiki/Data_lineage) · [W3C PROV](https://www.w3.org/TR/prov-overview/) |
| Single-source publishing | 单一来源出版 * | [Wikipedia](https://en.wikipedia.org/wiki/Single-source_publishing) |
| Pandoc | Pandoc | [Wikipedia](https://en.wikipedia.org/wiki/Pandoc) · [中文维基](https://zh.wikipedia.org/wiki/Pandoc) |

| person | 中文 | what they gave | read more |
|---|---|---|---|
| Stephen Toulmin | 史蒂芬·托尔明 | an argument as claim, grounds and warrant, with its qualifier and rebuttal (1958) | [Wikipedia](https://en.wikipedia.org/wiki/Stephen_Toulmin) · [中文维基](https://zh.wikipedia.org/wiki/史蒂芬·托尔明) |
| Linda Flower | 琳达·弗劳尔 * | writing as goal-directed thinking processes, with John R. Hayes (1981) | [Wikipedia](https://en.wikipedia.org/wiki/Linda_Flower) |
| Donald Knuth | 高德纳 | literate programming: a program and its explanation as one source (1984) | [Wikipedia](https://en.wikipedia.org/wiki/Donald_Knuth) · [中文维基](https://zh.wikipedia.org/wiki/高德纳) |

* no Chinese Wikipedia page or settled translation; the Chinese here is ours.

Where a Page sits
~~~~~~~~~~~~~~~~~

```
🧪 Task, 📚 Discovery, 🔎 Insight      Runs write Results with receipts
        ↓  each Evidence Item binds one Result
📄 Page    plan → evidence → prose → check → build
        ↓
📑 a paper Section, a Task report, a Discovery or Insight page
```

The same workbench writes every kind of Page; the families differ in what they ask, not in
how a Page is written (ours). The papers behind each method are listed in Related Paper.
