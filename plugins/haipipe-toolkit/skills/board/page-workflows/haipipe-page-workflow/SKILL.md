---
name: haipipe-page-workflow
description: >-
  The RUN router of the page family: two PARTS over ONE Board Page. The
  OUTLINE part (SHAPE → SURVEY → LAND → EMBED → SHAPE, until the plan and its
  runs agree) and the DRAFT part (WRITE, a machine loop with an AI pre-check,
  then CHECK, a cold judge and a person). Owns the cycle verbs, the phase
  receipt, the stop rules and the boundary between the parts. RUN is not
  ADVANCE; only CHECK may CLOSE. Trigger: run a page, run page lifecycle,
  outline part, draft part, page run receipt, /haipipe-page-workflow.
metadata:
  version: "0.25.1"
  last_updated: "2026-09-02"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-workflow · two parts, six cycles, one auditable RUN

`haipipe-page` is the door for ONE PAGE and says what a page IS.
This skill is the head of the page WORKFLOW: it drives one existing Page through its two parts as a bounded loop and leaves a receipt.
It moved here from `haipipe-page`'s RUN verb on 260815, so the workflow pattern reads the same in every family: one folder, one head skill, its member skills beside it.

**Who owns what**:

```
haipipe-page               what a page IS · CREATE · WORK ON
haipipe-page-workflow      RUN · the two parts · the packet · the receipt · the stop rules
page-workflows/ members    each phase's own authority: outline (SHAPE, SURVEY) ·
                           evidence (LAND, EMBED) · draft + revise (WRITE) · check (CHECK)
haipipe-board              the machinery this skill calls, never contains
```

## 🔁 The loop has TWO PARTS, and each ends where a person is (260901)

Ruled by JL on 260901, replacing the 260819 PREPARE/①-⑦ shape: "definitely,
we should separate them into the Outline part and Draft part"; the cycles go
by their WORDS, never a letter code (`C<n>` is a Content division in every plan
address, `W` the Wisdom handoff), never a circled number (the ①-⑦ mirrors
drifted within a day on 260819).

```text
OUTLINE part · the page decides what is TRUE and what it will therefore say
  SHAPE    haipipe-page-outline    plan + typed evidence expectations     👤 approved:
  SURVEY   haipipe-page-outline    supports + PageX + input + local Run   👤 Decide per item
  LAND     haipipe-page-evidence   validate sources → local Result         ⚙ every make-item ready
  EMBED    haipipe-page-evidence   fold ready Results into plan v<N+1>    ⚙ back to SHAPE
           └─ at SHAPE the tick carries the fork:
              approved + fresh items   → SURVEY again
              approved + every item folded → the DRAFT part

DRAFT part · the page is WRITTEN against a plan already agreed
  WRITE    haipipe-page-draft +    draft → revise → compile, chained; an inner
           haipipe-page-revise     machine loop: teeth → AI cold pre-check →
                                   revise, budget 3, a finding surviving two
                                   rounds = HOLD                          ⚙ ready
  CHECK    haipipe-page-check      a cold judge reads the BUILT page, then
                                   the person reads                       👤 accepted:
           └─ prose → WRITE · a number, citation or figure → SURVEY ·
              the argument itself → SHAPE · pass → CLOSE
```

**The law that makes the OUTLINE part converge**: SHAPE names each typed
Evidence Item and the ready Result it expects. SURVEY plans zero-to-many
Execution/Discovery Supporting Runs, optional exact PageX bindings, plus
exactly one local Page Evidence Item Run. LAND validates every supporting
Result and PageX authority, freezes one Local Input, and finishes the local
Run; EMBED interprets only the ready local Result.
The one authored ledger is `outline/<stem>-evidence-items.md`
(`haipipe-plugin-outline/ref/item-table.md`). Status is derived as `specified →
planned → ready → folded → accepted`, plus `stale · deferred · dropped · blocked`.

### Phase × Run Map · the workflow-level table every skill set must publish

