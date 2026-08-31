---
name: haipipe-page-for-task
description: >-
  The VARIANT contract for a TASK Page: one page per task, and the
  technical report of what that folder found — carrying the READING of the
  result, which no file in the folder can hold. Every shown number names the
  run that produced it, and a rerun reopens the page. Use when results exist
  but nobody wrote what they mean. Trigger: task page, technical report,
  results reading, verdict, rerun reopens, page-type task.
metadata:
  version: "0.10.0"
  last_updated: "2026-08-30"
  folder-kind: task | discovery   # a discovery folder is a special task (260819)
  outline:
    mode: grammar          # fixed | grammar | resolved
    source: "this SKILL.md"
    shape: "FLAT or NESTED; first word from {Introduction, Concept, Landscape, Data, Method, Result, Conclusion}; Introduction when present is division 1 and appears once; Concept, Landscape, Data may sit page-level; Method, Landscape and Result repeat; a residual earns its own Result-role division; Conclusion is one page-level division, always last. The ARC that orders them is haipipe-page-outline's, not this type's"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-task · the folder ran, and someone has to say what it means

## 📂 A DISCOVERY folder is a special task, not a page type of its own

Ruled 260819 (JL: "the discovery will be in the task as well, like a special
task?"). One `folder-kind:` key says which kind this page reads, and everything
else on this contract holds unchanged:

```text
  folder-kind: task        tasks/<group>/<folder>/     plan · build · execute · report
  folder-kind: discovery   discoveries/<group>/<folder>/  plan · build(opt) · execute · report
```

**Why one contract and not two.** Both are executors with the same four-phase
lifecycle, both answer a question by writing `QA/<n>-<slug>.md`, and both hand a
page the same job: read what the folder produced and say what it means. A sibling
contract would restate that and then drift from it. `haipipe-task` and
`haipipe-discovery` already share this shape at the layer below.

**What the key CHANGES**, and it is only these:

```text
  where the page reads      tasks/… vs discoveries/…
  what a `Result` division  a run's numbers  vs  a source list, a verdict,
  is reading                                     a landscape, or ideas
  what the verdict binds    a run name       vs  a discovery folder + its QA file
```

**What it does NOT change**: the grammar (as of 0.9.0, `Introduction · Concept ·
Landscape · Data · Method · Result · Conclusion`), the FLAT/NESTED fork (⚠️ these two words here describe the PAGE's division layout — one topic vs many; hierarchy.md reuses the same pair for a JOB's folder shape, a different axis entirely), `Conclusion` always last and page-level,
or the closing rule that a person must read the result against the folder's own
question. A discovery page that skips `Conclusion` is as unclosed as a task page.


**LOAD `haipipe-page` FIRST.** It owns the base frame. What this file guards is READING: a job can produce a correct number and answer nothing, and no file inside that folder is allowed to say so.

**The kind this variant covers**: one page per TASK.

⚠️ **REBOUND 260830 (JL), from JOB to TASK.** A job holds many tasks — Proj1's
`j04_aidatastore` holds eight — and one page reading eight unrelated computations
is a folder listing, not a reading. Since 260830 a task is SELF-CONTAINED and its
page lives inside it as `tNN_<name>/tNN_<name>.md`, so the page and the thing it
reads are one folder. Pages already written against a job stay valid and are read
as covering that job's whole task set; new ones are written per task.

The page's address IS the task's address: `b02j01t03`, read off the path.

```
kind      subject                              closes when
──────────────────────────────────────────────────────────────────────
Task      ONE job: inputs · code ·            a person READS the result against
          runs · results                        the task's own question, and the
                                                reading names the run it is bound to
```

**The type key.** A task page declares `page-type: task` in its frontmatter, and the line is REQUIRED: a task page wears whatever name its job has (`A01.01`, `B4_fit_scaling_law`, `C3-Visual-ForecastScaling`), and 31% of real jobs do not match the `{NN}_<name>` convention at all, so no filename shape can mark one. The `page-type:` key beats the filename (base, type resolution step ③).

## 📕 What the job already holds, and what it can never hold

Every one of these already exists on disk before a page is written, so the page must not re-hold any of them:

```
plan.yaml            what was intended        report.yaml   what ran
results/<run>/       the numbers              notebooks/    what happened
configs/ · runs/     how it was invoked       QA/<n>-<slug>.md  one caller's
                                                              question, write-once
```

Not one of them ever says **"and therefore ___"**. `metrics.json` holds `0.83`; nothing on disk holds "0.83 means the approach works" or "0.83 is the same as the baseline, so this direction is dead". That sentence is a human judgment about an empirical result, it is what everyone downstream actually needs, and it is the only thing this page exists to carry.

## 📰 The page IS a technical report, and the seven words are its ARC

A task page has one job with two halves, and the contract used to state only the
second. **It REPORTS what the folder found, and it closes when a person READS
that report against the folder's own question.** Reading is the closing act.
Reporting is the FORM, and the form is what a reader gets wrong first.

The seven words are not a checklist of boxes to fill. They are the arc a technical
report has always had, and each one earns its place from the one before it:

```text
  Introduction  the reader does not yet care        ─┐
  Concept       the reader cannot yet parse it       │  SETUP: without these
  Landscape     the reader cannot yet tell what      ├─ the result cannot be
                is NEW about it                      │  read
  Data          the reader cannot yet trust it       │
  Method        the reader cannot yet believe it    ─┘
  Result        what came out                       ─── THE FINDING
  Conclusion    what it costs, and what to run next ─── THE CONSEQUENCE
```

**Why `Landscape` sits after `Concept` and not straight after `Introduction`**
(ruled 260822 by JL, who asked for it: "这 concept 可不可以加一些，比如说
related work 呢"). A paper conventionally puts related work second, and this
set does not, because this set orders by what the reader still LACKS. A field
map written in terms the reader has not met is unreadable, so the vocabulary
goes first and the map goes second. That is the same test every other boundary
in this arc passes, applied one more time rather than an exception to it.

**⛔ THE SEQUENCE IS THE ARGUMENT, and this contract no longer owns that rule.**
A page may carry all seven words, each division correct and each in present
tense, and still not be a report, because the order came from the author's
history instead of the reader's need. That failure is not a task-page failure —
it reaches every Page Type, and there are ten of them — so the rule, the three
forbidden orderings (run · config · the order the AUTHOR found things out) and
the per-boundary swap test moved to **`haipipe-page-outline` §🎭** on 260822,
where the OUTLINE phase runs them as its ⓪ ARC check before any other check.

**The split, stated once so neither side restates the other:**

```text
  THIS contract    WHICH WORDS a task page may use, in what order,
                   and how many of each                      ── the TEMPLATE
  haipipe-page-    WHICH ARGUMENT those words are arranged
  outline §🎭      to make, on this page, this round          ── the ARC
```

**A residual is a DIVISION, not a footnote.** `Conclusion` carries a `not answered`
row, and that row is a pointer, not the account. What the runs did NOT settle
needs its own place before `Conclusion`, or the reader assembles it from asides
scattered through `Result`:

```text
  ✅  Data · Method · Result · <what is still not settled> · Conclusion
  🔴  Data · Method · Result · Conclusion
                        ▲
                        └── three residuals living as parenthetical remarks
                            inside a division whose job is the finding
```

The word for that division is free, as every title after the fixed prefix is. Its
ROLE is `Result`: it is what came out, stated as the part that came out empty.
A page with no residual either answered everything, which is rare enough to be
worth saying out loud, or has not looked.

**Why this belongs to THIS type and not to the base.** Every page reports
something. A task page reports an EMPIRICAL RESULT that regenerates, so its
author is always writing while the work is still moving, and learning order is
the order the material arrives in. A stage page is written once against a fixed
gate; a task page is written beside a folder that is still being run. The
pressure toward ③ is structural here and incidental elsewhere.

## 🏁 The closing rule, and why a rerun re-opens the page

A task page closes on one typed record in its LAST division, `Conclusion`, and nothing else closes it:

```
READING · <date> · <who read it>
<topic>   verdict-run <run>   ✅ read · <what it means, in plain words>
<topic>   verdict-run <run>   ⬜ unread
   RULE · in a NESTED job (hierarchy.md "Two job shapes") <run> is the PATH
   <task>/<run> — run stems are unique only within their task, so a bare stem
   is ambiguous the moment two tasks share one (both having a `wide`, say)
answers       Aim A1 · A2     which of this task's questions are now answered
not answered  A3              what these runs did NOT settle
next run      <the run that would settle it, or "none: the question is dead">
```

A FLAT page has one topic and so one row. A NESTED page has one row per topic, each naming its own run, which is why the record lives at page level and never inside a topic (§🪆).

A verdict may be red and still close the page: "the run happened, the result does not answer the question, and here is the run that would" is a complete reading. What is never a close is a green state with no reading under it.

**A rerun re-opens.** The verdict binds to `verdict-run`, not to the task's name, so when that run's `results/` change the page drops back to 🟡 and the reading is re-taken. This is the same fallback the display type uses when a unit is re-rendered after acceptance: what was accepted was a specific render, and what was read here was a specific run.

**This is what admits the type.** A 🪜 stage page closes when a human gate passes and it stays closed. A task page is RE-OPENABLE BY DISK, because its subject regenerates. That is the distinguishing fact, and without it this would be a template rather than a Page Type (the admission law, `QPs2-page-types.md` §1).

## 🗂 What this type FIXES, and what DRAFT's outline decides

Content shape has an owner at three altitudes (`haipipe-page-draft` §🧬): the FRAME fixes the section order for every page kind, this CONTENT layer fixes the division shape for task pages, and DRAFT's INSTANCE outline names this task's actual divisions. This type is deliberately thin at the middle layer: it fixes two things and leaves division titles to the outline.

```
Opening      ❓ what question was this task RUN to answer, and why now
             ◀ motivation #1: why the task exists
Diagram      raw data ─▶ input ─▶ code ─▶ results   the task's IPO shape
Content       🔒 one fixed word · ✍️ one free title, in ONE of two shapes
  FLAT     one topic  · the words ARE the divisions
  NESTED   many topics · a topic is the division, the words sit inside it
  ### n · Conclusion · <free>   exactly 1, ALWAYS LAST, in BOTH shapes
Aims         one Aim per question this task must answer
States       per question: answered · needs another run · dropped
Files        the job paths, including every QA/<n>-<slug>.md
```

**⛔ A division names what the READER LEARNS, never where the material came from.** `Inputs`, `Runs`, `Provenance` and `Run receipts` are MACHINERY, and a task page is the single most likely page in the system to lead with them, because its subject IS a folder and the folder's own names are sitting right there. Copying `configs/ runs/ results/` into `### 1 · Inputs`, `### 2 · Steps`, `### 3 · Runs` hands the reader the author's filing system instead of the finding. The machinery goes in `## Files`, or in a final appendix division, and never at the front. This is the base rule (`haipipe-page-draft` §🗂), restated here because this type walks into it by construction.

**Group by result family, or by topic.** `Scaling holds to 5M` and `Where it breaks` are divisions. Script-run order, config order, and the order the runs happened are accidents of history, and an outline that follows one reads as a log.

**One estimand per division**, so no single display has to pool two things that must not be compared.

**⛔ A NEW RUN IS NOT A NEW DIVISION.** Ruled 260821, on a page whose job
holds a twelve-job programme with more models still to come. A task page's
subject regenerates, so the pressure to grow it is constant and it always
arrives in the same shape: a run finishes, and the obvious move is to append a
`Result` division for it. Do that twelve times and the page is the run log this
contract already forbids, wearing correct role prefixes.

The two axes are different, and the contract already owns both:

```text
  a new RUN      ─▶  a new ROW in the Conclusion's READING record,
                     naming its own verdict-run, ⬜ unread
                     the page grows DOWN a table that was built to grow

  a new MESSAGE  ─▶  a new Result division
                     and only when the thing learned is not already
                     said by a division that exists
```

Twelve runs may produce three messages, and then the page has three `Result`
divisions and twelve READING rows. The test is not "did something run" but
**"can an existing division absorb this without its title becoming a lie?"** If
the title still holds, the run is a row and its number joins that division. If
the title would have to change, that is the signal a division was earned.

This is also what makes the page survive the work outlasting one sitting. The
READING record is the resumable surface: any later session opens the page, reads
which rows are ⬜, and knows where to start without reconstructing the argument.

**Why the TASK exists** is written twice and they are not the same sentence: `## Opening` orients — what this page is and why a reader should care — and `### 1 · Introduction` argues — what the folder was run to settle, what was already established, and what this report claims. Before 260822 only the first existed on a FLAT page, which is why a reader met the finding before meeting the question. **Why a TOPIC exists** is substance, and on a NESTED page it gets the topic-level `Introduction` paragraph.

## 📋 The outline DRAFT hands over

⛔ **THE OUTLINE IS NEVER WRITTEN INTO `## Content`** (JL 260817: "we should not have the outline here, we will have it in the outline plugin"). The 🧭 outline plugin DERIVES it from the `###` headings, the Aims and the States, on every open, storing nothing. A copy pasted into the body is a second authority that goes stale at the next edit, and on `QC1-visitlbp` it also dragged an HTML comment and a `verbatim` block into the generated `.tex`.

The table below is what the 🧭 tab SHOWS a person before prose is written. It is the shape to read, not the shape to type:



```text
###   division                            what the reader learns    evidence owed
──────────────────────────────────────────────────────────────────────────────────
 1 ·  Introduction · What this folder was   why anyone should read   ─ none ─
                run to settle               the four rows below
 2 ·  Data    · Four cohort numbers,       the number is not one    🔢 value
                and none of them match
 3 ·  Method  · Why Bonferroni makes       the test choice is the   🔢 value
                19 of 19 mean something    reason the result counts
 4 ·  Result  · 19 of 19 significant,      the headline + its one   🔢 value · 🖼 table
                and the two that are not   negative result
 5 ·  Conclusion · The verdict, and the       what it all bought       ✅ human, at CHECK
                run that settles the rest
```

That example is `QC1-descriptive-stats.md` re-titled, with the `Introduction` row added by the 0.9.0 ruling — the real page has four divisions, and the row above is what it would owe today: a real page with `page-type: task`, `job: tasks/B01_descriptive_analysis/01_descriptive_stats`, sitting at `🟡 RESULTS IN, UNREAD`.

## 🔗 The ROLE is shared, the TITLE is free

Two task pages must be comparable without being identical, and the thirteen real pages already solved this. Under each `### <n> ·` heading they write a bold line, and that line has TWO HALVES joined by a colon:

```text
  **What went in: and the number that is not the same as anyone else's.**
    ╰── SHARED ──╯  ╰──────── THIS PAGE'S OWN ────────╯
        the role         the fact only this page has

  **What went in: and why it is the smallest cohort in the project.**
  **Who is actually in the cohort: and the number that disagrees with its siblings.**
```

The left half repeats word for word across all thirteen pages, which is what makes them one kind. The right half is different on every page, which is what makes each one worth reading. **Unify the ROLE, never the title.**

**The role is a FIXED WORD AT THE FRONT OF THE HEADING, not a separate field** (JL 260816). The base already gives every heading a two-part grammar: whatever sits before the first ` · ` becomes the address chip a reader sees and clicks (`QPs1` §0.6, `⚙️ Engines · what RUNS this subject` shows `Engines`). A task page fills that first part from a closed set, so the role is visible without a lookup and cannot drift from the heading, which a separate `role:` line could.

```text
### <n> · Result · Which traits track the rating, and which barely do
         ╰FIXED╯   ╰──────────── FREE, this page's own ────────────╯
         the chip         what the reader learns here
```

**The closed prefix set, in the fixed order.** Seven words, from a set that grows only by ruling:

```text
prefix       answers                                required?   where it may sit
──────────────────────────────────────────────────────────────────────────────────
Introduction the question this folder was run to    optional    either shape,
             answer, what was already established,              and when present
             and what this report will claim                    it is division 1
Concept      what the terms MEAN                    optional    either shape
             (what ipsatization is · what SPS is)
Landscape    what the FIELD already established,    optional    either shape
             and where this work sits against it                repeatable
Data         what went in, and the fact about it    optional    either shape
             a reader must know
Method       what was actually run, and what it     optional    either shape
             was run INSTEAD OF                                 repeatable
Result       what came out                          ⭐ REQUIRED  either shape
                                                                repeatable
Conclusion   what it means, and what to run next    🔒 exactly 1 the LAST division,
                                                                PAGE level, never
                                                                inside a topic
──────────────────────────────────────────────────────────────────────────────────
(Runs)       ─ deleted, into ## Files ─
(Why)        ─ renamed Introduction 260822, see below ─
```

`Concept` was added on 260816 and earns its place from JL's own standing rule, define every term the first time, and a task page is full of terms a reader has never met (SPS, ADI, ipsatization).

**`Why` became `Introduction`, and it moved INTO the flat shape** (ruled 260822 by JL: "I think we should have an Introduction"). `Why` was topic-level only, on the argument that a single-topic page states its why in its `Opening`, so a FLAT page had no place to say why it exists. That argument conflated two different things, and every paper in existence keeps them apart:

```text
  ## Opening            the ABSTRACT. One paragraph, ABOVE ## Content.
                        what this page IS, and why a reader should care.
                        Fixed by the base frame; unchanged by this ruling.

  ### 1 · Introduction  the report's FIRST DIVISION, INSIDE ## Content.
                        the question this folder was run to answer,
                        what was already established before it ran,
                        and what this report will claim.
```

A reader who can find an abstract can find an introduction, and nobody confuses the two. What the old rule cost was concrete: a FLAT task page — the common shape — had six of the six words available and used five, and the one it could never use was the one that tells the reader what the work was FOR. `Introduction` is optional like every word but `Result`, and when a page writes one it is division 1, because an introduction that is not first is not an introduction.

**`Landscape`, added 260822 by JL ruling** ("这 concept 可不可以加一些，比如说 related work 呢？相当于放一些 literature review 的东西"), holding what a report establishes about the FIELD rather than about its own runs.

- **Why the set needed a seventh word at all.** External-evidence claims had nowhere legal to live. On `QC1-postrain-replication` two `route: discovery` probe cards — at what scale each framework has been demonstrated, and which organizations are documented as using one — served a division titled `Method · Both frameworks`, under a bullet whose own head reads `Two Claims That Rest On READMEs`. `Method` is defined four rows above as what was RUN and what it was run INSTEAD OF; a literature claim is neither, so the cards were filed under a word that excludes them.
- **Why one word and not `Related Work`.** This same set rejected `So what` on 260816 for being two words: it widens the chip and makes the checker's grep awkward. That precedent stands, so the seventh word had to be one word doing the job of two.
- **Why `Landscape` and not `Background`.** `Background` is the more familiar word and loses on the one thing that matters here: in ordinary use it covers the vocabulary AND the prior art, which is exactly the blur this set spent a word separating. `Landscape` cannot be confused with `Concept`, and it is already this repo's word for the same object one layer down — the discovery family writes `landscape.md` from a `landscape_review`, and a task page's `Landscape` division is written FROM those files. Two layers, one word, no translation.
- **Why it repeats.** A page may map more than one field — the frameworks and the methods are different landscapes — and the argument for repeating `Method` and `Result` applies unchanged.
- Rejected with it: `Prior` (one word, but grammatically incomplete as a chip: *prior what?*) and `Context` (vague, and it collides with `Introduction`).

**A topic with no `Result` is not a topic.** Everything else is optional, because a topic that reused the page's cohort owes no `Data` and a topic with no fork owes no `Method`.

**Why the core four are `Data` / `Method` / `Result` / `Conclusion` and not `Task-Input` / `Task-Method` / `Task-Output` / `Task-Meaning`** (the first draft, JL 260816, revised the same session):

- **No `Task-` prefix.** `QPs1` §0.6 already ruled the identical case: the page id drops off the front of a chip "because the tab and the breadcrumb already say which page you are on". The page type says `task` in its own head key, so repeating it on every chip costs width and buys nothing.
- **`Data` and `Result`, not `Input` and `Output`.** Input and output are the pipeline's words, and this same contract forbids the pipeline's words at division level twelve lines above. `Result` also matches the term already used here, RESULT FAMILY.
- **`Method`, and it records the CHOICE, not the steps.** `Why` was tried first and is too narrow: of the thirteen real Method divisions, six are titled `Why X and not Y` but five state what was actually run (`Three tests, three questions`, `Residualize, then recompute, rather than adding a control term`), and a regression's specification is not a "why". What all thirteen DO share is a FORK: every title names something that could have gone another way, marked by `and not`, `rather than`, or `deliberately`. So the division holds the choice and its alternative, never a step list, because the steps are in the code and the code is in `## Files`.
- **`Conclusion`, ruled 260821 by JL, replacing `Meaning`.** The set grows and CHANGES only by ruling, so the swap is recorded here rather than applied silently. `Meaning` was chosen on 260816 because the heading itself stated the closing rule: the page closes when someone says what the result MEANS, and a division named for the reader's takeaway beats one named for the act of reading, which is why it had replaced `Reading`. What that argument missed is that the reader already owns a name for this division. A task page IS a technical report (§📰), a report's last division has been called `Conclusion` for as long as there have been reports, and `Meaning` asks a reader to learn a local word for a section they can already find blindfolded.
- `Conclusion` clears every bar the 260816 rejections set: one word, not rare, not idiom, and the checker's grep stays a plain alternation. It was never considered then, which is why it did not win then.
- ⚠️ **What the rename gives up, and how it is paid back.** `Meaning` carried a demand inside the word: a division named for meaning cannot be filled with a restatement of the divisions above it. `Conclusion` is the softer word and invites exactly that summary. The demand therefore moves out of the name and into a rule: **a `Conclusion` division with no READING record in it is not written yet.** The closing rule below is unchanged; this line is what stops the word from loosening it.
- Rejected 260816 and still rejected: `So what` reads best of all for a weak English reader and loses on being two words, which widens the chip and makes the checker's grep awkward. `Verdict` and `Takeaway` are rarer words, and `Takeaway` is idiom.

## 🪆 Two shapes, and the one-line test that picks between them

A task page has one topic or several, and the seven words sit at a different level in each case (JL 260816). Both shapes are legal; forcing either one is the defect.

**FLAT · one topic.** The words ARE the divisions.

```text
  ### 1 · Introduction · What this folder was run to settle, and what it claims
  ### 2 · Data    · Who is in the cohort, and the number that disagrees
  ### 3 · Method  · Bonferroni across the whole family, not per test
  ### 4 · Result  · 19 of 19 significant, and the two that are not
  ### 5 · Conclusion · The verdict, and the run that settles the rest
```

**FLAT DOES NOT MEAN ONE OF EACH.** Ruled 260821 by JL, writing a report whose
shape a reader already owns: Introduction, Method 1..n, Result 1..n, Conclusion.
The closed set fixes the ORDER of the words and the position of `Conclusion`. It
never fixed their MULTIPLICITY, and the earlier text implying "Result repeats,
everything else appears once" was describing the one example in front of it.

```text
  ###  1 · Introduction · <free>  first when written, exactly one
  ###  2 · Concept · <free>     page-level, shared by every division below
  ###  3 · Landscape · <free>   what the field already established
  ###  4 · Data    · <free>
  ###  5 · Method  · <free>     Method 1
  ###  6 · Method  · <free>     Method 2      ← legal, and usually clearer than
  ###  7 · Method  · <free>     Method 3        one Method with #### beneath it
  ###  8 · Result  · <free>     Result 1
  ###  9 · Result  · <free>     Result 2
  ### 10 · Result  · <free>     what is still not settled  (the residual)
  ### 11 · Conclusion · <free>  page-level, last, exactly one
```

`Concept`, `Landscape` and `Data` may sit at `###` in a FLAT page for the same
reason they may in a NESTED one: they are page-level, shared by everything below,
and the only alternative is to define a term, or place the work against its field,
inside the first division that happens to need it.

`Introduction` is FLAT-legal since 260822 and is division 1 whenever it is
written. It does not repeat: a page with two introductions has none.

**The distinction that still matters** is not how many divisions carry a word, it
is whether a second topic needs its OWN `Data` or its OWN `Method`. If it does,
the shape is NESTED and the pairing has to survive; if it does not, repeating the
word at `###` is a flat report with several methods and several findings, which
is what most task pages are.

**The checker's FLAT line therefore admits `Introduction`, `Concept` and
`Landscape` at `###`:**
`^### \d+ · (Introduction|Concept|Landscape|Data|Method|Result|Conclusion) · `

**NESTED · several topics.** A TOPIC is the division, and the words become its `####` paragraphs, numbered by the base's own depth grammar (`QPs1`: `### 3` is a division, `#### 3.2.1` is a paragraph, and the depth of the number says a group exists).

```text
  ### 1 · Main OLS: does the association hold at all
  #### 1.1 · Introduction · why the pooled estimate comes first
  #### 1.2 · Concept · what SPS is, and what it is read out of
  #### 1.3 · Data    · the 83,230 with all ten scores
  #### 1.4 · Method  · joint OLS over ten traits, not ten separate correlations
  #### 1.5 · Result  · the standardized betas, largest first

  ### 2 · IV: what identification buys, and what it costs
  #### 2.1 · Introduction · why the pooled estimate is not enough
  #### 2.3 · Data    · the smaller instrument-eligible subsample  ← its OWN
  #### 2.4 · Method  · the instrument, and the one it was chosen over
  #### 2.5 · Result  · the second stage, and the first-stage F

  ### 3 · Conclusion · The verdict per topic, and what to run next
```

**Why NESTED exists at all.** In FLAT, `Data` and `Method` appear once at the top, so a page whose IV runs on a different subsample than its main OLS cannot pair each result with the sample and spec that produced it. `2.3 · Data` above is the whole point: the pairing survives. A reader also gets to read one topic end to end instead of reading every `Data` and then every `Method`.

**📐 The test, and it is one question:**

```text
  "Does a second topic need its OWN Data or its OWN Method?"

     no  ──▶  FLAT.   Result repeats, everything else appears once.
    yes  ──▶  NESTED. One division per topic.

  🚫 One topic forced into NESTED is six headings describing one regression.
```

**🔒 `Conclusion` NEVER goes inside a topic, in either shape.** It is always the last `###` division, exactly one per page. Per-topic readings would break the closing rule outright: with three topics read and two not, nothing could say whether the PAGE is closed. One record holds them all, one row per topic, each row naming its own run:

```text
  ### n · Conclusion · The verdict per topic, and what to run next

  READING · <date> · <who read it>
  Main OLS   verdict-run run_main   ✅ read · <what it means>
  IV         verdict-run run_iv     ⬜ unread
  DID        verdict-run run_did    ⬜ unread
  next run   <the run that would settle IV, or "none: the question is dead">
```

The page closes when every row is read. A rerun of ANY named run re-opens the page and un-reads that row alone.

**A NESTED page may put a word at `###` level when it is PAGE-level** (found 260817 by running this contract on two real pages). `Concept` and `Data` are shared by every topic as often as they are owned by one: a page defining `mme_ttl` once, or stating one 765,701-row sample every specification uses, would otherwise have to repeat the definition inside each topic or hide it in the Opening.

```text
  ### 1 · Concept · <free>       page-level · shared by every topic below
  ### 2 · Data    · <free>       page-level · every topic uses this sample
  ### 3 · <free topic title>     a topic
  #### 3.1 · Method · <free>       its own
  #### 3.2 · Result · <free>       its own
  ### 4 · <free topic title>     another topic
  #### 4.2 · Data   · <free>       ← a topic MAY still own one, and then
  #### 4.3 · Method · <free>         §2's page-level Data does not apply to it
  ### n · Conclusion · <free>       page-level, always, always last
```

A topic-level `Data` OVERRIDES the page-level one for that topic, and a topic that owns one says so. On a NESTED page `Introduction` may sit at BOTH levels and they answer different questions: the page-level one says what the folder was run to settle, a topic-level one says why that topic is here rather than folded into its neighbour.

**The checker greps at both levels**, and any other word before the first ` · ` is a finding:

```text
  FLAT     ^### \d+ · (Introduction|Concept|Landscape|Data|Method|Result|Conclusion) · 
  NESTED   ^### \d+ · (Introduction|Concept|Landscape|Data|Conclusion) · │ ^### \d+ · .+
           ^#### \d+\.\d+ · (Introduction|Concept|Landscape|Data|Method|Result) · 
  BOTH     the LAST ### is Conclusion, and Conclusion appears once
           Introduction, when present, is the FIRST ### and appears once
```

⛔ **AN EVIDENCE ENTRY IS A CARD, NOT A SENTENCE.** The `evidence owed` column above is the 🧭 tab's; the CARD is the file on disk and the 🚪 Probe tab is where a person reads it. A body sentence like `Evidence owed: probe/PP03-regression-n-gap, state raised.` is the defect: it duplicates a card that already renders, and it carries a `state:` the card owns, so the two disagree the moment the card moves. The page's prose cites a card by its bare id and says nothing about its state.

🚨 **A DECLARED ARTIFACT THAT DOES NOT EXIST IS THE WORST CASE OF THIS.** On `QC1-visitlbp` the outline declared `🖼 display` for one division and the page shipped with ZERO display unit folders: the sentence was the entire deliverable. Before a phase reports done, count them:

```text
  declared in the outline        exists on disk               verdict
  ──────────────────────────────────────────────────────────────────────
  🔢 4 value cards               4 × probe/PP<NN>-…/card.md   ✅ done
  🖼 1 display                   0 × display/<stem>-Display…/  🚨 NOT done
```

A division that needs a display and has no numbers yet writes NO display row at all, and says in one sentence that there is nothing to draw. Owing a thing and pretending to owe it are different, and only the first is honest.

**What `Method` holds, by kind of task.** The word is the same on every task page; what fills it is not. Each row below is taken from one of the thirteen real pages:

```text
task kind      Method holds                          the real page
──────────────────────────────────────────────────────────────────────────────
regression     which model, which controls, which    QD4 · joint OLS over all ten
               correction, and what it was run       traits, not ten separate
               INSTEAD OF                            per-trait correlations
clustering     k, the distance, and why not the      QC4 · k-means on five traits,
               other k                                not on ten
descriptive    which tests, which multiple-          QC1 · t-test + chi-square,
               comparison correction                  Bonferroni across the family
transform      the operation, and the simpler one    QC8 · ipsatization, "and not
               it was chosen over                     something easier"
code/builder   what the script DECIDES versus what   QB5 · "if the numbers are
               is hard-coded                          fixed, what does it do?"
data           the filter, the join, and why this    QD4 · requiring all ten scores
               cohort and not the larger one          drops the sample to 83,230
```

## 🃏 The four evidence cards, and which division owes which

`haipipe-page-evidence` ships THREE card kinds, and `probe` is not a fourth one: the value card LIVES in the probe lane, at `<page>/probe/PP<NN>-<slug>/card.md`. Probe is the folder, value is the kind, and they are one card.

A task page needs a fourth kind that genuinely does not exist yet: **the CODE card**, which binds a claim to the job that produced it (JL 260816, "when I say the method, I mean link it to the job"). A `Method` division saying `k-means on five traits and not on ten` is unbacked prose until something on disk points at the script that ran the k-means.

```text
kind          the card on disk                          BINDS TO                 GATE 🧑
────────────────────────────────────────────────────────────────────────────────────────
📚 citation   <page>/bibex/<stem>.bib entry             a published work         verified
🔢 value      <page>/probe/PP<NN>-<slug>/card.md        a QA file in the bank    state: bound
🖼 display    <page>/display/<stem>-Display<N>-…        a frozen intake +        accepted: ✅
                                                        its named renderer
💻 code  ⭐   <page>/code/CD<NN>-<slug>/card.md          the JOB,                 state: pinned
              ⭐ NEW for this type                        by path + commit
```

The code card's body is the four sister files and the fork the `Method` division claims:

```text
CD01-kmeans-five-traits
  script     tasks/B01_descriptive_analysis/04_clustering/04_clustering.py
  config     configs/run_k5.yaml
  run        runs/run_k5.sh
  notebook   notebooks/run_k5.ipynb
  commit     <sha of the job at the run>
  fork       k-means on FIVE traits · instead of ten, because EmotionStability
             covers 68.4% and requiring ten drops most of the sample
  state      pinned
```

(The same card on a NESTED job carries the task segment throughout:
`script t01_clustering/clustering.py · config t01_clustering/config/r05_k5.yaml ·
run t01_clustering/runs/r05_k5.sh · notebook notebooks/t01_clustering/r05_k5.ipynb`.)

⚠️ **A code card goes STALE the way a value card does.** When the script changes under a pinned commit, the `Method` division's claim is no longer backed, exactly as a rerun un-backs the `Conclusion` verdict. The two staleness rules are the same rule at two grains, and they are why a task page is re-openable by disk at all.

**⛔ This type does NOT assign card kinds to division names.** Any division may owe any card: a `Result` may owe a 📚 citation when it is compared against a published benchmark, a `Data` may owe a 🖼 display when the cohort needs a flow diagram, a `Method` may owe a 🔢 value when the parameter it chose came out of a sweep. Fixing a kind per division would repeat this contract's own worst version, the five hardcoded divisions of 0.1.0, one level down: it would make DRAFT's `evidence owed` column decoration, since the answer would already be written here.

It also breaks on real tasks. `ref/task-structure.md` §"Skill-Runner Jobs (Exemption)" exempts a whole class of job from having any `*.py` at all, so a `Method` division on one of those has no script to pin and a required 💻 code card would be unfillable by construction.

**WHO decides: DRAFT, per division, per page.** The `evidence owed` column of the outline is where it is written, and that column is the reason the outline is shown to a person before prose.

**What IS fixed, and it is one line:** the `Conclusion` division owes no card. Its evidence is the divisions above it plus a human judgment, which follows from the closing rule and needs no separate ruling.

The table below is what usually happens on the thirteen real pages. It is a HINT for DRAFT, never a rule, and a page that departs from it is not a finding:

```text
division    usually owes                              because
──────────────────────────────────────────────────────────────────────────────
Data        🔢 value                                  the cohort n is a number
Method      💻 code                                   the fork points at the
                                                      script that took it
Result      🔢 value · 🖼 display                     the numbers and what draws
                                                      them
Conclusion     ─ none ─   🔒 THE FIXED ONE                a person, at CHECK
```

⬜ **This fourth kind probably belongs upstream, not here.** Any page arguing from code needs it, not only a task page: a paper's methods section has the same hole. Promoting `💻 code` into `haipipe-page-evidence` alongside the other three is the right home, and it is not done, because that contract is being edited in another session right now. Until it moves, this type owns the card and the checker greps for it here.

⚠️ **A Method division with no fork in it has not been written yet.** All thirteen real titles name something that could have gone another way, and they mark it with `and not`, `rather than`, or `deliberately`. `Plain description, deliberately: no model, no test` is a fork too: the choice was to run nothing. A title reading `How it works: the steps, in the order the script runs them` is the boilerplate all thirteen pages carry above their real title, and it is the thing to delete.

Two task pages stay COMPARABLE because the prefix column is identical on both and its order is fixed. They stay READABLE because no two titles after the ` · ` are the same. That is the whole trade, and it needs no second field to hold it.

**A shared half with an EMPTY right half is the defect to look for.** Thirteen out of thirteen pages write `What came out: each number anchored to the file that holds it` and nothing more, so thirteen result divisions carry a role and say nothing. `QC1` and `QD4` show what the filled version looks like: `Which traits track the rating, and which barely do`. A role with no fact after the colon is a heading nobody wrote yet.

DRAFT's job on a task page is therefore mostly PROMOTION, not invention: take the right half of the bold line, make it the `###` heading, and keep the left half as the role.

**`Inputs` SURVIVES when it carries a finding, and it usually does.** The earlier rule here said `Inputs` is machinery and must go. That was ruled without reading the real pages, and it is wrong: on `QC1` the sample division holds the four-cohort-number problem, and on `QD4` it holds the two-sample-size split. Both are findings a reader needs. What was wrong was the HEADING, never the material.

**`Runs` does NOT survive, and the pages prove it.** On `QC1` it is one line. On `QD4` its only finding, an `INDEX.md` naming a run script that does not exist, is already written in `## States` as `A5.2`. A division that repeats States and Files is not a division.

**`Inputs` SURVIVES when it carries a finding, and it usually does.** The earlier rule here said `Inputs` is machinery and must go. That was ruled without reading the real pages, and it is wrong: on `QC1` the Inputs division holds the four-cohort-number problem, and on `QD4` it holds the two-sample-size split. Both are findings a reader needs. What was wrong was the HEADING, never the material.

**`Runs` does NOT survive, and the pages prove it.** On `QC1` it is one line. On `QD4` its only finding, an `INDEX.md` naming a run script that does not exist, is already written in `## States` as `A5.2`. A division that repeats States and Files is not a division.

The evidence column uses the three kinds `haipipe-page-evidence` owns: 📚 citation · 🔢 value · 🖼 display. On a task page almost every row is 🔢 value, because the job's own runs are what produce them, and each 🔢 names the run under rule ② below. A division with a blank evidence column is a division nobody can finish. The `Conclusion` row is the exception: its evidence is the numbers the rows above already landed, and the hand that fills it is human.

**The run table is not a division.** The `<NAME>` token binding the four sister files (`ref/authoring-conventions.md` §1) — `configs/<NAME>.yaml`, `runs/<NAME>.sh`, `results/<NAME>/`, `notebooks/<NAME>.ipynb` — is what makes rule ② checkable, and it lives in `## Files` where a reader looks for machinery.

## ⛓ Four binding rules

**① BY PATH, never by copy.** No code dump, no pasted data table, no inlined figure. `results/` regenerates on every run, so a copied number goes stale in silence and the page keeps asserting it. Name the file and, where a reader needs a size, carry a fingerprint instead: row count, date range, cohort n.

**② Every shown number names its run.** A number on this page that names no run is a defect OF THIS PAGE, even when the number is correct. This is the display type's provenance rule applied one layer down, and the failure it prevents is the same one: a figure asserts without a sentence, and a table asserts without a run.

**③ A rerun re-opens.** Stated above; restated here because it is the rule an automatic loop reaches by another door. A machine may refresh any result-family division's numbers from disk, since those are read from `results/<NAME>/`. **No machine writes the final `Conclusion` division, and no machine moves `state:` to ✅**, for the same reason a machine may not accept a render: what it judges is whether a number answers a question, and a cold read of the markdown never reaches that.

(This rule named `### 3 · Runs`, `### 4 · Results`, and `### 5 · Reading` by number until 0.2.0 stopped fixing them. Only `Conclusion` is fixed now, and it is fixed by POSITION — the last division — not by a number, because DRAFT decides how many result families come before it.)

**④ One authority each, between the page and `QA/`.** These two look alike and must not drift:

```
QA/<n>-<slug>.md   ONE outside caller's question · write-once · lives IN the folder
                   contract: haipipe-task/fn/qa.md · this layer holds the pen
the page           the task's OWN standing reading · edited over rounds · on the board
```

🚫 Never copy QA prose onto the page, and never edit a QA file from the page. `## Files` lists them by path, and that is the whole relationship. A question that arrives from outside is answered in a QA file; the reading the page carries is the one the task took of itself.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QPs1` §7). A task page is the one variant whose companion folder ALREADY EXISTS: it declares `job:` in its head rather than generating a folder of its own.

```text
 📥 INPUT   tasks/bNN_<block>/jNN_<job>/<task>/   ✍️ authored elsewhere, by the task layer
              code + config/ + runs/               what ran (flat: *.py · configs/ · runs/;
                                                   nested 260830: <task>/config/ · <task>/runs/)
              results/<run>/ · notebooks/<run>/    what came out (nested: results/<task>/<run>/)
              plan.yaml · report.yaml              intent and record
              QA/<n>-<slug>.md                     digests written for outside callers

 📤 OUTPUT  the READING · a verdict bound to one run name, plus the States
            rows saying which of this task's questions are now answered
```

⚠️ **`diagram/*.txt` inside a job is the shape this page replaces.** `ref/task-structure.md` §"Job-level diagram/" already specifies `01-overview.txt` (what/why/inputs/outputs), `02-design.txt` (the approach), `03-runs.txt` (the run table), and `04-progress.txt` (a dated log): divisions 1, 2 and 3 plus `## Log`, in four .txt files that nothing renders and nobody opens. A task with a page does not keep both. **Open ruling for JL**: the page absorbs `diagram/`, or `diagram/` stays as the source the page renders from. Until it is ruled, a task page names the .txt files in `## Files` and does not duplicate their prose.

## 📂 Files

```
haipipe-page-for-task/
├── SKILL.md            this variant contract
├── template.md         copy it to write one task page · RULE comments deleted as satisfied
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the folder this page mirrors is specified by `haipipe-task/ref/task-structure.md`; the write-once digest boundary is `haipipe-task/fn/qa.md`; the provenance rule is borrowed from `haipipe-page-for-display`, which this contract names but never contains.
