# The paper board layout: every group, every page, and how a filename is built

state: 🟡 PARTIAL · the layout is drawn from a live paper; three of its rules are not yet enforced
owner: JL
method: draw the whole paper board in one place, so a reader sees the shape before opening any one concern
session: d6d8c7f4-4e8d-4ebe-b16c-2d11a8f20e9e
## Opening

What does a paper's own board look like, all of it, on one page?
A paper board is the `0-lifecycle/board.md` inside a paper, such as the MISQ one.
It is grouped by Delivery concern, so the `Delivery · Opening` group there is what QB1 rules here.
A page in that group is an S page, such as `S-Work-1-claims.md`.
The shape only goes wrong where two groups meet, and one concern page can never show that.
So this page draws all ten groups at once.

**Where this page sits**: it sits before QB1 and is the only page here that shows the whole board.
Each of QB1 to QB10 carries a division for its own group, named `What we want on the paper board` on eight of them and `What the paper board shows` on QB1 and QB2.
This page is the index those ten divisions are slices of, and `§1` to `§10` here are its own one-per-group divisions.

**Why one page has to hold the whole thing**: a filename says which family wrote a page, and a group says which concern owns its rule.
Those two come apart in more than one way, and only one of those ways is a trap.
Nobody sees that by reading one concern at a time, so `§12` separates the cases instead of counting them.

**What it is measured against**: the MISQ paper, which is the only paper built far enough to show every group.
Where the design and that paper differ, the difference is named as a gap with an owner.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**This page DESIGNS; the paper board SHOWS**: it states what a paper must carry, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

**The PAPER board is the spine of every figure here**: a group name leads the line and the QB id annotates it, never the other way round (JL 260802).
**ONE PAGE, ONE LINE** (JL 260802): never put two page names on the same line to save space. A reader counting pages must be able to count lines.
This page answers what a paper carries, so a reader scanning the left edge must see the paper's own groups.

**Never restate a concern's own rules**: QB1 to QB10 own those.
This page owns the group list itself, one division per group in `§1` to `§10`, and then only what is true ACROSS the ten: every count in one table, what a filename says, how a filename is made, and what may sit in a group, `§11` to `§14`.

**ONE GROUP, ONE `###` DIVISION** (JL 260803, overriding the `####` rule of 260802): `§1` to `§10` walk the ten in board order, one division each, and `§11` to `§14` hold what is true across them.
`check.py` requires a caption and a figure under every `###`, and each group's figure is its own designed-against-live page list rather than a slice of the whole-board figure above.
A group division names the GAP between the design and the live paper; it never restates the rules, which belong to that group's QB page.

**A count here is a real count**: every number on this page was read off a live paper, never estimated.
If a number cannot be read off disk, do not write one.

## Diagram

**The whole paper board**: every page a paper carries, one per line, under the group that owns it.

```text
  📁 <paper>/0-lifecycle/ ── the board is a FOLDER, not one file
     board.md is its registry · the pages live in one subfolder per
     FAMILY, so the folder never tells you which group owns a page
  ════════════════════════════════════════════════════════════════
  🎯 WHAT WE EXPECT a paper to carry, group by group
  ### S01 · Delivery Opening                         ◀ ruled by QB1
      🌱 S-Open-Seed          ← the unit token IS the stage name
      🎯 S-Open-Venue
      📣 S-Open-Pitch
  ### S02 · Delivery Work                            ◀ QB2
      🗂 S-Work-R      control · which resources this paper has
      📦 S-Work-R1     one resource
      📦 S-Work-R2
      📦 S-Work-R3
      🗂 S-Work-C      control · which claims this paper has
      🎯 S-Work-C0     one claim
      🎯 S-Work-C1
      🎯 S-Work-C2
      🎯 S-Work-C3
      🧵 S-Work-N      the arc · one paper, one arc, no split
  ### S03 · Delivery Literature                      ◀ QB3
      🗂 S-Literature-Dash                          ✅ built 260803
      📄 S-Literature-1-<topic>                     ✅
      📄 S-Literature-2-<topic>                     ✅
      📄 ../sections/02_literature_review.tex     ← §2 prose, owned here
  ### S04 · Delivery Value                           ◀ QB4
      🗂 S-Value-Dash                               ✅ built 260803
      📄 S-Value-1-<topic>                          ✅
      📄 S-Value-2-<topic>                          ✅
  ### S05 · Delivery Display                         ◀ QB5
      🗂 S-Display-Dash                             the control page
      📄 S-Display-1a-hero-concept
      📄 S-Display-1b-research-design
      📄 S-Display-2a-distribution
      📄 S-Display-2b-validation-summary
      📄 S-Display-2c-llm-measurement
      📄 S-Display-3a-funnel
      📄 S-Display-3b-descriptives
      📄 S-Display-3c-variable-operationalization
      📄 S-Display-4al2-main-regression
      📄 S-Display-4al5-main-regression
      📄 S-Display-4b-context-regression
      📄 S-Display-4c-discretion-gradient
  ### S06 · Delivery Main                            ◀ QB6
      🗂 S-Main-Dash                                the control page
      📄 S-Main-0-abstract
      📄 S-Main-1-introduction
      📄 S-Main-3-theory
      📄 S-Main-4-measurement
      📄 S-Main-5-empirical
      📄 S-Main-6-results
      📄 S-Main-7-discussion
      📄 S-Main-8-conclusion
  ### S07 · Delivery Appendix                        ◀ QB7
      🗂 S-Appendix-0-control                       the control page
      📄 S-Appendix-A-prompts
      📄 S-Appendix-B-validation
      📄 S-Appendix-C-variables
      📄 S-Appendix-D-iv
      📄 S-Appendix-E-robustness
      📄 S-Appendix-F-bigfive
  ### S08 · Delivery Present                         ◀ QB8
      📄 QP0-present-delivery                       ← a Q page, no S page
  ### S09 · Delivery Build                           ◀ QB9
      📄 S-Submission-0-reconcile
      📄 S-Submission-1-compile
      📄 S-Submission-2-review
      📄 S-Submission-3-submit
  ### S10 · Delivery Round                          ◀ QB10
      📄 QR0-round-delivery
      ⚠️ one S-Round-<n> per batch                    ⚠️ family missing

  🔤 S-<Family>-<unit>-<slug>.md
     the FAMILY says who wrote it · the GROUP says who owns the rule
     since 260803 no page differs BY DESIGN, argued in §12.4
     this figure draws the DESIGN · one group per division below,
     §1 to §10 · every count in one table is §11
```

## Content

### 1 · Delivery · Opening

**Opening, designed against live**: the three pages the group owes, the four the MISQ paper carries today, and the one that left on 260803.

```text
  🌱 DESIGNED · 3 pages, 1 family    📄 LIVE on MISQ · 3 pages  ✅ MATCHED
  ──────────────────────────────────────────────────────────────────
     S-Open-Seed    ✅ live · 📁 0-open/ · why the paper exists
     S-Open-Venue   ✅ live · 📁 0-open/ · which contract governs
     S-Open-Pitch   ✅ live · 📁 0-open/ · the promise to that venue

  🔠 the unit token IS the stage name (JL 260803), not a number
     the three stages are not members of one series, so there is
     nothing for a number to count; the word says which stage it is

  ✔ what left this group
     S-Venue-2-narrative  ➡️ Work, §2, on 260803
     S-Venue-3-decisions  🚫 removed 260803, rulings moved to §14.6
  ✅ no gap · unit: a stage · no control page · ruled by QB1
```

🌱 Establishes that Opening owes three stages across two families, that one live page is still one too many, and that the page it handed to Work has already gone.

#### 1.1 · Opening fixes the contract every later group is checked against, and it splits into nothing
(unit: a stage · seed, venue, pitch, and none of the three has parts)
Opening says why the paper exists and which venue contract governs every unit after it.
`§14.3` gives the test: a stage is per-unit exactly when one unit can be approved while another is rejected.
Each of these three stages produces one answer, so there is nothing here to approve one piece at a time.
Work is the other group that runs stages, and its resource and claims stages do pass that test, which is why A2.1 splits them and nothing splits these.

#### 1.2 · The one page that must still leave cannot simply be deleted
(`S-Venue-3-decisions` is live, and `§14` allows no central decision register)
Read off the live `board.md` on 260803, the group lists four pages and owes three.
The extra one is `S-Venue-3-decisions`, and `§14.6` rules that a decision belongs on the page that owns it, as a `Decision Now` row.
Five rulings carry a heading of their own on that file, D01, D05, D11, D15 and D16, its `state:` line says two of the five are still open, and those two carry three unanswered asks between them.
A1.1 in `## Aims` holds this gap, and it stays open until those five sit on the pages they bind.

#### 1.3 · The page this group lost landed exactly where the design wanted it
(`S-Venue-2-narrative` is now indexed under `Delivery · Work`, and it kept its `Venue` filename)
The live `board.md` lists narrative under `Delivery · Work`, so this group carries four pages today rather than the five `§11` counted before 260803.
The same move closed the neighbour's row: `§2` owes three pages, and Work now lists three.
Narrative keeping a `Venue` name inside a `Work` group is the disagreement kept on purpose, which `§12.1` argues and this group no longer owns.

#### 1.4 · Sixteen live pages are measured against a contract three pages here fix
(the venue pin sits on `S-Venue-0-venue.md`, and no later group writes it)
`§6.1` says a Main section is closed when it satisfies the venue contract fixed in this group.
On the live board that is 9 Main pages and 7 Appendix pages reading something they cannot change.
So a page sitting in this group that the group does not own costs more than a spare page would anywhere else, which is what `§1.2` is about.

#### 1.5 · This group spans two families, so it spans two folders, and owns neither outright
(family `Seed` in `0-seed/`, family `Venue` in `2-venue/`)
`§12.3` rules that a page sits in the folder its family names, so a group with two families has two folders.
Opening has both: `S-Seed-0-seed.md` sits in `0-seed/` and its other three live pages sit in `2-venue/`.
Neither folder is only this group's, because `0-seed/` holds 2 pages and one of them is `§3`'s, and `2-venue/` holds 4 pages and one of them is `§2`'s.
So a folder listing never tells a reader what this group holds, and `board.md`'s `## Pages` is the only place that does.

