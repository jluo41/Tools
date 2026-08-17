---
name: haipipe-page-for-task
description: >-
  The VARIANT contract for a TASK Page: one page per task-folder, reading what that folder produced and carrying the one thing no file in it can hold, the READING of the result. It loads haipipe-page for the base frame and adds only what a task page needs: the closing rule that a person must read the numbers against the task's own question, the verdict bound to one run name so a rerun RE-OPENS the page, a Content shape whose divisions each open with one word from the closed set Why, Concept, Data, Method, Result, Meaning in one of two shapes, FLAT when the page has one topic and NESTED with one division per topic when a second topic needs its own Data or Method, with Meaning always the single last division, the outline with its evidence column that DRAFT hands over before prose, and the rule that every shown number names the run that produced it. Use when writing or fixing a task page, when results exist but nobody wrote what they mean, when a number on a page traces to no run, when a page's divisions have copied the task-folder's own directory names, or when a task closed green while its own question stayed unanswered. Trigger: task page, task folder page, results reading, verdict, verdict-run, rerun reopens, result family, page-type task, /haipipe-page-for-task.
metadata:
  version: "0.5.0"
  last_updated: "2026-08-16"
  summary: "Closing rule: a task page closes when the result is READ and each reading names the run it is bound to; a rerun re-opens it. 0.5.0 adds the FLAT/NESTED fork so one page can carry several topics, each with its own Data and Method, while Meaning stays one page-level division, always last."
  outline:
    mode: grammar          # fixed | grammar | resolved
    source: "this SKILL.md"
    shape: "FLAT or NESTED; first word from {Why, Concept, Data, Method, Result, Meaning}; Meaning is one page-level division, always last"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-task · the folder ran, and someone has to say what it means

**LOAD `haipipe-page` FIRST.** It owns the base frame. What this file guards is READING: a task-folder can produce a correct number and answer nothing, and no file inside that folder is allowed to say so.

**The kind this variant covers**: one page per TASK-FOLDER.

```
kind      subject                              closes when
──────────────────────────────────────────────────────────────────────
Task      ONE task-folder: inputs · code ·     a person READS the result against
          runs · results                        the task's own question, and the
                                                reading names the run it is bound to
```

**The type key.** A task page declares `page-type: task` in its frontmatter, and the line is REQUIRED: a task page wears whatever name its task-folder has (`A01.01`, `B4_fit_scaling_law`, `C3-Visual-ForecastScaling`), and 31% of real task-folders do not match the `{NN}_<name>` convention at all, so no filename shape can mark one. The `page-type:` key beats the filename (base, type resolution step ③).

## 📕 What the task-folder already holds, and what it can never hold

Every one of these already exists on disk before a page is written, so the page must not re-hold any of them:

```
plan.yaml            what was intended        report.yaml   what ran
results/<run>/       the numbers              notebooks/    what happened
configs/ · runs/     how it was invoked       QA/<n>-<slug>.md  one caller's
                                                              question, write-once
```

Not one of them ever says **"and therefore ___"**. `metrics.json` holds `0.83`; nothing on disk holds "0.83 means the approach works" or "0.83 is the same as the baseline, so this direction is dead". That sentence is a human judgment about an empirical result, it is what everyone downstream actually needs, and it is the only thing this page exists to carry.

## 🏁 The closing rule, and why a rerun re-opens the page

A task page closes on one typed record in its LAST division, `Meaning`, and nothing else closes it:

```
READING · <date> · <who read it>
<topic>   verdict-run <run>   ✅ read · <what it means, in plain words>
<topic>   verdict-run <run>   ⬜ unread
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
  ### n · Meaning · <free>   exactly 1, ALWAYS LAST, in BOTH shapes
Aims         one Aim per question this task must answer
States       per question: answered · needs another run · dropped
Files        the task-folder paths, including every QA/<n>-<slug>.md
```

