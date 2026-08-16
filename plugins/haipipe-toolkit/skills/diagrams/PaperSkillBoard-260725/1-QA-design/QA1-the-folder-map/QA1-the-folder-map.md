# The folder map: where a new rule, file, or page belongs

state: 🟡 PARTIAL · the map and the crossings are ruled; the paper family README still does not carry them
owner: JL
method: every THING has a board; name all eleven, allow four crossings, and treat the banks as a wall rather than a room
session: 28293c58-4cae-45db-93c3-41d754817af1

## Opening

Where does a new rule, file, or page belong?
Everything here comes in a pair: `skills/paper/` ships the procedure a run follows, and `PaperSkillBoard-260725` holds the rulings that produced it.
One word names both, so a file lands in the wrong half easily.
Nothing reports it, because a rule in the wrong folder binds nothing rather than breaking.
Eleven folders, six pairs, and one rule deciding which half of a pair owns what.

**Where this page sits**: This is the first face on the board, because every later ownership question assumes it is answered.
`QC3b` can only say who names a file once it is settled which tree the file is in.
`QA8` can only draw an ownership line inside a shared page once it is settled which two owners exist.
A reader who cannot place a thing cannot rule on it.

**What each wrong placement costs, and they are not symmetric**: A rule written into a working folder binds nothing, because no runtime reads it.
Working state written into the manual makes the manual wrong for every other paper.
A design argument that runtime starts depending on means the skill can no longer ship without its own history.
A paper that keeps its own copy of the universal contract drifts from it silently, because nothing compares the two.

**Which pages take it from here**: `QA2` what is inside the skill set · `QA3` what is on a skill board · `QA4` the board tool · `QA5` the evidence channel · `QA10` the prose verb · `QA6` what a new paper gets · `QA7` what is on a paper board.
How a question actually crosses the evidence wall, and what it may cost, is `QC4b`.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from `../BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md` and are not restated here.

**Never put a count in the title or the lead**: it has gone wrong twice, four to eight on 260726 and eight to eleven on 260802, and each time the title outlived the fact.
Name what the page is FOR, and let the number live in Content where it can be corrected without a rename.

**A glyph is introduced with its path**: the first time a division names `①`, write the path beside it.
The circled numbers are this page's own vocabulary, and a reader who arrived from one link has not met them.

**A claim about a folder we do not own carries its check**: those claims go stale in silence, because nothing on this side fails when the other side fixes itself.
`⑥` was recorded as "a design folder, not a board" for a week after that board existed.
State how a reader can tell the claim is still true, or do not state it.

**The numbers are append-only**: a new thing takes the next number and nothing renumbers.
Reading order is therefore imperfect and the table is what to read instead of the sequence.

## Diagram

**One door in**: `/haipipe-paper` is the only thing a human types, and it CALLS the two channels.

```text
                    👤  the human types ONE command
                              │
                              ▼
                    ①  /haipipe-paper
                       resolves the paper · routes · writes ⑦ and ⑧
                       renders NOTHING · computes NOTHING
                              │
               ┌──────────────┴───────────────┐
               │ calls                        │ calls
               ▼                              ▼
    ③ /haipipe-board                ⑤ /haipipe-probe
      THE HUMAN CHANNEL               THE EVIDENCE CHANNEL
      ├ build.py    ⑧ → board/ site   ├ organize  the stake stripped
      ├ serve.py    push the URL      ├ match     the bank, read-only
      └ write-back  a click → ⑧'s md  └ dispatch  through a clean agent
               │                              │
               ▼                              ▼
         👁 eyes · clicks · a yes       tasks/ · discoveries/
               │                              │
               └──── back into ⑧ ──┐  ┌── a QA file, bound BY PATH
                                   ▼  ▼
                         ⑦ the paper · ⑧ its board

🚫 the human NEVER types /haipipe-board or /haipipe-probe for paper work
🔓 both stay real doors for what is NOT a paper: ③ renders the design boards
```

**When ① calls ③**: three moments, and the middle one is what a naive reading misses.

```text
1️⃣ ENTER      resolve root → get-or-create → build.py → serve.py
              the human is looking at ⑧ BEFORE any work starts
2️⃣ AFTER      every write to ⑧: a stage run, a phase worker, a CHECK gate
   EVERY      each ends with a rebuild, or the human is reading a paper
   WRITE      that no longer exists
3️⃣ BEFORE     the REVERSE direction. A comment or a > lane arrived through
   ① ACTS     serve.py, so ⑧'s markdown changed under ①. Re-read, never cache

🔗 the dependency was ALREADY there: create-page.py calls the Board's stage.py
   to compose an S filename, so ① could never ship without ③ at the WRITE layer
```

