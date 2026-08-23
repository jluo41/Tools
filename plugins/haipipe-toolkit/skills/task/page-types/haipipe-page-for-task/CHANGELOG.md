## 0.9.0 · 2026-08-22 · `Introduction` enters the FLAT shape, `Landscape` enters the set, and the ARC leaves this contract

Three rulings by JL in one session, and they split cleanly: two grow the WORD SET,
one gives the ARC away.

- **`Why` → `Introduction`, and it becomes FLAT-legal as division 1.** JL: "I think
  we should have an Introduction". `Why` had been topic-level only, on the argument
  that a single-topic page states its why in `## Opening`. That argument conflated
  the ABSTRACT with the INTRODUCTION, which every paper keeps apart: Opening says
  what this page is and why to care, in one paragraph above `## Content`;
  `### 1 · Introduction` says what the folder was run to settle, what was already
  established, and what this report claims.
- **What the old rule cost, concretely.** `QC1-postrain-replication` is FLAT, the
  common shape. It carries sixteen divisions using five of the six available words,
  and the word it could never use was the one that tells a reader what the work was
  FOR. Its reader met the finding before meeting the question.
- **`Landscape`, added after `Concept`.** JL: "这 concept 可不可以加一些，比如说
  related work 呢？相当于放一些 literature review 的东西". It holds what the FIELD
  already established, as against what this folder's own runs established.
- **Why the set needed it.** External-evidence claims had nowhere legal to live. On
  the same page, two `route: discovery` cards — at what scale each framework has
  been demonstrated, which organizations are documented as using one — served a
  division titled `Method · Both frameworks`, under a bullet whose own head reads
  `Two Claims That Rest On READMEs`. `Method` is defined as what was RUN and what it
  was run INSTEAD OF; a literature claim is neither.
- **Why one word, and why this one.** `Related Work` is two words, and this set
  rejected `So what` in 260816 on exactly that ground — chip width and an awkward
  grep — so the precedent forced a single word. `Background` loses because in
  ordinary use it covers vocabulary AND prior art, which is the blur `Concept`
  exists to prevent. `Landscape` cannot be confused with `Concept` and is already
  this repo's word for the same object one layer down: the discovery family writes
  `landscape.md` from a `landscape_review`, and a `Landscape` division is written
  FROM those files. Rejected with it: `Prior` (incomplete as a chip) and `Context`
  (vague, collides with `Introduction`).
- **Why `Landscape` sits after `Concept` and not straight after `Introduction`.**
  A paper conventionally puts related work second. This set orders by what the
  reader still LACKS, and a field map written in terms the reader has not met is
  unreadable. The vocabulary goes first. That is the same boundary test every other
  pair in the arc passes, not an exception to it.
- **The ARC moves to `haipipe-page-outline` §🎭.** JL: "我们也会有其他的 pages 所以
  这个 four types 就是我们提供什么样的 outline template，然后 haipipe-page-outline
  目的就是想要讲什么样的 story arcs". Sequence-is-the-argument, the three forbidden
  orderings (run · config · the order the AUTHOR found things out) and the
  per-boundary swap test were 0.7.0 material living in this type. They are not
  task-specific — there are ten Page Types and every one of them can be ordered by
  the author's history — so they belong to the phase that plans any page. What stays
  here is WHICH WORDS; what leaves is WHICH ARGUMENT.
- **Checker lines updated at both levels**, plus one new invariant: `Introduction`,
  when present, is the FIRST `###` and appears once. A page with two introductions
  has none.

## 0.8.0 · 2026-08-21 · the last division is `Conclusion`, and the word it replaced left a rule behind

JL ruled the closed prefix set's last word from `Meaning` to `Conclusion`. The set
grows and changes only by ruling, so the swap is argued in SKILL.md rather than
applied silently.

- **Why now, and why it was cheap.** Zero pages in the repository used
  `### n · Meaning ·`; the word had lived only in the contract. Renaming after the
  first page would have been a migration, and this was the last moment it was not.
- **Why `Conclusion` wins an argument `Meaning` won in 260816.** That ruling chose
  `Meaning` because the heading stated the closing rule, and it rejected `So what`
  (two words), `Verdict` and `Takeaway` (rare, idiom). `Conclusion` was never on
  that list. It clears every bar those rejections set — one word, common, not
  idiom, plain grep — and it is the name the reader already has: §📰 says a task
  page IS a technical report, and a report's last division has always been called
  this.
- **⚠️ What was given up, and the rule that pays it back.** `Meaning` carried its
  demand inside the word: you cannot fill a division named for meaning with a
  restatement of the divisions above it. `Conclusion` is softer and invites exactly
  that summary. The demand moved out of the name and into a line: **a `Conclusion`
  division with no READING record in it is not written yet.** The closing rule
  itself is unchanged.
