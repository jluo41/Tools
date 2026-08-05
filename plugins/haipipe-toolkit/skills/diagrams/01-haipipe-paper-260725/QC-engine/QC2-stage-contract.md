# What a stage is, and what it takes to make one work
state: 🟡 PARTIAL
owner: JL
method: draw one stage whole, give every part a reader and a ruling face, and treat a field nobody reads as decoration

## Opening
What is a stage, considered on its own?
Not which stages this skill happens to have, and not why the lifecycle is cut where it is cut: those belong to `QA6`, which owns what a paper contains. This face is about the OBJECT. One stage, drawn whole, so that every other face in this group can be read as a ruling about one of its parts.

A stage is not an object anywhere in the code. Nothing constructs one. A router reads a small index, loads exactly one file, and acts on its fields, so a stage IS its `stage.md` frontmatter: twenty-four required fields in seven blocks, plus a conditional set. That is worth saying plainly because it decides what a ruling on this board means. Settling a grain question is a change to `runs:`. Settling a spending ceiling is a change to `probe_depth:`. A face here that cannot name the field it would change has not finished its work.

Making one work is therefore a concrete question about those fields, and specifically about who reads each one. There are exactly three readers. The ROUTER picks which stage is meant. The CREATOR makes its page. The EXECUTOR does the work. Only the first two are programs: `../../paper/haipipe-paper-stage/stages/index.yml` gives the router five fields, and `create-page.py` reads eleven contract fields, of which eight belong to the required twenty-four. The other sixteen required fields are read by an agent, as prose.

That asymmetry is the whole of this face, because it is where a stage half-works. A field a program reads fails loudly, at run time, in front of somebody. A field an agent reads fails silently, and the symptom arrives later as prose nobody can trace back. Every defect measured across the live contracts sits in the silent group and not one sits in the loud one: a `runs:` that does not match the shape of the work, twenty-two declared paths resolving to nothing, five templates naming a retired filename, ten done-criteria with no machine check, a stage-specific field census in `../../paper/haipipe-paper-stage/stages/CONTRACT.md` that no longer reproduces.

This is the first face of the group because every other one rules a part of the object drawn here. `QC3b` can only say which page a stage writes once it is settled that the BOARD block is what addresses it. `QC4` can only ask whether a phase may be skipped once `phases:` is known to be a list rather than a type. A reader who cannot see the stage whole cannot tell which face they want.

Scope: This page covers What a stage is made of, which of the three readers consumes each block, where every part lives on disk, the one-way chain from contract to PDF, and which face of this group rules each link in it. Neighbouring pages cover WHICH stages this skill has, what each one asks, and what sits outside them is `QA6`. Every block in the diagram names its own face.