**⛔ A division names what the READER LEARNS, never where the material came from.** `Inputs`, `Runs`, `Provenance` and `Run receipts` are MACHINERY, and a task page is the single most likely page in the system to lead with them, because its subject IS a folder and the folder's own names are sitting right there. Copying `configs/ runs/ results/` into `### 1 · Inputs`, `### 2 · Steps`, `### 3 · Runs` hands the reader the author's filing system instead of the finding. The machinery goes in `## Files`, or in a final appendix division, and never at the front. This is the base rule (`haipipe-page-draft` §🗂), restated here because this type walks into it by construction.

**Group by result family, or by topic.** `Scaling holds to 5M` and `Where it breaks` are divisions. Script-run order, config order, and the order the runs happened are accidents of history, and an outline that follows one reads as a log.

**One estimand per division**, so no single display has to pool two things that must not be compared.

**Why the TASK exists** is orientation and belongs in Opening, in both shapes. **Why a TOPIC exists** is substance, and on a NESTED page it gets the topic-level `Why` paragraph; on a FLAT page there is only one topic, so the Opening already said it and no `Why` division is written.

## 📋 The outline DRAFT hands over

⛔ **THE OUTLINE IS NEVER WRITTEN INTO `## Content`** (JL 260817: "we should not have the outline here, we will have it in the outline plugin"). The 🧭 outline plugin DERIVES it from the `###` headings, the Aims and the States, on every open, storing nothing. A copy pasted into the body is a second authority that goes stale at the next edit, and on `QC1-visitlbp` it also dragged an HTML comment and a `verbatim` block into the generated `.tex`.

The table below is what the 🧭 tab SHOWS a person before prose is written. It is the shape to read, not the shape to type:



```text
###   division                            what the reader learns    evidence owed
──────────────────────────────────────────────────────────────────────────────────
 1 ·  Data    · Four cohort numbers,       the number is not one    🔢 value
                and none of them match
 2 ·  Method  · Why Bonferroni makes       the test choice is the   🔢 value
                19 of 19 mean something    reason the result counts
 3 ·  Result  · 19 of 19 significant,      the headline + its one   🔢 value · 🖼 table
                and the two that are not   negative result
 4 ·  Meaning · The verdict, and the       what it all bought       ✅ human, at CHECK
                run that settles the rest
```

That example is not invented. It is `QC1-descriptive-stats.md` re-titled: a real page with `page-type: task`, `task-folder: tasks/B01_descriptive_analysis/01_descriptive_stats`, sitting at `🟡 RESULTS IN, UNREAD`.

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

**The closed prefix set, in the fixed order.** Six words, from a set that grows only by ruling:

```text
prefix     answers                                  required?   where it may sit
──────────────────────────────────────────────────────────────────────────────────
Why        why do this topic AT ALL                 optional    topic-level only
           (why run an IV at all)
Concept    what the terms MEAN                      optional    topic-level only
           (what ipsatization is · what SPS is)
Data       what went in, and the fact about it      optional    either shape
           a reader must know
Method     what was actually run, and what it       optional    either shape
           was run INSTEAD OF
Result     what came out                            ⭐ REQUIRED  either shape
Meaning    what it means, and what to run next      🔒 exactly 1 the LAST division,
                                                                 PAGE level, never
                                                                 inside a topic
──────────────────────────────────────────────────────────────────────────────────
(Runs)     ─ deleted, into ## Files ─
```

`Why` and `Concept` were added on 260816 with the nested shape and only make sense there: a single-topic page states why it exists in its Opening, and a term it uses once is defined inline. `Concept` earns its place from JL's own standing rule, define every term the first time, and a task page is full of terms a reader has never met (SPS, ADI, ipsatization).

**A topic with no `Result` is not a topic.** Everything else is optional, because a topic that reused the page's cohort owes no `Data` and a topic with no fork owes no `Method`.

**Why these four words and not `Task-Input` / `Task-Method` / `Task-Output` / `Task-Meaning`** (the first draft, JL 260816, revised the same session):

