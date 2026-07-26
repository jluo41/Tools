# ① The shared model, and the words it owns

state: 🟡 PARTIAL
owner: JL
method: inventory the folder, separate what it defines from what it delegates, and name the one thing it holds that it cannot run

## Question
What is in `probe/haipipe-probe/`, and what does the rest of the layer take from it?
Four files and a fixture, defining the anatomy, the loop, the ladder, the QA contract, the two laws, the derived states and the FAIL codes.
Everything else in the layer copies from here and says so in its own first lines.

The folder is the constitution and it holds no runtime.
Nothing in it dispatches, checks, or writes a probe file, so a reader looking for the enforcement will not find it here, and a reader who changes a word here has changed nothing until five other files are edited by hand.
That is the shape worth stating plainly, because the folder's name suggests it is the layer and it is the layer's dictionary.

## Boundary
- ✅ Covered here
  What is in the folder, what it defines, what it delegates, and the one artifact it holds for code it does not contain.
- ↪ Covered elsewhere
  Which file wins on a conflict and what strings must be propagated is `QD1`.
  The adapters that hold the runtime are `QA4`; the agent is `QA3`; each rule's own page is the rest of this board.

## Diagram
```
   probe/haipipe-probe/     v0.9.9 · last touched 2026-07-19
   ├── SKILL.md                353 lines   THE CONSTITUTION
   │     the four forms · the five-step loop · the cost ladder
   │     the probe-file anatomy · the QA state-line contract
   │     the two LAWS · the seven derived states · 11 FAIL codes
   │     ⚠️ "ONE SOURCE FOR THE VOCABULARY" — line 22
   ├── ref/probe-template.md   143 lines   the fillable form
   ├── test/
   │     fixture/proj/         a whole synthetic project
   │       papers/Paper-Fx/1-probes/PP01_states/  5 QX states
   │       tasks/ · discoveries/  with QA/ files
   │     run-checker-tests.sh   drives check-probe-cards.sh
   │                            ── which lives in ③ and ④ ──
   └── CHANGELOG.md

   it DEFINES everything and RUNS nothing.
   the one file that could run is a test for code in another folder.
```

## Content
### 1 · What it defines, and what it hands off
#### The constitution is one file, and both adapters name it in the same words
(`⭐ THE MODEL IS NOT THIS FILE'S`, written identically in `③` and `④`)
`SKILL.md` owns the probe-file anatomy, the five-step loop, the cost ladder, the QA state-line contract, the two LAWS, the seven derived states and the checker's FAIL codes.
Both adapters open by disclaiming ownership of all of it and pointing back here, in matching sentences, which is the strongest evidence the split was deliberate rather than accidental.
The line it draws is between the MODEL and the DO-THIS: `Phase rules` near the end are followable checklists, and the file says that on any conflict the model sections above win.

#### It also ships the layer's four verbs
(three report, one routes, and none of them executes a loop)
`/haipipe-probe` alone returns the operational contract, `contract|anatomy` returns the entry anatomy and the QA contract, and `status` derives every entry state from disk on each run and stores nothing.
The fourth, `/haipipe-probe "<question>"`, ROUTES rather than executes, and the test it applies is `QB7`'s.
Enumerating them is a glossary entry rather than a ruling, which is why they sit here with the folder that ships them instead of holding a page of their own.

#### Three things it deliberately does not own
(each named in the file, each pointing somewhere real)
The harvest lanes belong to the workers: `**values**:`, `**sources**:` and `**displays**:` are called out as HARVEST-LANE fields that "belong to the probe WORKERS, not to this model".
The executor-side flow that writes a QA file belongs to `../../task/haipipe-task/fn/qa.md` and its discovery twin.
The rationale belongs to `⑥`, which the metadata summary and line 19 both name as "spec + rationale".

### 2 · The vocabulary rule, stated at the top of the file it governs
#### Five strings, named individually, propagated by hand
(a `state:` value, a field name, `QA_WORKING_TTL_HOURS`, `YYYY-MM-DDTHH:MM`, `set -C`)
The rule is in the right place and it is specific, which is more than most shared-vocabulary rules manage.
It names the copiers too: the task and discovery twins, the `qa` verbs, the probe workers, and `check-probe-cards.sh`.
Nothing compares the copies, so a rename is invisible until a checker passes on a file it no longer understands, which is `QD1`'s open item and not this page's.

### 3 · The fixture for a checker that is somewhere else
#### `test/` builds a whole synthetic project to drive code from another skill folder
(five QX states, a papers tree, a tasks tree and a discoveries tree)
`test/fixture/proj/` carries `papers/Paper-Fx/1-probes/PP01_states/` with five files named for the states they exercise: planned, harvested, answered-not-read, concern, and a lying receipt.
`run-checker-tests.sh` then runs `check-probe-cards.sh`, which is in `③` and `④` and forked between them.
So the shared half owns the test and neither fork owns it, and nothing in the harness records which fork it ran, which means a green test proves one of the two is healthy without saying which.

## Items to Finish
- [x] 📚 The folder's contents are inventoried, with what each file is for
      Four files and a fixture, measured 260726: 353 + 143 lines plus a synthetic project covering five QX states.
- [x] 🪧 What it defines is separated from what it delegates
      Anatomy, loop, ladder, QA contract, laws, states and FAIL codes are its own; harvest lanes, the `qa` verb and the rationale are named and handed off.
- [x] 📖 The vocabulary rule sits at the top of the file it governs
      Five strings named individually, with the list of copiers beside them.
- [ ] 🔢 The version scheme is repaired, or the citations are
      `CHANGELOG.md` runs 7.10.0 → 8.x → 9.6.0 and then **0.9.9**, so the current version sorts below its own history.
      Thirteen citations across eight files still pin `probe SKILL 8.2.0`, `8.0.0`, `8.3.0`, `9.0.0`, `9.5.0` and `SKILL.md 6.0.0`, none of which can be ordered against 0.9.9.
      This matters here rather than in `QD1` because propagation is unverifiable when the version numbers do not order.
- [ ] 🧪 The fixture names which checker fork it ran
      `run-checker-tests.sh` drives a forked script and records nothing about which copy answered, so a pass is not attributable.
      This closes when the harness runs both forks, or names the one it runs.
- [ ] 📖 A worked example of every entry state ships with the skill
      The fixture covers five states as test inputs; the prose shows one filled entry and no others.
      A reader learning the layer reads the prose, not the fixture.

## Where we are
The constitution is well placed and unusually explicit about its own limits: it names its copiers, it names what it does not own, and it says which file wins.

Two gaps, both about the gap between defining and running.
The vocabulary rule is propagated by memory, which is `QD1`.
And the only executable thing in the folder is a test for a script that lives in two other folders in two versions, with no record of which one it exercised.

## Files
- `SKILL.md`
  The constitution. 353 lines, and the vocabulary source for the whole layer.
- `ref/probe-template.md`
  The fillable form and the per-field rules.
- `test/`
  The fixture project and `run-checker-tests.sh`.
- `CHANGELOG.md`
  Where a vocabulary change becomes visible to the skills that copy from it.