## Diagram
```
   ONE STAGE, WHOLE. Every part names the face that rules it.
   There is no stage object in the code: a stage IS this frontmatter.

   ┌──────────────────────────────────────────────────────────────────┐
   │ IDENTITY     key · order · title                                 │
   │              one_line     THE one question it answers            │
   ├──────────────────────────────────────────────────────────────────┤
   │ BOARD        board_family · board_unit · board_slug     → QC3b    │
   │              which S page it writes, and who names it            │
   │              ⚠️ the folder is named for the FAMILY, not the stage │
   ├──────────────────────────────────────────────────────────────────┤
   │ EXECUTION    phases  a LIST, always ending `check`      → QC4    │
   │              gates · runs · needs_paper                          │
   │              probe_depth  the spending ceiling          → QC4b    │
   ├──────────────────────────────────────────────────────────────────┤
   │ PRODUCT      template   the shape DRAFT fills           → QC3a    │
   │              artifact   the S page, and it IS the paper → QC3d    │
   │              output     generated, one way, never back  → QC3d    │
   │              sections · formatting                               │
   ├──────────────────────────────────────────────────────────────────┤
   │ EVIDENCE     probes · q_id_pattern · q_anchor           → QC4b    │
   ├──────────────────────────────────────────────────────────────────┤
   │ GRAPH        upstream · downstream · handoff                     │
   │              ⚠️ ADVISORY. The binding dependency is the S page's  │
   │                 own `requires:`, which carries live gate state.  │
   ├──────────────────────────────────────────────────────────────────┤
   │ CLOSING      done_criteria · closed_when · exit_when    → QC4d   │
   ├──────────────────────────────────────────────────────────────────┤
   │ conditional  runs · unit · units · units_from           → QC3b    │
   │              venue_aligned | venue_role                 → QC3b    │
   │              artifact_fallback · blocked_on             → QC3b    │
   └──────────────────────────────────────────────────────────────────┘

   the same object, in the order it is USED, and that IS this group:

      DECLARED    ▸ QC2 the fields
                    QC3b how it varies · QC3a its template
      ADDRESSED   ▸ QC3b which page · QC3c the second run
                    QC3d what it writes vs what is generated
      RUN         ▸ QC4 the phase list
                    └ QC4a DRAFT · QC4b PROBE · QC4c REVISE · QC4d CHECK

   ── WHO READS IT: three readers, and only two are programs ────────
   ┌─────────────────┬───────────────────────────┬───────────────────┐
   │ ① THE ROUTER    │ stages/index.yml          │  5 fields         │
   │   which stage   │ key order dir triggers    │  EVERY invocation │
   │   is meant      │ migrated                  │  fails 🔊 LOUD    │
   ├─────────────────┼───────────────────────────┼───────────────────┤
   │ ② THE CREATOR   │ create-page.py            │  8 of the 24      │
   │   make its page │ key title one_line        │  once per page    │
   │                 │ board_family board_unit   │  fails 🔊 LOUD    │
   │                 │ template artifact         │                   │
   │                 │ q_id_pattern              │                   │
   │                 │ + board_slug              │  3 more, OUTSIDE  │
   │                 │   venue_contract          │  the required 24  │
   │                 │   fallback_template       │                   │
   ├─────────────────┼───────────────────────────┼───────────────────┤
   │ ③ THE EXECUTOR  │ an AGENT reading the      │ 16 fields         │
   │   do the work   │ contract as prose         │  every phase      │
   │                 │ everything else           │  fails 🔇 SILENT  │
   └─────────────────┴───────────────────────────┴───────────────────┘

   ── and every measured defect is in ③ ─────────────────────────────
      a `runs:` that does not match the shape of the work
      22 of 31 declared paths resolving to nothing
      3 of 8 templates pointing a drafter at `artifact_fallback:`
      rather than at `artifact:` (2 more are correct, 3 have no such line)
      10 done_criteria with no machine check, on the stage that has them
      36 stage-specific fields in use where CONTRACT.md still says 43
      ⚠️ not one defect in ① or ②. Those REFUSE a malformed contract:
         no template, an artifact outside the lifecycle directory, a
         non-literal family. The refusals are the design working.

   ── declaring a stage: four files, and nothing else ───────────────
      1  stages/index.yml       + ONE ROW, read on EVERY invocation
      2  stages/<order>-<key>/  + ONE FOLDER
      3    stage.md               the 24 fields above
      4    template.md            the shape DRAFT fills        → QC3a
      ✅ no new skill · no version bump · no router edit
      📍 the whole procedure is SKILL.md:230, and it names 2 of the 4.
```

