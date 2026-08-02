# haipipe-board-page · v0.10.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page` defines the reusable working record: Q, S, and Skill page kinds; the fixed on-stage sections; and the safe, anchored places a machine may write. It is why a Paper stage can live in the same Markdown object a reader opens and comments on.

It stops at page mechanics. This Paper Board adds the semantic overlay: `QC3` says which Paper contracts own regions of a stage page, and `QC5` says what Paper sections, paragraphs, sentences, and evidence must accomplish. The shared page shape must not be mistaken for a manuscript template.

## Diagram
<!-- haipipe:skill:tree:start 372a94b2e00ec17f board/haipipe-board-page -->

```
haipipe-board-page/
  CHANGELOG.md         151 ln  haipipe-board-page · Changelog
  SKILL.md             295 ln  /haipipe-board-page · the page, as a contract you can load
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 372a94b2e00ec17f board/haipipe-board-page -->

**haipipe-board-page** · `0.10.0` · last shipped 2026-08-02

- folder   `board/haipipe-board-page/`
- tools    not declared
- summary  Two verbs, create and working-on, drive one page end to end; the skill owns the contract and calls haipipe-board's engine rather than containing it.

### SKILL.md




`haipipe-board` is the door you walk through to RUN a board.
This skill is the door for ONE PAGE, and the spec that page is measured against. Say `create a new page on <topic>` or `working on <page>` and it runs; load it with no board open and it is a pure contract.
QC1b §1 on the design board states the test it passes: a consumer needs these rules with no board open, and the consumers exist: the routing verb deciding "which page, which section", the chat drawer priming a per-page session, and the variant authors in other families.

**The boundary, and it is a hard one:**

**Who owns what**: this skill holds the spec, `haipipe-board` holds the machinery.

```
haipipe-board-page               haipipe-board
─────────────────────            ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (serve.py)
where a write may land           the checker (check.py)
the base/variant model           the template file itself (ref/page-template.md)
```

This skill never CONTAINS the renderer, the server or the checker. It calls them, because a reader asking for one page should not have to know which script does what, and owning one page end to end is not the same as owning the machinery.
The authoritative template stays `haipipe-board/ref/page-template.md`; this contract cites it and must never fork it.


- 1 · 🧬 Three page kinds, one base
      A page's KIND comes from its filename, and the kind decides how the page closes, what its Content holds, and which typed records it fills through the base frame's declared extension points.
      Everything else is the shared base (the model on the design board's QB4, JL 260729).
      **Three kinds, one base**: the filename decides the kind, and the kind decides how the page closes.
      ```
      kind          filename                     closes when
      ─────────────────────────────────────────────────────────────────
      Q  decision   Q<group><n>[<face>]-<slug>   every Aim is met or explicitly held
      S  stage      S-<Family>-<unit>-<slug>     its human gate passes
      Skill mirror  Skill-<unit>-<slug>          the unit ships · NEVER counted
      ```
      A page kind used by one consumer family is a VARIANT of the base: it defines Content and may populate fixed extension points in Aims, States, and Stage Contract, but it never redefines, adds, removes, or reorders those frame sections.
      The variant ships under its consumer (`haipipe-paper-stage` is the first), never here.
      This skill owns the BASE those variants extend.

- 2 · 📑 The seven sections, in their fixed on-stage order
      **The seven sections in order**: what each owes a reader, and how much a machine may write into it.
      ```
      #   section            owes the reader                      a machine may write
      ──────────────────────────────────────────────────────────────────────────────────
      1   Opening            the lead question + why it matters   nothing
      2   Diagram            the figure; ids in it are links      nothing without the human
      3   Content            the substance, ### divisions         nothing without the human
      4   Aims               durable Content-linked targets       revise only when intent changes
      5   States             one factual current State per Aim    update with evidence; a decision is closed only once answered
      6   Files              the action map, grouped by ACTION     append a row
      7   folds              Discussion · Law · Lesson · Glossary · Log  append a Log or > lane line
      ```
      Each section answers ONE reader question, and the same five rows define every section's contract (JL 260801, ruled on the design board's QB4 §0): **conveys**, the reader question it answers · **holds**, the elements it must contain · **source**, how the author writes it · **rules**, what binds a write · **omit**, when it may be absent.
      **One reader question per section**: the question it answers, and when it may be left out.
      ```
      section            conveys · the reader question                omit
      ──────────────────────────────────────────────────────────────────────
      🧭 Opening          what is this page, why should I care?        never
      🖼 Diagram          can I see the whole subject at once?         when no figure helps: delete
      📚 Content          what does this page actually establish?      Q may · S never
      🎯 Aims             what should become true, and for which Content division? never
      📍 States           what is true now for each Aim, what waits?   never
      📎 Files            which few files continue this work?          allowed, advised against
      🗃 folds            what was ruled, learned, changed, if needed  each optional
      ```
      A sentence answering another section's question is MISPLACED, and the protocol names its home: substance found in Opening moves to Content, Required Inputs and Venue move to Stage Contract, prose rules move to Writing Style, intended outcomes move to Aims, current facts move to States, and temporary next steps become an Aim's optional Plan.
      The full five rows per section live in the design board's `QB4` Content divisions; the authoritative source form stays `haipipe-board/ref/page-template.md`.
      An Aims or States group is `### A<n> · <emoji> <name>`, taking the NUMBER, NAME and EMOJI of the Content part it answers, so the three sections line up by eye as well as by id (JL 260802; it was `C<n>` until then, which made a reader translate one letter to see that `A3.1` belonged under it, and `C<n>` still resolves). `P` is for a target belonging to no single part. Files groups are a MENU of actions, taken as they apply: ⚙️ Engines what RUNS the subject · 📋 Contracts what CARRIES a rule to other pages · 🧪 Checks what CATCHES a page breaking one · 📥 Input files what the work READS · 📤 Output files what a BUILD writes. A group name states an ACTION, never a subject, because a subject-named group rots the moment its subject leaves the page.
      An Aim is not a task. Write `- A3.1 · target` for a result owned by Content part 3, under the group `### A3`, and `P1` only for a target that genuinely crosses parts. One division may have zero, one, or many Aims. Each Aim has a testable `Done when` and may carry a temporary `Plan`; changing Plan does not change the Aim.
      The section labels are deliberately both plural: `Aims` contains Aim records and `States` contains their State records. States mirrors every Aim id exactly once: `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person or something outside this page, `✅` met with the evidence named, or `❄️` on ice, held on purpose. Each says its meaning by SHAPE (JL 260802); the old `🟡` `🟠` `⏸️` still parse. This is the AIM vocabulary and NOT the page `state:` line, which keeps its own ✅ 🟡 🔴 ⏸️ set and is checked apart. The section is a snapshot, so the reason for a transition belongs in Log. The strict one-to-one relationship is Aim to current State row, never Content division to Aim.

- 3 · 🚪 Two verbs, and this skill is the door for both
      Say either of these and this skill runs it. You never call the engine yourself.
      ```
      📄 CREATE     /haipipe-board-page create a new page on <topic>   [on <board>]
      🔧 WORK ON    /haipipe-board-page working on <page>              or just the path
      ```
      `haipipe-board` owns the machinery and this skill owns the contract, which is why the boundary above says this skill never renders, serves or checks: it does not CONTAIN that code. It does CALL it. A page is one unit of work, and a reader asking for one page should not have to know which script does what.

- 3.1 · 📄 create a new page on a topic
      1. Resolve the board folder, and the group the page belongs to. Ask ONLY if the group is genuinely ambiguous.
      2. Pick the id (`Q<group><n>-<slug>`, or `S-<Family>-<unit>-<slug>` for a lifecycle stage) and copy `haipipe-board/ref/page-template.md` to it. Never retype the shape from memory: the template's guide sentences ARE the contract.
      3. Write the title so it states the page's PURPOSE, in sentence case.
      4. Write the Opening: the visible paragraph above the first blank line, everything else below it.
      5. Write Content as numbered parts, each opening with a caption, a `/diagram-ascii` figure and a short intro.
      6. Write Aims, their States, and Files.
      7. Register the page in the board's `board.md` roster.
      8. Build, check, and read the RENDER. Report the page's finding count, not the fact that you finished.

- 3.2 · 🔧 working on an existing page
      Scope is the one thing this verb got wrong when it was measured. On 260802 three fresh agents were each given one sentence and nothing else, and all three found this skill unaided and drove their page to zero findings. They then disagreed completely about how far to reach: one wrote to a single file, its own page; another wrote to fifteen, including four shipped `SKILL.md` files, four `CHANGELOG.md` files, six sibling pages and the shared `board.md`. Neither was wrong on the merits, and the wide one was fixing citations a renumbering really had broken. The skill simply never said where to stop, so steps 7 and 8 below now do.
      1. Read the whole target file first, including Content, Aims, States, Files and the settled folds.
      2. Run the checker on it and work its list. Every finding names the rule it breaks and the part it is in, so nothing has to be read to know what to do.
      3. Fix the MECHANICAL findings first, in bulk: dead `## Files` paths, a part with no figure, a figure with no caption, a group name that drifted. None needs judgment.
      4. Then read for what no checker reaches: the weak-English axis, whether each part still answers one question, whether the Opening's visible paragraph says anything the title did not.
      5. If a fix reveals a rule nobody wrote down, write it in three places: the owning page, `haipipe-board/ref/page-template.md`, and this file. A repair that stops at one page will be needed again next week.
      6. Build, check, read the render, and report the before and after counts.
      7. ONE page is the deliverable. Step 5 sends you to other files on purpose, and this step bounds it: a write outside the target page is allowed only when the page CANNOT be made correct without it, and every such write is named in the report, with the reason, file by file.
      8. Never rewrite a sibling page's content. Repointing a citation your own renumbering broke is repair; rewriting the page that citation lands in is a second job, and it belongs to that page's own turn.
      The engine both verbs call, so nobody has to remember it:
      ```bash
      python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
      python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE>'
      python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
      ```
      `watch.py` rebuilds on any `.md` save, so step "build" is usually already done; a change to `.py`, `.css` or `.js` is not watched and needs the build run once.

