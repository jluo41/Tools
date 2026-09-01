# The cycle job cards · six fields, every cycle, the same order

**What this file is for.** Each phase contract states its own authority in its
own words, and no two used the same fields: `haipipe-page-outline` writes
`owns · may do · exits · may not`, `haipipe-page-revise` writes a three-line
same-promise test, and `haipipe-page-check` writes `reads · writes · does not`.
All three are correct and none of them can be read next to the others.

JL asked the question that exposes it (260818 1402): "if I want to work with the
page workflow's each phase, what should each phase do". This file answers it
once, in six fields, identical for every cycle.

```text
❓ ASKS     the ONE question the cycle answers
📥 READS    what must already exist, or the cycle cannot start
📤 WRITES   the exact path it creates or changes
🚪 EXITS    a testable condition
✋ TICK     the person-reserved tick, or none
🔀 ROUTES   where it may go next
```

**The operational rule: you work a cycle by satisfying its 🚪 EXITS row.**

## 🔁 The loop has TWO PARTS, and the first one CONVERGES (260901)

Ruled by JL, 260901, replacing the 260819 PREPARE/①-⑦ shape: "definitely, we
should separate them into the Outline part and Draft part … C1 Agree, C2
Survey, C3 Creating, C4 Embed, and back to C1" (then the words, never the
letters: `C<n>` is a Content division in every plan address).

```text
  ┌── OUTLINE part · repeat until the plan and its runs agree ─────────┐
  │                                                                     │
  │   SHAPE ─▶ SURVEY ─▶ LAND ─▶ EMBED ─┐                               │
  │     ▲    👤 approved: 👤 Decide       │ plan v<N+1>                  │
  │     └────────────────────────────────┘                               │
  │     the tick at SHAPE carries the fork: fresh marks → SURVEY again;   │
  │     every ☑ make row folded → the DRAFT part                          │
  └────────────────────────┬────────────────────────────────────────────┘
                           │ 🚧 ONE boundary: approved: AND every make-row folded
                           ▼
  ┌── DRAFT part ──────────────────────────────────────────────────────┐
  │   WRITE   draft → revise → compile, chained; inner loop teeth →     │
  │           AI cold pre-check → revise, budget 3           ⚙ ready    │
  │   CHECK   a cold judge on the BUILT page, then a person 👤 accepted:│
  │           prose → WRITE · number/citation/figure → SURVEY ·         │
  │           argument → SHAPE · pass → CLOSE                           │
  └────────────────────────────────────────────────────────────────────┘
```

**The law under the first part.** Every evidence number is answered by a RUN at
a real address in `tasks/`; the run computes, the page interprets (EMBED). The
item table `outline/<stem>-items.md` is the one ledger: one row per mark, and a
derived status per row (`owed → bound → landed → folded → accepted`, plus
`stale · deferred · dropped · blocked`, `haipipe-plugin-outline/ref/item-table.md`).

**Why the first part loops.** Evidence does not confirm a plan; it changes it.
Two worked cases from 260819, both on `QPw00-page-loop`:

```text
  the plan said   COMPILE deserves its own division
  the evidence    0 contracts · 0 receipts · 0 ticks, and 0 of 4 split tests
  the plan now    14 divisions, COMPILE folded into §6.4

  the plan said   17 probe cards still at `planned`
  the evidence    checks/values.py recomputed it: 13
  the plan now    13
```

Neither was a defect in the plan. Both are the loop working: a plan written
before its evidence is a guess, and a plan rewritten after it is a plan.

## 🧑 A person's attention belongs to the OUTLINE part

Ruled by JL (260819): "for the user, we will mainly check the outline and the
evidences if we want. But if not, you can just go ahead for the draft and
revise and the compile." The OUTLINE part is where the page decides WHAT IS
TRUE; everything after is execution against a plan already agreed. So the
person's gates sit at the front (`approved:`, `Decide`) and at the exit
(`accepted:`); WRITE asks for nothing, and a run that stops inside it for a
person is stopping in the wrong place.

**Every cycle says which cycle it is, out loud.** A receipt carries `phase:`
and `cycle:`; the same words belong in whatever a person is shown.

## 🧭 SHAPE · `haipipe-page-outline` · phase OUTLINE