- **No `Task-` prefix.** `QPs1` §0.6 already ruled the identical case: the page id drops off the front of a chip "because the tab and the breadcrumb already say which page you are on". The page type says `task` in its own head key, so repeating it on every chip costs width and buys nothing.
- **`Data` and `Result`, not `Input` and `Output`.** Input and output are the pipeline's words, and this same contract forbids the pipeline's words at division level twelve lines above. `Result` also matches the term already used here, RESULT FAMILY.
- **`Method`, and it records the CHOICE, not the steps.** `Why` was tried first and is too narrow: of the thirteen real Method divisions, six are titled `Why X and not Y` but five state what was actually run (`Three tests, three questions`, `Residualize, then recompute, rather than adding a control term`), and a regression's specification is not a "why". What all thirteen DO share is a FORK: every title names something that could have gone another way, marked by `and not`, `rather than`, or `deliberately`. So the division holds the choice and its alternative, never a step list, because the steps are in the code and the code is in `## Files`.
- **`Meaning` stays**, because it states the closing rule in the heading: the page closes when someone says what the result MEANS. A division named for the reader's takeaway beats one named for the act of reading, which is why this replaces the name `Reading` used elsewhere in this file.
- Rejected: `So what` reads best of all for a weak English reader and loses on being two words, which widens the chip and makes the checker's grep awkward. `Verdict` and `Takeaway` are rarer words, and `Takeaway` is idiom.

## 🪆 Two shapes, and the one-line test that picks between them

A task page has one topic or several, and the six words sit at a different level in each case (JL 260816). Both shapes are legal; forcing either one is the defect.

**FLAT · one topic.** The words ARE the divisions.

```text
  ### 1 · Data    · Who is in the cohort, and the number that disagrees
  ### 2 · Method  · Bonferroni across the whole family, not per test
  ### 3 · Result  · 19 of 19 significant, and the two that are not
  ### 4 · Meaning · The verdict, and the run that settles the rest
```

**NESTED · several topics.** A TOPIC is the division, and the words become its `####` paragraphs, numbered by the base's own depth grammar (`QPs1`: `### 3` is a division, `#### 3.2.1` is a paragraph, and the depth of the number says a group exists).

```text
  ### 1 · Main OLS: does the association hold at all
  #### 1.1 · Why     · why the pooled estimate comes first
  #### 1.2 · Concept · what SPS is, and what it is read out of
  #### 1.3 · Data    · the 83,230 with all ten scores
  #### 1.4 · Method  · joint OLS over ten traits, not ten separate correlations
  #### 1.5 · Result  · the standardized betas, largest first

  ### 2 · IV: what identification buys, and what it costs
  #### 2.1 · Why     · why the pooled estimate is not enough
  #### 2.3 · Data    · the smaller instrument-eligible subsample  ← its OWN
  #### 2.4 · Method  · the instrument, and the one it was chosen over
  #### 2.5 · Result  · the second stage, and the first-stage F

  ### 3 · Meaning · The verdict per topic, and what to run next
```

**Why NESTED exists at all.** In FLAT, `Data` and `Method` appear once at the top, so a page whose IV runs on a different subsample than its main OLS cannot pair each result with the sample and spec that produced it. `2.3 · Data` above is the whole point: the pairing survives. A reader also gets to read one topic end to end instead of reading every `Data` and then every `Method`.

**📐 The test, and it is one question:**

```text
  "Does a second topic need its OWN Data or its OWN Method?"

     no  ──▶  FLAT.   Result repeats, everything else appears once.
    yes  ──▶  NESTED. One division per topic.

  🚫 One topic forced into NESTED is six headings describing one regression.
```

**🔒 `Meaning` NEVER goes inside a topic, in either shape.** It is always the last `###` division, exactly one per page. Per-topic readings would break the closing rule outright: with three topics read and two not, nothing could say whether the PAGE is closed. One record holds them all, one row per topic, each row naming its own run:

```text
  ### n · Meaning · The verdict per topic, and what to run next

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
  ### n · Meaning · <free>       page-level, always, always last
```