- 4 · ✍️ What both verbs are writing to
      Load this skill and `haipipe-board/ref/writing-rules.md` directly before writing.
      Do not copy their requirements into an assignment prompt: a copied checklist becomes a second prose authority and drifts.
      For an existing page, read the entire target file before changing any section, including Content, Aims, States, Files, and settled folds.
      A CHANGE IS FINISHED WHEN IT IS ON THE RENDERED PAGE, and nobody is asked for permission on the way (JL 260801: "don't wait me to say go next time, just go ahead and don't stop until the content is updated in the Page"). The unit of work is a visible page, not an edit. Carry every change all the way through: write the source, propagate the rule to `haipipe-board/ref/page-template.md` and to this file so a new page inherits it, run `check.py`, then confirm the RENDER rather than the markdown. Stopping mid-way to ask for a go leaves the change half-applied, which is strictly worse than either finishing or not starting: a renamed label with a dozen sentences still naming the old one, or a rule written on one page and in no template. Verify on the artifact a reader opens, because source-is-correct is not page-is-correct: a dead watcher and a shut `<details>` each produced a correct file and a wrong page.
      The page's own source is what keeps a rewritten Opening from promising something the rest of the page does not establish.
      The title is a phrase in SENTENCE CASE that says what the page is FOR (JL 260801, ruled on the design board's QB4 §8). Capitalize the first word and proper nouns and nothing else; a defined term keeps its capitals. A colon may carry a short subtitle, and that is usually where the purpose lands: `The page template: one grammar every page kind obeys` rather than `Page Template design`, which mixes two cases and names only a topic. On the Index the title is the only line a reader gets before choosing, so a title naming its subject alone makes them open the page to learn what the page was for. Sentence case is a string test a checker can own; whether the title states a purpose is a judgment and belongs to the Evaluation contract below.
      An Opening keeps one fixed physical shape: one real question paragraph, then one plain rationale paragraph.
      THE FIRST BLANK LINE IN `## Opening` IS THE SPLIT (JL 260801, ruled on QB4 §1). Above it is the ONE paragraph a reader sees without clicking, joined into a single block; below it is the `More details` drawer, behind a click. Nothing reports a blank line in the wrong place, so the failure mode is a page whose Opening renders as one bare question while its explanation sits unread. The visible paragraph is 4-5 sentences, about five lines on screen, under ~450 characters, measured on the RENDER. Write it in PLAIN ENGLISH for a reader whose English is weak: a shorter common word always beats a precise rare one. Its shape is the question, what the question's own words mean, why that is hard, what this page decides. NEVER open with a list that will grow: name examples and say the set grows, so a fourth member never forces an edit; the roster lives in the Content division that owns it.
      EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT (JL 260801, ruled on QB4 §2). Write `**Name**: what this diagram shows.` directly above the fence, one line only. A section may hold several figures, and an unlabelled one makes the reader decode it before learning what it is; the caption goes ABOVE because an explanation that arrives after the figure arrives too late.
      CONTENT IS NUMBERED ALL THE WAY DOWN (JL 260801, ruled on QB4 §1). A division is `### 3 · Content`, a group inside it is `**3.2 · Group title**`, and a paragraph is `#### 3.2.1 · Its heading`; an ungrouped division numbers its paragraphs `#### 3.1 ·` straight through, so the depth of the number says whether a group exists. This is the same rule the board applies one level up with `§6` against `§6.1`. Numbering is also a defect detector: it exposes a group holding exactly one paragraph, which is the floating-group-title defect, and it gives every paragraph a name a person can say in chat.
      `More details` IS A LIST OF LABELLED PARTS, NEVER ONE BLOCK OF PROSE (JL 260801, ruled on QB4 §1). Each part starts with a bold label saying what it answers, then its sentences, with a blank line between parts. The two halves of an Opening have two different readers: the paragraph on stage is read straight through by someone deciding whether to stay, while `More details` is opened by someone who already decided and is hunting one specific thing, so they scan for a label instead of reading from the top.
      A FIGURE ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE (JL 260801, ruled on QB4 §2). If a row could end in a period it is prose, and it belongs in the paragraph under the figure rather than inside the fence. A figure earns its fence by being scannable; a wall of clauses in a box is slower to read than the same clauses outside it.
      The rationale's FIRST job is to define the words the question itself uses (JL 260801, ruled on QB4 §1). A sharp lead question is specific, and being specific usually means naming this board's own things, so the sharper the question the more it leans on vocabulary a cold reader does not have. Give each such term one line with a REAL EXAMPLE, never a restatement: `a lifecycle-stage page carries one stage of a paper being written, such as its Results section` lands where `a lifecycle-stage page represents a stage` does not. A restatement passes the author's own eye as an explanation, because the author already knows what the word means. Only then place the page on the board (the bearing rule), and only then argue the stake: a reader who cannot parse the question cannot be told where the page sits or why it matters. Names chosen in the question bind the rest of the page and must be used identically in Content and Law.
      The rationale has no required sentence count and no required rhetorical order.
      Use as many short sentences as the page needs, then stop when a cold reader can say what the page asks, why that question deserves attention, and what this page owns.
      Difficulty, failure, downstream effect, and a success consequence are diagnostic prompts for missing stakes, not four slots to fill and not one sentence each.
      Speak about the subject whenever possible.
      `This page defines ...`, `The hard part is ...`, and `It succeeds when ...` are not forbidden phrases, but a writer may not use them as a reusable scaffold.
      If the paragraph still fits another page after its nouns are replaced, it is generic and must be rewritten.
      Move frameworks, implementation history, evidence inventories, current status, and plans to their owning sections instead of using them to pad the Opening.
      Before writing back, run a local self-check:
      1. Compare the question and rationale with the whole target page; remove any promise the page does not support.
      2. Remove any sentence whose only job is filling a category such as difficulty, downstream, or success.
      3. Apply the noun-substitution test; wording that could introduce a sibling page is not page-specific enough.
      4. Preserve one sentence per source line, English only, and the no-em-dash rule.
      This self-check improves the draft but never approves it.
      A fresh reviewer judges the page after the writer's context is gone.

- 5 · ✅ Evaluation contract
      Evaluation asks whether the authored page satisfies its declared requirements; it does not ask whether the reviewer personally likes the format.
      The requirements stay here, in the page spec and its cited template, rather than being copied into a second evaluation skill.
      The evaluator is a consumer of this contract.
      Resolve applicable requirements in this order:
      1. The base section contract in this skill and `ref/page-template.md`.
      2. The page kind or consumer variant, when one exists.
      3. The page's own `## Writing Style`; on S pages, also its `## Stage Contract`.
      4. The local `###` division purpose and each `####` heading's immediately following `(job line)`, when present.
      A more specific source may refine a broader one but may not silently contradict it.
      When two sources disagree, report a requirement conflict and stop judging that criterion until the owner resolves it.
      Review four distinct axes:
      | Axis | Question | Judge |
      |---|---|---|
      | Mechanics | Is the required structure present, ordered, addressable, and internally consistent? | `check.py` |
      | Function | Does this section answer the reader question the contract assigns to it? | semantic reviewer |
      | Evidence | Can every factual compliance claim point to visible text, a State row, or a linked artifact? | semantic reviewer |
      | Readability | Can a zero-background reader understand the section without supplying a missing premise? | fresh-context reviewer |
      The review units are every present `##` section, every direct `###` Content division, and every `####` paragraph whose local job must be tested.
      Use exactly four verdicts: `MEETS`, `NEEDS WORK`, `N/A`, and `NOT VERIFIABLE`.
      `N/A` means a rule genuinely does not apply; `NOT VERIFIABLE` means the required evidence is unavailable and is never a pass.
      When the same section changes on several pages, the batch is an additional readability unit.
      Read those sections consecutively in Board order after judging them page by page.
      A sentence can be clear alone and still fail in the batch when several pages reuse its opening stem, rhetorical sequence, or generic success ending.
      The batch NEEDS WORK when prose is interchangeable after noun substitution or when repeated scaffolds make distinct pages sound like one form letter.
      Do not repair this by demanding cosmetic synonym changes; the smallest fix is to restate each page's actual stake in its own natural order.
      The report is one row per review unit:
      **The evaluation row**: one row per reviewed unit, so a failed criterion points straight at its repair.
      ```text
      unit | applicable requirements + source | verdict | evidence | smallest fix
      ```
      Then report requirement conflicts, mechanical findings, and one page-level verdict.
      The review is read-only: it never edits prose, changes an Aim State, ticks Decision Now, or closes a page.
      Execution uses existing surfaces rather than a new skill:
      - `check.py --strict` supplies the deterministic mechanical findings.
      - The page's `✅ Quality Check` runs the complete row-by-row rubric quickly in the current page chat.
      - `haipipe-board-reviewer-agent` runs the same contract in a fresh context after revision and adds the batch voice gate when several pages changed.
      The quick check helps the author iterate; only the fresh reviewer tests whether the page stands on its own without conversation context.
      There is NO `## Boundary` section (JL 260731, said twice). It was added by CC on 260723 and never ruled in. What a page covers is the Opening's job; point at a neighbouring page from the prose that needs it, as a `**Covered elsewhere**:` part in the Opening's drawer.
      The same ruling renamed three sections: `## Question` -> `## Opening`, `## Items to Finish` -> `## Aims`, `## Where we are` -> `## States`. `src/common.py` still ALIASES every old name, so a page on the old vocabulary keeps rendering correctly. Do not read that as permission. This skill claimed the removal was finished on 260731; on 260802 the board still had 26 `## Boundary` sections and 45 of 55 pages on the old names, because a forgiving renderer means nobody ever sees the drift. `check.py` now reports every retired name as `retired-section`, which is the only reason this paragraph can be trusted.
      One name is RESERVED inside States (JL 260731): `### Decision Now` holds the decisions a machine proposes and the human must make, one `- [ ]` row each carrying the ask, the options, and a recommendation.
      A proposal never lives only in chat: it is written there on the owning page, the human answers by ticking, and an answered row moves into the page's dated record.
      The options take ONE LINE EACH, and each line says what choosing it commits you to (JL 260731: "I want the decision A, B, C, to be in a new line and explain each options, not all the options in one line").
      Three labels crammed onto one line name the options and explain none, so the reader has to reconstruct the consequences before they can choose.
      The recommendation is its own line, naming the letter and why it beats the others.
      **A Decision Now row**: the shape a page uses to put one choice in front of a human.
      ```markdown
      - [ ] 🗣 The ask, stated as one question
            One or two lines of context: what is true today, and what it costs.
            A · the first option, and what choosing it commits you to.
            B · the second option, and what it commits you to.
            → CC recommends B, because <the reason it beats A>.
      ```
      **The write anchor rule (QC1b §4, from a real casualty).**
      A machine write lands at a SECTION BOUNDARY, never at a byte offset: on 260730 a concurrent session spliced a `###` block into the middle of another page's `## Opening` sentence.
      Appending under a named `## ` heading is safe; inserting by offset is how that damage reproduces at scale.
      **The human-decision rule (QC1b §5).**
      A verb reading a transcript can report what the transcript CLAIMS, not verify it.
      So a machine may update an Aim's State only from evidence it can inspect, and may propose a human ruling as a `### Decision Now` row.
      **Closing a row (JL 260802, amending the never-tick rule).**
      A machine CLOSES a `### Decision Now` row once the human has answered it, and records the answer in the same write: which option, who ruled, when, and the words they used.
      What it may never do is close a row nobody answered, or flip a page-level human gate.
      The old rule left every answered row open, so a page showed decisions as pending that had been made hours earlier and acted on, which is the same drift the board exists to prevent.
      Answered means the human said it: in chat, in a comment lane, or by ticking. A machine's own recommendation is not an answer, however confident it is.

- 6 · 🏷 Addressing
      **How a location is addressed**: what each level of the board is called, and how it is written.
      ```
      page        QB4            #QB4
      face        QB4a           a page whose id carries its parent's number
      group       #group-QB      scrolls the index, opens nothing
      sentence    QB5's grammar  haipipe-board-sentence owns everything below the section
      ```
      Every id inside a fenced figure renders as a link (haipipe-board 0.53.0), so a contract that names pages is itself a map.

- 7 · 📂 Files
      **This skill's own files**: what ships in the folder, and what each part is for.
      ```
      haipipe-board-page/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 (the section mapping and requiredness) and §8 (on-stage order) as the authority; owns no scripts.
      The named next step (QC1b §1): `live/chat.py`'s four hand-rolled rule strings (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`) become this contract's consumers instead of restating it, which kills the copies, one of which has already rotted once.
