---
name: haipipe-board-page-for-venue
description: >-
  The VARIANT contract for a Board's venue pages: QBv<n>-<slug>, one page per submission TARGET, a journal, an agency, or a patent office. It loads haipipe-board-page for the base frame and never restates it, then adds only what a venue page needs and an ordinary decision page does not: three figures in a fixed order (desk taste, Venue-Structure, Submission-Rules), Content divisions named with the venue's own reading index (Sec-0-Abstract, Sec-1-Introduction, ... Sec-A-Appendix), the two-source rule that the DESK outranks the pack and every disagreement is written down, a Files section in five groups ending in Authority and Generated, with this contract itself filed under Contracts, the provenance stamp every desk fact carries, and the rule that a slot the pack cannot fill is PRINTED as an open row rather than left off. Use when writing or fixing a venue page, when a new outlet gets a page, when the pack and the desk disagree, or when a venue page states a number with no source. Trigger: venue page, QBv, outlet page, journal page, desk, venue pack, playbook, submission rules, page limit, Venue-Structure, Submission-Rules, exemplars, section kinds, /haipipe-board-page-for-venue.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-03"
  summary: "First release. Lifts the contract QBv1-misq was built to on 260803 into a loadable variant."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-venue · a venue page records a desk it cannot argue with

**LOAD `haipipe-board-page` FIRST.** It owns the base: the sections and their fixed order, the five rows that define each one, the title rule, the Opening split, the numbering, and the evaluation contract.
This file adds only what a venue page needs and an ordinary decision page does not.
It never repeats a base rule, because a copied rule goes a night out of date while the contract moves.

**The kind this variant covers**: one page per submission TARGET, and nothing above it.

```
kind    filename              subject                        closes when
────────────────────────────────────────────────────────────────────────────
Venue   QBv<n>-<slug>.md      ONE desk: a journal, a         its Aims are met
                              funder, a patent office        like any Q page
```

`QBv1-misq.md` is the reference implementation. Read it before writing a new one.
There is no pack-head page above the outlets (JL 260802): four outlets in one pack get four pages, and what they share is stated on each page that needs it, never in a fifth page nobody opens.

## 🏛 What makes a venue page different

A normal Q page settles something the team gets to decide. **A venue page settles nothing.** Its subject is a desk outside this repo that publishes its own rules, changes them without telling anyone, and rejects papers that ignore them. The page's job is to make that desk legible before a paper is written for it, not to have an opinion about it.

Three consequences, and every rule below comes from one of them:

```
1  the subject is EXTERNAL      →  every fact carries where it came from and when
2  there are TWO sources        →  the desk outranks the pack, and the gap is written down
3  a paper is BUILT from it     →  the page owes structure and mechanics, not just taste
```

**What a venue page does NOT own**: which venue this paper picks. That decision lives in the paper board's Opening concern (`QB1` on the paper board). This group is the catalog that decision reads.

## 📖 A venue page is a REFERENCE, not a rulebook

**The principle (JL 260803), and it governs everything below.** A venue page is read while writing a paper, and almost everything on it is a suggestion: the arcs, the budgets, the moves, the anti-patterns are all measurements of what published papers at that desk actually did. A drafter may depart from any of them on purpose, and doing so is off-pattern rather than wrong.

**One part of the page binds.** The desk's own published rules, which live in the `Submission-Rules` figure and the `Authority` group, are enforced by the desk itself: break one and the manuscript is returned unreviewed. Nothing else on the page has that force.

```
📖 REFERENCE   arcs · budgets · shapes · moves · the pack's refusals ·
               format values · exemplar language
               ↳ measured from papers · departing is a choice

⚖️ BINDING     category cap · manuscript format · reference style ·
               anonymity · required disclosures · the portal
               ↳ published by the desk · breaking one costs the submission
```

**Why it has to be written down.** A page full of measured numbers reads as a specification. `QBv1` printed `120-160 words, do NOT exceed ~185` for the abstract, which is the pack's measurement of eight papers, while the desk publishes no abstract cap at all. Read as a rule, it makes a drafter write to the middle of a distribution instead of to the paper. Found by JL 260803, who ruled ~250 words fine.

**So every length says whose it is**, and the page says it in the row itself:

```
✅  120-160w observed, no desk cap · ~250w ruled acceptable JL 260803
✅  55 pp Research Article · the DESK's cap, counting everything
🚫  120-160 words, do NOT exceed ~185        ← reads as a rule, is not one
```