A topic-level `Data` OVERRIDES the page-level one for that topic, and a topic that owns one says so. `Why` stays topic-level only, because the page's own why is its Opening.

**The checker greps at both levels**, and any other word before the first ` · ` is a finding:

```text
  FLAT     ^### \d+ · (Data|Method|Result|Meaning) · 
  NESTED   ^### \d+ · (Concept|Data|Meaning) · │ ^### \d+ · .+   word OR free title
           ^#### \d+\.\d+ · (Why|Concept|Data|Method|Result) · 
  BOTH     the LAST ### is Meaning, and Meaning appears once
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

A task page needs a fourth kind that genuinely does not exist yet: **the CODE card**, which binds a claim to the task-folder that produced it (JL 260816, "when I say the method, I mean link it to the task-folder"). A `Method` division saying `k-means on five traits and not on ten` is unbacked prose until something on disk points at the script that ran the k-means.

```text
kind          the card on disk                          BINDS TO                 GATE 🧑
────────────────────────────────────────────────────────────────────────────────────────
📚 citation   <page>/bibex/<stem>.bib entry             a published work         verified
🔢 value      <page>/probe/PP<NN>-<slug>/card.md        a QA file in the bank    state: bound
🖼 display    <page>/display/<stem>-Display<N>-…        a frozen intake +        accepted: ✅
                                                        its named renderer
💻 code  ⭐   <page>/code/CD<NN>-<slug>/card.md          the TASK-FOLDER,        state: pinned
              ⭐ NEW for this type                        by path + commit
```

The code card's body is the four sister files and the fork the `Method` division claims:

```text
CD01-kmeans-five-traits
  script     tasks/B01_descriptive_analysis/04_clustering/04_clustering.py
  config     configs/run_k5.yaml
  run        runs/run_k5.sh
  notebook   notebooks/run_k5.ipynb
  commit     <sha of the task-folder at the run>
  fork       k-means on FIVE traits · instead of ten, because EmotionStability
             covers 68.4% and requiring ten drops most of the sample
  state      pinned
```

⚠️ **A code card goes STALE the way a value card does.** When the script changes under a pinned commit, the `Method` division's claim is no longer backed, exactly as a rerun un-backs the `Meaning` verdict. The two staleness rules are the same rule at two grains, and they are why a task page is re-openable by disk at all.

**⛔ This type does NOT assign card kinds to division names.** Any division may owe any card: a `Result` may owe a 📚 citation when it is compared against a published benchmark, a `Data` may owe a 🖼 display when the cohort needs a flow diagram, a `Method` may owe a 🔢 value when the parameter it chose came out of a sweep. Fixing a kind per division would repeat this contract's own worst version, the five hardcoded divisions of 0.1.0, one level down: it would make DRAFT's `evidence owed` column decoration, since the answer would already be written here.

It also breaks on real tasks. `ref/task-structure.md` §"Skill-Runner Tasks" exempts a whole class of task-folder from having any `*.py` at all, so a `Method` division on one of those has no script to pin and a required 💻 code card would be unfillable by construction.

**WHO decides: DRAFT, per division, per page.** The `evidence owed` column of the outline is where it is written, and that column is the reason the outline is shown to a person before prose.

**What IS fixed, and it is one line:** the `Meaning` division owes no card. Its evidence is the divisions above it plus a human judgment, which follows from the closing rule and needs no separate ruling.

The table below is what usually happens on the thirteen real pages. It is a HINT for DRAFT, never a rule, and a page that departs from it is not a finding:

```text
division    usually owes                              because
──────────────────────────────────────────────────────────────────────────────
Data        🔢 value                                  the cohort n is a number
Method      💻 code                                   the fork points at the
                                                      script that took it
Result      🔢 value · 🖼 display                     the numbers and what draws
                                                      them
Meaning     ─ none ─   🔒 THE FIXED ONE                a person, at CHECK
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