| Cycle | L3 Task content modified | L4 Runs | Input / policy | Skill chain | Close / handoff |
|---|---|---|---|---|---|
| SHAPE | outline plan + item identity/expectation/acceptance | none | brief + phase-owned outline/narrative/style policy | `haipipe-page-workflow → haipipe-page-outline → haipipe-plugin-outline → <owning phase, e.g. haipipe-paper-narrative>` | approved typed plan |
| SURVEY | Evidence Item Supporting Runs + PageX Bindings + Local Input + Local Run plans + Decide | none | approved item contracts + existing Run/source inventory | `haipipe-page-workflow → haipipe-page-outline → haipipe-run → haipipe-plugin-outline/ref/evidence/pagex.md` | every item graph and exact source binding valid and decided |
| LAND · Supporting | item ledger gains resolved Run IDs and validated PageX authorities | Execution/Discovery `0..N` per item | selected Tickets/Results + exact PageX files/Results | `haipipe-page-workflow → haipipe-page-evidence → haipipe-run → haipipe-plugin-evidence → <Execution/Discovery worker>` | every Supporting Result and PageX binding valid |
| LAND · Local | item ledger binds frozen input, local Run ID, and typed Result | Page · Evidence Item exactly `1` per make-item | one envelope of Supporting Results + PageX/local sources | `haipipe-page-workflow → haipipe-page-evidence → haipipe-run → haipipe-plugin-evidence` | both Run layers finished; one ready local Result per item |
| EMBED | outline v<N+1> fold lines | none | ready local Results | `haipipe-page-workflow → haipipe-page-evidence` | return to SHAPE |
| WRITE | Page Content division | Page · Division Writing, one per commissioned division | approved evidence-aware outline + writing/style policy | `haipipe-page-workflow → haipipe-page-draft/haipipe-page-revise → <owning phase>` | built Page ready for CHECK |
| CHECK | receipt/findings; no producer mutation | none | built Page + plan + acceptance policy | `haipipe-page-workflow → haipipe-page-check → <owning phase gate>` | CLOSE or route back |

`<owning phase>` is an exact installed skill name, never a generic Page-Type
placeholder. For a paper Narrative Folder it is `haipipe-paper-narrative`.
There is no `haipipe-page-for-task` hop in the current chain.