## Content

### 1 · The map

**Six pairs**: every THING has a board, and the board holds the arguments that produced it.

```text
   🧩 THE THING                        📋 ITS BOARD
   ───────────────────────────────     ──────────────────────────────
 ① 📄 paper skill    skills/paper/  ⟷  ② PaperSkillBoard-260725   ← here
 ③ 👁 board tool     skills/board/  ⟷  ④ BoardSkillBoard-260722   read-only
 ⑤ 🔎 probe layer    skills/probe/  ⟷  ⑥ retired 260804 · was 01-probe-qa-260726
 ⑦ 📝 one paper      Paper-X/       ⟷  ⑧ Paper-X/0-lifecycle/
 ⑨ 🖼 display layer  skills/display/⟷  ⑩ retired 260804 · was 01-haipipe-display-260727
 ⑪ ✍️ writing layer  skills/writing/⟷  ② ◀━━ THIS BOARD · no board of its own

 🔑 the test for a board of its own: does the family own a KIND of artifact?
 🗑 ⑥ and ⑩ were retired on 260804 ("retire old boards"): their rulings had
    graduated into the owning skills, and the records live in git history
 🚫 the evidence banks are NOT on this map. They are the OUTSIDE
```

🗺 Establishes the eleven folders, what decides whether a family gets its own board, and why two counts on this page move independently.

