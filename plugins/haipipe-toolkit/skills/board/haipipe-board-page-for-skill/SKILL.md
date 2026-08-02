---
name: haipipe-board-page-for-skill
description: >-
  The VARIANT contract for a Board's roster pages: Skill-<n>-<slug>, which mirrors one shipped skill folder, and Agent-<n>-<slug>, which mirrors one shipped agent file. It loads haipipe-board-page for the base frame and never restates it, then adds only what a roster page needs and a decision page does not: an Opening that INTRODUCES a unit instead of asking a rhetorical question, the derived-versus-authored split across the three managed spans, state: as a health judgment rather than a version, Aims as the unit's own open work including defects other pages route here, and the rule that Content is the unit's own bytes and is never authored. Use when writing or fixing a Skill or Agent page, when a roster page's Opening reads like every other one, when a new unit ships and needs a page, or when a retired unit's page must be archived. Trigger: skill page, agent page, roster page, Skill-0, Agent-1, mirror page, skillpage, skill page Opening, roster row, working on a skill page, /haipipe-board-page-for-skill.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-02"
  summary: "First cut: the roster-page variant, opened because five Skill Openings came out of one template and the base could not have prevented it."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-skill · a roster page is not a decision page

**LOAD `haipipe-board-page` FIRST.** It owns the base: the seven sections, their fixed order, the five rows that define each one, the title rule, the numbering, and the evaluation contract.
This file adds only what a roster page needs and a decision page does not.
It never repeats a base rule, because a copied rule is the thing that goes a night out of date while the contract moves.

**The two kinds this variant covers**: both mirror something that ships elsewhere.

```
kind    filename              mirrors                        closes when
──────────────────────────────────────────────────────────────────────────
Skill   Skill-<n>-<slug>.md   one skill FOLDER · SKILL.md    the unit ships
Agent   Agent-<n>-<slug>.md   one agent FILE   · <name>.md   the unit ships
                              NEITHER is ever counted in the board's settled total
```

`<n>` orders the roster and never carries the version, because a filename that changed every release would break every link to the page.
A skill is LOADED into a context and an agent is DISPATCHED into a fresh one (JL 260731), which is why they are two kinds and not one.

## 🪞 What makes a roster page different

A Q page asks a question and closes when its Aims are met. An S page closes when its human gate passes.
A roster page **decides nothing**. Its subject exists on disk before the board mentions it, ships to other people, carries its own version and its own changelog, and closes only when the unit ships.

Three consequences, and every rule below comes from one of them:

```
1  it has no question       →  its Opening INTRODUCES; it does not ask
2  its Content is not ours  →  the unit's own bytes, in a managed span
3  it has a HEALTH          →  state: is a judgment about the unit, not a version
```

## 🧭 The Opening a roster page owes (the rule this skill was opened for)

**The failure, measured 260802.** Five roster pages on `01-boardform-260722` had Openings in one shape:

```
line 1   Does `<name>` <verb> one <noun> for <consumers>?
line 2   <what it owns>
line 3   The hard part is <X> without <Y>.
line 4   <consumers> depend on <Z>.
line 5   It is healthy when <W>.
```

Read alone each is clear. Read consecutively they are one letter with the nouns swapped, which is the failure `haipipe-board-reviewer-agent` 0.4.0 exists to catch and which JL caught first by eye.

**The base could not have prevented it, and that is why this file exists.**
The base already carries the noun-substitution test, so the rule was on the books and five writers broke it anyway.
The cause is upstream of the test: the base's Opening shape is `the question, what its words mean, why that is hard, what this page decides`, and a roster page **decides nothing**.
A writer obliged to produce a question about a unit that decides nothing can only manufacture a rhetorical one, and "Does X do X well?" has exactly one answer, "that is what it is for", which carries no information.
Give five writers the same impossible slot and they will fill it the same way. The slot was the defect, not the writers.

**What replaces it.** The visible paragraph answers three questions, in this order, in plain words for a reader who has never heard of the unit:

```
❶ WHAT IS IT, and what is it FOR
     one line. A reader who stops here should be able to say what it does.
❷ WHEN DO I REACH FOR IT, rather than its sibling
     name the sibling you would otherwise pick, and the line between them.
     A boundary stated against a real neighbour is checkable; "it owns X" is not.
❸ WHERE DOES IT STAND
     the one thing to know before trusting it: what is unproven, unbuilt,
     unruled, or moving fast. Never "it is healthy when ...", which describes
     a hypothetical unit rather than this one.
```

Keep the base's physical shape unchanged: one visible paragraph, the FIRST BLANK LINE is the split, `More details` below it as labelled parts.

**Four things a roster Opening may never do:**

```
🚫 open with a rhetorical question          it decides nothing, so it asks nothing
🚫 paraphrase the unit's own description:   Content already carries those bytes;
                                            a paraphrase is a lossy second copy
🚫 use the own · hard-part · depend ·       four slots produce four filler
   healthy scaffold                         sentences and one form letter
🚫 claim health the page cannot show        ❸ names evidence or says it is missing
```