<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## States
Mirrored into the Engine roster as the generic page contract used by every route. `QC3` is the bridge to Paper-specific page meaning; the Board card itself remains a reusable specification rather than a second Paper authoring contract.

## Log
260801 0000 · page generated from `board/haipipe-board-page/` by `skillpage.py new`

<!-- haipipe:skill:log:start 372a94b2e00ec17f board/haipipe-board-page -->

Converted from the skill's own `CHANGELOG.md`: 10 releases.

260802 · `0.10.0`
      - `working on an existing page` gains steps 7 and 8: ONE page is the deliverable,
        a write outside it is allowed only when the page cannot be made correct without
        it and must be named in the report, and a sibling page's CONTENT is never
        rewritten. Step 5 sends an agent to other files on purpose; nothing bounded it.
      - The verb now states the measurement that produced the rule. Three fresh agents
        were each given one sentence and nothing else on 260802. All three found this
        skill unaided (at tool calls #5, #6, #5) and drove their page to zero findings,
        including the one whose wording matches no trigger in the description. They then
        disagreed completely about reach: 1 file versus 15, the wide one touching four
        shipped `SKILL.md`, four `CHANGELOG.md`, six sibling pages and `board.md`.
        Neither was wrong on the merits, which is exactly why the bound had to be written
        rather than left to judgment.
260802 · `0.9.0`
      - A machine now CLOSES a `### Decision Now` row once the person has answered it,
        recording which option, who ruled, when, and the words they used (JL 260802:
        "I think you should close it automatically, please go ahead and do it").
        It still may not close a row nobody answered, and may not flip a page-level
        human gate; a machine's own recommendation is never an answer. Before this a
        row answered in chat and acted on within the hour still rendered as pending,
        so the page reported work as waiting that had already shipped.
260802 · `0.8.1`
      - Repointed every design-board citation after `QC1b`'s 260802 Content rebuild: the door test
        moved from `QC6 §7` to `QC1b §1`, the anchored-write rule from `QC6 §9` to `QC1b §4`, and the
        human-decision rule from `QC6 §10` to `QC1b §5`.
      - Corrected the named next step. The rule strings it must replace are not in `cli/serve.py` and
        there are not one of them: they moved to `live/chat.py` in the `QC2c` live-layer split, and
        there are four (`CHAT_RULES`, `FULL_RULES`, `BOARD_CHAT_RULES`, `BOARD_FULL_RULES`).
260801 · `0.5.1`
      - Clarified the base/variant boundary: a consumer variant defines Content and
        may fill typed records through declared Aims, States, and Stage Contract
        extension points, but it never redefines the shared frame sections.
260801 · `0.5.0`
      - Keeps requirements in the page spec instead of copying them into a separate
        evaluation skill.
      - Resolves base, variant, page-local, Stage Contract, division, and paragraph-job
        requirements before judging.
      - Defines four axes (mechanics, function, evidence, readability), four verdicts,
        and one evidence-bearing report row per section or Content unit.
      - Assigns execution to the existing `check.py`, `✅ Quality Check`, and fresh
        Board reviewer surfaces.
260801 · `0.4.1`
      - Canonicalized the paired section labels as `Aims / States`: both are plural
        collections, while one Aim still maps to one current State record.
      - Kept singular `State` as a legacy input alias alongside `Where we are` and
        `Now`.
260801 · `0.4.0`
      - The page contract now separates durable intent from present fact. `## Aims` holds stable Content-linked targets (`A3.1`, with `P1` for page-level targets), a testable `Done when`, and an optional temporary `Plan`. `## State` mirrors every Aim exactly once with ⬜, 🟡, 🟠, ✅, or ⏸️. State transitions go to Log; Decision Now remains the human-only checkbox edge. A Content division may have zero, one, or many Aims, while every Aim must have one current State row.
      - The fixed sequence is `Opening → Diagram → Content → Aims → State → Files`. The contract no longer teaches the retired generated Structure row or checkbox-based page completion. Historical `Items to Finish`, `Done when`, `Where we are`, and `Now` remain parser aliases, not canonical authoring guidance.
260801 · `0.3.0`
      - The five-row section contract (JL 260801, ruled as option A on the design board's
        QB4 Decision Now): every section answers ONE reader question, and the same five
        rows define each section's contract — conveys · holds · source · rules · omit.
        The seven-sections table gains the reader-question ladder plus the
        misplaced-sentence rule (substance in Opening → Content, contract material in
        Content → Stage Contract, settled flags → Where we are, open work → Items to
        Finish). Long form stays on the board's QB4a-QB4g faces; the compact form now
        lives here and in `ref/q-template.md`'s How-to-use comment, where a writer
        actually meets it.
260731 · `0.2.0`
      - Decision Now: the one RESERVED subsection name inside `## Where we are` (JL, same
        day: "don't make the decision here ... Always go to the corresponding Q's Where we
        are's subsection of Decision Now"). It lists the decisions a machine proposes and
        the human must make, one `- [ ]` row each with the ask, the options, and a
        recommendation; the human answers by ticking; an answered row moves into the
        page's dated record. The 260729 contextual-naming rule stands for every other
        subsection; this is its single exception.
      - The tick rule now names the landing spot: a machine PROPOSES a tick as a Decision
        Now row, never in chat alone.
      - The board pages `QB4e` (the Where-we-are face) and `QC6` on the design board carry
        the first two live subsections.
260731 · `0.1.0`
      - First cut, created on JL's order ("make the haipipe-board thinner, and have other
        skills, like haipipe-board-page ... please creating them now") from the roster the
        design board had already settled: QC6 §8's shape is one door, two SPECS, two VERBS,
        and this is the page SPEC the routing and digest verbs LOAD.
      - Contract-first: no code moved. It owns what a page IS (the three kinds over one
        base, the seven sections in their fixed order, the write anchors), and it cites
        `haipipe-board/ref/q-template.md` as the authority rather than forking it.
      - Carries the two machine-write rules with their provenance: writes land at a
        SECTION BOUNDARY, never a byte offset (QC6 §9, after a concurrent session spliced
        a heading into the middle of another page's Question sentence on 260730), and a
        transcript-reading verb may propose a tick but never tick or flip `state:`
        (QC6 §10, because reporting a claim is not verifying it).
      - Names its own next step from QC6 §7: `serve.py`'s `CHAT_RULES` becomes a consumer
        of this contract instead of a hand-rolled copy, which has already rotted once
        (QB5d caught it describing a page shape that no longer existed).

<!-- haipipe:skill:log:end -->