```
   WHERE THE PARTS LIVE ON DISK, AND WHAT FLOWS BETWEEN THEM.
   Four homes, and exactly one direction through them.

   ① THE SKILL · reusable, ships, never mentions a paper ────────────
      skills/paper/haipipe-paper-stage/
        SKILL.md              the router: resolve ▸ create ▸ walk phases
        stages/index.yml      reader ① reads THIS, on every invocation
        stages/CONTRACT.md    the 24 fields, measured across all eight
        stages/section-kinds.yml   which section kinds exist, per outlet
        stages/<order>-<key>/
          stage.md            ◀ THE CONTRACT. the stage IS this file.
          template.md         ◀ the GENERIC template, and see below
        create-page.py        reader ②
        check-contracts.py    resolves every declared path

   ② THE VENUE PACK · reusable, CONSULTED, never in the chain ───────
      skills/paper/venue/              504 files · 245 md · 254 pdf
        playbook-<family>/<VENUE>/
          taste.md
          <VENUE>-<kind>/template.md   ◀ the VENUE template
          <VENUE>-<kind>/style.md        the deep dive, reference only
          examples/*.pdf                 real published papers
      📌 a git submodule, PINNED BY COMMIT on the venue S page, with
         the drift diff recorded there when the pin moves.

   ── SO A TEMPLATE HAS TWO SOURCES, AND AN ORDER ──────────────────
      the venue pack has a template for this (venue, kind)
                                            ──▶ USE IT · authoritative
      no pack template, or a pack-less venue (grant · patent · NEJM)
                                            ──▶ FALL BACK to
                                 stages/5-section-edit/template.md
      ⚠️ and the order is NOT re-run per section. The VENUE stage
         resolves every path ONCE and writes them onto the S page:
           "### Section Styles (RESOLVED here -- downstream reads
            these rows, never re-derives)"
         a template path is therefore EVIDENCE ON A PAGE, not a
         lookup, which is why a stale pin is visible.        → QC3a

   ⑧ THE BOARD · one paper's control plane ─────────────────────────
      Paper-X/0-lifecycle/<family folder>/
        S-<Family>-<unit>-<slug>.md   ◀ THE RESULT. every stage
                                        writes exactly one of these.
          ## Content   the prose. THIS IS THE PAPER.         → QC3d
          state:       the gate                              → QC4d
          ## Log       the Gate Ledger                       → QC4d
          requires:    the BINDING dependency, not `upstream:`
        board.md · board/ site  built by ③ /haipipe-board    → QC3b

   ⑦ THE DELIVERABLE · the same paper, unnumbered ──────────────────
      Paper-X/
        sections/*.tex        GENERATED from the 4-main pages  → QC3d
        appendices/*.tex      GENERATED from the 5-appendix pages
        displays/<unit>/      float.tex + assets/
        <paper>.tex  <paper>.bib  <paper>.pdf
        <venue>.cls  <venue>.bst   ◀ copied out of the venue pack

   ── THE ONE-WAY CHAIN, END TO END ────────────────────────────────

     stage.md ──┐
     template ──┼─▶ DRAFT ─▶ S page ─▶ sections/ ─▶ <paper>.tex ─▶ .pdf
     venue pack ┘             ## Content   *.tex
                   ▲             ▲            ▲                     ▲
                 QC3a QC4a      QC3c QC4      ⚠️ NO PROGRAM        compile
                              QC4b QC4c        DOES THIS STEP
                              QC4d

     ⛔ nothing reads back. Not tex ▸ md. Not pdf ▸ anything.
     ⚠️ and the md ▸ tex step has NO SCRIPT anywhere in the family.
        An AGENT writes the .tex. That is exactly why QC3d's round-trip
        parity test has never been run: there is no generator to diff
        against, only a rule.

   ── AND WORD? IT DOES NOT EXIST ──────────────────────────────────
      no pandoc, no python-docx, no converter in any `.py` or `.sh`
      in the whole family. Word is a PROPOSED projection on `QBe3 §4`, and the many-consumer rule is `QC3@display`
      and nothing more. Its adapter diagram is a design, not a
      shipped path, and the same is true of HTML except for the
      board's own rendering.
```