```text
❓ ASKS     what will this page say, section by section, and what does each
            bullet still owe?
📥 READS    the person's brief · the Page Type's `outline:` block (fixed |
            grammar | resolved) · the venue requirement · the page's sections
📤 WRITES   <page>/outline/<stem>-outline-v<N>.md · the open D<nn> records in
            <stem>-discussion.md · one record in <stem>-log.md
            🚫 nothing in the page itself. The plan and the page are two files.
🚪 EXITS    FIVE machine checks, then a person ticks `approved:`
              ⓪ ARC: `arc:` argues, adjacent divisions pass the swap test, the
                heaviest finding has a division
              ① COVERAGE, both directions: every mark is served by a row, a
                card or a unit, or counted as owed; every unit on disk is
                cited or carries `retired:`; every open feedback row is served
                or declined
              ② every row's and card's address names a real bullet in this plan
              ③ every recomputable value matches the repo  (checks/values.py)
              ④ the plan's shape matches its Page Type (plan-shape-off-type);
                heads 4 to 11 words, Notes ≤ 30 words, no Note quotes the page
✋ TICK     `approved:`  ← a person, and only after the five pass. What the
            person judges is the plan's DIRECTION, never its arithmetic. The
            tick carries the FORK: fresh marks → SURVEY; every make-row folded
            → the DRAFT part.
🔀 ROUTES   SURVEY · the DRAFT part (haipipe-page-draft) · SHAPE again (a
            v<N+1> when EMBED returned a changed plan) · HOLD
```

## 🔍 SURVEY · `haipipe-page-outline` · phase OUTLINE

```text
❓ ASKS     for each thing the plan owes: where in tasks/ does it come from,
            how far up the tree is the gap, and does a person want it made?
📥 READS    the approved plan's marks · this page's earlier rows · the
            project's tasks/ tree (QA/ digests, results/ listings, run configs)
📤 WRITES   <page>/outline/<stem>-items.md — one record per mark:
              Need · Route (task · discovery · bibex · display · pagex) ·
              Run (found | rerun | new-run | new-task | new-job | new-block |
              person | none · <address>) · Decide (☐ make, for the person)
            🚫 no card, no run, no Status word: the table is the whole write
🚪 EXITS    every mark has a row, every row has its outcome and its address
            where one exists, and a signed Decide
✋ TICK     `Decide` on every row  ← a person (☑ make · ☑ defer · ☑ drop)
🔀 ROUTES   LAND (every row decided) · SHAPE (a row's outcome is `none`: the
            bullet is wrong) · SURVEY again (waiting on Decide) · HOLD
```

## 🟢 LAND · `haipipe-page-evidence` · phase EVIDENCE · rows in parallel

```text
❓ ASKS     is every run the table decided on made, and its result on disk?
📥 READS    the item table, every row decided · the runs the rows name
📤 WRITES   the project's tasks/ tree: an r<NN>_ config, a scaffolded task,
            executed results (/haipipe-task's door) · the ` → <result file>`
            append on each landed row's Run line · <page>/evidence/bibex/ (a
            transcribed entry) · <page>/evidence/display/<unit>/ (intake ·
            recipe · pick · build) · <page>/evidence/probe/PP<NN>-<slug>/ ONLY
            for a question that leaves the page (stripped executor, one door:
            haipipe-probe-q-executor-agent)
🚪 EXITS    every ☑ make row's result file exists (`landed`); a ☐ row is
            refused, a deferred or dropped row skipped
✋ TICK     `verified` on a citation ← a person; nothing else
🔀 ROUTES   EMBED · LAND again (an outbound card still unanswered) · HOLD
            (a run cannot be made: data absent, server unreachable, PHI would
            move) · SHAPE (the bullet is wrong)
```

### the three lanes inside LAND, each with its own hand

```text
📚 citation   a person    the bib entry is landed verbatim AND a person marked
                          it verified; `person` rows until discoveries/ joins
🧮 value      the run     the row's ` → <file>` exists; an outbound card's
                          proof/ holds the aggregate extract and PP<NN>.v<n>
🖼 display    a machine   intake/ frozen from the landed result AND the unit
                          drawn and previewable (intake, render, pick, build);
                          only CHECK's accept stays out
```

## 📌 EMBED · `haipipe-page-evidence` · phase EVIDENCE · the merge point

```text
❓ ASKS     does the plan now carry every landed number, and what does each
            one mean for its bullet?
📥 READS    every `landed` row's result file · the approved plan
📤 WRITES   <page>/outline/<stem>-outline-v<N+1>.md: `Answered:` (the number,
            its source address, one clause of interpretation), `Drawn:`,
            `Routed:` appended under the bullets that asked; `approved: ⬜`,
            `supersedes: v<N>`
            🚫 no head, bullet, paragraph or division added, removed, reordered
            or reworded: EMBED fills, never restructures
🚪 EXITS    every landed row is `folded`; a landed answer that breaks a
            bullet's claim is written as a D<nn> and routed, not edited
✋ TICK     none — the plan it produces is ticked at SHAPE
🔀 ROUTES   SHAPE, always: the person re-agrees the embedded plan
```

## ✏️ WRITE · `haipipe-page-draft` then `haipipe-page-revise` · phases DRAFT, REVISE