#### 1.1 · Every thing has a board, and a board may serve two things
(the pairing is the rule; `②` serving both `①` and `⑪` is the one exception and it has a test)
A family that owns a KIND of artifact has a subject of its own to argue, so it earns a board: `⑨` owns the float and earned `⑩` (retired 260804 once its rulings had graduated; the test, not a board's survival, is the rule).
A family that owns none is argued where its prose already lives: `⑪` owns no artifact kind, its own `writing/README.md` says so, and its record is `②` at `QA10`.
That is the whole test, and it is checkable by opening the family's README rather than by taste.

#### 1.2 · A shared family is not a channel
(four shared families, exactly two channels, and the counts move independently)
A channel is a door OUT of the paper. Evidence comes in through `⑤`, and a human reaches the work through `③`.
`⑨` and `⑪` are called without being doors: `⑨` makes a float the paper then owns and places, and `⑪` rewrites prose the paper already has.
Nothing leaves and nothing arrives, so merging the two words would make the map claim four doors where there are two.

#### 1.3 · Calling is not owning
(the test is what happens on failure, not what appears in the call graph)
`①` is the SINGLE thing a human types (JL 260726), and it calls `③` to build and open the board and `⑤` to ask across the wall.
In both cases it renders nothing and computes nothing itself.
When `serve.py` cannot reach the browser, `①` has no fallback renderer to fall back to, because it never had one: it prints the URL and says the push failed.

#### 1.4 · Two of them are boards, and they are opposites
(`②` and `⑧` share a tool and a grammar, which is exactly why the difference must be stated)
A design board is a RECORD, and its rulings are supposed to leave: `✅` means the Law is copied into `①`, and from then on the skill binds rather than the board.
A paper board is a CONTROL PLANE, and nothing leaves it: a gated S page keeps its Content, because that Content IS the paper.
Same glyph, opposite meaning, argued as deliberate opposites on `QA3` and `QA7`.

#### 1.5 · The numbers append and never move
(reading order is the price paid for not rewriting several hundred citations)
`⑨ ⑩ ⑪` were added on 260802 rather than slotted in beside the other reusable families.
Renumbering `⑦` and `⑧` would have rewritten several hundred glyph citations across QA and QC, and 260731 recorded on the board family what a sequential rename map does to prose.
So one manuscript sits in the middle of the shared families, and the table above is what to read instead of the sequence.

### 2 · The four crossings

**Legal movement**: three directions allowed, four forbidden, and nothing else.

```text
 ⒜ ② ━graduates━▶ ① AND ③     a ruling hits ✅ → its Law is COPIED   → QA3
 ⒝ ① ━calls━▶ ③, together ▶ ⑦ ⑧   two skills, ONE file, never the
                                  same REGION                    → QA4 QA8 QA9
 ⒞ ⑦ ━asks across━▶ 🧱 THE WALL   a STRING out, a FILE back, by PATH → QA5

 🚫 FORBIDDEN
    ① ▶ ②   a runtime skill needing an open Q page
    ③ ▶ ②   the tool depending on the board that designs it
    ② ▶ ④⑥⑩ ruling a record this family does not own
    ② ▶ ⑦   reading a paper's state off a design board
 ✅ the proof: delete any board and every skill still runs
```

🔀 Establishes the only movements allowed between the eleven, and the one that produces anything.

#### 2.1 · Crossing ⒝ carries the most weight, because it is the one that produces
(two skills write one markdown file and never contend, because their regions are disjoint)
`③` owns the filename, the page shell, the managed contract block, and every keystroke a human contributes through the live layer.
`①` owns Opening, Content, Aims and States, and is the only one of the two that generates `⑦`.
`QA8` states that ownership line seam by seam, and `QA9` states how work leaves a page and returns to it.

#### 2.2 · The banks are a wall, not a room
(`tasks/` and `discoveries/` are owned elsewhere, so numbering them would be false parity)
They sit beside `papers/` inside a project and are owned by `/haipipe-task` and `/haipipe-discovery`.
No page of this skill rules anything about their contents, so what matters here is the wall and how a question crosses it, never what is on the far side.

#### 2.3 · The forbidden directions have never been checked
(the rule is stated, and nothing verifies it)
No runtime skill may require an open Q page, and no paper's state may be inferred from a design board.
Both are stated in `## Law` and neither is mechanical, so a skill could acquire either dependency tomorrow without anything reporting it.

### 3 · Which of the eleven get a face here

**One rule decides all of it**: a board is ruled by its owner alone and consulted by everyone else.

```text
 🧩 THING                    🎭 face here?  ⚖️ why
 ────────────────────────    ───────────    ──────────────────────────────
 ④ the board we do NOT own   🚫 no          ruling a board we have no
   (⑥ ⑩ retired 260804)                     standing over
 ③ ⑤   paper-side seam is    ✅ yes         QA4 · QA8 · QA9   and   QA5
        ruled here
 ⑨     seam ruled in QB      🚫 not in QA   it is a DELIVERY seam: QB5 owns
                                            the line, QBe2 heads the series
 ⑪     its BOARD is ②        ✅ yes         QA10. there is nowhere else the
                                            argument could go
```

🎭 Establishes why some shared families get a face on this board and others are only named.

#### 3.1 · `⑪` is the case the old rule did not cover
(the rule forbids ruling a board we do not own, and `⑪` has no board at all)
JL placed `⑪`'s record here on 260802, so this board IS its owner.
The rule therefore permits the face rather than forbidding it, and no exception had to be added.

#### 3.2 · The two channels are not covered equally, and that is honest
(`③` has three faces, `⑤` has one, and the imbalance reflects where the rulings are)
`③`'s contract with `①` is heavily ruled here: who names a file, who creates a page, which dependency declaration binds, where state lives, the queue, the runner.
`⑤` owns nearly all of its own contract, and this family rules only which questions a paper raises and how a landed answer is interpreted.
The thing to watch is that the imbalance stays a reflection rather than becoming a habit: a second ruled seam earns a second face by the same test as anything else.

### 4 · Placing something new

**The routing table**: the page's own question, answered.

```text
 📥 WHAT YOU HAVE                      📤 WHERE IT GOES
 ─────────────────────────────────     ──────────────────────────────────
 🗣 a rule still being argued      ━▶  a Q face on ②
 ⚖️ a rule that is decided         ━▶  ② as ## Law, then graduate into ①
 🤖 a procedure an agent follows   ━▶  ①: the one SKILL.md, an fn/ verb, or the
                                       owning stage.md contract
 📝 one paper's prose · display    ━▶  ⑦
 📊 one paper's status · queue     ━▶  ⑧
 🔢 a number or citation from a run ━▶ across the wall: an E<n> division on ⑧'s
                                       S03/S04 evidence page, bound by path to a
                                       QA-probe in that stage's probes/ drawer
```

📍 Establishes the answer to the page's lead question, in the form a reader can apply without reading the rest.

#### 4.1 · The table is the deliverable, and it is not yet portable
(a fresh agent should be able to place a file without opening this board)
`paper/README.md` was rewritten to the thin family map on 260805 and extended again by the 260806 one-door collapse, and it still carries no routing table, so today the only place the routing exists is here.
That is the gap `A4.1` names, and it is what keeps this page 🟡 rather than ✅.

## Aims

### A1 · 🗺 The map
- A1.1 · The eleven folders are named in six pairs, each with the kind of truth it holds.
  **Done when:** every folder on the map resolves on disk, and no page of this board cites a folder the map does not name.
- A1.2 · The test for whether a family needs its own board is written down and checkable.
  **Done when:** the artifact-kind test is stated in `## Law`, and each of the six pairs can be justified by it without appeal to history.
- A1.3 · A claim about a folder this board does not own carries the check that keeps it true.
  **Done when:** no sentence on this page asserts the state of `④`, `⑥` or `⑩` without naming how a reader verifies it.

### A2 · 🔀 The four crossings
- A2.1 · The legal movements are stated, and the forbidden ones with them.
  **Done when:** the three allowed crossings and the four forbidden directions are in `## Law`, and each names the page that owns its detail.
- A2.2 · The evidence banks stay outside the map.
  **Done when:** no page of this board rules the contents of `tasks/` or `discoveries/`.
- A2.3 · The forbidden directions are mechanical, not merely stated.
  **Done when:** something reports a runtime skill that requires an open Q page, or that infers paper state from `②`.

### A3 · 🎭 Which of the eleven get a face here
- A3.1 · One rule decides every face-or-no-face case without a second rule.
  **Done when:** each of the eleven can be sorted by "is this board its owner?" alone, and the answers match the faces that exist.

### A4 · 📍 Placing something new
- A4.1 · A fresh agent can place a new file without reading this board.
  **Done when:** `paper/README.md` carries the routing table, and a cold agent given one new file names its folder correctly from the README alone.

### P · 🏁 Page-level
- P1 · This page obeys the page contract it is one of the first to adopt.
  **Done when:** `check.py` reports no `opening-*`, `division-no-figure`, `division-no-caption` or `dead-file-path` finding against this page.

## States

### A1 · 🗺 The map
- ✅ A1.1 · Eleven folders in six pairs. `⑨ display/` was admitted on 260802 after being cited eleven times in `## Links` while absent from the map; `⑪ writing/` was placed the same day. `⑥` and `⑩` no longer resolve on disk since the 260804 board retirement, and the map now says so beside them.
- ✅ A1.2 · The artifact-kind test is in `## Law` and each pair satisfies it. `⑪` is the only family with no board of its own, and `writing/README.md` states the reason in the family's own words.
- 🔨 A1.3 · The `⑥` claim was repaired on 260802 after standing false since 260726, and `QA5` carried the same claim as an open item. The rule is now in `## Writing Style`; whether the other two claims obey it has not been re-read.

### A2 · 🔀 The four crossings
- ✅ A2.1 · Three allowed, four forbidden, each naming its owning page.
- ✅ A2.2 · Ruled 260726. The banks were briefly counted as a fifth folder, which gave a folder owned by another family parity with the folders this one owns.
- ⬜ A2.3 · Not started, and never checked once. A skill could acquire either forbidden dependency tomorrow without anything reporting it.

### A3 · 🎭 Which of the eleven get a face here
- ✅ A3.1 · The rule sorted `⑪` correctly on the day it was written, without an exception being added for it.

### A4 · 📍 Placing something new
- ⬜ A4.1 · `paper/README.md` was rewritten to the thin family map on 260805 and rewritten again by the 260806 one-door collapse, and the placement routing table is still only here. This is the one gap keeping the page 🟡.

### P · 🏁 Page-level
- 🔨 P1 · First QA page migrated to the `QB4` contract, on JL's pilot ruling of 260802. The remaining ten are unmigrated.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `../../paper/README.md`
  The paper family map that should carry the routing table and does not. This is `A4.1`.
- `../../paper/haipipe-paper/ref/paper-folder-anatomy.md`
  Where the family states its folder rules, and the other place a placement rule could land (`PHILOSOPHY.md` retired with the thin restructure).

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Owns `dead-file-path` and the opening rules this page is measured by. It reads structure and never judges whether a sentence is still true, which is why `A1.3` exists.

### 📤 Output files · what a BUILD writes
- `../../board/QA/QA1-the-folder-map.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Law

- Eleven folders in six pairs, and exactly four crossings between them. Every thing has a board, and that board holds the arguments that produced it.
- A board may be the board of more than one thing. `②` is the board of `①` and of `⑪`, and the test of whether a family needs its own board is whether it owns a KIND of artifact. A family that owns one has a subject to argue and earns a board; a family that owns none is argued where its prose already lives. `⑨` owns the float and earned `⑩` (retired 260804); `⑪` owns nothing and has `②`.
- A shared family is not a channel. There are four shared families and exactly two channels, and the counts move independently: a channel is a door out of the paper, and `⑨` and `⑪` are neither.
- A settled ruling graduates from the skill board into the OWNING SKILL, which for seven of thirteen groups means both `①` and `③`, and only then binds. A ruling landed on one half of a pair is a defect.
- `①` and `③` produce `⑦` and `⑧` together, on one file, in disjoint regions: the tool owns the shell and every human keystroke, the paper skill owns the substance and every generated manuscript file. A paper consumes the settled contract and never stores the universal manual. A paper binds a question it cannot answer to a bank answer, by path, across a wall it may not reach through in any other way.
- The evidence banks are not a folder of this skill. They are owned elsewhere, and nothing on this board rules their contents.
- No runtime skill may require an open Q page, and no paper's state may be inferred from a design board. A design record is never a runtime dependency: delete any board and every skill still runs.
- A board is ruled by its owner alone and consulted by everyone else. This board rules `①`, `⑪`, and the contract half of `③`. It never rules `④`, `⑥` or `⑩`.

## Lesson

- Two things that look alike collapse into one word, and the collapse looks harmless until a rule crosses it. This page once said "design Board" in the singular, covering both the skill's board and a paper's board. They use the same tool, the same page grammar and the same four `state:` values, so nothing looked wrong. It was: the graduation rule, which says a settled ruling leaves the board for the skill, then appeared to apply to a paper's S pages, whose Content must never leave because it IS the paper.
- A claim about a folder this board does not own goes stale in silence. `⑥` was recorded as "a design folder rather than a board, the one gap" for a week after `01-probe-qa-260726` existed, on this page and on `QA5`, because nothing on this side fails when the other side fixes itself. `check.py` reads structure and never judges whether a sentence is still true.
- A count in a title outlives the fact it states. This page was `QA1-eight-folders.md` through two corrections before the name was changed to something that survives the next family.

## Glossary

- **Thing / board pair**: a folder that does work, and the folder that argues about how it does it.
- **Channel**: a door OUT of the paper. There are exactly two, and being a shared family does not make one.
- **Artifact kind**: the class of thing a family produces and owns, which is the test for whether it earns a board of its own.

## Log

- 260806 2215 · [REVISE-CC] swept to the 260806 architecture; rewrote the routing table's evidence row to the E-division grammar (an E<n> division on the S03/S04 evidence page, bound by path to a QA-probe in that stage's probes/ drawer) and pointed its procedure row at the one SKILL.md, an fn/ verb, or a stage.md.
- 260806 0720 · [REVISE-CC] swept to the thin architecture (one door + stage data + board rental); marked `⑥` and `⑩` retired on the map, repointed the probe routing row at S03/S04 `probes/` entries, and replaced the dead `PHILOSOPHY.md` contract path.

260802 · Migrated to the `QB4` page contract as JL's pilot for the QA series: Writing Style added, Content numbered into four divisions each with a face figure and caption, Aims regrouped as A1-A4 plus P with `Done when`, States mirrored one row per Aim, Files grouped by action. Three rulings that had been buried in prose became their own Aims: the artifact-kind test, the stale-claim rule, and the unchecked forbidden directions.
The page grew, 305 lines to 341, against an expectation that the contract would shrink it. The prose did compress, and the apparatus the contract requires (a Writing Style section, four face figures with captions, nine `Done when` conditions, nine mirrored State rows) added more than the compression saved. A page carrying eight Law paragraphs and four divisions is simply not the shape of the 122-line QB pages the estimate was drawn from.

260802 · JL placed `⑪ writing/` and used `⑨ display/` as the yardstick. `⑨` turned out to be absent from the map while eleven `@display` links cited it, and `⑥`'s "design folder, not a board" had been false since 260726. Grew to eleven folders in six pairs, appending rather than renumbering so `①` through `⑧` keep their meaning. Two rules added: a board may serve more than one thing, decided by whether the family owns an artifact kind; and a shared family is not automatically a channel. Renamed from `QA1-eight-folders.md`, because the title had stated a count that went wrong twice.

260726 · JL asked for a figure of how `/haipipe-paper` calls `/haipipe-board` and `/haipipe-probe`. The opening diagram showed OWNERSHIP and never showed FLOW, so it was replaced with a call-flow figure: one door in, two channels called, and what comes back. Two blocks added beside it: the three moments `①` calls `③`, and why this does not break "owns neither channel". Ruled and implemented the same day; see `QA4` for the ruling itself.

260726 · Grew from four folders to eight, in four pairs, after JL asked whether the board tool should be numbered. Every THING has a board, so its board is `⑥`. Then JL's synthesis reframed the whole map: `①` writes the paper and owns NEITHER channel out of it. `③` is the human channel, `⑤` the evidence channel. Renumbered so producers come before product. 383 glyphs preserved through the swap.