```
   APPLYING THE READER MODEL TO ALL TEN FACES. Three shapes fall out,
   and the third one was not visible until they were laid side by side.

   🔊 LOUD, whole block · a program reads it end to end
      QC3b  board_family · board_unit · board_slug · artifact
           refuses a missing family, a non-literal family, an artifact
           outside the lifecycle dir, two faces resolving one unit.
      ⇒ and QC3b is the ONLY face in the group that reached ✅.
        Loud enforcement is not incidental there; it is the cause.

   ⚡ SPLIT · the PATH is loud, the CONTENT is silent
      QC3a  `template:` resolves or raises · the file's prose does not
      QC3d  `artifact:` resolves or raises · `output:` describes a step
                                             nothing performs
      ⇒ this is the shape that produced the three misdirected `Fill` lines.
        The path resolved, so nothing raised, while the content told
        a drafter to write into a filename retired months ago.

   🔇 SILENT · reader ③, an agent reading prose
      QC3b  runs · venue_aligned · unit · units · units_from
      QC4  phases · gates
      QC4a  q_anchor · q_id_pattern · the placeholder grammar
      QC4b  probe_depth
      QC4d gates · done_criteria · closed_when · exit_when
      ⚖️ and QC4d is the one where silent is mostly CORRECT: 66 of its
         73 criteria are judgments and should stay judgments. There
         the answer is "a human at a named moment", and CHECK already
         is that moment.

   ⛔ NO FIELD AT ALL · nothing to read, so nothing to enforce
      QC3c   the second run
      QC4c  REVISE's `place`-first and why-comment rules
      ⇒ THE FINDING. These are the two faces whose rules are scattered
        across six files and three worker contracts respectively, and
        that is not a coincidence. A behaviour with no field has
        nowhere to be declared, so it gets patched wherever somebody
        was burned, and each patch is invisible to the next author.
        Give it a field first; the checker is the easy part.

   ── and FOUR of the ten are cheaply checkable TODAY ───────────────
      QC3b  a stage declaring `units:` must declare `runs: per-unit`
      QC4  one `[PHASE]` line in the S page's `## Log` per declared
           phase, or a logged skip verdict. Evidence already produced.
      QC4a  `\\cite{TOADD}` or `{VAL:?}` with no `[Q-…]` beside it.
           One regex. The grammar was designed to be greppable.
      QC4c every `%% {CC-<tag>}` names a DECLARED revise worker.
           NOT one comment per change: `-place/SKILL.md:94` exempts a
           pure `TOADD → \citep{key}` swap, so a per-change count
           would fail on every correct run. This one already fails:
           17 comments under six tags, three of which name DRAFT
           finders, and `place` has left zero.
      ⚠️ none of the four is written. Each is one assertion.
```

## Content
### A stage is its frontmatter
Nothing in the code constructs a stage. `../../paper/haipipe-paper-stage/stages/index.yml` is read on every invocation, including ones that turn out to be about something else, so it holds only what is needed to RESOLVE which stage is meant. The chosen `stage.md` is loaded only then, and it holds everything else. That difference in read rate is the entire constraint on what may live where, and it is why the index has stayed readable while the contracts grew to twenty-four required fields and forty-three stage-specific ones.

The practical consequence is that this group argues about fields rather than about ideas. Every face below names the block it would change, and a face that cannot has not finished.

### The three readers, and why only the third one hurts
`①` and `②` are programs, so their fields are load-bearing in the ordinary sense: get one wrong and something raises. `create-page.py` refuses a contract with no `template`, refuses an `artifact` that does not name a lifecycle directory, and refuses a `board_family` that is not a literal.

`③` is an agent reading prose and it has no refusal at all. A wrong `probe_depth` does not raise; it changes what gets commissioned. A wrong `runs` does not raise; it produces a gate nobody can answer. A `done_criteria` list that cannot be checked does not raise; it produces a gate somebody passes anyway. So sixteen twenty-fourths of every contract is enforced by attention, and attention is exactly what a lifecycle of unattended phases is trying not to spend.

### What "make one stage work" means
It means closing the gap for the silent sixteen, and there are only three ways to close it. Move the field to a program, which is what `../../paper/haipipe-paper-stage/check-contracts.py` did for every declared path. Move it to a human at a moment they are already looking, which is what `done_criteria` does at CHECK. Or delete it, which is what happened to `log:` and `inputs:`.

A field that is none of those three is decoration that looks like a contract, and decoration is worse than absence, because a reader trusts it.

Automation is not the answer to all of it, and that should be said plainly. Two of the seven blocks will never be programs: `done_criteria` is mostly judgments and mostly should be. The answer there is honesty about which fields bind, not more checking.

### The block that declares the same thing twice
`upstream`, `downstream` and `handoff` describe which stages feed this one and what it passes on. None of them binds. The authoritative dependency is the S page's own `requires:`, because that one carries the upstream page's live gate state and cannot go stale.

So the GRAPH block is orientation for a person, sitting in the same frontmatter, in the same syntax, as the fields that decide behaviour. Nothing in the file's shape tells a reader which is which, and a reader has no reason to guess correctly. This is the sharpest instance of the general problem and the cheapest one to fix.

### Declaring something new on a stage
```
 a new lifecycle step                 →  index.yml row + folder + 2 files
 a new thing the stage PRODUCES       →  PRODUCT block         → QC3a QC3d
 a new thing it must ASK for          →  EVIDENCE block        → QC4b
 a new condition for being DONE       →  CLOSING block         → QC4d
 a new way it VARIES per paper/venue  →  the conditional block → QC3b
 a path that cannot resolve yet       →  `blocked_on: <Q page>` beside it
 a fact only a human needs            →  the craft prose BELOW the
                                         frontmatter, never a field
