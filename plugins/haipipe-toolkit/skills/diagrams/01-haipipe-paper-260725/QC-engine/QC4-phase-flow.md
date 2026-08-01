# How does a stage call its phases, and may it skip one?
state: 🟡 PARTIAL
owner: JL
method: phases are a declared list, not a fixed type; a skip is legal only when it is announced

## Opening
A stage does not do its own work. It declares a list of phases and dispatches each one to a separate worker skill, in order, and that list is the whole of what "running a stage" means. So two things decide the behaviour of every stage in the system: what is in the list, and whether anything may be left out of a run.

Both are more open than they look. `phases:` reads like a type and is a list, and one stage already proves it: `2a-venue` declares `[draft, probe, check]` with no revise at all. That shape is legal, and it was decided rather than forgotten: `stages/CONTRACT.md:29` makes ends-with-`check` the field's only constraint, the router says "never pad a list to four", and venue's own contract spends nine lines of comment on why a stage that produces a contract rather than prose has nothing for REVISE to polish. What is missing is not the ruling but a test: venue states its own reason, and nothing tells the next contract author when that reason applies to them. And there are two entirely different ways to skip a phase, one at declaration time and one at run time, separated by exactly one sentence in one reference file and nowhere a contract author is sent to look.

The run-time one has already caused real damage. A live seed run silently skipped PROBE and REVISE and drifted into CHECK, and the person running it discovered the missing phase by accident afterwards. The rule written in response is the right one, that a skip must be an explicit logged verdict rather than a silence. It lives in a reference file that the stage router cites by name, and that three of the four phase workers it binds cite nowhere.

Scope: This page covers How the phase list is declared and dispatched, and what a legal skip is. Neighbouring pages cover Each phase's own rules are `QC4a` to `QC4d`; what a re-run does to the page is `QC3c`; what admits a stage in the first place is `QC2`.

## Diagram
```
   🔁 phases:  IS A LIST, NOT A TYPE.

      ┌ stage.md ─────────────────────────────────────────────┐
      │ phases: [draft, probe, revise, check]                 │
      │ gates:  [check]                                       │
      └──────────────────────┬────────────────────────────────┘
                             │  the router walks the list IN ORDER
        ┌────────────────────┼────────────────────┬───────────┐
        ▼                    ▼                    ▼           ▼
   Skill(haipipe-      Skill(…-probe)      Skill(…-revise)  Skill(…-check)
     paper-draft)
      → QC4a               → QC4b                → QC4c        → QC4d

      ⚠️ a phase executed INLINE, rather than through its Skill(),
         did not run. There is no "I did that part myself".

   ── what the eight actually declare ───────────────────────────────
      0-seed          [draft, probe, revise, check]
      1a-resource     [draft, probe, revise, check]
      1b-claims       [draft, probe, revise, check]
      2a-venue        [draft, probe,         check]   ◄── no REVISE
      2b-pitch        [draft, probe, revise, check]
      3-narrative     [draft, probe, revise, check]
      4-display       [draft, probe, revise, check]
      5-section-edit  [draft, probe, revise, check]

      ✅ INVARIANT: the list always ENDS with `check`, and
         `CONTRACT.md:29` states that as the field's ONLY constraint.
      ✅ 2a-venue omits revise BY DECISION, and it is said 3x:
         `CONTRACT.md:29` · router SKILL.md Step 4 "never pad a
         list to four" · `2a-venue/stage.md:13-21`, nine lines of
         comment: venue produces a CONTRACT, not prose.
      ❓ what is missing is a TEST, not a ruling. venue states its
         OWN reason; nothing tells the NEXT author when it applies.

   ── TWO ways to skip, and they are NOT the same thing ─────────────
      ① DECLARED     the contract omits the phase from `phases:`
                     visible before the run · reviewable · permanent
                     this is what 2a-venue does

      ② RUN-TIME     the phase is in the list and is not executed
                     legal ONLY as an explicit logged verdict:
                       one reply line with the reason
                       `[PROBE] skipped -- <reason>` in the S page's
                         `## Log`  ◄── NOT a `_LOG_<stage>.md`: that
                         sidecar was RETIRED 2026-07-26 and no live
                         paper ever carried one
                       `--` on the phase line of the closing block
                     "the draft looks fine" is a verdict to RECORD,
                     never a licence to say nothing.

      📍 default: a NEW artifact runs all four. Skip is for
         RE-ENTRIES and minor edits, which hands the question
         straight to QC3c.

   ── the failure that produced the announce rule ───────────────────
      a live seed run silently skipped PROBE and REVISE and drifted
      into CHECK. The user found the missing phase by accident.
      ⚠️ the rule now says: announce every boundary, one reply line
         + a `[PHASE]` entry in the S page's `## Log` + the phase
         line moves 🔥.   ref/08-stage-gate.md:84-93
      📖 WHO CITES IT: the ROUTER does, by name, at its Step 3, and
         so does CHECK (twice). draft · probe · revise cite it
         NOWHERE, and all three write their `[PHASE]` entry anyway
         (draft:246 · probe:121 · revise:25). The rule is not
         homeless; three of its four obligors have no pointer to it.

   ── per-unit changes what "the list" means ────────────────────────
      runs: per-unit  ──▶  the WHOLE list runs once PER UNIT   (→ QC3b)
      the ROUTER says that much out loud at Step 4. What it does NOT
      say is that a SKIP is then per unit too, and 5-section-edit is
      the only `runs: per-unit` contract, so it meets this first.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   phases · gates
      reader   ③ THE EXECUTOR · an agent walks the list        → QC2
      fails    🔇 SILENT, and it has: a live seed run skipped PROBE and
               REVISE and drifted into CHECK, and the person running it
               found the missing phase by accident afterwards.
      to bind  ✅ the announce rule ALREADY makes this checkable after
               the fact, and nobody has taken the last step. Every
               phase writes a `[PHASE]` line into the S page's
               `## Log`, so "one entry per declared phase, or a
               logged skip verdict" is an assertion. `checks.sh`
               already OPENS that `## Log` under `--stage-page`.
               The evidence is produced and nothing reads it.
