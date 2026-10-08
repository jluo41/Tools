- 261007 · review fixes (version unchanged): Description: read-only display only (setup and launch are haipipe-design's); the cards are the authority until design_views.py reads them; ref/design-board.md and ref/space-mapping.md carry an "older board page only" banner (they stay in place because other skills link them); placeholder examples replace the domain ones.

## 0.15.0 · 2026-10-07 · The design ladder on the shared frame (JL 261007; b12 s11 · s12 · s13 · s21) (version unchanged)

- SKILL.md rewritten for the ladder: tabs Guide · Block · Job ▾ · Task ▾, the six Spaces at each level as s11 · s12 ·
  s13 draw them, the files each view reads (design_reader.py · design_views.py · design_theme.py), the Runs panel from
  `haipipe-design-workflow/references/run-cards.md`, read-only. Notes that design_views.py still types its buttons in
  code; reading them from the cards is the next server change.
- The older page's text moved word for word to `ref/legacy/older-page.md`; `ref/design-board-space-mapping.md` moved to
  `ref/legacy/`. `ref/design-board.md` and `ref/space-mapping.md` stay in place: other skills link them there.

## 0.15.0 · 2026-10-07 · Renamed from haipipe-workbench-design (JL 261007)

- The skill is `workbench-design` (was `haipipe-workbench-design`), its folder `design/workbench-design/`, its trigger `/workbench-design`; every live reference in Tools follows. Older entries below keep the old name.

# Changelog

## 0.14.21 · 2026-10-05 · Method folders (JL 261005)

- JL: "each job will be a method of design settings … 2-Design-xxxx(method1) 2-Design-xxx(method2)";
  "do not change the UI that much". A board may hold `2-Design-M<NN>-<slug>/` groups, one per
  method, each with a `method.md` card and the Brief's tasks as Design Folders
  (`haipipe-design/ref/method-folders.md`).
- Board: the snapshot reads every group; a Brief row matches its folder under each method by name
  or Design-NN; Design Tasks' Views become one per method, no All View ("we can remove All"; its
  card's three steps side by side above the same table); New Design Folder opens a task under the method it is clicked in;
  the facts band counts methods; the csv gains a `method` column. A board with only `2-Design/`
  keeps the family Views and reads as before.
- Page: the header band names the method from `../method.md`; `?folder=M02/Design-01` and
  `/w/<board>/m02-design-01` reach one method's page, and a bare id held by several methods
  answers with a page listing them.
- Tests: `MethodFoldersTest` (snapshot, Views and card, New Design Folder under a method, csv).
- Under each method, the design unit's three steps as a second row of Views (JL 261005: "after
  adding the subspace (Method M01), we can add its subsubspace"): ① See input (the packet and the
  goal), ② Designs (opens: the messages and their reasons; JL: "can be changed to the message
  content"), ③ Check output (Verify state and predicted click-through), each with its part of
  `method.md` on top. The task table under the card is gone; a missing task keeps its New Design
  Folder button.

## 0.14.20 · 2026-10-03 · Guide › Method built on the six steps (JL 261003)

- JL: "why we still have this? I am thinking to merge this together"; "let's rethink the overall
  layout". Guide's own step list is off for Design (`explain` placement "only", a new opt-in in
  workbench_guide.py); the page carries the steps. The page: the picture, 1 The six steps (one
  table: what happens, where in the workbench, who), 2 Step 2 in depth (families, which method
  when, the cards), 3 Step 3 in depth (the element record), 4 Steps 4 and 6 in depth (the tests,
  the evidence), 5 Why it works (Simon, the four reasonings), Reference folded. Nothing cut.
- Parts are larger than their sub-sections on the page (article.theory h2 18px, h3 14.5px).
- Every part folds, in Guide's card style (JL 261003: "make each section collapsable"): the
  drawing card "Method design" and 1 The six steps open, the rest closed.
- The methods drawing adds a row for the four kinds of reasoning (what each knows and finds, a
  soup example, where it sits here, its Chinese term) and groups the 13 cards under the three
  families (Goal Only over two columns, External Insights one, Internal Insights three).

## 0.14.19 · 2026-10-03 · Guide › Method in five parts, one document (JL 261003)

- JL: "the structure of the method is not smooth"; "I want A to E, could you make the E to be
  the references?"; "we still need to have the draw". Guide › Method is the six steps, the
  methods drawing (at the top, redrawn: no "Design methods" title, Design Task), then one
  document, `ref/design-method.md`: A What design is · B The design methods · C How a design is
  checked · D In the workbench · E Reference, folded. It replaces `design-theory.md` and
  `design-methods.md`; nothing was dropped, the reference material moved into E.
- Three families, by where the rule comes from: Goal Only (By goal, By principle, By
  exploring, By slots), External Insights (By theory, By implementation), Internal Insights
  (the other seven). By theory and insight carries `also: External Insights` and shows in
  both board Views. B2 is a which-method-when guide.
- Plain explanations: Simon's sentence in plain words, the reasonings as sums, messages and
  soup diagrams with Chinese terms; terms and people with verified links; web links render.
- The Method page builds no board snapshot and only the views it shows (6.6 s to 0.05 s).

## 0.14.18 · 2026-10-03 · Design Task, with four views; one look for tabs and boxes (JL 261003)

- The page's Spaces are Design Task · Design Item · Delivery (no "Space" on the tab, as the
  board's Design Tasks). Design Task shows four View tabs: Aim · Requirements (the channel
  requirements and the rules) · Resources · Leave out; `?view=` opens one. The file stays
  `design-goal.md`, read the same way.
- The board header follows the Insight board's: the title, all boards · board index, one
  band of facts; the records-check line is gone from it.
- Space and View tabs take the shared Guide's look (400 16px, a filled pill when on), and
  each working Space sits in one box like the Guide's. The design card keeps its three
  columns at every width.
- The page header follows it too (all boards · ↑ Board level, which now opens the owning
  board from a /w/ link; a band of facts); the insight-eligibility line is gone, and the
  Runs panel stays on the right at every width.
- Guide › Related Paper is untitled, so its papers show unfolded; the RoadMap drawing is
  titled Workbench design.

## 0.14.17 · 2026-10-03 · Guide › Method holds the theory itself (JL 261003)