#### 1.6 · Its unit tokens stop at 1, and it has no control page to hold them
(units `0`, `0` and `1`, while unit `2` of family `Venue` is `§2`'s)
`§14.1` says a control page inventories a family's units, and `§12.2` says such a page takes a name instead of a unit.
Opening has none, because three different stages are not units of one series and there is nothing to inventory.
Reading family `Venue` in unit order walks out of this group at unit `2`, which is where narrative sits.
Five of the ten groups carry a control page in the design, and this is one of the five that does not.

### 2 · Delivery · Work

**Work, designed against live**: three pages owed, three present since 260803, and the ten those three still owe.

```text
  🧱 DESIGNED · 10 pages         📄 LIVE on MISQ · 10 pages  ✅ MATCHED
  ────────────────────────────────────────────────────────────────
     S-Work-R      control · which resources this paper has  🔴
     S-Work-R1     CMS Medicare Part D prescribing           🔴
     S-Work-R2     review-inferred perceived agreeableness   🔴
     S-Work-R3     the five first-pair cohorts               🔴
     S-Work-C      control · which claims this paper has     ✅ gated 260623
     S-Work-C0     the cohorts, exposure and outcomes exist  ✅
     S-Work-C1     the signal is beyond reputation           ✅
     S-Work-C2     the signal reaches high dose              ✅
     S-Work-C3     the signal is context-dependent           ✅
     S-Work-N      one paper, one arc, no split              ✅ gated 260624

  🔠 the letter says the STAGE, the number says the UNIT (JL 260802)
     R resource · C claims · N narrative, and N takes no number
     because there is nothing to approve one piece at a time
  📁 all ten in 1-work/ since 260803, when narrative came home
  ✅ no gap · unit: a resource, a claim, or the arc · ruled by QB2
```

🧱 Establishes that Work's page gap closed on 260803, that what is left is a shape rather than a missing page, and that this is the one group that will run two of `§11`'s shapes at once.

#### 2.1 · Work is the one group that will run two of the three shapes at once
(unit: a stage today; a resource, a claim, or the whole arc after A2.1)
`§14.3`'s test splits two of its three stages and leaves the third alone, so `§11`'s dash-plus-units shape and its one-page-per-stage shape both land inside this one group.
That gives Work two control pages, `S-Work-R` and `S-Work-C`, where every other group in `§11` has at most one.
Until the split lands the unit here is a stage, so a reader approves all three resources at once or none of them.

#### 2.2 · The arrival `§1` promised landed on 260803, so the page count matches
(one line in the paper's `board.md`, with no rename and no file move)
`## Pages` on the MISQ board now lists `S-Venue-2-narrative.md` under `Delivery · Work`, so three pages are owed and three are present.
The file itself never moved and is still `2-venue/S-Venue-2-narrative.md`, because the family and the filename did not change.
QB2 `§5.1` was written before that edit and still says two are live, so it is the stale side now.

#### 2.3 · Its three pages sit in two folders, and the folder never lies about which
(`1-work/` holds two of them, `2-venue/` holds the third)
Read off disk on 260803: `1-work/` holds `S-Work-0-resources.md` and `S-Work-1-claims.md`, and `2-venue/` holds `S-Venue-2-narrative.md`.
The folder follows the family and `§12.3` rules that, so a group spanning two families spans two folders and nothing about that is special to Work.
What is special is that the disagreement is kept on purpose here rather than being a trap, and `§12.1` argues why the family has to win.

#### 2.4 · The group is a chain inside itself and a fan-out at its end
(read off the three pages' own `requires:` and `provides:` lines on 260803)
`S-Work-0` requires `S-Seed-0` and `S-Seed-1`, `S-Work-1` requires `S-Work-0`, and `S-Venue-2` requires `S-Work-1` and `S-Venue-1`.
So the three cannot be approved in any order, and `S-Work-0` still reads `🔴 PROBE pending` while the two pages after it are gated.
`S-Work-1` provides the C0 to C3 ledger that `§3`, `§4` and `§6` read, and `S-Venue-2` provides the display requests that `§5` builds from.

#### 2.5 · Closing the shape gap is one paper's edit and no code change
(A2.1: the names compose and parse today, and no paper carries one)
`cli/stage.py`'s `FAMILIES` tuple already holds `Work`, so unlike `§3`, `§4` and `§10` this group waits on no new family.
Run on 260803, `resolve_filename("Work", "R", …)` returns `S-Work-R-resources.md` and `("Work", "R1", …)` returns `S-Work-R1-cms.md`, and `src/parse.py` matches both.
The same call rejects `Dash`, so Work's control pages can be composed while `S-Main-Dash` and `S-Display-Dash` cannot, which is the write side being narrower than the read side in `§13.4`.
What is left is splitting two live pages into nine, and A2.1 holds it.

### 3 · Delivery · Literature

**Literature, designed against live**: a dash plus one page per topic, against two pages borrowed from other families and two QB pages that describe one of them differently.

```text
  📚 DESIGNED · dash + 1 per topic   📄 LIVE on MISQ · 6  ✅ BUILT 260803
  ────────────────────────────────────────────────────────────────
     S-Literature-Dash        ✅   control · the four topics + the gap contract
     S-Literature-1           ✅   physician characteristics and behavior
     S-Literature-2           ✅   online reviews and visible reputation
     S-Literature-3           ✅   LLM-based construct measurement
     S-Literature-4           ✅   clinical discretion
     S-Main-2-literature      🔴   family Main, still in this group, ruled to stay
  📁 8-literature/ created 260803 · S-Seed-1 became the control page
  ✅ family ADMITTED and pages BUILT · unit: a topic · ruled by QB3
```

📚 Establishes that Literature owns no family and no stage, that it holds the board's only live family-against-group trap, and that it is the one group two QB pages currently describe differently.

#### 3.1 · A topic is the unit here because no stage is available to be one
(unit: a topic · `../../paper/route/haipipe-paper-stage/stages/index.yml` declares eight stages and none of them is literature)
Opening and Work can run one page per stage because `../../paper/route/haipipe-paper-stage/stages/index.yml` gives them seed, venue, pitch, resource, claims and narrative.
It declares nothing for this concern, so both live pages here were written by a stage another group owns: `seed` wrote one and `section-edit` wrote the other.
`§14.3` holds the test a unit has to pass, and `§11.2` files this group with the four others that split by unit rather than by stage.

#### 3.2 · It owns no family, so both of its live pages are borrowed
(`S-Seed-1-literature` sits in `0-seed/`; `S-Main-2-literature` sits in `4-main/`)
`§12.3` rules that a page's folder follows its family, so a group with no family has no folder of its own and this one spans two.
Of the three families the board still owes, `§13.6`, Literature is the only one that already has real pages: Value and Round hold one Q page each and have nothing to move.
So Literature is the only place where admitting a family also means renaming live files.
`S-Seed-1-literature` has an agreed destination, because QB3 rules that it becomes this group's control page.

#### 3.3 · This is where a reader files a page in the wrong group
(`S-Main-2-literature` is family `Main` sitting in group `Literature`, and `Main` is also a group)
The filename points at another group on this same board, which is what makes it a trap rather than a surprise.
`§12.4` separates this from the harmless cases and from the narrative disagreement, and that argument is not repeated here.
It is the only live case, so giving Literature its own family removes it from the board entirely.

#### 3.4 · The page stays here, and it keeps a filename that points somewhere else
(ruled 260803, after QB3 and QB6 had said opposite things for a day)
QB3 `§2.4` had said `S-Main-2-literature` "has gone back to `Delivery · Main`", QB6 `§2.2` said it stays here, and the live `board.md` had listed it here the whole time.
Two of the three agreed, so QB3's sentence was withdrawn and its new `§2.5` states the ruling with its reason.
The reason is `§12.5`: a group is one line a person moves inside `board.md`, while a family renames the file, moves it between folders, and breaks every id that cites it.
So this group keeps the board's one live trap on purpose, because removing it costs more than naming it does.

#### 3.5 · It sits between Work and Main, and both joins are live today
(receives what Work accepts from the discovery bank; feeds the sections Main closes)
The MISQ `board.md` Pipeline says accepted discovery answers return through Work and refresh both of the pages here.
QB6's contract lists Literature among what Main consumes, so a Main section cannot close until this group has accepted its sources.
The board order this page walks puts Literature after Work and before Value, Display and Main for exactly that reason.

#### 3.6 · Closing this gap needs a code change and a ruling, not a better name
(A13.2 holds the family, A3.1 holds the shape, A6.1 holds the borrowed page)
A13.2 landed on 260803, so `Literature` is in all six lists `§13.2` names and `S-Literature-Dash.md` composes and parses today; what is left is writing the pages.
A3.1 is QB3's own page work, and its State says the dash-plus-topics shape landed on 260802 while the trap is still unnamed there.
A6.1 is the ruling, and until someone makes it the two QB pages stay in disagreement and `S-Main-2-literature` stays where it is.

### 4 · Delivery · Value

**Value, designed against live**: a dash plus one page per topic, against one Q page that looks exactly like Present's and is not finished like it.

```text
  💰 DESIGNED · dash + 1 per topic   📄 LIVE on MISQ · 6  ✅ BUILT 260803
  ────────────────────────────────────────────────────────────────
     S-Value-Dash             🔴   control · the binding rule + inventory
     S-Value-1                🟡   headline LBP effect        ◀ claim C1
     S-Value-2                🟡   high-dose flags            ◀ claim C2
     S-Value-3                🟡   context gradient           ◀ claim C3
     S-Value-4                🔴   cohort and measure         ◀ claim C0
     QV0-value-delivery       🔴   the Q page that held it open, not yet retired
  📁 9-value/ created 260803 · ONE TOPIC PER CLAIM, because a Value topic
     IS the set of numbers one claim rests on
  ✅ family ADMITTED and pages BUILT · unit: a topic · ruled by QB4
```

💰 Establishes that Value and Present are the board's two look-alikes at one Q page each, and that only the per-unit test tells a reader which of them is finished.

#### 4.1 · Value and Present look identical from outside, and only one is finished
(the two facts a reader reaches for do not separate them)
`../../paper/route/haipipe-paper-stage/stages/index.yml` declares eight stages, and none of them is `value` or `present`, so neither group owns a stage.
No manuscript section belongs to either, because a Value number is printed inside Main or a caption and a deck is not a section at all.
Both facts are true of both groups, so a reader who stops there reads Value's row in `§11` as settled when it is not.
`§14.3` is the cut that works: Value's work splits into units that can be approved one at a time, and Present's does not, which `§8` argues on its own page.

#### 4.2 · Its unit is a topic, the same cut Literature takes
(a topic is the set of numbers one question produced)
A topic groups the work rather than the manuscript, so it does not line up with any section, figure or appendix letter.
Value and Literature are the only two of the ten groups whose unit is a topic, and both sit in the dash-plus-units shape `§11.2` calls the dominant one.
They are also two of the three rows `§11` marks family missing, with `Round` as the third, so the shape these two share is the one shape no paper can carry today.

#### 4.3 · One live Q page is standing in for the whole group
(`QV0-value-delivery.md` is the only file in `0-lifecycle/delivery-value/`)
The MISQ `board.md` lists that one page under `Delivery · Value`, and the folder on disk holds that one file.
Its state is 🔴 OPEN and its `Items to Finish` carries four unchecked items.
One of the four binds a single number, the Abstract's `12.90`, and another asks for a sweep of every quantitative sentence in the paper.
So one page is holding one unit's work and the whole group's rule at once, which is exactly what a dash plus topic pages would separate.

#### 4.4 · It sits between the group that asserts a number and the groups that print it
(`§2` accepts the run, `§5` and `§6` state the digits, this group holds the binding)
Work accepts the task answer that produced a number, and Display and Main are where a reader finally sees it.
Value owns nothing a reader sees, so its failures never surface on its own pages.
`QV0` names three pages it watches, `S-Work-1-claims`, `S-Main-0-abstract` and `S-Main-6-results`, sitting in two other groups.
The rule that makes the binding hold belongs to QB4 and is not restated here.

#### 4.5 · It had no family until 260803, and now the pages are simply unwritten
(`Value` is admitted in all six lists `§13.2` names, as of A13.2)
Until that day all six lists carried the same seven family names and `Value` was in none of them, so `S-Value-Dash.md` would not compose, would not parse as a page, and would not link from chat.
Run after the change, `resolve_filename("Value", "Dash", "")` returns `S-Value-Dash.md`, so nothing in the engine blocks this group any more.
What is left is authoring the control page and the topic pages, which is work rather than a blocker, and it is A4.1's own `Done when` that names the shape.

#### 4.6 · A4.1 was met on QB4 and this page did not notice
(checked by reading QB4 on 260803 rather than trusting the State row)
QB4 `§2` is drawn to the dash-plus-topics shape, and its figure lists a dash plus two topic pages.
A4.1's `Done when` also asks that QB4 stop calling itself a single-page concern, and QB4 `§2.2` is titled "Values have topics, so the concern splits by topic".
A4.1's State said QB4 had not been redrawn until this was found, which made it the third claim on this page to go stale with nothing checking it, after the join count and the page count that P1 already names.
QB8 `§2` still names Value as the same one-Q-page shape as Present, which is the confusion `§4.1` exists to stop and which nobody currently holds.

### 5 · Delivery · Display

**Display, designed against live**: a control page plus twelve display pages, matching exactly, and carrying the board's richest unit tokens.

```text
  🖼 DESIGNED · dash + 12           📄 LIVE on MISQ · dash + 12  ✅
  ─────────────────────────────────────────────────────────────────
     page in 3-display/                        unit token · §12.2
     S-Display-Dash                            Dash  a NAME, §14.1
     S-Display-1a-hero-concept                 1a
     S-Display-1b-research-design              1b
     S-Display-2a-distribution                 2a
     S-Display-2b-validation-summary           2b
     S-Display-2c-llm-measurement              2c
     S-Display-3a-funnel                       3a
     S-Display-3b-descriptives                 3b
     S-Display-3c-variable-operationalization  3c
     S-Display-4al2-main-regression            4al2  = 4a + a TAIL
     S-Display-4al5-main-regression            4al5  = 4a + a TAIL
     S-Display-4b-context-regression           4b
     S-Display-4c-discretion-gradient          4c
  ✅ no gap · 13 for 13 · unit: one display · ruled by QB5
```

🖼 Establishes that Display is the largest group on the board at thirteen pages, that it is the one place the dash-plus-units shape has been run at full size, and that its unit tokens are where `§12.2` is easiest to read.

#### 5.1 · One display is one approvable unit, which is the only reason this group is pages and not a page
(unit: one figure or table, and `§14.3` applied)
`§14.3` gives the test: a stage is per-unit exactly when one unit can be approved while another is rejected.
A display passes it, because one figure can be accepted while the figure beside it is still being rebuilt from a different run.
`S-Display-Dash` is a control page under `§14.1`, so it is the one of the thirteen that no stage writes.

#### 5.2 · It packages what Work claims and Value binds, and Main names it as evidence
(neighbours: `§2` and `§4` upstream, `§6` downstream)
The MISQ `board.md` says Display packages accepted claims and values, so `§2`'s claims and `§4`'s bound numbers arrive here already accepted.
The same registry says Main closes each section against accepted Literature, Value and Display evidence, so `§6` points at this group rather than restating what it holds.
A gap here would therefore surface twice: once as a number nobody packaged, and once as a section that cannot close.

#### 5.3 · Thirteen for thirteen is what makes this the worked example, not just another design
(`§11` marks four groups with no difference, and this is the biggest of the four)
The shape in `§11.2` asks for one control page plus one page per unit, and this group runs it at thirteen pages with nothing left over and nothing missing.
Literature and Value are drawn to that same shape in `§3` and `§4` and carry no unit page at all between them.
So the shape is not what those two are waiting on, because it has already been run at full size, and `§13.6` names what they are actually waiting on.

#### 5.4 · Its unit tokens are the richest evidence on the board for `§12.2`
(a number, a letter, a tail, and a name, all in one group)
`§12.2` says a unit may be lettered, numbered or named, and this is the group where all three sit side by side.
The twelve unit pages take a number for the block and a letter for the member, `1a` through `4c`, and the control page takes the name `Dash` because it is not a unit at all.
All thirteen filenames were run through the `src/parse.py:254` regex on 260803, and all thirteen returned the token drawn above.

#### 5.5 · `4al2` and `4al5` are one member written twice, and the code records why
(`4a` plus a tail, not a fifth and sixth member of block 4)
`src/parse.py:240` calls a number plus a letter plus a tail a VARIANT: the same claim and the same job under a different specification.
`src/parse.py:243` names the live case, that `S-Display-4al2` is `4a` on the binary trait_l2 exposure, and the two page titles read `Binary Exposure (trait_l2)` and `Continuous Exposure (trait_l5)`.
A variant inherits its parent's letter so that adding one renames nothing, which is the Appendix argument of `§12.2` applied one level further down.
It is also the one live name the chat layer cannot read back, which `§13.4` reports.

#### 5.6 · Family, folder and group all say Display, and that is not what keeps it clean
(`Display` the family, `3-display/` the folder, `Delivery · Display` the group)
`§12.4` sorts the family-against-group cases, and this group falls into none of them: every page in the group is family `Display`, and no other group holds one.
Main has the same three names agreeing and still lends `S-Main-2` to Literature, so a matching name is not the thing that stops the trap.
What stops it here is that no other concern wants one of these pages, which is a fact about the work and not about the naming.

### 6 · Delivery · Main

**Main, designed against live**: a dash plus nine sections, with one section away in Literature and two QB pages disagreeing about it.

```text
  📖 DESIGNED · dash + 9           📄 LIVE on MISQ · dash + 8
  ────────────────────────────────────────────────────────────────
     S-Main-Dash             ✅    S-Main-Dash
     S-Main-0-abstract       ✅    S-Main-0-abstract
     S-Main-1-introduction   ✅    S-Main-1-introduction
     S-Main-2-literature     ➡️    (indexed under Literature, §3)
     S-Main-3-theory         ✅    S-Main-3-theory
     S-Main-4-measurement    ✅    S-Main-4-measurement
     S-Main-5-empirical      ✅    S-Main-5-empirical
     S-Main-6-results        ✅    S-Main-6-results
     S-Main-7-discussion     ✅    S-Main-7-discussion
     S-Main-8-conclusion     ✅    S-Main-8-conclusion

  📁 4-main/ holds all TEN files on disk
     the folder follows the FAMILY, so only the GROUP differs, §12.3

  ⚖️ RULED 260803 · it stays indexed under Literature
     QB6 §2.2   sits under Literature, and that is correct  ◀ upheld
     QB3 §2.5   now says the same, with the reason
     board.md   indexes it under Delivery · Literature     ◀ live
  ⚠️ 1 page is away, on purpose · unit: one section · ruled by QB6
```

📖 Establishes that Main is one page per manuscript section, that the hole at `2` is a page the index has lent out, and that two QB pages still say different things about where it belongs.

#### 6.1 · Main's unit is one manuscript section, because a section is accepted whole
(unit: one section, `0` to `8`)
A reader meets a section as one argument, so it is accepted or sent back as one thing.
`§14.3` gives the test: a unit splits when one can be approved while another is rejected, and a section passes it, because Results can be settled while Discussion is still being written.
That is why Main is nine pages rather than one, and why `§11` files it with the four other dash-plus-units groups.

#### 6.2 · It is the last group that authors main-text prose, and it spends what four groups before it accepted
(consumes `§1`'s venue contract plus what `§3`, `§4` and `§5` accepted)
Opening fixes the venue contract every section is checked against.
Literature supplies the sources, Value supplies the numbers bound to their runs, and Display supplies the figures and tables a section points at.
After Main, `§7` holds the supplementary units, and `§8`, `§9` and `§10` only project, package and revise what Main has already fixed.
So a section cannot close before its evidence has, which is why Main sits sixth in the board order instead of first.

#### 6.3 · Its numbers are the argument, so it cannot letter its way out of a late unit
(`0` to `8`, against Appendix's `A` to `F` in `§7`)
`§7.2` says Appendix letters so a reviewer's late request lands as `G` and nothing citing `A` moves.
Main cannot borrow that, because where a section sits is part of what it claims.
A late Main section pushes every id after it, so adding one is a change to its neighbours and not only an addition.
That same rigidity is what makes an absent page visible, because the run cannot close up over a hole.

#### 6.4 · The gap at `2` is one page, and it is Main's only difference from the design
(dash + 9 designed, dash + 8 indexed, ten files on disk)
`board.md`'s `### Delivery · Main` lists nine pages: the dash plus `0`, `1`, `3`, `4`, `5`, `6`, `7` and `8`.
`S-Main-2-literature.md` is the tenth, and `### Delivery · Literature` lists it instead, next to `S-Seed-1-literature.md`.
The folder `4-main/` still holds all ten files, because a folder follows the family and never the group, which `§12.3` rules.
So nothing moved on disk, only the index differs, and that is the whole of Main's gap.

#### 6.5 · `Main` is the one family name that is also a group name
(which is what makes this single page the board's live trap)
`§12.4` rules that a family naming no group is normal and that a family which IS a group name is the trap, and this is the only live case of the second kind.
`§3.3` is where a reader actually meets it, because that is the group the page is indexed under.
Main is therefore the one group whose name a reader can read off a filename and still land in the wrong place.

#### 6.6 · Main's missing page is a loan, and on 260803 the loan was made permanent
(QB6 `§2.2` upheld; QB3's contrary sentence withdrawn into its new `§2.5`)
For a day QB6 said the page stays under `Delivery · Literature` and QB3 said it had come back here, while `board.md` indexed it under Literature throughout.
The live board and QB6 agreed, so QB3 was the stale one, and A6.1 closed by editing the page the ruling went against rather than by moving any file.
Main therefore keeps a permanent hole at `2`, and `§6.3` is why that hole stays visible: the numbers are the argument, so the run cannot close up over it.
Nothing about the file changed, because `§12.5` makes the group the cheap cut and the family the expensive one.

### 7 · Delivery · Appendix

**Appendix, designed against live**: a control page plus A to F, matching exactly, and the one control-page name the composer cannot write.

```text
  📎 DESIGNED · control + 6        📄 LIVE on MISQ · control + 6  ✅
  ────────────────────────────────────────────────────────────────
     S-Appendix-0-control    ⁉️    named `0-control`, not `Dash`
     S-Appendix-A-prompts    ✅
     S-Appendix-B-validation ✅
     S-Appendix-C-variables  ✅
     S-Appendix-D-iv         ✅
     S-Appendix-E-robustness ✅
     S-Appendix-F-bigfive    ✅
  ➕ the next unit is `G`, and nothing citing `A` moves · §12.2

  ⁉️ the THREE control pages, and the one name the composer can write
     S-Main-Dash             unit `Dash`     ✍️ stage.py REFUSES it
     S-Display-Dash          unit `Dash`     ✍️ stage.py REFUSES it
     S-Appendix-0-control    unit `0`        ✍️ stage.py composes it
  📖 parse.py reads all three · §13.4 argues the write-against-read split
  ✅ no gap · unit: one lettered unit · ruled by QB7
```

📎 Establishes that Appendix is the group a reviewer checks on its own, that matching page for page says nothing about whether the paper is ready, and that its control page carries the one name the composer cannot write.

#### 7.1 · A reviewer checks one lettered unit without reading the manuscript
(unit: one lettered unit, `A` to `F`, and one of them is approvable alone)
Appendix D can be accepted while Appendix E is still refused, which is the per-unit test in `§14.3`.
Here the unit a person approves and the unit a reviewer opens are the same object, which is not true of any other group.
That is why the group splits into a page per letter instead of holding all the back matter on one page.

#### 7.2 · Lettering is what lets a reviewer add a unit without moving anything
(`§12.2` owns why a unit is lettered; this says what it buys Appendix)
The live paper runs `A` to `F`, so a late request lands as `G` and nothing citing `A` moves.
Appendix is the only group whose unit count someone outside the project can change, so append-only naming matters more here than in `§5` or `§6`.
That makes `control + 6` what the paper carries today rather than a ceiling the group must stay under.

#### 7.3 · Main points into it, and Build ships it
(it holds what a reviewer must be able to check without reading the manuscript)
A section in `§6` cites a letter when its argument rests on evidence a reader should not have to take on trust.
So the prompts, the validation runs and the robustness checks live here, and the manuscript only refers to them.
`§9` then compiles both into one candidate, which is why a unit that is not ready blocks a submission and not just a section.

#### 7.4 · Matching page for page is evidence about the filing, not about the paper
(one of the four `none` rows in `§11`, next to Display, Present and Build)
Seven pages were designed and seven sit on disk in `5-appendix/`, so this shape needed no argument to get built.
What that shows is that a group with an admitted family and a folder of its own fills itself in, which is exactly what `§3`, `§4` and `§10` are still waiting for.
It does not show the appendix is ready, because QB7 records every MISQ unit refused at its gate today.
So the `none` in `§11` counts pages, and a reader must not take it as a green light.

#### 7.5 · Its control page is the only one not named `Dash`
(`S-Appendix-0-control` against `S-Main-Dash` and `S-Display-Dash`, all three live)
The live `board.md` registers three control pages, and two of them use `Dash` while this one uses `0-control`.
Read off disk on 260803: `resolve_filename()` at `cli/stage.py:260` refuses `Dash` as a unit at its `raise` on line 286, and `src/parse.py:254` accepts it through its `[A-Z][a-z]+` branch.
So `S-Appendix-0-control` is the one of the three the composer can produce, because it resolves as unit `0` with slug `control`.
`§13.4` argues that write-side against read-side split in general, and the fact this group adds is that the two candidate names are not equally cheap.

#### 7.6 · Nobody holds the naming question, and the table cannot show that
(no Aim on this page names it, and none of QB7's three does either)
QB7's Aims cover the gated source region, the group shape and the MISQ leaf split, and none of them mentions the control page's name.
This page carries no Aim for Appendix at all, and `§11` reads `none` for this row, so A11.1's sweep does not reach it either.
Nothing breaks while it stays open, because `§14.1` says no stage writes a control page, so the composer is never asked for one.
The two answers still cost different things: `Dash` is a change to `§13`'s composer, and `0-control` renames two live pages.

### 8 · Delivery · Present

**Present, designed against live**: one Q page and no S page, and the only group whose single Q page is a finished shape.

```text
  📣 DESIGNED · 1 Q page           📄 LIVE on MISQ · 1 Q page  ✅
  ────────────────────────────────────────────────────────────────
     QP0-present-delivery    ✅    QP0-present-delivery

  ❓ why no S page at all, now or ever
     `../../paper/route/haipipe-paper-stage/stages/index.yml` declares 8 stages and none is `present`
     no manuscript section belongs to it
     the work it causes happens in Display and Main
     `Present` is not one of the three families the board owes

  🔀 THREE groups read "1 Q page" live, and they are three states
     Present   ✅ FINISHED        no S page is ever owed   §8
     Value     ⚠️ UNFINISHED      topic pages are owed     §4
     Round     ⏳ EMPTY, correct  one page per batch owed  §10
  ✅ no gap · unit: none · ruled by QB8
```

📣 Establishes that Present is the one group finished at a single Q page, and separates it from the two groups that show one Q page for entirely different reasons.

#### 8.1 · Present is the only group that owes no S page, now or ever
(unit: none, and `../../paper/route/haipipe-paper-stage/stages/index.yml` names 8 stages with no `present` among them)
`../../paper/route/haipipe-paper-stage/stages/index.yml` declares seed, resource, claims, venue, pitch, narrative, display and section-edit, and that is the whole list.
No manuscript section belongs to Present either, so there is no per-unit thing an S page could hold.
The board owes three families, `Literature`, `Value` and `Round`, and `Present` is not one of them, because no S page will ever ask for one.

#### 8.2 · One Q page is three different states, and this is the only place all three are visible
(Value in `§4`, Present here, Round in `§10`)
Present is FINISHED at one Q page, because nothing more is owed.
Value is UNFINISHED at one Q page, because it owes a control page plus one page per topic and the family that would carry them does not exist.
Round is EMPTY AND CORRECT at one Q page, because no batch page should exist before the paper is reviewed, and it separately lacks a family.
QB4, QB8 and QB10 can each state only their own case, so the comparison exists nowhere but here.

#### 8.3 · A reader who merges the three will read the `§11` table wrong
(the live column says "1 Q page" three times, and the difference column is where they split)
Present's difference reads none, while Value's and Round's both read family missing.
Read by the live column alone, the table shows three unfinished groups when only two of the three are.
That misreading is the one failure this division exists to prevent.

#### 8.4 · It is the only group that consumes other groups and writes nothing back
(it projects what `§5` Display and `§6` Main already hold)
Slides and posters are renderings of pages that were already accepted somewhere else.
No manuscript page is built from a Present page, so nothing here can become a second source of truth for a claim.
`§14.3` asks whether one unit can be approved while another is rejected, and here there is no unit for that test to run on.

#### 8.5 · Having no family is why its folder is named after the concern
(`delivery-present/` holds 1 file, next to eight numbered family folders)
`§12.3` says a page's folder follows its family, and a Q page has no family for a folder to follow.
So `0-lifecycle/` holds eight numbered family folders plus `delivery-present/` and `delivery-value/`, which are named after their concern instead.
`QR0-round-delivery.md` is the odd one out in `7-round/`, a family folder for a family that is not admitted, and nobody has ruled which of the two namings is right.

#### 8.6 · A finished shape and a finished page are different questions
(`QP0-present-delivery.md` carries `state: 🔴 OPEN` and three unticked items)
The shape is settled, because this group will never carry a page it does not have today.
The page itself is open, because this paper has no talk scheduled and no poster registered, which is a state that will change.
A reader should conclude that nothing is missing here, and should not conclude that the work is done.

### 9 · Delivery · Build

**Build, designed against live**: four fixed pages, reused every round, matching exactly.

```text
  🏗 DESIGNED · 4 pages            📄 LIVE on MISQ · 4 pages  ✅
  ────────────────────────────────────────────────────────────────
     S-Submission-0-reconcile ✅   four ORDERED MOVES, not four
     S-Submission-1-compile   ✅   units: compile runs on what
     S-Submission-2-review    ✅   reconcile produced, so no one
     S-Submission-3-submit    ✅   of them settles on its own

  🏷 family Submission · group Build · folder 6-submission/
     🟢 Submission names NO group, so it traps nobody, §12.4
     ✅ and it IS an admitted family, unlike §3, §4 and §10
     🔒 23 live pages cite these ids · a rename moves them all
        14 in Display · 7 in Main · 2 in Venue

  🔁 §10 Round returns INTO this group, the only backward arrow
     on the board, and reuses these same four pages
  ✅ no gap · unit: none, nothing grows · ruled by QB9
```

🏗 Establishes that Build is a fixed set of four ordered moves rather than a growing one, and that it is the only group matching its design exactly while carrying another family's name.

#### 9.1 · Nothing grows here, because the four pages are one sequence and not four units
(unit: none, and the same four are reused every round)
Reconcile, compile, review and submit are four moves in one order, and no one of them can be settled while the one before it is rejected.
That is `§14.3`'s per-unit test failing, which is why the unit is none and the page count is fixed.
A paper on its third round still carries these four and not twelve.
`§11` puts Build in the fixed-set shape with `§8` and `§10`, and it is the only one of the three fixed at more than one page.

#### 9.2 · Four designed and four live, and it is the only exact match with a borrowed family name
(`§11` shows four groups with no gap, and Build is the only one whose pages are not named after it)
The live `board.md` lists four pages under `Delivery · Build`, and `6-submission/` holds exactly those four files.
Display and Appendix also match their design, and their pages carry their own group's name.
Present matches too, on a Q page that carries no family at all.
So Build is the one place a reader sees a clean group and a different family name at the same time.

#### 9.3 · The live board explains the difference at the point a reader meets it
(the group heading and the line under it both say so)
`§12.4` sorts the family-against-group cases, and Build sits in the harmless one.
What Build adds is where the explanation sits: the live group heading reads `### Delivery · Build (includes Submission and distribution)`.
The line under it says the historical `S-Submission` ids stay and that Build is the broader concern that now owns them.
A reader never has to leave the board to find out why the two names differ, which is exactly what `§3`'s trap does not offer.

#### 9.4 · The ids were kept so that nothing citing them moves
(the same argument `§12.2` makes for Appendix letters, applied to a group instead of a unit)
`§12.2` keeps Appendix lettered so a late unit lands as `G` and nothing citing `A` moves.
Build makes that trade one level up: the concern was widened and the four page ids were left alone.
Counted off the MISQ paper on 260803, 23 live pages outside `6-submission/` name an `S-Submission` id, 14 of them in Display, 7 in Main and 2 in Venue.
A stable id that no longer matches its group is cheaper than the 23-page edit a rename would force.

#### 9.5 · Build is where the board's only backward arrow lands
(ninth of ten, and the one group a later group returns to)
On the live `board.md` Board Map every forward arrow ends at Build, and the `§10` Round arrow leaves Build and comes back into it.
`board.md` says in words that a round loops through the affected pages and Build rather than running once at the end.
So the fourth page is not the end of the board, and the same four run again on every return.
That is why `§10` adds a dated page per batch and Build adds none.

#### 9.6 · Nothing about this group's page list is open
(no Aim on this page names Build, and that is correct rather than an oversight)
Three of the ten groups have no Aim here: Build, `§5` Display and `§7` Appendix.
`Submission` is one of the seven admitted families, so these four pages parse, sort on the Index and link in chat today, which is what `§3`, `§4` and `§10` are still waiting for.
QB9 carries four open items of its own, and not one of them adds or removes a page from this list.
So Build is settled at the layout altitude this page works at, and unsettled only at the altitude QB9 works at.

### 10 · Delivery · Round

**Round, designed against live**: one Q page plus one page per review batch, and the two separate reasons no batch page exists yet.

```text
  🔁 DESIGNED · 1 Q page + 1 per batch  📄 LIVE on MISQ · 1 Q page
  ────────────────────────────────────────────────────────────────
     QR0-round-delivery       ✅    QR0-round-delivery
     S-Round-1-<batch>        ⏳    no batch has happened yet
     S-Round-2-<batch>        ✍️    composes today, since 260803

  ❓ TWO reasons at once, and only the second one is a defect
     ⏳ no review has arrived, so 0 batch pages are owed today
     ✅ Round was admitted to all 6 lists on 260803, so this half is
        CLOSED and only the first reason is left
  📁 7-round/ exists and holds the Q page: a family-named folder for
     a family no file admits, and nobody has ruled that
  ⏳ correctly empty · unit: one review batch · ruled by QB10
```

🔁 Establishes that Round is empty for two reasons at once, that only one of them is a defect, and that only one of them will fix itself.

#### 10.1 · One review batch is the approvable unit, and neither a reviewer nor an edit is
(unit: one review batch: feedback, decisions, edits, response, rebuild, resubmission)
`§14.3` gives the test: a unit is real exactly when one of them can be approved while another is rejected.
A batch passes it, because round two can be wide open while round one is closed and already shipped.
A reviewer fails it, because one edit answers two reviewers at once and there is no way to accept half of that edit.
An edit fails it from the other side, because an edit is one move inside an answer rather than a thing a human gates.

#### 10.2 · Empty is correct today, and this half closes on its own
(no review has arrived, so no batch page is owed)
`board.md` lists one page under `Delivery · Round`, `QR0-round-delivery.md`, and no S page at all.
The paper has not been reviewed once, so a batch page written today would record something that did not happen.
The day reviews arrive this half closes with nobody writing any line of code, and QB10 rules it.

#### 10.3 · The other half was a defect, and it was closed on 260803
(`Round` is now in all six family lists, so a batch page can be written the day one is owed)
Until that day the six lists `§13.2` names admitted seven families and `Round` was in none of them, so `S-Round-1-<batch>.md` was a string the composer could not produce and the readers would not parse.
A13.2 admitted all three owed families at once, and `resolve_filename("Round", "1", "first-review")` now returns `S-Round-1-first-review.md`.
So this group is down to one reason for being empty, and it is the reason that is correct.

#### 10.4 · From outside the two halves look the same, so `§8` and `§4` are the two ways to read one Q page
(Present is finished at one Q page; Value is unfinished at one; Round is both at once)
`§8` shows a group that will never owe an S page, so its single Q page is the answer rather than a step toward one.
`§4` shows a group with real per-topic work waiting on a family, so its single Q page is a placeholder.
Round reads like `§8` on the surface and like `§4` underneath, which is why a reader who only counts pages cannot tell the two apart here.
The `§11` table records Round's difference as `family missing`, and that phrase names the defect half only.

#### 10.5 · Round runs back through the board rather than after it
(the ten divisions read in board order, and this one is not the end of that line)
A batch reopens whichever earlier pages it touched and then goes back out through `§9`, which is where the board order stops being a sequence.
Round is also the only group whose page count grows on an event nobody inside the paper controls.
That is what makes its empty state a fact about the outside world rather than a fact about the work.

#### 10.6 · Its folder is named after a family the code does not admit
(`7-round/` on disk, against `delivery-present/` and `delivery-value/`)
`0-lifecycle/` holds eight numbered folders named after families and two named after their concern, and `7-round/` is one of the eight.
It exists today and holds `QR0-round-delivery.md`, so a folder stands ready for a family that no file has heard of.
`QP0` and `QV0` sit in `delivery-present/` and `delivery-value/` instead, so the three Q pages of `§4`, `§8` and `§10` are filed by two different rules.
Nobody has ruled which rule is right, and `§12.3` states its folder-follows-family rule about S pages rather than about these.

### 11 · The ten at a glance, and the three shapes they sort into

**Designed against live**: every group's count in one place, recounted off the live `board.md` on 260803, and the shape each group runs.

```text
  group       DESIGNED, in §Diagram  LIVE on MISQ today   the difference      held by
  ─────────────────────────────────────────────────────────────────────────────────────
  Opening     3 pages                4 pages              1 page must leave   A1.1
  Work        control+units ×2 + 1   10 pages             none, since 260803
  Literature  dash + topics          dash + 4             none, since 260803
  Value       dash + topics          dash + 4 + QV0       none, since 260803
  Display     dash + 12              dash + 12            none
  Main        dash + 8               dash + 8             none, since 260803
  Appendix    control + 6            control + 6          none
  Present     1 Q page               1 Q page             none
  Build       4 pages                4 pages              none
  Round       1 Q page + 1 per batch 1 Q page             none, correctly empty
  ─────────────────────────────────────────────────────────────────────────────────────
  📐 61 live pages on the evening of 260803, up from 45 that morning: Work split
     3 ▸ 10, Literature grew 2 ▸ 6 and Value 1 ▸ 6, once the three owed families
     were admitted. 2 rows still show a gap, and each points at an Aim
```

🧭 Establishes what all ten groups owe against what one paper carries today, and shows that five rows differ, in three kinds, with nobody's gap left unowned.

**The three shapes**: the ten groups above sort into three, and one gate question decides which, not size.

```text
  🔑 THE TEST, from QC3b's Law: a stage is per-unit exactly when one unit
     can be approved while another is rejected
     ⚖️ size does not decide: Build has 4 live pages and never grows,
        Literature has 2 live pages and grows one per topic

  🗂 A DASH PLUS ONE PAGE PER UNIT    the test says YES · five groups
     Delivery · Literature   one per TOPIC                 ◀ QB3 · §3
     Delivery · Value        one per TOPIC                 ◀ QB4 · §4
     Delivery · Display      one per DISPLAY UNIT          ◀ QB5 · §5
     Delivery · Main         one per SECTION               ◀ QB6 · §6
     Delivery · Appendix     one per LETTERED UNIT         ◀ QB7 · §7

  🏗 ONE PAGE PER STAGE               the test says NO · two groups
     Delivery · Opening      seed · venue · pitch          ◀ QB1 · §1
     Delivery · Work         resource · claims · narrative ◀ QB2 · §2
        ⚠️ 2 of Work's 3 stages now answer YES, which A2.1 holds

  📄 A FIXED SET, OR ONE Q PAGE       no unit to test today · three groups
     Delivery · Build        four submission pages, reused ◀ QB9 · §9
     Delivery · Present      one Q page                    ◀ QB8 · §8
     Delivery · Round        one Q page + one per batch    ◀ QB10 · §10
        ⚠️ Round's unit only exists once a review batch arrives
```

#### 11.1 · One gate question sorts the ten, and the page count never does
(the QC3b test: per-unit exactly when one unit can be approved while another is rejected)
A group takes the dash-plus-units shape when a human can accept one of its units and reject the next one.
A group runs stage pages when its work closes once and cannot be signed off a piece at a time.
Size is not the test: Build carries 4 live pages and never grows, while Literature carries 2 and grows one per topic.
The rule is QC3b's Law, and `§14.3` is where this page restates it.

#### 11.2 · The shape holds across five groups, and only the name of the unit changes
(topic, display unit, section, lettered unit: four words for one structure)
Literature and Value count topics, Display counts displays, Main counts sections, and Appendix counts lettered units, and all five run one control page plus one page per unit.
A reader who learns one of the five can read the other four, because the control page and the unit pages do the same job in each.
What the unit is called then decides whether the filename carries a letter, a number or a word, which `§12.2` owns.
A group can also change shape, so A2.1 would move Work into this first bucket and make it the sixth.

#### 11.3 · Three cells in this table were wrong on 260803, and are corrected here
(the `S-Venue-2-narrative` move landed after the table was first built)
`S-Venue-2-narrative` moved in the live `board.md` from `Delivery · Opening` to `Delivery · Work` on 260803, so two rows were recounted line by line.
Opening now reads 4 live pages with 1 page that must leave, where this table had said 5 pages and 2 pages leave.
Work now reads 3 live pages and matches its design exactly, where this table had said 2 pages and 1 page arrives.
Round's designed cell is corrected to 1 Q page plus one per batch, because it had read 1 Q page against an identical live cell and still claimed a difference.

#### 11.4 · Five rows show a gap, in three kinds, and one Aim holds three of them
(a page that must leave, a page that is away, and three groups whose family the engine does not admit)
Opening's gap is a page that must leave, and A1.1 holds it, with the first half of its Done-when satisfied by the 260803 move and the second half still open.
Main's gap is a page that exists on disk and is indexed under another group, and A6.1 ruled on 260803 that it stays there, so the row is now a permanent loan rather than an open question.
Literature, Value and Round all read `family missing` until 260803, when A13.2 admitted all three; Literature and Value now read `pages not written` and are held by A3.1 and A4.1, and Round's row closed.
A3.1, A4.1 and A10.1 look like the owners of those three rows and are not, because each closes a QB page's drawing rather than the live paper, so no row here is left with nobody holding it, which is what A11.1 asks.

#### 11.5 · Three groups read `1 Q page` and mean three different things
(Value, Present and Round share a live cell and share nothing else)
Present is finished at one Q page, and `§8` gives the two facts that make it so.
Value is stuck at one Q page with per-topic work waiting, so its cell is a placeholder, `§4`.
Round is correct at one Q page today and blocked at the same time, and `§10` separates the two reasons.
So the live column counts pages and not progress, and a finished group and a blocked group are the same number in it.

#### 11.6 · A `none` row means the two lists match, and says nothing about the work
(which is why `§1` to `§10` sit below this table rather than instead of it)
Work reads `none` today and still owes the per-unit split A2.1 holds, because that split is not in the designed column either.
`S-Main-2-literature` is one file counted inside Literature's 2 and absent from Main's 9, so a single page moves two rows at once and the live total is 45 rather than 46.
The design names 48 pages: six were never written and three live pages are not in it, and 48 minus 6 plus 3 gives the 45 that `## Pages` and the family folders both hold.
A count also hides which family wrote a page, and `§12` is where that is read off the filename instead.

### 12 · What a filename says, and what it does not

**Three cuts over one page**: what the folder, the family and the group each say, and which one a reader gets wrong.

```text
  S-<Family>-<unit>-<slug>.md
    │         │       └── short lowercase name
    │         └────────── which unit, within the family
    └──────────────────── WHO WROTE IT, never who owns the rule

  🔠 the UNIT token · five forms, read in this order by parse.py:254
     4al2   a variant of a lettered member    S-Display-4al2-…
     0      a number, one letter optional     S-Main-0-abstract
     R1     a capital plus digits, JL 260802  S-Work-R1-…
     A      one capital                       S-Appendix-A-prompts
     Dash   a word: not a unit at all         S-Main-Dash

  🧭 THREE CUTS over one page, S-Main-2-literature
     📁 FOLDER   4-main/                  declared beside the family
     🏷 FAMILY   Main                     composed into the filename
     🗂 GROUP    Delivery · Literature    typed by hand into board.md
     only the GROUP has its own author, so only the GROUP can differ

  🟢 a family NO group is named after      common, and harmless
     S-Seed-1-literature      family Seed        ▸ group Literature
     S-Venue-1-pitch          family Venue       ▸ group Opening
     S-Submission-1-compile   family Submission  ▸ group Build

  ⚰️ a family that IS another group's name  the trap · NONE live
     S-Main-2-literature was the only one, and JL removed it 260803

  ⚰️ the disagreement once kept BY DESIGN, now retired
     S-Venue-2-narrative  ▸  S-Work-N, renamed 260803
     ↳ it existed because the FAMILY was thought to be the only
       record of venue-alignment; `stage.md` declares it in words

  🎨 the FAMILY answers what the group cannot: does a RETARGET
     rewrite this page?
     venue-FREE      0-seed/ · 1-work/
     venue-ALIGNED   2-venue/ · 3-display/ · 4-main/ · 5-appendix/
     no stage        6-submission/ · nothing answers for it

  🔑 what a name MEANS is here · how a name is MADE is §13
```

🔤 Establishes what each of the three cuts over a page means, names every live case where the family and the group differ, and says which of the two wins when they do.

#### 12.1 · The family carries a fact the group cannot
(venue-FREE against venue-ALIGNED: does a retarget rewrite this page?)
Four stage contracts declare `venue_aligned: true`, pitch, narrative, display and section-edit, and a retarget rewrites every page they wrote.
The seed, resource and claims contracts declare nothing there, because what a paper needs in order to exist does not depend on where it is sent.
The family sorted pages onto the two sides of that line, and this page used to say the filename was the ONLY thing that did. That was wrong, and renaming Opening to the `Open` family on 260803 is what exposed it: each stage's own `stage.md` declares `venue_aligned: true` in words, with a comment saying what it means, so a page that stops carrying `Venue` in its name loses nothing.
That is why `S-Venue-2-narrative` keeps `board_family: Venue` even though `§2` owns the arc, and the live `board.md` now carries that reason in one sentence under `Delivery · Work`.

#### 12.2 · A unit is lettered, numbered, named, or a capital plus digits
(Appendix letters so a late unit renumbers nothing; Main numbers because order is the argument)
Appendix uses `A` to `F`: a reviewer's late request lands as `G` and nothing citing `A` moves.
Main uses `0` to `8`: a section's position is part of what it claims.
Display adds a variant form, where `4al2` and `4al5` are the same member `4a` under two specifications, so adding one renames nothing.
A capital plus digits is a member of a lettered series (JL 260802), where `S-Work-R` is the control page and `S-Work-R1` is one resource, and a capitalised word like `Dash` marks a page that is not a unit at all.

#### 12.3 · The folder on disk follows the FAMILY, never the group
(so a group that spans two families also spans two folders)
`0-lifecycle/` holds one subfolder per family, seven folders for the seven admitted families, `0-seed/` through `6-submission/`, and read off disk on 260803 all 42 S pages sit in the folder their family names with no exception.
`S-Venue-2-narrative.md` is in `2-venue/` while `Delivery · Work` owns it, and `S-Main-2-literature.md` is in `4-main/` while `Delivery · Literature` owns it, and `board.md`'s own `## Links` block records both of those paths.
A Q page carries no family token at all, so nothing composes its folder name: `delivery-present/` and `delivery-value/` are named after their concern, and `7-round/` after a family slot that has no family.
Nobody has ruled which of those two habits is right, and it costs little today because the group is the only cut that ever moves, which `§12.5` argues.

#### 12.4 · Two different things have been called "the join", and only one is a problem
(a family with no group of its own is normal; a family that is also another group's name is the trap)
Seed, Venue and Submission name no group, so a page of theirs sitting in Opening, Work, Literature or Build surprises nobody.
The trap is a family whose name IS a group, because a reader then files the page in the wrong group without noticing: `S-Main-2-literature` is family `Main` sitting in `Delivery · Literature`, and it is still the only live case.
Narrative used to be a third thing, a disagreement kept ON PURPOSE, and on 260803 it stopped being one: `S-Venue-2-narrative` became `S-Work-N-narrative` and moved into `1-work/`, because the reason for the split was `§12.1`'s claim that only a filename records venue-alignment, and each stage's `stage.md` records it in words instead.
On 260803 JL removed `S-Main-2-literature` outright, so the trap category is now EMPTY on this board: every S page's family names its own group, except the `S-Submission` pages in Build, which are the harmless kind because `Submission` names no group.
Counting all three together is what produced four numbers for one fact on this page before 260802.

#### 12.5 · The group is the only one of the three cuts with its own author
(the folder and the family come out of one contract; the group is typed into `board.md`)
A stage contract declares `board_family` and `artifact:` side by side in one block, and `cli/stage.py` composes the filename from the first, so the folder and the family cannot drift apart on their own.
A group is a `###` heading a person types into `board.md`'s `## Pages`, in a different file, and no program compares the two.
So regrouping is cheap and refamilying is not: `S-Venue-2-narrative` changed group on 260803 by one line moving inside `board.md`, and no file moved and no id changed.
A family change would instead rename the file, move it between folders, and break every link and every `§` reference that cites the old id, which is why the group is the cut that gives way.

#### 12.6 · When the two disagree, the group says what the page owes and the family says what the file does
(read `## Pages` for the rule, read the filename for the file)
Look up the group in `board.md`'s `## Pages` to learn which concern gates the page, what it must carry, and which QB page rules it.
Read the second token of the filename to learn where the file sits, which stage rewrites it, and whether a retarget touches it at all.
Never infer one from the other, because they are written in two files by two hands, which `§12.5` explains.
A group holding a page from another family owes the reader one sentence saying so, and the live `board.md` carries such a sentence under `Delivery · Work`, under `Delivery · Main` and under `Delivery · Build`, but not under `Delivery · Literature`, which is the one group where a reader can actually be trapped.

### 13 · How a filename is made

**Write side against read side**: three declared fields, one composer, and the six lists that must already know the family.

```text
  ⚙️ WRITE · three declared fields, one composer
     stages/<dir>/stage.md      board_family: Venue
     (8 stage folders; the      board_unit:   2
      index.yml beside them     board_slug:   narrative
      declares none of them)
            │
            ▼  cli/stage.py:260   resolve_filename()
     📄 S-Venue-2-narrative.md   ← no file holds this string
     🚫 gated by cli/stage.py:27, the FAMILIES tuple

  📖 READ · FIVE more closed lists, five different failures
     src/parse.py:247       is this a page?  🔇 the file vanishes, silently
     src/parse.py:301       sort order       💥 KeyError, the build dies
     src/page_board.py:497  Index sections   🔀 parses, sorts into none
     live/chat.py:201       page id + focus  ⛔ every reply ends blocked
     check-contracts.py:40  declared family  🔔 the ONE that says why

  ⚖️ the two sides do not accept the same unit token
     Dash    reader ✅ parse.py:254   composer 🚫   S-Main-Dash is live
     4al2    composer ✅              chat.py 🚫 → S-Display-4, blocked

  🧩 5 of the 6 sit in  board/haipipe-board/
     the 6th sits in      paper/route/haipipe-paper-stage/
     and its bridge is BROKEN today: it imports
     board/haipipe-board/stage.py, which is now cli/stage.py

  📝 3 more restatements enforce nothing: index.yml:7 · CONTRACT.md:26
     · SKILL.md:95, which already names only six of the seven
```

⚙️ Establishes that a filename is composed rather than written, that the family set is closed in six places and not five, and that the write side and the read side do not accept the same unit.

#### 13.1 · A filename is composed from three declared fields, and nothing on disk holds the result
(each stage's own `stage.md` declares three fields, and one function joins them)
Each of the eight stage folders declares `board_family`, `board_unit` and `board_slug` in its own `stages/<dir>/stage.md` frontmatter, and `../../paper/route/haipipe-paper-stage/stages/index.yml` carries none of the three, only `key`, `order`, `dir`, `migrated` and `triggers`.
`resolve_filename()` at `cli/stage.py:260` is the one function that joins them into `S-<Family>-<unit>-<slug>.md`, and this page used to pin that function to line 27, which is where the `FAMILIES` tuple sits rather than the composer.
So `§12`'s grammar describes what the composer produces, and is not a rule written down anywhere for the composer to follow.
A page written by hand can carry a name the composer would never produce, and nothing compares the two.

#### 13.2 · Six lists close the family set, and this page's own Law said five
(`cli/stage.py:27`, `src/parse.py:247`, `src/parse.py:301`, `src/page_board.py:497`, `live/chat.py:201`, `check-contracts.py:40`)
The one the Law missed is `src/parse.py:301`, a second list inside the same file as the first: the regex at 247 decides whether a file is a page at all, and the `family_order` dict that ends `}[family]` at 301 decides where it sorts.
That one is the loudest of the six, because a name it lacks raises a `KeyError` that stops the whole board build rather than losing one page, and the message names a Python key instead of the problem.
On 260803 the sibling page `QB3-literature.md` said the list was closed in three places and named three, and the two it left out were `src/page_board.py:497` and `live/chat.py:201`, which are exactly the two that fail with no message at all.
`QB4-value.md` carried the same undercount in three places on the same day, so the miss this division warns about has now happened twice on two different pages.

#### 13.3 · A missing name fails differently in every file, and only one failure tells a person anything
(what someone actually sees, list by list)
`src/parse.py:247` decides the file is not a page, so it disappears from the board with no warning line anywhere.
`src/page_board.py:497` leaves the page parsed and outside every Index section, so a reader who knows it exists still cannot find it in the list.
`live/chat.py:201` supplies the `--focus` value for that page's own chat session, so `status.py` refuses it and every reply of that session closes blocked.
Of the five files that read a name back, `check-contracts.py:40` is the only one that says what is wrong, printing that the declared family is not a family and exiting 1.

#### 13.4 · The two sides accept different units, in both directions, and live pages sit in the gap
(`resolve_filename()` refuses `Dash`; `live/chat.py:201` refuses `4al2`)
`cli/stage.py` raises at line 286 for the unit `Dash`, listing the five forms it does take, while `src/parse.py:254` ends its unit alternation with `[A-Z][a-z]+` and reads `Dash` without complaint.
`4-main/S-Main-Dash.md` and `3-display/S-Display-Dash.md` are both live on the MISQ board, so two control pages exist that the tool owning the name cannot recreate.
The other direction is worse, because `live/chat.py:201` stops the unit at `\d+` or one `[A-Z]` and truncates rather than refusing: run on 260803, `S-Display-4al2-main-regression` returns `S-Display-4`, `S-Work-R1-cms` returns `S-Work-R`, and `S-Main-Dash` returns `S-Main-D`.
None of those three is a page id, and `S-Display-4al2` is a name the composer itself produces, so the write side and the read side already disagree on a page the MISQ paper carries today.

#### 13.5 · The sixth file is in another skill, and the bridge between the two skills is broken
(five lists in `board/haipipe-board/`, one in `paper/route/haipipe-paper-stage/`)
Someone adding a family works inside the board engine, finds five lists there, and has no reason to open the paper skill, which is why the Law names paths instead of saying "five places".
The paper skill reaches back by hard path, and `check-contracts.py:26` names `board/haipipe-board/stage.py`, a file that now lives at `cli/stage.py`, so running the checker on 260803 ends in a traceback before it reads a single contract.
So the only file that reports an unknown family does not run at all today, which is why nothing has told anyone about the `Dash` gap or the chat truncation.
Three more places restate the seven names and enforce nothing: `stages/index.yml:7` in a comment, `stages/CONTRACT.md:26` in a field table, and `SKILL.md:95`, which has already drifted to six by dropping `Submission`.

#### 13.6 · Which is why the three owed families are a code change, held by A13.1 and A13.2
(`Literature`, `Value` and `Round`, the groups `§3`, `§4` and `§10` mark family missing)
A13.1 asks for one declaration every file reads, which means the six lists become one exported constant plus five uses of it: `src/parse.py` building both its regex and its sort order from it, `src/page_board.py` building its Index sections, `live/chat.py` building its id regex, and `../../paper/route/haipipe-paper-stage/check-contracts.py` importing it instead of spelling its own set.
A13.2 landed on 260803 by editing all six by hand, and both boards were rebuilt and their page lists diffed to prove nothing existing moved.
Before that, an `S-Literature-1-<topic>.md` file would not have been a page, would have had no place on the Index, and would have made its own chat session report blocked.
Writing a group heading into `board.md` still costs nothing and still admits no family, which is why A13.1 is the one that matters: six hand-edited lists is the same defect waiting to happen again.

### 14 · The three page kinds inside a group

**What may sit in a group**: three kinds of S page, the Q page that is not one of them, and the kind that is abolished.

```text
  🔤 WHAT MAY SIT IN A GROUP · and how much of it a filename shows
  ════════════════════════════════════════════════════════════════
  🗂 a CONTROL PAGE · the family's inventory · no stage writes it
     S-Display-Dash                      which displays exist
     S-Main-Dash                         which sections exist
     S-Appendix-0-control                ⁉️ a third name · §7.5

  📑 a PER-UNIT PAGE · approvable while its neighbour is not
     S-Main-1-introduction               unit: one section
     S-Appendix-D-iv                     unit: one lettered unit
     S-Display-3a-funnel                 unit: one display

  📄 a STAGE PAGE · one stage that runs once, one page
     S-Work-1-claims                     stage: claims
     S-Venue-2-narrative                 stage: narrative
     ⚠️ the filename does NOT separate this kind from the one above

  ❓ a Q PAGE · not an S page · no family, no stage, no gate
     QV0-value-delivery                  ◀ Value · §4
     QP0-present-delivery                ◀ Present · §8
     QR0-round-delivery                  ◀ Round · §10

  🕳 FITS NO KIND · no stage, no inventory, no unit
     S-Submission-0-reconcile            ◀ Build · §9
     S-Submission-1-compile
     S-Submission-2-review
     S-Submission-3-submit
     S-Seed-1-literature                 ◀ Literature · §3

  🚫 ABOLISHED · no central decision register (JL 260802)
     S-Venue-3-decisions                 5 rulings · 2 open · 3 asks

  🔢 45 pages live · 21 named by a stage contract
     12 display units, whose stage still declares one page
     12 answer to no stage at all
```

🗂 Establishes the three kinds of S page a group may hold, the Q page that is not one of them, and the five live pages that fit no kind at all.

#### 14.1 · Every stage makes a page, and twelve live pages come from no stage
(counted off `board.md`'s `## Pages` against `../../paper/route/haipipe-paper-stage/stages/index.yml` on 260803)
`../../paper/route/haipipe-paper-stage/stages/index.yml` declares eight stages, and the six that run once each name exactly one live page, from `S-Seed-0-seed` through `S-Venue-2-narrative`.
Twelve of the forty-five live pages answer to no stage: three control pages, three Q pages, the four `S-Submission` pages, `S-Seed-1-literature`, and `S-Venue-3-decisions`.
A control page is not a stage page that went missing, because it answers what a unit page cannot: which units this paper has, and which are gated.
The write side agrees with that: `resolve_filename()` refuses the unit `Dash` at `cli/stage.py:286`, so the composer `§13` describes cannot produce `S-Main-Dash` even if someone asked it to.

#### 14.2 · A filename shows two of the four kinds and hides the other two
(what a reader can tell before opening the file)
A leading `Q` says the page decides something and closes when its Aims are met, while a leading `S` says the page belongs to a family and closes when its human gate passes.
A control page is visible too, but by two different spellings: `S-Display-Dash` and `S-Main-Dash` put a word where a unit goes, while `S-Appendix-0-control` puts it in the slug, and `§7.5` reports that nobody has ruled which is right.
What a filename cannot show is a stage page against a per-unit page, because `S-Work-1-claims` has exactly the shape of `S-Main-1-introduction`.
Only the owning group says which, in the `unit:` line each group division carries, so that distinction is read off `§1` to `§10` and never off the name.

#### 14.3 · Per-unit is decided by the gate, and by nothing else
(QC3b's Law: "a stage is `per-unit` exactly when one unit can be approved while another is rejected")
It is not size: `S-Appendix-D-iv` is one page holding a whole instrumental-variable analysis, and it is still one unit.
It is not how much work the stage costs: narrative is a large job and stays one page, because a paper has one arc and there is nothing to approve separately.
It is not how long the page grows: a page that gets long is a long page, not two units, and splitting it changes nothing a human can approve.
The test is a question about people, not about files: can a person say yes to one thing here while saying no to the thing beside it?

#### 14.4 · A Q page is a fourth thing a group may hold, and it is not an S page
(`QV0-value-delivery`, `QP0-present-delivery` and `QR0-round-delivery` are live today)
A Q page records a decision or a concern overview, takes the id shape `Q<group><n>-<slug>`, and carries no family, no stage, no `requires:` and no human gate.
A group holds one when no stage and no manuscript unit belongs to its concern, which `§8` argues is Present's finished shape, or when the concern is open and waiting on work, which `§4` and `§10` argue for Value and Round.
All three read `state: 🔴 OPEN` in their own headers, so a finished shape and a finished page are two different things.
Having no family, a Q page is also outside `§12.3`'s folder rule, and the three live ones sit in `delivery-value/`, `delivery-present/` and `7-round/`.

#### 14.5 · A kind is not a shape, and the two axes cross
(`§11` sorts GROUPS into three shapes; this division sorts PAGES into kinds)
A dash-plus-units group holds one control page plus one per-unit page for each unit, which is how Display, Main and Appendix are built today.
A one-page-per-stage group holds stage pages and nothing else, which is Opening and Work.
The third shape holds neither kind cleanly: Build's four `S-Submission` pages are written by no stage, inventory nothing, and grow with no unit, so they match none of the three kinds.
That hole is real and it is held elsewhere, in QC3b's open item "Rule what a family with no stage means", which `§9` points at from the group side.

#### 14.6 · A central decision register is abolished, and the live one is not empty enough to delete
(JL 260802; `2-venue/S-Venue-3-decisions.md` is still on the board)
The rule is that no page collects decisions on behalf of other pages: a decision is a `Decision Now` row inside the owning page's `States` section, carrying the ask, one line per option, and a recommendation.
`S-Venue-3` holds five rulings and its `state:` line says two of them are still open, carrying three unanswered asks between them, and each of the three binds two or more pages, so moving one means first choosing which single page owns it.
Its other entries are settled history, D11, D15 and D16, and a `Decision Now` row cannot hold a ruling already made, so those belong in the owning page's dated record instead.
`board.md` itself still points at the register twice, in its `close:` line and in its Topic paragraph, and both name D06, D07, D08 and D10, which moved to their asset pages on 260726.

## Aims

### A1 · 🌱 Delivery · Opening
- A1.1 · Opening carries three pages, not five.
  **Done when:** `S-Venue-2-narrative` is indexed under `Delivery · Work` and `S-Venue-3-decisions` is gone from the MISQ `board.md`.

### A2 · 🧱 Delivery · Work
- A2.1 · Work's resource and claims stages split into per-unit pages with a control page each.
  **Done when:** a paper carries `S-Work-R` plus `S-Work-R1…` and `S-Work-C` plus `S-Work-C1…`, and the old single pages are their controls.
- A2.2 · The parser accepts a capital-plus-digit unit.
  **Done when:** `src/parse.py` matches `S-Work-R1-<slug>.md`, and a rebuild shows no existing page re-parsing differently.

### A3 · 📚 Delivery · Literature
- A3.1 · Literature carries the dash-plus-topics shape on its own page, and names the trap where a reader meets it.
  **Done when:** QB3 shows a dash plus one page per topic, and names `S-Main-2-literature` sitting in its group.

### A4 · 💰 Delivery · Value
- A4.1 · Value carries the dash-plus-topics shape on its own page.
  **Done when:** QB4 shows a dash plus one page per topic, and no longer describes itself as a single-page concern.

### A6 · 📖 Delivery · Main
- A6.1 · `S-Main-2` comes home, or the borrow is made permanent on purpose.
  **Done when:** either Literature owns a family and `S-Main-2-literature` is renamed into it, or a ruling says the borrow stays and QB3 and QB6 both say so.

### A8 · 📣 Delivery · Present
- A8.1 · A reader can tell a thin group from an unfinished one.
  **Done when:** QB8 states on its own page that one Q page is its finished shape.

### A10 · 🔁 Delivery · Round
- A10.1 · Round says on its own page that empty is correct until the paper is reviewed.
  **Done when:** QB10 states it, and separates it from the missing family, which is a defect.

### A11 · 🧭 The ten at a glance, and the three shapes they sort into
- A11.1 · Every gap in the `§11` table is closed on the paper, or is owned by a named Aim somewhere.
  **Done when:** each non-`none` row in `§11` points at the Aim that closes it, and no row is left with nobody holding it.

### A12 · 🔤 What a filename says, and what it does not
- A12.1 · No page states a bare count of "joins".
  **Done when:** every page naming the family-against-group problem names the case instead of counting cases, and QB2 still names the narrative disagreement it keeps by design.

### A13 · ⚙️ How a filename is made
- A13.1 · The family list is declared once, and every file reads it from there.
  **Done when:** the composer and the four readers resolve the family set from one source, and admitting a family edits one file.
- A13.2 · The three owed families are admitted in every place at once.
  **Done when:** `Literature`, `Value` and `Round` are in all six lists, and a rebuild shows one page of each parsing, sorting on the Index, and linking in chat.
- A13.3 · The one file that reports an unknown family runs again.
  **Done when:** `../../paper/route/haipipe-paper-stage/check-contracts.py` imports the composer from the path it lives at today and finishes a real check instead of a traceback.
- A13.4 · Every unit token a live page carries is readable by every layer that reads a name.
  **Done when:** `live/chat.py` resolves `S-Display-4al2`, `S-Work-R1` and `S-Main-Dash` to their whole page ids, and `resolve_filename()` composes the unit `Dash`.

### P · 🏁 Page-level
- P1 · Every number on this page is read off a live paper.
  **Done when:** a check resolves each count here against the MISQ board rather than trusting the prose.

## States

### A1 · 🌱 Delivery · Opening
- ⬜ A1.1 · Not started, and opened 260803 to hold a gap A11.1 had found with no owner. Both pages are live on the MISQ board today.

### A2 · 🧱 Delivery · Work
- ✅ A2.1 · Done 260803. The MISQ paper carries the shape: `S-Work-R` plus `R1` `R2` `R3`, and `S-Work-C` plus `C0` `C1` `C2` `C3`, with `S-Venue-2` unsplit. The two old single pages were rewritten as the controls and deleted under their old names, so nine pages replaced two. Splitting them broke `requires:` on 30 other pages, all repointed to `S-Work-R` and `S-Work-C` and re-synced, and the board rebuilds with zero warnings.
- ✅ A2.2 · Done 260802. `src/parse.py` gained `[A-Z]\d+` ahead of `[A-Z]`, and `cli/stage.py`'s `resolve_filename()` gained the matching branch, so the read and write sides agree. Proved safe by rebuilding both boards and diffing the page list: 85 pages on this board and 47 on the MISQ paper, byte-identical before and after.

### A3 · 📚 Delivery · Literature
- ✅ A3.1 · Done 260803. QB3 was redrawn on 260802 and its new `§2.5` now names `S-Main-2-literature` sitting in its own group, with the reason. The MISQ paper also carries the shape: `8-literature/` holds `S-Literature-Dash` plus one page for each of the four strands its `### Literature map` already listed, and `S-Seed-1-literature` became the control page and was deleted under its old name.

### A4 · 💰 Delivery · Value
- ✅ A4.1 · Met on the QB page, and BUILT on the paper the same day. `9-value/` holds `S-Value-Dash` plus four topic pages, cut one per claim, because a Value topic is the set of numbers one claim rests on. Found already met on the QB page rather than done that day: QB4 `§2` is drawn to the dash-plus-topics shape and its `§2.2` is titled "Values have topics, so the concern splits by topic". The State had said the opposite since 260802, which is the third stale claim P1 now names.

### A6 · 📖 Delivery · Main
- ✅ A6.1 · Closed 260803, then SUPERSEDED the same day, and the row is kept because a State that hides a reversal is worse than a long one. It was first closed by ruling that `S-Main-2-literature` stays indexed under `Delivery · Literature`, upholding QB6 against QB3. JL then ruled the page REMOVED outright, so there is nothing left to index: it is archived at `4-main/_archive/`, the §2 prose it gated is owned by `S-Literature-Dash`, and nine contract chains were repointed. Main is now dash plus 8 by design as well as live, and `§12.4`'s trap category is empty.

### A8 · 📣 Delivery · Present
- ✅ A8.1 · Done 260802. QB8 `§2.2` says so on its own page.

### A10 · 🔁 Delivery · Round
- ✅ A10.1 · Done 260802. QB10 `§2.1` says so on its own page.

### A11 · 🧭 The ten at a glance, and the three shapes they sort into
- 🔨 A11.1 · The `§11` table was built on 260802 by reading the MISQ `board.md` row by row, and six of its ten rows show a gap. On 260803 the three that no Aim held were given one: Opening's two extra pages became A1.1, the `S-Main-2` borrow became A6.1, and the `Round` family is inside A13.2. Every non-`none` row now points somewhere, and the remaining work is a check that keeps it that way.

### A12 · 🔤 What a filename says, and what it does not
- 🔨 A12.1 · Reopened 260802 after it was closed on a false claim, and this page states no bare count. QB2 `§1.3` names the narrative case. The remaining work moved to A3.1 on 260803, because naming the trap is Literature's own page to do.

### A13 · ⚙️ How a filename is made
- ⬜ A13.1 · Not started. Read off disk 260803: the seven families are written out in `cli/stage.py:27`, `src/parse.py:247`, `src/page_board.py:497`, `live/chat.py:201` and `check-contracts.py:40`, and a sixth time as a comment in `stages/index.yml:7`. Nothing derives one from another.
- ✅ A13.2 · Done 260803. `Literature`, `Value` and `Round` added to all six lists, inserted in BOARD order so every existing family keeps its rank and nothing re-sorts. Proved safe by rebuilding both boards and diffing their page lists: 86 files here and 47 on the MISQ paper, identical before and after. `resolve_filename` now returns `S-Literature-Dash.md`, `S-Value-Dash.md` and `S-Round-1-first-review.md`.
- ✅ A13.3 · Done 260803, the same day it was opened. `check-contracts.py:26` had imported `board/haipipe-board/stage.py`, which moved to `cli/stage.py`, so it died in a traceback before reading one contract. Repointed, and it now checks 8 stage contracts and reports one KNOWN deferral on `4-display`.
- ✅ A13.4 · Done 260803, the same day it was opened. `live/chat.py:201` had truncated a unit at `\d+` or one capital, so `S-Display-4al2-main-regression` resolved to `S-Display-4`, which is not a page id; its alternation now mirrors `src/parse.py` and returns the whole id for all three cases. On the write side `resolve_filename()` gained the control-page form, and a control page composes with NO slug, so it returns `S-Main-Dash.md` rather than inventing a third spelling of a name that exists twice on disk.

### P · 🏁 Page-level
- ⬜ P1 · Not started. Every count here was read off the MISQ board by hand on 260802 and 260803, and nothing re-checks them. Two have drifted since: the join count, killed on 260802, and the page count in the Log, corrected on 260803.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order this page indexes
- `QB1-opening.md` · the first concern, and the pattern the other nine follow

📥 **Input files** · what the work reads

- `../../paper/route/haipipe-paper-stage/stages/index.yml` · declares which stages exist, and therefore which concerns own one
- `../../board/haipipe-board/src/parse.py` · owns the filename grammar this page describes
- `../../board/haipipe-board/cli/stage.py` · composes a filename from a stage's three declared fields
- `../../board/haipipe-board/src/page_board.py` · holds the family order the Index sorts by
- `../../board/haipipe-board/live/chat.py` · turns a page id into a link, and drops the ones it does not know
- `../../paper/route/haipipe-paper-stage/check-contracts.py` · the only file that reports an unknown family
- `QC-engine/QC3b-page-name.md` · owns the per-unit test and the naming Law

## Law

- 🧱 **ONE GROUP IS ONE `###` DIVISION** (JL 260803). `§1` to `§10` are the ten Delivery groups in board order and each opens with its own designed-against-live page list; `§11` to `§14` hold what is true across them. This overrides the 260802 rule that a group was a `####` paragraph, which had been argued from `check.py` requiring a figure per division. A group's figure is not a slice of the whole-board figure: it is that group's own pages, what it owes against what the live paper carries.
- 🧬 **The family list is closed in SIX places, and the three families once owed were admitted on 260803.** The rule that survives is the count and the paths, not the shortage: `cli/stage.py:27` composes, `src/parse.py:247` decides whether a file is a page, `src/parse.py:301` decides where it sorts, `src/page_board.py` orders the Index sections, `live/chat.py:201` matches ids in the chat layer, and `check-contracts.py:40` checks the declaration. FIVE of those live in `board/haipipe-board/` and the sixth in `paper/route/haipipe-paper-stage/`, so a person working inside the board engine can find every list there and still miss one. A name admitted to five of the six is a page that parses and then sorts into the wrong place, and a name missing from `src/parse.py:301` stops the whole build with a `KeyError`. Three more places restate the names and enforce nothing: `stages/index.yml:7`, `stages/CONTRACT.md:26`, and `SKILL.md:95`, which had already drifted by dropping `Submission`. `§13` argues how the write side and the read side come apart.
- 🛠 **A NAME THE COMPOSER COULD NOT WRITE AND A NAME THE CHAT LAYER COULD NOT READ WERE BOTH LIVE** (found and fixed 260803). `resolve_filename()` raised on the unit `Dash` that `S-Main-Dash` and `S-Display-Dash` both use, and `live/chat.py:201` truncated `S-Display-4al2-main-regression` to `S-Display-4`, which is not a page id. Nothing reported either, because `../../paper/route/haipipe-paper-stage/check-contracts.py` had not run since its import path moved. All three closed the same day, and the lesson is the one A13.1 still holds: a rule spelled out in six files is a rule nothing enforces.
- 🔠 **A capital plus digits is a per-unit member of a lettered series** (JL 260802). `S-Work-R` is the control page and `S-Work-R1` is one unit. In the read regex it must lead `[A-Z]`, which would otherwise consume the `R` and leave the page silently unparseable rather than rejected.
- 🔤 **A filename names the FAMILY that wrote a page; a group names the CONCERN that owns its rule.** A reader must never infer one from the other, and NO PAGE STATES A COUNT OF "JOINS" (JL 260802), because three unlike things were being added together: a family no group is named after, which is normal; a family that is also another group's name, which is the trap; and a disagreement kept on purpose, which is narrative. Naming the case beats counting the cases.
- 🗂 **Every stage makes a page, and not every page comes from a stage.** A family control page has no stage and is not missing one.
- 📄 **A concern with one Q page and no S page is finished, not thin.** Present is correct in that shape, and Round is until a paper is reviewed.
- 🗂 **A concern whose work has topics takes a dash plus one page per topic** (JL 260802). Literature and Value both do, which is the same shape Display, Main and Appendix already run under different unit names.
- 🔠 **In Work, the letter says the stage and the number says the unit** (JL 260802, choosing option A). `R` resource, `C` claims, `N` narrative; `S-Work-R` is the control and `S-Work-R1` is a unit. Rejected: reusing the existing `0a` and `1b` shape, which parses today with no code change but buries the stage behind a number and breaks every name if two stages ever swap order.

## Glossary

- **Paper board**: the `0-lifecycle/` FOLDER inside a paper. `board.md` is its registry and the pages live in one subfolder per family.
- **Family**: the first token of an S filename, saying which stage family authored the page.
- **Control page**: a page that inventories a family's units and that no stage writes.

## Discussion
> JL: I think here one challenge is how to build these pages.
> Like for writing one pages, you might need to load other pages, or first write other pages and do the current pages. I think we might need to think clear about what we are doing.

## Log

260803 · JL: `S-Main-2-literature` removed, and with it the board's last family-against-group trap. I argued against it first, on three grounds that were all true: the page carried JL's own 260727 ruling to keep §2 as a logged deviation from the MISQ blueprint, it gated 13,533 bytes of live `sections/02_literature_review.tex`, and the four Literature topic pages say they FEED it rather than replace it. JL reaffirmed, so it is archived at `4-main/_archive/S-Main-2-literature.md` rather than deleted, and `S-Literature-Dash` was given the §2 prose in its Files so the manuscript section is not left with no page behind it. Nine contract chains repointed. `§12.4`'s trap category is now empty: every S page's family names its own group, except the `S-Submission` set in Build, which is the harmless kind. What went into the archive with it: 7 unticked items and the 260727 keep-ruling, and anything still owed has to be re-raised on `S-Literature-Dash`.
260803 · JL: Work's ten pages take the letter form all the way, so `S-Venue-2-narrative` became `S-Work-N-narrative` and moved into `1-work/`. That retires the board's one disagreement KEPT ON PURPOSE, and it retires it for the same reason Opening's rename exposed: the split existed only because `§12.1` claimed a filename was the sole record of venue-alignment, and every `stage.md` records it in words. `2-venue/` now holds nothing but its `_archive/`, and one live family-against-group case is left on the whole board, `S-Main-2-literature`, plus the harmless `S-Submission` pages in Build. The Diagram legend no longer says any page differs by design, because none does.
260803 · JL: Opening's three pages become `S-Open-Seed`, `S-Open-Venue` and `S-Open-Pitch`, so the group finally owns a family and a folder of its own, `0-open/`. `Open` was admitted to all six lists, the three files moved out of `0-seed/` and `2-venue/`, and 40 files were repointed. The objection this page would have raised does not survive contact with the code: `§12.1` claimed the FILENAME was the only thing saying whether a retarget rewrites a page, and each stage's own `stage.md` declares `venue_aligned: true` in words with a comment explaining it, so dropping `Venue` from a filename loses nothing. `§12.1` is corrected. The second objection, that a word unit would sort alphabetically and render Pitch before Seed, does not bite either: `parse.py` appends pages in `## Pages` order and only falls back to the unit key for pages nobody listed. `2-venue/` now holds one page, `S-Venue-2-narrative`, which is the group-against-family case kept on purpose.
260803 · A2.1, A3.1 and A4.1 all BUILT on the MISQ paper, which is the first time this page's design has been carried by a real board rather than only argued. Three agents ran in parallel, one per group, each writing only inside its own folder while this page's owner kept `board.md` to itself. Work went 3 pages to 10, Literature 2 to 6 with a new `8-literature/`, and Value 1 to 6 with a new `9-value/`; the paper went 45 pages to 61. Every count in `§11` and in the `§2` `§3` `§4` figures was recounted off the live `board.md` afterwards rather than carried over. Three breakages followed from the splits and all are closed: 30 pages pointed `requires:` at the two deleted Work pages, every stage contract went stale after the repoint, and five pages required `S-Display-4a`, a parent member that has never had a page, now pointing at `S-Display-4al2` because D05 (a) rules the binary exposure primary. That last one was older than any of this work and only surfaced once the board was quiet enough to show it.
260803 · JL: the ten Delivery groups each need their own index. They had none, because `group_token` reads everything before the `·` and every heading began `Delivery ·`, so all ten tokened to `Delivery` and collapsed into one 511 KB group page. Renamed `S01 · Delivery Opening` through `S10 · Delivery Round`, and the board now generates ten group pages of about 95 KB each. This is a defect the naming hid rather than a preference about labels.
260803 · A13.2, A13.3 and A13.4 all closed, in that dependency order, and the MISQ paper board updated to match. First the reporter, because nothing else could be verified while it was dead: `check-contracts.py:26` was repointed from `board/haipipe-board/stage.py` to `cli/stage.py`, and it now checks 8 stage contracts instead of dying on import. Then the two names the layers disagreed on: `live/chat.py:201` now mirrors `src/parse.py`'s unit alternation, so `S-Display-4al2-main-regression` resolves whole instead of to `S-Display-4`, and `resolve_filename()` gained the control-page form with NO slug, returning `S-Main-Dash.md` exactly as the live page is spelled. Then `Literature`, `Value` and `Round` were admitted to all six lists, inserted in BOARD order so no existing family changes rank. Both boards were rebuilt and their page lists diffed: identical, 86 files here and 47 on the MISQ paper. The three `family missing` rows in `§11` are gone: Literature and Value now read `pages not written` and are held by A3.1 and A4.1, and Round's row closed because its remaining emptiness is the correct kind. A13.1 stays open and is now the only one of the four that matters, because six hand-edited lists is the same defect waiting to happen again.
260803 · The Law had been left saying FIVE places for a full pass, because a replacement written against `§4` was applied after `§4` had been renumbered to `§13`, so it matched nothing and reported nothing. Found by grep rather than by the checker. Every scripted edit on this page now asserts its target exists before writing.
260803 · One agent per division, fourteen of them, each read-only and each returning markdown that this page's owner spliced in; no agent wrote to the file, because fourteen concurrent writes to one page is the corruption the page contract warns about. Content went from 28 paragraphs to 83. Every count the agents returned was re-derived off disk before it landed, and one was wrong: `§9` said 22 live pages cite an `S-Submission` id and the real number is 23, 14 in Display, 7 in Main and 2 in Venue. Two drafts also disagreed about `S-Venue-3-decisions`, 2 open rulings against 3 open asks, and both were right at different grain, so the page now says 2 of 5 rulings open carrying 3 unanswered asks.
260803 · The fan-out found three live bugs that no page had recorded. `check-contracts.py:26` imports `board/haipipe-board/stage.py`, which moved to `cli/stage.py`, so the ONE file that reports an unknown family has not run since; A13.3 opened. `live/chat.py:201` truncates a unit at `\d+` or one capital, so `S-Display-4al2-main-regression` resolves to `S-Display-4`, which is not a page id, and that is a page the MISQ paper carries today; A13.4 opened and also holds the reverse case, `resolve_filename()` raising on the unit `Dash` that two live control pages use. The two are connected: nothing reported either because the reporter does not run.
260803 · The family list is closed in SIX places, not five. `src/parse.py` holds two: the regex at 247 that decides whether a file is a page, and the `family_order` dict at 301 that decides where it sorts. The second is the loudest of the six, because a name it lacks stops the whole build with a `KeyError` rather than losing one page quietly. The Law is corrected, and so is `§13`.
260803 · A4.1 was found already met rather than done. QB4 `§2` has been drawn to the dash-plus-topics shape since 260802 and its State here said the opposite for a day. Same shape as the join count and the page count before it, so P1 now names three stale claims and still has nothing checking them.
260803 · Three defects found while checking the restructure, all on this page and all fixed. The Opening said family and group "disagree on purpose in three places", which is exactly the bare join count this page's own Law forbids and `§12.4` killed on 260802; it now says the cases come apart in more than one way and points at `§12`. The Opening also claimed every concern page carries a `What we want on the paper board` division, and QB1 and QB2 call theirs `What the paper board shows`, so the Opening now names the split, 8 against 2. The Writing Style still declared a three-part scope written before `§3` and `§4` existed, and now names all fourteen divisions. Historical `§` references in this Log were left as written and annotated with where each lives now, because a Log is a dated record and repointing it would erase what was true then.
260803 · JL: ONE GROUP IS ONE `###` DIVISION, not a `####` paragraph. He ruled it against a Decision Now row offering three shapes and took none of them: "we will have a lot of divisions, `### Delivery · Opening` <--- this will be a division, and `### Delivery · Work` and `### Delivery · Literature`". That row is closed and removed. Content went from four divisions to fourteen: `§1` to `§10` are the ten Delivery groups in board order, and `§11` to `§14` hold the cross-cutting facts, which are the at-a-glance table with the three shapes, what a filename says, how a filename is made, and the three page kinds. Every group division opens with its own designed-against-live page list, which answers the 260802 objection that ten figures would be ten slices of the whole-board figure: they are not slices, they are one group's own pages. Aims and States were regrouped to match, `A1` to `A14`, and two gaps that A11.1 had found with nobody holding them finally got an owner: A1.1 for Opening's two extra pages, and A6.1 for the `S-Main-2` borrow. The old `A2.1` and `A3.1` moved to the group that actually owns the work, Literature and Work.
260803 · `§13` opened, and was `§4` for one build, because the Law said a family is admitted in five files and no Content division argued it, so this page described a naming grammar without ever saying where a name comes from. It splits the write side, three declared fields joined by `cli/stage.py resolve_filename()`, from the read side, four files that each hold the family list on their own and fail in four different silent ways. Every path and line number was read off disk on 260803. Two things surfaced while doing it: four of the five files live in `board/haipipe-board/` and the fifth in `paper/route/haipipe-paper-stage/`, which the Law now says, and `stages/index.yml:7` restates the list in a comment that enforces nothing. A13 opened with two Aims, neither started.
260803 · The Diagram lists 48 page names plus one `S-Round-<n>` placeholder, and the 260802 Log had said 45. Corrected. This is the second count on this page to drift with nothing checking it, so P1's State now names both.
260802 · JL: one Question Group is one unit of Content. `§1` was three cross-cutting essays whose spine did not match the figure's, so a reader could see ten groups drawn and then not look one up. It now walks the ten in board order, `§1.1` to `§1.10`, each naming that group's unit, shape and gap, with the three-shapes figure and its two paragraphs kept below as `§1.11` and `§1.12`. Those became `§1` to `§10` and `§11.1` to `§11.2` on 260803. Written as `####` rather than `###` because `check.py:657` requires a figure under every division, and ten per-group figures would be ten slices of the figure this page already draws; the Writing Style now carries that reason. Aim ids did not move.
260802 · The join count is dead as a number. This page had said four in the Diagram legend, three in the Law, one in `§2.3`, and had a ✅ State claiming `§2` named all three when `§2` showed one arrow. The cause was three unlike things counted together, separated in what was then `§2.4` and is now `§12.4`: a family no group is named after, a family that is also another group's name, and a disagreement kept on purpose. Only the middle one is a trap and only `S-Main-2-literature` is live. A2.1 reopened, because it had been closed on the false claim.
260802 · `§1`'s table was read row by row off the MISQ `board.md` rather than off this page's own figure, which is how two live pages turned out to be invisible here: `S-Venue-3-decisions` in Opening, which `§3` abolishes, and `S-Seed-1-literature` in Literature. A1.3 opened to hold the six gaps, three of which no Aim owns yet.
260802 · The Literature group redrawn to the dash-plus-topics shape JL ruled, and the two families the board is missing, `Literature` and `Round`, are now one Law entry naming the three files that close the list rather than two separate notes.
260802 · JL asked what the per-group `📁` line meant, and the honest answer is that it repeated the family: `Delivery · Display` said `3-display/`, which the filenames already said. Ten such lines removed. The header now states the folder rule in one place and `§2.3`, now `§12.3`, argues it once, which is where it belongs.
260802 · JL: the paper board is a FOLDER, not just a `board.md`, and these groups are what we EXPECT rather than a report. The figure header now names the folder and says so, each group carries the subfolder its pages live in, and `§2.3`, now `§12.3`, states the rule that came out of checking it: the folder follows the FAMILY exactly, so the group is the only cut that differs. Found while checking: `QV0` and `QP0` sit in folders named after the concern while `QR0` sits in one named after the family slot, and nobody has ruled that.
260802 · JL: one page, one line. The Opening, Work, Literature and Build rows had been packing two or three page names onto a line, and Display, Main and Appendix had been collapsed to a count. Every page a paper carries is now its own row, 48 of them plus one placeholder, and the Writing Style carries the rule.
260802 · JL: the figures were skill-board led, with QB ids down the left edge and the paper's pages on the right, and the two edges did not line up. Redrawn with the PAPER board as the spine: each line starts with the group a paper carries and the QB id annotates it on the right. A Writing Style rule now holds it that way.
260802 · A3.2 closed. The unit grammar now accepts a capital plus digits on both sides: `src/parse.py` reads it and `cli/stage.py resolve_filename()` composes it. Nothing existing moved, proved by rebuilding this board and the MISQ paper board and diffing their page lists, 85 and 47, byte-identical. Found while doing it: `resolve_filename()` rejects `Dash`, which the reader accepts and `S-Main-Dash.md` uses, so the write side has been narrower than the read side for some time.
260802 · Opened on JL's ask, because nothing showed the whole paper board: each of QB1 to QB10 carried only its own group. Drawn from the MISQ paper, the only one built far enough to show every group. Three cross-concern facts landed here rather than being repeated ten times: the three kinds of concern, the family-against-group grammar with its three deliberate joins, and the three page kinds a group may hold.
260802 · JL chose option A for Work's unit naming: the letter says the stage, the number says the unit. A3.2 opened, because the parser rejects a capital-plus-digit unit today.