**A binding rule also has a WHEN, and it is not always submission.** Nature Communications requires no particular structure or format at first submission and says style and length "will not directly influence consideration"; its caps are enforced at REVISION. A page that files those caps beside JAMA's tells a drafter to spend weeks on a gate that is not there yet, and a page that omits them lets a revision arrive over the limit. So a binding row carries the moment it bites:

```
⚖️ AT SUBMISSION    the desk checks it before an editor reads · JAMA's 3,000 words
⏳ AT REVISION      free at first submission, enforced later · Nature Communications
🎯 AT ACCEPTANCE    priced or demanded once accepted · every Nature-family APC,
                    and npj's waiver, which must be REQUESTED at submission anyway
```

**Write the pack's refusals as the pack's.** `the pack refuses more than ~160 words` rather than `do not exceed ~160 words`, so the page never sounds like it is the one doing the refusing.

## 📚 The two sources, and which one wins

```
📦 THE PACK          paper/venue/playbook-<family>/<OUTLET>/
                     taste.md · <OUTLET>-<section>/style.md + template.md · examples/
                     ⚖️ READ and NEVER written by this plugin: the packs are their
                        own repository, jluo41/Venue-Paper, pinned as a submodule

🏛 THE DESK          the venue's own published instructions, on its own site
                     submission guidelines · categories and lengths · policies ·
                     review process · the manuscript templates it publishes

⚔️ WHEN THEY DISAGREE   the DESK wins, and the disagreement is WRITTEN DOWN on the
                        page, naming both readings. A correction never goes into
                        paper/venue/, because this plugin does not write there.
```

The disagreement is the most valuable thing on the page, so it is never quietly resolved. `QBv1` records three of them: the pack observed "40-50 published pages" where the desk sets a 55-page submission ceiling, the pack records no reference style where the desk requires APA 7th, and the pack records none of the submission mechanics at all.

**Provenance is stamped, and HOW it was read is part of it.** A desk fact carries the date and the method, because these two are not equally strong:

```
✅  fetched and verified 260802
✅  re-checked 260803 through search summaries only, the site answers a direct
    fetch with HTTP 403 · re-read before submitting
🚫  "MISQ requires APA 7th"            ← true, and unciteable, and unmaintainable
```

## 🖼 Three figures, in this order, in `## Diagram`

The base allows any number of figures and requires a caption line above each. A venue page carries these three, and a page missing one is incomplete rather than short:

```
① DESK TASTE        what COUNTS as the contribution · what is DESK-REJECTED ·
                    the desk's own test, quoted · the exemplar count
                    answers: would this desk even look at my paper?

② VENUE-STRUCTURE   the sections in the venue's READING ORDER, each with its
                    budget and what it owes · the one ceiling over all of them ·
                    whether a kind is a floor a real paper may exceed
                    answers: what am I actually writing?

③ SUBMISSION-RULES  category and cap · manuscript format · reference style ·
                    the submission system · anonymity · required disclosures ·
                    the odds, the clock and the money · an open row for what is
                    NOT on record · the desk's own URLs
                    answers: what does the portal demand on the day I upload,
                             and what am I signing up for by choosing this desk?
```

**When the desk publishes a TOTAL, add the pack's parts up and print the sum against it.** This is a required row in `Venue-Structure`, not an optional nicety, because it went 3 for 3 the first time anyone checked:

```
JAMA IM         desk 3,000 w body   ·  pack floors sum to 3,350   ·  over before you start
PNAS            desk ~4,000 w       ·  pack floors sum to ~6,970  ·  74% over
Diabetes Care   desk 4,000 w body   ·  pack floors sum to 3,950   ·  the cap IS the floor
MISQ            desk 55 pp counting everything · no per-section desk limit at all
```

The arithmetic is systematic rather than unlucky. A pack measures PUBLISHED papers section by section, and a published page is not a submission budget, so the parts were never fitted to the whole. Neither source is wrong and the page resolves nothing: it prints both, names the cap as the binding one, and opens an Aim on how the body gets allocated. A drafter who writes to the middle of every per-section budget is over the cap at every desk that has one.

**The odds and the clock belong on the page.** Acceptance rate, how many review rounds a paper takes, how long a cycle runs, whether submission or open access costs anything: these decide whether a desk is worth a year, and none of them are in any pack. They are the desk's reported statistics rather than promises, and the row says so.

**A venue page ends with the gate as a runnable list.** The last Content division turns the binding figure into an ordered checklist run once on the final file, because a rule remembered while drafting is a rule half-applied. `QBv1` runs seven steps: count the pages, pick the category, strip the author out, fix the references, move nothing outside the limit, write the disclosures, upload. The division also names the ONE step a finished paper cannot fix in an afternoon, which at every desk with a hard cap is the page count.