```

## Content
### The list is the stage
There is no code path in which a stage does work. It resolves a contract, creates or finds its page, and walks `phases:`, dispatching each name to its own skill. Everything else on this board about stages is a statement about one of those four workers or about the fields the router read on the way in.

That is why "a phase executed inline did not run" is a real rule and not pedantry. A phase has a worker because the worker has its own contract, its own limits, and in PROBE's case its own clean context. Doing the work in the stage's context is not a shortcut past the dispatch; it is a shortcut past the limit.

### Two skips, one word
A declared skip is a design decision, visible in the contract before anything runs, reviewable by whoever reads it. A run-time skip is a judgment made mid-flight about this particular artifact. They deserve different treatment and currently share a word. Exactly one sentence separates them, at `ref/08-stage-gate.md:93`: a phase absent from `phases:` is also `--` on the phase line, but is "omitted by contract rather than skipped at runtime". That sentence is in a file a contract author is never sent to, which is the whole of the problem; venue's own comment block shows that when an author does think about it, the decision gets written down properly.

The run-time rule is already good: announce the boundary, log the verdict, mark the phase line. Its weakness is reach rather than homelessness. The router that walks the list cites `ref/08-stage-gate.md` by name at its Step 3, naming the Phase Transition Contract specifically, and the CHECK worker cites it twice. DRAFT, PROBE and REVISE cite it nowhere, and each writes its own `[PHASE]` entry regardless, which means the rule is being obeyed by convergence rather than by contract.

### What per-unit does to all of this
For a per-unit stage the phase list runs once per unit, and the router says that much out loud at its Step 4. What follows from it and is nowhere stated is that both kinds of skip become per-unit too: a section that needs no probe, a display asset already revised. `5-section-edit` is the only contract that declares `runs: per-unit`, so it is the stage where this comes up first.

## Items to Finish
- [x] 📐 Declared per stage, and the list ends with `check`
      Re-checked all eight `stages/*/stage.md` on 260727: eight `phases:` lists, eight ending with `check`, eight `gates: [check]`. `stages/CONTRACT.md:29` states ends-with-`check` as the field's only constraint.
- [x] 📐 A run-time skip must be announced and logged
      `ref/08-stage-gate.md:91-93`, Phase Transition Contract rule 2: one reply line with the reason, `[PROBE] skipped -- <reason>` in the S page's `## Log`, and `--` on the phase line.
- [x] 📐 A shorter declared list is legal, and venue says why
      Ruled in three places, so the 🧠 this face carried was already answered on disk: `stages/CONTRACT.md:29`, the router's Step 4 ("`phases:` is a LIST, not a type ... never pad a list to four"), and `stages/2a-venue/stage.md:13-21`, nine lines of comment saying venue produces a contract rather than prose.
- [ ] 🔍 Assert one `[PHASE]` line per declared phase
      In `2-phase/3-check/haipipe-paper-check/checks.sh`, which already takes `--stage-page <file>`, reads that S page's `## Log`, and ❌-fails a `[REVISE]` entry carrying no `workers:` line. Extend it: read `phases:` from the stage's `stage.md`, require one `[PHASE]` entry per declared name or a `[PHASE] skipped -- <reason>`. This is the assertion that would have caught the silent seed run.
- [ ] 🔧 Cite the Phase Transition Contract in three worker skills
      `haipipe-paper-draft`, `-probe` and `-revise` SKILL.md contain zero references to `ref/08-stage-gate.md`, though each writes its own `[PHASE]` entry (draft:246, probe:121, revise:25). The router (`haipipe-paper-stage/SKILL.md:69`) and CHECK (`haipipe-paper-check/SKILL.md:87,292`) already cite it, so this is three missing pointers, not a homeless rule.
- [ ] 📐 Separate the two skips in the vocabulary
      `ref/08-stage-gate.md:93` already draws the line in one sentence: a phase absent from `phases:` is "omitted by contract rather than skipped at runtime". Put that distinction on `stages/CONTRACT.md:29`, next to the `phases:` field a contract author is actually reading, and give the declared kind its own word.
- [ ] 📐 State what a skip means for a per-unit stage
      The router's Step 4 says the whole list runs once per unit; nothing extends that to a skip. `stages/5-section-edit/stage.md:29` is the only `runs: per-unit` contract, so it meets this first.

## Where we are
The dispatch works and is uniform across all eight stages. The invariant holds: every list ends with `check`, and every stage declares its gates the same way it declares its phases.

What is open is no longer a ruling. Re-checking this face on 260727 found the short-list question already answered in three files, so what remains is one mechanical assertion nobody has written, three worker skills with no pointer to the rule that binds them, and two decisions that are made but recorded where a contract author will not meet them.

## Files
- `haipipe-paper-stage/SKILL.md`
  Step 4: drive the declared phases, each through its own `Skill()` dispatch.
- `stages/2a-venue/stage.md`
  The one contract that declares three phases instead of four.
- `1-lifecycle/ref/08-stage-gate.md`
  The announce-every-boundary rule and the no-silent-skips rule, and the seed run that caused them.

## Law
A stage does not do work; it walks its declared `phases:` in order and dispatches each to its own worker skill. A phase executed inline did not run.

`phases:` is a list, not a type, and it always ends with `check`. `gates:` is declared the same way, and defaults to `[check]`.

No silent skips. A phase may be skipped at run time only by an explicit logged verdict: one reply line with the reason, a `[PHASE] skipped -- <reason>` entry in the owning S page's `## Log`, and `--` on the phase line. "The draft looks fine" is a verdict to record, never a licence to say nothing.

## Discussion
> CC 260727: this face's one 🧠 turned out to be already ruled on disk, in three places, so after this pass nothing on it is undecided and everything left is write-down, check, or pointer work. Under the board's own `state:` contract that reads ✅ RULED, not 🟡. I did not touch the line, because closing a face is JL's act and because there is a real cost to closing it: four open items sit in this queue, one of them the mechanical assertion that would have caught the silent seed run, and a ✅ face gets read less often than a 🟡 one.
> My recommendation is to close it and pay that cost, because the alternative is worse. Leaving 🟡 on a question whose answer is already written in three files is exactly the merge of decision and implementation that board.md unmerged on 260726.

## Log
260726 · Created in the QB restructure, replacing `_archive/QC3-four-phases.md`, which explained what the four phases are. The live question is how they are CALLED and whether one may be left out, which is the thing that has actually gone wrong. Tabulating all eight contracts is what surfaced `2a-venue`'s three-phase list.

260726 · The announce rule turns out to already PRODUCE the evidence a checker would need. Added the assertion that would have caught the silent seed run: one `[PHASE]` line per declared phase, or a logged skip verdict.

260727 · Re-verified every claim on this face against disk, and three of them were wrong. FIRST, the log destination: this page said a skip verdict lands in `_LOG`, and `_LOG_<stage>.md` was RETIRED on 2026-07-26 (`stages/CONTRACT.md:114`, `ref/04-lifecycle-map.md:107`, which records that no live paper ever carried one). The rule has always meant the owning S page's `## Log`, which is what `ref/08-stage-gate.md:86-93` actually says. Corrected in the Diagram, the Content, the Law and the queue, and it matters beyond tidiness: a checker written against the page as it stood would have grepped a file that does not exist. SECOND, "cited by no worker contract" was false in two directions. The stage router, which is the thing that walks the list, cites `ref/08-stage-gate.md` by name at its Step 3 and names the Phase Transition Contract specifically; CHECK cites it twice. Only DRAFT, PROBE and REVISE cite it nowhere, and all three write their `[PHASE]` entry anyway, so the rule is being obeyed by convergence rather than by contract. The 🔧 item was narrowed from moving a homeless rule to adding three missing pointers. THIRD, "nothing says whether a short list is legal" was false: `stages/CONTRACT.md:29` makes ends-with-`check` the only constraint, the router says "never pad a list to four", and `2a-venue/stage.md:13-21` spends nine lines of comment on its own reason. The 🧠 became an [x], and what survives is the narrower and much cheaper gap: venue states its own rationale and no file states a test the next contract author could apply. The same correction reached the per-unit item, where the router does say the list runs per unit and only the skip half is unwritten.

260727 · The 🔍 assertion now names its home. `2-phase/3-check/haipipe-paper-check/checks.sh` already accepts `--stage-page <file>`, already opens that S page's `## Log`, and already ❌-fails a `[REVISE]` entry with no `workers:` line. Requiring one `[PHASE]` entry per declared phase is an extension of a hook that exists rather than a new checker, which is what makes this the cheapest unwritten check in the group.