- JL: "move the design theory things to here. We do not [want] the things named Design
  methods; here is the new Method view to hold that information". Guide › Method is the six
  steps, then one page with no sub-tabs: the theory (`design-theory.md`, sections 1 to 9,
  the shared loop now section 6), the method cards (`design-methods.md`, retitled "The
  method cards", sections 10 to 12) and the methods drawing. The theory page's new `method`
  view composes them; it shows only when asked for (`views=method`).
- No view, heading or card line is called Design methods any more.

## 0.14.16 · 2026-10-03 · Guide › Method reads like Insight's (JL 261003)

- JL: "for the Design, its guide is very very bad", against Insight's Method. Design's six
  steps now lead the View and are actions (Set the Design Goal · Pick the method · Generate
  N designs · Evaluate · Release · Run the Exp); the framed page follows them, its sub-tabs
  in the order Design methods · Methods studio · Design theory (`views=` sets the order).
- `design-methods.md` is 131 lines, not 240: the shared loop with one paragraph, then the
  thirteen cards, the tests and the evidence. The reasoning, the two loops, the design
  elements, the six families and O'Cathain's map moved to `design-theory.md`, sections 6-9.
- `workbench-table.md`: Guide rows in place of the old Theory of Design rows, and a Folder
  column; Guide › RoadMap Draw shows it, with a Workflow block from the entry's new `flow`.

## 0.14.15 · 2026-10-02 · Guide is Description · Method · RoadMap Draw · Related Paper (JL 261002)

- JL: "we don't need the skills set"; "all the four just to one RoadMap Draw, and then add
  the Related paper"; "Descriptions, then Method, and then RoadMap, and then Related Paper".
  The shared Guide now has those four Views; the Design entry gives a `description` and
  frames three pages: Method (Design theory · Design methods · Methods studio), RoadMap
  Draw (`design-workbench-ui.excalidraw`, now one drawing of the skills, the method, the
  workbench and the folders) and Related Paper (the Papers view alone).
- The theory embed takes `views=<comma list>` to show a subset of its views. Old
  `space=theory|methods|studio` links forward to `guide=method`, `space=papers` to
  `guide=related-paper`.
- Docs, the 13 cards and the reference files say Guide › Method and Guide › Related Paper.

## 0.14.14 · 2026-10-02 · The theory moves into the shared Guide (JL 261002)

- JL: "follow the design here, workbench-shared, to update workbench-design"; "work on the
  guide space first"; "this is the guide I want to keep" (Design theory · Design methods ·
  Methods studio · Papers). The theory explains the family, so it is Guide › Methods now:
  Guide frames this board's theory page (`/_board/design-board?embed=theory`,
  `render_theory_embed`) at the top of the View, its four views unchanged, the methods
  studio still saving to `ref/design-methods.excalidraw`. The generated method flow folds
  beneath it.
- The board keeps one working Space, Design Tasks. An old `space=theory|methods|studio|
  papers` link forwards to `guide=methods` (303). The theory script is one constant,
  `_THEORY_JS`, used by the framed page.
- The Design family's Guide entry (`servers/workbench-shared/guide_families.py`): five
  skills; six method steps (requirements, insights, method, Generate, Evaluate and the
  Revise loop, Ready and the Exp and the Learning loop); Spaces at both levels; folders
  with element records. Its new optional `explain` field (view → route, params, title,
  "first") lets a family's own page lead or follow a Guide View; only Design uses it.
- Guide › Workbench shows the generated UI map, then the UI design drawing
  `servers/workbench-design/studio/design-workbench-ui.excalidraw`: eight screens in
  workbench-shared's style, generated by `design-workbench-ui.py` from its drawing pieces.
- The 13 method cards, `design-methods.md`, `design-theory.md`, `design-papers.md` and the
  board docs say Guide › Methods where they said the Theory of Design Space.

## 0.14.13 · 2026-10-02 · The element record is required (JL 261002)

- When the board's Design Goal names its elements, `add_item` appends one rule to every
  new Design Item: "every element recorded", a semantic rule that commissions
  `elements.yaml` and lists the Design Goal's element names (`goal_element_rule`). The
  Generate writes the record under those names, the Verify checks it, and the element
  matrix reads it first. An item that already has its own `elements.yaml` rule keeps it;
  a board without the line is unchanged.

## 0.14.12 · 2026-10-02 · The element matrix (JL 261002)