**Embed the desk's links twice, on purpose.** A row inside a fenced figure is plain text: the renderer runs `esc()` and the figure linker over a fence, never the inline markdown pass, so a URL written in a figure will not be clickable. Put the bare hosts in the figure so it stays readable when copied, and repeat them as real markdown links in a line directly under the fence.

**Never put a bare URL alone on its own line inside `## Diagram`.** That is the Excalidraw canvas slot. A desk URL alone on a line is safe only because the renderer matches the excalidraw host specifically; do not rely on it, and keep desk links inline in prose.

## 🔢 A section division carries the venue's index

**The rule (JL 260803, "I want to see the index").** A Content division that describes one section of the paper is named with the venue's own reading position in front of the section name:

```
### 4 · Sec-0-Abstract: one unstructured paragraph, question forward
    ▲       ▲
    │       └── Sec-<n> from ZERO, so the index IS the S-Main page number ·
    │           only the appendix takes a letter, Sec-A
    └── the Content division number, which counts the judgment divisions too

### A4 · 📝 Sec-0-Abstract: one unstructured paragraph, question forward
         ▲   the emoji lives on the Aims and States group and on the division's
             closing line. NOT on the division heading, however tempting the
             symmetry: check.py strips it from a group name and not from a
             division, so ten divisions produce twenty group-name-drift
             warnings at once. Written, built, reverted, 260803.
```

**The index counts from ZERO and carries the `Sec-` prefix** (JL 260803, arrived at in three tries). A 1-based index sat one off the `S-Main-<n>` page forever, so every reader converted; 0-based fixes that, and `Sec-` is what keeps `Sec-0-Abstract` from reading as a typo where a bare `0-Abstract` would. Letters were tried and dropped: a journal that letters its own appendix sections, as MISQ does with Appendix A and Table A1, gives a lettered section index two meanings at once. Only the appendix keeps a letter, `Sec-A`, precisely because it matches the desk's own lettering.

```
Sec-0-Abstract → S-Main-0     Sec-3-Methods → S-Main-3
Sec-1-Introduction → S-Main-1  Sec-4-Results → S-Main-4
Sec-2-Theory → S-Main-2        Sec-5-Discussion → S-Main-5   Sec-A-Appendix → S-Appendix-A
```

**`Sec-<i>` = `S-Main-<i>` is a PROPERTY, not a law, and a page must check it rather than assume it.** The identity holds only where the desk's reading order matches the order `section-kinds.yml` resolves, and three of the first four venue pages written to this contract broke it in a different way:

```
PNAS       reading order is Significance ▸ Abstract ▸ … ▸ Methods LAST, while the
           resolver has abstract=0, significance=1, methods=3 · the two columns
           genuinely disagree, so QBv13 prints BOTH and explains why
JAMA NO    no theory kind at this outlet, so Methods is Sec-2 where MISQ has Sec-3 ·
           the index is the DESK's order, never a shared numbering across venues
JAMA IM    a Research Letter is a whole article type with no reading position, so
           QBv6 gave it Sec-L rather than claiming a slot in the sequence
```

**When the two disagree, `Sec-<n>` follows the RESOLVER and the desk's printed order gets its own row.** The fan-out split 2-2 on this before anyone ruled: `QBv12` and `QBv10` bound the index to `section-kinds.yml`, `QBv9` and `QBv13` bound it to the desk's reading order. Both printed both numbers, so nothing was lost either way, but a board cannot carry two conventions. The resolver wins for one reason: `Sec-<n>` exists to JOIN the `S-Main` page a paper actually writes, and an index that tracks the desk stops being a join key the moment the two differ. Describing the desk is `Venue-Structure`'s job, and it has a column for it.

**The desk's own section list can be longer than the resolver's, and that gap is a finding.** `section-kinds.yml` declaring seven kinds is not evidence that the desk asks for seven blocks: MISQ expects Concluding Remarks that the resolver does not declare, Management Science requires a ≤250-word nontechnical executive summary that no pack folder covers, and JAMA Network Open publishes a Research Letter the resolver withholds. A draft built from the resolver alone reaches the portal with a required field empty. Print the block in `Venue-Structure` with the gap named, and open an Aim on it.

**A section has three numbers, and only one pair agrees**, so `Venue-Structure` prints all three: the venue index counts from 0 and the lifecycle page `S-Main-<n>` counts from 0, so those two LINE UP, which is the whole reason 0-based was chosen; the Content division is the one that differs, because it counts the judgment divisions ahead of it. State this in the figure; do not make a reader work it out.