```text
❓ ASKS     does the page now say, in real sentences with real numbers, only
            what the agreed plan and its landed runs support?
📥 READS    the approved plan with its Answered:/Drawn: lines · the landed
            rows · verified bibex entries · drawn display units
📤 WRITES   <page>/<stem>.md
              step 1 DRAFT: Content as sentences ending `<!-- realizes: C.P.B -->`,
              each number under a `> Value:` lane citing its row or PP<NN>.v<n>,
              no hole token · the Aims rows and their Now:
              step 2 REVISE (COMPILE folded): the sentence citing each drawn
              unit by id and its caption · a `> ✎` record under each rewritten
              sentence · the States rows · delivery/latex/ and delivery/word/
              rebuilt from the current source
            one record in outline/<stem>-log.md per pass, the diff folded
🚪 EXITS    the inner loop's cold pre-check returns zero blocking findings:
              1 write pass · 2 TEETH (realizes coverage · every number
              sourced · citations resolve · latex compiles · writing-score
              floor) · 3 a FRESH check-agent context in pre-check mode ·
              4 findings → the next pass; budget 3 rounds; a finding
              surviving two consecutive rounds is a HOLD with the trail
✋ TICK     none
🔀 ROUTES   CHECK · WRITE again · SURVEY (a claim lacks a landed run) · SHAPE
            (the promise itself must move) · HOLD
🚫 MAY NOT  open a card, make a run, or invent a number. The plan carries
            every number WRITE may use.
```

## ✅ CHECK · `haipipe-page-check` · phase CHECK

```text
❓ ASKS     is this exact BUILT version closable, and who must act next?
📥 READS    the RENDERED page and the built artifact, not only the markdown ·
            WRITE's last findings trail
📤 WRITES   one finding placed at the sentence, section or artifact it concerns
            the check record · the route
🚪 EXITS    CLOSE, or a named route back to any earlier cycle
✋ TICK     `accepted: ✅` on the page and on each selected display unit, plus
            the Folder owner's declared RULING when one exists; a person's
            "no" is one feedback record, routed like a finding, and a
            checkable "no" is PROMOTED into a tooth or a pre-check rule
🔀 ROUTES   CLOSE · WRITE (wording) · SURVEY (a number, citation or figure) ·
            SHAPE (the argument) · HOLD
🚫 MAY NOT  repair a substantive finding inside the same pass, and may not
            judge a version the same actor produced. In pre-check mode (inside
            WRITE) it may only say "another pass" or "ready", never CLOSE.
```

## 🧾 Person-reserved ticks, gathered

```text
tick             lives on                          reserved by            cycle
────────────────────────────────────────────────────────────────────────────────
`approved:`      outline/<stem>-outline-v<N>.md    haipipe-page-outline     SHAPE
`Decide`         outline/<stem>-items.md, per row  haipipe-page-outline     SURVEY
`verified`       each evidence/bibex entry         haipipe-plugin-bibex     LAND
`read:`          each evidence/probe/PP*/card.md   haipipe-plugin-probe     LAND (outbound only)
`accepted: ✅`   the page · each display README    haipipe-page-check       CHECK
the RULING       phase Gate/Closure or legacy Type Folder owner             CHECK
```

For a phase-owned Folder, `## Gate and Closure` declares the Page owner
RULING. A mechanical gate declares no additional person tick. When that gate
already names a person, the same domain-gate receipt satisfies CHECK; never ask
for a duplicate approval. Legacy Page Types retain their declared RULING.
Plugin ticks remain nested controls and do not mint GI/GD transitions.

`read:` and display `accepted:` REVERT when their inputs change; a folded row
REVERTS to `stale` when its run's result is newer than the plan. Persistence
of an owner RULING follows that owner's reopening law. A Page owes only the
plugin ticks selected by its phase plus its owner RULING, if any.

**Which selected person ticks this page still owes, right now**, one row each with the
approver's machine half beside it:

```bash
python3 <haipipe-board>/cli/pagephase.py <page-dir> --owed
```

The plugin tick kinds have rules files under `agents/approve-rules/`, so an
approver can establish everything AROUND the judgment and write `checked:`
(R10). An owner RULING has none: deciding the phase-owned question is the point,
and the ledger says which owner supplies it instead of inventing a check.

**The board page that argues this file** is `QPw00-page-loop` on
`BoardSkillBoard-260722`. Each phase's own page (`QPw1` … `QPw6`, plus the three
lane faces `QPw4c` · `QPw4v` · `QPw4d`) carries what its contract leaves open;
`QPw3-probe` is the retired cycle's history. The run's three cross-cutting
axes are NOT cycles and carry no cycle names: `QPw00a` who acts · `QPw00r` what
proves it ran · `QPw00g` who says yes.