- The Design Space shows an **element matrix** above the cards (JL: "I want to see how
  design element played an important role here"): one row per design with a draft, one
  column per element the Design Goal names (`Elements:` under Resources), and `added`.
  `·` kept, `★ <words>` changed, `removed`; a last row counts how many designs changed
  each element. A design's element record is read first (`record_reading`); otherwise a
  word comparison with the starting text (`slot_reading`). A task whose designs each
  change one element reads as a one-element-at-a-time comparison at a glance.
- The board's Design Goal gains its `Elements:` line.

## 0.14.11 · 2026-10-02 · Both insights, design elements, a methods pilot (JL 261002)

- A sixth family, **With both insights**, and a 13th card, **By theory and insight**
  (JL: "how about the family that use both external and internal insights?"): follow a
  signed insight that a named theory explains; where they disagree, the insight decides
  for this audience and the gap becomes a question for the next Exp. With the first
  three families it makes a 2 × 2 of external and internal insights. The cards after By
  tailoring renumber 10 to 13.
- **Design elements** (JL: "how to choose each element … the reasoning of the designer
  … sometimes … the intuitive … we can document both"): `design-methods.md` §2 says a
  design is a set of elements, each with where it came from (requirements, internal,
  external, intuition) and how it was chosen (reasoned, System 2; intuitive, System 1,
  recorded as a hunch and never warrant), after Evans & Stanovich 2013 (Paper Run r65)
  and MacLean 1991. The run contract gains an optional element record
  (`elements.yaml`); the card's Design elements fold shows it, as the designer recorded
  it, above the comparison with the starting text.
- A methods pilot is registered in one Design folder: four items with
  one open goal, one bet and the same rules, differing only in `basis` × `mode`: By goal
  (brief-only, compose), By theory (brief-only, theory-driven, the board's message
  theories as reference), By insight (evidence-informed, compose) and By theory and
  insight (evidence-informed, theory-driven). Each commissions the element record by a
  semantic rule. They wait for a person's release.
- The Methods studio drawing shows six family columns and an element-by-element example.

## 0.14.10 · 2026-10-02 · Revise loop and Learning loop (JL 261002)

- Two loops named (JL: the evaluation "serve as the inner loop" and goes "back to the
  Method if it think it is not good"; "Exp will be the outer loop"). The **Revise loop**
  (inner) is Method, Generate and Evaluate, repeated until the design passes: a broken
  rule goes back to Generate, a weak reason (critique or pretest) back to Method. The
  **Learning loop** (outer) starts at Ready: the Exp tests the design in use and its data
  becomes the next internal insights. The names follow Hevner 2007's tight Design Cycle
  inside a Relevance Cycle; its Rigor Cycle is the external insights.
- The step "Test now" is now **Evaluate**. The test codes leave the format diagram: T0
  to T3 are Evaluate, in the Revise loop; T4 is the Exp, in the Learning loop
  (`design-methods.md` §3, "How a design is evaluated", with a `where` column). Cards say
  "tested in Evaluate … in the Exp" (`method_cards(..., now=)`); other boards keep "now".
- Hevner 2007 joins the papers table without a DOI (its journal issues none; checked in
  the AIS eLibrary), so it opens no Paper Run.
- Both drawings show the two loops.

## 0.14.9 · 2026-10-02 · Three inputs, Design, Exp (JL 261002)

- The format is now **design requirements + internal insights + external insights →
  Design → Exp** (JL: "internal insights, which from the internal data, and then external
  insights, like the open domain knowledges, the literatures, and also design
  requirements"). The requirements are the Design Goal; internal insights are signed on an
  InsightBoard from our own data (past experiments, readers' records); external insights
  are the literature and theory. The Exp is the test in use (T4, renamed from Field), and
  its data is the next round's internal insights.
- Reasoning sits in fixed places (Dorst 2011): induction makes insights, Design is
  abduction (abduction-2 with no insight, abduction-1 with one), the test now is
  deduction. `design-theory.md` names the two abductions in its table.
- Five families by where the design's how comes from, replacing From the goal, From what
  is known and From trying: Requirements only (By goal, By principle); With external
  insights (By theory, By implementation); With internal insights (By insight, By
  precedent, By revising, By tailoring); Making internal insights now (By user test, By
  co-design); Making internal insights next (By exploring, By slots). The cards renumber
  1 to 12 in that order.
- Two new cards: **By revising** (change one tested design where its result says;
  Nielsen 1993, Kohavi et al. 2009) and **By tailoring** (a design per segment of readers,
  per reader later; Hawkins et al. 2008, Noar et al. 2007, Nahum-Shani et al. 2018), each
  paper a Paper Run (r60 to r64).
- A card's head gains `reasoning:`; its `reads:` names the inputs, and the view colours
  each by kind (requirements, internal, external). Design methods says "in the Exp" where
  other boards keep "in use" (`method_cards(..., in_use=)`).
- The Methods studio drawing is redrawn for the new format and families; the workbench
  drawing's Design methods panel follows.

## 0.14.8 · 2026-10-02 · Ten methods, every O'Cathain category placed (JL 261002)

- Two new method cards. **By implementation** (7, From what is known): design for reach,
  adoption, delivery and lasting effect, from RE-AIM (Glasgow et al. 1999) and the
  overview's implementation-based approach. **By co-design** (10, From trying): design
  with the people it is for, from the overview's partnership approach and Voorberg et
  al. 2015; its AI form is a simulated patient panel that helps decide (JL: "we can use a
  LM to simulate the patient … that is a future design"), so it carries `status: future`.
- The cards renumber: By user test is 8, By exploring 9. Families: 1 to 3, 4 to 7, 8 to 10.
- `design-methods.md` §2 maps all eight O'Cathain categories to where each lives here
  (stepped = the shared loop; intervention-specific = a board's Design Goal; combination
  = By exploring); none is left without a place.
- By slots adds MOST's three phases (preparation, optimisation, evaluation) from the full
  text of the overview.
- A future card is dashed and tagged "future · not run yet". Papers: two rows, each a
  Paper Run (r58, r59) with abstract and verbatim BibTeX.
- The Methods studio drawing shows the ten cards and the category map.

## 0.14.7 · 2026-10-02 · Methods studio (JL 261002)

- A fourth Theory view, **Methods studio** ("add a new studio … put it in the excalidraw
  to explain these methods"): `ref/design-methods.excalidraw`, drawn once (the shared
  loop, the three families of method cards with their status, an open card's two sides,
  T0 to T4, the bet), opened in the self-hosted Excalidraw canvas as the Paper
  workbench's RoadMap Draw is, and loaded only when the view is shown.
- Saving it works on a machine where `Tools` is a link: the studio workbench's
  `excalidraw-save` now accepts a scene inside a folder linked in at the root itself
  (`under_root`); a link deeper down, or a path that climbs out, is still refused.
- The shared loop's second step is **Method**, not Frame (JL 261002: "why we call it a
  frame?"): it is where a method is chosen and what it reads is read. Frame stays the
  word for Dorst's frame creation, in Design theory and the By principle card.

## 0.14.6 · 2026-10-02 · Method cards read against O'Cathain et al. 2019 in full (JL 261002)

- Each card gains a `taxonomy` line: its category among O'Cathain's eight approaches, or
  why it has none (By goal, By principle, By exploring) or sits outside them (By
  precedent, adaptation).
- The cards' literature side adds what the full text says, cited `[O'Cathain 2019
  taxonomy]`: research waste (By goal); understand the real issues first (By principle);
  efficiency-based designs, factorial and micro-randomised (By slots); mapping
  determinants to techniques, authors' reports of effect, several theories (By theory);
  assessing the evidence base (By insight); adaptation (By precedent); think-aloud and
  diverse samples, randomised-trial reports, slow iteration (By user test); divergent then
  convergent, several rough prototypes narrowed to one (By exploring).
- `design-methods.md` §2: why partnership and implementation-based have no card, the
  seven domains mapped onto the shared loop, and the paper's six questions for choosing.
- A citation that names two papers of one author and year picks one by a title word.

## 0.14.5 · 2026-10-02 · Design method cards (JL 261002)

- The Design methods view draws the eight methods as cards, one file each in
  `ref/methods/` ("make each of them a card (design method card)"), grouped into three
  families by where a design's reason comes from. `design-methods.md` section 2 is now
  their index table; its two earlier tables are folded into the cards.
- A card, open, sets What the literature says (rationale, context, the authors' steps,
  strengths, limitations; O'Cathain et al. 2019, Table 2) beside **Applied to AI** (the
  agent, its steps, returns, verify, AI risk, evidence on AI, skill) ("add a new thing
  about how this can be applied to AI").
- Every bracketed source, and every "comes from" source with its idea, links to the
  paper's card in the Papers view, which opens on it (paper cards carry an id).
- Closed, a card says whether any study tests the method; four say none does yet.
- The doc reader draws pipe tables as tables.

## 0.14.4 · 2026-10-02 · Papers live in the workbench, with their PDFs (JL 261002)

- The Papers view reads the workbench's own `ref/design-papers.md`, the same for every
  board ("put them in the Tools of the workbench of the design"); the board-level
  `design-papers.md` is gone. Its last column is `pdf`, a file in `ref/papers/`.
- `ref/papers/` keeps the 10 full texts under CC BY, listed with their licenses in
  `ref/papers/README.md`; a paper under any other license is not kept there.
- A card without its own copy borrows the free copy, abstract and Paper Run link of a
  Discovery Paper Run in the board's Project that holds the same DOI.
- A card with its PDF carries a **PDF** badge, and **Show only the N papers with a PDF**
  hides the rest and opens the folds (JL 261002: "I can still not see the papers").
- A file reached through a folder linked under the root (`Tools`) gets a server path.

## 0.14.3 · 2026-10-02 · Papers: each card reads its Paper Run and shows the PDF (JL 261002)

- A row's `record` names its Discovery Paper Run by compact address (`b01j01t01r09`);
  the card reads that Result under the Project's `discoveries/`: its abstract (folded)
  and, when a lawful free copy was saved, `paper.pdf` shown in the open card (loaded on
  open) and in a new tab. 📄 marks a card with its PDF inside; the head counts Paper Runs
  and PDFs. A legacy topic note (`S02/02 · S007`) still links after the address.
- A card says which case it is: no free full text, no DOI and so no Paper Run, or not yet
  a Paper Run.

## 0.14.2 · 2026-10-02 · Theory of Design: three views, and Papers (JL 261001)

- The Theory of Design Space shows one view at a time, all general: Design theory,
  Design methods (new `ref/design-methods.md`: the shared loop, eight methods, the T0 to
  T4 tests, what the evidence says), Papers (URL `view=`). The board's own message
  theories are no longer shown here; Add a theory moves to the Design Goal's Resources. Papers reads the board's `design-papers.md` and renders it as the Paper
  workbench's Related Papers: a band per design method, a card per paper (title; who ·
  year · journal; role), why it is here and its links inside.
- Its Runs panel adds **Add a paper** (Discovery orchestrator, `haipipe-discovery`): it
  turns one row into a Paper Run and fills the row's `record`.
- A card in a UTD24 journal carries a UTD24 mark, and the head counts them (JL 261002).
- A `key` column marks the papers a board's methods rest on most; each band shows those
  and folds the rest under "N more papers" (JL 261002).
- The reader of these files joins a list item that wraps onto an indented line.

## 0.14.1 · 2026-10-01 · Rationale: Evidence chain and Design elements (JL 261001)

- The card's Rationale is the Design move and two folds, the Design elements first. **Evidence chain**: from each
  row the design acts on (`because:`) down the links the insight pages record on their
  `←` lines, one quoted row per level, to the data; named DO NOT rows are Limits; cited
  pages off the chain are "Also cited". **Design elements**: the shown draft against the
  Design Goal's `Starting text`, each element kept, new, removed, changed or required by
  the Design Goal, with the rows that support it. Replaces the Insight Evidence ladder,
  the Rule followed block and the stance/basis words.
- `because:` reads the current page ids and several rows (`W01-full · W1, W3`; pages
  split by `;`); a named row not on its page says so.

## 0.14.0 · 2026-10-01 · Workbench Table (JL 261001)

- `ref/workbench-table.md`: Level · Space · View · Run type · Agent · Skill · Person signs for
  both levels, in the `table-workbench` shape. The Design Goal Space's five views follow the
  blocks of `design-goal.md`; their skill is the new `haipipe-design-goal`. Its cards are
  `haipipe-design-workflow/references/run-cards.md`.
- The Runs panel reads those cards (`design_run_types`) instead of a list in `design.py`: the
  Design Goal Space offers its five run types, and every prompt names the agent that runs it.

## 0.14.0 · 2026-10-01 · Two board Spaces and a Runs panel (JL 261001)

- Board level: Design Tasks Space (was Goal) and a new Theory of Design Space, which renders
  `ref/design-theory.md` and the board's own `design-theory.md`. The board's Design and
  Delivery Spaces are gone; every design, run and delivery lives at the page level.
- Every Space at both levels has the shared Runs panel (`live.runs_panel`), as in the Paper
  and Page workbenches. It replaces the "Run types in this Space" guide, the "New design
  tasks" form and the "New Design Item" form; the native Commission and queue buttons stay.
- The Insight board line and the "Insight pages the designs use" fold are removed at both levels.
- Page level: the Goal Space is now called **Design Goal Space** (the key stays `goal`), and it
  shows the full design input: Aim, Venue (venue default beside this task), Rules, Resources,
  Leave out (what must never appear in the message), each line with its source, gaps counted as "not stated". Source: the board's
  `design-goal.md` with `Task · <folder>` overrides, plus the venue profile and the register.
  Its Runs panel gains a "Design input" run type that fills the gaps.
- `{LINK}` is the link slot: Delivery and the csv show it after the ask's colon on every
  design; stored texts are unchanged. `haipipe-design-unit`'s `max_chars` does not count it.
- The drawing's board frame shows the two Spaces; its Design Theories table names the new Spaces.

## 0.13.0 · 2026-10-01 · Three Spaces at both levels (JL 261001)

- Page level: Goal · Design · Delivery. Goal states the one design task, with the rules every
  design keeps. Design shows the task again above one card per design, each closed row in four
  columns: Design · Rationale · Supporting work · Expectation. A card's insight pages and runs
  fold inside it; the Insight and Run Spaces are gone, and their old links open Design.
- Board level: the same three Spaces. Goal lists the design tasks and the rules every task
  keeps; Design shows one folded block per design task; Delivery is unchanged plus a csv. The
  header names the board only, no counts.
- The screen says `Design N` (the files keep `ITEMNN`) and "design task" again, not "targets".
- `/_board/design-bundle?…&folder=<name>` returns one design task's csv; the page's Delivery
  Space links it.

## 0.12.4 · 2026-10-01 · Targets, not Brief (JL 261001)

- The screen says **targets** where it said "Brief" or "design tasks": the board's Goal Space
  heading is "Targets", its column "target", its form "New targets"; a design built without
  insight reads "from the targets only". The file keeps its name, `0-BR-brief/BR00-brief.md`,
  and the skill stays `haipipe-design-brief` until a separate rename pass.
- New design drawing `servers/workbench-design/studio/design-board-workbench-design.py` (generates
  the `.excalidraw`): four Spaces (Goal · Knowledge · Design · Delivery), one High/Low table per
  target, general design theory (abduction, C-K, FBS, axiomatic design, satisficing) and the
  domain theories for messages. The served screen does not follow the drawing yet.

## 0.12.3 · 2026-09-29 · Each card names the rule it follows

- A Design Item may carry `because: <page id> · <row>` (`because: FW02 · W1`). The card's
  new **Because** row prints that rule's DO / DO NOT sentence, linked to the Insight page.
- No line reads honestly: "AI idea, not from an insight" for `because: none` or a
  `brief-only` item, "no rule named" for an `evidence-informed` item, "no such rule" when
  the row is not on the page. A `challenge` item adds "if it loses, the rule holds".
- The design bundle csv gains a last column, `because`.

## 0.12.2 · 2026-09-28 · No content hashes (JL 260928)

- The Design buttons write run records, decisions and receipts that name files by path
  only: no `sha256` on inputs, no `ticket_sha256` on receipts.
- Run Space and Design Space no longer show a draft's sha256; the design bundle csv
  drops its `sha256` column.
- "Queue again" finds an out-of-date queued run by file time: a file it names is newer
  than its run record. The presenter holds render pictures to the Result's file time.

## 0.12.1 · 2026-09-27

- The Design workbench reads a Design Folder's register, feedback and draft request from `draft/`
  (Page layout 0.118) and falls back to `outline/` on a Folder not yet moved; a new Design Folder
  starts with `draft/`. Design Run tickets `rdNN_<operation>_*` stay in flat `runs/`: the Page
  migration no longer sorts them as Page Delivery Runs. The Design skill docs name `draft/`.

## 0.12.0 · 2026-09-22

- Renamed with the vocabulary: `plugin` now means only a Claude Code plugin
  (`plugins/haipipe-toolkit`), a **lane** is a folder on disk, a **workbench** is
  a served tab and its contract. This skill was `haipipe-plugin-design`; it pairs by name with
  `servers/workbench-design`.
- Moved from the Page family to `skills/design/`, beside `haipipe-design-unit`, the writer of
  the Results this tab renders.
- Absorbed `haipipe-plugin-design-board` 0.7.2 as `ref/design-board.md` (its Space map is
  `ref/design-board-space-mapping.md`): one skill per served workbench, the board grain a ref.

## 0.11.3 — 2026-09-21

- A card no longer carries the strip of Runs (`Commission ✓ JL → Generate ✓ →
  Verify ✓ → next: …`). The card's own line says the state and what is waited
  on; the Runs are Run Space's business. Asked for by JL.
- No control acts on every item at once. The "For all items at once" bar is
  gone from the surface and `perform_action` refuses `release-all`, `queue-all`
  and `adopt-all`: one decision, one item, one sentence on the record.
- A declined item no longer reappears in the Run-type block's per-item table:
  Delivery folds its card away, so the fold is the whole promise.
- A line that waits on a person says "you" and never the reader's name, on the
  item line, in the next-Run guidance and in the board's waiting counter. A
  name there read as the person who signed the last record, which is a
  different fact.

## 0.11.2 — 2026-09-21

- Add Space-specific Run Type guidance with plain purpose, canonical Type,
  actor, owner/worker Skills and prerequisites, separately from matching records.
- Each item explains its next eligible native Run, or current Run/repair wait,
  with its actual Commission, draft and matching record context. Preserve the
  existing Commission and queue controls.
- Add contextual Generate/Verify chat copy beside eligible item controls and
  for compatible queued Runs. Copying only changes the clipboard; prompts
  reread state, reuse Run ids, preserve Commission/reviewer gates, and report
  the actual receipt. Reuse the existing clipboard helper unchanged.
- Label native live starts and read-only views explicitly; retain Run Space
  history and read-only Delivery. Static item cards now omit mutation controls.
- Show canonical Type and target beside actual Run names. No shared helpers,
  styles, central catalog, gate rules or dispatch implementation changed.
- Tests were not added or run for this follow-up, as requested.

## 0.11.1 — 2026-09-20

- Align current docs with Commission → Generate → independent Verify and ready
  Delivery. Runs are recorded work; Delivery is a projection and internal Steps
  do not add Run identities. Historical Adopt rows keep their original ids.
- Distinguish a human `commission held` decision from a `blocked` worker Run;
  show the blocked Run and repair owner without Commission controls.
- Read optional hash-bound render evidence from the candidate's own Result.
  Existing Delivery manifests remain a fallback only when no Result manifest
  exists; an invalid current manifest never falls back to an older picture.
- Clarify held/released Commission counts, valid completed-review retry limits,
  and the allowed operation-specific fields derived from released config.
- Revalidate the exact Generate and independent Verify Results before Delivery.
  Changed artifacts, checks, config or render pins display `records invalid`
  and are excluded from ready totals and CSV exports.

## 0.11.0 — 2026-09-18

- Delivery handoff now follows a passed independent Verify directly. The live
  surface no longer creates or shows an Adopt action, state, counter, or batch
  button; Goal and Board count `ready` items, and Delivery lists only ready
  candidates. Historical `rdNN_adopt_*` bytes remain readable as legacy
  records but are never created by the current writer.

- A legacy folder parked under the board's `_archive/` no longer holds its
  old links at 410: the file it names is gone, so the link heals to the
  `Design-NN` folder that replaced it (B00's DS01 link now opens Design-01).

- The card rewrite (JL 260918). Each item is one fixed-height row (46px):
  id, title, the design in one line (a screen previews its goal), state, and
  who is waited on; on a phone the preview hides. A row opens into a
  fixed-height card (560px) that scrolls inside; `open all · close all` sits
  above the list. The design sits on the left and stays in view while the
  explanation scrolls; the decision form and buttons sit under the design, so
  they are never below the fold. The explanation is a bordered two-column
  table: Why this design, From insight to design, The bet, Rules, Steps.
- From insight to design is a flow of the item's pages by level, Data →
  Information → Knowledge → Wisdom → This design, with an Also read level for
  a source that is not an insight page and `· avoid` on a page the register
  avoids. Each insight page shows as its label and title (`full-D02`, never
  the file id `FD02`), linked to the Insight view only when the page is under
  the server root. The one-line insight pointer of 0.8.0 is gone.
- Rules are marked by the Verify of the draft the card shows, else by that
  draft's self-check, else "not checked yet"; a hand-written config shows its
  own criteria in words. The card warns when the register changed after
  release. Steps mark a run that failed the records check with `✗` and skip
  superseded runs.
- A card shows the adopted draft, else the latest draft that passed the
  records check; a failed draft is never shown, in Design Space, Delivery
  Space, or the csv.
- Waiting on "agent" only while a run is queued or running; otherwise the
  person, with the step (queue the draft, queue the review, queue again, …).
  New states `commission open`, `adoption open`, and `queued run out of date`
  (a queued run whose pinned file changed), with the button "Queue again with
  today's insight files": the old run becomes `superseded` with its reason.
- Every state that waits on a click shows its button (a held Commission gets
  its Release form back, a held Adopt its Adopt form, `verify invalid` its
  Queue Verify); the page refuses any other action, naming the state and who
  is waited on. One Commission per item. A draft that passed its review is
  revised only through a person's Revise decision.
- Generate and Verify copy the released Commission's config and evidence, so
  a later register edit never reaches this item's drafts. The config's `goal`
  is the goal sentence.
- Rule compiling: not, does not, doesn't, don't count as negative; `ends
  with 'X'` and `starts with 'X'` are their own checks; "under N characters"
  allows N − 1; every quoted phrase of a rule is compiled; apostrophes inside
  words are never quotes.
- Routing: a draft that fails the records check goes back to Generate, a
  review that fails it goes back to Verify, a fail verdict goes to a revise.
- Run Space: a revise reads `Generate · revise of rdNN` with its feedback;
  checks name their rule in words; a fail verdict is red with its checks
  open; a superseded run is grey with its reason.
- Insight Space: pages by label and title; "what it says" never shows an
  opening question; "Available, unused: none …" when every signed insight is
  used; `?item=` says "showing ITEM02 only · show every item".
- `?item=` opens and marks the card and scrolls to it; every item button lands
  back on Design Space at the item.
- The Adopt preview is one copy per draft, versioned per item, with the
  draft's own suffix, for all four decisions.
- Short links: an ambiguous `?folder=` answers with a page listing each board
  that holds it (404), never a guess; `Design-1` reads as `Design-01`.
- Legacy `2-DS-design/DS*` folders are refused with 410; an old DS link is
  rewritten only when the file it names is gone.
- The New Design Item form uses plain labels (approach, built on, expected,
  wrong if, insights, rules); stance `generate` reads "a new design".
- Docs: the register and card examples judge design quality (no arm, winner,
  or re-fielding); the contract word no longer follows a plain word in
  parentheses; the demo rebuild refuses without `--force`.

## 0.10.0 — 2026-09-18

- Screens read as pictures (JL: "design the UI for the whole population"):
  `delivery/render/manifest.json` names the rendered picture of a draft;
  the Design Space card shows it beside the facts (`the HTML behind this
  screen` folds the source), and Delivery Space shows every screen as a
  gallery. `_render_for` matches the picture to the exact draft shown.
- `compile_criteria`: a rule "judged on the render" is a `visual` check.
- A declined item is retired from the Delivery overview and folded under
  `Declined, kept for the record · N` (Page and Board level).
- First real use: `B01_DesignBoard-AuthenUI-260917`, six screens for all
  patients, measured at 390 x 844 in headless Chrome.

## 0.9.5 — 2026-09-17

- An old link is only rewritten to a current folder name when that folder
  exists. A legacy folder (`2-DS-design/DS01-…`, `design/DU*`) is now read as
  given and served 410 with "legacy design/DU* storage is not a current
  Design Folder", instead of a bare 404 from the rewritten path.

## 0.9.4 — 2026-09-17

- Titles read as one plain phrase (JL: "the name here is not good"):
  `design_title(row)` gives `<job> <venue> for <who>`, e.g. `Prescription
  review SMS for all patients`; Goal Space says `10 prescription review SMS
  designs for all patients`. The demo Brief's audience became `all patients`,
  so the folder is `Design-01-all-patients-prescription-review-sms`.

## 0.9.3 — 2026-09-17

- Delivery Space is a quick overview of what we designed (JL: "it is not
  about what to adopt"): one table, one row per item, item (id · title) and
  the design text. The Adopted / Not adopted yet groups, hashes, verifier,
  preview, and adopt words left the Space; they remain in Design Space and
  Run Space. `shown_design(item)` picks the adopted draft, else the latest.

## 0.9.2 — 2026-09-17

- Delivery Space lists every item (JL): **Adopted** cards first, then **Not
  adopted yet** cards with the latest draft text, state, waiting on, and a
  link to decide in Design Space; they say "not adopted, so not delivered".
- Folder names say the goal: the first three content words of the Brief's
  audience, job, and venue, filler dropped. The demo folders became
  `Design-01-all-patients-prescription-review-sms` and
  `Design-02-patients-refill-due-refill-review-ui-card`, titled from their
  Brief line. `renamed_folder` sends an old link or `?folder=` to the folder
  with the same `Design-NN` number.

## 0.9.1 — 2026-09-17

- Decision forms are folded by default (JL): each item's name + words +
  buttons sit under one line (`Adopt, decline, revise, or hold`, `Release or
  hold the commission`, `Queue a revise, with feedback`), open for the item
  selected with `?item=`. The batch bar folds the same way (`For all items at
  once: …`). A single agent-queue button stays in view.

## 0.9.0 — 2026-09-17

- Batch buttons above the cards: Release all · Queue all · Adopt all
  verified, each shown only when it has work; one name and sentence for the
  batch, one decision Run per item.
- Goal Space: "Ask the agent to draft the missing N" writes a draft request
  (goal, insights with FINDING / CONSEQUENCE / DO / DO NOT, count); the open
  request is shown until the register is filled.
- Insight Space lists the rules each insight implies (its DO / DO NOT lines);
  `counsel_rules` turns every DO NOT into an acceptance rule.
- `mode` left the card; `cli/design_queue.py` lists and runs the agent queue
  from a terminal (`claude -p`), closing each run with the records check.
- Old `2-DS-design/DS01-…` links redirect to the full-name folders.
- `release_worker`: a dead worker's run goes back to planned with the lost
  worker named on the receipt; the runner stops on the first dead worker.

## 0.8.1 — 2026-09-16

- Full names: Design Folders live at `2-Design/Design-NN-<audience>-<job>-<venue>/`
  (never `DS`). Goal Space reads an optional `insight` column on the Brief
  line, the Insight board that task draws from; empty means the board's
  `reads:`. A named board that is not found shows in red.

## 0.8.0 — 2026-09-16

- Five Spaces in time order (JL): `Goal Space` (the Brief line that names
  the folder: venue · who · their job · how many designs wanted/registered/
  adopted · the Insight board), `Design Space` (the cards), `Insight Space`
  (per item, the supporting insights: signed by whom, what they say from the
  handoff's FINDING/CONSEQUENCE, pinned or not, "needs an insight", and the
  board's signed pages no item uses), `Run Space`, `Delivery Space`.
- Plain words on the surface: the Brief and its lines (never roster), signed
  insight (never handoff), run record (never Ticket), draft (never
  candidate), records check (never check_unit). The card's long evidence row
  became a one-line `insight` pointer.
- The Brief table gained a `designs` column (how many the line asks for).

## 0.7.0 — 2026-09-16

- Plain words (JL): the first Space is `Design Space` (query `space=design`;
  `intent` still resolves), Design Item ids are `ITEM01…` (DI read as
  Data→Information next to the Insight workbench), and the register field
  `intent:` is `goal:`. Run slugs follow (`rd02_generate_item01`).
- Header cut to one line, `Page level · <folder>` with a link up to the Board
  level; the source, register, signal, and waiting lines are gone. A red line
  appears only for a legacy folder or an unsigned handoff.
- Card rows: `goal` (the sentence), `why` in plain words (follows the
  evidence · built on evidence · written fresh, contract words in
  parentheses), `evidence`, `predict`, `rules`, `runs`.

## 0.6.0 — 2026-09-16

- Made the Design Item the row of the tab: a register at
  `outline/<stem>-design-items.md` (intent only) and `item:` on every Ticket;
  state is derived by folding the item's Runs, with an explicit "waiting on"
  (agent or the named person) beside it.
- Reduced the surface to three Spaces: Intent (register), Run (per-item
  timeline with who/when/outcome/next, folded checks and candidate text,
  live `check_unit` audit), Delivery (one card per adopted item pinned to the
  exact candidate hash and the adopter's words). Signal moved to a header line.
- The presenter now reads the v2 contract files (`runtime.yaml`,
  `checks.yaml`, `result.yaml` artifacts, `decision.yaml`, config
  `design_intent`/`criteria`) instead of guessing from file names; removed the
  `adopt|accept` filename heuristic, the counters, the static Flow Table, and
  the Anchor/Shape/Trial/Commit vocabulary.
- Design Space became one card per item that shows the design text, the bet
  (intent · stance · basis · mode), the evidence rows with signature and
  Ticket pin, the prediction (expected · falsified if), the acceptance rules,
  and the Runs; the register grew `stance`, `basis`, `mode`, `expected`,
  `falsified`, and `evidence` lines.
- Added the actions: `POST /_board/design-act` (`servers/workbench-design/design_actions.py`)
  writes Commission release/hold and Adopt adopt/decline/revise/hold as the
  person's decision Runs, queues planned Generate/Verify/revise Tickets for
  the agent, and appends a new item to the register; the button an item shows
  is the one its state licenses.
- Added `design_actions.complete_run`: the caller-side close of a worker Run
  that gates the returned Result with `check_unit` and writes the receipt
  truthfully (`complete` + next route, or `failed` with the gate's words);
  a review that fails the gate shows as `verify invalid · agent · verify`.
  `queue_verify` now carries the item's evidence inputs, so an
  evidence-informed Verify Ticket passes the gate.
- Added `tests/fixture_design_v2.py`, which builds contract-valid Design
  Folders (and the one-page InsightBoard they read) for the tests and
  regenerates the demo boards.

## 0.5.1 — 2026-09-16

- Reworked the Design presenter to use the Outline workbench's shared reader
  presentation: compact Space tabs, quiet page chrome, lightweight cards, and
  source-first tables.
- Kept Design's own four Space meanings and transformation Flow unchanged.

## 0.5.0 — 2026-09-16

- Made the designed artifact directly inspectable in Run Space → Shape and
  Delivery Space instead of exposing only file paths.
- Kept candidate display, verification receipt, source artifact, and commit
  status visibly separate.

## 0.4.0 — 2026-09-16

- Restored fixed `Run Space` and `Delivery Space` names required by the Page
  workbench vocabulary.
- Renamed the two Design-specific spaces to `Design Space` and `Signal Space`.
- Kept the Design-native `Anchor → Signal → Shape → Trial → Commit` Flow Table
  inside Run Space.

## 0.3.0 — 2026-09-16

- Replaced the borrowed Draft/Evidence/Run/Delivery vocabulary with the
  Design-native Frame, Signal, Shape, and Launch spaces.
- Replaced the Space matrix with a transformation-oriented Design Flow
  Table: Anchor → Signal → Shape → Trial → Commit.
- Added a distinct console visual language and kept old `space`/`run` query
  values as compatibility aliases while new links use `space`/`flow`.

## 0.2.0 — 2026-09-16

- Reframed the Page-level surface as Draft Space, Evidence Space, Run Space,
  and Delivery Workspace, matching the Page workflow presentation pattern.
- Added a read-only Run Space Workflow map with Design Run Specs as rows and
  the four Spaces as columns.
- Connected Evidence Space to the owning DesignBoard `reads:` allowlist and
  person-signed InsightBoard Wisdom Handoffs; unsigned or undeclared sources
  remain blocked.

## 0.1.0 — 2026-09-16

- Added the first page-folder-level Design category workbench contract.
- Defined Plan, Create, Review, Run, and Delivery as internal read-only workspaces.
- Kept Design Folder, Run, Result, adoption, and Page CHECK authority with their owning contracts.

---

# Board grain · history of the folded design-board skill (was `haipipe-workbench-design/ref/design-board.md`, last 0.7.2)

## 0.7.2 — 2026-09-21

- Show the Design Run Type guide in each applicable Space, separate from
  actual matching Run/status records and the full history ledger.
- Item rows explain the next Run/actor, purpose, owner/worker Skills and
  prerequisites, using the owning folder's context. Link to native item
  controls; Board actions do not allocate Design Runs.
- Offer contextual Generate/Verify chat copy for eligible items and compatible
  queued Runs, using their own Folder/Page context and the Page prompt builder.
  Copying only changes the clipboard; prompts preserve native owner/gate rules,
  reuse queued identities and report actual receipts. Static views and unsafe
  or nonactionable states have no prompt; the shared clipboard helper is unchanged.
- Preserve the existing task/folder writes and read-only Delivery. Actual Run
  rows additionally name their canonical Type and bounded target.
- Tests were not added or run for this follow-up, as requested.

## 0.7.1 — 2026-09-20

- Align current guidance with Verify-passed `ready` items and Delivery as a
  projection; CSV exports only eligible ready drafts. Commission, Generate,
  and Verify are the workflow's Run types.
- Revalidate the exact reviewed candidate and its independent Verify before
  projecting Delivery. Changed artifacts, checks, results, frozen config, or
  render evidence make the records invalid and remove the item from ready/CSV.
- Preserve historical `rdNN_adopt_*` IDs in text, links, and tooltips; label
  their recorded type `Adopt (historical)` and distinguish queue actions.
- Document `new-folder.row` as the parsed Brief row key (`R3`, for example),
  separate from the human-readable task title and an integer row position.
- Fresh-context validation found sparse Boards could omit the promised
  presentation entry. `new-folder` now creates `## Pages` when missing and
  preserves existing groups/sections; repeat requests still create no duplicate.

  Ready/Delivery and historical-ID runtime changes were coordinated with
  the Design family repair; this patch aligns the Board workbench contract.

## 0.7.0 — 2026-09-18

- A retired record parks under the board's `_archive/` instead of being
  migrated or deleted: the checker judges no `_` folder, so `2-DS-design/DS*`
  keeps its bytes for the Log to cite while the board claims only its live
  design tasks (B00's DS01, JL 260918).

- Tasks show by their full name, `<job> <venue> for <who>`; the Brief's row
  id (`R1`) is a key in the file and never a name on screen, refusals
  included (JL 260918).
- The task list is the first Brief table whose header names `audience`,
  `job` and `venue` together, so an audience table elsewhere is never read as
  the list. A Brief with no `line` column numbers its rows R1, R2 … in order,
  and `new-folder` writes the folder cell on that same row, so a second click
  is refused instead of opening a duplicate folder.
- `new-folder` writes a page that passes the board checker: `state: 🔴 OPEN ·
  no design registered yet`, `owner:` (the board's, else the Brief's), an
  Opening question, and an entry in board.md `## Pages` under its Design
  heading.
- The csv gains a `state` column and lists the adopted draft, else the
  latest draft that passed the records check; a failed draft is never listed.
  The send system takes the rows whose state is `adopted`; declined rows stay
  in with state `declined`.
- Insight Space groups "used by" per folder (`Design-01 · 6 items`, linked to
  that folder's Insight Space), adds a table of the other pages the designs
  use (not signed insights), and shows a red line when no design rests on a
  signed insight. The Insight board picker offers only boards that resolve,
  by folder name. Design Space shows each item's design text under its title.
- The header is one line; a bare `/_board/design-board` with several boards
  answers 200 with the list; an ambiguous Page-level `?folder=` answers 404
  with a page listing each board that holds it, never a guess.
- The board checker knows `board-kind: design-board` and `insight-board`,
  accepts a `reads:` entry that is a `../` path staying inside the checkout,
  and audits folders holding only Commission and Adopt runs.
- Docs: the board-kind and board-name rules, the csv columns, the gallery and
  the declined fold are now in the SKILL body; the examples match the demo
  (10 wanted · 10 registered · 1 adopted).

## 0.6.0 — 2026-09-18

- Delivery Space shows a folder of screens as a picture gallery (the Page
  level's rendered pictures); text designs keep the table. The csv gains a
  `render` column naming each screen's picture.
- A Project folder can be the server root: boards under its `applications/`
  are found, and `reads:` may name an Insight board in another Project by a
  path relative to the board's parent (first use: `Project-Application-
  AuthenUIDesign` reading `Project-Application-SMSDesign`'s A00).

## 0.5.3 — 2026-09-17

- New Design Folders are titled `<job> <venue> for <who>` (`design_title`),
  the same plain phrase the Page level shows.

## 0.5.2 — 2026-09-17

- Delivery Space is a quick list of every design, one table per folder:
  item (id · title) and the design text; no adoption status. The csv
  download became **Download all designs**, one row per design.

## 0.5.1 — 2026-09-17

- Delivery Space lists every design: **Adopted** cards, then **Not adopted
  yet** cards with the latest draft text, state, and waiting-on.
- New folders are named from the first three content words of each Brief
  cell, filler dropped (`Design-03-young-male-age-prescription-review-sms`).

## 0.5.0 — 2026-09-17

- Delivery Space: **Download the bundle**, `GET /_board/design-bundle`, one
  csv row per adopted draft with its Brief line, text, hash, verifier, and
  adopter.
- Insight Space shows the DO / DO NOT rules each signed page implies.

## 0.4.0 — 2026-09-16

- Five Spaces at board grain, Goal · Design · Insight · Run · Delivery. Goal
  Space is the list of design tasks from the Brief (who · their job · venue ·
  how many wanted/registered/adopted · insight board · folder · status) with
  the **New design tasks** form: subgroups one per line, their job, venue,
  how many each, which Insight board, open folders now. Insight Space lists
  every signed page the programme draws on and which folder · item uses it.
- Second write `add-tasks`: one Brief line per subgroup (adds the `designs`,
  `insight`, `folder` columns or the whole section when missing), then a
  Design Folder per line. Refusals write nothing.
- Full names (JL): the group is `2-Design/`, folders are `Design-NN-…`;
  `DS` is gone from disk, code, tests, and docs.

## 0.3.0 — 2026-09-16

- Plain words: "From the Brief" with `line · who · their job · venue · wanted ·
  folder · status` (never roster); signed insights; draft; records check.
  Snapshot keys `brief_rows` / `unlisted`; `new_folder` returns
  `brief_updated`. The Page level now has Goal and Insight Spaces; the Board
  keeps Design · Run · Delivery at board grain.

## 0.2.0 — 2026-09-16

- Follows the Page level's plain words: `Design Space` (query `space=design`),
  `ITEM01…` ids, register field `goal:`. The Brief's spine left the header.

## 0.1.0 — 2026-09-16

- First Board-level grain of the Design workbench (`servers/workbench-design/designboard.py`,
  route `/_board/design-board`, static `board/design.html`): the Brief's
  roster against the folders on disk, every Design Item across folders with
  its state and waiting-on, the cross-folder queue (person first), every Run
  newest first, every adopted version, and the Design Unit gate result across
  folders. Same three Space names as the Page level, one grain up; every row
  links down to the Page-level card.
- One write: `new-folder` opens a Design Folder for a roster row that has
  none and names it on that row.