## 📐 The division shape a section division repeats

Divisions `§1` to `§3` are the desk's judgment layer. Every division after them describes ONE section kind and repeats the same five parts, which is what makes the sections comparable across venues:

```
### <n> · <index>-<Kind>: <what this section is, in the desk's terms>
    **Caption**: the one thing that is true of it here and not elsewhere.
    ```text fence: 📐 ARC · 📏 BUDGET · 🧱 SHAPE · 🔀 VARIANT or 🖼 DISPLAYS OWED
    <emoji> Establishes ...        one line, what this division settles

#### <n>.1 · The moves, as slots        fill the shape; never lift the sentence
#### <n>.2 · What the pack refuses      each a named anti-pattern, not a preference
#### <n>.3 · Format values              words · citation density · value density · displays
#### <n>.4 · The language, in the papers' own words   5-6 attributed sentences, one move each
```

The judgment divisions are not fixed in number, and `QBv1` runs three: what the desk buys and refuses, what arriving here costs, and which sibling outlet a paper leans to with the tie-break that pins it here.

**Every number states its source inline.** A word budget, a paragraph count, or a citation density may appear only with the line that records it: a `style.md` line number, an exemplar name, or the desk's own page. Never as the page's own claim.

**A slot the sources cannot fill is PRINTED.** `🔢 VALUE DENSITY  not recorded by the pack` is a finding; deleting the row is a silent gap. The same holds in `Submission-Rules`, which carries an open `❓ NOT ON RECORD YET` row.

**Say what the desk REFUSES, not what it prefers**, because a preference does not decide a submission:

```
✅  a better classifier is not a MISQ paper
🚫  MISQ values theory highly
```

## 🏛 When the target is NOT a journal

A funder and a patent office are venue targets, and four of this contract's rules break on them. All four were found on 260803, by the agents that wrote `QBv15-grant` and `QBv16-patent`, and each is a real adaptation rather than a licence to skip the section.

```
1  Sec-<n> HAS NO RESOLVER      section-kinds.yml declares ZERO kinds for grant and
                                for patent, so no S-Main page exists and the index
                                cannot be "the S-Main number"
                                → grant used Row-<i>-<AGENCY>, the pack's own unit
                                → patent read its index off 37 CFR 1.77(b), with
                                  HOLES: conditional items take a figure row and no
                                  division, so the index is not contiguous

2  ONE TARGET, MANY DESKS       playbook-grant covers 8 agencies, playbook-patent
                                covers CNIPA + USPTO + EPO, each with its own
                                prescribed order
                                → Venue-Structure becomes a MATRIX, one lane per
                                  agency; or PIN one, say so in three places, and
                                  keep the others' deltas as their own divisions

3  "PACK OBSERVATION" IS EMPTY  the label means measured from published work, and
                                these packs hold ZERO funded proposals and ZERO
                                filings
                                → use AGENCY RULE vs PACK RECORD, and say on the
                                  page why the measured tier is missing

4  A RULE NEEDS ITS CYCLE       a journal's guidelines stand until changed; a
                                funder's expire every round and an office's fees
                                are dated
                                → provenance says when it was READ · a non-journal
                                  row also says which CYCLE it binds
```

**The unfixable step is not the page count.** At a journal it usually is. At a funder it is CHOOSING THE AGENCY, because a 15-page NSF description, a 5-page ERC Part I and a 7-page ARC description are three documents rather than three formats of one. At a patent office it is what the specification failed to disclose, because `35 U.S.C. 132(a)` bars new matter after the filing date. Verify the claim at source before writing it, as `QBv16` did.

**A blueprint-only pack has no exemplar language, and the page says so.** The per-section shape (`n.1` moves, `n.2` refusals, `n.3` format values, `n.4` the papers' own words) presumes measured work. Fill only what the pack or the office actually says, and never print four subsubsections with empty rows to satisfy the shape.

## 📎 Files: five groups, and two of them are this kind's own

The base offers a menu of action groups. A venue page takes these five, in this order:

```
⚙️ Engines       what REGENERATES this page       _tools/sync-exemplars.py
📋 Contracts     THIS FILE, and the base it        haipipe-board-page-for-venue ·
                 extends                           haipipe-board-page
📥 Input files   the pack files this page READS   taste.md · style.md · README.md ·
                                                  stages/section-kinds.yml
🔗 Authority     what the DESK itself PUBLISHES, read directly and never through
                 the pack · opens with the provenance stamp · carries the desk's
                 links AND every place the desk contradicts the pack