- Checker updated at both levels: `^### \d+ · (Data|Method|Result|Conclusion) · `,
  and `the LAST ### is Conclusion`. The `#### ` nested alternation is untouched,
  because this word never sat at topic level.
- One occurrence of `Meaning` is deliberately preserved: the 260816 note rejecting
  `Task-Input / Task-Method / Task-Output / Task-Meaning`. Rewriting a quoted
  history to match a later ruling would make the record lie.

Two more, ruled the same day on the same page:

- **`⛔ A NEW RUN IS NOT A NEW DIVISION.`** A task page's subject regenerates, so
  the pressure to append a `Result` division per finished run is constant, and
  twelve of them produce the run log this contract already forbids wearing
  correct role prefixes. The two axes are separated: a new RUN is a new ROW in
  the READING record, which was built to grow; a new MESSAGE is a new division,
  and only when no existing title can absorb it without becoming a lie. This is
  also the answer to work outlasting one sitting — the READING record is the
  resumable surface, and ⬜ rows say where to restart.
- **`⛔ FLAT DOES NOT MEAN ONE OF EACH.`** Found by running 0.8.0's own checker
  against the first page written to it: ten of eleven divisions passed and
  `### 1 · Concept` was flagged, on a page whose shape JL had specified directly.
  The closed set always fixed the ORDER of the words and the position of
  `Conclusion`; it never fixed their MULTIPLICITY, and the line implying "Result
  repeats, everything else appears once" was describing its one example. A flat
  report with Method 1..n and Result 1..n is the ordinary shape of a technical
  report and is now named as legal, with `Concept` and `Data` admitted at `###`
  for the same page-level reason NESTED already admitted them. The FLAT grep
  gains both words. The FLAT/NESTED test is unchanged and is still the only
  thing that decides between the shapes.
- **`template.md` now EXISTS.** §📂 Files has declared it since 0.1.0 and the file
  was never written, which is precisely the failure the contract itself names as
  the worst case: a declared artifact whose only deliverable was the sentence
  declaring it. Every sibling under `paper/page-types/` ships one. It carries the
  RULE comments inline, to be deleted as each is satisfied.

## 0.7.0 · 2026-08-20 · reporting is the FORM, and the sequence is the argument

New section `📰 The page IS a technical report, and the six words are its ARC`,
placed before the closing rule, because what a page is FOR precedes how it closes.

- The contract stated only half its job. It closed on READING and never said the
  page REPORTS, so the six words read as a checklist of boxes rather than as the
  arc a technical report has always had. The section groups them: Why, Concept,
  Data and Method are SETUP, without which the result cannot be read; Result is
  the finding; Meaning is the consequence.
- **Role-complete is not arc-coherent.** All six words present, each division in
  present tense with checked counts, and still not a report. Named as the
  commonest shape that passes every mechanical check and fails its reader.
- **LEARNING ORDER is a third kind of log**, beside run order and config order,
  and it is the one that survives every check. The two already forbidden are
  caught by their titles carrying the machinery's own names; this one has correct
  present-tense titles and hides the diary in the spacing between divisions.
  Found 260820 on a Board plan whose five divisions fell into three blocks
  matching what was known before a session, what the session did, and what it
  left open. Repair: the two machinery divisions merged, since their only
  separation was arrival time.
- **The swap test**: for each adjacent pair, name why N must precede N+1. "Method
  before Result, or the number cannot be believed" passes. "That is the order we
  found them in" fails, because a reason that is a date is not a reason.
- **A residual is a DIVISION, not a footnote.** `Meaning`'s `not answered` row is
  a pointer, not the account. What the runs did not settle takes its own place
  before `Meaning`, with role `Result`, or it lives as parentheticals inside the
  division whose job is the finding.
- Says why this belongs to this type and not the base: a task page is written
  beside a folder that is still being run, so learning order is the order its
  material arrives in. The pressure is structural here and incidental elsewhere.
- Frontmatter: description leads with TECHNICAL REPORT; `outline.shape` now
  carries the sequence rule and the residual rule; triggers gain report
  structure, division order, learning order, residual division.

## 0.6.0 — 2026-08-19