```

## Aims
- [x] 📐 State the fields by measurement rather than by inference
      `../../paper/haipipe-paper-stage/stages/CONTRACT.md` names 24 required fields in 7 blocks, and all eight `stage.md` files carry all 24, checked field by field. `../../paper/haipipe-paper-stage/check-contracts.py`'s `REQUIRED` list is the same 24, so the document and the checker cannot disagree.
- [x] 📐 Declaring a stage costs four files and no more
      One `../../paper/haipipe-paper-stage/stages/index.yml` row, one `stages/<order>-<key>/` folder, its `stage.md`, its `template.md`. No new skill, no version bump, no router edit.
- [x] 🔧 Move every declared PATH into a program
      `../../paper/haipipe-paper-stage/check-contracts.py` resolves them all; 22 of 31 were dead the first time it ran. The eight contracts declare 28 such paths today, and exactly one carries `blocked_on:`, at `4-display/stage.md:30`.
- [x] 🔍 Classify every face in this group by reader
      Done 260726 across `QC3b`-`QC4d`. Four shapes: loud whole-block (`QC3b` only), split path-loud content-silent (`QC3a`, `QC3d`), silent (`QC3b`, `QC4`, `QC4a`, `QC4b`, `QC4d`), and no field at all (`QC3c`, `QC4c`).
- [x] 🔧 Correct the reader counts this face was built on
      260727, read off `create-page.py`: it reads 11 contract fields over 10 `values.get()` call sites, not 7. Eight are in the required 24 (`key title one_line board_family board_unit template artifact q_id_pattern`); `board_slug`, `venue_contract` and `fallback_template` sit outside it. The silent share is therefore 16 of 24, not 17.
- [~] ↪ MOVED to `QC3c` and `QC4c` · the field a field-less behaviour needs
      The finding stays here, because it came out of laying the ten faces side by side: a behaviour with no field has nowhere to be declared. The ruling is theirs. Neither the re-run nor REVISE's why-comment rule appears among the 71 distinct top-level frontmatter keys the eight contracts use, and `QC3c` already offers Ⓐ-Ⓓ for the first while `QC4c` asks whether `place`-first belongs in the contract at all.
- [ ] 🧠 Give every silent required field a named reader
      The 16 are `order phases gates probe_depth runs needs_paper sections formatting probes q_anchor upstream downstream handoff done_criteria closed_when exit_when`. Each must end up checked by a program, read by a human at a named moment, or deleted. Two live ways to get there: rule all 16 one at a time, or rule the three GRAPH fields below and declare the remaining 13 craft prose by default. `order:` is the free one: it is copied from the `../../paper/haipipe-paper-stage/stages/index.yml` row and nothing reads it out of `stage.md`.
- [ ] 📐 Mark the advisory fields advisory in the file itself
      `upstream`, `downstream` and `handoff` do not bind, `../../paper/haipipe-paper-stage/stages/CONTRACT.md` already says so in prose, and all eight contracts still carry them in the same syntax as the fields that decide behaviour. The decision is made, so write it 24 times: one inline comment beside each of the three fields in each of the eight `stage.md` files.
- [ ] 🔧 Recount the stage-specific field census in `../../paper/haipipe-paper-stage/stages/CONTRACT.md`
      It says "Forty-three such fields are in use today across the eight contracts". Counting top-level frontmatter keys gives 71 distinct, of which 36 are neither in the required 24 nor in the conditional block. Either state the counting rule or fix the number, because the measurement argument this whole face rests on currently fails to reproduce on its own headline figure.
- [ ] 🔍 Give the four cheap assertions a host script
      `QC3b`, `QC4`, `QC4a` and `QC4c` each own one unwritten one-line assertion. What none of them can own is where it RUNS: `../../paper/haipipe-paper-stage/check-contracts.py` reads contract form and declared paths only, and the whole paper family holds 2 `.py` and 5 `.sh` files, none of which reads an S page's `## Log` or greps a placeholder. Name the host before four faces each invent their own. Note where the evidence actually is: `log:` and its `_LOG_<stage>.md` were retired 2026-07-26 and no live paper ever carried one, so a phase entry lands in the owning S page's `## Log` per `ref/08-stage-gate.md:86-93`. Where CONTRACT-FORM checking lives is `QF2`'s open ruling, not this one.