📤 Generated     what a tool WRITES into this page, between markers
```

`Authority` and `Generated` are this variant's additions; the other three are the base menu's own names. Both additions state an action, which is the base's test for a group name.

**This contract goes in `Contracts`, never in `Engines`** (JL 260803 asked which). The base's split is what decides it: an Engine is something you RUN and open to change behavior, while a Contract is what CARRIES a rule to other pages, and a loadable spec that never executes is named there. The row also has to say the link runs both ways: the page is this contract's reference implementation, so a rule changed on the page is changed in this file in the same pass, and a sibling outlet page reads this file rather than reading the reference page.

## 🤖 The generated spans

`_tools/sync-exemplars.py` on the paper board owns two marker blocks inside `## Files`, and nothing else:

```
<!-- exemplars:begin --> … <!-- exemplars:end -->    one row per exemplar PAPER,
                                                     keyed by filename stem
<!-- kinds:begin -->     … <!-- kinds:end -->        the S-page roster, resolved
                                                     from stages/section-kinds.yml
```

```bash
python3 <board>/_tools/sync-exemplars.py            # rewrite every outlet page
python3 <board>/_tools/sync-exemplars.py --check    # exit 1 if any block is stale
```

Never hand-edit between the markers: the next run overwrites it. The blocks are replaced by a marker regex, so they may sit under any heading, but keep the kinds block after the exemplars block. Run `--check` before calling a page finished; a stale block is a count that disagrees with the folder.

## 🩺 `state:` on a venue page

The page keeps the base's four values, and the readable note answers one question: **how much of this desk is actually recorded, and how much is still prose nobody reads?**

```
✅  🟡 PARTIAL · 15 exemplars · 7 sections · taste ✓ · the one-sentence test is
                 unread by any skill
🚫  🟡 PARTIAL                              ← says nothing a reader can check
🚫  🟡 PARTIAL · pack looks good            ← a mood, not a count
```

The desk being well documented is not the same as the desk being wired in. A page whose facts are complete and whose Aims are all `⬜` is honest, and common: the pack is a library until a lifecycle stage reads it.

## 🎯 Aims and States

**This variant does NOT override the base's Aim form.** Ids, `Done when`, and one State row per Aim id all apply, unlike the skill-page variant, which drops them. Use `### A<n> · <emoji> <index>-<Kind>: <name>` to mirror the Content division, and `### P` for a target belonging to no single section, such as the submission mechanics or propagating a template to sibling pages.

An Aim on a venue page is almost always the same shape: **something the pack records and nothing reads.** `Done when` names the run that would prove it, not the reading.

```
✅  A4.1 · The abstract variant is chosen before drafting, since it decides
          whether a number may appear.
    Done when: an abstract draft records its variant and its measured word
               count against the 120-160 budget.
🚫  A4.1 · Understand the abstract norms.        ← no run can close this
```

**Keep States honest against the folds.** A Log line that says a question was settled and a State row that still says `⬜ Not started, and the pack cannot answer it` is the drift this board exists to catch; it happened on `QBv1` between 260802 and 260803.

## 🚪 The two verbs

### 📄 create a venue page

1. Confirm the pack exists: `paper/venue/playbook-<family>/<OUTLET>/`. A missing file at either level is a missing ANSWER to record, not a reason to stop.
2. Copy `QBv1-misq.md` as the shape, never `ref/page-template.md` alone: the base template has no three-figure Diagram, no Authority group, and no section-division pattern.
3. Take the next free `QBv<n>` and register the page in `board.md`'s `## Pages` under `QBv`.
4. Fill `§1`-`§3` from `taste.md` and the family `README.md`, then one division per section kind from that kind's `style.md` and `template.md`.
5. Fetch the DESK itself. Write `Submission-Rules` and the `Authority` group from it, with the provenance stamp, and record every contradiction with the pack.
6. Run `sync-exemplars.py`, then build, check, and read the RENDER.

### 🔧 work on a venue page

1. Read the whole page first, including the folds.
2. Run the checker and clear the mechanical findings.
3. Then check the three things no checker reaches: does every number name its source, is every desk fact stamped with how it was read, and does any State contradict a Log line.
4. Re-read the desk when a fact is older than the last issue. A page limit or a reference style changes without a changelog.

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^QBv'
python3 <board-folder>/_tools/sync-exemplars.py --check
```

## 📂 Files

```
haipipe-board-page-for-venue/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base frame is `haipipe-board-page`; the engine is `haipipe-board`; the generator for the marked spans is the paper board's `_tools/sync-exemplars.py`; the group's own law lives in that board's `board.md` under `### QBv · Delivery Venue`; the reference implementation is `QBv1-misq.md`.