- **A discovery folder is a special TASK.** New `folder-kind: task | discovery`
  key; no sibling page type is created (JL 260819: "the discovery will be in the
  task as well, like a special task?"). Both are executors with the same
  four-phase lifecycle answering into a `QA/<n>-<slug>.md`, so a second contract
  would restate this one and then drift from it.
- The key changes only where the page reads, what a `Result` division is reading,
  and what the verdict binds to. The grammar, the FLAT/NESTED fork and the
  `Meaning`-last closing rule are untouched.

haipipe-page-for-task · Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.5.0 - 2026-08-16

**FLAT and NESTED: one page may carry several topics, each with its own Data and
Method** (JL 260816, "what if one page with different topic? I mean one division
can be one topic, and each topic we can have the Why, Concept, Data, Method,
Result, Meaning").

0.4.0 put the words at division level and let `Result` repeat. That works for one
topic and breaks for several: `Data` and `Method` appear ONCE at the top, so a
page whose IV runs on a different subsample than its main OLS cannot pair each
result with the sample and spec that produced it. The pairing was silently lost.

- **FLAT** — one topic. The words ARE the divisions, unchanged from 0.4.0.
- **NESTED** — several topics. A TOPIC is the `###` division with a free title,
  and the words become its `#### <n>.<m> ·` paragraphs, using the base's own depth
  grammar (`QPs1`: the depth of the number says whether a group exists).
- **The test is one question**, and it is not a preference: "does a second topic
  need its OWN Data or its OWN Method?" No → FLAT. Yes → NESTED. One topic forced
  into NESTED is six headings describing one regression.
- **Two words added, topic-level only**: `Why` (why do this topic at all) and
  `Concept` (what the terms mean). `Concept` earns its place from JL's standing
  rule that every term is defined the first time, and a task page is full of terms
  a reader has never met: SPS, ADI, ipsatization. Neither word appears on a FLAT
  page: its Opening already says why the one topic exists.
- **`Result` is the only REQUIRED word.** A topic with no result is not a topic.
  A topic reusing the page's cohort owes no `Data`; a topic with no fork owes no
  `Method`.

**🔒 `Meaning` never goes inside a topic, in either shape.** This is the ruling
that keeps the closing rule intact. Per-topic Meaning divisions would leave
nothing able to say whether the PAGE is closed when three topics are read and two
are not. So `Meaning` stays exactly one page-level division, always last, and its
record carries ONE ROW PER TOPIC, each row naming its own `verdict-run`:

```
READING · <date> · <who read it>
Main OLS   verdict-run run_main   ✅ read · <what it means>
IV         verdict-run run_iv     ⬜ unread
```

The page closes when every row is read. A rerun of any named run re-opens the page
and un-reads that row alone.

- The checker now greps at both levels: `^### \d+ · (Data|Method|Result|Meaning) · `
  for FLAT, `^#### \d+\.\d+ · (Why|Concept|Data|Method|Result) · ` for NESTED, and
  in both shapes the LAST `###` must be `Meaning` and `Meaning` must appear once.

## 0.4.0 - 2026-08-16

**`Why` becomes `Method`, and it records the CHOICE, not the steps** (JL 260816,
"what is the method? Like the regression method, the code method").

0.3.0 picked `Why` after seeing that the real division titles start with "Why".
Reading all thirteen Method divisions instead of two shows that was half the set:

- SIX are titled `Why X and not Y` (`Why k-means on five traits and not on ten`).
- FIVE state what was actually run (`Three tests, three questions`, `Residualize,
  then recompute, rather than adding a control term`). A regression's
  specification is not a "why", and `Why` had no room for it.
- What all THIRTEEN share is a FORK: every title names something that could have
  gone another way, marked `and not`, `rather than`, or `deliberately`. Even
  `Plain description, deliberately: no model, no test` is a fork — the choice was
  to run nothing.

So the division holds the choice AND its alternative, never a step list, because
the steps are in the code and the code is in `## Files`. `Method` is the word that
carries both halves, and it is the field's own word for it.

- New table: what `Method` holds for a regression, clustering, descriptive,
  transform, code/builder and data task, each row taken from one of the thirteen
  real pages.
- New finding rule: a Method division with no fork in it has not been written yet.
  `How it works: the steps, in the order the script runs them` is the boilerplate
  all thirteen pages carry ABOVE their real title, and it is what to delete.
- The closed set is now `Data · Method · Result · Meaning`.

## 0.3.0 - 2026-08-16

**Every division opens with one fixed word: `Data` · `Why` · `Result` · `Meaning`**
(JL 260816, "should we have the section starting with the fixed words"). This
answers the question 0.2.0 left open: if DRAFT names every division freely, two
task pages look nothing alike and nothing can compare or roll them up.

The fix is not to unify the TITLE. It is to unify the ROLE, and to put that role
in the heading itself rather than in a second field:

```
### 3 · Result · Which traits track the rating, and which barely do
        ╰FIXED╯  ╰────────────── FREE, this page's own ──────────────╯
```

- The prefix uses machinery the board ALREADY renders: `QPs1` §0.6 makes whatever
  sits before the first ` · ` the heading's address chip. So the role is visible
  and clickable with nothing new built, and it cannot drift from the heading the
  way a separate `role:` line could.
- `Result` REPEATS, once per result family. A task running main OLS, robustness,
  IV and DID gets four `Result` divisions. That is how one page covers many
  topics while staying comparable to a page that has one.
- `Meaning` is exactly one, always LAST, and is the closing division. It replaces
  the name `Reading` used in 0.1.0-0.2.0: a division named for the reader's
  takeaway beats one named for the act of reading.
- `Runs` stays deleted (0.2.0's ruling), into `## Files`.
- A checker greps `^### \d+ · (Data|Why|Result|Meaning) · `; any other word before
  the first ` · ` is a finding.

**Word choice, and what was rejected.** JL's first draft was `Task-Input` /
`Task-Method` / `Task-Output` / `Task-Meaning` ("I just randomly pick up some
word, maybe you can put better words").

- `Task-` dropped. `QPs1` §0.6 already ruled the identical case for page ids: the
  prefix drops "because the tab and the breadcrumb already say which page you are
  on". The `page-type: task` head key says it once; every chip need not repeat it.
- `Input`/`Output` → `Data`/`Result`. Input and output are the pipeline's own
  words, and this contract forbids the pipeline's words at division level twelve
  lines above its own prefix table. `Result` also matches the term already in use
  here, RESULT FAMILY.
- `Method` → `Why`. The thirteen real pages label the division `How it works`, and
  then every actual title under it opens with Why: `Why these three splits and
  this correction`, `Why a violin plot and not a scatter`. The reader's word is Why.
- `Meaning` kept, from JL's draft; it was the best of the four.
- Rejected: `So what` reads best of all for a weak English reader and loses only on
  being two words, which widens the chip and makes the grep awkward. `Verdict` and
  `Takeaway` are rarer words, and `Takeaway` is idiom.

## 0.2.0 - 2026-08-16

**The five fixed divisions were a defect, and the base contract already said so.**
0.1.0 declared `### 1 · Inputs`, `### 2 · Method`, `### 3 · Runs`, `### 4 · Results`,
`### 5 · Reading` as the type's content shape. Three of those five are MACHINERY,
which `haipipe-page-draft` §🗂 forbids at division level: "a division names what the
READER LEARNS, never where the material came from ... `QA inputs`, `Displays`,
`Run receipts`, and `Provenance` are machinery."

A task page walks into this by construction, because its subject IS a folder and the
folder's own names (`configs/ runs/ results/`) are sitting right there waiting to be
copied up into headings. 0.1.0 copied them.

- The type now fixes TWO things only: the LAST division is always `Reading` (the
  closing division), and divisions group by the task's own RESULT FAMILIES rather
  than by the order the pipeline ran.
- Division titles move to DRAFT's INSTANCE outline, per the three-layer model in
  `haipipe-page-draft` §🧬 (FRAME = section order · CONTENT = the Page Type's
  division shape · INSTANCE = DRAFT's outline for this page).
- New `## 📋 The outline DRAFT hands over` section: the numbered division list with
  the `establishes` and `evidence owed` columns, using the three evidence kinds
  `haipipe-page-evidence` owns (📚 citation · 🔢 value · 🖼 display). 0.1.0 had no
  evidence column at all, so its outline had no testable exit.
- The run table and the `<NAME>` sister-file token move from a division into
  `## Files`, where a reader looks for machinery.

## 0.1.0 - 2026-08-16

First contract, written on JL's question "我们对这个 task 的配置定义应该是什么样子的?"

- Closing rule ruled: a task page closes when THE RESULT IS READ — a person wrote
  what the numbers mean against the task's own question — and the reading is bound
  to one run name. A rerun of that run RE-OPENS the page.
- That re-openability is what admits the type under the admission law
  (`QPs2-page-types.md` §1): a stage page closes when a human gate passes and stays
  closed; a task page is re-openable BY DISK, because its subject regenerates.
- Head keys: `page-type: task` (required, because 31% of real task-folders do not
  match the `{NN}_<name>` convention, so no filename can mark one), `task-folder:`
  (the companion already on disk), `verdict-run:`.
- Four binding rules: by path never by copy · every number names its run · a rerun
  re-opens · one authority each between the page and `QA/<n>-<slug>.md`.
- ⬜ Open ruling for JL, unchanged from 0.1.0: `ref/task-structure.md` §"Task-level
  diagram/" already ships `01-overview · 02-design · 03-runs · 04-progress` per
  task-folder, in .txt files nothing renders. Either the page absorbs them or they
  stay as its source. Until ruled, the page names them in `## Files` and does not
  duplicate their prose.
- ⬜ No `template.md` yet: a template serializes the typed record, and freezing its
  fields while the type definition is still moving would be premature.