The evidence column uses the three kinds `haipipe-page-evidence` owns: 📚 citation · 🔢 value · 🖼 display. On a task page almost every row is 🔢 value, because the task-folder's own runs are what produce them, and each 🔢 names the run under rule ② below. A division with a blank evidence column is a division nobody can finish. The `Meaning` row is the exception: its evidence is the numbers the rows above already landed, and the hand that fills it is human.

**The run table is not a division.** The `<NAME>` token binding the four sister files (`ref/authoring-conventions.md` §1) — `configs/<NAME>.yaml`, `runs/<NAME>.sh`, `results/<NAME>/`, `notebooks/<NAME>.ipynb` — is what makes rule ② checkable, and it lives in `## Files` where a reader looks for machinery.

## ⛓ Four binding rules

**① BY PATH, never by copy.** No code dump, no pasted data table, no inlined figure. `results/` regenerates on every run, so a copied number goes stale in silence and the page keeps asserting it. Name the file and, where a reader needs a size, carry a fingerprint instead: row count, date range, cohort n.

**② Every shown number names its run.** A number on this page that names no run is a defect OF THIS PAGE, even when the number is correct. This is the display type's provenance rule applied one layer down, and the failure it prevents is the same one: a figure asserts without a sentence, and a table asserts without a run.

**③ A rerun re-opens.** Stated above; restated here because it is the rule an automatic loop reaches by another door. A machine may refresh any result-family division's numbers from disk, since those are read from `results/<NAME>/`. **No machine writes the final `Meaning` division, and no machine moves `state:` to ✅**, for the same reason a machine may not accept a render: what it judges is whether a number answers a question, and a cold read of the markdown never reaches that.

(This rule named `### 3 · Runs`, `### 4 · Results`, and `### 5 · Reading` by number until 0.2.0 stopped fixing them. Only `Meaning` is fixed now, and it is fixed by POSITION — the last division — not by a number, because DRAFT decides how many result families come before it.)

**④ One authority each, between the page and `QA/`.** These two look alike and must not drift:

```
QA/<n>-<slug>.md   ONE outside caller's question · write-once · lives IN the folder
                   contract: haipipe-task/fn/qa.md · this layer holds the pen
the page           the task's OWN standing reading · edited over rounds · on the board
```

🚫 Never copy QA prose onto the page, and never edit a QA file from the page. `## Files` lists them by path, and that is the whole relationship. A question that arrives from outside is answered in a QA file; the reading the page carries is the one the task took of itself.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QPs1` §7). A task page is the one variant whose companion folder ALREADY EXISTS: it declares `task-folder:` in its head rather than generating a folder of its own.

```text
 📥 INPUT   tasks/{G}{NN}_<group>/{NN}_<task>/     ✍️ authored elsewhere, by the task layer
              *.py · configs/ · runs/              what ran
              results/<run>/ · notebooks/<run>/    what came out
              plan.yaml · report.yaml              intent and record
              QA/<n>-<slug>.md                     digests written for outside callers

 📤 OUTPUT  the READING · a verdict bound to one run name, plus the States
            rows saying which of this task's questions are now answered
```

⚠️ **`diagram/*.txt` inside a task-folder is the shape this page replaces.** `ref/task-structure.md` §"Task-level diagram/" already specifies `01-overview.txt` (what/why/inputs/outputs), `02-design.txt` (the approach), `03-runs.txt` (the run table), and `04-progress.txt` (a dated log): divisions 1, 2 and 3 plus `## Log`, in four .txt files that nothing renders and nobody opens. A task with a page does not keep both. **Open ruling for JL**: the page absorbs `diagram/`, or `diagram/` stays as the source the page renders from. Until it is ruled, a task page names the .txt files in `## Files` and does not duplicate their prose.

## 📂 Files

```
haipipe-page-for-task/
├── SKILL.md            this variant contract
├── template.md         copy it to write one task page · RULE comments deleted as satisfied
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the folder this page mirrors is specified by `haipipe-task/ref/task-structure.md`; the write-once digest boundary is `haipipe-task/fn/qa.md`; the provenance rule is borrowed from `haipipe-page-for-display`, which this contract names but never contains.
