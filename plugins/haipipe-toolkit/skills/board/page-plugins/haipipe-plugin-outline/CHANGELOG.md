## 0.20.2 — 2026-08-31
- Evidence record heads carry the plan's words (record-shape 0.18.1);
  `Ref` its own row, only when one exists.

## 0.20.1 · 2026-08-31

Scope: outline/ is legal on any unit folder, task folders included (the unit
symmetry); same kinds and grammar, no venue requirement file owed there.



## 0.20.0 — 2026-08-31
Rewritten to one lane, "the folder and the tab": 846 → 194 lines, present
tense. The grammars a writer or parser needs are now FILES a phase loads
instead of paragraphs inside this skill:
- **`ref/plan-grammar.md`** (new): ONE plan grammar, with the Page Type as the
  switch (a Section page's bullet is a sentence slot `S<n> · …`, any other
  page's bullet is a point); heads 4 to 11 plain words; a Note ≤ 30 words (a
  wrapped source line is still one Note; the specimen's longest is 28); the
  marks; the freeze; the teeth. The "terse Capitalized LABEL, ≤ 10 words"
  head rule is DELETED: it coexisted with the approved shape in one section,
  and 19 of 20 MISQ plans were written to it (`Trait relevance`).
- **`ref/record-shape.md`** (new): the seven record kinds in one table (id,
  labels, writer, teeth) with the per-kind rules, the board-wide `D<nn>`
  allocation grep, and the three laws every kind keeps.
- **`ref/specimen-section-plan.md`** (new): SM00 v3, frozen as the approved
  example.
- **Retired from this file**: every "was / until / ruled" narration (the
  `## States` merge, the proof mark, the `✅ have it` mark, the 0.16.x thread
  and version arguments, the Aims-in-plan window), the count words in
  headings (`Seven chips`), and the documentation of legacy parses (the
  renderer's tolerance for pre-0.18 shapes is engine behaviour, not law).
- **From the SM01 field test**: `ref/plan-grammar.md` states one `## C<n>` per
  Content division, `🎯 P<n>` beside `🎯 A<n>.<m>`, a `Cut:` bullet only where
  something leaves (zero is normal), provenance (`Gordon #41`, `D05 b`) is not
  attribution, and the coverage wording for a bare mark;
  `ref/record-shape.md` states the `D<nn>` race under concurrent sessions
  (grep right before the write, again after; the later writer renumbers).

## 0.19.0 — 2026-08-31

- **Aims back on the page; the plan keeps no Aim rows** (JL 260831, QPf12
  row 2: "In the Page as well, and should map to the content"). §🗂 and the
  plan-shape section say so; `live/outline.py plan_card` reads the page's
  `## Aims` first and lets a plan row fill only an id the page lacks.
- **Seventh kind, `<stem>-files.md`** (QPf12 row 3): the page's retired
  `## Files` as `### F<n>` records with `Path` and `Role`, a
  Related Board Page as `Role: related` with its row verbatim; 📎 Files chip
  (`_SIBLINGS`, physician-space-21).

## 0.18.3 — 2026-08-31

- **The plan never quotes the prose it plans** (JL, on SM00 plan v3: "too
  long, more like the sentences", then "I love this outline style" once the
  heads were 4 to 11 words and every Note one line): §✂️ gains the approved
  shape for a Section page, one bullet per sentence slot `S<n> · <what it
  does>`, groups by move, findings tagged `C1:`/`C2:`/`C3:` plus a word, a
  `Cut:` bullet for what leaves, terms defined inline the first time. A head
  that names nothing ("the question, with its two conditions named once") is
  the named failure.

## 0.18.2 — 2026-08-31

- **Paper-Personality-Opioid-MedJournal board carried into the record shape**
  (JL: "apply it for … MedJournal as well"): its 12 pages were in the original
  three-section shape (`## Aims` groups, `## States` with one ✅/🔨/🧠/⬜ row
  per Aim, `## Log`, no Discussion). Each Aim's state row became the plan
  row's tick and `**Now:** <emoji> <sentence>` (52 rows: 21 met, 31 open;
  three page Aims the plans lacked were appended); Log rows became records;
  every page keeps a `## Files` pointer and a `.pre-outline` backup; each
  outline/ folder gained an empty discussion (`(no open question)`), the
  requirement (venue-only, 0.18.1) and the evidence file. No thread ids were
  minted on that board.
- **JL's QPf12-outline rulings applied on both boards** (260831, rows 2 and 3):
  Aims are BACK ON THE PAGE as their only home (row 2: "In the Page as well,
  and should map to the content"): each page's `## Aims` rebuilt from the plan's
  rows as `- ✅/⬜ A<g>.<n> · head` + `Done when:` + `Now:` under `### A<g> · …`
  groups (group `A<n>` maps to Content division `<n>`); the latest plans keep no
  Aim rows (`.pre-revert` beside each); the 76 carried work items on SM03–SM07
  are dated log records, never Aims (0.16.1). `## Files` left every page for
  `outline/<stem>-files.md` (row 3: "A"), one `### F<n> · <label>` per file with
  `Path` and `Role` (reads · writes · checks · contract · archive · related);
  the 🧭 tab gains the 📎 Files chip (`live/outline.py _SIBLINGS`). Engine
  teeth and contract text for both rulings: the MISQ-Board session.
- **The seven MISQ plans with bare Aim rows were assessed** (AM01–AM06, SM00:
  52 Aims, 20 met, 32 open, each with a `Now:` fact); `aim-without-state`
  reads 0 on the MISQ board.

## 0.18.1 — 2026-08-31

- **Requirement is venue-only, four records** (JL, reading SM00's 📏 tab:
  "requirement is very hard to read, make it concise and readable, and maybe
  focus on the venue is sufficient"): V1 Shape (+ the desk's ARC chain),
  V2 Size (Words · Citations · Displays, `measured …` folded), V3 Refused
  (one line per anti-pattern), V4 Moves (first four slot names in the head,
  exemplars folded). `N1`/`N2` (Narrative row and style) and `B1`/`B2` (board
  rules) are gone from the file; the Narrative page and
  `ref/writing-rules.md` keep them. A page with no `structure-source:` gets
  no file. `check.py` `requirement-*` teeth follow: venue desk only.
- **Feedback header is three lines and the Round is one text block** (JL:
  "these are too detailed and hard to read"): the law paragraph, `source:`
  and `received:` lines are gone; the Round's verdict, people, dates and a
  link sit on one line, then Ask · Order · Gate; each row's parent R-row
  concern is folded detail (`↳ R01 · …`) under the card, not a label row,
  so the chip count equals the routed rows.

## 0.18.0 — 2026-08-31

- **One record shape for every file in the folder** (JL 260831, reading the
  SM00 lenses: "really hard to read", "the discussion is not for human,
  rubbish", "the logging is very bad", "the design of all of them are very
  bad … we should unify the format"). New §🧾: `### <ID> · <HEADLINE>`, then
  `- **Label**: value` rows, detail indented and folded, signed `>` lanes kept.
  Ids and label sets per kind: discussion `D<nn>` Ask/Options/We lean/Decide;
  log `YYMMDD` headline; feedback `S<x>-PP<n>` From/State/Landed (0.17.4's
  Feedback/Work/Parent rows fit the same grammar); evidence `C.P.B` Has/Status;
  requirement `V/N/B` Rule/Source. `live/outline.py _records` is the one
  renderer (id badge, headline, label grid, status pill, "more" fold) and
  still reads every pre-0.18.0 shape.
- **Discussion = open questions only, in plain words** (§💬 rewritten): a
  thread leaves the file when it settles and becomes one dated `-log.md`
  record, `D<nn> settled by JL: <ruling>`, argument kept under the fold.
  `check.py discussion-settled-thread` (proved 13 → 0 on the MISQ board).
  Board-wide id allocation now greps the log files too.
- **Log = a timeline of one-line records** (new §📜): `### YYMMDD · headline`
  (15 to 25 words), detail folded under. Restructuring an old row gives it a
  headline and moves its text under the fold verbatim; nothing is rewritten.
- **The requirement generator exists**: `cli/requirement.py` writes V (venue
  division: shape, moves, refusals, format values), N (Narrative row and
  Writing Style) and B (board hard rules, plain-English floor) records; run
  by `haipipe-page-outline` ⓪ REQUIRE. Teeth: `requirement-missing`,
  `requirement-hand-edited`, `requirement-stale`. 15 MISQ section pages got
  their file; the 📏 chip now draws.
- **`### Stage Record` is a retired block** (`check.py retired-block`, JL:
  "why we have this? we should not have this"); 13 MISQ pages cut.
- Content: SM00, SM01, SM02, SM08 discussion and log rewritten (5/3/3/2 open
  threads; 20/19/25/22 log records); `.pre-0.18` backups beside each.
- Content, the other 16 MISQ pages (after the peer session's `## States` →
  `## Aims` merge): `## Aims`, `## Discussion` and `## Log` moved off every page
  into `outline/` records. Triage: a `Needs JL` or `Decision Now` row is a
  thread only if it has options, a lean, a ruling verb or a question mark (55
  threads, D43–D126); the other 76 rows are CC's own work and became
  `- [ ] A<g>.<n>` rows under `### A<g> · 📋 Open items carried off the page`
  in each plan; ticked rows and `### D<nn>` records with a decision became log
  records; page Aim rows merged their tick and `Now:` into the plan by id.
  `checks/outline.py` passes on every plan; `.pre-outline` backups beside each
  page; next free id D127.

## 0.17.4 — 2026-08-31

- **A feedback row carries the Round's words** (JL, reading SM00's 🗣 tab:
  "it lost a lot of informations"): `collect` now copies each §2B row's
  `Feedback:` and `Work:` sentences, the full concern of every parent R-row
  (`- **Parent R03**: … → routes SM00, SM03, SM06, SM08`) and the §2A
  proposed reader order, all verbatim. 0.17.0's head-and-ids-only rule
  confused "never AUTHOR here" with "never SHOW here"; a file regenerated
  whole cannot drift from its source. `landed:` still preserved by row id.
  Ledger-only rows (NA01) keep their closing quote in the head.

## 0.17.3 — 2026-08-31

- **One chip per sibling file on the 🧭 tab** (JL: "we should have more
  buttons here to host the content in the outline folder"): 📏 Requirement ·
  💬 Discussion · 🗣 Feedback · 🧾 Evidence · 📜 Log, each drawn only when its
  file exists, each read-only, with a row count on the chip. Verified in Chrome
  on SM01: `🧭 By part | 🚦 What is left | 💬 Discussion · 6 | 🗣 Feedback · 8 |
  🧾 Evidence · 28 | 📜 Log · 12`.

## 0.17.3 — 2026-08-31

- **`Routed:` is a folded line** beside `Note:`/`Answered:`/`Drawn:` (NA01
  field test: the phase named it in 0.11.0 and this file, both parsers, and
  the renderer did not know it; 8 of 16 lines vanished from the fold).
- The §📐 example reads `supersedes: none`, not the em-dash.
- Roster row updated to the six kinds; 0.17.1 and 0.17.2 had not touched it.

## 0.17.2 — 2026-08-31

- **`<stem>-evidence.md`, the sixth kind** (JL: "an evidence-status.md in the
  outline plugin, to check what is the current evidence status"): a dated
  snapshot of the 🧭 join, one bullet per line in the Evidence Bundle's six
  status words, written only by `cli/evidence-status.py` (imports
  `live/outline.py`, so file and tab cannot disagree). Two `check.py` teeth,
  `evidence-stale` and `evidence-hand-edited`, each proven 0 → 1 → 0 on SM08.
  SM06 reports 37 owed / 0 landed, which is honest: its `probe/V01-…` and
  `display/S-Display-…` are retired shapes the contract cannot read.

## 0.17.1 — 2026-08-31

- **`<stem>-requirement.md`, the fifth kind** (JL 260830: "put the writing
  requirements as one subfolder as well"). FLAT, not a subfolder, because the
  0.17.0 layout rule reserves folders for many-files kinds and a requirement is
  one per page. GENERATED by the same `stage.py sync` that today pastes a
  sha256-stamped `### Writing Style` block into 17 MISQ pages (149 lines), from
  the venue row (`structure-source` + `structure-division`), the Narrative row
  (`style-from`) and `ref/writing-rules.md`; that page block is retired. Never
  authored (it would fork the consumer-neutral venue bank), never versioned
  (its sources carry their own); a page-specific deviation is a `D<nn>` thread,
  cited by id.

## 0.16.1 — 2026-08-30

Field test on SM08 (15 frictions, ledger 5 MATCH · 2 SKILL GAP · 0 EXPECTATION GAP):

- **`D<nn>` ids are BOARD-WIDE**, allocated from the board's max with a grep;
  the first run minted D01-D06 page-locally while SM06 owned D01/D05/D11, and
  `D16` was already duplicated between AM02 and SM04. A thread id is a
  cross-page address (cited from ten files), which is the same fact that keeps
  this file unversioned.
- **A live ask that owns no Aim becomes a 🔴 thread, never a minted Aim** (the
  run invented `A1.10`, a target nobody agreed to).
- The page keeps a `## Files` pointer at both moved files; header shape for
  both files; rows newest-first; `round: —` legal before the first Round.

## 0.16.0 — 2026-08-30

- **Three kinds in one folder** (JL: "outline plugin is a folder!!!!"): the plan
  `<stem>-outline-v<N>.md`, plus `<stem>-log.md` (what CHANGED, append-only) and
  `<stem>-discussion.md` (what was ARGUED, `D<nn>` threads with status/serves/
  round). `page.md` is the PRODUCT; this folder is the PROCESS. Neither new
  name may contain `outline` (the plan globs are `*-outline-*.md`).
- **`## States` is gone from the page**, finishing the 260819 merge: one Aim
  row carries tick + `Done when:` + `Now:`; live asks become the Aim's `Now:`.
- **The Aims stay with the plan and the page keeps no copy.**
- **The discussion is never versioned**: threads settle independently (D01
  closed while D05 stayed open), a thread id is a cross-page address, threads
  move between pages; `> ✎` already records edits; a status change owes one
  log row naming the id.

## 0.17.0 — 2026-08-31

- **Fourth kind: `<stem>-feedback.md`**, what OTHERS said, one file per Round
  (JL 260831: "it will have its own file and folder"). Rows are PROJECTED from
  the Round's §2A/§2B by `haipipe-board/cli/feedback.py collect`, never
  paraphrased; the page writes exactly one field, `landed:`. PULL, not push:
  the page collects during OUTLINE ⓪ and no Round writes into another page's
  folder. First run: 15 pages, 104 rows, from RD01 on the MISQ board.
- **The layout rule.** One-per-page kinds sit flat with the stem
  (`-requirement`, `-discussion`, `-log`); many-per-page kinds get a folder
  named by SOURCE (`<stem>-feedback.md`, `## RD01` inside). The plan is grandfathered flat.
- **Feedback ≠ discussion**, stated: discussion is authored here, feedback is
  received and may not be rewritten here.

## 0.16.1 — 2026-08-30

- Patched from the SM08 field test (15 frictions): `D<nn>` ids are BOARD-WIDE
  with the grep that allocates them (the run minted D01-D06 against SM06's
  D01/D05/D11; D16 was already doubled between AM02 and SM04); an ask owning
  no Aim becomes a THREAD, never a minted Aim; the page keeps a `## Files`
  pointer; header shape for both files; newest-first; `round: —` is legal.

## 0.16.0 — 2026-08-30

- **Three kinds in one folder** (JL: "outline plugin is a folder!!!!"): the
  plan, `<stem>-log.md` (what CHANGED) and `<stem>-discussion.md` (what was
  ARGUED). `## States` is gone from the page, finishing the 260819 merge; the
  Aims stay with the plan and the page keeps no copy. The discussion is never
  versioned: the unit that freezes is the THREAD, and a thread id is a
  cross-page address. Neither new name may contain `outline`.

## 0.15.0 — 2026-08-20

- **§✂️'s `Answered:` line gains the `· recount` tail** (JL: "看看哪里可以去
  优化"): it flags a value that counts the run's own artifacts so DRAFT knows
  the one kind of value it must re-read from the card instead of trusting the
  plan.

## 0.14.0 — 2026-08-19

- **The Aims live in the plan file** (JL: "Aims should be move together with
  outline"): §📐 gains the `## Aims` trailing section — one target plus its
  `**Done when:**` test per Aim — and the 🎯 tie diagram routes plan bullet →
  plan `## Aims` → page transcription → page `## States`. Before the move a
  renumbered plan pointed ids at the page's OLD Aims (nine of sixteen on
  QPw00 did).
- **§✂️ plain, common words** (JL, on `The control rung.`: "不要用这样的词了"):
  a rare word fails even when apt; a technical term survives only as the
  thing's real name, defined at first use; metaphor vocabulary is rewritten
  to the plain thing it means.

## 0.13.0 — 2026-08-19

- **§✂️ concise bullets**: one bullet = a few-word HEAD (the point or the
  question) · evidence appends (`Answered:` / `Drawn:`, written by the fold
  when the card lands or the unit builds) · the end-anchored mark. The head
  never restates what lives behind its own mark (JL: "越 concise 越好…冒号后面
  的东西其实都有点喧宾夺主了").
- **Same night, the bullet's hidden detail**: every bullet folds a concise
  explanation behind a click — `Note:` (authored at OUTLINE) or the fold's
  `Answered:`/`Drawn:` — with NO disclosure marker; heads are terse labels or
  questions ("Figure for Whole Workflow Loop"). 131/131 bullets on QPw00
  carry one.
- **Levels styling**: paragraph rows show their own address + a short accent
  tick; one shared left-aligned address column aligns every title (JL picked
  the accent bar from four previews, then trimmed it to a tick).
- Coherence pass, same law: §🔒 qualified — the fold APPENDS `Answered:`/
  `Drawn:` (and `📮 PP<NN>` ids) into bullets in place, into the working file
  while `approved:` is ⬜ or into `v<N+1>` after a tick; §📐 counts FIVE
  display kinds (`illustration` added), its worked example now shows §✂️-style
  bullets (terse Capitalized head + folded `Note:`), and the ↩ example says
  "answered", not the retired "bound"; §🚧 no longer pins the sibling phase
  skill's version.

## 0.12.0 — 2026-08-19

- **📮 probe and 🧮 value are now SEPARATE marks** (JL: "You mean you put the
  probe and values together? I want to separate them"). 📮 = this point needs
  a QUESTION answered — bare before ② raises the card, `📮 PP<NN>` after; the
  answer may be a finding or a folder of numbers. 🧮 = this point QUOTES one
  value, `PP<NN>.v<n>`, out of an answered card's `## Values` block, and
  `checks/values.py` re-computes it. 📮 deliberately shares phase ②'s glyph
  (same concept) and is end-anchored in the scanners so prose about the phase
  never reads as a mark.

## 0.11.1 — 2026-08-19

- **🧮 widened from "a number" to "a probe-answered fact".** JL: "this point
  might need a probe to provide the evidence, do you get it?" — the mark IS
  the needs-a-probe mark, and the card already binds ANY answer by path; the
  `PP<NN>.v<n>` ids and `checks/values.py` recompute are the numeric
  specialization, not the definition. Bare 🧮 = probe needed · 🧮 PP<NN> =
  raised · ↩ ✓ = landed.

## 0.11.0 — 2026-08-19

- **The ✅ "have it" mark is RETIRED.** It asserted "backed on disk" without
  naming what backs it, so no machine could recheck it; an unmarked bullet
  already means "plain point, nothing owed"; and the glyph already works two
  other jobs (`approved: ✅` tick syntax, phase ⑦), which produced a phantom
  chip on a bullet that merely QUOTED the tick name. JL failed to read it
  three separate times. Zero plans carried it at retirement, so no alias is
  kept: an end-of-line ✅ in a plan is now just text. The mark grammar is
  four: 🧮 value · 📚 citation · 🖼 display · 🎯 aim.

## 0.10.1 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.10.0 — 2026-08-19

- **Mark to plugin, written down once.** A mark names what a bullet OWES and a
  plugin names WHERE it is answered, so `🔢 value` is served by `probe/` and
  there is no plugin called `value`. JL asked for one on 260819; a fourth
  plugin would be a second home for one folder.
- **A paragraph carries 3 to 6 bullets.** The `### C<n>.P<n>` line is a brief
  the tab prints above them, and eight bullets under one brief means the brief
  cannot describe them. Split by idea, not by count.
- **🧮 proof RETIRED.** JL 260819: "我从开始到最后都没有说 proof，我一直说
  probe". The mark came from ONE transcribed quote ("citation, display, values
  and proofs") and no Log row ever ruled it. Going to a task folder or a
  discovery folder for the evidence behind a claim IS a probe, which is 🔢.
  It was the only mark with no plugin, no folder, no lane, no id and no
  backlink, and that was the symptom rather than a design.
  ⚠️ `proof/` the FOLDER is untouched: it belongs to a probe card.

- Six marks become FIVE: 🎯 aim · ✅ have it · 📚 citation · 🔢 value · 🖼 display.
- `live/outline.py` drops 🧮 from `_MARK`, from `_live`, from the Evidence
  Bundle kinds and from the `owed` count. 48 marks stripped from 14 plan files.

## 0.9.1 — 2026-08-19

- **A bullet never carries a markdown heading mark.** JL objected twice in one
  session, to `####` inside a bullet and then to `` `## Opening` ``: they are the
  file's own syntax, so a reader parses them as structure before as a reference.
  Name the part in words or with the § anchor.
- The same rule stated for `## ` lines: only `## C<n> ·` is a division. A stray
  `## ` in a plan's preamble was counted as a phantom division and shifted every
  address below it by two. `live/outline.py` now matches `^## C\d+` and nothing
  else, so the file and the renderer agree.

# CHANGELOG · haipipe-plugin-outline

## 0.9.0 — 2026-08-17

Adds the derived Point-addressed Evidence Bundle. The outline surface joins
sentence scaffolds, Probe/Bibex/proof/Display resources, and owner feedback
without creating an `evidence/` copy or mutating the approved plan.

## 0.7.0 — 2026-08-17

**The plan is SKIMMED, so the evidence stops outweighing the sentence** (JL
260817, with a screenshot: "太肥太胖了 … 你把这些 outline 都给挤得不知道去哪儿
了"). 0.6.0 shrank the popover, which was the wrong target: the weight was in
the ROW.

```
                      was                          now
────────────────────────────────────────────────────────────────────────
chip placement        a sibling of .row's flex,    inside the sentence's
                      so each one was a COLUMN     own span, inline
                      that stole the text's width
chip shape            14px, 999px radius, 0 9px    10.5px monospace, 4px
                      → 22px tall, wrapped to      radius, 0 4px, nowrap
                      two lines beside a 19px row  → 17px tall, one line
note text             "Gray2021 in bibex/"         "Gray2021"
                      "no unit declared yet"       "owed"
                      "↩ PP04 serve this bullet    "↩ PP04 0/1"
                       · 0 of 1 answered"
row                   13px, 3px 0 1px padding      12px/1.4, 1px 0
addr column           62px, 600 weight             42px, right-aligned
```

Measured in Chrome at a 660px pane, same page, same 66 rows: document height
2017 → 1807 px, widest tag 143×22 → 124×17 px. The structural half (inline
instead of a flex column) is not in those two numbers, because CSS alone cannot
undo it; the screenshot pair is its evidence.

- 🚫 **No emoji inside a tag.** `⬜` and `📄` render at full glyph size in a
  10.5px tag and double its width. The dashed border and muted colour already
  say "not landed", so `PP01 answered 1📄 ⬜` is now `PP01 answered 1`.
- **A fact is never printed twice on one row.** The ↩ backlink is suppressed
  for a card the row already names as a chip, so `🔢 PP01 answered 1` no longer
  drags `↩ PP01 ✓` behind it. It still fires where it is the only speaker: a
  bare mark, or a bullet with no mark at all, which is the normal case since
  the plan is frozen before the card exists.
- **A plain bullet can now carry a ↩ too.** It used to `continue` before the
  backlink was computed, so a card serving an unmarked sentence showed nowhere.
- `&nbsp;` was written into a string that then went through `_e()`, so the plan
  card's header printed the five literal characters (`0 accepted &nbsp; aim 9`).
  Separators moved into the markup.

## 0.6.0 — 2026-08-17

**The evidence card is sized as a NOTE** (JL 260817: "现在我感觉这个 evidence
card 太大了"). It opens beside a 13px outline row, so a 34em/14px panel with
13/16 padding read as a modal. Measured in Chrome before and after:

```
🔢 PP01   512×131 px  →  339×120        📚 Deyo2015  367×86 px  →  327×64
🔢 PP03   512×109 px  →  339×101        width       34em/14px  →  25em/12.5px
```

- **A citation prints `Author et al.`**, not the author list. Six names is what
  made a 📚 panel twice a 🔢 panel's height, and the key in the panel's own
  title bar already carries the first author. `Dowell2022` went 235 → 144 chars.
- BibTeX's `---` prints as an EN dash, never three raw hyphens and never an
  em dash (JL's standing rule).
- **A chip no longer prints its id twice.** `🎯 A4.2 → A4.2` was visible in the
  260817 screenshot: with an id the note stays empty, and only a bullet with NO
  id spends the note on saying it is untracked.

Also in this pass, and it is the reason the size question got asked at all: the
🧭 join read a card's state through `raised`/`working`/`bound`, three words
`haipipe-plugin-probe` 0.7.0 had retired, so two ANSWERED cards on
`QC1-visitlbp` rendered `⬜ 0 of 1 bound`. The join now resolves through the
protocol's own ladder (`_pstate`), keeps the retired words as aliases, counts a
`read` card toward `accepted`, and prints `all answered` / `2 of 3 answered`.

## 0.5.0 — 2026-08-17

**🧮 proof earns NO folder**, closing the ⬜ this file opened on 260817. The
ruling is `haipipe-page-probe` §🧭's: a proof lands as prose, and the pulled
file a derivation rests on already lives in a probe card's `proof/`, so a
second home for the same material would be one thing filed twice. A 🧮 bullet
carries no id and no card backlinks it.

## 0.4.0 — 2026-08-17

**The PHASE moves out to `page-workflows/haipipe-page-outline`** (0.1.0, same
day). This file kept both the material and the phase's rules while the phase had
no home; now it states neither twice and points at the contract instead. DRAFT's
own §🗂 was trimmed at the same time and no longer owns the outline.

**Each evidence ref opens as the board's own evidence card** (JL 260817: "我想让
它有点像那个 evidence card 一样"). Chip in the line, popover panel beside it,
holding the THING itself as `haipipe-sentence` §🃏 requires: the reference as
printed, the probe card's own question, the display unit's own claim.

- Native `popover`, no script: deleting every `<script>` must leave the panel
  readable, and it is real body text rather than a `title=` attribute.
- The class is `.evchip`, NOT `.chip`: the lens toggle buttons already own
  `.chip` on this page, and reusing it made the two fight (found by driving it).
- Two parser bugs fixed the same way: BibTeX `{CDC}` protects capitalisation and
  is not part of the title, and a README `claim` wraps onto the next line.

## 0.3.1 — 2026-08-17

**📚 means a published work, never a sibling board page** (JL 260817 asked
whether C1 should have citations and why there were so few). It had NONE: the
page's `bibex/QC1-visitlbp.bib` held zero entries, and the three 📚 marks in its
plan pointed at `QB1`, `QB2`, `QB3`, which are board pages.

- `_disk_state` now reads `bibex/*.bib`, so a 📚 is checkable like 🔢 and 🖼:
  `in bibex/` · `🚨 not in bibex/` · `🚨 <id> is a board page, not a citation`.
- A cross-reference to a sibling page is a different act from a citation and is
  written in the bullet's own words, without the mark.

## 0.3.0 — 2026-08-17

**A bullet is a POINT, not a sentence** (JL 260817: "一个 bullet point 我们可能有几个 sentences 去 cover，所以我感觉可能还是 B 比较好"). The proof was in the plan's own text: one bullet listed six OLS specification families, which is plainly several sentences, not one.

- The address is `C<n>.P<n>.B<n>`. One `B` becomes 1..n `S` at REVISE, and
  `C<n>.P<n>` is shared with the sentence address so the link survives.
- `haipipe-sentence` keeps `S` on the rendered page. Neither redefines the other.
- `C` STAYS and is not decoration (JL asked why): Aims use `A` and page-wide uses
  `P` in that same slot, so dropping it would collide `C1` with `A1`. It prints
  ONCE on the section heading; the rows carry only `P<n>.B<n>`, the part that
  changes.

**A bullet with no mark is the normal case, not a defect.** 0.2.0 required a mark
on every line and flagged bare ones 🕳. That made the plan unreadable and buried
the few lines that actually owed something. A mark is now the exception, written
at the END of a bullet, because that is where the card will hang on the real
sentence.

**THE PAGE NOW folds shut** (JL 260817: "第二部分还有必要要吗？我感觉有点
confusing"). The tab shows two halves answering two different questions, and
neither was labelled: 🧭 THE PLAN, what the page said it would cover, and
📄 THE PAGE NOW, what is written today. Both are labelled now and the second
collapses to one line, since on a page whose aims carry no ids it was nine empty
cards in the reader's way.

- Empty-division wording fixed: "nothing lands here yet" read as "this part is
  fine". It now says "no aim, state or file on this page names this part", which
  is the actual reason.

## 0.1.0 — 2026-08-16

First contract for a plugin that had already SHIPPED without one.

- The engine, checker, and drawer JS landed in commit `711b964c` ("Ship the
  pagex and outline plugins"), and QPf12's own state line recorded the gap:
  `open: marks on old pages, plugin skill`. Without a SKILL.md no agent could
  discover the surface or knew what `§N` meant, so pages kept being written
  with every aim unanchored.
- Records the four facets as built: storage NONE (live, storage-less, the QPf1
  folderstat precedent), writer NOBODY (rule-based, no model call at render
  time), surface `GET /_board/outline` with the 🧭 By division and 🚦 By
  progress lenses, boundary deliberately OFF the plugin roster as a meta-surface
  twinned with 📂 folder.
- Adds the DRAFT link (JL 260816, "is that before the draft, we should also have
  a outline for this page as well?"): this tab is WHERE a DRAFT outline is read
  and approved. DRAFT writes the material — divisions, `### A<n>` groups, `§N`
  anchors — and the surface reads it back. No outline phase and no outline file:
  a fifth phase would only take DRAFT's authority over what divisions exist.
- States the one-click test: a page whose 🧭 tab is one big 🌐 card has no plan
  yet, only prose.