- [ ] 📐 Put the declaration procedure where an author looks
      Four files, seven blocks, three readers, in one place. Today it is `SKILL.md:230`, one line that names a folder and an index row and never mentions `stage.md` or `template.md`, plus a field list in `../../paper/haipipe-paper-stage/stages/CONTRACT.md` that never states the procedure.
- [ ] 🧪 Write a ninth contract from the documentation alone
      Author `stages/9-<key>/stage.md` and its `template.md` from `../../paper/haipipe-paper-stage/stages/CONTRACT.md` and `SKILL.md:230` only, run `../../paper/haipipe-paper-stage/check-contracts.py`, and count what it rejects. This tests the CONTRACT; `QF3` tests running an existing stage and `QC3a` tests the template alone, so the three do not overlap.

## States
The object is measured rather than inferred, and the loud half is in good shape. The router and the creator both refuse malformed contracts, and every declared path now either resolves or carries `blocked_on:` with a reason.

The silent half is the work, and it is what the rest of this group is for. Seventeen of twenty-four required fields are read by an agent as prose, every measured defect sits among them, and two of the three blocks involved will never become programs. So the remaining question is not how to check more; it is how to stop an advisory field from looking binding.

## Files
- `../../paper/haipipe-paper-stage/stages/CONTRACT.md`
  The required core, measured across all eight, plus the conditional and retired fields.
- `../../paper/haipipe-paper-stage/stages/index.yml`
  Reader `①`. Its header states why it must stay small: it is read on every invocation.
- `create-page.py`
  Reader `②`. Eleven contract fields over ten `values.get()` call sites, and seventeen `raise SystemExit` refusals.
- `../../paper/haipipe-paper-stage/check-contracts.py`
  The one thing that has moved a field out of the silent group.
- `haipipe-paper-stage/SKILL.md`
  Line 230 is the entire current declaration procedure, and it names one folder and one index row rather than four files.
- `../../paper/haipipe-paper-stage/stages/section-kinds.yml`
  The closed set of section kinds, measured per outlet; what `section_kind:` may be.
- `venue/`
  The second template source: 504 files, `playbook-<family>/<VENUE>/<VENUE>-<kind>/template.md`. A pinned submodule, consulted and never in the chain of command.
- `0-lifecycle/2-venue/S-Venue-0-venue.md`
  Where the venue resolution is STORED, in the `Section Styles` table, alongside the pack's pinned commit and its drift diff.