**Why the parts split where they do.** The OUTLINE part is where the page
decides WHAT IS TRUE; everything after is execution against a plan already
agreed. A wrong sentence is cheap to fix; a wrong plan has already been paid
for in runs. So a person's two gates sit at the FRONT (`approved:`, `Decide`)
and one at the EXIT (`accepted:`); between them the machine runs unattended
(JL 260819: "if not, you can just go ahead for the draft and revise and the
compile"), and a controller that halts inside WRITE for a person is halting in
the wrong place.

**The boundary is hard.** The DRAFT part refuses to start until the OUTLINE
part has exited: plan `approved: ✅` AND every `☑ make` item `folded`. A hole
found later is a ROUTE BACK (CHECK → SURVEY or SHAPE), never patched inline.
Each part is separately runnable (`run <page> outline` walks SHAPE→EMBED and
stops; `run <page> draft` walks WRITE→CHECK; `run <page>` does both through
the boundary).

**EMBED always returns to SHAPE, and SHAPE's tick carries the fork.** The
embedded plan is a new version and the person agrees it like any other; the
machine never decides that the part is over. Back to SURVEY only on a
STRUCTURAL change (a landed answer that breaks a bullet's claim); a number
filling a hole is absorbed by the fold.

### The WRITE loop · automatic, bounded, judged cold

```text
WRITE round n
  1 WRITE pass      draft (round 1) or revise (round 2+); compile folded in
  2 TEETH           mechanical, first, free: every bullet realized
                    (realizes: coverage) · every number has its PP<NN>.v<n> or
                    result source · citations resolve · latex compiles ·
                    the writing-score floor (haipipe-writing score.py)
  3 AI COLD READ    a FRESH check-agent context (pre-check mode) reads the
                    BUILT version against plan + Aims; returns findings, and
                    may only say "another pass" or "ready" — never CLOSE
  4 findings → round n+1
exit to CHECK when the cold read returns zero blocking findings
stop rules: 3 rounds; the same finding surviving two consecutive rounds is a
HOLD shown to the person with the trail; the producer never declares itself done
```

Teeth before the cold read: never spend an AI judgment on a version that
fails grep-level checks. Cold means cold: an in-thread "looks good" is
contaminated by construction.

### A person's "no" at CHECK · routed, never a dead end

The person's disagreement is one sentence, landed as a feedback record in
`outline/`; `accepted:` simply stays unticked. It is ROUTED exactly like a
machine finding (wording → WRITE · a number, citation, figure → SURVEY, the
table gains or revises a row · the argument → SHAPE). A checkable "no" is
PROMOTED into a tooth or a pre-check rule (the approver promotion law,
`agents/approve-rules/`), so the machine catches it every time after. The
machine's "ready" was always a floor, not a verdict; the same "no" twice means
the fix was routed too shallow, so it escalates one level.

## 🤖 ONE agent per display unit, and the skill chain it walks (260819)

JL 260819: "each display you can have a subagent to call the specific skills to
work on it, right?" Yes, and the fan-out unit is the UNIT, not the page:

```text
  one 🖼 row  ─▶  one display unit  ─▶  one agent instance   (at LAND)
```

Four units on `QPw00-page-loop` went stale the moment the loop's phase order
changed, and four agents rebuilt them in parallel. Each one owns exactly one
folder and may not touch the page's prose or a sibling unit.

**The chain each agent walks, three layers:**

```text
  ① the agent      display/agents/haipipe-display-unit-agent
                   resolves the intake, writes recipe/ · assets/ · README.md
  ② the one door   haipipe-display
                   reads README's `kind:` row and routes
  ③ the renderer   📊 table  → haipipe-display-table
                   📈 figure → haipipe-display-figure
                   📐 diagram→ haipipe-display-diagram
                   ✒️ tex    → haipipe-display-tex
                   🎨 illust → haipipe-display-illustration
```

**Why the fan-out is safe.** Each unit is a separate folder with its own intake,
recipe and README, so two agents cannot collide. The dispatching cycle keeps the
two things an agent may NOT do: it never ticks `accepted:`, which is a person's at
CHECK, and it never edits the sentence that cites the unit, which is WRITE's.

**What every such dispatch must carry**, because a display agent in a fresh
context knows none of it:

```text
  the unit's absolute path        it owns one folder and nothing else
  WHY it is stale                 which frozen input changed, from checks/intake.py
  what changed, as facts          plus the files that are the AUTHORITY, so the
                                  agent verifies rather than trusting the prompt
  the rebuild commands            the unit's own, from its README
  the verification to run         checks/intake.py must stop reporting it
```

⚠️ **"An input moved" is not "the figure is wrong."** One of the four was told to
DECIDE first and redraw only if a specific line had become false. A re-freeze is
not a redraw, and a figure rebuilt for no reason loses its own history.

## 👷 One producer agent per phase (260819), two cycles per producer (260901)

Ruled by JL an hour after the fan-out: "for the creator-agent, it should have the
outline-agent, etc." The display precedent generalizes to the whole loop:

```text
  phase        agent (skills/board/page-workflows/agents/)     cycles          fan-out?
  ──────────────────────────────────────────────────────────────────────────────────────
  OUTLINE      haipipe-page-outline-agent                      SHAPE · SURVEY  no — the plan
                                                                               is ONE file
  EVIDENCE     haipipe-page-evidence-agent                     LAND · EMBED    LAND fans out:
                                                                               one display-
                                                                               unit-agent per
                                                                               🖼 row
  DRAFT        haipipe-page-draft-agent                        WRITE step 1    no
  REVISE       haipipe-page-revise-agent (COMPILE folded)      WRITE step 2    no
  CHECK        haipipe-page-check-agent                        WRITE's pre-    no — one
                                                               check · CHECK   version, one
                                                                               cold judge
  verbs/base   haipipe-page-creator-agent keeps create-page and
               revise-opening and is the producers' BASE;
               haipipe-board-reviewer-agent keeps whole-BOARD
               reviews and is the judge's BASE
```

`haipipe-page-probe-agent` retired 260901 with its phase: the MATCH half is
SURVEY's table, the dispatch half is LAND's card, and the one courier out is
still `haipipe-probe-q-executor-agent`.

**The thin-wrapper law, and it is what makes six files safe:** a phase agent
carries identity, its skill chain, role walls and the receipt duty, and
restates NOTHING a contract holds. A restated route table or tick rule is a
mirror, and on 260819 every mirror on this board — phase-cards numbers, the
route code, four of five figures — drifted within a day of the loop changing.
The packet, procedure, house rules and return contract live once, in
`ref/producer-contract.md` (carved out of the creator agent later the same
day, so no agent reads another agent's file).

**A pass performed in a person's own session** (the 🎨 Studio chat,
`haipipe-plugin-chat` §🔁) is a pass when it leaves the same trace an agent
leaves: the artifact, one log record with the receipt folded under it, and the
strip in the reply. What this section forbids is the edit that leaves none of
those, and the judgment of a version by the session that produced it: CHECK is
always a fresh context.

## 🧑 Where a RUN stops for a person, and the mode that decides

```text
  OUTLINE part   SHAPE ⇄ SURVEY ⇄ LAND ⇄ EMBED     🧑 ATTENDED · approved: · Decide
                 │
                 ▼
  DRAFT part     WRITE (auto-loop)                 🤖 UNATTENDED
                 CHECK                             🧑 judges · accepted:
```

**"if we want" is a MODE, and since 260821 the packet carries it.** `mode:
copilot | auto` — one rule set, two readings, never two rule sets:

```text
  🧑 copilot   the human half BLOCKS       a person is here; wait for them
  🤖 auto      the human half DEFERS       the loop moves on the machine half
                                           (`checked:`) and the debt lands on
                                           the ledger, `--owed`, once at the end
```

**Auto defers selected plugin ticks; the owning phase decides whether a RULING
exists.** `approved:` `verified` `read:` and `accepted:` each have a rules file,
so an approver can establish everything around them. A phase-owned Folder's
`page_ruling` declares `none | domain-gate | local`: `none` adds no owner gate,
`domain-gate` reuses the workflow's gate receipt, and `local` keeps a Page-local
RULING. The latter two are nonwaivable and the controller hardens them even when
the caller omitted `human_gate.required`. A Page without phase metadata keeps the
legacy behavior: auto hardens its local RULING. `ref/page-run-contract.md` §🔀
fixes the packet and the audit invariant behind the write-back. The `Decide`
field of the Evidence Item table is a person's in both modes; auto may leave an
item `☐` and LAND then refuses it, reporting the item as still in SURVEY.

Every step reports its `phase:` and its `cycle:` to whoever is watching, not
only into the receipt: work that does not name its cycle cannot be routed or
audited.

**The phase strip mechanizes that duty** (JL 260820: "I want to have a status
strip to show what phases we are in"). One command, one row per phase, derived
from DISK plus the newest receipt, never from what a page says about itself:

```bash
python3 <haipipe-board>/cli/pagephase.py <page-dir>        # --md to paste on a page
python3 <haipipe-board>/cli/pagephase.py <page-dir> --owed # the LEDGER, see §✋
```

```text
✅ 🧭 OUTLINE   v4 approved · marks 📮4 🧮0 📚0 🖼0 · items 4 · decided 4/4
⏳ 🃏 EVIDENCE  landed 3/4 · folded 0/4 · 📚 0/0 verified · 🖼 0/0 drawn
⏳ ✏️ DRAFT     3 content divisions · page predates outline tick
⏳ 🖊 REVISE·⑥  latex/ present · pdf STALE/none
⬜ 🔍 CHECK     last receipt: OUTLINE → HOLD (round 1)
→ now: LAND · ✋ human ticks still owed: 1
```

**✋ is a COUNT; `--owed` is the LEDGER, and that is the copilot/auto join.**
A count says there is a debt. It never says where to spend the one act that is a
person's, which is why `QPw00g-human-gate` carried "no surface joins the owed
ticks" as an open ruling. `--owed` is that join: one row per owed tick, each
carrying the approver's `checked:` beside the question only a person can answer.

```text
 1. 🧑 approved  outline/QB3-diet-outline-v3.md
      v3
      🤖 not checked yet · approve-rules.md has never run here
      ❓ is this the DIRECTION I want, and is this round worth doing now?
```

One artifact, two readings, and this is what makes the two modes ONE mechanism
rather than two rule sets that drift:

```text
  🧑 copilot   you watch the list shrink and answer as you go
  🤖 auto      the run does not stop; the list is what you are handed at the end
```

⚠️ **The ledger is variable, but its count/list invariant is fixed.** Plugin
artifacts select their own ticks; the phase contract selects the owner RULING.
Legacy Pages conservatively keep one. `sum(ticks_owed)` always equals
`len(owed_ledger())`, and `tests/test_page_phase_ledger.py` asserts mechanical,
domain-gate, and legacy cases.

⚠️ The `→ now` row is the first cycle whose exit test FAILS, in loop order: a
REPORT, never a routing. Which cycle runs next stays with the authority test
(§🔤), and CHECK may still route anywhere. Sit it beside its two siblings:
`status.py` answers "where is this SESSION", `pagestatus.py` "where is every
page in this GROUP", `pagephase.py` "which CYCLE is this PAGE in".

**And the strip rides in the closing block** (JL 260820: "how to update this so
I know which phase of the page I am in?"). A page-focused `status.py` prints
the same state as a fourth row, so every reply about a page says where the page
is without anyone running a second command:

```text
⏱️ LAND · 🧭✅ 🃏⏳ ✏️⬜ 🖊⬜ 🔍⬜ · ✋1
```

**What each phase COSTS is measured, not guessed**: `ref/measured-cost.md`
carries real agent returns from the 260820 QC1 and QC2 runs, minutes and tokens
and tool calls per phase (JL 260820: "could you document for each of them, how
long it takes for us?"). The short version: wall-clock tracks TOOL CALLS at
about 14 seconds each, EVIDENCE is the longest phase because it opens the most
files, a display unit runs 5 to 17 minutes, and fanning the display lane out is
the one real speedup in the loop.

The bar reuses one phase emoji set (🧭 🃏 ✏️ 🖊 🔍); CHECK carries 🔍 in the
bar because ✅ is the strip's DONE marker. Circled digits were the first attempt
and JL could not read them at terminal size (260820); they retired from the
contracts on 260901.

Both forms read `haipipe-board/src/page_phase.py`. One computation, two
surfaces: a second copy of the phase rules would go stale the first time this
loop changed, which is exactly the §🪞 failure this family already records.

## 🔤 Five words, and none substitutes for another

```text
word         answers                    in one receipt        repeats?
──────────────────────────────────────────────────────────────────────
🌀 WORKFLOW  which LOOP is this?        the run itself        no
📦 PART      OUTLINE or DRAFT?          implied by `cycle:`   YES
⏱️ PHASE     which AUTHORITY acts?      `phase:`              YES
🔄 CYCLE     which PASS of it?          `cycle:`              YES
🧮 STEP      WHERE in this run?         `step:`               never
🔁 ROUND     which PROMISE era?         `round:`              on reopen
```

⚠️ **PHASE may not be renamed to STEP** (JL weighed it and ruled against it, 260818).
`step` is already a field meaning the monotonic position, so one receipt would carry
two meanings on one key. A phase is a TYPE and a step is an INSTANCE of one: in
`260805-0216-QB8e` the single CHECK phase occupies steps 1, 3 and 5. The word must
permit repetition, which is the same reason RUN is not ADVANCE. `QPw00 §11` argues it.

A phase is the SKILL that acts (outline · evidence · draft · revise · check); a
cycle is the named pass inside it (SHAPE or SURVEY inside OUTLINE, LAND or
EMBED inside EVIDENCE, WRITE across DRAFT + REVISE, CHECK alone). Each may
repeat; SURVEY and LAND are skipped when the plan promises nothing it cannot
already support; CHECK may route back to any earlier cycle. Which cycle runs
next is decided by AUTHORITY (`haipipe-page`'s authority test), not by
position, which is why the verb is RUN and not ADVANCE.

**Five phase members, and the retirement that made them five (260901):**

```
phase       authority                                          load
────────────────────────────────────────────────────────────────────────────────
OUTLINE 🚧  SHAPE writes <page>/outline/<stem>-outline-v<N>.md,  ../haipipe-page-outline
            the plan down to the POINT, each owed thing a named    (the plan's shape is
            E<NN>-VALUE/CITE/DISPLAY item with expectation and      haipipe-plugin-outline §📐,
            acceptance; SURVEY completes <stem>-evidence-items.md  the table's is its
            with support/PageX/input/local Run plans and Decide     ref/item-table.md)
EVIDENCE ⚖️ LAND validates each item's Supporting Results and     ../haipipe-page-evidence
            exact PageX authorities, freezes one input, then
            executes exactly one local Evidence Item
            Run; EMBED writes ready Results into plan v<N+1> and
            returns to SHAPE
DRAFT       instantiate each Point as sentences with real numbers  ../haipipe-page-draft
REVISE      realize the prose, cite units by id, caption, and       ../haipipe-page-revise
            COMPILE latex · pdf · word (folded in)
CHECK       judge the BUILT version and route its authority;       ../haipipe-page-check
            in pre-check mode, gate WRITE's inner loop
```

PROBE retired on 260901 with `/haipipe-probe`. SURVEY now plans the graph using
two separate dimensions: family (`Execution | Discovery`) and action (`reuse |
rerun | new-run | new-task | new-job | new-block`). LAND executes that graph.
`found`, `person`, and `none` are not current actions. The 260817 splits still hold
(OUTLINE ≠ DRAFT: one phase must not agree the shape AND write the page;
raising ≠ landing: a card at `raised` bound to a bank that did not exist read
as done; REVISE ≠ COMPILE: "the prose is right" shipped a PDF full of raw
`<!-- -->`).

Legacy outbound-card history is read-only migration input. The current typed
Evidence Item graph reads any retained aggregate only through a declared
Supporting Result and never creates a new `probe/` lane or card.

## 🪪 Each phase in SIX fields · `ref/phase-cards.md`

JL asked the question this section exists for (260818 1402): "if I want to work
with the page workflow's each phase, what should each phase do". Every phase
contract already answered it, and no two answered in the same fields, so
`ref/phase-cards.md` states every cycle ONCE, in the same six fields, in loop
order:

```text
❓ ASKS     the one question the cycle answers
📥 READS    what must already exist, or the cycle cannot start
📤 WRITES   the exact path it creates or changes
🚪 EXITS    a testable condition
✋ TICK     the person-reserved tick, or none
🔀 ROUTES   where it may go next
```

**The operational rule is the 🚪 EXITS row: you work a cycle by satisfying it.**
The cards declare their possible plugin ticks. The owning domain phase then adds
no RULING, reuses its domain gate, or declares a local one; cycles with no
selected tick run machine-only from start to finish.

That file is a SUMMARY and this family is its source. When the two disagree, the
phase contract wins and the card is the defect.

## 🃏 One typed item through planning, Runs, and the Page

```text
SHAPE    E01-VALUE-adjusted-effect
         Target + Label + Need + Expected + Acceptance     specified
SURVEY   Supporting Runs: Execution/Discovery 0..N
         PageX Bindings: exact accepted cross-Folder sources 0..N
         Local Run: Page · Evidence Item exactly 1          planned
LAND     validate supports + PageX → freeze one input → local Run
         → one typed ready Result                           ready
EMBED    `Answered: E01… · interpretation · Result`         folded
WRITE    one or more Division Writing Runs realize prose
CHECK    accepted: on the Page                              accepted
```

SHAPE and SURVEY modify planning content in the L3 Task Folder but mint no L4
Run. LAND is where work identities begin. Different item graphs may execute in
parallel; within one item the local Run waits for its declared supports and
PageX bindings. This is not a contradiction with parallel LAND—the dependency
is local to the item.

`stale` is the reopen law: a changed Supporting Result or PageX authority
invalidates the frozen local input; a changed local Result invalidates the fold. The historical Runs
stay immutable while LAND or EMBED repeats with the correct identity.

## 🪞 The page never writes prose about what a plugin already holds

Every cycle can fail the same way, and on 260817 one page failed it three times in one session (`QC1-visitlbp`, CMSRegBoard). The failure is writing a SENTENCE where a THING belongs.

```text
what got written into the page body        what already held it        what happened
────────────────────────────────────────────────────────────────────────────────────
the DRAFT outline table, pasted into       🧭 the outline plugin,      two copies, and the
`## Content`                                which derives it from       body copy goes stale
                                            the ### headings            the next edit
"Evidence owed: E03 is specified"          🧭 Outline Evidence         the sentence carries a
                                            Workspace renders it        state the item owns
                                            and its live status         and will contradict
"evidence owed: 🖼 display"                 🖼 the display surface      🚨 ZERO units existed.
                                                                        The sentence WAS the
                                                                        whole deliverable.
```

**The rule.** A plugin owns a kind of material and a surface that shows it. The page's prose CITES that material by id and never restates it. `Display1` in a sentence is a citation; "a display is owed here" is prose pretending to be work.

**The rule that catches the third row, and it is the one that matters.** A cycle may not report done while it DECLARED an artifact it did not CREATE. Declaring is free; the receipt must record the count.

```text
  ✅ 4 rows decided · 4 results on disk
  🚨 1 display declared · 0 unit folders on disk   ← the cycle is NOT done
```

`haipipe-page-check` already rules that a declared unit which never rendered is a CHECK finding. That rule never fired here because CHECK never ran: the work was called done at DRAFT. So the count moves EARLIER, into every cycle's own receipt, and a cycle whose declared-versus-created counts disagree stops rather than reports.

**And the third failure of the same session, for the receipt to catch too**: verify the artifact the READER opens, not the one you just wrote. That session checked the built HTML and shipped a PDF full of raw `<!--` comments and literal `**`; checked `build.py`'s exit and served a page four minutes stale; and guessed at a CSP instead of opening the screenshot that showed the tab rail working perfectly. Wire green is not UI green (JL, standing rule).

## 🔁 run one Page lifecycle

RUN is the automatic, bounded loop. Use it when the process itself must be
exercised and audited, rather than when one known edit is enough.

1. Read `ref/page-run-contract.md` and assemble its raw-material packet. Resolve
   the owning Folder contract first: authoritative `workflow/phase.yaml`
   current kind, then Page `folder-kind:`; use `page-type:`/filename only as a
   legacy fallback. For a new Page, CREATE and register it first
   (that verb stays with `haipipe-page`), then start at OUTLINE (SHAPE). For an
   existing Page with no known next authority, start at CHECK. Before each phase
   dispatch, materialize that phase's Related Board Pages packet with
   `haipipe-board/cli/pagecontext.py`; an invalid row or missing scope is a
   named HOLD, never omitted context.

   Two duties precede any dispatch to CHECK, both priced on a live run (260828):

   ```text
   ① CURE SELF-REGISTERED DEBTS FIRST   a version whose own state line or Open
     division names an uncured debt is a KNOWN-DIRTY version; a cold judge
     bought against it returns the registration as its route, which is a paid
     confirmation (~77k tokens and one whole round on the run that priced it)
   ② RUN THE EXIT SWEEP                 the producing phase's exit checklist
     (the official-document sweep in the draft and revise contracts) is a
     MECHANICAL pre-dispatch step: grep each cured fact's keywords across the
     state line, Aims, States and Open, so no clause still tells the old story
     (one skipped sweep forced a third CHECK on the same run)
   ```
2. Invoke `haipipe-board/ref/page-lifecycle.workflow.js` with the packet,
   **FROM THE MAIN SESSION**, as ONE object with the packet in `args`:

   ```text
   Workflow({ scriptPath: "<abs>/…/ref/page-lifecycle.workflow.js",
              args: <the packet, a JSON OBJECT> })
   ```

   🚫 **Do not delegate this step to a subagent.** A subagent is not handed the
   `Workflow` tool. `haipipe-page-auditor-agent` declared it, was dispatched
   for the first time on 260818, and returned `blocked` at this exact step with
   0 steps and no receipt. That agent is a packet builder and a receipt keeper
   since 0.3.0; the dispatch is the main session's and cannot be moved.

   The workflow then dispatches a phase-scoped producer for OUTLINE, EVIDENCE,
   DRAFT, REVISE, or COMPILE, a mechanical builder/version snapshot, and a
   fresh read-only reviewer for CHECK. The producer's return names its
   `cycle:` beside its `phase:`.
3. Follow returned routes rather than a prescribed order. Only CHECK may CLOSE.
   A route to DRAFT from another phase begins a new round only when purpose or an
   Aim reopened.
4. Stop at CLOSE, explicit HOLD, a missing input, a version mismatch, a required
   human gate, `max_steps`, or `max_rounds`. A limit stop means the run did not
   converge; it never means quality passed.
5. Write the exact Workflow result to
   `<board>/_runs/page/<page-id>/<run-id>.json`. Do not append the terminal CHECK
   result to the Page, because that would mutate the approved version.
6. Run `haipipe-board/cli/pageflow.py audit <receipt.json>`. Report the terminal
   route, checked version, traversed edges, deterministic finding count,
   semantic finding count, human-gate state, and residual risk.

RUN never lets one hidden pass write, judge, fix, and approve. The producer and
judge have different actor identities, and every changed version returns
through CHECK before CLOSE.

## 🧾 The receipt is the workflow's one state source

`<board>/_runs/page/<page-id>/<run-id>.json` is where a run's history lives, in the exact shape `ref/page-run-contract.md` fixes.
A surface that shows where a page stands in its lifecycle reads these receipts and nothing else, the same way the labeling stepper reads `## States`.
That surface ships: the 🪜 Workflow menu's `📄 Page phases` stepper (`haipipe-board/assets/js/10-drawer/65-plugin-pageflow.js`) draws the loop along the bottom of the split viewer, fed by `GET /_board/pageruns` (`live/pageruns.py`), which matches receipts by their own `page` field.
A page with no receipts is not an error: its next authority is the contract's own default, CHECK for an existing page, OUTLINE for a new one, and the stepper states exactly that.

## 📂 Files

**This skill's own files**: what ships in the folder, and what each part is for.

```
haipipe-page-workflow/
├── SKILL.md            this contract
├── CHANGELOG.md        version history
└── ref/
    ├── page-run-contract.md   the packet + receipt spec RUN and its members share
    ├── producer-contract.md   every phase producer's packet, procedure, house
    │                          rules and return shape, in one copy
    └── phase-cards.md         every cycle in the same six fields, in loop order
```

The executable machinery stays under `haipipe-board`: `ref/page-lifecycle.workflow.js` (the controller), `src/page_lifecycle.py` (the deterministic auditor), and `cli/pageflow.py` (the audit CLI).
The non-interactive dispatch target is `agents/haipipe-page-auditor-agent.md`, which invokes this contract in a fresh context.

**The Board pages that argue this family** are the `QPw` group on
`BoardSkillBoard-260722`, re-cut 260818 when JL ruled one page per workflow step
(their numbering predates the 260901 two-part law; `QPw3-probe` is that
cycle's history, and the survey and land cycles are argued on `QPw1` and `QPw4`):

```text
🔁 QPw00  the loop itself: the time axis, RUN ≠ ADVANCE, the audit

⏱️ THE PHASES · one page per phase, in loop order, each one RUNS
🧭 QPw1  OUTLINE (SHAPE · SURVEY)   ✏️ QPw2  DRAFT    📮 QPw3  probe, retired 260901
🃏 QPw4  EVIDENCE (LAND · EMBED)    🖊 QPw5  REVISE   ✅ QPw6  CHECK
   └─ QPw4's three PARALLEL lanes: 📚 QPw4c citation · 🧮 QPw4v value
                                   · 🖼 QPw4d display intake

🔧 THE MACHINE · cuts ACROSS all of them. No position in time; never "runs"
🤲 QPw00a  🎭 WHO acts       the three agent units, and the act each may never do
🧾 QPw00r  📜 WHAT proves it the receipt per attempted phase, chained by hash
✋ QPw00g  ⚖️ WHO says yes    the selected ticks a machine may never write
```

COMPILE has no page because it has no contract of its own; it is folded into `haipipe-page-revise`, and whether that fold is permanent is `QPw5`'s open ruling. Each page's `## Law` rows and its `### Decision Now` carry what its contract leaves open.