**The test, and it is not the author's to pass.** Read the changed Openings CONSECUTIVELY in board order, not one at a time. A page that is clear alone still fails if its Opening would introduce its sibling after a noun swap. Dispatch `haipipe-board-reviewer-agent`; the writer's own read cannot see this, because the writer knows which unit they meant.

## ✍️ Derived and authored: the split a machine enforces

`haipipe-board/cli/skillpage.py` owns three spans and nothing else. Everything outside them is a person's.

```
DERIVED · skillpage.py sync rewrites, hash-checked
  ## Diagram  <!-- haipipe:skill:tree:… -->   the folder tree, one purpose line per file
  ## Content  <!-- haipipe:skill:body:… -->   the unit's SKILL.md, its own bytes
  ## Log      <!-- haipipe:skill:log:… -->    its CHANGELOG, converted to Log lines
  the title's `· v<version>`                  so the index row shows it unmaintained

AUTHORED · a script that rewrites one of these is a defect
  ## Opening · the WORKFLOW fence in Diagram · ## Aims · ## States
  · the page's own hand-written ## Log lines · state: · owner: · method:
```

`sync` replaces only the marked spans; `check` REPORTS a stale hash instead of rewriting, so drift is visible rather than possible.

**A green `check` means less than it looks.** `digest()` hashes the frontmatter's derived facts only, by its own docstring, "so prose edits never look like drift". ✅ means the metadata is current, NOT that the page's copy of the `SKILL.md` still matches it. Byte equality needs a regenerate-and-diff by hand.

```bash
python3 <board-skill>/cli/skillpage.py new   <board> <unit> --group "<GROUP>" --stamp "YYMMDD HHMM"
python3 <board-skill>/cli/skillpage.py sync  <board> [<page>|--all]
python3 <board-skill>/cli/skillpage.py check <board>
```

An AGENT is one file, so its tree span renders EMPTY rather than being omitted: `sync` replaces spans it can find, and a missing one reports forever as an older page needing repair.
The WORKFLOW fence carries the whole picture on an agent page, because there is no tree to carry it.

## 🩺 `state:` is health, and only a person writes it

The page `state:` line keeps the base's four values, and on a roster page it answers one question: **is this unit stable, in flux, in question, or parked?**

A version cannot answer it: a unit at `0.1.0` may be finished and one at `0.9.4` mid-rewrite. So `new` seeds `🔴 OPEN` and a person changes it. The version rides the TITLE, never `state:` and never the filename, so a machine number and a human judgment never compete for one line.

**The readable note after the emoji must carry the evidence**, not a mood:

```
✅  🟡 in flux · ~60 releases in 11 days, 3 open defects
✅  🟡 in question · existence unruled since 260729
✅  🟡 in flux · consumers declared, none measured
🚫  🟡 in flux                    ← says nothing a reader can check
🚫  🟡 in flux · v0.9.0           ← that is the title's job
```

`🔴 OPEN` on a unit that ships is almost always a page nobody finished, not a real judgment.

## 🎯 Aims and States on a roster page

A roster page's Aims are **the unit's own open work**, not the page's. The page is finished the moment it describes the unit truthfully; the unit is not.

Three sources fill them, and the third is the one people miss:

```
① what the unit itself still owes      unbuilt verbs, unwritten contracts
② what is unproven about it            shipped but never run, never measured
③ a defect another page ROUTED here    because this unit ships the file
```

③ is correct routing, not passing the buck: the page that finds a defect is rarely the page that ships the file, and a finding parked on the finder's page is a finding nobody owns. Name the page it came from.

States carries one dated record per real event, in the base's `- YYMMDD WHO · <emoji> <title>` form with indented body lines. **Never leave `Page generated <date>. Nothing ruled yet.`** on a page whose unit ships: that is the generator's stub, and it is a claim that nobody has looked, which stops being true the moment somebody has.

## 🗄 When a unit retires

`git mv` the page into `_archive/`, remove its line from `board.md` `## Pages`, and add BOTH its id and its old `Q-Skill-<name>` alias to `## Links` pointing at the archived path, so every existing citation still resolves. Then grep the board for prose that still names the unit as live: a Log line recording what was true when written STAYS, and a sentence in live prose claiming it still ships is now false.

Proven on `haipipe-board-index`, retired 260802: the page went to `_archive/`, its id still resolved, and the sweep found eight live-prose sentences on four other pages plus one dead citation on a sibling board.

## 📂 Files

```
haipipe-board-page-for-skill/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The generator is `haipipe-board/cli/skillpage.py`; the base frame is `haipipe-board-page`; the writing standard is `haipipe-board/ref/writing-rules.md`; the roster's design record is the board's `QC3a` (how a folder becomes a page) and `QC1b` (which units exist at all).