## Law

- A stage is not an object. It IS its `stage.md` frontmatter: twenty-four required fields in seven blocks, plus a conditional set. A ruling on this board is a change to a named field, and a face that cannot name the field it would change has not finished its work.
- Every field answers to a named reader. The ROUTER reads `../../paper/haipipe-paper-stage/stages/index.yml` on every invocation, so that file holds only what is needed to CHOOSE. The CREATOR reads eleven contract fields to make the page, eight of them from the required twenty-four. The EXECUTOR reads the remaining sixteen, as prose, and cannot refuse anything.
- A field must be checked by a program, read by a human at a named moment, or deleted. A field that is none of the three is decoration that looks like a contract, and a reader will trust it.
- `upstream`, `downstream` and `handoff` are craft orientation and do not bind. The authoritative dependency is the S page's own `requires:`, because it carries the upstream page's live gate state and cannot go stale.
- Declaring a stage costs four files and nothing else: one row in `../../paper/haipipe-paper-stage/stages/index.yml`, one folder at `stages/<order>-<key>/`, its `stage.md`, its `template.md`. No new skill, no version bump, no router edit.
- A declared path that cannot resolve carries `blocked_on: <Q page>` with the reason. A dangling path with no `blocked_on` is a defect, and nothing may report it as green.

## Discussion
> CC 260727: the sixteen silent fields do not need sixteen rulings, and I would not spend them that way. Three of the sixteen are the GRAPH block, which the Law already declares advisory, so ruling those three closes the sharpest instance and costs one inline comment repeated 24 times. My recommendation is to rule GRAPH now and declare the remaining thirteen craft prose by default, with the burden on any future author who wants one to BIND.
> The cost is honest: "craft prose by default" means `probe_depth`, `runs` and `needs_paper` stay unenforced even though a wrong value in any of the three changes what a run spends or produces. That is thirteen fields a reader will keep trusting. The alternative, sixteen separate rulings, is more correct and will not finish, and an unfinished census is what produced the 43-versus-36 mismatch in the queue above.
> One of the sixteen is already being argued on its own face: `QC4b` applies this face's Law to `probe_depth` and asks whether a field all eight contracts set to the identical 0 is decoration. If JL rules that one, the field-by-field route stops being hypothetical and the two threads should be answered together.

> CC 260727: `gate_mode` is not a field. It appears zero times in `skills/paper/` and `skills/board/`, and the two files that were said to disagree about it now agree: `1-lifecycle/ref/08-stage-gate.md:10` says mode is an invocation or session choice, "it is not Board frontmatter", recorded in the owning S page's `## Log`, and `2-phase/3-check/haipipe-paper-check/SKILL.md:85` says the same thing and cites the first as owner. I removed it from this face's defect list. `QC4d` still carries the stale claim in its opening, its `## Where we are`, and an open item, and I am not editing that face; it needs a pass, and its `state:` may improve when it gets one.
> The cost of leaving it: whoever reads `QC4d` next will go looking for a field that does not exist, which is exactly the cost this face's Law says a decorative field imposes.

## Log
260726 · Rewritten three times in one day, and the third time was the premise. It began as "what IS a stage", answered descriptively. It became a gatekeeping question about refusing a ninth stage. JL corrected that: adding stages is open, and the work is making ONE stage run well. It was rebuilt in `QA1`'s style around 24 fields, 7 blocks and 3 readers, which produced the finding that `create-page.py` reads exactly seven fields while an agent reads seventeen, and that every measured defect sits in the seventeen. JL then corrected the SCOPE: which stages this skill has, what each asks, and what sits outside them are `QA6`'s, not this group's. The eight-question table, the resource-versus-claims example and the outside-the-eight list left this face; what stayed is the object, and the map of which face rules each of its parts.

260726 · JL asked the Diagram to say WHERE the parts live and how they relate. Added a second block: the four homes (the skill, the venue pack, the board, the deliverable), the two template sources with their resolution order, and the one-way chain from contract to PDF. Two things surfaced while drawing it. The venue resolution is STORED on the venue S page rather than recomputed, so a template path is evidence rather than a lookup. And the md-to-tex step has no program at all, which is a stronger statement than `QC3d` had been making.

260726 · Move 1 of the QB plan: the reader model applied to all ten sibling faces, each now declaring which reader consumes its block, whether it fails loud or silent, and what would make it loud. Laying the ten side by side produced a shape nobody had seen: two faces, `QC3c` and `QC4c`, have NO contract field at all, and those are exactly the two whose rules are scattered across six files and three worker contracts. A behaviour with no field has nowhere to be declared. It also surfaced four assertions that are cheap today and unwritten.

260727 · A verification pass corrected the numbers this face is built on. `create-page.py` reads eleven contract fields over ten `values.get()` call sites, not seven: the seven named here missed `q_id_pattern`, which is in the required twenty-four, and `board_slug`, `venue_contract` and `fallback_template`, which are not. Eight of the twenty-four are therefore read by a program and sixteen by an agent, so the Question, the reader table, the Content and the Law all moved from 7/17 to 8/16. Three further repairs. `gate_mode` left the defect list, because it is not a field anywhere in `skills/paper/` or `skills/board/` and its two supposed homes now say the same thing. The declaration procedure is `SKILL.md:230`, not `:193`. And the defect that replaced `gate_mode` is a real one found while counting: `../../paper/haipipe-paper-stage/stages/CONTRACT.md` claims forty-three stage-specific fields where the eight contracts carry thirty-six. The Items queue was then regrounded on counts read off disk (28 declared paths with one `blocked_on:`, 71 distinct top-level frontmatter keys, 8 `stage.md` files, 2 `.py` and 5 `.sh` files in the family), the aggregate assertion item was narrowed to the one thing no sibling can own, which is where those assertions would RUN, and the field-for-a-field-less-behaviour item became a pointer to `QC3c` and `QC4c`, which already carry that ruling with its options.

260727 · One more stale target, caught from the main session and verified. This face said the cheap `QC4` assertion would count `[PHASE]` lines in `_LOG`. There is no `_LOG`. The `log:` field was retired 2026-07-26 precisely because it declared `_LOG_<stage>.md` on all eight stages and no live paper ever carried one, per `stages/CONTRACT.md:114` and `ref/04-lifecycle-map.md:107`, and the phase entry has always landed in the owning S page's `## Log`, per `ref/08-stage-gate.md:86-93`. Both mentions on this face now name the S page. This one is worth recording rather than quietly fixing, because it is the exact failure the Law describes from the other direction: an assertion written against the retired wording would have grepped a file that does not exist, reported nothing, and passed. `QC4` was corrected in the same pass; `QC4b` still names `_LOG` as the destination in two prose lines and is not this face's to edit.

260727 · Three counts corrected after two subagents disagreed and I remeasured. The `Fill` line defect is 3 of 8, not 5: `1a-resource` and `2a-venue` were already repaired and match their `artifact:`, while `0-seed`, `1b-claims` and `2b-pitch` point at their own `artifact_fallback:`, which is a real file for a paper predating the S-face restructure and the wrong target for a new page. So none is dangling and three are misdirected, which is a smaller and more precise defect than this face had claimed. The silent-field count also settled at sixteen rather than seventeen, because `create-page.py` reads `q_id_pattern` and that field is inside the required 24.

260727 · Corrected the fourth cheap assertion after the QC4c pass disproved it. This face had claimed a REVISE run should leave one `%% {CC-*}:` comment per changed region. The shipped rule is NON-TRIVIAL changes only, and `2-phase/2-revise/haipipe-paper-revise-place/SKILL.md:94` exempts a pure `TOADD` to `\citep{key}` swap outright, so a per-change count would fail on every correct `place` run. The assertion that does hold is that every `%% {CC-<tag>}` names a declared revise worker, and it already fails on the live paper. `gate_mode` was also removed from the defect list earlier in the same pass: the field does not exist.
